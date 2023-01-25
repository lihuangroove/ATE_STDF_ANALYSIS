#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : ui_processing.py
@Author  : Link
@Time    : 2022/7/31 13:35
@Mark    : 
"""

from typing import Union

import numpy as np
from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt, QCloseEvent, QShowEvent
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Slot, QModelIndex

from common.app_variable import FailFlag, Calculation, DatatType
from common.li import Li
from ui_component.ui_app_variable import UiGlobalVariable
from ui_component.ui_analysis_stdf.ui_designer.ui_processing import Ui_Form

import pyqtgraph as pg
import pandas as pd

from ui_component.ui_common.my_text_browser import Print


class ProcessWidget(QWidget, Ui_Form):
    """
    TODO: 需要传入类似给到JMP的数据类型, 需要拥有表头
        简单一些, 不用莫名其妙的信号传入了, 打开的时候传入选取的数据
    """
    top_item_list = QStandardItemModel()  # yield, avg, limit ...
    bot_item_list = QStandardItemModel()  # group by item
    select_item_list = QStandardItemModel()
    jmp_df: pd.DataFrame = None
    calculation: dict = None

    def __init__(self, parent=None, icon=None):
        super(ProcessWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("制程能力")
        if icon:
            self.setWindowIcon(icon)
        self.listView_3.setModel(self.select_item_list)
        self.listView_2.setModel(self.top_item_list)
        self.listView_2.clicked.connect(self.top_row_change)
        self.listView.setModel(self.bot_item_list)
        self.listView.clicked.connect(self.bot_row_change)
        self.cpk_info_table = pg.TableWidget(self)
        self.verticalLayout.addWidget(self.cpk_info_table)
        self.cpk_info_table.setEditable(True)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 15)

        self.init_listView_3()
        self.init_listView_2()

    def init_listView_3(self):
        self.select_item_list.clear()
        for index, each in enumerate(UiGlobalVariable.PROCESS_VALUE):
            item = QStandardItem(each)
            item.setCheckState(Qt.Unchecked)
            item.setCheckable(True)
            if index == 0:
                item.setCheckState(Qt.Checked)
            self.select_item_list.appendRow(item)

    def get_listView_3_choose_items(self) -> Union[list, None]:
        select_item_list = []
        for index, each in enumerate(UiGlobalVariable.PROCESS_VALUE):
            temp = self.select_item_list.item(index)
            if temp.checkState() == Qt.Checked:
                select_item_list.append(temp.text())
        return select_item_list if select_item_list else None

    def init_listView_2(self):
        self.top_item_list.clear()
        for index, each in enumerate(UiGlobalVariable.PROCESS_TOP_ITEM_LIST):
            item = QStandardItem(each)
            self.top_item_list.appendRow(item)

    def gen_listView(self):
        """
        通过 GROUP 和 DA_GROUP 来做处理
        :return:
        """
        temp_df = self.jmp_df
        bot_item_list_df = temp_df["GROUP"] + "@" + temp_df["DA_GROUP"]  # type:pd.DataFrame
        bot_item_list = bot_item_list_df.drop_duplicates(keep="first").tolist()
        self.bot_item_list.clear()
        for index, each in enumerate(bot_item_list):
            item = QStandardItem(each)
            self.bot_item_list.appendRow(item)

    def set_data(self, jmp_df: pd.DataFrame, calculation: dict):
        """
        设置数据后才可以调用 gen_listView
        :return:
        """
        self.jmp_df = jmp_df
        self.calculation = calculation

    def set_front_df_process(self):
        """
        将数据显示到前台中. 一般在这里的时候, 数据已经经理了group by阶段了
        :return:
        """
        if self.jmp_df is None:
            return False
        self.gen_listView()

    @Slot(QModelIndex)
    def top_row_change(self, model_index: QModelIndex):
        """
        放良率. 和 avg 对比
        :param model_index:
        :return:
        """
        if self.jmp_df is None:
            return

        temp_df = self.jmp_df
        if "GROUP" not in temp_df or "DA_GROUP" not in temp_df:
            return

        if model_index.data() == "YIELD":
            df_group = temp_df.groupby(["GROUP", "DA_GROUP"])
            yield_data = []  # type:list
            for key, each_df in df_group:
                if not isinstance(key, tuple):
                    item_name = str(key)
                else:
                    item_name = '@'.join([str(ea) for ea in key])
                total = len(each_df)
                fail_num = len(each_df[each_df.FAIL_FLAG != FailFlag.PASS])
                pass_num = len(each_df) - fail_num
                yield_data.append({
                    "Item": item_name,
                    "Total": total,
                    "Pass": pass_num,
                    "Fail": fail_num,
                    "Yield": "{}%".format(round(pass_num / total * 100, 3)),
                })
            self.cpk_info_table.setData(yield_data)
            return

        if model_index.data() == "DATA":
            """
            这个稍微复杂一些, 先将数据都获取到, 然后再整理起来
            """
            if not self.calculation:
                return Print.warning("未选取测试项目, 故只能查询良率数据@!!!")
            item_list = self.get_listView_3_choose_items()
            if item_list is None:
                return
            df_group = temp_df.groupby(["GROUP", "DA_GROUP"])
            group_cpk_dict = dict()
            for key, each_df in df_group:
                if not isinstance(key, tuple):
                    item_name = str(key)
                else:
                    item_name = '@'.join([str(ea) for ea in key])
                _cpk_df = each_df[each_df.FAIL_FLAG == FailFlag.PASS][self.calculation.keys()]
                _mean = _cpk_df.mean()
                _std = _cpk_df.std()
                temp_data_list = []
                for index, item_key in enumerate(self.calculation.keys()):
                    item: dict = self.calculation[item_key]
                    temp_std = _std[item_key]
                    temp_mean = _mean[item_key]
                    if temp_std == 0:
                        cpk = 0
                    else:
                        cpk = round(min(
                            [(item["HI_LIMIT"] - temp_mean) / (3 * temp_std),
                             (temp_mean - item["LO_LIMIT"]) / (3 * temp_std)])
                            , UiGlobalVariable.GraphPlotFloatRound)
                    temp_dict = {
                        "TEST_ID": item["TEST_ID"],
                        "DATAT_TYPE": item["DATAT_TYPE"],
                        "TEXT": item_key,
                        "UNITS": item["UNITS"],
                        "LO_LIMIT": item["LO_LIMIT"],
                        "HI_LIMIT": item["HI_LIMIT"],
                        "LO_LIMIT_TYPE": item["LO_LIMIT_TYPE"],
                        "HI_LIMIT_TYPE": item["HI_LIMIT_TYPE"],
                        f"{item_name}_AVG": round(_mean[item_key], 5),
                        f"{item_name}_STD": round(_std[item_key], 5),
                        f"{item_name}_CPK": cpk,
                    }
                    temp_data_list.append(temp_dict)
                group_cpk_dict[item_name] = temp_data_list

            """
            前台展示数据
            """
            data_table_list = []
            for index, key in enumerate(group_cpk_dict.keys()):
                temp_each_data = group_cpk_dict[key]
                if index == 0:
                    for i, row in enumerate(temp_each_data):
                        d = {
                            "TEST_ID": row["TEST_ID"],
                            "DATAT_TYPE": row["DATAT_TYPE"],
                            "TEXT": row["TEXT"],
                            "UNITS": row["UNITS"],
                            "LO_LIMIT": row["LO_LIMIT"],
                            "HI_LIMIT": row["HI_LIMIT"],
                            "LO_LIMIT_TYPE": row["LO_LIMIT_TYPE"],
                            "HI_LIMIT_TYPE": row["HI_LIMIT_TYPE"],
                        }
                        for each in item_list:
                            if each == "MEAN":
                                d[f"{key}_AVG"] = row[f"{key}_AVG"]
                            if each == "STD":
                                d[f"{key}_STD"] = row[f"{key}_STD"]
                            if each == "CPK":
                                d[f"{key}_CPK"] = row[f"{key}_CPK"]
                        data_table_list.append(d)
                else:
                    for i, row in enumerate(temp_each_data):
                        for each in item_list:
                            if each == "MEAN":
                                data_table_list[i][f"{key}_AVG"] = row[f"{key}_AVG"]
                            if each == "STD":
                                data_table_list[i][f"{key}_STD"] = row[f"{key}_STD"]
                            if each == "CPK":
                                data_table_list[i][f"{key}_CPK"] = row[f"{key}_CPK"]
            self.cpk_info_table.setData(data_table_list)
            return

    @Slot(QModelIndex)
    def bot_row_change(self, model_index: QModelIndex):
        """
        放单个数据, 单个数据可以有value类型和diff类型
        :param model_index:
        :return:
        """
        if not self.calculation:
            return Print.warning("未选取测试项目, 故只能查询良率数据@!!!")
        group, da_group = model_index.data().split("@")
        df = self.jmp_df[(self.jmp_df.GROUP == group) & (self.jmp_df.DA_GROUP == da_group)]
        if self.radioButton_2.isChecked():
            cpk_list = []
            temp_df = df[df.FAIL_FLAG == FailFlag.PASS][self.calculation.keys()]
            _mean, _min, _max, _std, _median = temp_df.mean(), temp_df.min(), temp_df.max(), temp_df.std(), temp_df.median()
            for key, item in self.calculation.items():  # type:str, dict
                temp_std, temp_mean = _std[key], _mean[key]
                cpk = 0 if temp_std == 0 else round(
                    min([(item["HI_LIMIT"] - temp_mean) / (3 * temp_std),
                         (temp_mean - item["LO_LIMIT"]) / (3 * temp_std)])
                    , 6)
                temp_dict = {
                    "TEST_ID": item["TEST_ID"],
                    "DATAT_TYPE": item["DATAT_TYPE"],
                    "TEST_NUM": item["TEST_NUM"],
                    "TEST_TXT": item["TEST_TXT"],
                    "UNITS": item["UNITS"],
                    "LO_LIMIT": item["LO_LIMIT"],
                    "HI_LIMIT": item["HI_LIMIT"],
                    "AVG": round(_mean[key], 6),
                    "STD": round(_std[key], 6),
                    "CPK": cpk,
                    "QTY": len(df),
                    # "Fail": fail_qty,
                    # "Fail/Total": "{}%".format(round(fail_qty / len(df) * 100, 3)),
                    # "Reject": reject_qty,
                    # "Reject/Total": "{}%".format(round(reject_qty / len(df) * 100, 3)),
                    # "MIN": round(_min[key], 6),
                    # "MAX": round(_max[key], 6),
                    "LO_LIMIT_TYPE": item["LO_LIMIT_TYPE"],
                    "HI_LIMIT_TYPE": item["HI_LIMIT_TYPE"],
                    "TEXT": key,
                }
                cpk_list.append(temp_dict)
            self.cpk_info_table.setData(cpk_list)
            return
        if self.radioButton.isChecked():
            """
            DIFF, 只看均值以及PTR项目
            """
            diff_compare_df = df
            length = len(diff_compare_df)
            start, stop = int(length * 0.05), int(length * 0.95)

            diff_data_list = []
            df_group = self.jmp_df.groupby(["GROUP", "DA_GROUP"])
            for item_key, test_item in self.calculation.items():  # type:str, dict
                if test_item["DATAT_TYPE"] == DatatType.FTR:
                    continue
                temp_dict = dict()
                diff_data_list.append(temp_dict)
                temp_dict["TEST_ID"] = test_item["TEST_ID"]
                temp_dict["TEXT"] = test_item["TEXT"]
                temp_dict["UNITS"] = test_item["UNITS"]
                temp_dict["LO_LIMIT"] = test_item["LO_LIMIT"]
                temp_dict["HI_LIMIT"] = test_item["LO_LIMIT"]
                temp_dict["LO_LIMIT_TYPE"] = test_item["LO_LIMIT_TYPE"]
                temp_dict["HI_LIMIT_TYPE"] = test_item["HI_LIMIT_TYPE"]

                compare_data = np.mean(sorted(diff_compare_df[item_key].to_list())[start: stop])
                for key, each_df in df_group:
                    if not isinstance(key, tuple):
                        item_name = str(key)
                    else:
                        item_name = '@'.join([str(ea) for ea in key])
                    temp_data = each_df[item_key].to_list()
                    temp_length = len(each_df)
                    temp_start, temp_stop = int(temp_length * 0.05), int(temp_length * 0.95)
                    temp_data = sorted(temp_data)[temp_start: temp_stop]
                    temp_data = np.mean(temp_data)
                    gap = compare_data - temp_data
                    temp_dict[item_name] = gap

            self.cpk_info_table.setData(diff_data_list)
            return

    def showEvent(self, event: QShowEvent) -> None:
        self.set_front_df_process()
        event.accept()
