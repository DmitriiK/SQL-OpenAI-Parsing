from typing import List, Tuple
import re

default_schema = 'dbo'


def parse_db_obj_full_name(obj_name: str) -> List[str]:
    return [x.strip('[] ') for x in obj_name.split('.')]


def shorten_full_name(object_name: str) -> str:
    ss = parse_db_obj_full_name(object_name)
    match len(ss):
        case 1:
            return ss[0]
        case 2:
            return ss[1] if ss[0] == default_schema else '.'.join(ss)
        case 3:
            return '.'.join(ss)
        case _:
            raise ValueError('incorrect name of object')


def get_table_schema_db_srv(object_name: str) -> Tuple[str, str, str, str]:
    ss = parse_db_obj_full_name(object_name)
    match len(ss):
        case 1:
            return (ss[0], 'dbo', None, None)  # table name only means dbo by default
        case 2:
            return (ss[1], ss[0], None, None)  # table name and schema name
        case 3:
            return (ss[2], ss[1], ss[0], None)
        case 4:
            return (ss[3], ss[2], ss[1], ss[0])
        case _:
            raise ValueError('incorrect name of object')


def sql_objs_are_eq(o1: str, o2: str) -> bool:
    ooo1 = get_table_schema_db_srv(o1)
    ooo2 = get_table_schema_db_srv(o2)
    return all((ooo1[i].lower() if ooo1[i] else '') == (ooo2[i].lower() if ooo2[i] else '') for i in range(4))


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
    

def find_sql_objects(search_where, search_what, current_db=None, first_match_only=True) -> List[Tuple[int, int]]:
    def sql_name_regex(inp: str) -> str:
        """tbl_name => tbl_name or [tbl_name] for regex search with []"""
        return fr'\[\s*{inp}\s*\]|\b{inp}'

    entity_name, _, _, _ = get_table_schema_db_srv(search_what) 
    part_pattern = r"(\[*\s*\w+\s*\]*\.)?" # any word, that might be inside spaces, that might be inside [], followed by a dot
    re_str = fr"(?<!\w)({part_pattern*3}({sql_name_regex(entity_name)}))(?!\w)"

    object_name_pattern = re.compile(re_str,re.VERBOSE | re.IGNORECASE | re.MULTILINE)
    matches = []
    for match in object_name_pattern.finditer(search_where):
        found = match.group(0)
        if sql_objs_are_eq(found, search_what):       
            matches.append((match.start(), match.end()))
            if first_match_only:
                break
    return matches


