from typing import List, Tuple
import re


def parse_db_obj_full_name(obj_name: str) -> List[str]:
    return [x.strip('[]') for x in obj_name.split('.')]


def get_table_schema_db(object_name: str) -> Tuple[str, str, str]:
    ss = parse_db_obj_full_name(object_name)
    match len(ss):
        case 1:
            return (ss[0], 'dbo', None)  # table name only means dbo by default
        case 2:
            return (ss[1], ss[0], None)  # table name and schema name
        case 3:
            return (ss[2], ss[1], ss[0])
        case _:
            raise ValueError('incorrect name of object')


def rename_sql_object(sql_def: str, new_name: str):
    # Regular expression to match creating patterns and capture the original object name
    pattern = r"^(create(?: or alter)?(?:\s+view|\s+procedure|\s+function)?)\s+(\S+\.?\S*)"

    def repl(match):
        create_stmt = match.group(1)  # The create or alter statement part
        return f"{create_stmt} {new_name}"

    updated_sql_def = re.sub(pattern, repl, sql_def, flags=re.IGNORECASE | re.MULTILINE)
    return updated_sql_def


def create_obj_name_for_replacement(obj_name: str, obj_name2: str):
    nnn = parse_db_obj_full_name(obj_name)
    if len(nnn) > 1:
        return f'{nnn[-2]}.{obj_name2}'
    return obj_name2


def script_file_read(file_name: str):
    with open(rf'modules\sql_modules\scripts\{file_name}.sql', 'r') as f:
        sql = f.read()
    return sql


def db_name_inject(db_name: str, sql: str):
    return re.sub(r'\bsys\.', f'{db_name}.sys.', sql)

