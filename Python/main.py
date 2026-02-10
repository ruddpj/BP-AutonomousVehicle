import cv2 as cv
import time
import os
import connect as cnt
import transform as tf
import interpret as itp
import detect as dt

DEBUG_MODE = True

def videoLoop():
    while True and not DEBUG_MODE:
        response = os.system(f"ping -c 1 {cnt.CAM_IP} > /dev/null 2>&1")
        if response == 0:
            print("ESP32-CAM online")
            break
        print(".", end="")
        time.sleep(1)

    cap = cv.VideoCapture(0 if DEBUG_MODE else cnt.CAM_URL)
    if not cap.isOpened():
        print("Cannot open camera")
        exit(1)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.resize(frame, (320, 240))

        yolo = dt.detect(frame)

        canny = tf.canny_transform(frame)
        roi = tf.define_roi(canny)
        hough, lines = tf.hough_transform(frame, roi)

        steering = itp.compute_steering(frame, lines)

        if steering is not None:
            print(steering)
            cnt.sendUDP(steering)
            cv.putText(frame, str(steering), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cnt.badUDP()
            cv.putText(frame, "Lane not detected", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        stack = tf.video_grid(frame, canny, yolo, hough)
        cv.imshow("Lane detection", stack)

        if cv.waitKey(1) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    try:
        cnt.startHotspot()
        time.sleep(2)

        videoLoop()
    finally:
        cnt.stopHotspot()
