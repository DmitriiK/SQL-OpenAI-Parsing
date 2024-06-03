from enum import Enum
from typing import List, Optional

from langchain_core.pydantic_v1 import BaseModel, Field


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


class SP_DCSs(BaseModel):
    sp_name: str = Field(description='Stored procedure name')
    DCSs: List[DCS] = Field()
