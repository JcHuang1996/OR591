# -*- coding: utf-8 -*-
# @Time     : 2025/10/22
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


from util.headers import *
from util.names import *
from util.project_logger import init_logger
from dao.data_reader import DataReader
from dao.data_processor import DataProcessor
from model import ModelMain, ModelSub

import numpy as np
from gurobipy import GRB
import logging

init_logger()


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

# scenario_list = ['s_1', 's_2', 's_3', 's_4', 's_5', 's_6', 's_7', 's_8', 's_9', 's_10']
scenario_list = ['s_1', 's_2', 's_3']
time_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

main_model_data = DataProcessorModule.data_process(
    scenario_list_assigned=scenario_list,
    time_list_assigned=time_list
)
DataProcessorModule.clear_existing_data()

sub_model_data_dict = {}
for s in scenario_list:
    sub_model_data = DataProcessorModule.data_process(
        scenario_list_assigned=[s],
        time_list_assigned=time_list
    )
    sub_model_data_dict[s] = sub_model_data
    DataProcessorModule.clear_existing_data()

model_main = ModelMain(model_name='Main', model_data=main_model_data)
model_main.build_main_model()

bds_cut_cut_info_dict = {}

for ite_num in range(10):
    model_main.solve()
    curr_main_result = model_main.get_result([VarName.DG_RATED_POWER, VarName.LINE_HARDEN])
    logger.info(f'Current main obj: {model_main.model.ObjVal}')

    bds_cut_cut_info_dict[ite_num] = {}

    # build, solve and collect information from each subproblem corresponding to scenarios
    for s in scenario_list:

        # build the sub model for the given scenario in this iteration
        sce_sub_model_data = sub_model_data_dict[s]
        sce_sub_model = ModelSub(
            model_name=f'{s}_model',
            model_data=sce_sub_model_data,
            main_result=curr_main_result
        )
        sce_sub_model.build_sub_model()

        # update the model immediately,
        # in case that following operations (e.g. generating Relaxed Benders Optimality Cuts) requires an updated model
        sce_sub_model.update_model()

        # ===========================
        # Benders optimality cut
        # ===========================
        # solve sub model's LP relax for Benders optimality cut
        sce_sub_model.solve_relaxed()

        # compute the information for generating Benders optimality cut
        constant_term, var_coeff_dict = sce_sub_model.generate_info_benders_opt_cut()

        # record the benders cut info
        bds_cut_cut_info_dict[ite_num][s] = [constant_term, var_coeff_dict]

    # update the main model

    # add benders cuts by every scenario
    for s in scenario_list:
        model_main.add_constr_benders_opt_cut(
            scenario_idx=s,
            constant_term=bds_cut_cut_info_dict[ite_num][s][0],
            var_coef_dict=bds_cut_cut_info_dict[ite_num][s][1],
            track_idx=f'ite_{ite_num}'
        )
    model_main.reset_model()

model_main.solve()
curr_main_result = model_main.get_result([VarName.DG_RATED_POWER, VarName.LINE_HARDEN])
