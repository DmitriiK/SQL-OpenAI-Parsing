from enum import Enum
from typing import List, Optional

from langchain_core.pydantic_v1 import BaseModel, Field
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
    crud_type: DCS_Type = Field(description='One of possible SQL CRUD data-changing types')
    target_table: str = Field(description='Target table for data-changing SQL statement')
    source_tables: Optional[List[str]] = Field(description='Names of source tables or views for SQL statement')

    def to_dict(self):
        # Create a dictionary representation of the instance with conditional logic
        data = {'crud_type': self.crud_type.value, 'target_table': self.target_table}
        if self.source_tables:
            data['source_tables'] = self.source_tables
        return data


class SP_DCSs(BaseModel):
    sp_name: str = Field(description='Stored procedure name')
    DCSs: List[DCS] = Field()

    def to_yaml(self):
        # Convert nested DCS objects to dictionaries
        data = {'sp_name': self.sp_name, 'DCSs': [dcs.to_dict() for dcs in self.DCSs]}
        return yaml.dump(data, sort_keys=False)