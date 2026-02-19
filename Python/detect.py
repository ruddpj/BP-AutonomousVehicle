import cv2 as cv
from ultralytics import YOLO

model = YOLO("yolov8n.pt")


def detect(frame):
    return model(frame, verbose=False)[0]


def draw_boxes(frame, boxes):
    for box in boxes.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if (y2 - y1) > frame.shape[0] // 2:
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.drawMarker(frame, ((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1), (0, 255, 0), markerType=cv.MARKER_CROSS, markerSize=15)
    return frame