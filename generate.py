from calendar_generator.config import CalendarConfig
from calendar_generator.renderer.calendar import render_png

if __name__ == "__main__":
    cfg = CalendarConfig(
        width=1179,
        height=2556,
        background_color="#000000",
        start_date="2026-01-01",
        end_date="2026-12-31",
        scale=1,
        day_style="circle",
        padding={"top": 800, "bottom": 10, "left": 180, "right": 140},
        colors={
            "past": "#5B9CF6",
            "future": "#E0E0E0",
            "today": "#FF6B35",
            "text": "#FFFFFF",
        },
        circle_ratio=0.5,
    )
    png_b64 = render_png(cfg, "test.png")

