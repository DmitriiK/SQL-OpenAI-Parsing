
from typing import List
from modules.data_classes import SQL_Object, DCS_Type, DB_Object_Type, SP_DCSs
from .sql_modules.sql_engine import SQL_Executor
from .llm_communicator import LLMCommunicator
from .sql_modules.sql_string_helper import sql_objs_are_eq


sx = SQL_Executor()
sx.close_connection_finally = False
llm = LLMCommunicator()


def build_data_flow_graph(table_name: str) -> List[SP_DCSs]:
    """To collect all stored procedures and tables, that participate as upstream source of data flow for some table

    Args:
        table_name (str): _description_
        ret_chain (List[SP_DCSs], optional): _description_. Defaults to None.

    Returns:
        List[SP_DCSs]: _description_
    """
    ret_chain, target_tables = [], []

    def traverse_dependencies(table_name: str):
        target_tables.append(table_name) # need to track tables already passed to on prev leevels to avoid eternal loop
        depending_sps = sx.get_depending(table_name, DB_Object_Type.SQL_STORED_PROCEDURE)
        for dsp in depending_sps:
            parsed_before = [x for x in ret_chain if sql_objs_are_eq(x.sp_name, dsp.name)]  # TODO compare by full name
            # we can already have necessary instanse for this sp in prev iteration
            if parsed_before:
                sp_stms = parsed_before[0]
            else:
                defn = sx.get_module_def(dsp.full_name)
                sp_stms = llm.request_and_parse(defn)
            data_inp_stms = [stm for stm in sp_stms.DCSs
                             if sql_objs_are_eq(stm.target_table, table_name)
                             and stm.source_tables]
            # filtered out the statements where our table is target for data read
            if data_inp_stms:
                ret_chain.append(sp_stms)
                for stm in data_inp_stms:  # TODO consider data flow chains inside SP
                    src_tbls = [t for t in stm.source_tables
                                if t.endswith('_tbl')
                                and not any(sql_objs_are_eq(t, tt) for tt in target_tables)]
                    # TODO ret rid on relying on naming conv
                    for vw in (t for t in stm.source_tables if t.endswith('_vw')):
                        vw_tbls = sx.get_dependent(vw) # TODO consider recursive relations in views
                        src_tbls.extend(vw_tbls)
                    for src_tbl in src_tbls:
                        traverse_dependencies(src_tbl)

    traverse_dependencies(table_name=table_name)
    return ret_chain