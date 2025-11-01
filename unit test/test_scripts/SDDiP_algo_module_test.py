# -*- coding: utf-8 -*-
# @Time     : 2025/10/27
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com
from turtledemo.clock import current_day

from flask import current_app

from util.headers import *
from util.names import *
from util.local_output import *
from util.project_logger import init_logger
from dao.data_reader import DataReader
from dao.data_processor import DataProcessor
from model import ModelMain, ModelSub, ModelCombined
from algo.SDDiP import SDDiP_planning
from algo.algo_simple_tools import *

import numpy as np
import pandas as pd
from datetime import datetime
from gurobipy import GRB
import logging
import os

# control whether to write running logs to log output folder
ENABLE_LOG_OUTPUT = False  # set to 'False' to disable log file creation

init_logger(enable_file_output=ENABLE_LOG_OUTPUT)

scenario_list = ['s_1', 's_2', 's_3']
time_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

logger = logging.getLogger(__name__)

test_read_method = InputMethodName.LOCAL_CSV
test_file_path = '/Users/huangjiacheng/OR591/unit test/test_local_csv_file'
data_set_name = 'function test'

timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'output', timestamp)
os.makedirs(output_dir, exist_ok=True)

r = DataReader(
    read_method=test_read_method,
    local_file_path=test_file_path,
    data_set_name=data_set_name
)

r.read()
print("CSV read success:")

SDDiP_module = SDDiP_planning(raw_data=r.raw_data, scenario_list=scenario_list, time_list=time_list)

# =========================================
# estimate the obj value lb for every scenario
# =========================================
obj_lb_dict = {}
single_s_optimal_main_result_dict = {}
for s in scenario_list:
    obj_lb_dict[s], single_s_optimal_main_result_dict[s] = SDDiP_module.sub_model_lb_estimator(sub_model_sce_list=[s])

# build the main model
SDDiP_module.build_main_stage_model()

# =========================================
# user-iteration
# cut generation are based on given main results
# =========================================

for s in sorted(single_s_optimal_main_result_dict.keys()):
    s_main_result = single_s_optimal_main_result_dict[s]
    ite_name = str('init' + s)
    SDDiP_module.execute_single_iteration(
        iteration_name=ite_name,
        est_sub_lb_dict=obj_lb_dict,
        given_main_result=s_main_result
    )

# =========================================
# free-iteration
# cut generation are only based on the solved main model
# =========================================

for ite_num in range(125):

    ite_name = str(ite_num)

    SDDiP_module.execute_single_iteration(
        iteration_name=ite_name,
        est_sub_lb_dict=obj_lb_dict
    )

iter_general_csv(
    ite_obj_value_dict=SDDiP_module.ite_obj_value_dict,
    output_dir=output_dir
)
iter_sub_prob_info(
    ite_obj_value_dict=SDDiP_module.ite_obj_value_dict,
    output_dir=output_dir,
    scenario_list=scenario_list
)

print('')


