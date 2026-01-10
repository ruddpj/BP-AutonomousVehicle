from typing import Any
import numpy as np

def find_left_right_lines(lines: np.ndarray) -> tuple[list[np.floating[Any]], list[np.floating[Any]]]:
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


def average_lines(lines: list[np.floating[Any]]) -> tuple[np.floating[Any], np.floating[Any]] | None:
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


def x_at_y(line: tuple[np.floating[Any], np.floating[Any]], y: int) -> int:
    m, b = line
    return int((y - int(b)) / int(m))

def find_lane_center(frame: np.ndarray, lines: np.ndarray) -> int:
    height, width = frame.shape[:2]
    y = int(height * 0.6)

    left_lines, right_lines = find_left_right_lines(lines)

    left_lane = average_lines(left_lines)
    right_lane = average_lines(right_lines)

    left_x = x_at_y(left_lane, y)
    right_x = x_at_y(right_lane, y)

    return (left_x + right_x) // 2
