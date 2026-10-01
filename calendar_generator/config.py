from dataclasses import dataclass, field
from datetime import date


DEFAULT_PADDING = {
    "top": 250,
    "bottom": 300,
    "left": 40,
    "right": 40,
}


DEFAULT_COLORS = {
    "past": "#5B9CF6",
    "future": "#E0E0E0",
    "today": "#FF6B35",
    "text": "#000000",
}


@dataclass
class CalendarConfig:
    width: int = 1179
    height: int = 2556
    background_color: str = "#000000"
    start_date: str = ""
    end_date: str = ""
    scale: float = 1.0
    day_style: str = "circle"
    padding: dict = field(default_factory=lambda: DEFAULT_PADDING.copy())
    colors: dict = field(default_factory=lambda: DEFAULT_COLORS.copy())
    circle_ratio: float = 0.75

    @classmethod
    def from_event(cls, event):
        today = date.today()

        padding = DEFAULT_PADDING.copy()
        padding.update(event.get("padding") or {})

        colors = DEFAULT_COLORS.copy()
        colors.update(event.get("colors") or {})

        config = cls(
            width=int(event.get("width", 1179)),
            height=int(event.get("height", 2556)),
            background_color=event.get("background_color", "#000000"),
            start_date=event.get(
                "start_date",
                f"{today.year}-01-01",
            ),
            end_date=event.get(
                "end_date",
                f"{today.year}-12-31",
            ),
            scale=float(event.get("scale", 1.0)),
            day_style=event.get("day_style", "circle"),
            padding=padding,
            colors=colors,
            circle_ratio=float(
                event.get("circle_ratio", 0.75)
            ),
        )

        config.validate()

        return config

    def validate(self):
        if self.width <= 0:
            raise ValueError("width must be positive")

        if self.height <= 0:
            raise ValueError("height must be positive")

        if self.scale <= 0:
            raise ValueError("scale must be positive")

        if not 0 < self.circle_ratio <= 1:
            raise ValueError(
                "circle_ratio must be between 0 and 1"
            )

        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)

        if start > end:
            raise ValueError(
                "start_date must not be later than end_date"
            )

        if self.day_style not in {
            "circle",
            "rectangle",
            "number",
        }:
            raise ValueError(
                "day_style must be circle, rectangle or number"
            )

        required_padding = {
            "top",
            "bottom",
            "left",
            "right",
        }

        if set(self.padding) != required_padding:
            raise ValueError(
                "padding must contain exactly: "
                "top, bottom, left, right"
            )

        for name, value in self.padding.items():
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"padding.{name} must be a number"
                )

            if value < 0:
                raise ValueError(
                    f"padding.{name} must not be negative"
                )

        area_w = (
            self.width
            - self.padding["left"]
            - self.padding["right"]
        )

        area_h = (
            self.height
            - self.padding["top"]
            - self.padding["bottom"]
            - 520
        )

        if area_w <= 0:
            raise ValueError(
                "padding leaves no usable horizontal area"
            )

        if area_h <= 0:
            raise ValueError(
                "padding leaves no usable vertical area"
            )

        required_colors = {
            "past",
            "future",
            "today",
            "text",
        }

        if set(self.colors) != required_colors:
            raise ValueError(
                "colors must contain exactly: "
                "past, future, today, text"
            )