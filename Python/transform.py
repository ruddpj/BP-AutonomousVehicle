import numpy as np
import cv2 as cv

lower_white = np.array([0, 0, 180])
upper_white = np.array([180, 40, 255])

def region_of_interest(frame):
    h, w = frame.shape[:2]
    roi_mask = np.zeros_like(frame)
    roi_height = 100

    roi_mask[h - roi_height:h, :] = [255, 255, 255]
    masked = cv.bitwise_and(frame, roi_mask)
    return masked


def mask_road(frame):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_white, upper_white)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    return mask


def find_contours(mask):
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours

def video_grid(video_array):
    return np.concatenate(video_array, axis=1)