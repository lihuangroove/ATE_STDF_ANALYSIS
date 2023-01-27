#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : ui_app_variable.py
@Author  : Link
@Time    : 2022/12/23 21:06
@Mark    : 控制信号
"""
import collections
from dataclasses import dataclass

from var_language import language

ACTIONS_NAME = collections.namedtuple('Action', ["name", "text"])


@dataclass
class AppBus:
    code: int
    data: object = None


class UiAppCode:
    Ui = 0x20000

    DataAnalysis = 0x10000


class QtPlotAllUse:
    """
    需要在对外面的界面中被识别并修改全局变量
    MultiSelect = True:
        图形处于可多选状态
    """
    MultiSelect = False


class UiGlobalVariable:
    # --------------------------------------------------------------- 数据分析相关
    JmpNoLimit = False
    JmpPlotSeparation = False
    JmpDisPlotBox = False
    JmpDisPlotSigma = False
    JmpPlotBin = True
    JmpBins = 30
    JmpScreen = 0
    JmpMeanAddSubSigma = 3
    JmpPlotColumn = 1
    JmpPlotFloatRound = 6
    # --------------------------------------------------------------- 参数
    JMP_PARAMS = [
        {
            'name': language.JmpSetting["JmpSetting"], 'type': 'group', 'children':
            [
                {'name': language.JmpSetting["JmpNoLimit"], 'type': 'bool',
                 'value': JmpNoLimit},

                {'name': language.JmpSetting["JmpPlotSeparation"], 'type': 'bool',
                 'value': JmpPlotSeparation},

                {'name': language.JmpSetting["JmpDisPlotBox"], 'type': 'bool',
                 'value': JmpDisPlotBox},

                {'name': language.JmpSetting["JmpDisPlotSigma"], 'type': 'bool',
                 'value': JmpDisPlotSigma},

                {'name': language.JmpSetting["JmpPlotBin"], 'type': 'bool',
                 'value': JmpPlotBin},

                {'name': language.JmpSetting["JmpBins"], 'type': 'int',
                 'value': JmpBins},

                {'name': language.JmpSetting["JmpScreen"], 'type': 'list',
                 'value': JmpScreen,
                 'limits': {"LCL-To-UCL": 0, "PassMin-To-PassMax": 1, "DataMin-To-DataMax": 2, "Average_Sigma": 3}},

                {'name': language.JmpSetting["JmpMeanAddSubSigma"], 'type': 'int',
                 'value': JmpMeanAddSubSigma, },

                {'name': language.JmpSetting["JmpPlotColumn"], 'type': 'int',
                 'value': JmpPlotColumn},

                {'name': language.JmpSetting["JmpPlotFloatRound"], 'type': 'int',
                 'value': JmpPlotFloatRound},
            ]
        },
    ]

    GraphUseLocalColor = False
    GraphPlotBin = True
    GraphBins = 60
    GraphScreen = 0
    GraphMeanAddSubSigma = 3
    GraphPlotColumn = 1
    GraphPlotScatterSimple = False
    GraphPlotScatterSimpleNum = 10000
    GraphPlotFloatRound = 6
    GraphPlotWidth = 1000
    GraphPlotHeight = 600
    # --------------------------------------------------------------- 参数
    GRAPH_PARAMS = [
        {
            'name': "PyqtGraph绘图相关设定", 'type': 'group', 'children':
            [
                {'name': language.GraphSetting["GraphScreen"], 'type': 'list',
                 'value': GraphScreen,
                 'limits': {"LCL-To-UCL": 0, "PassMin-To-PassMax": 1, "DataMin-To-DataMax": 2, "Average_Sigma": 3}},

                {'name': language.GraphSetting["GraphMeanAddSubSigma"], 'type': 'int',
                 'value': GraphMeanAddSubSigma, },

                {'name': language.GraphSetting["GraphBins"], 'type': 'int',
                 'value': GraphBins,
                 'max': 100, 'min': 20},

                {'name': language.GraphSetting["GraphPlotScatterSimple"], 'type': 'bool',
                 'value': GraphPlotScatterSimple},

                {'name': language.GraphSetting["GraphPlotScatterSimpleNum"], 'type': 'int',
                 'value': GraphPlotScatterSimpleNum},

                {'name': language.GraphSetting["GraphPlotWidth"], 'type': 'int',
                 'value': GraphPlotWidth},

                {'name': language.GraphSetting["GraphPlotHeight"], 'type': 'int',
                 'value': GraphPlotHeight},
            ]
        },
    ]

    PLOT_BACKEND = language.PLOT_BACKEND

    ALL_CHART_ACTIONS = [ACTIONS_NAME("action_distribution", "测试数据分布图"),
                         ACTIONS_NAME("action_distribution_trans", "横向分布图"),
                         ACTIONS_NAME("action_comparing", "比较密度图"),
                         ACTIONS_NAME("action_scatter", "散点图"),
                         ACTIONS_NAME("action_box_plot", "箱线图"),
                         ACTIONS_NAME("action_mapping", "BIN Mapping"),
                         ACTIONS_NAME("action_visual_map", "Visual Map"),
                         ACTIONS_NAME("action_linear", "线性回归"),
                         ACTIONS_NAME("action_multiple_chart", "多图选取")]

    JMP_CHARTS = ALL_CHART_ACTIONS
    QT_GRAPH_CHARTS = [
        # ALL_CHART_ACTIONS[1],
        # ALL_CHART_ACTIONS[3],
        # ALL_CHART_ACTIONS[5],
        # ALL_CHART_ACTIONS[6],
    ]

    ALTAIR_CHARTS = [
        ALL_CHART_ACTIONS[3],
        ALL_CHART_ACTIONS[-1]
    ]

    R_CHARTS = [

    ]

    WEB_ACTIONS = [
        ACTIONS_NAME("action_web_search", "服务器解析数据分析"),
        ACTIONS_NAME("action_material_report", "量产测试数据报表"),
        ACTIONS_NAME("action_server_scan", "服务器数据解析状态"),
        ACTIONS_NAME("action_tools", "服务器设置工具"),
    ]

    JMP_MULTI_SELECT = ["测试数据分布图", "横向分布图", "比较密度图", "散点图", "箱线图(点型)", "箱线图(线型)", "SOFT_BIN MAP",
                        "HARD_BIN MAP", "FIRST_FAIL MAP", "VISUAL_MAP(热图)", "VISUAL_MAP(点型)", "数据Filter"]

    SUMMARY_GROUP = ["LOT_ID", "SBLOT_ID", "WAFER_ID", "FLOW_ID", "TEST_COD", "NODE_NAM", "BLUE_FILM_ID"]
    DATA_GROUP = ["SITE_NUM"]

    PROCESS_VALUE = ["MEAN", "STD", "CPK"]
    PROCESS_TOP_ITEM_LIST = ["YIELD", "DATA"]
