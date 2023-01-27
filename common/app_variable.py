"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2021/12/16 9:21
@Software: PyCharm
@File    : app_variable.py
@Remark  : 
"""
import os
from dataclasses import dataclass
from typing import Union, Dict

import pandas as pd
from numpy import (
    uint8 as U1,
    uint16 as U2,
    uint32 as U4,
    int8 as I1,
    int16 as I2,
    int32 as I4,
    float32 as R4,
    float64 as R8,
    nan
)


# 尽可能将数据类型都定义为 dataclass 或是 nametuple, 比dict数据容易操作, 最好是nametuple

@dataclass
class PtmdModule:
    ID: int  # UI赋予的ID
    TEST_ID: int
    DATAT_TYPE: str
    TEST_NUM: int
    TEST_TXT: str
    PARM_FLG: int
    OPT_FLAG: int
    RES_SCAL: int
    LLM_SCAL: int
    HLM_SCAL: int
    LO_LIMIT: float
    HI_LIMIT: float
    UNITS: str
    TEXT: str


@dataclass
class Calculation:
    """
    暂未用到
    """
    TEST_ID: int
    DATAT_TYPE: str
    TEST_NUM: int
    TEST_TXT: str
    UNITS: str
    LO_LIMIT: float
    HI_LIMIT: float
    AVG: float
    STD: float
    CPK: float
    QTY: int
    FAIL_QTY: int
    FAIL_RATE: float
    REJECT_QTY: int
    REJECT_RATE: float
    MIN: float
    MAX: float
    LO_LIMIT_TYPE: Union[str, float]
    HI_LIMIT_TYPE: Union[str, float]
    ALL_DATA_MIN: float
    ALL_DATA_MAX: float
    TEXT: str


@dataclass
class DataLiBackup:
    select_summary: pd.DataFrame = None
    prr_df: pd.DataFrame = None


@dataclass
class ToChartCsv:
    # TODO: Must
    df: pd.DataFrame = None  # 所有数据
    group_df: Dict[str, pd.DataFrame] = None
    chart_df: pd.DataFrame = None  # 前台展示数据, 基于分组后的select
    group_chart_df: Dict[str, pd.DataFrame] = None
    select_group: set = None

    # TODO: Optional PAT
    limit: pd.DataFrame = None
    group_limit: Dict[str, pd.DataFrame] = None


@dataclass
class DataModule:
    """
    数据空间整合后的数据模型
    """
    prr_df: pd.DataFrame = None
    dtp_df: pd.DataFrame = None  # 数据
    ptmd_df: pd.DataFrame = None  # 测试项目相关


class DatatType:
    FTR: str = "FTR"
    PTR: str = "PTR"
    MPR: str = "MPR"


class FailFlag:
    PASS = 1
    FAIL = 0


class LimitType:
    NoHighLimit = "NA"
    EqualHighLimit = "LE"
    ThenHighLimit = "LT"

    NoLowLimit = "NA"
    EqualLowLimit = "GE"
    ThenLowLimit = "GT"


class PartFlags:
    ALL = 0
    FIRST = 1
    RETEST = 2
    FINALLY = 3
    XY_COORD = 4
    PART_FLAGS = ('ALL', 'FIRST', 'RETEST', 'FINALLY', "XY_COORD")


class GlobalVariable:
    """
    用来放一些全局变量
    TODO: 以大写作为主要的HEAD
    """
    DEBUG = True
    SAVE_PKL = False  # 用来将数据保存到二进制数据中用来做APP测试 TODO: 此版本暂时作废
    SQLITE_PATH = r"D:\1_STDF\stdf_info.db"  # 用于存summary

    CACHE_PATH = r"D:\1_STDF\STDF_CACHE"
    JMP_CACHE_PATH = r"D:\1_STDF\JMP_CACHE"
    LIMIT_PATH = r"D:\1_STDF\LIMIT_CACHE"
    NGINX_PATH = r"D:\1_STDF\NGINX_CACHE"

    STD_SUFFIXES = {
        ".std",
        ".stdf",
        ".std_temp"  # py_ate
    }
    LOT_TREE_HEAD = (
        "ID", "LOT_ID", "SBLOT_ID", "WAFER_ID", "BLUE_FILM_ID", "TEST_COD", "FLOW_ID", "QTY", "PASS",
        "YIELD", "PART_TYP", "JOB_NAM", "NODE_NAM", "SITE_CNT", "START_T"
    )
    LOT_TREE_HEAD_LENGTH = len(LOT_TREE_HEAD)

    PART_FLAGS = PartFlags.PART_FLAGS
    FILE_TABLE_HEAD = ("READ_FAIL", "PART_FLAG", "MESSAGE", "LOT_ID", "SBLOT_ID", "WAFER_ID", "TEST_COD", "FLOW_ID",
                       "PART_TYP", "JOB_NAM", "NODE_NAM", "SETUP_T", "START_T", "TST_TEMP", "FILE_PATH")
    SKIP_FILE_TABLE_DATA_HEAD = {"READ_FAIL", "PART_FLAG"}

    # Save memory
    PRR_HEAD = ("PART_ID", "HEAD_NUM", "SITE_NUM", "X_COORD", "Y_COORD", "HARD_BIN", "SOFT_BIN", "PART_FLG",
                "NUM_TEST", "FAIL_FLAG", "TEST_T")
    PRR_TYPE = (U2, U1, U1, I2, I2, U2, U2, U1, U2, U1, U4,)
    PRR_TYPE_DICT = dict(zip(PRR_HEAD, PRR_TYPE))

    DTP_HEAD = ("PART_ID", "TEST_ID", "RESULT", "TEST_FLG", "PARM_FLG", "OPT_FLAG", "LO_LIMIT", "HI_LIMIT")
    DTP_TYPE = (U2, U4, R4, U1, U1, U1, R4, R4)
    DTP_TYPE_DICT = dict(zip(DTP_HEAD, DTP_TYPE))

    PTMD_HEAD = ("TEST_ID", "DATAT_TYPE", "TEST_NUM", "TEST_TXT", "PARM_FLG", "OPT_FLAG", "RES_SCAL", "LLM_SCAL",
                 "HLM_SCAL", "LO_LIMIT", "HI_LIMIT", "UNITS")
    PTMD_TYPE = (U2, str, U4, str, U1, U1, I1, I1, I1, R4, R4, str)
    PTMD_TYPE_DICT = dict(zip(PTMD_HEAD, PTMD_TYPE))

    JMP_SCRIPT_HEAD = ["GROUP", "DA_GROUP", "PART_ID", "X_COORD", "Y_COORD", "HARD_BIN", "SOFT_BIN", "FAIL_FLAG"]

    DIE_ID_ADD = 1000000

    TEST_ID_COLUMN = 0
    TEST_TYPE_COLUMN = 1
    TEST_NUM_COLUMN = 2
    TEST_TXT_COLUMN = 3
    LO_LIMIT_COLUMN = 5
    HI_LIMIT_COLUMN = 6
    CPK_COLUMN = 9
    TOP_FAIL_COLUMN = 11
    REJECT_COLUMN = 13
    LO_LIMIT_TYPE_COLUMN = 17
    HI_LIMIT_TYPE_COLUMN = 18

    @staticmethod
    def init():
        if not os.path.exists(GlobalVariable.CACHE_PATH):
            os.makedirs(GlobalVariable.CACHE_PATH)
        if not os.path.exists(GlobalVariable.JMP_CACHE_PATH):
            os.makedirs(GlobalVariable.JMP_CACHE_PATH)


class TestVariable:
    """
    用于测试的各种路径
    """
    TEMP_PATH = os.getenv("TEMP")

    TEMP_PRR_PATH = os.path.join(TEMP_PATH, "StdfTempPrr.csv")
    TEMP_DTP_PATH = os.path.join(TEMP_PATH, "StdfTempDtp.csv")
    TEMP_PTMD_PATH = os.path.join(TEMP_PATH, "StdfTempPtmd.csv")
    TEMP_BIN_PATH = os.path.join(TEMP_PATH, "StdfTempHardSoftBin.csv")

    PATHS = (TEMP_PRR_PATH, TEMP_DTP_PATH, TEMP_PTMD_PATH, TEMP_BIN_PATH)

    # HDF5_PATH = os.path.join(GlobalVariable.CACHE_PATH, "TEST_DATA.h5")
    HDF5_PATH = r"D:\1_STDF\STDF_CACHE\TEST_DATA.h5"
    HDF5_2_PATH = r"D:\1_STDF\STDF_CACHE\TEST.h5"
    HDF5_3_PATH = r"D:\1_STDF\STDF_CACHE\N49HT00000\DEMO1_CP1.h5"
    # HDF5_PATH = r".\test_data\TEST.h5"

    TABLE_PICKLE_PATH = os.path.join(GlobalVariable.CACHE_PATH, '{}.pkl'.format("TABLE_DATA"))

    STDF_PATH = r"D:\SWAP\TEST_DATA.std"
    STDF_FILES_PATH = r"D:\SWAP\TE"
