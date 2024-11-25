import unittest
from pathlib import Path
from modules.pipeline import analyze_file_by_llm


class TestLLM(unittest.TestCase):
    def test_parse_sp(self):
        file_name = Path(r"data/output/input/datafeedOut_generateChangeFilesAddress_prc.sql" )
        analyze_file_by_llm(file_name)

