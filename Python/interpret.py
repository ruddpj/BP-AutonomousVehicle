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
    return round(511 - (cx / width) * 510)


def show_text(frame, steering, stop):
    if steering != 0:
        cv.putText(frame, str(steering),
                   (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 255, 0), 2)
    elif stop:
        cv.putText(frame, "Obstacle detected",
                   (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 0, 255), 2)
    else:
        cv.putText(frame, "Lane not detected",
                   (10, 30), cv.FONT_HERSHEY_SIMPLEX,
                   1, (0, 255, 0), 2)

    return frame