from dataclasses import dataclass
from typing import List
import yaml

@dataclass
class SQL_Config:
    sql_server: str
    sql_db: str
    other_sql_dbs: List[str]
    odbc_driver: str

    @classmethod
    def load_config(cls, file_path: str) -> 'Config':
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return cls(**data)