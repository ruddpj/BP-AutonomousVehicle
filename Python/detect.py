import cv2 as cv
from ultralytics import YOLO
import torch

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
torch.use_deterministic_algorithms(True)

WIDTH = 320
HEIGHT = 240
LANE_LEFT = 130
LANE_RIGHT = 190

CENTER_THRESHOLD = 60
CONF_THRESHOLD = 0.5

model = YOLO("yolov8s.pt")

obstructions = {"person" : 4000,
                "bicycle" : 5000,
                "car" : 8000,
                "motorcycle" : 4000,
                "bus" : 30000,
                "truck" : 20000,
                "cat" : 1500,
                "dog" : 3000,
                "horse" : 6000,
                "sheep" : 4000,
                "cow" : 6000}


def detect(frame):
    return model(frame, verbose=False)[0]


def decide_stop(det):
    for box in det.boxes:
        cls = int(box.cls[0])
        name = model.names[cls]

        if name in obstructions:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            area = (x2 - x1) * (y2 - y1)
            conf = float(box.conf[0])
            margin = int(area * 0.001)

            in_front = x1 < (LANE_RIGHT + margin) and x2 > (LANE_LEFT - margin)
            close = area > obstructions[name]
            reliable = conf > CONF_THRESHOLD

            if in_front and close and reliable:
                return True, box
    return False, None


def draw_boxes(frame, box):
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv.drawMarker(frame, ((x2 - x1) // 2 + x1, (y2 - y1) // 2 + y1), (0, 255, 0), markerType=cv.MARKER_CROSS, markerSize=15)
    cv.putText(frame, model.names[int(box.cls[0])], (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame