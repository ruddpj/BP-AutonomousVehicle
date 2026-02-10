import cv2 as cv
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

STOP_THRESHOLD = 200
SLOW_THRESHOLD = 150


def detect(frame):
    results = model(frame)[0]


    for det in results.boxes:
        x1, y1, x2, y2 = map(int, det.xyxy[0])
        conf = float(det.conf[0])
        cls = int(det.cls[0])

        cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return frame