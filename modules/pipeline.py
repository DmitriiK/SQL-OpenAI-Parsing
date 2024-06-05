
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


def take_analyze_and_save(skip_existing = True):
 
    if skip_existing:
        already_done_sps = [Path(x).stem for x in 
                            glob.glob(fr'{OUTPUT_PATH}\*.{OUTPUT_FILE_EXTENSION}')]
    inp_files = glob.glob(INPUT_PATH, recursive=True)
    # sql_script_path = r'D:\projects\DataFeedEngine\DataFeedEngineIndex\stg\Stored procedures\PullData_RussellUS2_IndexSecurityValue_prc.sql'
    model = llmc.LLMCommunicator()
    for sql_script_path in inp_files:
        if skip_existing:
            if Path(sql_script_path).stem in already_done_sps:
                continue
        with open(sql_script_path) as f:
            script = f.read()
            ln = len(script)
            if ln > 10000:
                logging.warning(f'script len = {len(script)} if too big, from file {sql_script_path}. Skipping')
                continue
            logging.info(f'parsing string, len = {len(script)}, from file {sql_script_path}')
        out = model.request_and_parse(script)
        logging.info(f'spend {model.input_tokens + model.output_tokens} tokens')
        export_to_yaml(out, dir=r'.\data\output')


def test_yaml():
    print('test yaml')
    sp_name = 'SP_CRUDs_example'
    inst = SP_DCSs(sp_name=sp_name, DCSs=[DCS(target_table='[stg].[targ1]', crud_type=DCS_Type.TRUNCATE),
                                          DCS(target_table='[stg].[targ1]', crud_type=DCS_Type.INSERT,
                                                                            source_tables=['[dbo].src1', 'dbo.src2']),
                                            ])
    export_to_yaml(inst, r'.\data\output')
    
    


    
