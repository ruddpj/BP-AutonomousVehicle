import cv2 as cv
import connect as cnt
import transform as tf
import interpret as itp

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

    stack = tf.video_grid(frame, canny, roi, hough)
    cv.imshow("Lane detection", stack)

    if cv.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv.destroyAllWindows()
