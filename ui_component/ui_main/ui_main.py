"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/4/29 15:27
@Software: PyCharm
@File    : ui_main.py
@Remark  : 
"""

import pandas as pd
import psutil
import datetime as dt
from typing import List, Dict, Union
import gc

from PySide2.QtCore import QTimer, Slot, Qt, QObject
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QMdiArea, QMessageBox, \
    QInputDialog, QAction

from pyqtgraph.dockarea import *

from chart_core.chart_jmp.jmp_box import JmpBox
from chart_core.chart_jmp.jmp_factory import JmpFactory
from chart_core.chart_jmp.jmp_file import JmpFile
from chart_core.chart_jmp.jmp_plot import JmpPlot
from chart_core.chart_jmp.jmp_script_factory import JmpScript
from chart_core.chart_jmp_factory.class_jmp_factory import NewJmpFactory
from chart_core.chart_pyqtgraph.ui_components.chart_sample_line import PyqtCanvas
from common.app_variable import GlobalVariable
from ui_component.ui_common.my_text_browser import UiMessage, MQTextBrowser
from ui_component.ui_common.ui_utils import MdiLoad
from ui_component.ui_main.mdi_data_concat import ContactWidget
from ui_component.ui_main.ui_designer.ui_main import Ui_MainWindow
from ui_component.ui_main.ui_jmp_select import JmpSelect
from ui_component.ui_main.ui_setting import SettingWidget
from ui_component.ui_main.mapping_select import MappingSelect
from ui_component.ui_analysis_stdf.ui_stdf import StdfLoadUi
from ui_component.ui_app_variable import UiGlobalVariable


class Main_Ui(QMainWindow, Ui_MainWindow):
    mdi_count = 0
    mdi_cache = None  # type: Dict[int, MdiLoad]  # int:mdi_count
    focus_id = 0

    def __init__(self, parent=None, license_control=False):
        super(Main_Ui, self).__init__(parent)
        self.setupUi(self)
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(":/pyqt/source/images/icon_swf.svg"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(self.icon)
        self.area = DockArea()
        self.setCentralWidget(self.area)
        self.license_control = license_control

        " ??????????????????MDI, MDI??????????????????MERGE???CONTACT????????? "
        self.mdi_cache = {}

        " ?????????????????????????????? "
        self.setting = SettingWidget(self)
        dock_table = Dock("CHART SETTING", size=(100, 600))
        dock_table.addWidget(self.setting)
        self.setting.comboBox.currentIndexChanged[str].connect(self.q_action_visible)

        " ???table????????????????????????QTextBrowser,??????????????????????????? "
        self.text_browser = MQTextBrowser(self)
        dock_text_browser = Dock("TextBrowser", size=(100, 400))
        dock_text_browser.addWidget(self.text_browser)
        self.text_browser.setTextInteractionFlags(Qt.TextEditable)
        self.text_browser.setLineWrapMode(MQTextBrowser.NoWrap)

        self.area.addDock(dock_table, "left")
        self.area.addDock(dock_text_browser, "bottom", dock_table)

        """
        ????????????????????????
        ???????????????????????????????????????, ?????????????????????????????????
        """
        self.load_widget_mdi = QMdiArea(self)
        self.load_widget_mdi.scrollContentsBy(2000, 2000)
        self.load_widget_mdi.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.load_widget_mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        dock_stdf_windows = Dock("Load STDF Mdi Widget", size=(400, 300))
        self.area.addDock(dock_stdf_windows, "right")
        dock_stdf_windows.addWidget(self.load_widget_mdi)

        self.cpu_percent = []
        self.rom_percent = []
        self.monitor_widget = QWidget(self)
        self.monitor_widget_verticalLayout = QVBoxLayout(self.monitor_widget)
        self.cpu_percent_pg, _ = PyqtCanvas.set_graph_ui(self.monitor_widget_verticalLayout, "CPU????????????")
        self.rom_percent_pg, _ = PyqtCanvas.set_graph_ui(self.monitor_widget_verticalLayout, "??????????????????")

        dock_monitor = Dock("System Status", size=(100, 300))
        dock_monitor.addWidget(self.monitor_widget)

        self.area.addDock(dock_monitor, "bottom", dock_text_browser)
        self.area.moveDock(dock_text_browser, 'above', dock_monitor)

        self.mapping_select_dialog = MappingSelect(None, self.icon)
        self.mapping_select_dialog.bin_signal.connect(self.jmp_mapping_init_with_run)

        self.jmp_select_dialog = JmpSelect(None, self.icon)
        self.jmp_select_dialog.itemSignal.connect(self.jmp_models_init_with_run)

        self.mdi_contact_dialog = ContactWidget(None, self.icon)
        self.mdi_contact_dialog.messageSignal.connect(self.mdi_space_message_emit)
        self.mdi_contact_dialog.dataSignal.connect(self.mdi_space_data_contact)

        self.recode_timer = QTimer(self)
        self.recode_timer.timeout.connect(self.recode_system_status)
        self.recode_timer.start(3000)
        self.now_space_timer = QTimer(self)
        self.now_space_timer.timeout.connect(self.scan_now_space)
        self.now_space_timer.start(300)

        if not license_control:
            for each in UiGlobalVariable.WEB_ACTIONS:
                action: QAction = getattr(self, each.name)
                action.setVisible(False)

    def m_append(self, mes: UiMessage):
        self.text_browser.m_append(mes)

    def recode_system_status(self):
        """
        ??????????????????
        :return:
        """
        if len(self.rom_percent) > 320:
            self.rom_percent.pop(0)
            self.cpu_percent.pop(0)
        rom_percent = psutil.virtual_memory()[2]
        cpu_percent = psutil.cpu_percent()
        self.rom_percent.append(rom_percent)
        self.cpu_percent.append(cpu_percent)
        rom_pen = '#FFA500' if rom_percent > 85 else 'g'
        cpu_pen = '#FFA500' if cpu_percent > 85 else 'g'
        rom_pen = 'r' if rom_percent > 95 else rom_pen
        cpu_pen = 'r' if cpu_percent > 95 else cpu_pen
        self.cpu_percent_pg.plot(self.cpu_percent, pen=cpu_pen, clear=True)
        self.rom_percent_pg.plot(self.rom_percent, pen=rom_pen, clear=True)

    def scan_now_space(self):
        now = self.load_widget_mdi.activeSubWindow()
        if now is not None:
            """
            ????????????????????????????????? focus_id ?????????cache???
            """
            self.focus_id = now.widget().space_nm

    def check_focus_id_with_return(self) -> Union[None, QObject]:
        if self.focus_id in self.mdi_cache:
            mdi_load = self.mdi_cache[self.focus_id]  # type:MdiLoad
            return mdi_load.mdi

    @Slot()
    def on_action_add_stdf_module_triggered(self):
        """
        ????????????, ???MDI?????????
        :return:
        """
        self.mdi_count += 1
        home_load_mdi = StdfLoadUi(self, space_nm=self.mdi_count)
        home_load_mdi.closeSignal.connect(self.mdi_space_delete)
        self.mdi_cache[self.mdi_count] = MdiLoad(
            self.mdi_count, home_load_mdi, "STDF??????????????????: {}".format(self.mdi_count)
        )
        self.load_widget_mdi.addSubWindow(home_load_mdi)
        home_load_mdi.show()

    @Slot()
    def on_action_path_select_triggered(self):
        """
        ????????????, ???MDI?????????, ????????????????????????
        """
        self.mdi_count += 1
        home_load_mdi = StdfLoadUi(self, space_nm=self.mdi_count, path_select=True)
        home_load_mdi.closeSignal.connect(self.mdi_space_delete)
        self.mdi_cache[self.mdi_count] = MdiLoad(
            self.mdi_count, home_load_mdi, "STDF??????????????????: {}".format(self.mdi_count)
        )
        self.load_widget_mdi.addSubWindow(home_load_mdi)
        home_load_mdi.show()

    @Slot()
    def on_action_pyside2_triggered(self):
        QApplication.aboutQt()

    @Slot()
    def on_action_email_triggered(self):
        if self.message_show(
                'mail.To = "lihuan.hello@qq.com"\r\nmail.Cc = "865789047@qq.com"\r\n??????????????????outlook????????????'
        ):
            QTimer.singleShot(0, self.send_email)

    @staticmethod
    def send_email():
        pass

    @Slot()
    def on_action_cascade_triggered(self):
        self.load_widget_mdi.cascadeSubWindows()

    @Slot(str)
    def q_action_visible(self, backend: str):
        for each in UiGlobalVariable.ALL_CHART_ACTIONS:
            action: QAction = getattr(self, each.name)
            action.setVisible(False)
        if backend == UiGlobalVariable.PLOT_BACKEND[0]:
            for each in UiGlobalVariable.JMP_CHARTS:
                action: QAction = getattr(self, each.name)
                action.setVisible(True)
        if backend == UiGlobalVariable.PLOT_BACKEND[1]:
            for each in UiGlobalVariable.QT_GRAPH_CHARTS:
                action: QAction = getattr(self, each.name)
                action.setVisible(True)
        if backend == UiGlobalVariable.PLOT_BACKEND[2]:
            for each in UiGlobalVariable.ALTAIR_CHARTS:
                action: QAction = getattr(self, each.name)
                action.setVisible(True)

    @Slot()
    def mdi(self) -> QWidget:
        mdi = self.check_focus_id_with_return()  # type:StdfLoadUi
        if mdi is None:
            return self.mdi_space_message_emit("???????????????@")
        if mdi.li.to_chart_csv_data.df is None:
            return self.mdi_space_message_emit("???????????????????????????!@")
        return mdi

    def get_df_use_to_chart_or_csv(self, no_test_id: bool = False):
        """

        :return:
            jmp_df: ??????
            jmp_limit: limit namedtuple
            jmp_cpk: li.cpk_dict ?????????
        """
        mdi = self.mdi()  # type:StdfLoadUi
        if mdi is None:
            return
        return mdi.get_select_data_to_csv_or_jmp_or_altair(no_test_id)

    @Slot()
    def on_action_distribution_triggered(self):
        """ ??????????????? """
        data = self.get_df_use_to_chart_or_csv()
        if data is None:
            return
        jmp_df, temp_calculation = data
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            if UiGlobalVariable.JmpPlotSeparation:
                for key, df in jmp_df.groupby("GROUP"):
                    save_csv_path = "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, key)
                    self.jmp_distribution_show(df, temp_calculation, title=key, save_csv=save_csv_path)
            else:
                save_csv_path = "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, 'all_data')
                self.jmp_distribution_show(jmp_df, temp_calculation, save_csv=save_csv_path)

    def jmp_distribution_show(self, jmp_df, temp_calculation, title: str = "dis_all",
                              save_csv: str = "D:/1_STDF/JMP_CACHE/temp_jmp_data.csv"):
        csv_file_path = self.save_df_to_csv(jmp_df, save_csv)
        if csv_file_path is None:
            return self.mdi_space_message_emit('CSV??????????????????!!!@')
        jmp_script = JmpScript.factory(
            JmpFile.load_csv_file(csv_file_path),
            NewJmpFactory.jmp_distribution(
                capability=temp_calculation, title=title
            )
        )
        JmpFile.save_with_run_script(
            jmp_script, scrip_name="{}/temp_{}.jsl".format(GlobalVariable.JMP_CACHE_PATH, title)
        )

    @Slot()
    def on_action_distribution_trans_triggered(self, script_name='distribution'):
        """ ??????????????? """
        # if GlobalVariable.SAVE_PKL:
        #     mdi = self.mdi()  # type:StdfLoadUi
        #     mdi.li.save_to_obj(script_name)
        data = self.get_df_use_to_chart_or_csv()
        if data is None:
            return
        jmp_df, temp_calculation = data
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            distribution_csv_path = self.save_df_to_csv(
                jmp_df, "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, script_name)
            )
            if distribution_csv_path is None:
                return self.message_show('CSV??????????????????!!! ')
            jmp_script = JmpScript.factory(
                JmpFile.load_csv_file(distribution_csv_path),
                NewJmpFactory.jmp_distribution_trans_bar(capability=temp_calculation)
            )
            JmpFile.save_with_run_script(
                jmp_script, scrip_name="{}/temp_{}.jsl".format(GlobalVariable.JMP_CACHE_PATH, script_name)
            )

    @Slot()
    def on_action_comparing_triggered(self, script_name='fit_plot_data'):
        """ ??????????????? """
        # if GlobalVariable.SAVE_PKL:
        #     mdi = self.mdi()  # type:StdfLoadUi
        #     mdi.li.save_to_obj(script_name)
        data = self.get_df_use_to_chart_or_csv()
        if data is None:
            return
        jmp_df, temp_calculation = data
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            fit_csv_path = self.save_df_to_csv(jmp_df,
                                               "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, script_name))
            if fit_csv_path is None:
                return self.message_show(f'CSV??????????????????!!! ')
            jmp_script = JmpScript.factory(
                JmpFile.load_csv_file(fit_csv_path),
                JmpFactory.comparing(temp_calculation)
            )
            JmpFile.save_with_run_script(
                jmp_script, scrip_name='{}/temp_{}.jsl'.format(GlobalVariable.JMP_CACHE_PATH, script_name)
            )

    @Slot()
    def on_action_linear_triggered(self, script_name='jmp_point_data'):
        """ ???????????? """
        remark, _ = QInputDialog.getText(self, "???????????????", "?????????????????????????????????????????????????????? TEST_ID")
        try:
            remark = int(remark)
        except ValueError:
            return self.message_show("?????????????????????????????????,??????: TEST_ID -> 10001")
        mdi = self.mdi()  # type:StdfLoadUi
        if mdi is None:
            return
        if remark not in mdi.li.capability_key_dict.keys():
            return self.message_show("?????????????????????????????????!")
        test_id_list = mdi.get_test_id_column()
        if test_id_list is None:
            self.message_show("?????????????????????????????????????????????@")
            return
        if remark not in mdi.li.capability_key_dict:
            test_id_list.append(remark)
        jmp_df, temp_calculation = mdi.li.get_unstack_data_to_csv_or_jmp_or_altair(test_id_list)
        fit_csv_path = self.save_df_to_csv(
            jmp_df, "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, script_name)
        )
        if fit_csv_path is None:
            return self.message_show(f'CSV??????????????????!!! ')
        jmp_script = JmpScript.factory(
            JmpFile.load_csv_file(fit_csv_path),
            JmpBox.new_window(JmpBox.new_outline_box(
                *JmpBox.new_group_item(
                    *[JmpPlot.line_fit(self.li.get_text_by_test_id(remark), arg, group=True)
                      for arg in temp_calculation.keys()],
                    col=UiGlobalVariable.JmpPlotColumn
                )
            ))
        )
        JmpFile.save_with_run_script(
            jmp_script, scrip_name='{}/temp_{}.jsl'.format(GlobalVariable.JMP_CACHE_PATH, script_name)
        )

    @Slot()
    def on_action_scatter_triggered(self, script_name='distribution_scatter'):
        """ ????????? """
        # if GlobalVariable.SAVE_PKL:
        #     mdi = self.mdi()  # type:StdfLoadUi
        #     mdi.li.save_to_obj(script_name)
        data = self.get_df_use_to_chart_or_csv()
        if data is None:
            return
        jmp_df, temp_calculation = data
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            distribution_csv_path = self.save_df_to_csv(
                jmp_df, "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, script_name)
            )
            if distribution_csv_path is None:
                return self.message_show('CSV??????????????????!!! ')
            jmp_script = JmpScript.factory(
                JmpFile.load_csv_file(distribution_csv_path),
                JmpFactory.scatter(temp_calculation)
            )
            JmpFile.save_with_run_script(jmp_script,
                                         scrip_name="{}/temp_{}.jsl".format(
                                             GlobalVariable.JMP_CACHE_PATH, script_name))

    @Slot()
    def on_action_box_plot_triggered(self, script_name='distribution_box'):
        """ ????????? """
        data = self.get_df_use_to_chart_or_csv()
        if data is None:
            return
        jmp_df, temp_calculation = data
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            distribution_csv_path = self.save_df_to_csv(
                jmp_df, "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, script_name)
            )
            if distribution_csv_path is None:
                return self.message_show('CSV??????????????????!!! ')
            if self.message_show("?????? OR ?????? ? @"):
                jmp_script = JmpScript.factory(
                    JmpFile.load_csv_file(distribution_csv_path),
                    JmpFactory.scatter_line(temp_calculation),
                )
            else:
                jmp_script = JmpScript.factory(
                    JmpFile.load_csv_file(distribution_csv_path),
                    JmpFactory.scatter_box(temp_calculation),
                )
            JmpFile.save_with_run_script(jmp_script,
                                         scrip_name="{}/temp_{}.jsl".format(
                                             GlobalVariable.JMP_CACHE_PATH, script_name))

    @Slot()
    def on_action_mapping_triggered(self):
        self.mapping_select_dialog.show()

    @Slot(int)
    def jmp_mapping_init_with_run(self, mapping_type: int):
        """
        Mapping??????????????????
        TODO: ?????????????????????????????????????????????
        """
        data = self.get_df_use_to_chart_or_csv(no_test_id=True)
        if data is None:
            return
        jmp_df, temp_calculation = data
        bin_head = None
        if mapping_type == MappingSelect.SOFT_BIN:
            bin_head = "SOFT_BIN"
        if mapping_type == MappingSelect.HARD_BIN:
            bin_head = "HARD_BIN"
        if bin_head is None:
            return
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            mapping_csv_str = "{}_{}".format("bin_temp", bin_head)
            mapping_csv_path = self.save_df_to_csv(
                jmp_df, "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, mapping_csv_str)
            )
            jmp_script = JmpScript.factory(
                JmpFile.load_csv_file(mapping_csv_path),
                JmpFactory.bin_mapping(temp_calculation, jmp_df=jmp_df, bin_head=bin_head),
            )
            JmpFile.save_with_run_script(
                jmp_script, scrip_name='{}/temp_{}.jsl'.format(GlobalVariable.JMP_CACHE_PATH, mapping_csv_str)
            )
            self.mapping_select_dialog.hide()

    @Slot()
    def on_action_visual_map_triggered(self, script_name='visual_data'):
        """ Visual Map """
        # if GlobalVariable.SAVE_PKL:
        #     mdi = self.mdi()  # type:StdfLoadUi
        #     mdi.li.save_to_obj(script_name)
        data = self.get_df_use_to_chart_or_csv()
        if data is None:
            return
        jmp_df, temp_calculation = data
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            visual_csv_path = self.save_df_to_csv(
                jmp_df, "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, script_name)
            )
            if visual_csv_path is None:
                return self.message_show(f'CSV??????????????????!!! ')
            if self.message_show("?????? OR ????????? \n@????????????????????????????????????, ???????????????Chart????????????"):
                jmp_script = JmpScript.factory(
                    JmpFile.load_csv_file(visual_csv_path),
                    JmpFactory.heatmap_visual_map(temp_calculation, jmp_df=jmp_df),
                )
            else:
                jmp_script = JmpScript.factory(
                    JmpFile.load_csv_file(visual_csv_path),
                    JmpFactory.points_visual_map(temp_calculation, jmp_df=jmp_df),
                )
            JmpFile.save_with_run_script(
                jmp_script, scrip_name='{}/temp_{}.jsl'.format(GlobalVariable.JMP_CACHE_PATH, script_name)
            )

    @Slot()
    def on_action_multiple_chart_triggered(self):
        if self.mdi() is None:
            return
        self.jmp_select_dialog.show()

    @Slot(list)
    def jmp_models_init_with_run(self, item_select: List[int]):
        if not item_select:
            return
        data = self.get_df_use_to_chart_or_csv()
        if data is None:
            return
        jmp_df, temp_calculation = data
        if self.setting.comboBox.currentText() == UiGlobalVariable.PLOT_BACKEND[0]:
            multi_csv_path = self.save_df_to_csv(
                jmp_df, "{}/temp_{}.csv".format(GlobalVariable.JMP_CACHE_PATH, "mult_csv")
            )
            if multi_csv_path is None:
                return self.message_show('CSV??????????????????!!! ')
            jmp_fac_string = [JmpFile.load_csv_file(multi_csv_path)]
            bin_head = ""
            for each in item_select:
                if each == 6:
                    bin_head = "SOFT_BIN"
                if each == 7:
                    bin_head = "HARD_BIN"
                fac_func = getattr(JmpFactory, JmpFactory.item_dict[each])
                fac_jsl_script = fac_func(temp_calculation,
                                          jmp_df=jmp_df,
                                          bin_head=bin_head)
                jmp_fac_string.append(fac_jsl_script)
            jmp_script = JmpScript.factory(*jmp_fac_string)
            JmpFile.save_with_run_script(
                jmp_script, scrip_name='{}/temp_{}.jsl'.format(GlobalVariable.JMP_CACHE_PATH, "multi_csv")
            )

    @Slot()
    def on_action_contact_triggered(self):
        """
        ????????????contact, ???????????????????????????contact????????????????????????, ????????????????????????, ??????????????????????????????, ??????????????????????????????
        ?????? contact summary ??? li
        :return:
        TODO:
            1. ????????????????????????mid, ???mdi_cache???
            2. mdi_cache?????????mdi_count(small int),
            3. ????????????(MdiLoad??????)???name
            4. ????????????????????????tree_load???widget(hide)
        """
        if not self.mdi_cache:
            return self.mdi_space_message_emit("????????????Contact, ????????????Contact??????")
        self.mdi_contact_dialog.insert(self.mdi_cache)
        self.mdi_contact_dialog.show()

    @Slot(pd.DataFrame)
    def mdi_space_data_contact(self, summary: pd.DataFrame):
        """ ???????????????????????????, ???????????????mdi?????????contact????????? """
        self.mdi_count += 1
        merge_mdi = StdfLoadUi(self, space_nm=self.mdi_count, select=False)
        merge_mdi.dock_file_load.hide()
        self.mdi_cache[self.mdi_count] = MdiLoad(
            self.mdi_count, merge_mdi, "STDF??????????????????: {}".format(self.mdi_count)
        )
        """ ???????????? """
        merge_mdi.summary.set_data(summary)
        merge_mdi.tree_load_widget.set_tree()
        self.load_widget_mdi.addSubWindow(merge_mdi)
        merge_mdi.show()

    @Slot(str)
    def mdi_space_message_emit(self, message: str):
        """
        append message
        :param message:
        :return:
        """
        self.statusbar.showMessage("==={}==={}===".format(dt.datetime.now().strftime("%H:%M:%S"), message))

    def delete_mdi(self, count_id):
        mdi = self.mdi_cache.get(count_id, None)
        if mdi is not None:
            del mdi
            del self.mdi_cache[count_id]
            gc.collect()

    @Slot(int)
    def mdi_space_delete(self, count_id: int):
        QTimer.singleShot(100, lambda: self.delete_mdi(count_id))

    def message_show(self, text: str) -> bool:
        res = QMessageBox.question(self, '?????????', text,
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
        if res == QMessageBox.Yes:
            return True
        else:
            return False

    def save_df_to_csv(self, data_object: pd.DataFrame, file_path):
        if data_object is None:
            return self.mdi_space_message_emit('????????? ?????????????????????!!! ')
        if any(data_object):
            data_object.to_csv(file_path, encoding='utf_8_sig', index=False)
            self.mdi_space_message_emit(f'??????????????????,?????????:>>>{file_path},????????????JMP??????')
            return file_path
        else:
            self.mdi_space_message_emit('????????? ?????????????????????!!! ')
            return None


class Application(QApplication):
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        # QApplication.setStyle('fusion')
