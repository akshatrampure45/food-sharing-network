"""
Notification dispatch. Logs locally when AWS isn't configured, publishes to
SNS once app.config.settings.sns_topic_arn / AWS keys are set.
"""
import logging

from app.config import settings

logger = logging.getLogger("notify")


def send_notification(event: str, message: str) -> None:
    if not settings.sns_topic_arn or not settings.aws_access_key_id:
        logger.info("[notify:%s] %s (SNS not configured — logged only)", event, message)
        return

    import boto3

    client = boto3.client(
        "sns",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
    client.publish(
        TopicArn=settings.sns_topic_arn,
        Message=message,
        MessageAttributes={"event": {"DataType": "String", "StringValue": event}},
    )
