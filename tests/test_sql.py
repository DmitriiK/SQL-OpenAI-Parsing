import unittest
import logging
from rich import print

from modules.sql_modules.sql_engine import SQL_Executor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class TestSQL(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.exr = SQL_Executor()
        super(TestSQL, self).__init__(*args, **kwargs)

    def test_sql_connection(self):
        ret = self.exr.get_sql_result("SELECT 1 as c1")
        for row in ret:
            assert row.c1
            print(row.c1)
        
    def test_get_dependent(self):
        tcs = ['DataFeedOut_SnP350V2_Portfolio_vw',  # 'dbo.datafeedOut_applyChangesCompanyNames_prc'
              ]
        for object_name in tcs:
            ret = self.exr.get_dependent(object_name)
            assert ret
        print(ret)

    def test_get_referencing(self):
        refed_tbl = 'DataFeedEngineCache.dbo.dataFeedOut_SearchCompanyNamesUsPubFile_tbl'
        ret = self.exr.get_relations(refed_tbl, get_referenced=False)
        assert ret
        print(ret)

    def test_get_depending(self):
        refed_tbl = 'RussellUS2_Constituent_tbl' # 'DataFeedEngineCache.dbo.dataFeedOut_SearchCompanyNamesUsPubFile_tbl'
        ret = self.exr.get_depending(refed_tbl)
        assert ret
        print(ret)

    def test_get_module_def(self):
        modef = self.exr.get_module_def('dbo.MergeData_RussellUS2_Constituent_prc')
        assert modef
        print(modef)





