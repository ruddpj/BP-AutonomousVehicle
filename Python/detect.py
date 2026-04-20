import cv2 as cv
from ultralytics import YOLO

WIDTH = 320
HEIGHT = 240
CENTER = 160

CENTER_THRESHOLD = 60
AREA_THRESHOLD = 5000
CONF_THRESHOLD = 0.5

model = YOLO("yolov8n.pt")

obstructions = ["person", "bicycle", "car", "motorcycle", "bus",
                "truck", "cat", "dog", "horse", "sheep", "cow"]


def detect(frame):
    return model(frame, verbose=True)[0]


def decide_stop(det):
    for box in det.boxes:
        cls = int(box.cls[0])
        name = model.names[cls]

        if name in obstructions:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            obj_center = (x2 + x1) // 2
            area = (x2 - x1) * (y2 - y1)
            conf = float(box.conf[0])

            in_front = abs(obj_center - WIDTH // 2) < CENTER_THRESHOLD
            close = area > AREA_THRESHOLD
            reliable = conf > CONF_THRESHOLD

            if in_front and close and reliable:
                return True, box
    return False, None


def draw_boxes(frame, boxes):
    for box in boxes.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if (y2 - y1) > CENTER:
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.drawMarker(frame, ((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1), (0, 255, 0), markerType=cv.MARKER_CROSS, markerSize=15)
    return frame