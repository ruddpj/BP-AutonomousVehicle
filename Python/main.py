import cv2 as cv
import time
import connect as cnt
import transform as tf
import interpret as itp
import detect as dt

DEBUG_MODE = True

def videoLoop():
    if not DEBUG_MODE:
        cnt.ping_cam()

    cap = cv.VideoCapture(0 if DEBUG_MODE else cnt.CAM_URL)
    if not cap.isOpened():
        print("Cannot open camera")
        exit(1)

    frame_count = 0
    detections, true_det = None, None
    stop = False

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv.resize(frame, (320, 240))

        # Detect obstacles every 6 frames
        if frame_count % 6 == 0:
            detections = dt.detect(frame)
            frame_count = 0

            for det in detections:
                stop, true_det = dt.decide_stop(det)

        # If an obstacle is detected, stop the car
        if stop:
            dt.draw_boxes(frame, true_det)
            steering = 0
        else:
            # No obstacle detected, find the lane center and continue
            contours = tf.transform(frame)

            cx, cy = itp.find_center(contours)
            if cx is not None:
                itp.mark_center(frame, cx, cy)
                steering = itp.compute_steering(cx)
            else:
                steering = 0

        cnt.sendUDP(steering)
        output = itp.show_text(frame, steering, stop)

        # All inputs have to be 3-dimensional
        cv.imshow("Lane detection", output)

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
