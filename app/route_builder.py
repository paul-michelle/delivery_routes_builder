import re
from typing import List, Optional, Tuple

from . import utils
from . import exceptions

SINGLE_DIGIT_X_AND_Y_PATTERN = r"^((?P<plot_size>\dx\d)(?P<drop_points>(\(\d,\d\))*))$"

Point: Tuple[int, int]

WEST = 'W'
EAST = 'E'
NORTH = 'N'
SOUTH = 'S'
DROP = 'D'


class RouteBuilder:

    def __init__(self, plot_description: str, starting_point: 'Point' = (0, 0), filter_duplicated_points: bool = False):
        self._plot_description = plot_description
        self._starting_point = starting_point
        self._filter_duplicated_points = filter_duplicated_points

    def parse_and_validate_plot_description(self) -> List['Point']:
        plot_descr_valid_pattern = re.compile(pattern=SINGLE_DIGIT_X_AND_Y_PATTERN)
        plot_descr_matched = plot_descr_valid_pattern.match(self._plot_description)
        if not plot_descr_matched:
            raise exceptions.PlotDescriptionParsingError(
                'Expected plot size and drops points coordinates, e.g.: "5x5(1,3)(4,4)"'
            )

        plot_size = plot_descr_matched.group('plot_size')
        plot_x_size, plot_y_size = map(int, plot_size.split('x'))
        if plot_x_size == 0:
            raise exceptions.UnprocessablePlotError('Plot X-axis size greater than 0 expected')

        if plot_y_size == 0:
            raise exceptions.UnprocessablePlotError('Plot Y-axis size greater than 0 expected')

        drop_points_string = plot_descr_matched.group('drop_points')
        if not drop_points_string:
            raise exceptions.UnprocessablePlotError('Coordinates of at least one drop point expected')

        drop_points: List[Tuple[int, int]] = utils.drop_points_string_to_tuples(drop_points_string)

        drop_points_out_of_scope = utils.find_drop_points_out_of_scope(plot_x_size, plot_y_size, drop_points)
        if drop_points_out_of_scope:
            raise exceptions.UnprocessablePlotError(
                f'Drop point(s) situated out of specified scope: {drop_points_out_of_scope}'
            )

        if self._filter_duplicated_points:
            duplicated_drop_points, unique_drop_points = utils.find_duplicated_drop_points(drop_points)
            if duplicated_drop_points:
                print(
                    f"Warning: duplicates of drop point(s) found: {duplicated_drop_points}. Those won't be considered.")
            return unique_drop_points

        return drop_points

    def build_route(self) -> str:
        drop_points = self.parse_and_validate_plot_description()

        route = ''
        move_from = self._starting_point
        drop_points_sorted_asc = sorted(drop_points, key=lambda point: (point[0], point[1]))

        for next_drop_point in drop_points_sorted_asc:
            shift_along_x_axis = next_drop_point[0] - move_from[0]
            route += shift_along_x_axis * (EAST if shift_along_x_axis > 0 else WEST)

            shift_along_y_axis = next_drop_point[1] - move_from[1]
            route += shift_along_y_axis * (NORTH if shift_along_y_axis > 0 else SOUTH)

            route += DROP
            move_from = next_drop_point

        return route
