# -*- coding: utf-8 -*-
# @Time     : 2025/09/16
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


from util.headers import *
from util.names import *

from gurobipy import GRB
import gurobipy as gp
import math
import os
import datetime
import logging

logger = logging.getLogger(__name__)


class ModelBase:

    def __init__(self, model_name='default_m', model_data=None):

        if model_data is None:
            logger.error("Error: no model data provided")
            raise

        self.model_name = model_name
        self.data = model_data

        # create a new gurobi model
        self.model = gp.Model(self.model_name)
        self.model_relax = None                 # incase that we want to solve the relax model

        # initialize vars and results dict
        self.var, self.result = {}, {}

        # generate dict to save specific terms of objective functions
        self.obj_term = {}

        # initialize model status
        self.solve_status = ModelStatus.UNSOLVED

    def solve(self):
        logger.info("Start Solving model")
        self.model.optimize()

        if self.model.status == GRB.Status.OPTIMAL:
            self.solve_status = ModelStatus.SOLVED_OPT
            logger.info("Model solved with an optimal solution")

        elif self.model.status == GRB.Status.INFEASIBLE:
            self.solve_status = ModelStatus.INFEASIBLE
            logger.info("Model infeasible, IIS available")

        elif self.model.status in {GRB.Status.INF_OR_UNBD, GRB.Status.UNBOUNDED}:
            self.solve_status = ModelStatus.INF_OR_UNBD
            logger.info("Model infeasible or unbounded, and IIS not guaranteed")

        elif self.model.status == GRB.Status.TIME_LIMIT:
            if self.model.SolCount > 0:
                self.solve_status = ModelStatus.SOLVED_TIMEOUT_WS
                logger.info("Model timed out, feasible solution found")
            else:
                self.solve_status = ModelStatus.SOLVED_TIMEOUT_WOS
                logger.info("Model timed out, no feasible solution found")

        else:
            self.solve_status = f'{ModelStatus.UNKNOWN}_{self.model.status}'
            logger.info(f'An Unknown model status: {self.model.status}')
            raise

    def solve_relaxed(self):
        self.model_relax = self.model.relax()
        self.model_relax.optimize()

        if self.model_relax.status == GRB.Status.INFEASIBLE:
            logger.info("Relaxed Model infeasible, IIS available")

        elif self.model_relax.status in {GRB.Status.INF_OR_UNBD, GRB.Status.UNBOUNDED}:
            logger.info("Relaxed Model infeasible or unbounded, and IIS not guaranteed")

        else:
            logger.info(f'An Unknown model status for relaxed model: {self.model.status}')
            raise

    def get_result(self, var_name_list):

        # todo: check if the var names in the input var name list are valid

        logger.info(f'Get result for following variables: {var_name_list}')

        for var_name in var_name_list:
            self.result[var_name] = {}
            for key in sorted(self.var[var_name].keys()):
                self.result[var_name][key] = self.var[var_name][key].X
