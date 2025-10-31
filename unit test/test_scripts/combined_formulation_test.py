# -*- coding: utf-8 -*-
# @Time     : 2025/10/04
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


from util.headers import *
from util.names import *
from util.project_logger import init_logger
from dao.data_reader import DataReader
from dao.data_processor import DataProcessor
from model.model_combined import ModelCombined

import math
import logging


logger = logging.getLogger(__name__)

test_read_method = InputMethodName.LOCAL_CSV
test_file_path = '/Users/huangjiacheng/OR591/unit test/test_local_csv_file'
data_set_name = 'function test'

r = DataReader(
    read_method=test_read_method,
    local_file_path=test_file_path,
    data_set_name=data_set_name
)

r.read()
print("CSV read success:")

DataProcessorModule = DataProcessor(r.raw_data)
processed_data = DataProcessorModule.data_process(
    scenario_list_assigned=['s_1', 's_2', 's_3'],
    time_list_assigned=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
)

print('Data processing completed.')

m_combined = ModelCombined(model_name='m_combined_test', model_data=processed_data)
m_combined.build_model_all_obj_terms()
m_combined.solve()
m_combined.get_result([VarName.DG_INSTALL, VarName.LINE_CONNECTED])

print('Solved')