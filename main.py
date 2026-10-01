import json

from calendar_generator.config import CalendarConfig
from calendar_generator.renderer.calendar import render_png_base64


def handler(event, context):
    try:
        cfg = CalendarConfig.from_event(event or {})
        png_b64 = render_png_base64(cfg)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/png",
            },
            "isBase64Encoded": True,
            "body": png_b64,
        }

    except ValueError as exc:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
            },
            "isBase64Encoded": False,
            "body": json.dumps(
                {"error": str(exc)},
                ensure_ascii=False,
            ),
        }