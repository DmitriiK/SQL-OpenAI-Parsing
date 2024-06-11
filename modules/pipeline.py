
import os
import glob
from pathlib import Path

import logging

from config_data import INPUT_PATH, OUTPUT_FILE_EXTENSION, OUTPUT_PATH
import modules.llm_communicator as llmc
from modules.data_classes import SP_DCSs, DCS, DCS_Type


def export_to_yaml(inst: SP_DCSs, dir: str = None, file_name: str = None):
    test_yml_str = inst.to_yaml()
    print(test_yml_str)
    file_name = file_name or f'{inst.sp_name}.{OUTPUT_FILE_EXTENSION}'
    if dir:
        file_name = os.path.join(dir, file_name)
    logging.info(f'saving to {file_name}')
    with open(file_name, 'w') as yaml_file:
        yaml_file.write(test_yml_str)


def analyze_file(sql_script_path: str, model=None):
    model = model or llmc.LLMCommunicator()
    with open(sql_script_path) as f:
        script = f.read()
        ln = len(script)
        if ln > 10000:
            logging.warning(f'script len = {len(script)} if too big, from file {sql_script_path}. Skipping')
            return
        logging.info(f'parsing string, len = {len(script)}, from file {sql_script_path}')
    out = model.request_and_parse(script)
    logging.info(f'spend {model.input_tokens + model.output_tokens} tokens')
    export_to_yaml(out, dir=r'.\data\output')


def analyze_files(skip_existing=True):
    if skip_existing:
        already_done_sps = [Path(x).stem for x in 
                            glob.glob(fr'{OUTPUT_PATH}\*.{OUTPUT_FILE_EXTENSION}')]
    inp_files = glob.glob(INPUT_PATH, recursive=True)
    model = llmc.LLMCommunicator()
    # inp_files = [r'D:\projects\DataFeedEngine\DataFeedEngineIndex\dbo\Stored Procedures\Merge\MergeData_Russell2_IdentifierType_prc.sql']
    for sql_script_path in inp_files:
        if skip_existing:
            if Path(sql_script_path).stem in already_done_sps:
                continue
        analyze_file(sql_script_path, model)




    
