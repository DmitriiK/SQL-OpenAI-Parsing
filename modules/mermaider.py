
from typing import List, Iterable
from modules.data_classes import SP_DCSs
"""
taking list of SPs, 
finding target table as target table in the SP list  of the statements,
for each of the statements take source tables
for each of them find SPs, where they are targeted
if no new SP for SP have been find, recursion stops,  - we are at the top level of data stream
"""


def build_upstream_chain_from_yaml(files: List[str], table_name: str):
    sps_stms = (SP_DCSs.from_yaml_file(f) for f in files)
    build_upstream_chain(sps_stms, table_name=table_name)


def build_upstream_chain(sps_stms: Iterable[SP_DCSs], table_name: str):
    # upsteam_sps = [sp for sp in sps_stms if any(dcs.target_table == table_name for dcs in sp.DCSs)]
    for sp in sps_stms:
        stms = (stm for stm in sp.DCSs if stm.target_table == table_name)
        for stm in stms:
            print(sp.sp_name)
            for st in stm.source_tables:
                build_upstream_chain(sps_stms, st)
        
            
    
        
        
    
    