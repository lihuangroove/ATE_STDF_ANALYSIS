"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/12/23 16:59
@Site    : 
@File    : mixin.py
@Software: PyCharm
@Remark  : 
"""

from dataclasses import dataclass
from enum import Enum

import numpy as np
from pyqtgraph import PlotWidget, InfiniteLine

from common.li import Li
from ui_component.ui_app_variable import UiGlobalVariable


class ChartType(Enum):
    BinMap = 0x10
    BinPareto = 0x11
    TransBar = 0x20
    TransScatter = 0x30
    VisualMap = 0x40


@dataclass
class RangeData:
    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0


def GraphRangeSignal(func):
    """
    这个是为了防止信号误触发
    :param func:
    :return:
    """

    def wrapper(ctx, *args, **kwargs):
        try:
            ctx.pw.sigRangeChanged.disconnect()
        except RuntimeError:
            pass
        if ctx.p_range is None:
            ctx.p_range = RangeData()
        res = func(ctx, *args, **kwargs)
        ctx.p_range.x_min, ctx.p_range.x_max = ctx.bottom_axis.range
        ctx.p_range.y_min, ctx.p_range.y_max = ctx.left_axis.range
        ctx.pw.sigRangeChanged.connect(ctx.set_range_data_to_chart)
        return res

    return wrapper


class BasePlot:
    """
        TODO: rota: 0b000000
            0bX_____ -> select x  选取后筛选X轴的数据
            0b_X____ -> select y  选取后筛选Y轴的数据
            0b__X___ -> lint x    H_L_Limit/AVG 放在X轴 -> 主要数据分布在X上
            0b___X__ -> lint y    H_L_Limit/AVG 放在Y轴 -> 主要数据分布在Y上
            0b____X_ -> zoom x    X轴放大缩小
            0b_____X -> zoom y    Y轴放大缩小
    """
    pw: PlotWidget = None
    rota: int = None
    li: Li = None
    p_range: RangeData = None
    line_init: bool = False

    key: int = None  # 显示的测试项目
    lines: dict = None
    unit: str = ''

    sig: int = 0  # 方向
    change: bool = False  # 是否已经绘图了

    def set_data(self, key: int):
        """
        :param key: TEST_ID
        :return:
        """
        if self.li is None:
            raise Exception("first set li")
        row = self.li.capability_key_dict.get(key, None)
        if row is None:
            return
        self.key = key
        title = str(row["TEST_NUM"]) + ":" + row["TEST_TXT"]
        self.set_title(title)
        if self.p_range is None:
            self.p_range = RangeData()

    def set_title(self, title: str = "PlotItem with CustomAxisItem, CustomViewBox"):
        self.pw.plotItem.setTitle(title)

    def resize(self, w, h):
        self.pw.resize(w, h)

    def widget(self, width: int):
        self.pw.setMaximumWidth(width)
        return self.pw

    @GraphRangeSignal
    def pw_show(self):
        """
        graph_range_signal的意义在于不要触发因为坐标改变导致的信号循环
        :return:
        """
        self.pw.show()

    def set_lines(self, **kwargs):
        """
        line可以缓存
        """
        if self.lines is None:
            self.lines = {}
        for key, item in kwargs.items():
            if key in self.lines:
                inf = self.lines[key]  # type:InfiniteLine
                inf.setPos(item)
            else:
                ang = 0 if self.sig else 90
                inf = InfiniteLine(
                    movable=False, angle=ang, pen=(255, 0, 0), hoverPen=(0, 200, 0),
                    label=key + '={value:0.' + str(UiGlobalVariable.GraphPlotFloatRound) + 'f}' + self.unit,
                    labelOpts={'color': (255, 0, 0), 'movable': True, 'fill': (0, 0, 200, 100), 'position': 0.1, }
                )
                inf.setPos(item)
                self.pw.addItem(inf)

    def set_range_data_to_chart(self, a, ax) -> bool:
        if self.li is None:
            return False
        if self.sig == 1:  # 0 是 X, 1 是Y 的变化
            data_min, data_max = self.p_range.y_min, self.p_range.y_max
        else:
            data_min, data_max = self.p_range.x_min, self.p_range.x_max
        percent = (ax[self.sig][1] - ax[self.sig][0]) / (data_max - data_min)
        if 0.85 < percent < 1.15:
            """ 性能会好些,体验会差点 """
            return False
        self.set_p_range(ax[self.sig][0], ax[self.sig][1])
        return True

    def set_line_self(self):
        row = self.li.capability_key_dict.get(self.key, None)
        if row is None: return
        self.unit = row["UNITS"] if not isinstance(row["UNITS"], float) else ""
        if UiGlobalVariable.GraphScreen == 0:
            l_limit = row["LO_LIMIT"]
            if isinstance(row["LO_LIMIT_TYPE"], float):
                l_limit = row["MIN"]
            h_limit = row["HI_LIMIT"]
            if isinstance(row["HI_LIMIT_TYPE"], float):
                h_limit = row["MAX"]
            self.set_lines(
                HI_LIMIT=h_limit,
                LO_LIMIT=l_limit,
                AVG=row["AVG"],
            )
            return
        if UiGlobalVariable.GraphScreen == 1:
            l_limit = row["MIN"]
            h_limit = row["MAX"]
            self.set_lines(
                VAILD_MAX=h_limit,
                VAILD_MIN=l_limit,
                AVG=row["AVG"],
            )
            return
        if UiGlobalVariable.GraphScreen == 2:
            l_limit = row["ALL_DATA_MIN"]
            h_limit = row["ALL_DATA_MAX"]
            self.set_lines(
                DATA_MIN=h_limit,
                DATA_MAX=l_limit,
                AVG=row["AVG"],
            )
            return
        if UiGlobalVariable.GraphScreen == 3:
            if row["STD"] == 0 or np.isnan(row["STD"]):
                l_limit, h_limit = -0.1, 1.1
            else:
                rig_x = row["STD"] * UiGlobalVariable.GraphMeanAddSubSigma
                l_limit = row["AVG"] - rig_x
                h_limit = row["AVG"] + rig_x
            self.set_lines(
                SIGMA_MIN=h_limit,
                SIGMA_MAX=l_limit,
                AVG=row["AVG"],
            )
            return

    # @GraphRangeSignal
    def set_range_self(self):
        """
        显示
        :return:
        """
        row = self.li.capability_key_dict.get(self.key, None)
        if row is None: return
        if UiGlobalVariable.GraphScreen == 0:
            l_limit = row["LO_LIMIT"]
            if isinstance(row["LO_LIMIT_TYPE"], float):
                l_limit = row["MIN"]
            h_limit = row["HI_LIMIT"]
            if isinstance(row["HI_LIMIT_TYPE"], float):
                h_limit = row["MAX"]
            step = row["STD"] * 2
            self.set_p_range(l_limit - step, h_limit + step)
            return
        if UiGlobalVariable.GraphScreen == 1:
            self.set_p_range(row["MIN"], row["MAX"])
            return
        if UiGlobalVariable.GraphScreen == 2:
            low = self.li.to_chart_csv_data.df[self.key].min()
            high = self.li.to_chart_csv_data.df[self.key].max()
            self.set_p_range(low, high)
            return
        if UiGlobalVariable.GraphScreen == 3:
            if row["STD"] == 0 or np.isnan(row["STD"]):
                l_limit, h_limit = -0.1, 1.1
            else:
                step = row["STD"] * self.li.rig
                l_limit, h_limit = row["AVG"] - step, row["AVG"] + step
            self.set_p_range(l_limit, h_limit)
            return

    def set_p_range(self, p_min, p_max):
        if self.sig == 1:
            self.p_range.y_min, self.p_range.y_max = p_min, p_max
        else:
            self.p_range.x_min, self.p_range.x_max = p_min, p_max

    def set_front_chart(self):
        pass

    def __del__(self):
        print("chart delete")
        try:
            self.li.QChartSelect.disconnect(self.set_front_chart)
        except RuntimeError:
            pass
        try:
            self.li.QChartRefresh.disconnect(self.set_front_chart)
        except RuntimeError:
            pass
