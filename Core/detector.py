"""
=========================================================
Smart People Flow Analytics Pro
Detection Engine
=========================================================
"""

import time
from ultralytics import YOLO

from config import (
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
    PERSON_CLASS_ID,
    TRACKER_CONFIG
)


class PeopleDetector:
    """
    YOLO11 + ByteTrack Detection Engine
    """

    def __init__(self):

        print("\nLoading YOLO Model...")

        self.model = YOLO(MODEL_PATH)

        print("✓ Model Loaded Successfully")

        self.last_inference_time = 0

    # =====================================================
    # Detect People
    # =====================================================

    def detect(self, frame):

        start = time.time()

        results = self.model.track(

            frame,

            persist=True,

            tracker=TRACKER_CONFIG,

            conf=CONFIDENCE_THRESHOLD,

            iou=IOU_THRESHOLD,

            verbose=False

        )

        self.last_inference_time = time.time() - start

        detections = []

        if len(results) == 0:
            return detections

        result = results[0]

        if result.boxes is None:
            return detections

        boxes = result.boxes

        for box in boxes:

            cls = int(box.cls[0])

            if cls != PERSON_CLASS_ID:
                continue

            if box.id is None:
                continue

            track_id = int(box.id.item())

            confidence = float(box.conf.item())

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            width = x2 - x1
            height = y2 - y1

            center_x = int((x1 + x2) / 2)

            # Feet Position
            center_y = y2

            detections.append({

                "id": track_id,

                "confidence": confidence,

                "bbox": (x1, y1, x2, y2),

                "center": (center_x, center_y),

                "width": width,

                "height": height,

                "class": cls

            })

        return detections

    # =====================================================
    # Performance
    # =====================================================

    def inference_time(self):

        return self.last_inference_time

    def inference_fps(self):

        if self.last_inference_time == 0:
            return 0

        return 1 / self.last_inference_time

    # =====================================================
    # Utility
    # =====================================================

    def people_count(self, detections):

        return len(detections)

    def is_empty(self, detections):

        return len(detections) == 0