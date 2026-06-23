from dataclasses import dataclass
from datetime import date
@dataclass
class DayInfo:
    date: date
    state: str
