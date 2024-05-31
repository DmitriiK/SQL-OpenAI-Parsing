import logging
import re

from langchain.output_parsers import YamlOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from config_data import OPENAI_API_KEY, PARSE_SP_PROMPT_PATH, LLM_MODEL_NAME
from modules.data_classes import SP_CRUDs


def _strip_square_brackets(data: str) -> str:
    return re.sub(r'[\[\]]', '', data)


class LLMCommunicator:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=LLM_MODEL_NAME, temperature=0)
        self.__prepare_prompt()

    def __prepare_prompt(self):

        with open(PARSE_SP_PROMPT_PATH) as f:
            pr_mess = f.read()

        self.output_parser = YamlOutputParser(pydantic_object=SP_CRUDs)
        format_instructions = self.output_parser.get_format_instructions()
        # print(format_instructions)

        self.prompt = PromptTemplate(
            template=pr_mess,
            input_variables=['input_sql_script'],
            partial_variables={"format_instructions": format_instructions,
                               # "example": example,
                               },
        )
        self.chain = self.prompt | self.llm  # | output_parser

    def request_and_parse(self, sql_script: str) -> SP_CRUDs:
        prompt_params = {'input_sql_script': sql_script}
        raw_r = self.chain.invoke(prompt_params)
        logging.info(f'got request from LLM, len = {len(raw_r.content)}, trying to parse')
        raw_r.content = _strip_square_brackets(raw_r.content)  # otherwise it will fail on [dbo].
        print(f'yaml: {raw_r.content}')
        parsed_r = self.output_parser.parse(raw_r.content)
        print(parsed_r)
        return parsed_r


# if __name__ == "__main__":
