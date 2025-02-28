import glob
from pathlib import Path
import os

import logging

from config_data import INPUT_PATH_SPs, INPUT_PATH_BASE_DIR, OUTPUT_FILE_EXTENSION, OUTPUT_PATH
import modules.llm_communicator as llmc
from modules.view_parser import extract_table_view_names
from modules.data_classes import SP_DCSs
from modules.sql_modules.sql_string_helper import shorten_full_name


def export_to_yaml(inst: SP_DCSs, dir: str = None, file_name: str = None):
    test_yml_str = inst.to_yaml()
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
    file_name = file_name or f'{shorten_full_name(inst.sp_name)}.{OUTPUT_FILE_EXTENSION}'
    file_path = Path(dir, file_name) if dir else Path(file_name)
    logging.info(f'saving to {file_path}')
    with open(file_path, 'w') as yaml_file:
        yaml_file.write(test_yml_str)


def analyze_file_by_llm(sql_script_path: str, model=None):
    model = model or llmc.LLMCommunicator()
    with open(sql_script_path) as f:
        script = f.read()
        ln = len(script)
        if ln > 100000:
            logging.warning(f'script len = {len(script)} if too big, from file {sql_script_path}. Skipping')
            return
        logging.info(f'parsing string, len = {len(script)}, from file {sql_script_path}')
    out = model.request_and_parse(script)
    logging.info(f'spend {model.input_tokens + model.output_tokens} tokens')
    export_to_yaml(out, dir=Path(OUTPUT_PATH))


def analyze_files_by_llm(skip_existing=True):
    model = llmc.LLMCommunicator()
    pathes = get_files_to_parse(INPUT_PATH_SPs, skip_existing)
    for sql_script_path in pathes:
        analyze_file_by_llm(sql_script_path, model)


def analyze_views(skip_existing=False):
    pattern = Path(INPUT_PATH_BASE_DIR, '**', 'Views', '**', '*.sql')
    pathes = get_files_to_parse(pattern, skip_existing)
    for sql_script_path in pathes:
        with open(sql_script_path, 'r') as f:
            script = f.read()
            tv = extract_table_view_names(script)
            print(tv)


def get_files_to_parse(inp_path: str, skip_existing=True):
    if skip_existing:
        already_done_sps = [Path(x).stem for x in
                            glob.glob(fr'{OUTPUT_PATH}\*.{OUTPUT_FILE_EXTENSION}')]
    inp_files = glob.glob(inp_path, recursive=True)
    # inp_files = [r'D:\projects\DataFeedEngine\DataFeedEngineIndex\dbo\Stored Procedures\Merge\MergeData_Russell2_IdentifierType_prc.sql']
    for sql_script_path in inp_files:
        if skip_existing and Path(sql_script_path).stem in already_done_sps:
            continue
        yield sql_script_path




    
