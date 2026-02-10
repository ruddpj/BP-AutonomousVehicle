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

        frame = tf.region_of_interest(frame)
        mask = tf.mask_road(frame)
        contours = tf.find_contours(mask)
        tf.mark_contours(frame, contours)

        steering = None
        if steering is not None:
            print(steering)
            cnt.sendUDP(steering)
            cv.putText(frame, str(steering), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cnt.badUDP()
            cv.putText(frame, "Lane not detected", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv.imshow("Lane detection", frame)
        cv.imshow("Mask", mask)

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
