SELECT
	d.referencing_id,
	OBJECT_SCHEMA_NAME(d.referencing_id) referencing_object_schema,
	OBJECT_NAME (d.referencing_id) AS referencing_object,
	:referencing_db_name as referencing_database_name,
	ob.type_desc as referencing_type_desc,
	d.referenced_database_name, 
	d.referenced_id,
    referenced_schema_name, 
	referenced_entity_name,
	referenced_ob.type_desc referenced_type_desc
	FROM sys.sql_expression_dependencies d
	JOIN sys.objects ob on ob.object_id=d.referencing_id
	LEFT JOIN sys.objects referenced_ob on referenced_ob.object_id=d.referenced_id --in the same db
WHERE is_ambiguous = 0