#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : stdf_class.py
@Author  : Link
@Time    : 2021/7/31 13:32
@Mark    : 必须要3.7及以下的python版本, 更高的版本无法顺利载入dll, 本人已经放弃
"""
import ctypes
import os
import itertools
import string


class LinkStdf:
    stdf = None
    import_status = False

    def __init__(self):
        cur_path = os.path.dirname(__file__)
        dll_path = os.path.join(cur_path, "")
        self.std_dll = ctypes.cdll.LoadLibrary(os.path.join(dll_path, "./stdf_ctype.dll"))
        """
        init func
        """
        "生成类"
        self._detector_new_func = self.std_dll.NewStdf
        self._detector_new_func.restype = ctypes.c_void_p
        "获取到Finish_T"
        self._get_finish_t = self.std_dll.GetFinishT
        self._get_finish_t.argtypes = [ctypes.c_void_p]
        self._get_finish_t.restype = ctypes.c_int
        "执行STDF CSV数据文件生成. 后续要么改成HDF5要么就用pybin11"
        self._parser_stdf_to_csv = self.std_dll.ParserStdfToHdf5
        self._parser_stdf_to_csv.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_char_p]
        self._parser_stdf_to_csv.restype = ctypes.c_bool
        "清空stdf缓存"
        self._delete_stdf_func = self.std_dll.DeleteStdf
        self._delete_stdf_func.argtypes = [ctypes.c_void_p]
        self._delete_stdf_func.restype = ctypes.c_bool

    def init(self):
        """
        初始化类
        """
        if self.stdf:
            self._delete_stdf_func(self.stdf)
        self.stdf = self._detector_new_func()

    def clear(self):
        if self.stdf:
            self._delete_stdf_func(self.stdf)
            self.stdf = None

    def __del__(self):
        if self.stdf:
            self._delete_stdf_func(self.stdf)
            self.stdf = None
        del self.std_dll

    def parser_stdf_to_csv(self, stdf_file: str, save_path: str):
        resp = self._parser_stdf_to_csv(self.stdf, self.string_to_wchar(stdf_file), self.string_to_char(save_path))
        self.import_status = True if resp else False
        return resp

    def get_finish_t(self):
        if not self.import_status:
            return 0
        return self._get_finish_t(self.stdf)

    @staticmethod
    def string_to_char(_string: str) -> ctypes.Array:
        return ctypes.create_string_buffer(bytes(_string, encoding='utf8'))

    @staticmethod
    def string_to_wchar(_string: str):
        return ctypes.create_unicode_buffer(_string)

    @staticmethod
    def char_to_string(c_char: ctypes.c_char_p) -> str:
        temp_bytes = ctypes.string_at(c_char)
        return temp_bytes.decode("utf-8")

    @staticmethod
    def generator_a_z():
        length = 1
        while length:
            for letters in itertools.product(string.ascii_uppercase, repeat=length):
                yield ''.join(letters)
            length += 1
