
from typing import List
from modules.data_classes import SP_DCSs


def build_upstream_chain(files: List[str], table_name: str):
    sps_stms = (SP_DCSs.from_yaml_file(f) for f in files)
    upsteam_sps = [sp for sp in sps_stms
                   if any(dcs.target_table == table_name for dcs in sp.DCSs)]
    return upsteam_sps
    
        
        
    
    