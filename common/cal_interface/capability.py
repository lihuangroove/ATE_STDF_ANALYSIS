"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/20 14:15
@Site    : 
@File    : capability.py
@Software: PyCharm
@Remark  : 
"""
from typing import List, Union

import pandas as pd
import numpy as np

from app_test.test_utils.wrapper_utils import Time
from common.app_variable import PtmdModule, LimitType, DataModule, DatatType, Calculation, FailFlag
from parser_core.stdf_parser_func import PtmdOptFlag, DtpTestFlag, PtmdParmFlag
from ui_component.ui_app_variable import UiGlobalVariable


class CapabilityUtils:
    """
    要注意:
        存到数据库中的数据必然不能被Round操作
    """

    @staticmethod
    # @Time()
    def top_fail(top_fail_df: pd.DataFrame, data_df: pd.DataFrame) -> (pd.DataFrame, int):
        """
        TODO:
            从原始数据集中计算, 直接确认是否fail
            不能找PASS, 要找Fail了多少
            时间开销大
        :param top_fail_df: ["PART_ID", "FAIL_FLAG"]
        :param data_df: Dtp Data, 需要和 top_fail_df 同步
        :return: 60k row, 40 column, 800ms, column吃时间
        """
        all_qty = len(top_fail_df)
        temp_data_df = data_df[data_df.index.isin(top_fail_df.index)]
        fail_df = temp_data_df[temp_data_df.FAIL_FLG == FailFlag.FAIL]
        fail_qty = len(fail_df)
        top_fail_df = top_fail_df[~top_fail_df.index.isin(fail_df.index)]
        if len(top_fail_df) > all_qty:
            raise Exception("error len(top_fail_df) > all_qty")
        return top_fail_df, fail_qty

    @staticmethod
    @Time()
    def calculation_top_fail(df_module: DataModule):
        """
        Top Fail如何计算? 算逐项fail即可.
        TODO:
            1. 去除多个文件中, 重复的数据
            2. 取数据并进行运算
        :param df_module:
        :return:
        """
        df_use_top_fail = df_module.prr_df
        dtp_df = df_module.dtp_df
        top_fail_dict = {}
        for row in df_module.ptmd_df.itertuples():  # type:PtmdModule
            " 逐项计算Top Fail "
            df_use_top_fail, fail_qty = CapabilityUtils.top_fail(
                df_use_top_fail,
                dtp_df.loc[row.TEST_ID]
            )
            try:
                top_fail_dict[row.TEST_ID] += fail_qty
            except:
                top_fail_dict[row.TEST_ID] = fail_qty
        return top_fail_dict

    @staticmethod
    # @Time()
    def re_cal_top_fail(ptmd: PtmdModule, prr_df: pd.DataFrame, dtp_unit_df: pd.DataFrame) -> pd.DataFrame:
        """
        重新计算, 使用ptmd中包含的新的limit信息
        :param ptmd:
        :param prr_df:
        :param dtp_unit_df:
        :return: 60k row, 40 column, 800ms -> ??? sometimes faster than top_fail function
        """
        logic_and = []
        if not ptmd.OPT_FLAG & PtmdOptFlag.NoLowLimit:
            if ptmd.PARM_FLG & PtmdParmFlag.EqualLowLimit:  # >=
                logic_and.append((dtp_unit_df.RESULT >= ptmd.LO_LIMIT))
            else:  # >
                logic_and.append((dtp_unit_df.RESULT > ptmd.LO_LIMIT))
        if not ptmd.OPT_FLAG & PtmdOptFlag.NoHighLimit:
            if ptmd.PARM_FLG & PtmdParmFlag.EqualHighLimit:  # <=
                logic_and.append((dtp_unit_df.RESULT <= ptmd.HI_LIMIT))
            else:  # <
                logic_and.append((dtp_unit_df.RESULT < ptmd.HI_LIMIT))
        if len(logic_and) == 0:  # No fail
            return dtp_unit_df
        if len(logic_and) == 1:
            items = logic_and[0]
            fail_df = dtp_unit_df.loc[~items]
        else:
            items = np.logical_and(*logic_and)
            fail_df = dtp_unit_df.loc[~items]
        dtp_unit_df.loc[~items, "FAIL_FLG"] = FailFlag.FAIL
        prr_df.loc[prr_df.index.isin(fail_df.PART_ID), "FAIL_FLAG"] = FailFlag.FAIL
        return dtp_unit_df

    @staticmethod
    @Time()
    def calculation_new_top_fail(df_module: DataModule):
        """
        TODO:
            @20230204->需要修改下逻辑->先计算dtp_df的FAIL_FLG->再直接调用calculation_top_fail即可
            @20230205->后面如果需要更新BIN值, 是否可以在这里面进行操作, ptmd_df 可以扩展?
        重新设置limit值后top fail的计算 -> 精度丢失问题, 即使limit没有变化, 算出来的fail rate和上面的函数可能也不一样
        运行时间肯定会长了一些 -> 实际和上面的操作时间一致? 上面的操作应该会更加简单和速度的.
        Top Fail如何计算? 算逐项fail即可.
        :param df_module:
        :return:
        """
        dtp_df = df_module.dtp_df.copy()
        dtp_df.loc[:, "FAIL_FLG"] = FailFlag.PASS
        dtp_df.reset_index(inplace=True)
        dtp_df_dict = {}
        new_dtp_df_list = []
        for test_id, df in dtp_df.groupby("TEST_ID"):
            dtp_df_dict[test_id] = df
        for row in df_module.ptmd_df.itertuples():  # type:PtmdModule
            unit_dtp = CapabilityUtils.re_cal_top_fail(
                row,
                df_module.prr_df,
                dtp_df_dict[row.TEST_ID],
            )
            new_dtp_df_list.append(unit_dtp)
        new_dtp_df = pd.concat(new_dtp_df_list)
        new_dtp_df.set_index(["TEST_ID", "DIE_ID"], inplace=True)
        df_module.dtp_df = new_dtp_df
        return CapabilityUtils.calculation_top_fail(df_module)

    @staticmethod
    def calculation_ptr(
            ptmd: PtmdModule, top_fail_qty: int, data_df: pd.DataFrame, all_qty: int
    ) -> Union[Calculation, dict]:
        """
        TODO:
            3倍中位数绝对偏差去极值
            时间开销大
        :param top_fail_qty:
        :param ptmd:
        :param data_df:
        :param all_qty: 计算Top Fail Rate
        :return:
        """

        # def _mad(factor):
        #     """
        #     3倍中位数绝对偏差去极值 by CSDN: https://blog.csdn.net/m0_37967652/article/details/122900866
        #     """
        #     me = np.median(factor)
        #     mad = np.median(abs(factor - me))
        #     # 求出3倍中位数的上下限制
        #     up = me + (3 * 1.4826 * mad)
        #     down = me - (3 * 1.4826 * mad)
        #     # 利用3倍中位数的值去极值
        #     factor = np.where(factor > up, up, factor)
        #     factor = np.where(factor < down, down, factor)
        #     return factor

        # data_df["RESULT"] = _mad(data_df["RESULT"])
        decimal = UiGlobalVariable.GraphPlotFloatRound
        fail_exec = data_df.FAIL_FLG == FailFlag.FAIL
        reject_qty = len(data_df[fail_exec])
        if len(data_df) == reject_qty:
            pass_df = data_df  # TODO: 全部失效了
        else:
            pass_df = data_df[~fail_exec]
        data_mean, data_min, data_max, data_std, data_median = \
            pass_df.RESULT.mean(), pass_df.RESULT.min(), pass_df.RESULT.max(), pass_df.RESULT.std(), \
            pass_df.RESULT.median()
        if data_std == 0:
            data_std = 1E-05
        cpk = round(min([(ptmd.HI_LIMIT - data_mean) / (3 * data_std),
                         (data_mean - ptmd.LO_LIMIT) / (3 * data_std)]), decimal)
        l_limit_type = LimitType.ThenLowLimit
        if ptmd.OPT_FLAG & PtmdOptFlag.NoLowLimit:
            l_limit_type = LimitType.NoLowLimit
        if ptmd.PARM_FLG & PtmdParmFlag.EqualLowLimit:
            l_limit_type = LimitType.EqualLowLimit
        h_limit_type = LimitType.ThenHighLimit
        if ptmd.OPT_FLAG & PtmdOptFlag.NoHighLimit:
            h_limit_type = LimitType.NoHighLimit
        if ptmd.PARM_FLG & PtmdParmFlag.EqualHighLimit:
            h_limit_type = LimitType.EqualHighLimit
        temp_dict = {
            "TEST_ID": ptmd.TEST_ID,  # 每个测试项目最后整合后只会有唯一一个TEST_ID
            "DATAT_TYPE": ptmd.DATAT_TYPE,
            "TEST_NUM": ptmd.TEST_NUM,
            "TEST_TXT": ptmd.TEST_TXT,
            "UNITS": ptmd.UNITS,
            "LO_LIMIT": round(ptmd.LO_LIMIT, decimal),
            "HI_LIMIT": round(ptmd.HI_LIMIT, decimal),
            "AVG": round(data_mean, decimal),
            "STD": round(data_std, decimal),
            "CPK": abs(cpk),
            "MEDIAN": round(data_median, decimal),
            "QTY": len(data_df),
            "FAIL_QTY": top_fail_qty,
            # TODO: 注意 top fail的Rate一定是要%总颗数,不能%测试颗数, 待更新
            "FAIL_RATE": "{}%".format(round(top_fail_qty / all_qty * 100, 3)),
            "REJECT_QTY": reject_qty,
            "REJECT_RATE": "{}%".format(round(reject_qty / len(data_df) * 100, 3)),
            "MIN": round(data_min, decimal),  # 注意, 是取得PASS区域的数据
            "MAX": round(data_max, decimal),  # 注意, 是取得PASS区域的数据
            "LO_LIMIT_TYPE": l_limit_type,
            "HI_LIMIT_TYPE": h_limit_type,
            "ALL_DATA_MIN": round(data_df.RESULT.min(), decimal),
            "ALL_DATA_MAX": round(data_df.RESULT.max(), decimal),
            "TEXT": ptmd.TEXT,
        }
        # return Calculation(**temp_dict)
        return temp_dict

    @staticmethod
    def calculation_ftr(
            ptmd: PtmdModule, top_fail_qty: int, data_df: pd.DataFrame, all_qty: int
    ) -> Union[Calculation, dict]:
        """
        只计算fail rate
        :param top_fail_qty:
        :param ptmd:
        :param data_df:
        :param all_qty:
        :return:
        """
        decimal = UiGlobalVariable.GraphPlotFloatRound
        reject_qty = len(data_df[data_df.TEST_FLG & DtpTestFlag.TestFailed == DtpTestFlag.TestFailed])
        temp_dict = {
            "TEST_ID": ptmd.TEST_ID,  # 每个测试项目最后整合后只会有唯一一个TEST_ID
            "DATAT_TYPE": ptmd.DATAT_TYPE,
            "TEST_NUM": ptmd.TEST_NUM,
            "TEST_TXT": ptmd.TEST_TXT,
            "UNITS": ptmd.UNITS,
            "LO_LIMIT": round(ptmd.LO_LIMIT, decimal),
            "HI_LIMIT": round(ptmd.HI_LIMIT, decimal),
            "AVG": np.nan,
            "STD": np.nan,
            "CPK": np.nan,
            "QTY": len(data_df),
            "FAIL_QTY": top_fail_qty,
            # TODO: 注意 top fail的Rate一定是要%总颗数,不能%测试颗数, 待更新
            "FAIL_RATE": "{}%".format(round(top_fail_qty / all_qty * 100, 3)),
            "REJECT_QTY": reject_qty,
            "REJECT_RATE": "{}%".format(round(reject_qty / len(data_df) * 100, 3)),
            "MIN": -0.1,  # 注意, 是取得有效区域的数据
            "MAX": 1.1,  # 注意, 是取得有效区域的数据
            "LO_LIMIT_TYPE": LimitType.ThenLowLimit,
            "HI_LIMIT_TYPE": LimitType.EqualHighLimit,
            "ALL_DATA_MIN": -0.1,
            "ALL_DATA_MAX": 1.1,
            "TEXT": ptmd.TEXT,
        }
        # return Calculation(**temp_dict)
        return temp_dict

    @staticmethod
    @Time()
    def calculation_capability(df_module: DataModule, top_fail_dict: dict) -> List[dict]:
        """
        python dict 是可以保持顺序的
            用于计算整个数据的Top Fail等信息
        :param df_module:
        :param top_fail_dict:
        :return:
        """
        all_qty = len(df_module.prr_df)
        capability_key_list = []
        for row in df_module.ptmd_df.itertuples():  # type:PtmdModule
            data_df = df_module.dtp_df.loc[row.TEST_ID].loc[:].copy()  # TODO: 10%时间开销
            if row.DATAT_TYPE in {DatatType.PTR, DatatType.MPR}:
                cal_data = CapabilityUtils.calculation_ptr(
                    row, top_fail_dict[row.TEST_ID], data_df, all_qty
                )
                capability_key_list.append(cal_data)
                continue
            if row.DATAT_TYPE == DatatType.FTR:
                cal_data = CapabilityUtils.calculation_ftr(
                    row, top_fail_dict[row.TEST_ID], data_df, all_qty
                )
                capability_key_list.append(cal_data)
                continue
        return capability_key_list
