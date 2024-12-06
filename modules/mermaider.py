
from typing import Iterable
from itertools import product
from pathlib import Path

from modules.data_classes import SP_DCSs
from modules.sql_modules.sql_string_helper import sql_objs_are_eq
from modules.mermaid_diagram import MermaidDiagram
"""
taking list of SPs, 
finding target table as target table in the SP list  of the statements,
for each of the statements take source tables
for each of them find SPs, where they are targeted
if no new SP for SP have been find, recursion stops,  - we are at the top level of data stream
"""


def build_upstream_chain_from_yaml(dir: str, trg_tbl: str):
    dir = Path(dir)
    sps_stms = [SP_DCSs.from_yaml_file(f) for f in dir.iterdir()]
    cb = chain_builder(sps_stms)
    cb.build_upstream_chain(trg_tbl)
    mmd_out = cb.mmd.generate_mermaid_code()
    print(mmd_out)


class chain_builder:
    def __init__(self, sps_stms: Iterable[SP_DCSs]):
        self.recursion_depth = 0
        self.sps_stms = sps_stms
        self.mmd = MermaidDiagram()

    def build_upstream_chain(self, trg_tbl: str):
        # upsteam_sps = [sp for sp in sps_stms if any(dcs.target_table == table_name for dcs in sp.DCSs)]
        self.recursion_depth += 1
        for sp in self.sps_stms:
            for stm in sp.DCSs:
                if sql_objs_are_eq(stm.target_table, trg_tbl) and stm.source_tables:
                    print(sp.sp_name)
                    trg_node_id = self.mmd.add_node(node_caption=stm.target_table, id_is_caption=False)
                    for st in stm.source_tables:
                        src_node_id = self.mmd.add_node(node_caption=st, id_is_caption=False)
                        self.mmd.add_edge(target=trg_node_id, source=src_node_id,
                                          caption=f'{stm.crud_type}: {sp.sp_name}')
                        print(f'{st}-->{trg_tbl}')
                        self.build_upstream_chain(st)


def _get_sql_object_synonyms_(object_name: str) -> Iterable[str]:
    dot, sb1, sb2, defsch = '.', '[', ']', 'dbo'

    def envsb(s: str) -> str:  # envelope in []
        return f'{sb1}{s}{sb2}'

    if dot not in object_name:
        sns = ['', defsch, envsb(defsch)]
        ons = [object_name, envsb(object_name)]            
    else:
        sn, tn = object_name.split(dot)  # schema name and table/view/whatever name
        if sn == defsch:
            sns = ['', sn, envsb(sn)]
        else:
            sns = [sn, envsb(sn)]
        ons = [tn, envsb(tn)]

    ps = product(sns, ons)
    full_names = {f'{x[0]}.{x[1]}' if x[0] else x[1] for x in ps}
    return full_names
        
            
    
        
        
    
    