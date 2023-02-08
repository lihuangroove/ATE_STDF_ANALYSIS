#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : csv_read_test.py
@Author  : Link
@Time    : 2022/12/21 23:29
@Mark    : 
"""
import os
import unittest

from app_test.test_utils.log_utils import Print
from app_test.test_utils.mixins import CsvDataLoad
from app_test.test_utils.wrapper_utils import Tester
from common.app_variable import GlobalVariable as GloVar, TestVariable
from common.cal_interface.pandas_utils import PandasStdfUtils
from parser_core.dll_parser import LinkStdf
from parser_core.stdf_parser_file_write_read import ParserData


class ReadCsvCase(unittest.TestCase, CsvDataLoad):
    """
    从缓存的csv文件中读取数据
    """

    def test_something(self):
        self.assertEqual(True, True)

    @Tester()
    def test_delete_temp_file(self):
        """
        测试的时候不用删除
        :return:
        """
        ParserData.delete_temp_file()

    def test_parser_stdf_to_csv(self):
        stdf = LinkStdf()
        stdf.init()
        boolean: bool = stdf.parser_stdf_to_csv(TestVariable.STDF_PATH, TestVariable.TEMP_PATH)
        self.assertEqual(True, boolean)
        print(stdf.get_finish_t())
        del stdf

    @Tester(
        ["load_data"],
        exec_time=True,
    )
    def test_load_data(self):
        self.assertEqual(True, self.load)
        print(self.df_module.prr_df)

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_gen_pcr(self):
        pcr_list = [PandasStdfUtils.df_generator_pcr(df=self.df_module.prr_df, head_num=0xff, site_num=0xff)]
        for site, each_df in self.df_module.prr_df.groupby("SITE_NUM"):
            if not isinstance(site, int):
                continue
            pcr_list.append(PandasStdfUtils.df_generator_pcr(each_df, 1, site))
        Print.print_table(pcr_list)

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_gen_hbr(self):
        """

        :return:
        """
        hbr_list = PandasStdfUtils.df_generator_hbr(self.df_module.prr_df, 0xff, 0xff, )
        for site, each_df in self.df_module.prr_df.groupby("SITE_NUM"):
            if not isinstance(site, int):
                continue
            hbr_list += PandasStdfUtils.df_generator_hbr(each_df, 1, site)
        Print.print_table(hbr_list)

    @Tester(
        ["load_data"],
        exec_time=True,
        skip_args_time=True,
    )
    def test_gen_sbr(self):
        sbr_list = PandasStdfUtils.df_generator_sbr(self.df_module.prr_df, 0xff, 0xff, )
        for site, each_df in self.df_module.prr_df.groupby("SITE_NUM"):
            if not isinstance(site, int):
                continue
            sbr_list += PandasStdfUtils.df_generator_sbr(each_df, 1, site)
        Print.print_table(sbr_list)

    @Tester(
        ["load_data"],
        exec_time=True,
    )
    def test_save_hdf5(self):
        hdf_full_path = os.path.join(GloVar.CACHE_PATH, '{}.h5'.format("TEST"))
        ParserData.save_hdf5(self.df_module, hdf_full_path)
