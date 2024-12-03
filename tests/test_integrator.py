import unittest
from modules.integrator import build_data_flow_graph


class TestIntegrator(unittest.TestCase):

    def test_build_data_flow_graph(self):
        ch = build_data_flow_graph('RussellUS_Constituent_tbl')
        assert len(ch) > 1