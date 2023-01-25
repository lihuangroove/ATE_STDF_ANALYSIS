"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/4/15 14:48
@Software: PyCharm
@File    : console_ui.py
@Remark  :
"""
import re
import sys
import pyqtgraph.console
from PySide2.QtCore import Slot
from pyqtgraph.console import template_pyside2
from PySide2.QtWidgets import QApplication, QMainWindow, QPlainTextEdit
from pyqtgraph.dockarea import DockArea, Dock

from ui_component.ui_common.syntax_highlighting import PythonHighlighter
from ui_component.ui_common.ui_designer.ui_console import Ui_MainWindow


class LiConsole(pyqtgraph.console.ConsoleWidget):
    def runCmd(self, cmd):
        # cmd = str(self.input.lastCmd)

        orig_stdout = sys.stdout
        orig_stderr = sys.stderr
        encCmd = re.sub(r'>', '&gt;', re.sub(r'<', '&lt;', cmd))
        encCmd = re.sub(r' ', '&nbsp;', encCmd)
        encCmd = re.sub(r'\n', '<br>', encCmd)

        self.ui.historyList.addItem(cmd)
        self.saveHistory(self.input.history[1:100])

        try:
            sys.stdout = self
            sys.stderr = self
            if self.multiline is not None:
                self.write("<br><b>%s</b>\n" % encCmd, html=True, scrollToBottom=True)
                self.execMulti(cmd)
            else:
                self.write("<br><div style='background-color: #CCF; color: black'><b>%s</b>\n" % encCmd, html=True,
                           scrollToBottom=True)
                self.inCmd = True
                self.execSingle(cmd)

            if not self.inCmd:
                self.write("</div>\n", html=True, scrollToBottom=True)

        finally:
            sys.stdout = orig_stdout
            sys.stderr = orig_stderr

            sb = self.ui.historyList.verticalScrollBar()
            sb.setValue(sb.maximum())


class ConsoleWidget(QMainWindow, Ui_MainWindow):
    console_win = None
    field_code_input = None
    syntax_highlight = None

    def __init__(self, parent=None, icon=None, namespace=None, text=None):
        super(ConsoleWidget, self).__init__(parent)
        self.setupUi(self)
        self.area = DockArea()
        self.setCentralWidget(self.area)
        self.init_text_edit()
        self.init_console(namespace, text)
        self.setWindowTitle("利用pandas|numpy分析数据")
        if icon:
            self.setWindowIcon(icon)

    def init_text_edit(self):
        self.field_code_input = QPlainTextEdit(self)
        dock_text_edit = Dock("Code Text Edit", size=(100, 700))
        dock_text_edit.addWidget(self.field_code_input)
        self.area.addDock(dock_text_edit, "right")
        self.field_code_input.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.field_code_input.setTabStopWidth(20)
        self.field_code_input.setObjectName("field_code_input")
        # TODO: 加入可以从文件读取的方法
        self.field_code_input.setPlainText("""
'''
# TODO: 待加入可以从文件读取的方法
# TODO: 待更新, 可以在这里写一些语法来操作li
'''
        """)
        self.syntax_highlight = PythonHighlighter(self.field_code_input.document())

    def init_console(self, namespace, text):
        self.console_win = LiConsole(namespace=namespace, text=text)
        dock_console_win = Dock("Code Text Edit", size=(200, 700))
        dock_console_win.addWidget(self.console_win)
        self.area.addDock(dock_console_win, "left")

    @Slot()
    def on_action_select_run_triggered(self):
        cmd = self.field_code_input.textCursor().selection().toPlainText()
        self.console_win.runCmd(cmd)

    @Slot()
    def on_action_run_all_triggered(self):
        cmd = self.field_code_input.toPlainText()
        self.console_win.runCmd(cmd)

    @Slot()
    def on_action_refresh_triggered(self):
        cmd = 'li.update();li.refresh_chart()'
        self.console_win.runCmd(cmd)
