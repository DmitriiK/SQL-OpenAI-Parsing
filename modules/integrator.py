
from typing import List
from modules.data_classes import SQL_Object, DCS_Type, DB_Object_Type, SP_DCSs
from .sql_modules.sql_engine import SQL_Executor
from .llm_communicator import LLMCommunicator
from .sql_modules.sql_string_helper import sql_objs_are_eq


sx = SQL_Executor()
llm = LLMCommunicator()

def build_data_flow_graph(table_name: str, ret_chain: List[SP_DCSs] = None) -> List[SP_DCSs]:
    if not ret_chain:
        ret_chain = []
    depending = sx.get_dependent(table_name)
    for d in depending:
        if d.type in {DB_Object_Type.SQL_STORED_PROCEDURE}:
            defn = sx.get_module_def(d.full_name)
            sp = llm.request_and_parse(defn)
            for stm in sp.DCSs:
                if sql_objs_are_eq(stm.target_table, table_name):
                    for srct in stm.source_tables:
                        build_data_flow_graph(srct, ret_chain)
    return ret_chain