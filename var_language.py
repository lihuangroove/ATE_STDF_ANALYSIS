#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : var_language.py
@Author  : Link
@Time    : 2022/12/24 11:22
@Mark    :

    datas=[
        ('parser_core\\dll_parser\\stdf_ctype.dll', '.'),
        ('chart_core\\chart_pyqtgraph\\core\\visual\\visual.cp37-win_amd64.pyd', '.'),
        ('colors\\CET-C6.csv', '.'),
        ('colors\\CET-D8.csv', '.'),
    ],
"""

from dataclasses import dataclass


class LanguageZh:
    JmpSetting = {
        "JmpSetting": "JMP绘图相关设定",
        "JmpNoLimit": "不加入Limit",
        "JmpPlotSeparation": "JMP分布分离显示",
        "JmpDisPlotBox": "显示分布箱线图",
        "JmpDisPlotSigma": "显示分布长期Sigma",
        "JmpPlotBin": "自定义JMP分布组数",
        "JmpBins": "JMP分布组数量",
        "JmpScreen": "JMP绘图值筛选区间",
        "JmpMeanAddSubSigma": "JMPMeanSigma±区间",
        "JmpPlotColumn": "JMP绘图分列数",
        "JmpPlotFloatRound": "JMP绘图小数精确位",
    }
    GraphSetting = {
        "GraphSetting": "PyqtGraph绘图相关设定",
        "GraphPlotBin": "自定义Graph分布组数",
        "GraphBins": "Graph分布组数量",
        "GraphScreen": "Graph绘图值筛选区间",
        "GraphMeanAddSubSigma": "Average_Sigma±区间",
        "GraphPlotColumn": "绘图分列数",
        "GraphPlotScatterSimple": "开启散点图抽样",
        "GraphPlotScatterSimpleNum": "散点趋势图抽样数",
        "GraphPlotFloatRound": "绘图小数精确位",
        "GraphPlotWidth": "绘图最大宽度",
        "GraphPlotHeight": "绘图最大高度",
    }

    Altair = {

    }

    R = {

    }

    PLOT_BACKEND = ("JMP", "PyqtGraph", "Altair", "R")

    kwargs = {}
    for key, values in JmpSetting.items():
        kwargs[values] = key
    for key, values in GraphSetting.items():
        kwargs[values] = key
    for key, values in Altair.items():
        kwargs[values] = key


language = LanguageZh
