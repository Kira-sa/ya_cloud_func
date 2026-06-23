import base64, io, calendar
from datetime import date, datetime, timedelta
from PIL import Image, ImageDraw, ImageFont

def render_png_base64(cfg):
    img=Image.new("RGB",(cfg.width,cfg.height),cfg.background_color)
    d=ImageDraw.Draw(img)
    font=ImageFont.load_default()

    start=datetime.strptime(cfg.start_date,"%Y-%m-%d").date()
    end=datetime.strptime(cfg.end_date,"%Y-%m-%d").date()
    today=date.today()

    pad=cfg.padding
    x0,y0=pad["left"],pad["top"]
    w=cfg.width-pad["left"]-pad["right"]
    h=cfg.height-pad["top"]-pad["bottom"]-120

    years=list(range(start.year,end.year+1))
    cols=max(1,min(3,len(years)))
    rows=(len(years)+cols-1)//cols

    block_w=w//cols
    block_h=h//rows
    cell=min((block_w-40)//22,(block_h-40)//40)
    cell=max(cell,2)

    for idx,year in enumerate(years):
        bx=x0+(idx%cols)*block_w
        by=y0+(idx//cols)*block_h
        d.text((bx,by),str(year),fill="black",font=font)

        for month in range(1,13):
            mx=bx+((month-1)%4)*(cell*8+10)
            my=by+20+((month-1)//4)*(cell*8+15)

            weeks=calendar.monthcalendar(year,month)
            for r,week in enumerate(weeks):
                for c,day in enumerate(week):
                    if not day:
                        continue
                    cur=date(year,month,day)
                    color="#E0E0E0"
                    if cur < today:
                        color="#5B9CF6"
                    elif cur == today:
                        color="#FF6B35"

                    d.rectangle(
                        [mx+c*cell,my+r*cell,mx+c*cell+cell-1,my+r*cell+cell-1],
                        fill=color
                    )

    total=(end-start).days+1
    elapsed=max(0,min(total,(min(today,end)-start).days+1 if today>=start else 0))
    pct=(elapsed/total*100) if total else 0

    text=f"{elapsed}/{total} ({pct:.1f}%)"
    d.text((x0,cfg.height-pad["bottom"]+40),text,fill="black",font=font)

    buf=io.BytesIO()
    img.save(buf,format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
