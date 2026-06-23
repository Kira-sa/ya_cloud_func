from dataclasses import dataclass, field
from datetime import date

@dataclass
class CalendarConfig:
    width:int=1179
    height:int=2556
    background_color:str="#000000"
    start_date:str=""
    end_date:str=""
    scale:float=1.0
    day_style:str="circle"
    padding:dict=field(default_factory=dict)
    colors:dict=field(default_factory=dict)
    circle_ratio:float=0.75

    @classmethod
    def from_event(cls,e):
        t=date.today()
        return cls(
            width=e.get("width",1179),
            height=e.get("height",2556),
            background_color=e.get("background_color","#000000"),
            start_date=e.get("start_date",f"{t.year}-01-01"),
            end_date=e.get("end_date",f"{t.year}-12-31"),
            scale=float(e.get("scale",1.0)),
            day_style=e.get("day_style","circle"),
            padding=e.get("padding",{"top":250,"bottom":300,"left":40,"right":40}),
            colors=e.get("colors",{
                "past":"#5B9CF6","future":"#E0E0E0",
                "today":"#FF6B35","text":"#000000"
            }),
            circle_ratio=e.get("circle_ratio", 0.75)
        )
