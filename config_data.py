import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

OPENAI_API_KEY = os.getenv('OPEN_AI_TOKEN')
LLM_MODEL_NAME = 'gpt-4'  # gpt-3.5-turbo

PARSE_SP_PROMPT_PATH = r'prompt\parse_sp_prompt.txt'
SP_EXAMPLE_PATH = r'prompt\examples\sp_example.sql'
SP_EXAMPLE_OUTPUT_PATH = r'prompt\examples\sp_example.yaml'



