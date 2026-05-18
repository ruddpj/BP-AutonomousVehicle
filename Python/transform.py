import numpy as np
import cv2 as cv

lower_black = np.array([0,0, 0])
upper_black = np.array([180, 255, 70])

def region_of_interest(frame):
    h, w = frame.shape[:2]
    roi_height = 100
    roi_mask = np.ones_like(frame) * 255

    roi_mask[h - roi_height:h, :] = frame[h - roi_height:h, :]

    return roi_mask


def mask_road(frame):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_black, upper_black)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    return mask


def find_contours(mask):
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return contours

def transform(frame):
    roi = region_of_interest(frame)
    mask = mask_road(roi)
    contours = find_contours(mask)

    return contours