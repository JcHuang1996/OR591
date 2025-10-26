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

# abstract the scenario prob dict, just for convenience
scenario_prob_dict = main_model_data[DataName.DICT_SC_PROB].copy()

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

# ============================
# initializing the iteration data
# ============================

# the dict for collecting information of benders optimality cuts
bds_cut_cut_info_dict = {}

# the dict for collecting objective values
ite_obj_value_dict = {}

for ite_num in range(5):

    # the sub-dict collecting results of the current iteration
    ite_obj_value_dict[ite_num] = {}
    bds_cut_cut_info_dict[ite_num] = {}

    # =======================================================
    # solve the main model at the beginning of the iteration
    # =======================================================

    model_main.solve()
    model_main.cal_detailed_obj()

    # record the result of the main model required by the sub problems
    curr_main_result = model_main.get_result([VarName.DG_RATED_POWER, VarName.LINE_HARDEN])

    # show and record the main model objective value (the best bound objective value)
    best_bound_objective_value = model_main.model.ObjVal
    best_main_stage_objective_value = (
        model_main.obj_term_value[ObjName.DG_FIXED_COST]
        + model_main.obj_term_value[ObjName.DG_VARIANT_COST]
        + model_main.obj_term_value[ObjName.LINE_HARDEN_COST]
    )
    ite_obj_value_dict[ite_num]['main_obj(bound)'] = {
        'total': best_bound_objective_value,
        'detail': model_main.obj_term_value.copy()
    }
    logger.info(f'Current main obj: {best_bound_objective_value}')

    # the best incumbent objective value will be given by the weighted sum of sub-problem objective values
    # starting from 0
    best_incumbent_obj_value = 0

    # build, solve and collect information from each subproblem corresponding to scenarios
    for s in scenario_list:

        # ============================
        # build and solve sub problem models
        # ============================
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

        # solve the sub problem model
        sce_sub_model.solve()
        sce_sub_model.cal_detailed_obj()

        # collect the scenario's objective value.
        # Note: the 1st stage objective value is included.
        sce_obj_value = sce_sub_model.model.ObjVal + best_main_stage_objective_value
        best_incumbent_obj_value += sce_obj_value * scenario_prob_dict[s]
        ite_obj_value_dict[ite_num][s] = {'total': sce_obj_value, 'detail': sce_sub_model.obj_term_value.copy()}

        # ===========================
        # generating Benders optimality cut
        # ===========================
        # solve sub model's LP relax for Benders optimality cut
        sce_sub_model.solve_relaxed()

        # compute the information for generating Benders optimality cut
        constant_term, var_coeff_dict = sce_sub_model.generate_info_benders_opt_cut()

        # record the benders cut info
        bds_cut_cut_info_dict[ite_num][s] = [constant_term, var_coeff_dict]

    # ===============================
    # summarize the current iteration
    # ===============================
    ite_obj_value_dict[ite_num]['sub_obj(best_incumbent)'] = {
        'sub_p_total': best_incumbent_obj_value
    }

    # ===============================
    # update the main model
    # ===============================

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
