import unittest
import os

from modules.integrator import data_flow_to_yaml, data_flow_to_mermaid
from config_data import OUTPUT_PATH

trg_tbl = 'RussellUS_Constituent_tbl'


class TestIntegrator(unittest.TestCase):
        
    def test_data_flow_to_yaml(self):
        out_dir_pth = os.path.join(OUTPUT_PATH, f'target_table = {trg_tbl}')
        cnt = data_flow_to_yaml(trg_tbl, out_dir_pth)
        assert cnt > 3

    def test_data_flow_to_mermaid(self):
        cnt = data_flow_to_mermaid(trg_tbl)
        assert cnt > 3
    
       