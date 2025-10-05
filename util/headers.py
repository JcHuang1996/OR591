# -*- coding: utf-8 -*-
# @Time     : 2025/09/05
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com


# ===========================================
# All headers of input tables are stored here
# Decoupling the headers used in the program from headers of the original input
# Preventing errors caused by typo
# Helping checking headers' meanings
# ===========================================

class NodeHeader:
    NODE_ID = 'node_id'
    P_LOAD = 'Pload_MW'
    Q_LOAD = 'Qload_MW'


class BranchHeader:
    FROM_NODE = 'from_bus'
    TO_NODE = 'to_bus'
    R = 'R'
    X = 'X'
    INIT_STATE = 'init_state'
    POLE_NUMBER = 'pole_number'


class ScenarioProbHeader:
    SCENARIO_ID = 'scenario_id'
    SCENARIO_PROB = 'probability'


class ScenarioFaultLineHeader:
    SCENARIO_ID = 'scenario_id'
    FROM_NODE = 'from_bus'
    TO_NODE = 'to_bus'

class ScenarioLineStateHeader:
    SCENARIO_ID = 'scenario_id'
    TIME_IDX = 'time_idx'
    NATURE_HOUR = 'nature_hour'
    FROM_NODE = 'from_bus'
    TO_NODE = 'to_bus'
    STATE_NO_HARDEN = 'state_no_harden'
    STATE_HARDEN = 'state_harden'
    BROKEN_POLE_NUM_NO_HARDEN = 'broken_pole_num_no_harden'
    BROKEN_POLE_NUM_HARDEN = 'broken_pole_num_harden'


class ParameterHeader:
    PARAM = 'parameter'
    VALUE = 'value'


class ParameterKey:
    MODEL_FOR = 'model_for'
    LOAD_CURVE_CHOICE = 'load_curve_choice'

    LIFE_DG = 'life_dg'
    LIFE_BES = 'life_bes'
    LIFE_POLE_HARDEN = 'life_pole_harden'
    INTEREST_RATE = 'interest_rate'
    INFLATION_RATE = 'inflation_rate'
    ANNUAL_DISASTER_NUM = 'annual_disaster_num'

    DG_NUM_LIM = 'dg_num_lim'
    DG_COST_MW = 'dg_cost_MW'
    DG_CV = 'dg_kv'             # cost per MW, when DG_RATE_POWER is variable
    DG_CF = 'dg_kf'             # fixed cost, when DG_RATE_POWER is a fixed value
    DG_P_RATE = 'dg_p_rate'
    DG_P_MAX = 'dg_p_max'
    DG_P_MIN = 'dg_p_min'
    DG_ABLE_SET = 'dg_able_set'

    BES_NUM_LIM = 'bes_num_lim'
    BES_KP = 'bes_kp'
    BES_KE = 'bes_ke'
    BES_P_MAX = 'bes_p_max'
    BES_P_MIN = 'bes_p_min'
    BES_E_MAX = 'bes_e_max'
    BES_E_MIN = 'bes_e_min'
    BES_ABLE_SET = 'bes_able_set'

    POLE_HARDEN_COST = 'pole_harden_cost'
    POLE_HARDEN_NUM_UB = 'pole_harden_num_ub'
    POLE_REPAIR_COST = 'pole_repair_cost'

    INVEST_UB = 'invest_ub'

    DG_MAINTAIN = 'dg_maintain'
    BES_MAINTAIN = 'bes_maintain'
    C_DG_OPERATING = 'c_dg_operating'
    C_LOAD_SHED = 'c_load_shed'
    C_EQUITY = 'c_equity'
    SOC_UB = 'soc_ub'
    SOC_LB = 'soc_lb'
    SOC_T0 = 'soc_t0'
    EFF = 'eff'
    LIC = 'LIC'
    LIC_SVI = 'LIC_SVI'
    SC = 'SC'
    SC_Q_rate = 'SC_q_rate'
    SVC = 'SVC'
    SVC_CAP = 'SVC_cap'
    P_BASE = 'p_base'
    V_0 = 'v_0'
    V_MIN = 'v_min'
    V_MAX = 'v_max'
    S_MAX = 's_max'
    DG_PF_LB = 'dg_pf_lb'
    BES_PF_LB = 'bes_pf_lb'
    S_REDUCED = 's_reduced'

    MIN_RANGE_FOR_PH_HALTING = 'min_range_ph_halting'   # float, the max range of one continuous variable in all scenarios if PH can halt
    PH_PENALTY = 'ph_penalty'
    PH_CON_PENALTY = 'ph_con_penalty'
    PH_PENALTY_BI_EACH = 'ph_penalty_bi_each'
    PH_PENALTY_CON_EACH = 'ph_penalty_con_each'

    SLACK_NODE_IDX = 'slack_node'   # str, the index of the slack node of the system

class ModelForHeader:
    DG_ONLY = 'DG'
    DG_BES = 'DG_BES'
    DG_POLE = 'DG_POLE'
    DG_BES_POLE = 'DG_BES_POLE'

class PowerCurveHeader:
    TIME = 'Time'
    JAN = 'Jan'
    APR = 'Apr'
    JULY = 'July'
    OCT = 'Oct'

class ScenarioNodePowerHeader:
    SCENARIO_ID = 'scenario_id'
    NODE = 'node'
    P_LOAD_MW = 'P_LOAD_MW'
    Q_LOAD_MW = 'Q_LOAD_MW'


class PresentValueCoefHeader:
    PVC_DG = 'pvc_dg'
    PVC_BES = 'pvc_bes'
    PVC_POLE = 'pvc_pole'

class PHPenaltyHeader:
    DG_LOC = 'dg_loc'
    BES_LOC = 'bes_loc'
    HARDEN_LINE = 'harden_line'
    DG_PRT = 'dg_prt'
    BES_PRT = 'bes_prt'
    BES_ERT = 'bes_ert'