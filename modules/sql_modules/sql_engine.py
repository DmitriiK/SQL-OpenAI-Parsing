import logging
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text

connection_string_template = (
    'mssql+pyodbc://{sql_serv}/{db_name}?'
    'driver=ODBC+Driver+17+for+SQL+Server;'
    'Trusted_Connection=yes;'
    'Encrypt=yes;'
    'TrustServerCertificate=yes;'
)


class SQL_Executor():
    def __init__(self, sql_serv: str, db_name: str, driver: str):
        connection_url = URL.create(
            "mssql+pyodbc",
            host=sql_serv,
            database=db_name,
            query={
                "driver": driver,
                "TrustServerCertificate": "yes",
                "Trusted_Connection": "yes",
                "Encrypt": "yes"
            },
        )

        self.sql_serv, self.db_name, self.driver = sql_serv, db_name, driver
        self.engine = create_engine(connection_url, connect_args={'timeout': 60})
        self.connection = None

    def ensure_connection(self):
        if self.connection is None or not self.connection.closed:
            logging.info(f'connecting to {self.sql_serv}; DB: {self.db_name}')
            self.connection = self.engine.connect()
            logging.info('connected')

    def close_connection(self):
        if self.connection is not None and not self.connection.closed:
            self.connection.close()
    
    def get_sql_result(self, sql: str):
        query = text(sql)
        logging.info('connecting..')        
        with self.engine.connect() as connection:
            logging.info('connected!')
            cursor = connection.execute(query)
            for row in cursor:
                yield row
    
    def get_relations(self, object_name: str):
        with open(r'modules\sql_modules\scripts\get_dependent_objects.sql', 'r') as f:
            sql = f.read()
        # sql += "\nAND d.referencing_id = object_id(:object_name)"
        query = text(sql)
        self.ensure_connection()
        result = self.connection.execute(query, {"object_name": object_name}).fetchall()
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
