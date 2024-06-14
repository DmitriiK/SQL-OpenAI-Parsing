
from typing import List, Iterable
from itertools import product
from modules.data_classes import SP_DCSs
"""
taking list of SPs, 
finding target table as target table in the SP list  of the statements,
for each of the statements take source tables
for each of them find SPs, where they are targeted
if no new SP for SP have been find, recursion stops,  - we are at the top level of data stream
"""


def build_upstream_chain_from_yaml(files: List[str], table_name: str):
    sps_stms = [SP_DCSs.from_yaml_file(f) for f in files]
    cb = chain_builder(sps_stms, table_name)
    cb.build_upstream_chain(sps_stms, table_name=table_name)


class chain_builder:
    def __init__(self, sps_stms: Iterable[SP_DCSs], table_name: str):
        self.table_name = table_name
        self.target_obj_syn = _get_sql_object_synonyms_(table_name)
        self.sps_stms = sps_stms

    def build_upstream_chain(self):
        # upsteam_sps = [sp for sp in sps_stms if any(dcs.target_table == table_name for dcs in sp.DCSs)]

        for sp in self.sps_stms:
            # stms = (stm for stm in sp.DCSs if stm.target_table == table_name)
            for stm in sp.DCSs:
                if stm.target_table in self.target_obj_syn and stm.source_tables:
                    print(sp.sp_name)
                    for st in stm.source_tables:
                        print(f'{st}-->{self.table_name}')
                        self.table_name
                        self.build_upstream_chain()


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
        
            
    
        
        
    
    