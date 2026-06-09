"""
FarmTech Solutions - Fase 6: Computer Vision (YOLOv5 — Car/Drone Detection)
Author: Richard Schmitz - RM567951
"""

import os
import random
from datetime import datetime

LABELS = ["car", "drone"]
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(_BASE, "dataset", "images", "test")


def _yolo_available() -> bool:
    try:
        import torch  # noqa: F401
        return True
    except ImportError:
        return False


def run_inference(image_path: str) -> dict:
    """
    Run YOLOv5 inference on an image.
    Falls back to a confidence-scored simulation if torch is not installed.
    """
    if not os.path.exists(image_path):
        return {"error": "Image not found", "detections": []}

    if _yolo_available():
        return _run_yolo(image_path)
    return _simulate_detection(image_path)


def _run_yolo(image_path: str) -> dict:
    import torch
    try:
        model = torch.hub.load(
            "ultralytics/yolov5", "custom",
            path="models/yolov5_farmtech.pt",
            force_reload=False,
            verbose=False,
        )
        model.conf = 0.4
        results = model(image_path)
        detections = []
        for *box, conf, cls in results.xyxy[0].tolist():
            detections.append({
                "label": LABELS[int(cls)] if int(cls) < len(LABELS) else "unknown",
                "confidence": round(conf, 3),
                "bbox": [round(v, 1) for v in box],
            })
        return {"image": os.path.basename(image_path), "detections": detections,
                "timestamp": datetime.now().isoformat(), "source": "YOLOv5"}
    except Exception as e:
        return _simulate_detection(image_path, note=str(e))


def _simulate_detection(image_path: str, note: str = "") -> dict:
    fname = os.path.basename(image_path).lower()
    if "car" in fname:
        label, conf = "car", round(random.uniform(0.88, 0.99), 3)
    elif "drone" in fname:
        label, conf = "drone", round(random.uniform(0.85, 0.97), 3)
    else:
        label = random.choice(LABELS)
        conf = round(random.uniform(0.60, 0.85), 3)

    return {
        "image": os.path.basename(image_path),
        "detections": [{"label": label, "confidence": conf, "bbox": [50, 50, 300, 300]}],
        "timestamp": datetime.now().isoformat(),
        "source": "Simulated" + (f" ({note})" if note else ""),
    }


def get_test_images() -> list:
    if not os.path.exists(DATASET_DIR):
        return []
    return [
        os.path.join(DATASET_DIR, f)
        for f in os.listdir(DATASET_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]


def alert_needed(result: dict) -> bool:
    """Returns True if a detection warrants an AWS SNS alert."""
    for det in result.get("detections", []):
        if det["confidence"] >= 0.70:
            return True
    return False


def format_alert_message(result: dict) -> str:
    lines = [f"🚨 FarmTech Vision Alert — {result['timestamp']}",
             f"Image: {result['image']}"]
    for det in result["detections"]:
        lines.append(f"  • {det['label'].upper()} detected — confidence: {det['confidence']*100:.1f}%")
    lines.append("\nRecommended action: Inspect the farm area immediately.")
    return "\n".join(lines)
