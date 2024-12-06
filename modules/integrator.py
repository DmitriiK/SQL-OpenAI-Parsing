
from typing import Iterable

from joblib import Memory

from modules.data_classes import SQL_Object, DCS_Type, DB_Object_Type, SP_DCSs
from .sql_modules.sql_engine import SQL_Executor
from .llm_communicator import LLMCommunicator
from .sql_modules.sql_string_helper import sql_objs_are_eq, get_table_schema_db, shorten_full_name
from .pipeline import export_to_yaml
from .mermaid_diagram import MermaidDiagram


sx = SQL_Executor()
sx.close_connection_finally = False
llm = LLMCommunicator()
mmd = MermaidDiagram()
# Create a joblib memory instance
memory = Memory("./cachedir", verbose=0)


@memory.cache  # just wrapper for caching
def request_and_parse(sql_script: str) -> SP_DCSs:
    return llm.request_and_parse(sql_script)


def build_data_flow_graph(table_name: str) -> Iterable[SP_DCSs]:
    """To collect all stored procedures and tables, 
    that participate as upstream source of data flow for some table.
    taking list of SPs, 
    finding target table as target table in the SP list  of the statements,
    for each of the statements take source tables
    for each of them find SPs, where they are targeted
    if no new SP for SP have been find, recursion stops,  - we are at the top level of data stream

    Args:
        table_name (str): _description_
        ret_chain (List[SP_DCSs], optional): _description_. Defaults to None.

    Returns:
        List[SP_DCSs]: _description_
    """
    ret_chain, target_tables = [], []

    def traverse_dependencies(table_name: str):
        target_tables.append(table_name) # need to track tables already passed to on prev leevels to avoid eternal loop
        tsd = get_table_schema_db(table_name)
        if tsd[2] and tsd[2].lower() == 'indexdata':
            return  # TODO get rid of ugly shit
        depending_sps = sx.get_depending(table_name, DB_Object_Type.SQL_STORED_PROCEDURE)
        for dsp in depending_sps:
            parsed_before = [x for x in ret_chain if sql_objs_are_eq(x.sp_name, dsp.name)]  # TODO compare by full name
            # we can already have necessary instanse for this sp in prev iteration
            if parsed_before:
                sp_stms = parsed_before[0]
            else:
                defn = sx.get_module_def(dsp.full_name)
                sp_stms = request_and_parse(defn)
            data_inp_stms = [stm for stm in sp_stms.DCSs
                             if sql_objs_are_eq(stm.target_table, table_name)
                             and stm.source_tables]
            # filtered out the statements where our table is target for data read
            if data_inp_stms:
                ret_chain.append(sp_stms)
                yield sp_stms
                for stm in data_inp_stms:  # TODO consider data flow chains inside SP

                    trg_node_id = mmd.add_node(node_caption=shorten_full_name(stm.target_table), id_is_caption=False)  #TODO - separate 

                    src_tbls = [t for t in stm.source_tables
                                if t.endswith('_tbl')
                                and not any(sql_objs_are_eq(t, tt) for tt in target_tables)]
                    # TODO ret rid on relying on naming conv
                    for vw in (t for t in stm.source_tables if t.endswith('_vw')):
                        vw_tbls = sx.get_dependent(vw) # TODO consider recursive relations in views
                        for vw_tbl in vw_tbls:
                            src_tbls.append(vw_tbl.full_name)
                    for src_tbl in src_tbls:
                        src_node_id = mmd.add_node(node_caption=shorten_full_name(src_tbl), id_is_caption=False)
                        ec = f'{stm.crud_type}: {shorten_full_name(sp_stms.sp_name)}'
                        mmd.add_edge(target=trg_node_id, source=src_node_id, caption=ec)
                        print(f'{src_tbl}-->{table_name}')

                        yield from traverse_dependencies(src_tbl)

    yield from traverse_dependencies(table_name=table_name)
    mmd_out = mmd.generate_mermaid_code()
    print(mmd_out)


def data_flow_to_yaml(table_name: str, output_folder_path: str) -> int:
    sps = build_data_flow_graph(table_name=table_name)
    cnt = 0
    for sp in sps:
        export_to_yaml(sp, output_folder_path)
        cnt += 1
    return cnt
