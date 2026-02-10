import cv2 as cv

def find_center(contours):
    if contours:
        largest = max(contours, key=cv.contourArea)
        M = cv.moments(largest)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            return cx, cy
    return None, None


def mark_center(frame, cx, cy):
    cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)


def compute_steering(cx, width=320):
    cx = max(0, min(cx, width))
    return round(1 + (cx / width) * 510)
