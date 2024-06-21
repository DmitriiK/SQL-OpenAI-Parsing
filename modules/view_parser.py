import re

# Regex pattern to match CREATE TABLE and CREATE VIEW statements, including schema names
create_table_pattern = r'CREATE\s+TABLE\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)'
create_view_pattern = r'CREATE\s+VIEW\s+([a-zA-Z0-9_]+\.[a-zA-Z0-9_]+|[a-zA-Z0-9_]+)'


def extract_table_view_names(sql_script):
    table_names = re.findall(create_table_pattern, sql_script, re.IGNORECASE)
    view_names = re.findall(create_view_pattern, sql_script, re.IGNORECASE)
    all_names = table_names + view_names
    # Filter out temporary tables (those starting with '#')
    filtered_names = [name for name in all_names if not name.split('.')[-1].startswith('#')]

    return filtered_names