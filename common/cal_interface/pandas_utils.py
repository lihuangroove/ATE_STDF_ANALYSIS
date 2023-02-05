#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : pandas_utils.py
@Author  : Link
@Time    : 2022/12/21 23:47
@Mark    : 
"""

import pandas as pd

from parser_core.stdf_parser_func import PrrPartFlag


class PandasStdfUtils:
    @staticmethod
    def df_generator_pcr(df: pd.DataFrame, head_num: int, site_num: int, ) -> dict:
        good_cnt = len(df[df.FAIL_FLAG == 1])
        pcr = df[df.PART_FLG & PrrPartFlag.FirstTest == 0]
        rt_pcr = df[df.PART_FLG & PrrPartFlag.FirstTest != 0]
        record_all = {
            "HEAD_NUM": head_num,
            "SITE_NUM": site_num,
            "PART_CNT": len(pcr),
            "RTST_CNT": len(rt_pcr),
            "ABRT_CNT": 0,
            "GOOD_CNT": good_cnt,
            "FUNC_CNT": 0,
        }
        return record_all

    @staticmethod
    def df_generator_hbr(df: pd.DataFrame, head_num: int, site_num: int, bin_name=None) -> list:
        """
        注意从MIR中找到bin相关信息
        """
        if bin_name is None:
            bin_name = dict()
        br_data = []
        for group_tuple, c_df in df.groupby(["HARD_BIN", "FAIL_FLAG"]):
            r_bin, pf = group_tuple
            br_data.append(
                {
                    "HEAD_NUM": head_num,
                    "SITE_NUM": site_num,
                    "HBIN_NUM": r_bin,
                    "HBIN_CNT": len(c_df),
                    "HBIN_PF": "P" if pf else "F",
                    "HBIN_NAM": bin_name.get(r_bin, ""),
                }
            )
        return br_data

    @staticmethod
    def df_generator_sbr(df: pd.DataFrame, head_num: int, site_num: int, bin_name=None) -> list:
        """
        注意从MIR中找到bin相关信息
        """
        if bin_name is None:
            bin_name = dict()
        br_data = []
        for group_tuple, c_df in df.groupby(["SOFT_BIN", "FAIL_FLAG"]):
            r_bin, pf = group_tuple
            br_data.append(
                {
                    "HEAD_NUM": head_num,
                    "SITE_NUM": site_num,
                    "SBIN_NUM": r_bin,
                    "SBIN_CNT": len(c_df),
                    "SBIN_PF": "P" if pf else "F",
                    "SBIN_NAM": bin_name.get(r_bin, ""),
                }
            )
        return br_data
