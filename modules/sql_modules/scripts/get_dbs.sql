SELECT  
    database_id, 
    name as database_name
    ,IIF(DB_ID()=database_id, 1,0) as is_current_db 
FROM master.sys.databases dbs 
WHERE dbs.state_desc = 'ONLINE' 
AND  name NOT IN ('master', 'tempdb', 'model', 'msdb')
ORDER BY is_current_db DESC