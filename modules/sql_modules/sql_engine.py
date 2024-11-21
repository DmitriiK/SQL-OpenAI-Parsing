import logging
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text

from modules.sql_modules.sql_config import SQL_Config
import config_data as cfg


class SQL_Executor():
    def __init__(self):
        sql_cfg = SQL_Config.load_config(cfg.SQL_CONFIG_FILE_PATH)
        connection_url = URL.create(
            "mssql+pyodbc",
            host=sql_cfg.sql_server,
            database=sql_cfg.sql_db,
            query={
                "driver": sql_cfg.odbc_driver,
                "TrustServerCertificate": "yes",
                "Trusted_Connection": "yes",
                "Encrypt": "yes"
            },
        )

        self.sql_server, self.db_name, self.driver = sql_cfg.sql_server, sql_cfg.sql_db, sql_cfg.odbc_driver
        self.engine = create_engine(connection_url, connect_args={'timeout': 60})
        self.connection = None
        self.close_connection_finally = True

    def ensure_connection(self):
        if self.connection is None or not self.connection.closed:
            logging.info(f'connecting to {self.sql_server}; DB: {self.db_name}')
            self.connection = self.engine.connect()
            logging.info('connected')

    def close_connection(self):
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
    
    def get_sql_result(self, sql: str, **sql_params):
        query = text(sql)
        self.ensure_connection()
        cursor = self.connection.execute(query, sql_params)
        # self.close_connection()
        result = cursor.fetchall()
        if self.close_connection_finally:
            self.close_connection()
        return result

    def get_relations(self, object_name: str):
        with open(r'modules\sql_modules\scripts\get_dependent_objects.sql', 'r') as f:
            sql = f.read()
        result = self.get_sql_result(sql, object_name=object_name)
        return result


def test():
    SQL_SERVER = 'QTDFEDBDV01.ciqdev.com\\feeds'
    DB_NAME = 'DataFeedEnginePrice'
    driver = 'ODBC Driver 17 for SQL Server'

    xx = SQL_Executor(SQL_SERVER, DB_NAME, driver)
    result = xx.get_sql_result('select 1 as xx')
    for row in result:
        print(row.xx)


if __name__ == '__main__':
    test()
