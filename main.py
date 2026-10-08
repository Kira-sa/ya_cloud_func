import json

from calendar_generator.config import CalendarConfig
from calendar_generator.renderer.calendar import render_png_base64


def handler(event, context):
    try:
        request = event or {}

        # Для обычного HTTPS-вызова Yandex Cloud
        body = request.get("body")

        if body:
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
        else:
            # Позволяем также вызывать функцию напрямую
            data = request

        cfg = CalendarConfig.from_event(data)
        png_b64 = render_png_base64(cfg)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "image/png",
            },
            "isBase64Encoded": True,
            "body": png_b64,
        }

    except (ValueError, TypeError, json.JSONDecodeError) as exc:
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