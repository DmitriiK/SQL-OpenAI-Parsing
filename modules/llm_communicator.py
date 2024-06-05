import logging
import re

import tiktoken
from langchain.output_parsers import YamlOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from config_data import OPENAI_API_KEY, PARSE_SP_PROMPT_PATH, LLM_MODEL_NAME, SP_EXAMPLE_PATH, SP_EXAMPLE_OUTPUT_PATH
from modules.data_classes import SP_DCSs


def _strip_square_brackets(data: str) -> str:
    return re.sub(r'[\[\]]', '', data)


class LLMCommunicator:
    def __init__(self):
        self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=LLM_MODEL_NAME, temperature=0)
        self.__prepare_prompt()
        self.script_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.encoding = tiktoken.encoding_for_model(LLM_MODEL_NAME)

    def __prepare_prompt(self):

        with open(PARSE_SP_PROMPT_PATH) as f:
            pr_mess = f.read()
            
        with open(SP_EXAMPLE_PATH) as f:
            sql_script_example = f.read()
            
        with open(SP_EXAMPLE_OUTPUT_PATH) as f:
            example_output = f.read()
            
        example = f"""Input example:
            --
            {sql_script_example}.
            --
            Output:
            {example_output}
        """

        self.output_parser = YamlOutputParser(pydantic_object=SP_DCSs)
        format_instructions = self.output_parser.get_format_instructions()
        # print(format_instructions)

        self.prompt = PromptTemplate(
            template=pr_mess,
            input_variables=['input_sql_script'],
            partial_variables={"format_instructions": format_instructions,
                               "example": example,
                               },
        )
        self.chain = self.prompt | self.llm  # | output_parser

    def request_and_parse(self, sql_script: str) -> SP_DCSs:
        prompt_params = {'input_sql_script': sql_script}
        self.script_tokens += len(self.encoding.encode(sql_script))
        raw_r = self.chain.invoke(prompt_params)
        logging.info(f'got request from LLM, len = {len(raw_r.content)}, trying to parse')
        raw_r.content = _strip_square_brackets(raw_r.content)  # otherwise it will fail on [dbo].
        # print(f'yaml: {raw_r.content}')
        parsed_r = self.output_parser.parse(raw_r.content)
        tu = raw_r.response_metadata['token_usage']
        self.input_tokens += tu['prompt_tokens']
        self.output_tokens += tu['completion_tokens']
        print(parsed_r)
        return parsed_r


# if __name__ == "__main__":
