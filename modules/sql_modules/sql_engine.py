import logging
from typing import List, Tuple

from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text, Table

from modules.sql_modules.sql_config import SQL_Config
from modules.sql_modules.sql_string_helper import get_table_schema_db, script_file_read, db_name_inject
from modules.data_classes import SQL_Object
import config_data as cfg


class SQL_Executor():
    def __init__(self, sql_cfg: SQL_Config = None):
        sql_cfg = sql_cfg or SQL_Config.load_config(cfg.SQL_CONFIG_FILE_PATH)
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
        self.other_sql_dbs = sql_cfg.other_sql_dbs
        self.engine = create_engine(connection_url, connect_args={'timeout': 60})
        self.connection = None
        self.close_connection_finally = True

    def ensure_connection(self):
        if self.connection is None or self.connection.closed:
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

    def get_relations(self, object_name: str, get_referenced=True, referencing_db_name: str = None) -> List[Tuple]:
        """Get SQL dependencies using sys.sql_expression_dependencies views
        Args:
            object_name (str): sql object name
            get_referenced (bool, optional): if true - taking dependent, child objects. Defaults to True.

        Returns:
            _type_: _description_
        """
        sql = script_file_read('get_dependent_objects')
        if referencing_db_name and referencing_db_name != self.db_name:
            sql = db_name_inject(referencing_db_name, sql)
        if get_referenced:
            sql += '\nAND d.referencing_id = object_id(:object_name)'
            sql_params = dict(object_name=object_name,
                              referencing_db_name=referencing_db_name or self.db_name) 
        else:  # get depending, parent  objects
            referenced_entity_name, referenced_schema_name, referenced_db = get_table_schema_db(object_name)
            sql += '\nAND referenced_entity_name = :referenced_entity_name'

            or_schema_cond = 'OR referenced_schema_name IS NULL' if referenced_schema_name == 'dbo' else ''
            sql += f'\nAND (referenced_schema_name = :referenced_schema_name {or_schema_cond})'
            if not referenced_db or referenced_db == self.db_name:
                sql += '\nAND (referenced_database_name = :referenced_database_name or referenced_database_name IS NULL)'
            else:
                sql += '\nAND referenced_database_name = :referenced_database_name'
            sql_params = dict(referenced_entity_name=referenced_entity_name,
                              referenced_schema_name=referenced_schema_name,
                              referenced_database_name=referenced_db or self.db_name,
                              referencing_db_name=referencing_db_name or self.db_name)
        result = self.get_sql_result(sql, **sql_params)
        return result

    def get_dbs(self):
        sql = script_file_read('get_dbs')
        return self.get_sql_result(sql)

    def get_dependent(self, object_name: str) -> List[SQL_Object]:
        xx = self.get_relations(object_name=object_name, get_referenced=True)
        sqlobs = [SQL_Object(name=x.referenced_entity_name,
                  db_schema=x.referenced_schema_name,
                  db_name=x.referenced_database_name,  # type=x.referencing_type_desc,
                  object_id=x.referenced_id)
                  for x in xx]
        return sqlobs

    def get_depending(self, object_name: str) -> List[SQL_Object]:
        """Retrieve depending objects from all DBs on Server
        Args:
            object_name (str): Dependend object name
        Returns:
            List[Tuple]: List of Depending objects
        """
        self.close_connection_finally = False
        # dbs = self.get_dbs()
        dbs = [self.db_name] + self.other_sql_dbs
        ret = []
        for db in dbs:
            db_deps = self.get_relations(object_name=object_name,
                                         get_referenced=False,
                                         referencing_db_name=db)
            sqlobs = [SQL_Object(name=x.referencing_object,
                      db_schema=x.referencing_object_schema,
                      db_name=db,
                      type=x.referencing_type_desc,
                      object_id=x.referencing_id)
                      for x in db_deps]                
            ret.extend(sqlobs)
        self.close_connection_finally = True
        return ret

    def get_module_def(self, object_name: str) -> str:
        """
        Gets the definition of a SQL Server view or stored procedure.        
        Args:
            object_name (str): The name of the view or stored procedure.            
        Returns:
            str: The definition of the view or stored procedure.
        """
        nnn = get_table_schema_db(object_name)
        db_name = nnn[2] or ''
        sql = script_file_read('get_module_def')
        if db_name and db_name != self.db_name:
            sql = db_name_inject(db_name, sql)
        sql_param = dict(object_name=object_name)
        return self.get_sql_result(sql, **sql_param)


def test():
    xx = SQL_Executor()
    result = xx.get_sql_result('select 1 as xx')
    for row in result:
        print(row.xx)


if __name__ == '__main__':
    test()
