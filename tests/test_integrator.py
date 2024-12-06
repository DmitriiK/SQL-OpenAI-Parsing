import unittest
import os

from modules.integrator import build_data_flow_graph, data_flow_to_yaml
from config_data import OUTPUT_PATH

trg_tbl = 'RussellUS_Constituent_tbl'


class TestIntegrator(unittest.TestCase):
        
    def test_build_data_flow_graph(self):
        out_dir_pth = os.path.join(OUTPUT_PATH, f'target_table = {trg_tbl}')
        cnt = data_flow_to_yaml(trg_tbl, out_dir_pth)
        assert cnt > 3
       