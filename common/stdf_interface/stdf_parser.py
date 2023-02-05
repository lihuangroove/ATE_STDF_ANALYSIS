"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2021/12/13 20:20
@Software: PyCharm
@File    : stdf_parser.py
@Remark  : 
"""
import os

from Semi_ATE import STDF
from common.app_variable import GlobalVariable


class SemiStdfUtils:
    @staticmethod
    def is_std(file_name):
        suffix = os.path.splitext(file_name)[-1]
        if suffix not in GlobalVariable.STD_SUFFIXES:
            return False
        return True

    @staticmethod
    def get_lot_info_by_semi_ate(filepath: str, **kwargs) -> dict:
        data_dict = {
            "FILE_PATH": filepath,
            **kwargs,
            "LOT_ID": "",
            "SBLOT_ID": "",
            "WAFER_ID": "",
            "BLUE_FILM_ID": "",
            'TEST_COD': '',
            'FLOW_ID': '',
            'PART_TYP': '',
            'JOB_NAM': '',
            'TST_TEMP': '',
            'NODE_NAM': '',
            'SETUP_T': 0,
            'START_T': 0,
            'SITE_CNT': 0,
        }
        for REC in STDF.records_from_file(filepath):
            if REC.id == "PIR": break
            if REC is None: continue
            if REC.id == "MIR":
                mir = REC.to_dict()
                data_dict["LOT_ID"] = mir["LOT_ID"]
                data_dict["SBLOT_ID"] = mir["SBLOT_ID"]

                data_dict["TEST_COD"] = mir["TEST_COD"]
                data_dict["FLOW_ID"] = mir["FLOW_ID"]
                data_dict["PART_TYP"] = mir["PART_TYP"]
                data_dict["JOB_NAM"] = mir["JOB_NAM"]
                data_dict["TST_TEMP"] = mir["TST_TEMP"]
                data_dict["NODE_NAM"] = mir["NODE_NAM"]

                data_dict["SETUP_T"] = mir["SETUP_T"]
                data_dict["START_T"] = mir["START_T"]

            if REC.id == "WIR":
                wir = REC.to_dict()
                if wir["HEAD_NUM"] == 233:
                    data_dict["BLUE_FILM_ID"] = wir["WAFER_ID"]
                else:
                    data_dict["WAFER_ID"] = wir["WAFER_ID"]

            if REC.id == "WCR":
                pass

            if REC.id == "SDR":
                sdr = REC.to_dict()
                data_dict["SITE_CNT"] = sdr["SITE_CNT"]

        return data_dict
