"""
FarmTech Solutions — "Ir Além": AWS Rekognition Integration
Author: Richard Schmitz - RM567951

This module demonstrates AWS Rekognition for agricultural image analysis.
It detects labels in farm images (e.g. crops, vehicles, animals) and can
complement the YOLOv5 results from Fase 6.

Setup:
  1. pip install boto3
  2. aws configure
  3. Ensure your IAM user/role has rekognition:DetectLabels permission.
"""

import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime

AWS_REGION = "us-east-1"
MIN_CONFIDENCE = 70.0


def _get_client():
    return boto3.client("rekognition", region_name=AWS_REGION)


def detect_labels_from_file(image_path: str, max_labels: int = 10) -> dict:
    """
    Send a local image to AWS Rekognition DetectLabels.
    Returns detected labels with confidence scores.
    """
    if not os.path.exists(image_path):
        return {"success": False, "error": "Image file not found"}

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        client = _get_client()
        response = client.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=max_labels,
            MinConfidence=MIN_CONFIDENCE,
        )

        labels = [
            {
                "name": lbl["Name"],
                "confidence": round(lbl["Confidence"], 2),
                "categories": [c["Name"] for c in lbl.get("Categories", [])],
            }
            for lbl in response.get("Labels", [])
        ]

        return {
            "success": True,
            "image": os.path.basename(image_path),
            "labels": labels,
            "label_count": len(labels),
            "timestamp": datetime.now().isoformat(),
            "source": "AWS Rekognition",
        }

    except NoCredentialsError:
        return {"success": False, "error": "AWS credentials not configured"}
    except ClientError as e:
        code = e.response["Error"]["Code"]
        return {"success": False, "error": f"AWS Error ({code}): {e.response['Error']['Message']}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def detect_labels_from_s3(bucket: str, key: str, max_labels: int = 10) -> dict:
    """
    Analyze an image stored in S3 using Rekognition.
    """
    try:
        client = _get_client()
        response = client.detect_labels(
            Image={"S3Object": {"Bucket": bucket, "Name": key}},
            MaxLabels=max_labels,
            MinConfidence=MIN_CONFIDENCE,
        )
        labels = [
            {"name": lbl["Name"], "confidence": round(lbl["Confidence"], 2)}
            for lbl in response.get("Labels", [])
        ]
        return {"success": True, "bucket": bucket, "key": key,
                "labels": labels, "timestamp": datetime.now().isoformat()}
    except NoCredentialsError:
        return {"success": False, "error": "AWS credentials not configured"}
    except ClientError as e:
        return {"success": False, "error": str(e)}


def interpret_farm_labels(labels: list) -> dict:
    """
    Map Rekognition labels to agricultural actions.
    """
    farm_keywords = {
        "vehicle": "🚗 Vehicle detected — check for unauthorized access",
        "car": "🚗 Car detected — verify authorization",
        "drone": "🚁 Drone detected — potential surveillance threat",
        "aircraft": "🚁 Aircraft detected — monitor airspace",
        "person": "👤 Person detected — verify identity",
        "animal": "🐄 Animal detected — check fence perimeter",
        "fire": "🔥 Fire/smoke detected — alert fire department immediately",
        "flood": "💧 Flood signs detected — check drainage",
        "plant": "🌱 Crop detected — normal activity",
    }

    actions = []
    for label in labels:
        for keyword, action in farm_keywords.items():
            if keyword.lower() in label["name"].lower():
                actions.append({"label": label["name"],
                                 "confidence": label["confidence"],
                                 "action": action})

    return {
        "actions": actions,
        "requires_alert": any(
            kw in lbl["name"].lower()
            for lbl in labels
            for kw in ["vehicle", "car", "drone", "aircraft", "person", "fire"]
        ),
    }


def get_architecture_description() -> str:
    return """
## AWS Rekognition Architecture — FarmTech Solutions

```
Farm Images (local / ESP32-CAM)
         │
         ▼
  [Streamlit Dashboard]
         │
         ▼
  [boto3 SDK — Python]
         │
         ▼
  AWS Rekognition (DetectLabels)
         │
    ┌────┴────┐
    │         │
 Labels    Confidence
    │         │
    └────┬────┘
         │
         ▼
  [Interpret Labels]
         │
    ┌────┴────┐
    │         │
 Normal    Alert needed
             │
             ▼
        AWS SNS
     (Email / SMS)
```

Services used:
- **Amazon Rekognition** — DetectLabels API
- **Amazon SNS** — alert delivery (email + SMS)
- **IAM** — least-privilege policy: rekognition:DetectLabels + sns:Publish
"""
