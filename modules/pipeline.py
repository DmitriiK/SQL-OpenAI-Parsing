
import os

import modules.llm_communicator as llmc
from modules.data_classes import SP_CRUDs, CRUD_Statement, CRUD_Type
from pydantic_yaml import to_yaml_str

model = llmc.LLMCommunicator()


def export_to_yaml(inst: SP_CRUDs, dir: str = None, file_name: str = None):
    test_yml_str = to_yaml_str(inst)
    file_name = file_name or f'{inst.sp_name}.yaml'
    if dir:
        file_name = os.path.join(dir, file_name)
    with open(file_name, 'w') as yaml_file:
        yaml_file.write(test_yml_str)


def take_analyze_and_save():
    sql_script_path = r'D:\projects\DataFeedEngine\DataFeedEngineIndex\stg\Stored procedures\PullData_RussellUS2_IndexValue_prc.sql'

    with open(sql_script_path) as f:
        script = f.read()
    out = model.request_and_parse(script)
    print(out)
    
    
def test_yaml():
    sp_name = 'SP_CRUDs_example'
    inst = SP_CRUDs(sp_name=sp_name, cruds=[CRUD_Statement(target_table='[stg].[targ1]', crud_type=CRUD_Type.TRUNCATE),
                                            CRUD_Statement(target_table='[stg].[targ1]', crud_type=CRUD_Type.INSERT,
                                                           source_tables=['[dbo].src1', 'dbo.src2']),
                                            ])
    export_to_yaml(inst, r'.\data\output')
    
    


    
