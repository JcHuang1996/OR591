# -*- coding: utf-8 -*-
# @Time     : 2025/10/27
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


from util.headers import *
from util.names import *
from util.local_output import *
from util.project_logger import init_logger
from dao.data_reader import DataReader
from dao.data_processor import DataProcessor
from model import ModelMain, ModelSub
from algo.SDDiP import SDDiP_planning

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

# build the main model
SDDiP_module.build_main_stage_model()

for ite_num in range(5):

    ite_name = str(ite_num)

    # =======================================================
    # solve the main model at the beginning of the iteration
    # =======================================================
    best_main_stage_obj_value = SDDiP_module.solve_and_record_main_stage_model(ite_name=ite_name)

    # record the result of the main model required by the sub problems
    curr_main_result = SDDiP_module.model_main.get_result([VarName.DG_RATED_POWER, VarName.LINE_HARDEN])

    # the best incumbent objective value will be given by the weighted sum of sub-problem objective values
    # starting from 0
    best_incumbent_obj_value = 0

    # ============================
    # using the current main result, iterating scenarios
    # ============================

    # decide how to group and iterate the scenarios
    sce_group_list = [
        [s] for s in scenario_list
    ]

    # iterating by the above division
    for sub_sce_list in sce_group_list:

        # ============================
        # build and solve the corresponding sub problem model
        # ============================

        # build the sub model
        curr_sub_model = SDDiP_module.build_sub_model(
            sub_model_sce_list=sub_sce_list,
            given_main_result = curr_main_result
        )

        # solve the sub model and update the objective record, including the detailed record in the algo module
        sub_obj_value = SDDiP_module.solve_and_record_sub_model(
            sub_model_sce_list=sub_sce_list,
            sub_model=curr_sub_model,
            main_stage_obj_value=best_main_stage_obj_value,
            ite_name=ite_name
        )
        best_incumbent_obj_value += sub_obj_value * sum(
            SDDiP_module.sce_prob_dict[s_idx]
            for s_idx in sub_sce_list
        )

        # ===========================
        # generating Benders optimality cut
        # ===========================
        SDDiP_module.generate_benders_opt_cut(
            sub_model=curr_sub_model,
            sub_model_sce_list=sub_sce_list,
            ite_name=ite_name
        )

    # ===============================
    # Operations after the solving process
    # ===============================

    # summarize the current iteration record
    SDDiP_module.ite_obj_value_dict[ite_name]['sub_obj(best_incumbent)'] = {
        'sub_p_total': best_incumbent_obj_value
    }

    # update the main model:

    # adding benders cuts from all scenarios
    for sub_sce_list in sce_group_list:
        SDDiP_module.add_benders_cut(
            sub_model_sce_list=sub_sce_list,
            ite_name=ite_name
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


