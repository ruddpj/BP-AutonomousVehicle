import cv2 as cv
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

obstructions = ["person", "car", "dog", "truck"]


def detect(frame):
    return model(frame, verbose=True)[0]


def decide_stop(det, center = 160, min_h = 50):
    for box in det.boxes:
        cls = int(box.cls[0])
        name = model.names[cls]

        if name in obstructions:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            obj_center = (x2 + x1) // 2
            area = (x2 - x1) * (y2 - y1)

            if abs(obj_center - center) < min_h and area > 10000:
                return True, box
    return False, None


def draw_boxes(frame, boxes):
    for box in boxes.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if (y2 - y1) > frame.shape[0] // 2:
            cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv.drawMarker(frame, ((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1), (0, 255, 0), markerType=cv.MARKER_CROSS, markerSize=15)
    return frame