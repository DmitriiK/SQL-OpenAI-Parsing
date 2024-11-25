import os
from dotenv import load_dotenv
import logging
from enum import Enum


class GPT_Model(str, Enum):
    GPT_4 = 'gpt-4'
    GPT_3_5_Turbo_0125 = 'gpt-3.5-turbo-0125'
    GPT_4o = 'gpt-4o'

    def __repr__(self) -> str:
        return str.__repr__(self.value)


load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
LLM_MODEL_NAME = GPT_Model.GPT_4o

PARSE_SP_PROMPT_PATH = r'prompt/parse_sp_prompt.txt'
SP_EXAMPLE_PATH = r'prompt/examples/sp_example.sql'
SP_EXAMPLE_OUTPUT_PATH = r'prompt\examples\sp_example.yaml'

INPUT_PATH_SPs = r'D:\projects\DataFeedEngine\DataFeedEngineIndex\*\Stored procedures\*\*.sql'
INPUT_PATH_BASE_DIR = r'D:\projects\DataFeedEngine\DataFeedEngineIndex'
OUTPUT_PATH = r'./data/output'
OUTPUT_FILE_EXTENSION = 'yaml'

SQL_CONFIG_FILE_PATH = r'modules/sql_modules/sql_config.yaml'



