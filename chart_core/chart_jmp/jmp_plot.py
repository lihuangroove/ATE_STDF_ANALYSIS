"""
-*- coding: utf-8 -*-
@Author  : Link
@Time    : 2022/3/29 11:04
@Software: PyCharm
@File    : jmp_plot.py
@Remark  : 
"""
from ui_component.ui_app_variable import UiGlobalVariable


class JmpPlot:
    """
    图形生成器
    Graph Builder
    """

    @staticmethod
    def line_fit(x: str, y: str, group: bool = True):
        """

        """
        return f"""
        Graph Builder(
            Show Control Panel( 0 ),
            Variables( X( :"{x}" ), Y( :"{y}" ),  {'Wrap( :"GROUP" )' if group else ''} ),
            Elements( Points( X, Y, Legend( 5 ) ), Line Of Fit( X, Y, Legend( 6 ) , 
            Confidence of Prediction( 1 ), Equation( 1 )), F Test( 1 ) ),
        );
        """

    @staticmethod
    def bin_mapping(column: str, bin_length: int, send_to_report: str):
        """ 要再group条件下启动 """
        return """
        Graph Builder(
            Size( 650, 660 ),
            Show Control Panel( 0 ),
            Variables( X( :X_COORD ), Y( :Y_COORD ), Overlay( :"{column}", Levels( {bin_length} ) ), Wrap( :GROUP ) ),
            Elements( Points( X, Y, Legend( 31 ) ) ),
            {send_to_report}
        );
        """.format(column=column, bin_length=bin_length, send_to_report=send_to_report)

    @staticmethod
    def bin_scale_dis(bins: list, mi: int, ma: int):
        # mark_size = math.ceil(250 / (ma - mi))
        properties = ""
        # for index, each in enumerate(bins):
        #     properties += """
        #     Properties(
        #         %s,
        #         {Marker( "FilledSquare" )},
        #         Item ID( "%s", 1 )
        #     ),
        #     """ % (index, each)  # , Marker Size( %s )
        return """
        Dispatch(
            ,
            "X_COORD",
            ScaleBox,
            {{Inc( 1 ), Minor Ticks( 0 ), Label Row( Show Major Grid( 1 ) )}}
        ),
        Dispatch(
            ,
            "Y_COORD",
            ScaleBox,
            {{Min( {ma} ), Max( {mi} ), Inc( 1 ), Minor Ticks( 0 ), Label Row( Show Major Grid( 1 ) )}}
        ),
        Dispatch(
            ,
            "400",
            ScaleBox,
            {{Legend Model(
                31, 
                {properties}
            )}}
        )
        """.format(properties=properties, ma=ma, mi=mi)

    @staticmethod
    def trans_distribution(arg: dict, send_to_report: str) -> str:
        return """
        Graph Builder(
            Size( 1085, 320 ),
            Show Control Panel( 0 ),
            Legend Position( "Inside Right" ),
            Variables( Group X( :"GROUP" ), Overlay( :GROUP ), X( :"DA_GROUP" ), Y( :"{test_text}" ) ),
            Elements( Histogram( X, Y, Legend( 5 ) ) ),
            
            {send_to_report}
        )
        """.format(test_text=arg["TEXT"], send_to_report=send_to_report)

    @staticmethod
    def trans_box(arg: dict, send_to_report: str) -> str:
        return """
        Graph Builder(
            Size( 1085, 320 ),
            Show Control Panel( 0 ),
            Legend Position( "Inside Right" ),
            Variables( Group X( :"GROUP" ), Color( :GROUP ), X( :"DA_GROUP" ), Y( :"{test_text}" ) ),
            Elements( Box Plot( X, Y, Legend( 5 ) ) ),

            {send_to_report}
        )
        """.format(test_text=arg["TEXT"], send_to_report=send_to_report)

    @staticmethod
    def trans_box_point(arg: dict, send_to_report: str) -> str:
        return """
        Graph Builder(
            Size( 1085, 320 ),
            Show Control Panel( 0 ),
            Legend Position( "Inside Right" ),
            Variables( Group X( :"GROUP" ), Color( :GROUP ), X( :"DA_GROUP" ), Y( :"{test_text}" ) ),
            Elements( Points( X, Y, Legend( 5 ) , Jitter( "Random Uniform" ) ) ),

            {send_to_report}
        )
        """.format(test_text=arg["TEXT"], send_to_report=send_to_report)

    @staticmethod
    def trans_scatter(arg: dict, send_to_report: str) -> str:
        return """
        Graph Builder(
            Size( 1085, 380 ),
            Show Control Panel( 0 ),
            Legend Position( "Inside Right" ),
            Variables( Group X( :"GROUP" ), X( :"PART_ID" ), Y( :"{test_text}" ), Overlay( :"DA_GROUP" ) ),
            Elements( Points( X, Y, Legend( 11 ) ), ),
            {send_to_report}
        )
        """.format(test_text=arg["TEXT"], send_to_report=send_to_report)

    @staticmethod
    def trans_scale_dis(cpk_info: dict) -> str:
        decimal = UiGlobalVariable.JmpPlotFloatRound
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
        avg = cpk_info["AVG"]
        displace = (h_limit - l_limit) / 4
        if displace <= 0:
            displace = h_limit / 5
        inc = (h_limit - l_limit) / UiGlobalVariable.JmpBins
        if l_limit == h_limit:
            l_limit = l_limit - 1
            h_limit = h_limit + 1
        return """
        Dispatch(
                ,
                "{test_text}",
                ScaleBox,
                {{Format( "Fixed Dec", 12, {decimal} ), Min( {mIn} ), Max( {mAx} ), Inc( {iNc} ), Minor Ticks( 0 ), 
                Add Ref Line({l_limit}, "Solid", "Medium Dark Red", "下限值({l_limit})", 1), 
                Add Ref Line( {h_limit}, "Solid", "Dark Red", "上限值({h_limit})", 1 ), 
                Add Ref Line( {avg}, "Solid", "Medium Dark Blue", "良品均值({avg})", 1)
                    }}
            )
        """.format(test_text=cpk_info["TEXT"], decimal=decimal,
                   mIn=format(l_limit - displace, '.{}f'.format(decimal)),
                   mAx=format(h_limit + displace, '.{}f'.format(decimal)),
                   l_limit=format(l_limit, '.{}f'.format(decimal)),
                   h_limit=format(h_limit, '.{}f'.format(decimal)),
                   avg=format(avg, '.{}f'.format(decimal)),
                   iNc=format(inc, '.{}f'.format(decimal)))

    @staticmethod
    def trans_visual_points(arg: dict, group: bool, send_to_report: str, percent: float) -> str:
        """
        TODO: Elements( Points( X, Y, Legend( 5 ) ) ) 散点
        TODO: Elements( Contour( X, Y, Legend( 5 ) ) ) 等高线
        """
        y = int(650 * percent * 0.6) + 10
        return """
        Graph Builder(
            // Size( 650, {0} ),
            Size( 570, 580 ),
            Show Control Panel( 0 ),
            Variables( X( :X_COORD ), Y( :Y_COORD ), Color( :"{1}" ), {2}),
            Elements( Points( X, Y, Legend( 5 ) ) ),

            {send_to_report}
        )
        """.format(y, arg["TEXT"], " Wrap( :GROUP ) " if group else "", send_to_report=send_to_report)

    @staticmethod
    def trans_visual_heatmap(arg: dict, group: bool, send_to_report: str, percent: float) -> str:
        """
        TODO: Elements( Points( X, Y, Legend( 5 ) ) ) 散点
        TODO: Elements( Contour( X, Y, Legend( 5 ) ) ) 等高线
        """
        y = int(650 * percent * 0.6) + 10
        return """
        Graph Builder(
            Size( 570, 580 ),
            Show Control Panel( 0 ),
            Variables( X( :X_COORD ), Y( :Y_COORD ), Color( :"{1}" ), {2}),
            Elements( Heatmap( X, Y, Legend( 5 ) ) ),

            {send_to_report}
        )
        """.format(y, arg["TEXT"], " Wrap( :GROUP ) " if group else "", send_to_report=send_to_report)

    @staticmethod
    def visual_dis(arg, y_max, y_min, mark_size=10) -> str:
        # mark_pro = """
        #     Properties(
        #         1,
        #         {Marker( "FilledSquare" )},
        #         )
        #     """  # .format(mark_size=mark_size) # , Marker Size( {mark_size} )
        return """
            Dispatch(
                ,
                "Graph Builder",
                OutlineBox,
                {{Set Title( "{test_text}" ), Image Export Display( 正常 )}}
            ),
            Dispatch(
                ,
                "X_COORD",
                ScaleBox,
                {{ Inc( 1 ), Minor Ticks( 0 ), Label Row( Show Major Grid( 1 ) )}}
            ),
            Dispatch(
                ,
                "Y_COORD",
                ScaleBox,
                {{ Min( {y_max} ), Max( {y_min} ), Inc( 1 ), Minor Ticks( 0 ), Label Row( Show Major Grid( 1 ) )}}
            ),
            Dispatch(
                , "400", ScaleBox, 
                {{
                Legend Model(
                    5, 
                        Properties( 
                        0, {{gradient( {{Range Type( "Middle 90%" ), Label Format( "Fixed Dec", 12, 5 )}} )}}, 
                        Item ID( "{test_text}", 1 )
                        )
                        , {mark_pro}
                    )
                }}
            )
            """.format(test_text=arg["TEXT"],
                       y_max=format(y_max, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
                       y_min=format(y_min, '.{}f'.format(UiGlobalVariable.JmpPlotFloatRound)),
                       mark_pro="")

    @staticmethod
    def variability_chart(args):
        """
        变异性分析
        """
        return """
        
        """

    @staticmethod
    def variability_chart_line_dis():
        """
        在scale box上添加有的没得
        """
