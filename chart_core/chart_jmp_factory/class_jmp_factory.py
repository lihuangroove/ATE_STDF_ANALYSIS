#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : class_jmp_factory.py
@Author  : Link
@Time    : 2022/10/7 10:51
@Mark    : 调用并运行的地方
"""
import pandas as pd

from chart_core.chart_jmp.jmp_box import JmpBox
from chart_core.chart_jmp_factory.class_jmp_distribution import JmpDistribution
from chart_core.chart_jmp_factory.class_jmp_graph_builder import JmpGraphBuilder
from ui_component.ui_app_variable import UiGlobalVariable


class NewJmpFactory:

    @staticmethod
    def get_df_map_coord(jmp_df: pd.DataFrame) -> tuple:
        y_max = jmp_df["Y_COORD"].max()
        y_min = jmp_df["Y_COORD"].min() - 1
        x_max = jmp_df["X_COORD"].max()
        x_min = jmp_df["X_COORD"].min()
        percent = (y_max - y_min) / (x_max - x_min)
        return x_min, x_max, y_min, y_max, percent

    @staticmethod
    def get_jmp_lsl_usl(cpk_info: dict, is_dis: bool = False) -> dict:
        l_limit = cpk_info["LO_LIMIT"]
        h_limit = cpk_info["HI_LIMIT"]
        if UiGlobalVariable.JmpScreen == 0:
            l_limit = cpk_info["LO_LIMIT"]
            if isinstance(cpk_info["LO_LIMIT_TYPE"], float):
                l_limit = cpk_info["MIN"]
            h_limit = cpk_info["HI_LIMIT"]
            if isinstance(cpk_info["HI_LIMIT_TYPE"], float):
                h_limit = cpk_info["MAX"]
        if UiGlobalVariable.JmpScreen == 1:
            l_limit = cpk_info["MIN"]
            h_limit = cpk_info["MAX"]
        if UiGlobalVariable.JmpScreen == 2:
            l_limit = cpk_info["ALL_DATA_MIN"]
            h_limit = cpk_info["ALL_DATA_MAX"]
        if UiGlobalVariable.JmpScreen == 3:
            rig_x = cpk_info["STD"] * UiGlobalVariable.JmpMeanAddSubSigma
            l_limit = cpk_info["AVG"] - rig_x
            h_limit = cpk_info["AVG"] + rig_x
        step_nm = abs(h_limit - l_limit) / UiGlobalVariable.JmpBins
        if step_nm <= 0:
            step_nm = h_limit / 20
        if l_limit == h_limit:
            l_limit = l_limit - 1
            h_limit = h_limit + 1
        if not is_dis:
            return {
                "l_limit": format(l_limit, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
                "h_limit": format(h_limit, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
                "step_nm": format(step_nm, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
            }
        return {
            "decimal": UiGlobalVariable.JmpPlotFloatRound,
            "min": format(l_limit - 8 * step_nm, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
            "max": format(h_limit + 8 * step_nm, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
            "l_limit": format(l_limit, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
            "h_limit": format(h_limit, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
            "inc": format(step_nm, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
            "t_inc": format(step_nm * 2, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
            "avg": format(cpk_info["AVG"], '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
        }

    @staticmethod
    def jmp_distribution(capability: dict, title: str = "dis_bar") -> str:
        """
        :param:

            jmp_limit: limit namedtuple
            jmp_cpk: li.cpk_dict 中取出
            title:str
            ...
        :return:
        """
        jmp_dis = JmpDistribution()
        """ 要修改一些全局参数可以在set_config这里修改 """
        jmp_dis.set_config(
            "Stack( 1 )",
            "By(  )",
            "Automatic Recalc( 1 )",
            "Arrange in Rows( {col} )".format(col=UiGlobalVariable.JmpPlotColumn)
        )

        for key, row in capability.items():
            # new_continuous_distribution
            column = "Column( :\"{}\"  )".format(key)
            hor = "Horizontal Layout( 1 )"
            ver = "Vertical( 0 ), Outlier Box Plot( {} )".format(1 if UiGlobalVariable.JmpDisPlotBox else 0)
            cap_ans = ""
            if not UiGlobalVariable.JmpNoLimit:
                cap_ans = "Capability Analysis( LSL( {l_limit} ), USL( {h_limit} ) )".format(
                    **NewJmpFactory.get_jmp_lsl_usl(row)
                )
            jmp_dis.new_continuous_distribution(column, hor, ver, cap_ans)

            # new_dispatch
            dis_limit_box = ""
            if not UiGlobalVariable.JmpNoLimit:
                jmp_lsl_usl = NewJmpFactory.get_jmp_lsl_usl(row, is_dis=True)
                dis_limit_box = """
            Dispatch( {{:"{column}"}} , "1", ScaleBox, 
            {{Min( {min} ), Max( {max} ), Inc( {t_inc} ), Minor Ticks( 1 )}})
                """.format(
                    column=key,
                    **jmp_lsl_usl
                )
            cap_ans_number_box_collapse = """
            Dispatch({{ :"{column}",  "Capability Analysis"}},"Portion",StringColBox,{{Visibility( "Collapse" )}})
            """.format(
                column=key
            )
            cap_ans_string_box_collapse = """
            Dispatch({{ :"{column}",  "Capability Analysis"}},"% Actual",NumberColBox,{{Visibility( "Collapse" )}})
            """.format(
                column=key
            )
            outline_box_close = ""
            if not UiGlobalVariable.JmpDisPlotSigma:
                outline_box_close = """
            Dispatch({{ :"{column}",  "Capability Analysis"}}, "长期 Sigma", OutlineBox, {{ Close( 1 ) }})
                """.format(
                    column=key
                )

            jmp_dis.new_dispatch(dis_limit_box, cap_ans_number_box_collapse, cap_ans_string_box_collapse,
                                 outline_box_close)

        jmp_dis.new_dispatch("""
            Dispatch( , "Distributions", OutlineBox, {{Set Title( "{}" )}} )
        """.format(title))

        return jmp_dis.execute()

    @staticmethod
    def jmp_distribution_trans_bar(capability: dict, title: str = "trans_bar") -> str:
        jmp_plots = []
        for key, row in capability.items():
            jmp_dis = JmpGraphBuilder()
            jmp_dis.set_config(
                """
            Size( 1085, 320 ),
            Show Control Panel( 0 ),
            Legend Position( "Inside Right" ),
            Variables( Group X( :"GROUP" ), Overlay( :GROUP ), X( :"DA_GROUP" ), Y( :"{column}" ) ),
            Elements( Histogram( X, Y, Legend( 5 ) ) )
                """.format(column=key)
            )
            jmp_dis.new_dispatch(
                """
            Dispatch(
            ,
            "{column}",
            ScaleBox,
            {{
            Format( "Fixed Dec", 12, {decimal} ), Min( {min} ), Max( {max} ), Inc( {inc} ), Minor Ticks( 0 ), 
            Add Ref Line( {l_limit}, "Solid", "Medium Dark Red", "下限值({l_limit})", 1), 
            Add Ref Line( {h_limit}, "Solid", "Dark Red", "上限值({h_limit})", 1 ), 
            Add Ref Line( {avg}, "Solid", "Medium Dark Blue", "良品均值({avg})", 1)
            }}
            )
                """.format(
                    column=key,
                    **NewJmpFactory.get_jmp_lsl_usl(row, is_dis=True)
                )
            )
            jmp_plots.append(jmp_dis.execute())
        jmp_script = JmpBox.new_window(JmpBox.new_outline_box(*JmpBox.new_group_item(
            *jmp_plots, col=UiGlobalVariable.JmpPlotColumn
        ), title=title))
        return jmp_script
