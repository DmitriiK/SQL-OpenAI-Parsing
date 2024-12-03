SELECT 
	ob.object_id, ob.name as object_name, sch.name as schema_name, ob.type_desc, m.definition
	FROM sys.sql_modules m
	JOIN sys.objects ob on ob.object_id=m.object_id
	JOIN sys.schemas sch on sch.schema_id = ob.schema_id
	-- WHERE m.definition LIKE '%[^a-zA-Z0-9_]GenerateChanges_RussellUS_Constituent_prc[^a-zA-Z0-9_]%'