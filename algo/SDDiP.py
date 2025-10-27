# -*- coding: utf-8 -*-
# @Time     : 2025/10/27
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com

from util.headers import *
from util.names import *
from util.project_logger import init_logger
from dao.data_reader import DataReader
from dao.data_processor import DataProcessor
from model import ModelMain, ModelSub

import numpy as np
import pandas as pd
from datetime import datetime
from gurobipy import GRB
import logging
import os

init_logger()


logger = logging.getLogger(__name__)


class SDDiP_planning():

    def __init__(self, raw_data, time_list, scenario_list):

        self.data_processor_module = DataProcessor(raw_data=raw_data)
        self.time_list = time_list
        self.scenario_list = scenario_list

        self.main_model_data, self.sub_model_data_dict = {}, {}

        self.sce_prob_dict = {}

        self.model_main = None

        # the dict for collecting information of benders optimality cuts
        self.bds_cut_cut_info_dict = {}

        # the dict for collecting objective values
        self.ite_obj_value_dict = {}

    def build_main_stage_model(self):

        # process the data for main model
        self.main_model_data = self.data_processor_module.data_process(
            scenario_list_assigned=self.scenario_list,
            time_list_assigned=self.time_list
        )
        self.data_processor_module.clear_existing_data()

        self.sce_prob_dict = self.main_model_data[DataName.DICT_SC_PROB].copy()

        # build the main model with processed main model data
        self.model_main = ModelMain(model_name='Main', model_data=self.main_model_data)
        self.model_main.build_main_model()

    def solve_and_record_main_stage_model(self, ite_name=None):
        self.model_main.solve()
        self.model_main.cal_detailed_obj()

        # show and record the main model objective value (the best bound objective value)
        best_bound_objective_value = self.model_main.model.ObjVal
        best_main_stage_objective_value = (
                self.model_main.obj_term_value[ObjName.DG_FIXED_COST]
                + self.model_main.obj_term_value[ObjName.DG_VARIANT_COST]
                + self.model_main.obj_term_value[ObjName.LINE_HARDEN_COST]
        )

        # create the corresponding dict if
        if ite_name not in self.ite_obj_value_dict:
            self.ite_obj_value_dict[ite_name] = {}

        # record the objective value and values of every terms
        self.ite_obj_value_dict[ite_name]['main_obj(bound)'] = {
            'total': best_bound_objective_value,
            'detail': self.model_main.obj_term_value.copy()
        }

        return best_main_stage_objective_value

    def build_sub_model(self, sub_model_sce_list=None, given_main_result=None):
        """
        The function iterates one round on the given scenarios based on the given main result.
        :param
        sub_model_sce_list: the list of scenarios considered in this sub model.
        given_main_result: the main stage result for current iteration
        :return:
        """

        # the sub model's scenario cannot be empty
        if sub_model_sce_list is None:
            raise ValueError('sub_model_sce_list cannot be None')

        # process the sub model data
        sub_model_data = self.data_processor_module.data_process(
            scenario_list_assigned=sub_model_sce_list,
            time_list_assigned=self.time_list
        )
        self.data_processor_module.clear_existing_data()

        # ============================
        # build and solve sub problem models
        # ============================
        # build the sub model for the given scenario(s) in this iteration
        sce_sub_model = ModelSub(
            model_name=f'{tuple(sub_model_sce_list)}_model',
            model_data=sub_model_data,
            main_result=given_main_result
        )
        sce_sub_model.build_sub_model()

        # update the model immediately,
        # in case that following operations (e.g. generating Relaxed Benders Optimality Cuts) requires an updated model
        sce_sub_model.update_model()

        return sce_sub_model

    def solve_and_record_sub_model(self, sub_model_sce_list=None, sub_model=None, main_stage_obj_value=None, ite_name=None):
        # solve the sub problem model
        sub_model.solve()
        sub_model.cal_detailed_obj()

        # solve the sub problem model
        sub_model.solve()
        sub_model.cal_detailed_obj()

        # collect the scenario's objective value.
        # Note: the 1st stage objective value is included.
        sce_obj_value = sub_model.model.ObjVal + main_stage_obj_value

        # create the corresponding dict if
        if ite_name not in self.ite_obj_value_dict:
            self.ite_obj_value_dict[ite_name] = {}

        self.ite_obj_value_dict[ite_name][tuple(sub_model_sce_list)] = {
            'total': sce_obj_value,
            'detail': sub_model.obj_term_value.copy()
        }

        return sce_obj_value

    def generate_benders_opt_cut(self, sub_model, sub_model_sce_list=None, ite_name=None):

        # solve sub model's LP relax for Benders optimality cut
        sub_model.solve_relaxed()

        # compute the information for generating Benders optimality cut
        constant_term, var_coeff_dict = sub_model.generate_info_benders_opt_cut()

        if ite_name not in self.bds_cut_cut_info_dict:
            self.bds_cut_cut_info_dict[ite_name] = {}

        # record the benders cut info
        self.bds_cut_cut_info_dict[ite_name][tuple(sub_model_sce_list)] = [constant_term, var_coeff_dict]

    def add_benders_cut(self, sub_model_sce_list=None, ite_name=None):
        sub_model_key = tuple(sub_model_sce_list)
        self.model_main.add_constr_benders_opt_cut(
            sub_problem_sce_list=sub_model_sce_list,
            constant_term=self.bds_cut_cut_info_dict[ite_name][sub_model_key][0],
            var_coef_dict=self.bds_cut_cut_info_dict[ite_name][sub_model_key][1],
            track_idx=f'i_{ite_name}'
        )
        self.model_main.reset_model()





