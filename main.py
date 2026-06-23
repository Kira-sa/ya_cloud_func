# import json

from calendar_generator.config import CalendarConfig
from calendar_generator.renderer import render_png_base64

def handler(event, context):
    cfg = CalendarConfig.from_event(event or {})
    png_b64 = render_png_base64(cfg)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "image/png"},
        "isBase64Encoded": True,
        "body": png_b64,
    }


# def handler(event, context):
#     return {
#         'statusCode': 200,
#         'headers': {
#             "Content-Type": "image/png"
#         },
#         'isBase64Encoded': True,
#         'body': encoded_png
#     }