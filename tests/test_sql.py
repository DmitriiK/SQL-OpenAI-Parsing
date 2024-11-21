import unittest
import logging

import config_data as cfg
from modules.sql_modules.sql_config import SQL_Config
from modules.sql_modules.sql_engine import SQL_Executor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class TestSQL(unittest.TestCase):

    def test_sql_connection(self): 
        sql_cfg = SQL_Config.load_config(cfg.SQL_CONFIG_FILE_PATH)
        exr = SQL_Executor(sql_cfg.sql_server, sql_cfg.sql_db, sql_cfg.odbc_driver)       
        ret = exr.get_sql_result("SELECT 1 as c1")
        for row in ret:
            assert row.c1
            print(row.c1)
        
    def test_get_relations(self):
        sql_cfg = SQL_Config.load_config(cfg.SQL_CONFIG_FILE_PATH)
        exr = SQL_Executor(sql_cfg.sql_server, sql_cfg.sql_db, sql_cfg.odbc_driver) 
        ret = exr.get_relations('dbo.datafeedOut_applyChangesCompanyNames_prc')
        print(ret)



