from modules.pipeline import analyze_files_by_llm, analyze_file_by_llm

# analyze_files_by_llm(skip_existing=False)
fld = r"D:\projects\DataFeedEngine\DataFeedEngineIndex" 
file_name = fld + r'\stg\Stored procedures\PullData_RussellUS2_Constituent_prc.sql'
analyze_file_by_llm(file_name)


