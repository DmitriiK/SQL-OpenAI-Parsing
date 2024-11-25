import unittest

from modules.pipeline import analyze_file_by_llm


class TestLLM(unittest.TestCase):
    def test_parse_sp(self):
        fld = r"D:\projects\DataFeedEngine\DataFeedEngineIndex" 
        file_name = fld + r'\stg\Stored procedures\PullData_RussellUS2_Constituent_prc.sql'
        analyze_file_by_llm(file_name)

