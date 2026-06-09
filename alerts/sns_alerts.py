"""
FarmTech Solutions - AWS SNS Alert Service
Author: Richard Schmitz - RM567951

Setup:
  1. pip install boto3
  2. aws configure  (or set env vars AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION)
  3. Create an SNS topic and paste its ARN in TOPIC_ARN below or pass it at runtime.
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from datetime import datetime

TOPIC_ARN = "arn:aws:sns:us-east-1:311141542302:Farmtech_alertas"
AWS_REGION = "us-east-1"


def _get_client():
    return boto3.client("sns", region_name=AWS_REGION)


def send_alert(subject: str, message: str, topic_arn: str = TOPIC_ARN) -> dict:
    """
    Publish a message to an SNS topic.
    Subscribers (email / SMS) receive the alert automatically.
    """
    if not topic_arn:
        return {"success": False, "error": "TOPIC_ARN not configured"}
    try:
        client = _get_client()
        response = client.publish(
            TopicArn=topic_arn,
            Subject=subject[:100],
            Message=message,
        )
        return {"success": True, "message_id": response["MessageId"]}
    except NoCredentialsError:
        return {"success": False, "error": "AWS credentials not found"}
    except ClientError as e:
        return {"success": False, "error": str(e)}


def send_sensor_alert(umidade: float, ph: float, temp: float,
                      nutrientes: int, topic_arn: str = TOPIC_ARN) -> dict:
    """Compose and send a structured sensor alert."""
    issues = []
    actions = []

    if umidade < 60:
        issues.append(f"Soil humidity LOW ({umidade}%)")
        actions.append("Activate irrigation pump immediately")
    elif umidade > 80:
        issues.append(f"Soil humidity HIGH ({umidade}%)")
        actions.append("Check drainage system")

    if not (6.0 <= ph <= 6.8):
        issues.append(f"Soil pH out of range ({ph})")
        actions.append("Apply lime or acidifier to correct pH")

    if temp > 30:
        issues.append(f"High temperature ({temp}°C)")
        actions.append("Monitor crop for heat stress")

    if nutrientes < 2:
        issues.append(f"Low NPK nutrients ({nutrientes}/3)")
        actions.append("Apply fertilizer — check N, P, K levels")

    if not issues:
        return {"success": True, "message_id": "no_alert_needed"}

    subject = "⚠️ FarmTech Alert — Sensor Threshold Exceeded"
    body = (
        f"FarmTech Solutions — Automated Alert\n"
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"ISSUES DETECTED:\n" + "\n".join(f"  • {i}" for i in issues) +
        f"\n\nRECOMMENDED ACTIONS:\n" + "\n".join(f"  {n+1}. {a}" for n, a in enumerate(actions)) +
        f"\n\nPlease log into the FarmTech dashboard for full details."
    )
    return send_alert(subject, body, topic_arn)


def send_vision_alert(detection_result: dict, topic_arn: str = TOPIC_ARN) -> dict:
    """Send alert triggered by Fase 6 vision detection."""
    subject = "🚨 FarmTech Vision Alert — Unauthorized Object Detected"
    detections = detection_result.get("detections", [])
    lines = [f"  • {d['label'].upper()} — {d['confidence']*100:.1f}% confidence"
             for d in detections]
    body = (
        f"FarmTech Solutions — Vision System Alert\n"
        f"Timestamp: {detection_result.get('timestamp', datetime.now().isoformat())}\n"
        f"Image: {detection_result.get('image', 'unknown')}\n\n"
        f"DETECTIONS:\n" + "\n".join(lines) +
        f"\n\nRECOMMENDED ACTION: Inspect the farm perimeter immediately.\n"
        f"Contact security if unauthorized vehicle/drone is confirmed."
    )
    return send_alert(subject, body, topic_arn)


def list_subscriptions(topic_arn: str = TOPIC_ARN) -> list:
    """List current SNS topic subscriptions."""
    try:
        client = _get_client()
        resp = client.list_subscriptions_by_topic(TopicArn=topic_arn)
        return resp.get("Subscriptions", [])
    except Exception:
        return []


def subscribe_email(email: str, topic_arn: str = TOPIC_ARN) -> dict:
    """Subscribe an email address to the SNS topic."""
    try:
        client = _get_client()
        resp = client.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint=email)
        return {"success": True, "subscription_arn": resp.get("SubscriptionArn", "")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def subscribe_sms(phone: str, topic_arn: str = TOPIC_ARN) -> dict:
    """Subscribe a phone number (E.164 format: +5511999999999) to the SNS topic."""
    try:
        client = _get_client()
        resp = client.subscribe(TopicArn=topic_arn, Protocol="sms", Endpoint=phone)
        return {"success": True, "subscription_arn": resp.get("SubscriptionArn", "")}
    except Exception as e:
        return {"success": False, "error": str(e)}
