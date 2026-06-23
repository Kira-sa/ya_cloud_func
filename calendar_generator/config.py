from dataclasses import dataclass
from datetime import date

@dataclass
class CalendarConfig:
    width:int=1179
    height:int=2556
    background_color:str="#FFFFFF"
    start_date:str=""
    end_date:str=""
    scale:float=1.0
    layout:str="years"
    padding:dict=None

    @classmethod
    def from_event(cls,event):
        today=date.today()
        return cls(
            width=event.get("width",1179),
            height=event.get("height",2556),
            background_color=event.get("background_color","#FFFFFF"),
            start_date=event.get("start_date",f"{today.year}-01-01"),
            end_date=event.get("end_date",f"{today.year}-12-31"),
            scale=float(event.get("scale",1.0)),
            layout="years",
            padding=event.get("padding",{"top":300,"bottom":350,"left":50,"right":50})
        )
