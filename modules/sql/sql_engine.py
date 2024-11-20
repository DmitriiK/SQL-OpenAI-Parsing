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
    
    def get_sql_result(self, sql: str):
        query = text(sql)
        print('connecting..')
        with self.engine.connect() as connection:
            print('connected!')
            cursor = connection.execute(query)
            for row in cursor:
                yield row


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
