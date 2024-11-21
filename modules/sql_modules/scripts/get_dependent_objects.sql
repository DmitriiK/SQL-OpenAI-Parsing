SELECT
	d.referencing_id,
	OBJECT_SCHEMA_NAME(d.referencing_id) referencing_object_schema,
	OBJECT_NAME (d.referencing_id) AS referencing_object,
	ob.type_desc,
	referenced_database_name, 
	d.referenced_id,
    referenced_schema_name, 
	referenced_entity_name
	 FROM sys.sql_expression_dependencies d
	 JOIN sys.objects ob on ob.object_id=d.referencing_id
WHERE is_ambiguous = 0
