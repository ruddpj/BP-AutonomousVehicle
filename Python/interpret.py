from typing import Any

import numpy as np
from numpy import floating


def find_left_right_lines(lines: np.ndarray) -> tuple[list[floating[Any]], list[floating[Any]]]:
    left_lines = []
    right_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]

        if x2 == x1:
            continue

        slope = (y2 - y1) / (x2 - x1)

        if abs(slope) < 0.5:
            continue

        if slope < 0:
            left_lines.append([x1, y1, x2, y2])
        else:
            right_lines.append([x1, y1, x2, y2])

    return left_lines, right_lines


def average_lines(lines: np.ndarray) -> tuple[floating[Any], floating[Any]] | None:
    slopes = []
    intercepts = []

    for x1, y1, x2, y2 in lines:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        slopes.append(m)
        intercepts.append(b)

    if len(slopes) == 0:
        return None

    return np.mean(slopes), np.mean(intercepts)
