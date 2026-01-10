import numpy as np
import cv2 as cv

def video_grid(frame: np.ndarray,
               canny: np.ndarray,
               roi: np.ndarray,
               hough: np.ndarray) -> np.ndarray:
    height, width = frame.shape[:2]

    frame = cv.resize(frame, (width, height))
    canny = cv.resize(canny, (width, height))
    roi = cv.resize(roi, (width, height))
    hough = cv.resize(hough, (width, height))

    canny = cv.cvtColor(canny, cv.COLOR_GRAY2BGR)
    roi = cv.cvtColor(roi, cv.COLOR_GRAY2BGR)

    top = np.hstack((frame, canny))
    bot = np.hstack((roi, hough))

    stacked = np.vstack((top, bot))

    return stacked

def canny_transform(frame: np.ndarray) -> np.ndarray:
    canny = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    canny = cv.GaussianBlur(canny, (5, 5), 0)
    canny = cv.Canny(canny, 100, 200)

    return canny

def define_roi(frame: np.ndarray) -> np.ndarray:
    height, width = frame.shape
    mask = np.zeros_like(frame)

    polygon = np.array([[
        (0, height),
        (width, height),
        (width // 2, height // 2)
    ]], np.int32)

    cv.fillPoly(mask, polygon, 255)
    roi = cv.bitwise_and(frame, mask)

    return roi

def hough_transform(frame: np.ndarray, roi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lines = cv.HoughLinesP(
        roi,
        rho=1,
        theta=np.pi / 180,
        threshold=50,
        minLineLength=30,
        maxLineGap=200
    )

    line_frame = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)
            if abs(slope) > 0.5:
                cv.line(line_frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    hough = cv.addWeighted(frame, 0.8, line_frame, 1, 1)

    return hough, lines