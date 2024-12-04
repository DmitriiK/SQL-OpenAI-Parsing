from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
import yaml


class DCS_Type(str, Enum):
    INSERT = 'INSERT'
    MERGE = 'MERGE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    CREATE = 'CREATE'
    TRUNCATE = 'TRUNCATE'
    DROP = 'DROP'

    def __repr__(self) -> str:
        return str.__repr__(self.value)


class DCS(BaseModel):
    """Data changing SQL statement
    """
    crud_type: DCS_Type = Field(description='One of possible SQL CRUD data-changing types')
    target_table: str = Field(description='Target table name for data-changing SQL statement')
    source_tables: Optional[List[str]] = Field(description='Names of source tables or views for SQL statement')

    def to_dict(self):
        # Create a dictionary representation of the instance with conditional logic
        data = {'crud_type': self.crud_type.value, 'target_table': self.target_table}
        if self.source_tables:
            data['source_tables'] = self.source_tables
        return data


class SP_DCSs(BaseModel):
    """Compact representation of SQL statements inside some Stored Procedure
    """
    sp_name: str = Field(description='Stored procedure name')
    DCSs: List[DCS] = Field(description='Each elememnt in the list corresponds one data-changing SQL statement inside stored procedure')

    def to_yaml(self):
        # Convert nested DCS objects to dictionaries
        data = {'sp_name': self.sp_name, 'DCSs': [dcs.to_dict() for dcs in self.DCSs]}
        return yaml.dump(data, sort_keys=False)
    
    @classmethod
    def from_yaml_file(cls, file_path: str):
        with open(file_path, 'r') as file:
            yaml_data = yaml.safe_load(file)
            inst = cls(**yaml_data)
            return inst


class ViewSourceTables(BaseModel):
    """Data source tables (or views), been referenced in the view
    """
    view_name: str = Field(description='Target table for data-changing SQL statement')
    source_tables: Optional[List['ViewSourceTables']] = Field(description='Names of source tables or views for SQL statement')


class DB_Object_Type(Enum):
    USER_TABLE = 'USER_TABLE'
    VIEW = 'VIEW'
    SQL_STORED_PROCEDURE = 'SQL_STORED_PROCEDURE'
    SQL_SCALAR_FUNCTION = 'SQL_SCALAR_FUNCTION'  
    SQL_INLINE_TABLE_VALUED_FUNCTION = 'SQL_INLINE_TABLE_VALUED_FUNCTION'
    CLR_STORED_PROCEDURE = 'CLR_STORED_PROCEDURE'


class SQL_Object (BaseModel):
    """SQL object, table, view, stored procedure, whaever

    """
    object_id: Optional[int] = Field(default=None)
    name: str
    type: DB_Object_Type = Field(default=None)
    db_schema: Optional[str] = Field(default='dbo')
    db_name: Optional[str] = Field(default=None)
    server_name:  Optional[str] = Field(default=None)

    @property
    def full_name(self):
        nnn = f'{self.db_schema or 'dbo'}.{self.name}'
        if self.db_name:
            nnn = f'{self.db_name}.{nnn}'
            if self.server_name:
                nnn = f'{self.server_name}.{nnn}'
        return nnn
