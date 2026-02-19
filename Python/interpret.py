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


def compute_steering(cx, detections, width=320):
    obstacle = avoid_obstacles(detections)
    print("Obstacle: ", obstacle)
    cx = max(0, min(cx, width))
    return round(1 + (cx / width) * 510)


def avoid_obstacles(detections, half_frame_width=160):
    steering = 0

    for det in detections.boxes:
        x1, y1, x2, y2 = map(int, det.xyxy[0])

        cx = (x1 + x2) // 2
        height = y2 - y1

        if height > half_frame_width:
            offset = (cx - half_frame_width) / half_frame_width
            steering += -offset

    return steering