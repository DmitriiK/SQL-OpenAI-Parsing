
from typing import List
from modules.data_classes import SQL_Object, DCS_Type, DB_Object_Type, SP_DCSs
from .sql_modules.sql_engine import SQL_Executor
from .llm_communicator import LLMCommunicator
from .sql_modules.sql_string_helper import sql_objs_are_eq


sx = SQL_Executor()
sx.close_connection_finally = False
llm = LLMCommunicator()


def build_data_flow_graph(table_name: str, ret_chain: List[SP_DCSs] = None) -> List[SP_DCSs]:
    """To collect all stored procedures and tables, that participate as upstream source of data flow for some table

    Args:
        table_name (str): _description_
        ret_chain (List[SP_DCSs], optional): _description_. Defaults to None.

    Returns:
        List[SP_DCSs]: _description_
    """
    if not ret_chain:
        ret_chain = []
    depending = sx.get_depending(table_name)
    for d in depending:
        if d.type in {DB_Object_Type.SQL_STORED_PROCEDURE}:
            #  TODO - add filtering by obj type on server level
            defn = sx.get_module_def(d.full_name)
            sp = llm.request_and_parse(defn)
            data_inp_stms = [stm for stm in sp.DCSs  
                             if sql_objs_are_eq(stm.target_table, table_name)
                             and stm.source_tables]
            # if among SQL statments we have ones with our table as data flow target
            if data_inp_stms:
                ret_chain.append(sp)
                for stm in data_inp_stms:  # TODO consider data flow chains inside SP
                    src_tbls = [t for t in stm.source_tables 
                                if t.endswith('_tbl')
                                and not sql_objs_are_eq(t, table_name)]
                    # TODO ret rid on relying on naming conv
                    for vw in (t for t in stm.source_tables if t.endswith('_vw')):
                        vw_tbls = sx.get_dependent(vw) # TODO consider recursive relations in views
                        src_tbls.extend(vw_tbls)
                    for src_tbl in src_tbls:
                        build_data_flow_graph(src_tbl, ret_chain)
    return ret_chain