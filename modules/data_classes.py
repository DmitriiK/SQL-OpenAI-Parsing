from enum import Enum
from typing import List, Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class CRUD_Type(str, Enum):
    INSERT = 'INSERT'
    MERGE = 'MERGE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    CREATE = 'CREATE'
    TRUNCATE = 'TRUNCATE'

    def __repr__(self) -> str:
        return str.__repr__(self.value)


class CRUD_Statement(BaseModel):
    crud_type: CRUD_Type = Field(description='One of possible SQL CRUD types')
    target_table: str = Field(description='Target table for CRUD operation')
    source_tables: Optional[List[str]] = Field(description='Names of source tables or views for CRUD operation')


class SP_CRUDs(BaseModel):
    sp_name: str = Field(description='Stored procedure name')
    cruds: List[CRUD_Statement] = Field()
