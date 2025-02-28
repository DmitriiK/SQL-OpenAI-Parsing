import logging
from typing import List, Tuple

from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text
from modules.sql_modules.sql_config import SQL_Config
from modules.sql_modules.sql_string_helper import get_table_schema_db_srv, script_file_read, db_name_inject
from modules.data_classes import SQL_Object, DB_Object_Type
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
    
    def get_sql_object(self, object_name: str) -> SQL_Object:
        sql = script_file_read('get_sql_object')
        _, _, obj_db = get_table_schema_db_srv(object_name)
        if obj_db and obj_db != self.db_name:
            sql = db_name_inject(obj_db, sql)
        sql_params = dict(object_name=object_name,)
        result = self.get_sql_result(sql, **sql_params)
        if result:
            result_dict = result[0]._asdict()  # Convert Row object to dictionary
            sql_object = SQL_Object(**result_dict)
            return sql_object
        else:
            logging.warning(f"No object found with the provided name {object_name}")
            #  raise ValueError("No object found with the provided name")

        # return SQL_Object(object_id=result.ob, name = result.na, db_schema = result.)

    def get_depending_by_modules_search(self, object_name: str,  referencing_db_name: str = None,
                                        referencing_type_descr: DB_Object_Type = None) -> List[Tuple]:
        """Get SQL dependencies using direct search in module definition in sys.modules
        Args:
            object_name (str): sql object name
        Returns:
            
        """
        sql = script_file_read('get_modules_def')
        if referencing_db_name and referencing_db_name != self.db_name:
            sql = db_name_inject(referencing_db_name, sql)
        referenced_entity_name, referenced_schema_name, referenced_db = get_table_schema_db_srv(object_name)

        nlp = '[^a-zA-Z0-9_]'  # not letter pattern for SQL like by word boundary
        obj_name_pattern = f'%{nlp}{referenced_entity_name}{nlp}%'

        sql += '\nWHERE m.definition LIKE  :obj_name_pattern'
        # TODO consider schema name and []
        if referencing_type_descr:
            sql += '\nAND ob.type_desc = :referencing_type_descr'

        sql_params = dict(obj_name_pattern=obj_name_pattern,
                          referencing_type_descr=referencing_type_descr.value if referencing_type_descr else None)
        result = self.get_sql_result(sql, **sql_params)
        return result
 
    def get_relations(self, object_name: str, get_referenced=True, referencing_db_name: str = None,
                      referencing_type_descr: DB_Object_Type = None) -> List[Tuple]:
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
            referenced_entity_name, referenced_schema_name, referenced_db = get_table_schema_db_srv(object_name)
            sql += '\nAND referenced_entity_name = :referenced_entity_name'

            or_schema_cond = 'OR referenced_schema_name IS NULL' if referenced_schema_name == 'dbo' else ''
            sql += f'\nAND (referenced_schema_name = :referenced_schema_name {or_schema_cond})'
            if not referenced_db or referenced_db == self.db_name:
                sql += '\nAND (referenced_database_name = :referenced_database_name or referenced_database_name IS NULL)'
            else:
                sql += '\nAND referenced_database_name = :referenced_database_name'

            if referencing_type_descr:
                sql += '\nAND ob.type_desc = :referencing_type_descr'

            sql_params = dict(referenced_entity_name=referenced_entity_name,
                              referenced_schema_name=referenced_schema_name,
                              referenced_database_name=referenced_db or self.db_name,
                              referencing_db_name=referencing_db_name or self.db_name,
                              referencing_type_descr=referencing_type_descr.value if referencing_type_descr else None)
        result = self.get_sql_result(sql, **sql_params)
        return result

    def get_dbs(self):
        sql = script_file_read('get_dbs')
        return self.get_sql_result(sql)

    def get_view_child_components(self, view_name: str, deep_dive=False) -> List[SQL_Object]:
        ret_lst = []
        
        def get_next_level(vn: str):
            obs = self.get_dependent(vn)
            if not deep_dive:
                ret_lst.extend(obs)
            else:
                ret_lst.extend([x for x in obs if x.type == DB_Object_Type.USER_TABLE])
                child_views = [x for x in obs if x.type == DB_Object_Type.VIEW]
                for cv in child_views:
                    get_next_level(vn=cv.full_name)
                    
        get_next_level(view_name)
        return ret_lst

    def get_dependent(self, object_name: str) -> List[SQL_Object]:
        def sql_row2data_class(x):
            so = SQL_Object(name=x.referenced_entity_name,
                            db_schema=x.referenced_schema_name or 'dbo',
                            db_name=x.referenced_database_name,
                            type=x.referenced_type_desc,
                            object_id=x.referenced_id)
            if so.db_name and not so.object_id:  # cross-db relations
                f_name = f'[{so.db_name}].[{so.db_schema}].[{so.name}]'
                cross_db_so = self.get_sql_object(f_name)
                if cross_db_so:
                    so.object_id = cross_db_so.object_id
                    so.type = cross_db_so.type
                else:
                    logging.warning(f'object {f_name} is missing')
            return so
        _, _, db = get_table_schema_db_srv(object_name=object_name)
        xx = self.get_relations(object_name=object_name, get_referenced=True, referencing_db_name=db)
        return [sql_row2data_class(x) for x in xx]

    def get_depending(self, object_name: str, referencing_type_descr: DB_Object_Type = None) -> List[SQL_Object]:
        """Retrieve depending objects from all DBs on Server
        Args:
            object_name (str): Dependend object name
        Returns:
            List[SQL_Object
            ]: List of Depending objects
        """
        ccf_status = self.close_connection_finally
        self.close_connection_finally = False
        # dbs = self.get_dbs()
        dbs = [self.db_name] + self.other_sql_dbs
        ret = []
        for db in dbs:
            db_deps = self.get_relations(object_name=object_name,
                                         get_referenced=False,
                                         referencing_db_name=db,
                                         referencing_type_descr=referencing_type_descr)
            sqlobs = [SQL_Object(name=x.referencing_object,
                      db_schema=x.referencing_object_schema,
                      db_name=db,
                      type=x.referencing_type_desc,
                      object_id=x.referencing_id)
                      for x in db_deps]                
            ret.extend(sqlobs)
        self.close_connection_finally = ccf_status
        return ret

    def get_module_def(self, object_name: str) -> str:
        """
        Gets the definition of a SQL Server view or stored procedure.        
        Args:
            object_name (str): The name of the view or stored procedure.            
        Returns:
            str: The definition of the view or stored procedure.
        """
        nnn = get_table_schema_db_srv(object_name)
        db_name = nnn[2] or ''
        sql = script_file_read('get_module_def')
        if db_name and db_name != self.db_name:
            sql = db_name_inject(db_name, sql)
        sql_param = dict(object_name=object_name)
        ret = self.get_sql_result(sql, **sql_param)
        return ret[0][0] if ret else None


def test():
    xx = SQL_Executor()
    result = xx.get_sql_result('select 1 as xx')
    for row in result:
        print(row.xx)


if __name__ == '__main__':
    test()
