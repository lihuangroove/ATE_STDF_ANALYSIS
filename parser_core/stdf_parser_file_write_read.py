#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : stdf_parser_file_write_read.py
@Author  : Link
@Time    : 2022/12/24 12:07
@Mark    : 
"""
import os
from typing import Union, List, ValuesView

import pandas as pd
import numpy as np
from pandas import DataFrame as Df

from app_test.test_utils.wrapper_utils import Time
from common.app_variable import TestVariable as TestVar, DataModule, GlobalVariable as GloVar, PtmdModule, TestVariable, \
    PartFlags, FailFlag, GlobalVariable
from parser_core.stdf_parser_func import PrrPartFlag, DtpTestFlag


class ParserData:
    @staticmethod
    def delete_temp_file():
        for path in TestVariable.PATHS:
            if os.path.exists(path):
                os.remove(path)

    @staticmethod
    def load_csv() -> Union[DataModule, None]:
        """
        TODO: 需要支援93k就在这边操作, 尽少的在C++中对程序进行修改
              93k主要注意@符号,分割第一个@
              OPT_FLG为0x0的数据就更新一下
        :return:
        """
        try:
            prr_df = pd.read_csv(
                TestVar.TEMP_PRR_PATH, header=None, names=GloVar.PRR_HEAD, dtype=GloVar.PRR_TYPE_DICT)
            dtp_df = pd.read_csv(
                TestVar.TEMP_DTP_PATH, header=None, names=GloVar.DTP_HEAD, dtype=GloVar.DTP_TYPE_DICT)
            ptmd_df = pd.read_csv(
                TestVar.TEMP_PTMD_PATH, header=None, names=GloVar.PTMD_HEAD, dtype=GloVar.PTMD_TYPE_DICT)

            # if 93k?
            new_ptmd_list = []
            # ========================= TODO: only for 93k
            cache_test_ptmd = dict()
            ptmd_df_dict_list = ptmd_df.to_dict(orient='records')
            for each in ptmd_df_dict_list:
                temp_split_text = each["TEST_TXT"].split("@", 1)
                if len(temp_split_text) == 0:
                    continue
                else:
                    key = temp_split_text[0]
                    if key in cache_test_ptmd:
                        pass
                    else:
                        cache_test_ptmd[key] = each
                if each["OPT_FLAG"] == 0:
                    temp_each = cache_test_ptmd[key]
                    each["PARM_FLG"] = temp_each["PARM_FLG"]
                    each["OPT_FLAG"] = temp_each["OPT_FLAG"]
                    each["RES_SCAL"] = temp_each["RES_SCAL"]
                    each["LLM_SCAL"] = temp_each["LLM_SCAL"]
                    each["HLM_SCAL"] = temp_each["HLM_SCAL"]
                    each["LO_LIMIT"] = temp_each["LO_LIMIT"]
                    each["HI_LIMIT"] = temp_each["HI_LIMIT"]
                    each["UNITS"] = temp_each["UNITS"]
                new_ptmd_list.append(each)
            ptmd_df = pd.DataFrame(new_ptmd_list)
            # ==================================================

            df_module = DataModule(prr_df=prr_df, dtp_df=dtp_df, ptmd_df=ptmd_df)
            return df_module
        except Exception as err:
            print(err)

    @staticmethod
    def save_hdf5(df_module: DataModule, file_path: str) -> bool:
        try:
            df_module.prr_df.to_hdf(file_path, "prr_df", mode="w")
            df_module.ptmd_df.to_hdf(file_path, "ptmd_df", mode="r+", format="table")
            df_module.dtp_df.to_hdf(file_path, "dtp_df", mode="r+")
            return True
        except Exception as err:
            print(err)
            return False

    @staticmethod
    def get_yield(prr_df, part_flag, read_fail) -> dict:
        """
        获取简单的良率信息
        :param read_fail:
        :param part_flag: PART_FLAGS = ('ALL', 'FIRST', 'RETEST', 'FINALLY', "XY_COORD")
        :param prr_df:
        :return:
        """
        df = ParserData.get_prr_data(prr_df, part_flag, read_fail)
        return ParserData.get_yield_data(df)

    @staticmethod
    def get_prr_data(prr_df, part_flag, read_fail) -> pd.DataFrame:
        df = prr_df
        if not read_fail:
            df = df[df.FAIL_FLAG == FailFlag.PASS]
        if part_flag == PartFlags.FIRST:
            df = df[df.PART_FLG & PrrPartFlag.FirstTest != PrrPartFlag.FirstTest]
        if part_flag == PartFlags.RETEST:
            df = df[df.PART_FLG & PrrPartFlag.FirstTest == PrrPartFlag.FirstTest]
        if part_flag == PartFlags.FINALLY:
            first_df = df[df.PART_FLG & PrrPartFlag.FirstTest != PrrPartFlag.FirstTest]
            retest_df = df[df.PART_FLG & PrrPartFlag.FirstTest == PrrPartFlag.FirstTest]
            first_pass_df = first_df[first_df.FAIL_FLAG == FailFlag.PASS]
            df = pd.concat([first_pass_df, retest_df])
        if part_flag == PartFlags.XY_COORD:
            df1 = df[["DIE_ID", "X_COORD", "Y_COORD"]].groupby(["X_COORD", "Y_COORD"]).last()
            df = df[df.DIE_ID.isin(df1.DIE_ID)]
        return df

    @staticmethod
    def get_yield_data(df: pd.DataFrame):
        pass_qty = len(df[df.FAIL_FLAG == FailFlag.PASS])
        qty = len(df)
        if qty == 0:
            pass_yield = "0.0%"
        else:
            pass_yield = '{}%'.format(round(pass_qty / qty * 100, 2))
        return {
            'QTY': qty,
            'PASS': pass_qty,
            'YIELD': pass_yield,
        }

    @staticmethod
    def load_prr_df(file_path: str) -> Union[pd.DataFrame, None]:
        """
        理论上, HDF5数据都可以load不会有报错的
        :param file_path:
        :return:
        """
        df = pd.read_hdf(file_path, key="prr_df")
        if not isinstance(df, Df):
            return None
        return df

    @staticmethod
    @Time()
    def load_hdf5_analysis(file_path: str, part_flag: int, read_fail: int, unit_id: int) -> DataModule:
        """
        根据条件来选取数据, 能走到这一步的基本不会有报错了
        TODO:
            ID是文件的ID, 用来区分多个STDF的
            ptmd_df需要被用来做多个文件间的limit对比
            只要想办法让每颗DIE的DIE_ID不同既可以安心的做数据分析处理了
        :return: 在tree中处理并返回
        """
        prr_df = pd.read_hdf(file_path, key="prr_df")
        dtp_df = pd.read_hdf(file_path, key="dtp_df")
        ptmd_df = pd.read_hdf(file_path, key="ptmd_df")
        if not isinstance(prr_df, Df) or not isinstance(dtp_df, Df) or not isinstance(ptmd_df, Df):
            raise Exception("ERROR@!!!load_hdf5_analysis")
        prr_df.insert(0, column="ID", value=unit_id)
        dtp_df.insert(0, column="ID", value=unit_id)
        ptmd_df.insert(0, column="ID", value=unit_id)

        prr_df["DIE_ID"] = prr_df["PART_ID"] + unit_id * GlobalVariable.DIE_ID_ADD
        prr_df["SITE_NUM"] = prr_df["SITE_NUM"].apply(lambda x: 'S{:0>3d}'.format(x))
        # TODO: TEXT看情况是否需要TEST_NUM
        ptmd_df["TEXT"] = ptmd_df["TEST_NUM"].astype(str) + ":" + ptmd_df["TEST_TXT"]
        prr_df = ParserData.get_prr_data(prr_df, part_flag, read_fail)

        dtp_df["DIE_ID"] = dtp_df["PART_ID"] + unit_id * GlobalVariable.DIE_ID_ADD
        dtp_df = dtp_df[dtp_df.PART_ID.isin(prr_df.PART_ID)]
        temp_fail_exec = dtp_df.TEST_FLG & DtpTestFlag.TestFailed == DtpTestFlag.TestFailed
        temp_fail = dtp_df[temp_fail_exec].copy()
        temp_pass = dtp_df[~temp_fail_exec].copy()
        temp_pass["FAIL_FLG"] = FailFlag.PASS
        temp_fail["FAIL_FLG"] = FailFlag.FAIL
        dtp_df = pd.concat([temp_pass, temp_fail])
        dtp_df["FAIL_FLG"] = dtp_df["FAIL_FLG"].astype(np.uint8)

        return DataModule(prr_df=prr_df, dtp_df=dtp_df, ptmd_df=ptmd_df)

    # @staticmethod
    # def contact_with_unstack_data_module(args: ValuesView[DataModule]):
    #     """
    #     先做数据叠加, 时间耗费较长
    #     TODO:
    #         流程:
    #         1. 首先可以先用contact_data_module的模型, 生成一个唯一的DataModule
    #         2. 使用这个DataModule生成UnStackModule
    #         3. 计算top fail等
    #         问题:
    #         1. unstack数据中会有较多的NAN, top fail和 fail rate计算需要注意
    #         2. 如果是limit更新后的数据, 计算起来也会比较麻烦
    #     :param args:
    #     :return:
    #     """
    #     df_module = ParserData.contact_data_module(list(args))
    #     df_module.prr_df.set_index(["DIE_ID"], inplace=True)
    #     df_module.dtp_df.set_index(["TEST_ID", "DIE_ID"], inplace=True)
    #     df_module.prr_df["DA_GROUP"] = "*"
    #     unstack_module = UnStackModule()
    #     # 0.194
    #     temp_result = df_module.dtp_df[["RESULT"]].copy()
    #     temp_need_index = ~temp_result.index.duplicated(keep="last")
    #     temp_result = temp_result[temp_need_index]  # 如果是同一个测试项目, 则取出最后一次测试值
    #     temp_result = temp_result.unstack(0).RESULT
    #     # 1.152
    #     temp_test_flg = df_module.dtp_df[["TEST_FLG"]]
    #     temp_test_flg = temp_test_flg[temp_need_index]
    #     temp_fail_exec = temp_test_flg.TEST_FLG & DtpTestFlag.TestFailed == DtpTestFlag.TestFailed
    #     # 1.153
    #     temp_fail = temp_test_flg[temp_fail_exec].copy()
    #     temp_pass = temp_test_flg[~temp_fail_exec].copy()
    #     temp_pass["TEST_FLG"] = 1
    #     temp_fail["TEST_FLG"] = 0
    #     temp_test_flg = pd.concat([temp_pass, temp_fail])
    #     temp_test_flg["TEST_FLG"] = temp_test_flg["TEST_FLG"].astype(np.uint8)
    #     df_module.
    #     # temp_test_flg = temp_test_flg.unstack(0).TEST_FLG
    #
    #     unstack_module.prr_df = df_module.prr_df
    #     unstack_module.df = temp_result
    #     # unstack_module.test_flg = temp_test_flg
    #
    #     # print(unstack_module.df)
    #     # print(unstack_module.test_flg)
    #     # 2.28
    #
    #     return df_module, unstack_module

    @staticmethod
    @Time()
    def contact_data_module(args: List[DataModule]):
        """
        关键函数, 将多份的数据组合起来, 特别是不同程序的数据, 并将所有的TEST_ID重新分配, 按照 TEST_NUM:TEST_TXT 来分配唯一TEST_ID
        TODO: ID也是用来和Summary链接的桥梁
        :param args:
        :return:
        """
        if len(args) == 1:
            return args[0]
        prr_df_list: list = list()
        dtp_df_list: list = list()
        ptmd_df_list: list = list()
        for data_module in args:
            prr_df_list.append(data_module.prr_df)
            dtp_df_list.append(data_module.dtp_df)
            ptmd_df_list.append(data_module.ptmd_df)
        prr_df = pd.concat(prr_df_list)
        dtp_df = pd.concat(dtp_df_list)
        ptmd_df = pd.concat(ptmd_df_list)

        new_test_id = 0
        ptmd_dict = {}  # 需要生成一份新的PTMD数据, 不绑定ID了
        new_dtps = []
        dtp_dict = dict()
        for (_id, _test_id), _dtp_df in dtp_df.groupby(["ID", "TEST_ID"], sort=False):
            key = "{}-{}".format(_id, _test_id)
            dtp_dict[key] = _dtp_df

        for text, df in ptmd_df.groupby("TEXT", sort=False):
            new_test_id += 1
            for row in df.itertuples():  # type:PtmdModule
                # TODO: 1. 取出所有旧的TEST_ID 2. 替换成新的TEST_ID
                # start = time.perf_counter()
                key = "{}-{}".format(row.ID, row.TEST_ID)
                _dtp_df = dtp_dict[key]
                _dtp_df["TEST_ID"] = new_test_id
                new_dtps.append(_dtp_df)
                # use_time = round(time.perf_counter() - start, 3)
                # print("func: {} exec time: {}.".format("loc", use_time))
                ptmd_dict[new_test_id] = row

        ptmd_df = pd.DataFrame(ptmd_dict.values())
        for k, v in GloVar.PTMD_TYPE_DICT.items():
            ptmd_df[k] = ptmd_df[k].astype(v)
        ptmd_df["TEST_ID"] = ptmd_dict.keys()
        dtp_df = pd.concat(new_dtps)
        return DataModule(prr_df=prr_df, dtp_df=dtp_df, ptmd_df=ptmd_df)
