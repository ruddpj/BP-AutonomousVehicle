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

    frame_count = 0
    detections = None
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.resize(frame, (320, 240))

        roi = tf.region_of_interest(frame)
        mask = tf.mask_road(roi)
        contours = tf.find_contours(mask)

        if frame_count % 6 == 0:
            detections = dt.detect(frame)
            frame_count = 0

        if detections is None:
            cx, cy = itp.find_center(contours)
            if cx is not None:
                itp.mark_center(frame, cx, cy)
                steering = itp.compute_steering(cx)
            else:
                steering = None
        else:
            steering = itp.avoid_obstacles(detections)

        if steering is not None:
            cnt.sendUDP(steering)
            cv.putText(frame, str(steering), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cnt.badUDP()
            cv.putText(frame, "Lane not detected", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        #All inputs have to be 3-dimensional
        videogrid = tf.video_grid((frame, cv.cvtColor(mask, cv.COLOR_GRAY2BGR)))
        cv.imshow("Lane detection", videogrid)

        if cv.waitKey(1) & 0xFF == 27:  # ESC
            break

        frame_count += 1

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    try:
        cnt.startHotspot()
        time.sleep(2)

        videoLoop()
    finally:
        cnt.stopHotspot()
