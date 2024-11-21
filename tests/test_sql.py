import unittest
import logging

from modules.sql_modules.sql_engine import SQL_Executor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class TestSQL(unittest.TestCase):

    def test_sql_connection(self):
        exr = SQL_Executor()
        ret = exr.get_sql_result("SELECT 1 as c1")
        for row in ret:
            assert row.c1
            print(row.c1)
        
    def test_get_relations(self):
        exr = SQL_Executor()
        ret = exr.get_relations('dbo.datafeedOut_applyChangesCompanyNames_prc')
        print(ret)



