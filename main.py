import re
from typing import Any, Tuple, List

SINGLE_DIGIT_X_n_Y_PATTERN = r"^((?P<plot_size>\dx\d)(?P<drop_points>(\(\d,\d\))*))$"


def drop_points_string_to_tuples(drop_points_string: str) -> List[Tuple[int, int]]:
    drop_points_string_coordinates_pairs: List[str] = drop_points_string.replace("(", "").replace(")", " ").split(" ")

    drop_points = []
    for drop_points_string_coordinates_pair in drop_points_string_coordinates_pairs:
        if drop_points_string_coordinates_pair == "":
            continue
        x, y = map(int, drop_points_string_coordinates_pair.split(","))
        drop_points.append((x, y))

    return drop_points


def find_drop_points_out_of_scope(x: int, y: int, drop_points: List[Tuple[int, int]]):
    return list(filter(lambda coord_pair: (coord_pair[0] > x or coord_pair[1] > y), drop_points))


def parse_plot_description(plot_descr: str, pattern: str = SINGLE_DIGIT_X_n_Y_PATTERN) -> Any:
    plot_descr_valid_pattern = re.compile(pattern=pattern)
    plot_descr_matched = plot_descr_valid_pattern.match(plot_descr)
    if not plot_descr_matched:
        print('Expected plot size and drops points coordinates, e.g.: "5x5(1,3)(4,4)"')
        return

    plot_size = plot_descr_matched.group('plot_size')
    plot_x_size, plot_y_size = map(int, plot_size.split('x'))
    if plot_x_size == 0:
        print('plot X-axis size greater than 0 expected')
        return
    if plot_y_size == 0:
        print('plot Y-axis size greater than 0 expected')
        return

    drop_points_string = plot_descr_matched.group('drop_points')
    if not drop_points_string:
        print('Coordinates of at least one drop point expected')
        return
    drop_points: List[Tuple[int, int]] = drop_points_string_to_tuples(drop_points_string)

    drop_points_out_of_scope = find_drop_points_out_of_scope(plot_x_size, plot_y_size, drop_points)
    if drop_points_out_of_scope:
        print(f'Drop point(s) situated out of specified scope: {drop_points_out_of_scope}')
        return

    print(plot_x_size, plot_y_size, drop_points)


if __name__ == '__main__':
    import sys

    plot_description = sys.argv[1]
    parse_plot_description(plot_description)
