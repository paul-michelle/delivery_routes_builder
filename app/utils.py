from collections import Counter
from typing import Tuple, List, Optional

Point: Tuple[int, int]


def drop_points_string_to_tuples(drop_points_string: str) -> List['Point']:
    drop_points_string_coordinates_pairs: List[str] = drop_points_string.replace("(", "").replace(")", " ").split(
        " ")

    drop_points = []
    for drop_points_string_coordinates_pair in drop_points_string_coordinates_pairs:
        if drop_points_string_coordinates_pair == "":
            continue
        x, y = map(int, drop_points_string_coordinates_pair.split(","))
        drop_points.append((x, y))

    return drop_points


def find_drop_points_out_of_scope(x: int, y: int, points: List['Point']) -> List[Optional['Point']]:
    return list(filter(lambda coord_pair: (coord_pair[0] > x or coord_pair[1] > y), points))


def find_duplicated_drop_points(drop_points: List['Point']) -> Tuple[List[Optional['Point']], List['Point']]:
    duplicates = []
    unique_drop_points = list(set(drop_points))

    if len(unique_drop_points) < len(drop_points):
        duplicates = list((Counter(drop_points) - Counter(unique_drop_points)).elements())

    return duplicates, unique_drop_points
