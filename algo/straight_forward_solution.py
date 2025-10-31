# -*- coding: utf-8 -*-
# @Time     : 2025/10/04
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


from util.headers import *
from util.names import *
from util.project_logger import init_logger
from dao.data_reader import DataReader
from dao.data_processor import DataProcessor
from model import ModelMain, ModelSub, ModelCombined

import numpy as np
import pandas as pd
from datetime import datetime
from gurobipy import GRB
import logging
import os


logger = logging.getLogger(__name__)


class FullModel():

    def __init__(self, raw_data, obj_term_list, scenario_list, time_list):

        self.data_processor_module = DataProcessor(raw_data=raw_data)
        self.data = {}
        self.obj_term_list = obj_term_list
        self.scenario_list = scenario_list
        self.time_list = time_list
        self.model = None

    def process_data(self):
        self.data = self.data_processor_module.data_process(
            scenario_list_assigned=self.scenario_list,
            time_list_assigned=self.time_list
        )

    def build_model(self):
        self.model = ModelCombined(model_name='m_combined_test', model_data=self.data)
        self.model.build_model_given_obj_terms(input_term_list=self.obj_term_list)

    def solve_model(self):
        self.model.solve()
        self.model.cal_detailed_obj()

    def compute_obj_lb(self, scenario_list, time_list):
        self.process_data()
        self.build_model()
        self.model.solve_model()

        return self.model.obj_term_value
