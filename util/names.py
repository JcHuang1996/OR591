# -*- coding: utf-8 -*-
# @Time     : 2025/09/05
# @Author   : J. Huang
# @Email    : jiachenghuang0601@gmail.com

# ============================================================
# Save all names for important vars used in the code here
# To change any name in the code, change the name here
# To check the detail of any vars, check it here
# Preventing errors caused by typo
# Helping checking the variables/datas' meanings
# ============================================================

# ============================================================
# Notations
# AFN: short for 'Algo File Notations', the notation of corresponding content in the algo file.
# ============================================================

class ModelStatus:
    SOLVED_OPT = 'opt'                                  # model is solved and an optimal solution (including solution within required gap) is found
    SOLVED_TIMEOUT_WS = 'timeout_with_s'                # time out, and a feasible solution is found
    SOLVED_TIMEOUT_WOS = 'timeout_without_s'            # time out, and no feasible solution is found
    UNSOLVED = 'unsolved'                               # model is not solved yet
    INFEASIBLE = 'infeasible'                           # model is infeasible. IIS can be solved.
    INF_OR_UNBD = 'inf_or_unbd'                         # model is infeasible or unbounded. No iis guaranteed
    UNKNOWN = 'unknown'                                 # prefix of an unknown model status


class InputMethodName:
    LOCAL_CSV = 'local_csv'                             # read input data from local csv file


class InputDataName:
    PARAMETERS_DICT = 'parameters_dict'                 # dict, all parameters of the model
    NODE_DF = 'node_df'                                 # dataframe, node data
    BRANCH_DF = 'branch_df'                             # dataframe, branch data
    POWER_CURVE_DF = 'power_curve_df'                   # dataframe, power curve
    SCENARIO_NODE_LOAD_DF = 'scenario_node_load_df'     # dataframe, power of each node with normal distribution fluctuation
    SCENARIO_PROB_DF = 'scenario_prob_dict'             # dataframe, prob of all scenario

    SCENARIO_FAULT_LINE_DF = 'scenario_fault_line_df'   # detaframe, fault line scenario

    SCENARIO_LINE_STATE_WO_HARDEN_DF = 'scenario_line_state_wo_harden_df'   # dataframe, line state at each time idx in each scenario with/without line harden
    SCENARIO_TIME_IDX_HOUR_DF = 'scenario_time_idx_hour_df'     # dataframe, (time idx - nature hour) correspondence in each scenario


class DataName:
    # === Set ===
    LIST_SCENARIO = 'list_scenario'                     # list, [sc_1, sc_2, ...], the set of all scenarios. AFN: S
    LIST_NODE = 'list_node'                             # list, [node_1, node_2, ...], the set of all nodes. AFN: J
    LIST_LINE = 'list_line'                             # list, [(i, j), ...], the set of all lines. AFN: L
    LIST_TIME = 'list_time'                             # list, [t1, t2, ...], the set of all time slots. AFN: T

    # === Parameters / Data ===
    NUM_DG_UB = 'dg_ub'                                 # integer, upperbound on number of generators. AFN: \overline{N^{G}} key: dg_num_lim
    DICT_SC_PROB = 'dict_scenario_prob'                 # dict, {sc_1: float, ...}, probability of each scenario. AFN: P_s
    DICT_DG_COST_FIX = 'dict_dg_cost_fix'               # dict, {j: float, ...}, fixed cost of installing DG at node j. AFN: C^{Gf}_j
    DICT_DG_COST_VAR = 'dict_dg_cost_var'               # dict, {j: float, ...}, variable cost of installing DG at node j. AFN: C^{Gv}_j
    DICT_DG_COST_UNIT = 'dict_dg_cost_unit'             # dict, {j: float, ...}, unit cost of generating power at node j. AFN: C^{Gu}_j
    DICT_DG_ALPHA_UB = 'dict_dg_alpha_ub'               # dict, {j: float, ...}, power factor upperbound of DG at node j. AFN: \Alpha^{G}_j
    DICT_LINE_COST_HARDEN = 'dict_line_cost_harden'     # dict, {(i,j): float, ...}, fixed cost of hardening line (i,j). AFN: C^{H}_{ij}
    DICT_LINE_RESISTANCE = 'dict_line_resistance'       # dict, {(i,j): float, ...}, resistance of line (i,j). AFN: R_{ij}
    DICT_LINE_REACTANCE = 'dict_line_reactance'         # dict, {(i,j): float, ...}, reactance of line (i,j). AFN: X_{ij}
    DICT_LINE_HEALTHY = 'dict_line_healthy'             # dict, {(i,j,t,s): status_binary, ...}, healthy status of line (i,j) at time t in scenario s. AFN: H_{ijts} column: state_no_harden
    NUM_VOLTAGE_LB = 'voltage_lb'                       # float, lower bound of bus voltage. AFN: \underline{V} key: v_min
    NUM_VOLTAGE_UB = 'voltage_ub'                       # float, upper bound of bus voltage. AFN: \overline{V} key: v_max
    NUM_VOLTAGE_SLACK = 'voltage_slack'                 # float, slack bus voltage. AFN: V_0 key: v_0
    DICT_LINE_THERMAL_UB = 'dict_line_thermal_ub'       # dict, {(i,j): float, ...}, thermal limit of line (i,j). AFN: \overline{S_{ij}}
    DICT_NODE_CHILDREN = 'dict_node_children'           # dict, {j: [child_nodes1, ...], ...}, child neighbors of node j. AFN: \Theta_j
    DICT_NODE_PARENTS = 'dict_node_parents'             # dict, {j: [parent_nodes1, ...], ...}, parent neighbors of node j. AFN: \Pi_j
    #
    # # --- Quote note from algo file ---
    # # Note: just using one 'all neighbors of node j' is sufficient, as it is formulated as an undirected graph.
    # # We divide into 'child' and 'parent' only for coding convenience.
    # # Given nodes i and j, implementing (i, j) = (j, i) is more complex,
    # # while only defining (i, j) and ensuring i ∈ Θ_j or Π_j is easier.
    #
    DICT_DEMAND_ACTIVE = 'dict_demand_active'           # dict, {(j,t,s): float, ...}, active power demand at node j at time t in scenario s. AFN: D^{p}_{jts}
    DICT_DEMAND_REACTIVE = 'dict_demand_reactive'       # dict, {(j,t,s): float, ...}, reactive power demand at node j at time t in scenario s. AFN: D^{q}_{jts}
    NUM_COST_SHED = 'cost_shed'                         # float, cost of load shedding. AFN: C^{L} key: c_load_shed
    #
    # # Important values and coefficient
    NUM_TOTAL_POWER = 'total_power'                     # num, the total power demand in the system
    SLACK_NODE_IDX = 'slack_node_idx'                   # num/str, the slack node's index in list of nodes


class VarName:
    # === Main Variables ===
    SUB_OBJ_VALUE = 'eta'               # Continuous, η_s value of the subproblem objective in scenario s. AFN: \eta_{s}
    DG_INSTALL = 'xg'                   # Binary, xg_j indicating whether DG is installed at node j. AFN: x^{G}_{j}
    LINE_HARDEN = 'xl'                  # Binary, xl_ij indicating whether line (i,j) is hardened. AFN: x^{L}_{ij}
    DG_RATED_POWER = 'pgrt'             # Continuous, pgrt_j the rated power capacity of DG at node j. AFN: p^{Grt}_{j}

    # === Sub Variables ===
    LINE_CONNECTED = 'yc'               # Binary, yc_ijts indicating whether line (i,j) is connected at time t in scenario s. AFN: y^{C}_{ijts}
    LOAD_SHED_RATIO = 'yl'              # Continuous, yl_jts percentage of load shed at node j at time t in scenario s. AFN: y^{L}_{jts}
    BUS_VOLTAGE = 'v'                   # Continuous, v_jts bus voltage magnitude at node j at time t in scenario s. AFN: v_{jts}
    DG_ACTIVE_POWER = 'pg'              # Continuous, pg_jts active power generation of DG at node j at time t in scenario s. AFN: p^{G}_{jts}
    DG_REACTIVE_POWER = 'qg'            # Continuous, qg_jts reactive power generation of DG at node j at time t in scenario s. AFN: q^{G}_{jts}
    LINE_ACTIVE_FLOW = 'p'              # Continuous, p_ijts active power flow on line (i,j) at time t in scenario s. AFN: p_{ijts}
    LINE_REACTIVE_FLOW = 'q'            # Continuous, q_ijts reactive power flow on line (i,j) at time t in scenario s. AFN: q_{ijts}

    # --- Virtual / Topology-related variables ---
    VIRTUAL_LINE_FLOW = 'ul'            # Continuous, ul_ijts virtual flow on line (i,j) at time t in scenario s. AFN: u^{L}_{ijts}
    VIRTUAL_SOURCE_INDICATOR = 'us'     # Binary, us_jts indicating whether node j is virtual source at time t in scenario s. AFN: u^{S}_{jts}
    VIRTUAL_INJECT_POWER = 'ui'         # Continuous, ui_jts virtual power injected from virtual source at node j at time t in scenario s. AFN: u^{I}_{jts}


class ConstrName:
    # === Main Problem Model Constraints ===
    DG_UPPERBOUND = 'dg_ub'                             # AFN: Generator number upperbound
    OPTIMAL_CUT = 'opt_cut'                             # AFN: Optimal Cut (generated by solving sub-problems)

    # === Sub-problem Model Constraints ===
    # Line connectivity
    LINE_CONNECTED = 'line_conn'                        # AFN: Line connected condition

    # System topology constraints
    VIRTUAL_FLOW_BAL_C1 = 'virt_flow_c1'                # AFN: Virtual power flow balance (eq. 1)
    VIRTUAL_FLOW_BAL_C2 = 'virt_flow_c2'                # AFN: Virtual power flow balance (eq. 2)

    VIRTUAL_INJECTION_UB = 'virt_inj_ub'                # AFN: Virtual power injection upperbound
    NO_VIRTUAL_ON_OPEN = 'virt_no_open'                 # AFN: No virtual flow on open line
    RADIALITY = 'radiality'                             # AFN: Radiality

    # DG operating constraints
    DG_ACTIVE_POWER_UB = 'dg_p'                         # AFN: Amount of generated active power
    DG_REACTIVE_POWER_UB = 'dg_q'                       # AFN: Amount of generated reactive power

    # System operating constraints
    VOLTAGE_RANGE_C1 = 'volt_rng_c1'                    # AFN: Voltage range (lower bound)
    VOLTAGE_RANGE_C2 = 'volt_rng_c2'                    # AFN: Voltage range (upper bound)
    VOLTAGE_SLACK_BUS = 'slack_bus'                     # AFN: Slack bus voltage equality

    VOLTAGE_FLOW_REL = 'volt_flow'                      # AFN: Voltage - flow relationships

    FLOW_BALANCE_C1 = 'flow_bal_p'                      # AFN: Flow balance (active power)
    FLOW_BALANCE_C2 = 'flow_bal_q'                      # AFN: Flow balance (reactive power)

    NO_FLOW_ON_OPEN_C1 = 'no_flow_open_p'               # AFN: No flow on open line (active)
    NO_FLOW_ON_OPEN_C2 = 'no_flow_open_q'               # AFN: No flow on open line (reactive)

    LINE_THERMAL_C1 = 'thermal_c1'                      # AFN: Linearized thermal limitation (part 1)
    LINE_THERMAL_C2 = 'thermal_c2'                      # AFN: Linearized thermal limitation (part 2)
    LINE_THERMAL_C3 = 'thermal_c3'                      # AFN: Linearized thermal limitation (part 3)


# class MGDataName:
#     # node
#     NODE_LIST = 'node_list'                             # list, [node_1, ...], all nodes in the model
#
#     # branch
#     BRANCH_LIST = 'branch_list'                         # list, [(start_node1, end_node1), ...], all directed line in the model
#     BRANCH_R_DICT = 'branch_r_dict'                     # dict, {(from_node, to_node): R_ij}
#     BRANCH_X_DICT = 'branch_x_dict'                     # dict, {(from_node, to_node): X_ij}
#     BRANCH_INIT_STATE_DICT = 'branch_init_state_dict'   # dict, {(from_node, to_node): init_state}
#     BRANCH_INIT_CONNECTED_LIST = 'branch_init_connected_list'           # list, [(start_node1, end_node1), ...], branches that initially connected
#     BRANCH_INIT_NOT_CONNECTED_LIST = 'branch_init_not_connected_list'   # list, [(start_node1, end_node1), ...], branches that initially not connected
#     BRANCH_POLE_NUMBER_DICT = 'branch_pole_number_dict' # dict, {(from_node, to_node): pole_number}
#
#     # scenario: list and prob
#     SCENARIO_LIST = 'scenario_list'                     # list, [s_1, ...], all scenario
#     SCENARIO_PROB_DICT = 'scenario_prob_dict'           # dict, {s_1: probability}
#
#     # # scenario: fault line (for DG_only siting)
#     # SCENARIO_LINE_DICT = 'scenario_line_dict'           # dict, {s_1: [(start_node1, end_node1), ...], ...},
#     #                                                     # the list of lines needed to be considered in given scenario
#     # # Note: (for DG_only siting)
#     # # term 'line' indicates healthy line in each scenario, term 'branch' indicates the edges in the full graphs
#     # # In a scenario, only healthy lines need to consider
#
#     # scenario: line status (for line hardening)
#     TIME_IDX_DICT = 'time_idx_dict'                     # dict, {s_1: [t_1, t_2,...], ...,}
#     TIME_IDX_HOUR_DICT = 'time_idx_hour_dict'           # dict, {(t_1, s_1): nature hour, ....}
#     TIME_STEP_VALUE = 'time_step_value'                 # single value, default = 1
#                                                         # get from first scenario: TIME_DICT[(t_2, s_1)] - TIME_DICT[(t_1, s_1)] (if<0, add 24)
#                                                         # check in data_processor, make sure all scenario share the same time step
#     HARDEN_CHOICE_LIST = 'harden_choice_list'           # list, [non_harden, harden] for now
#                                                         # if have multiple harden ways, additional lines can be added
#     SCENARIO_LINE_STATUS_DICT = 'scenario_line_status_dict'
#                                                         # dict, {(harden_choice, line_ij,time_t,s): healthy_state_h,ij,t,s}
#     SCENARIO_BROKEN_POLE_NUM_DICT = 'scenario_broken_pole_num_dict'
#                                                         # dict, {(harden_choice, line_ij,s): broken_pole_number_(h,ij,s)}
#
#     # scenario: load demand of each node
#     P_LOAD_NODE_DICT = 'p_load_node_dict'               # dict, {(node_j, time_idx, scenario): P_load_j,t,s}
#     Q_LOAD_NODE_DICT = 'q_load_node_dict'               # dict, {(node_j, time_idx, scenario): Q_load_j,t,s}
#
#     # power curve
#     POWER_CURVE_DICT = 'power_curve_dict'               # dict, {clk_1: load_1, ..., clk_24: load_23}
#     HOUR_LIST = 'hour_list'                             # list, ['clk_1', 'clk_1',..., 'clk_24'], for power curve
#
#     # parameters
#     PARA_DICT = 'para_dict'                             # dict, all parameters of the model, checked
#
#     Q_C_RATE_DICT = 'q_c_rate_dict'                     # dict, {node_j: Q_C_rt} (without SC: set 0)
#     SVC_CAP_DICT = 'svc_cap_dict'                       # dict, {node_i: SVC_cap} (without SVC: set 0)
#     SC_LIST = 'sc_list'                                 # list, shunt compensator list
#     SVC_LIST = 'svc_list'                               # list, static var compensator location list
#
#     LIC_LIST = 'lic_list'                               # list, LIC node list, get from parameter.csv
#     LIC_SVI_DICT = 'lic_svi_dict'                       # dict, {node_j: LIC_SVI} (only for LIC_node)
#     EQUITY_COST_COEF_DICT = 'equity_cost_coef_dict'     # dict, {node_j: c_equity * LIC_SVI_DICT[node_j]} (only for LIC_node)
#
#     PVC_DICT = 'pvc_dict'                               # dict, {DG: pvf_dg, BES: pvf_bes}, present value coefficient, for levelizing annual capital cost
#     DG_ABLE_LIST = 'dg_able_list'                       # list, nodes that are able to settle DG, sum of LIC node and DG able nodes from parameter.csv
#     BES_ABLE_LIST = 'bes_able_list'                     # list, nodes that are able to settle BES, sum of LIC node and BES able nodes from parameter.csv
#
#     VAR_KEY_DICT = 'var_key_dict'                       # dict, the list of keys (a tuple or a string) of a given variable, e.g. {var_name1: [var_name_key_1, ...]}
#     PH_PENALTY = 'ph_penalty'                           # dict, penalty value of each 1-stage variable, {x_G: penalty1, x_B: penalty2...}
#
#
# class MGVarName:
#     # stage-1 variables
#     DG_LOCATION = 'dg_location'                         # {node_j: xG_j}, binary, indicating the existence of DG at node j
#     DG_RATE_POWER = 'dg_rate_power'                     # {node_j: P_Grt_j}, rated power of DG at node j
#
#     BES_LOCATION = 'bes_location'                       # {node_j: xB_j}, binary, indicating the existence of BES at node j
#     BES_RATE_POWER = 'bes_rate_power'                   # {node_j: P_Brt_j}, rated power of BES at node j
#     BES_RATE_ENERGY = 'bes_rate_energy'                 # {node_j: E_Brt_j}, rated energy of BES at node j
#
#     HARDEN_LINE = 'harden_line'                         # {line_ij: xH_ij}, binary, indicating whether harden line_ij or not
#
#
#     # stage-2 variables
#     STAGE2_COST = 'stage2_cost'                         # {scenario_s: f}, second stage cost in scenario_s
#
#     # PSE and load shed
#     LOAD_SHED_PERCENT = 'load_shed_percent'             # {(node_j,time_t,s): y_j,t,s}, load shed percentage
#     DELTA_PSE = 'delta_PSE'                             # {(LIC_at_node_j,s): delta_j}, shortfall of PSE for LIC_j in scenario s, only for the node in LIC_LIST list
#     PSE = 'PSE'                                         # {(node_j,s): PSE_j}, percentage of served energy (PSE)
#     PSE_SYS = 'pse_sys'                                 # {(s): PSE_sys_j}, percentage of served energy (PSE) of whole system
#
#     # DG output
#     P_DG = 'p_dg'                                       # {(node_j,time_t,s): P_G_j,t,s}, DG active output
#     Q_DG = 'q_dg'                                       # {(node_j,time_t,s): Q_G_j,t,s}, DG reactive output
#
#     # battery related
#     S_BES_P = 's_bes_p'                                 # {(node_j,time_t,s): s+_j,t,s}, BES_j is discharging or not
#     S_BES_N = 's_bes_n'                                 # {(node_j,time_t,s): s-_j,t,s}, BES_j is charging or not
#     P_BES_P = 'p_bes_p'
#     P_BES_N = 'p_bes_n'
#     P_BES = 'p_bes'
#     Q_BES = 'q_bes'
#     E_BES = 'e_bes'
#
#     # line harden related
#     LINE_HEALTH = 'line_health'                         # {(line_ij,time_t,s): s_ij,t,s}, binary, indicating connected/disconnected state of a line
#
#     # line connection
#     SWITCH_CMD = 'switch_cmd'                           # {(line_ij,time_t,s): s_ij,t,s}, binary, indicating ON/OFF command of line switch
#     # LINE_CONNECTION = 'line_connection'                 # binary variable indicating connected/open state of line, same with SWITCH_CDM, since 'line' are all healthy
#     VIRTUAL_FLOW = 'virtual_flow'                       # {(line_ij,time_t,s): vl_ij,t,s},  vl, virtual power on line(i,j)
#     VIRTUAL_SOURCE = 'virtual_source'                   # {(node_j,time_t,s): vs_j,t,s},   vs, binary, indicating the node is virtual source or not
#     VIRTUAL_POWER_INJECT = 'virtual_power_inject'       # {(node_j,time_t,s): vp_j,t,s},   vp, virtual power injected in node
#     VIRTUAL_AUXILIARY = 'virtual_auxiliary'             # {(node_j,time_t,s): v_j,t,s},     v = vs*vp, for linearization
#
#     # Q compensation
#     Q_SC = 'q_sc'                                       # {(node_j, time_t, s): Q_C_j,t,s}, shunt compensator Q output
#     Q_SVC = 'q_svc'                                     # {(node_j, time_t, s): Q_SVC_j,t,s}, SVC compensator Q output
#
#     # power balance
#     P_INJECT_NODE = 'p_inject_node'
#     Q_INJECT_NODE = 'q_inject_node'
#
#     P_LINE = 'p_line'                                   # {(line_ij,time_t,s): P_ij,t,s}, active power in the line
#     Q_LINE = 'q_line'                                   # {(line_ij,time_t,s): Q_ij,t,s}, reactive power in the line
#     V_NODE = 'v_node'                                   # {(node_j,time_t,s): V_j,t,s}, node voltage
#                                                         # in p.u., should *V_ref in voltage calculation
#     V_DEVIATION_ABS = 'v_deviation_abs'                 # {(node_j,time_t,s): V_deviation_j,t,s}, deviation of node voltage = |V_j - V_0|
#     PH_BENCHMARK_ABS = 'ph_benchmark_abs'
#
#
# class MGLinExprName:
#     INVEST_DG = 'invest_dg'
#     INVEST_BES = 'invest_bes'
#     INVEST_POLE_HARDEN = 'invest_pole_harden'
#
#     SWITCH_CMD_UB = 'switch_cmd_ub'
#
#     # stage1 objective function and its components
#     OBJ_FUNCTION = 'obj_function'               # overall stage1 obj = OBJ_STAGE1_ALL + (lin_expr.OBJ_STAGE2_COST or var.STAGE2_COST)
#     OBJ_STAGE1_ALL = 'obj_stage1_all'           # overall obj excluding stage2 cost part
#     OBJ_STAGE2_COST = 'obj_stage2_cost'         # only effective in direct_run(), stage2 expectation in overall obj
#     OBJ_ANNUAL_CAP_DG = 'obj_annual_cap_dg'     # dg part in stage1 obj
#     OBJ_PERTURBATION_DG = 'obj_perturbation_dg'
#     OBJ_ANNUAL_CAP_BES = 'obj_annual_cap_bes'   # bes part in stage1 obj
#     OBJ_PERTURBATION_BES = 'obj_perturbation_bes'
#     OBJ_ANNUAL_CAP_POLE = 'obj_annual_cap_pole'  # line harden part in stage1 obj
#     OBJ_PERTURBATION_POLE = 'obj_perturbation_pole'
#
#     # stage2 cost components, {scenario: scenario_expression}
#     STAGE2_COST_DG_OPERATION = 'stage2_cost_dg_operation'
#     STAGE2_COST_LOAD_SHED = 'stage2_cost_load_shed'
#     STAGE2_COST_EQUITY = 'stage2_cost_equity'
#     STAGE2_COST_VOLTAGE = 'stage2_cost_voltage'
#     STAGE2_COST_SWITCH = 'stage2_cost_switch'
#
#     STAGE2_COST_POLE_REPAIR = 'stage2_cost_pole_repair'
#
#     # only for PH
#     PH_OBJ_VALUE = 'ph_obj_value'       # obj value with PH add-on items
#     PH_OBJ_WEIGHTED_X = 'ph_obj_weighted_x'
#     PH_OBJ_PENALTY_ABS_X_BI = 'ph_obj_penalty_abs_x_bi'
#     PH_OBJ_PENALTY_ABS_X_CON = 'ph_obj_penalty_abs_x_con'
#
# class MGVarResultName:
#     OBJ_DG_OPERATION_EXP = 'obj_dg_operation_exp'       # expectation considering all scenarios
#     OBJ_LOAD_SHED_EXP = 'obj_load_shed_exp'
#     OBJ_EQUITY_EXP = 'obj_equity_exp'
#     OBJ_POLE_REPAIR_EXP = 'obj_pole_repair_exp'
#     OBJ_VOLTAGE_EXP = 'obj_voltage_exp'
#
#
# class MGDebugChoiceName:
#     DATA_INVEST_UNLIMITED = 'data_invest_UNLIMITED' # inf invest limit
#
#     DG_LIMITED_SITE = 'dg_limited_site'     # 0 - all nodes can site a DG
#                                             # 1 - only nodes in self.data[MGDataName.DG_ABLE_LIST] can have DG
#     BES_LIMITED_SITE = 'bes_limited_site'   # 0 - all nodes can site a BES
#                                             # 1 - only nodes in self.data[MGDataName.BES_ABLE_LIST] can have BES
#     IF_USE_LINE_HEALTH_VAR = 'if_use_line_health_var'   # 0 - do not define & use self.var[MGVarName.LINE_HEALTH]
#                                                         # 1 - define & use
#     IF_REWRITE_BES_EQ = 'if_rewrite_bes_eq' # 0 - original eq.(6c) expression
#                                             # 1 - rewrite to avoid binary chain logic
#     EQUITY_CONSTRAINT = 'equity_constraint' # 0 - PSE_LIC + delta >= sum(PSE)/N
#                                             # 1 - PSE_LIC + delta >= PSE_sys
#
#     # currently, only under MGDebugChoiceName.IF_USE_LINE_HEALTH_VAR == 0
#     ENABLE_HEALTH_LINE_DISCONNECT = 'enable_health_line_disconnect'
#                                             # 1 - healthy line can be disconnected, y_ij <= h_ij
#                                             # 0 - healthy line should be connected, only decide tie-line connectivity
#
#     # currently, only use in PH
#     # do not have any iterations, all decisions settled, mainly used for operation_without equity (old)
#     APPLY_RESULTS = 'apply_results'         # 1 - fill the planning results (stage1 decisions) in model, for getting planning_with_equity_but_operation_without_equity results
#                                             # 0 - normal PH
#
#     # currently, only use in PH
#     # still have iteration, but with some decisions made
#     FORCE_PART_RESULTS = 'force_part_results'   # 1 - provide part of the planning decisions, for resuming the non-converged solving results
#                                                 # 0 - normal