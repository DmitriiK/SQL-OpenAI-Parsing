import unittest

from modules.data_classes import SP_DCSs, DCS, DCS_Type
from modules.pipeline import export_to_yaml
from modules.mermaider import build_upstream_chain_from_yaml, _get_sql_object_synonyms_
from modules.mermaid_diagram import MermaidDiagram

fld = r"D:\projects\DataFeedEngine\DataFeedEngineIndex" 
file_name = fld + r'\dbo\Stored Procedures\Merge\RussellUS\MergeData_RussellUS2_Constituent_prc.sql'
file_yml_to_dc = r'D:\projects\SQL-OpenAI-Parsing\data\output\MergeData_RussellUS2_Constituent_prc.yaml'


class TestChain(unittest.TestCase):

    @unittest.skip('no need')
    def test_yaml(self):
        print('test yaml')
        sp_name = 'SP_CRUDs_example'
        inst = SP_DCSs(sp_name=sp_name, DCSs=[DCS(target_table='[stg].[targ1]', crud_type=DCS_Type.TRUNCATE),
                                              DCS(target_table='[stg].[targ1]', crud_type=DCS_Type.INSERT,
                                                  source_tables=['[dbo].src1', 'dbo.src2']),
                                                ])
        export_to_yaml(inst, r'.\data\output')

    @unittest.skip('no need')
    def test_file_to_dc(self):
        """
        Test load file to data class
        """
        print('test_file_to_data class')
        inst = SP_DCSs.from_yaml_file(file_yml_to_dc)
        print(inst)
        
    def testchain(self):
        ttn = 'RussellUS2_Constituent_tbl'
        dir = r"D:\projects\SQL-OpenAI-Parsing\data\output"
        sps = ['stg.PullData_RussellUS2_Constituent_prc',
               'MergeData_RussellUS2_Constituent_prc',
               'PullData_Russell2_PortfolioHolding_prc']
        paths = [f'{dir}\\{x}.yaml' for x in sps]
        build_upstream_chain_from_yaml(paths, ttn)

    def test_sql_syn(self):
        ret = _get_sql_object_synonyms_('stg.xxx') 
        assert ret == {'stg.xxx', '[stg].[xxx]', 'stg.[xxx]', '[stg].xxx'}
        ret = _get_sql_object_synonyms_('dbo.xxx')
        assert ret == {'dbo.xxx', '[dbo].[xxx]', 'dbo.[xxx]', '[dbo].xxx', 'xxx', '[xxx]'}


class TestMMGen(unittest.TestCase):
    def test_mm_gen(self):
        diagram = MermaidDiagram()
        diagram.add_node("A")
        diagram.add_node("B")
        diagram.add_node("C")
        diagram.add_node("D")

        diagram.add_edge("A", "B", 'a2b')
        diagram.add_edge("A", "C", 'a2c')
        diagram.add_edge("B", "D")
        diagram.add_edge("C", "D")

        mermaid_code = diagram.generate_mermaid_code()
        print(mermaid_code)


"""
This will output:
```
flowchart TD;
    A[A];
    B[B];
    C[C];
    D[D];
    A-->B;
    A-->C;
    B-->D;
    C-->D;
    
    """

if __name__ == '__main__':
    print('main')
    unittest.main()