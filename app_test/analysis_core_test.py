#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : analysis_core_test.py
@Author  : Link
@Time    : 2022/12/16 21:24
@Mark    :
"""
import pickle
import unittest

import pandas as pd

from app_test.test_utils.mixins import Hdf5DataLoad
from app_test.test_utils.wrapper_utils import Tester
from app_test.test_utils.log_utils import Print
from common.app_variable import TestVariable
from common.cal_interface.capability import CapabilityUtils
from parser_core.stdf_parser_func import DtpOptFlag, PrrPartFlag


class ReadHdf5BaseAnalysisCase(unittest.TestCase, Hdf5DataLoad):
    """
    read hdf5 file with base analysis
    query占用的时间比较长,尽量不要用,快速验证可以用
    DA_GROUP
    TODO: 单个数据单元的测试, UI中组合的会复杂一些
        @20230107:
            1. 先转为通用格式
            2. 每个子数据使用unstack进行转置
            3. 更新最新的列名
    """
    top_fail_dict = None

    @Tester(
        ["load_data"],
        exec_time=True,
    )
    def test_load_data(self):
        """
        测试Read Hdf5数据
        :return:
        """
        select_summary, id_module_dict = self.summary.load_select_data([1, 2])
        self.li.set_data(select_summary, id_module_dict)
        self.li.concat()

    @Tester(
        ["load_data"],
        exec_time=True,
    )
    def test_print_base_data(self):
        """

        :return:
        """

        " 测试能否根据 TEST_ID/测试项目 这个测试项目的所有数据 "
        df = self.df_module.dtp_df[self.df_module.dtp_df.TEST_ID == 1]
        print(df)

        " 测试是否可以识别测试数据的Only Pass "
        pass_df = self.df_module.prr_df.query(
            """
            FAIL_FLAG == 1
            """
        )
        print(df.query(
            """
            index in @pass_df.index
            """
        ))
        pass_qty = len(pass_df)
        Print.success("PassQty:{}".format(pass_qty))

        " 测试是否可以识别测试数据的Only Fail "
        fail_df = self.df_module.prr_df.query(
            """
            FAIL_FLAG != 1
            """
        )
        print(df.query(
            """
            index in @fail_df.index
            """
        ))
        fail_qty = len(fail_df)
        Print.success("FailQty:{}".format(fail_qty))

        all_qty = pass_qty + fail_qty
        Print.success("AllQty:{}".format(all_qty))

        " 测试数据是否可以被解析为动态PAT "
        if len(df) != len(df[df.OPT_FLAG & DtpOptFlag.PatValid == DtpOptFlag.PatValid]):
            Print.warning("No Pat Data")
        else:
            Print.success("Can Get Pat Data")
        return True

    @Tester(
        ["test_load_data"],
        exec_time=True,
    )
    def test_print_first_re_finally_test(self):
        """
        测试识别初测和复测的数据
        :return:
        """
        first_df = self.df_module.prr_df[
            self.df_module.prr_df.PART_FLG & PrrPartFlag.FirstTest != PrrPartFlag.FirstTest
            ]
        Print.success("FirstTestQty:{}".format(len(first_df)))
        retest_df = self.df_module.prr_df[
            self.df_module.prr_df.PART_FLG & PrrPartFlag.FirstTest == PrrPartFlag.FirstTest
            ]
        Print.success("RetestTestQty:{}".format(len(retest_df)))

        """
        finally_df:
            1. get first_df pass
            2. get retest all
            3. concat 1&2
        """
        first_pass_df = first_df.query(
            """
            FAIL_FLAG == 1
            """
        )
        finally_df = pd.concat([first_pass_df, retest_df])
        Print.success("FinallyTestQty:{}".format(len(finally_df)))
        self.assertEqual(len(first_df), len(finally_df))

    @Tester(
        ["test_load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_print_only_coord(self):
        """
        测试识别最后的坐标数据
        Example Data: Chroma, TTK(NI TestStand@), STS(NI TestStand@)
        :return:
        """
        df1 = self.df_module.prr_df[["DIE_ID", "X_COORD", "Y_COORD"]].groupby(["X_COORD", "Y_COORD"]).last()
        df = self.df_module.prr_df[self.df_module.prr_df.DIE_ID.isin(df1.DIE_ID)]
        Print.success("FinallyTestQty:{}".format(len(df)))

    @Tester(
        ["test_load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_calculation_top_fail(self):
        """
        原始数据的top fail计算
        query占用的时间比较长,尽量不要用
        :return:
        """
        self.top_fail_dict = CapabilityUtils.calculation_top_fail(self.li.df_module)
        for key, value in self.top_fail_dict.items():
            print(key, value, sep=" : ")

    @Tester(
        ["test_load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_calculation_new_top_fail(self):
        """
        重新设置limit值后top fail的计算 -> 精度丢失问题, 即使limit没有变化, 算出来的fail rate和上面的函数可能也不一样
        运行时间肯定会长了一些 -> 实际和上面的操作时间一致? 上面的操作应该会更加简单和速度的.
        :return:
        """
        if len(self.li.df_module.prr_df) == 0:
            Print.danger("No Prr Data!")
            self.assertEqual(1, 0)
        self.top_fail_dict = CapabilityUtils.calculation_new_top_fail(self.li.df_module)
        for key, value in self.top_fail_dict.items():
            print(key, value, sep=" : ")

    @Tester(
        ["test_load_data", "test_calculation_top_fail"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_calculation_capability(self):
        """
        计算制程能力并优化这个逻辑的执行时间, 计算时间保持在 100k row, 200 column -> 1s之内
        数据量到达什么级别就用多线程?
        PTR才做计算
        FTR只统计失效比例( FTR上下限改为 0.9-1.1 )
        :return:
        """
        if len(self.df_module.prr_df) == 0:
            Print.danger("No Prr Data!")
            self.assertEqual(1, 0)

        if self.top_fail_dict is None:
            print("top fail is None")
            return

        capability_key_list = CapabilityUtils.calculation_capability(self.df_module, self.top_fail_dict)
        Print.print_table(capability_key_list)

        with open(TestVariable.TABLE_PICKLE_PATH, 'wb') as file_obj:
            data_pik = pickle.dumps(capability_key_list)
            file_obj.write(data_pik)

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_include_select_to_new_data(self):
        """
        选取想看的测试项目
        :return:
        """

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_exclude_select_to_new_data(self):
        """
        选取不想看的项目并删掉
        :return:
        """

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_select_and_delete_out_limit_data(self):
        """
        只看选取项目全PASS的数据
        :return:
        """

    @Tester()
    def load_other_data(self):
        return "Data"

    @Tester(
        ["load_data", "load_other_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_concat_two_data(self, **kwargs):
        """
        将两个不同程序的相同Device数据链接到一起
        数据结构改变了, 链接起来相对比较困难了
        :return:
        """
        print(kwargs)

    @Tester()
    def load_wat_data(self):
        return "Data"

    @Tester(
        ["load_data", "load_wat_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_merge_wat_cp_data(self, **kwargs):
        """
        使用算法将WAT的数据和CP的数据链接
        因为数据结构的改变, 算法套用不那么简单了 -> 主要是速度慢了很多
        :return:
        """
        print(kwargs)

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_select_date_unstack(self):
        """
        to csv, jsl read
        unstack的key是 TEST_NUM:TEST_TXT
        """
        pass

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_save_data_to_jmp(self):
        """
        to csv, jsl read
        """
        pass
