"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/3/28 19:28
@Software: PyCharm
@File    : jmp_fit.py
@Remark  : 
"""
from ui_component.ui_app_variable import UiGlobalVariable


class JmpFit:

    @staticmethod
    def fit_group(*one_ways: str, col=2) -> str:
        ",".join(one_ways) + "\n,    "
        return """
        Fit Group(
            {one_ways}
            ,<<{{Arrange in Rows( {col} )}}
        );
        """.format(one_ways=",".join(one_ways), col=col)

    @staticmethod
    def one_way(arg: dict, send_to_report: str) -> str:
        test_text = str(arg["TEST_NUM"]) + ":" + arg["TEST_TXT"]
        return """
        Oneway(
        Y( :Name( "{test_text}" ) ),
        X( :"ALL_GROUP" ),
        All Graphs( 0 ),
        Means and Std Dev( 1 ),
        Compare Densities( 1 ),
        Mean Error Bars( 1 ),
        Std Dev Lines( 1 ),
        Histograms( 1 ),
            {send_to_report}
        )
        """.format(test_text=test_text, send_to_report=send_to_report)

    @staticmethod
    def limit_color_dis(cpk_info: dict) -> str:
        if UiGlobalVariable.JmpNoLimit:
            return ""
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
            step_nm = l_limit / 5
        min_jmp = l_limit - step_nm
        max_jmp = h_limit + step_nm
        return """
        Dispatch(
            {{"Compare Densities"}},
            "1",
            ScaleBox,
            {{Min( {min_jmp} ), Max( {max_jmp} ), Inc( {inc} ), Minor Ticks( 1 ),
            Add Ref Line( {{{l_limit}, {h_limit}}}, "Solid", "Dark Blue", "", 1, 0.25 )}}
        )
        """.format(min_jmp=min_jmp, max_jmp=max_jmp, inc=step_nm,
                   l_limit=format(l_limit, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
                   h_limit=format(h_limit, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)))

    @staticmethod
    def fill_color_dis() -> str:
        return """
        Dispatch(
            {},
            "222",
            ScaleBox,
            {Legend Model(
                1,
                Properties( 0, {Line Color( -14948892 ), Fill Color( -14948892 )} ),
                Properties( 1, {Line Color( -3636920 ), Fill Color( -3636920 )} ),
                Properties( 2, {Line Color( -5091146 ), Fill Color( -5091146 )} ),
                Properties( 3, {Line Color( -9981603 ), Fill Color( -9981603 )} ),
                Properties( 4, {Line Color( -16744192 ), Fill Color( -16744192 )} ),
                Properties( 5, {Line Color( -10901032 ), Fill Color( -10901032 )} ),
                Properties( 6, {Line Color( -16220607 ), Fill Color( -16220607 )} ),
                Properties( 7, {Line Color( -9282864 ), Fill Color( -9282864 )} ),
                Properties( 8, {Line Color( -6995852 ), Fill Color( -6995852 )} ),
                Properties( 9, {Line Color( -1524612 ), Fill Color( -1524612 )} ),
                Properties( 10, {Line Color( -9458080 ), Fill Color( -9458080 )} ),
                Properties( 11, {Line Color( -14452073 ), Fill Color( -14452073 )} ),
                Properties( 12, {Line Color( -6391856 ), Fill Color( -6391856 )} ),
                Properties( 13, {Line Color( -2745505 ), Fill Color( -2745505 )} ),
                Properties( 14, {Line Color( -10199751 ), Fill Color( -10199751 )} ),
                Properties( 15, {Line Color( -7150697 ), Fill Color( -7150697 )} )
            )}
        )
        """
