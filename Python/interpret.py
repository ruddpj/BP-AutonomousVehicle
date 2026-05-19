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


def compute_steering(cx, box, center=160, alpha=1.6):
    error = (cx - center) / center
    error = pow(abs(error), alpha) * (1 if error >= 0 else -1)

    if box is not None:
        x1, _, x2, _ = map(int, box.xyxy[0])
        obj_center = (x1 + x2) / 2

        if obj_center < cx:
            bias = x2 / cx
        else:
            bias = -(1.0 - (x1 - cx) / cx)

        error = max(-1.0, min(1.0, error + bias))

    return int(256 + error * 255)


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