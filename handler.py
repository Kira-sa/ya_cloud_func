from calendar_generator.config import CalendarConfig
from calendar_generator.renderer.calendar import render_png_base64

def handler(event, context):
    cfg = CalendarConfig.from_event(event or {})
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "image/png"},
        "isBase64Encoded": True,
        "body": render_png_base64(cfg),
    }
