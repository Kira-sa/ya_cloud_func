from dataclasses import dataclass, field
from datetime import date


@dataclass
class CalendarConfig:
    width: int = 1179
    height: int = 2556
    background_color: str = "#000000"
    start_date: str = ""
    end_date: str = ""
    scale: float = 1.0
    day_style: str = "circle"
    padding: dict = field(default_factory=dict)
    colors: dict = field(default_factory=dict)
    circle_ratio: float = 0.75

    @classmethod
    def from_event(cls, event):
        today = date.today()

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
            padding=event.get(
                "padding",
                {
                    "top": 250,
                    "bottom": 300,
                    "left": 40,
                    "right": 40,
                },
            ),
            colors=event.get(
                "colors",
                {
                    "past": "#5B9CF6",
                    "future": "#E0E0E0",
                    "today": "#FF6B35",
                    "text": "#000000",
                },
            ),
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

        if start.year != end.year:
            raise ValueError(
                "Only one year is supported"
            )

        if self.day_style not in {"circle", "rectangle", "number"}:
            raise ValueError(
                "day_style must be circle, rectangle or number"
            )
