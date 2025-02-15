from ultralytics import YOLO
import numpy as np

# Load YOLO ONNX model
model_path = "app/models/bestyolov8s.onnx"
model = YOLO(model_path)  # Load ONNX model

def run_inference(image):
    """Runs YOLO ONNX inference using Ultralytics and returns detections."""
    results = model(image)  # Run inference

    detections = []
    for result in results:
        boxes = result.boxes.xyxy.numpy()  # Bounding box (x1, y1, x2, y2)
        confs = result.boxes.conf.numpy()  # Confidence scores
        classes = result.boxes.cls.numpy()  # Class IDs

        for box, conf, cls in zip(boxes, confs, classes):
            if conf > 0.25:  # Confidence threshold
                detections.append({
                    "x1": int(box[0]),
                    "y1": int(box[1]),
                    "x2": int(box[2]),
                    "y2": int(box[3]),
                    "confidence": float(conf),
                    "class": int(cls)
                })

    return detections
