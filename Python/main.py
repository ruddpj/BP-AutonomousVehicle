import cv2 as cv
import connect as cnt
import numpy as np

def video_grid(frame_v: np.ndarray,
               canny_v: np.ndarray,
               roi_v: np.ndarray,
               hough_v: np.ndarray) -> np.ndarray:
    h, w = frame_v.shape[:2]

    frame_v = cv.resize(frame_v, (w, h))
    canny_v = cv.resize(canny_v, (w, h))
    roi_v = cv.resize(roi_v, (w, h))
    hough_v = cv.resize(hough_v, (w, h))

    canny_v = cv.cvtColor(canny_v, cv.COLOR_GRAY2BGR)
    roi_v = cv.cvtColor(roi_v, cv.COLOR_GRAY2BGR)

    top = np.hstack((frame_v, canny_v))
    bot = np.hstack((roi_v, hough_v))

    stacked = np.vstack((top, bot))

    return stacked


cap = cv.VideoCapture(cnt.CAM_URL)
if not cap.isOpened():
    print("Cannot open stream")
    exit(1)

print("Stream connected")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv.resize(frame, (320, 240))

    canny = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    canny = cv.GaussianBlur(canny, (5, 5), 0)
    canny = cv.Canny(canny, 100, 200)

    height, width = canny.shape
    mask = np.zeros_like(canny)
    polygon = np.array([[
        (0, height),
        (width, height),
        (width//2, height//2)
    ]], np.int32)
    cv.fillPoly(mask, polygon, 255)
    roi = cv.bitwise_and(canny, mask)

    lines = cv.HoughLinesP(
        roi,
        rho=1,
        theta=np.pi/180,
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

    #cnt.sendUDP(direction)
    #cv.putText(frame, direction, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    stack = video_grid(frame, canny, roi, hough)
    cv.imshow("Lane detection", stack)

    if cv.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv.destroyAllWindows()
