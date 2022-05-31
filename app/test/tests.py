import unittest
from app.route_builder import RouteBuilder
from app.exceptions import PlotDescriptionParsingError, UnprocessablePlotError


class TestIt(unittest.TestCase):

    def test_ill_formatted_plot_description_returns_error_msg(self):
        builder = RouteBuilder(plot_description="5x5(1, 2)")
        with self.assertRaises(PlotDescriptionParsingError):
            builder.build_route()

        builder = RouteBuilder(plot_description="5x5 (1,2)")
        with self.assertRaises(PlotDescriptionParsingError):
            builder.build_route()

        builder = RouteBuilder(plot_description="5x5(1,2)")
        route = builder.build_route()
        assert route is not None
        assert 'D' in route

    def test_plot_width_and_height_should_be_both_greater_then_zero(self):
        builder = RouteBuilder(plot_description="5x0(1,2)")
        with self.assertRaises(UnprocessablePlotError):
            builder.build_route()

        builder = RouteBuilder(plot_description="0x5(1,2)")
        with self.assertRaises(UnprocessablePlotError):
            builder.build_route()

    def test_drop_points_should_be_within_the_specified_plot_size(self):
        builder = RouteBuilder(plot_description="3x3(1,4)")
        with self.assertRaises(UnprocessablePlotError):
            builder.build_route()

        builder = RouteBuilder(plot_description="9x8(9,9)")
        with self.assertRaises(UnprocessablePlotError):
            builder.build_route()

        builder = RouteBuilder(plot_description="9x8(9,8)(7,1)(1,1)(0,0)(9,9)")
        with self.assertRaises(UnprocessablePlotError):
            builder.build_route()

    def test_at_least_one_drop_point_expected(self):
        builder = RouteBuilder(plot_description="5x5")
        with self.assertRaises(UnprocessablePlotError):
            builder.build_route()

    def test_duplicates_will_be_ignored_if_flag_is_on(self):
        builder = RouteBuilder(plot_description="5x5(0,0)(0,0)", filter_duplicated_points=True)
        an_extremely_short_root = builder.build_route()
        assert an_extremely_short_root != 'DD'
        assert an_extremely_short_root == 'D'

    def test_route_built_correctly(self):
        plot_descr_vs_expected_route = {
            "5x5(1,3)(4,4)": "ENNNDEEEND",
            "3x3(1,1)(3,3)": "ENDEENND",
            "4x4(4,4)": "EEEENNNND",
            "5x5(0,0)(0,0)(0,0)": "DDD",
            "5x5(0,0)(1,3)(4,4)(4,2)(4,2)(0,1)(3,2)(2,3)(4,1)": "DNDENNDEDEDEDNDDNND"
        }

        for plot_descr, expected_route in plot_descr_vs_expected_route.items():
            builder = RouteBuilder(plot_description=plot_descr)
            route = builder.build_route()
            assert route == expected_route
