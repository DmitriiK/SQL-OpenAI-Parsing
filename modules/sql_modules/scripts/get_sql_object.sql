SELECT 
	o.object_id,
    OBJECT_SCHEMA_NAME(o.object_id) AS db_schema,
    o.name AS name,
    o.type_desc as [type]
FROM 
    sys.objects o
INNER JOIN 
    sys.schemas s ON s.schema_id = o.schema_id 
WHERE object_id = OBJECT_ID(:object_name)