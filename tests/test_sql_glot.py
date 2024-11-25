from sqlglot import parse_one, parse, Dialects, exp
"""
# print all column references (a and b)
for column in parse_one("SELECT a, b + 1 AS c FROM d").find_all(exp.Column):
    print(column.alias_or_name)

# find all projections in select statements (a and c)
for select in parse_one("SELECT a, b + 1 AS c FROM d").find_all(exp.Select):
    for projection in select.expressions:
        print(projection.alias_or_name)

# find all tables (x, y, z)
for table in parse_one("SELECT * FROM x JOIN y JOIN z").find_all(exp.Table):
    print(table.name)
    """
sql = """CREATE view stg.test_parse as 
        WITH cte_yy as (SELECT ID, C2 FROM yy_tbl WHERE ss = 0)
        SELECT  x.ID, x.C1, y.C2, 'x' as EX
        from xx_tbl x 
        JOIN cte_yy y 
            on x.ID=y.ID;
            
         INSERT INTO  dbo.trg(ID, C1, C2, EX)      
         SElect * FROM stg.test_parse 
        """
prs = parse(sql, dialect=Dialects.TSQL     )
for st in prs:
    print(st)
