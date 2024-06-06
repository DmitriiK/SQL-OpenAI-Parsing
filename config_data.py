import os
from dotenv import load_dotenv
import logging
from enum import Enum


class GPT_Model(str, Enum):
    GPT_4 = 'gpt-4'
    GPT_3_5_Turbo = 'gpt-3.5-turbo'
    GPT_4o = 'gpt-4o'

    def __repr__(self) -> str:
        return str.__repr__(self.value)


load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
LLM_MODEL_NAME = GPT_Model.GPT_4o

PARSE_SP_PROMPT_PATH = r'prompt\parse_sp_prompt.txt'
SP_EXAMPLE_PATH = r'prompt\examples\sp_example.sql'
SP_EXAMPLE_OUTPUT_PATH = r'prompt\examples\sp_example.yaml'

INPUT_PATH = r'D:\projects\DataFeedEngine\DataFeedEngineIndex\*\Stored procedures\*\*.sql'
OUTPUT_PATH = r'.\data\output'
OUTPUT_FILE_EXTENSION = 'yaml'



