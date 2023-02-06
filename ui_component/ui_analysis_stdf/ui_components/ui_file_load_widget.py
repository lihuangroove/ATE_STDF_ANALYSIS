"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/5/9 17:44
@Software: PyCharm
@File    : ui_file_load_widget.py
@Remark  : 
"""
import os
import time

from PySide2.QtGui import QColor, QGuiApplication
from PySide2.QtWidgets import QWidget, QHeaderView, QFileDialog, QTableWidgetItem
from PySide2.QtCore import Qt, QThread, Signal, Slot

from typing import List, Set, Union

from common.app_variable import GlobalVariable
from common.li import SummaryCore
from common.stdf_interface.stdf_parser import SemiStdfUtils
from parser_core.stdf_parser_file_write_read import ParserData
from ui_component.ui_analysis_stdf.ui_designer.ui_file_load import Ui_Form as FileLoadForm

from parser_core.dll_parser import LinkStdf
from ui_component.ui_common.my_text_browser import Print


class RunStdfAnalysis(QThread):
    """
    结束测试时间还是非常需要的, 考虑下只有在线版本才有这个功能是否会方便一些
    """
    stdf = None  # type:LinkStdf
    file_list = None  # type:List[dict]
    id = 0
    by_analysis_list: list = None
    eventSignal = Signal(dict)

    def __init__(self, parent=None):
        super(RunStdfAnalysis, self).__init__(parent)
        self.stdf = LinkStdf()
        self.stdf.init()

    def set_analysis_list(self, file_list):
        self.file_list = file_list

    def set_id(self, mid_nm):
        self.id = int(mid_nm * 1000)

    def run(self) -> None:
        if self.file_list is None:
            return
        self.by_analysis_list = []
        for index, each in enumerate(self.file_list):
            # try:
            """ 阻止不同的程序一起解析 """
            # if self.cache_pro is not None and self.cache_pro != each['JOB_NAM']:
            #     self.indexSignal.emit({"index": index, "status": -1, "message": "异同的测试程序!暂无法解析不同程序数据!"})
            #     continue
            start = time.perf_counter()

            _, file_name = os.path.split(each["FILE_PATH"])
            stdf_name = file_name[:file_name.rfind('.')]
            save_path = os.path.join(GlobalVariable.CACHE_PATH, each["LOT_ID"])

            if not os.path.exists(save_path):
                os.mkdir(save_path)
            save_name = os.path.join(save_path, stdf_name + '.h5')
            if not os.path.exists(save_name):
                self.eventSignal.emit({"index": index, "status": 0, "message": "开始解析STDF中!"})
                ParserData.delete_temp_file()
                boolean = self.stdf.parser_stdf_to_csv(each["FILE_PATH"])
                if not boolean:
                    self.eventSignal.emit({"index": index, "status": -1, "message": "STDF文件解析失败!"})
                    continue
                df_module = ParserData.load_csv()
                ParserData.save_hdf5(df_module, save_name)
            else:
                self.eventSignal.emit({"index": index, "status": 0, "message": "缓存文件存在,调用缓存数据!"})

            """
            开始读取prr然后进行数据处理!
            """
            mdi_id = int(self.id + index)
            prr = ParserData.load_prr_df(save_name, unit_id=mdi_id)
            by_analysis_data_dict = {
                **SemiStdfUtils.get_lot_info_by_semi_ate(each["FILE_PATH"], FILE_NAME=file_name, ID=mdi_id),
                **ParserData.get_yield(prr, each["PART_FLAG"], each["READ_FAIL"]),
                "PART_FLAG": each["PART_FLAG"],
                "READ_FAIL": 1 if each["READ_FAIL"] else 0,
                "HDF5_PATH": save_name,
            }
            """ 阻止不同的程序一起解析 """
            # if self.cache_pro is None:
            #     self.cache_pro = by_analysis_data_dict['JOB_NAM']
            use_time = round(time.perf_counter() - start, 2)
            self.by_analysis_list.append(by_analysis_data_dict)
            self.eventSignal.emit(
                {"index": index, "status": 1, "message": "STDF解析文件成功!用时{}s".format(use_time)}
            )
        """数据整理OK"""
        self.eventSignal.emit({"index": len(self.file_list), "status": 11, "message": "数据解析完成"})


class FileLoadWidget(QWidget, FileLoadForm):
    """
    file select
    STDF文件 Load模块,需要使用一种线程池来解析STDF
    建议的做法, 为了节省内存, 做懒处理, FileLoad只解析, 然后提取关键数据给Tree, 减少内存的占用
    缺点就是载入的数据变长了
    """

    finished = Signal()  # 传送父子数据给TreeWidget
    closeSignal = Signal(int)

    th = None  # type:RunStdfAnalysis
    select_file = None  # type:Union[Set[str], None]
    summary: SummaryCore = None

    def __init__(self, summary: SummaryCore, parent=None, space_nm=1):
        super(FileLoadWidget, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("STDF File Select")
        self.summary = summary
        self.space_nm = space_nm
        self.comboBox.addItems(GlobalVariable.PART_FLAGS)
        self.title = "STDF数据载入空间: {}".format(space_nm)
        self.th = RunStdfAnalysis(self)
        self.th.set_id(self.space_nm)
        self.th.finished.connect(self.th_finished)
        self.th.eventSignal.connect(self.th_message_event)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.tableWidget.set_table_head(GlobalVariable.FILE_TABLE_HEAD)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def select_stdf(self) -> List[str]:
        """
        去重复, 读取STDF
        :return:
        """
        path_list, _ = QFileDialog.getOpenFileNames(self,
                                                    'Open Stdf File',
                                                    filter='stdf(*.std;*.stdf;*.std_temp)',
                                                    # options=QFileDialog.DontUseNativeDialog,
                                                    )
        return path_list

    def select_stdf_directory(self) -> List[str]:
        """
        从整个文件夹下选取所有的文件
        """
        directory = QFileDialog.getExistingDirectory(self, "getExistingDirectory", "./")
        return self.scan_directory(directory)

    @staticmethod
    def scan_directory(directory):
        path_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                suffix = os.path.splitext(file)[-1]
                if suffix in GlobalVariable.STD_SUFFIXES:
                    path_list.append(os.path.join(root, file))
        return path_list

    def first_select(self):
        """
        初始化选择
        :return:
        """
        self.select_file = set()
        select_stdf = self.select_stdf()
        if len(select_stdf) == 0:
            return Print.warning("无文件被选取!")
        self.select_file = set(select_stdf)
        self.analysis_path_stdf_by_semi_ate()

    def first_directory_select(self):
        """
        初始化文件夹下文件选择
        """
        self.select_file = set()
        select_stdf = self.select_stdf_directory()
        if len(select_stdf) == 0:
            return Print.warning("无文件被选取!")
        self.select_file = set(select_stdf)
        self.analysis_path_stdf_by_semi_ate()

    def directory_select_test(self, test_path):
        select_stdf = self.scan_directory(test_path)
        if len(select_stdf) == 0:
            return Print.warning("无文件被选取!")
        self.select_file = set(select_stdf)
        self.analysis_path_stdf_by_semi_ate()

    def analysis_path_stdf_by_semi_ate(self):
        """
        执行数据载入, 并按照时间排序
        :return:
        """
        if not self.select_file:
            return Print.warning("无文件被选取, 无法执行分析!")
        table_data = []
        for filepath in self.select_file:
            table_data.append(SemiStdfUtils.get_lot_info_by_semi_ate(filepath))
        table_data = sorted(table_data, key=lambda ev: ev['SETUP_T'])
        self.tableWidget.set_table_data(table_data)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(self.tableWidget.table_count)

    @Slot()
    def on_pushButton_2_pressed(self):
        """
        追加选择数据
        :return:
        """
        select_stdf = self.select_stdf()
        if len(select_stdf) == 0:
            return Print.warning("无文件被选取!")
        if set(select_stdf) == self.select_file:
            return Print.warning("文件结构未改变!")
        if self.select_file is None:
            self.select_file = set()
        self.select_file = self.select_file | set(select_stdf)
        self.analysis_path_stdf_by_semi_ate()

    @Slot()
    def on_pushButton_3_pressed(self):
        self.tableWidget.set_read_all_r(Qt.Checked)

    @Slot()
    def on_pushButton_4_pressed(self):
        self.tableWidget.set_read_all_r(Qt.Unchecked)

    @Slot()
    def on_pushButton_6_pressed(self):
        self.select_file = set()
        self.tableWidget.clearContents()

    @Slot(int)
    def on_comboBox_currentIndexChanged(self, e):
        self.tableWidget.set_all_part_flag(e)

    @Slot(dict)
    def th_message_event(self, info: dict):
        index = info['index']
        self.progressBar.setValue(index)
        if index == self.tableWidget.table_count:
            return Print.info("{} > 完成数据解析!".format(self.title))
        # self.tableWidget.selectRow(index)
        item = QTableWidgetItem(info['message'])
        if info['status'] == -1:
            item.setBackground(QColor(255, 110, 55))
        elif info['status'] == 0:
            item.setBackground(QColor(180, 208, 201))
        else:
            item.setBackground(QColor(176, 255, 210))
        self.tableWidget.update_table_data(index, "MESSAGE", item)

    def th_finished(self):
        """
        接收后台整理好的数据到前台调用
        :return:
        """
        self.summary.set_data(self.th.by_analysis_list)
        self.finished.emit()
        self.pushButton.setEnabled(True)

    @Slot()
    def on_pushButton_pressed(self):
        """
        想要RUN之前得进行一些判定
        使用线程池进行数据处理
        可以给前台传一个Process
        给线程传入R, R版本才会分析Fail项目
        :return:
        """
        if self.tableWidget.table_count == 0:
            return Print.warning("无文件结构被读取")
        self.tableWidget.update_temp_data()
        self.th.set_analysis_list(self.tableWidget.temp_table_data)
        self.th.start()
        self.pushButton.setEnabled(False)

    def keyPressEvent(self, event):
        """ Ctrl + C复制表格内容 """
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            # 获取表格的选中行
            ranges = self.tableWidget.selectedRanges()
            if not ranges:
                return
            selected_ranges = ranges[0]  # 只取第一个数据块,其他的如果需要要做遍历,简单功能就不写得那么复杂了
            text_str = "\t".join(GlobalVariable.FILE_TABLE_HEAD) + '\n'  # 最后总的内容
            # 行（选中的行信息读取）
            for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
                row_str = ""
                # 列（选中的列信息读取）
                for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
                    item = self.tableWidget.item(row, col)
                    if item is None:
                        row_str += '\t'
                        continue
                    row_str += item.text() + '\t'  # 制表符间隔数据
                text_str += row_str + '\n'  # 换行
            clipboard = QGuiApplication.clipboard()  # 获取剪贴板
            clipboard.setText(text_str)  # 内容写入剪贴板
