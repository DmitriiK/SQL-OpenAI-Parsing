from modules.pipeline import analyze_files, analyze_file

# analyze_files(skip_existing=False)
fld = r"D:\projects\DataFeedEngine\DataFeedEngineIndex" 
file_name = fld + r'\dbo\Stored Procedures\Merge\RussellUS\MergeData_RussellUS2_Constituent_prc.sql'
analyze_file(file_name)
