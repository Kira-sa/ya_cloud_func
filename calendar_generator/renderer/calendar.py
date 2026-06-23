import io,base64,calendar
from datetime import datetime,date
import math
from PIL import Image,ImageDraw,ImageFont
from calendar_generator.layouts.years import compute_year_grid
from calendar_generator.progress import calc_progress

def render_png_base64(cfg):
    img=Image.new("RGB",(cfg.width,cfg.height),cfg.background_color)
    draw=ImageDraw.Draw(img)
    font=ImageFont.load_default()

    start=datetime.strptime(cfg.start_date,"%Y-%m-%d").date()
    end=datetime.strptime(cfg.end_date,"%Y-%m-%d").date()
    today=date.today()

    pad=cfg.padding
    area_w=cfg.width-pad["left"]-pad["right"]
    area_h=cfg.height-pad["top"]-pad["bottom"]-120

    years=list(range(start.year,end.year+1))
    rows,cols=compute_year_grid(years)

    block_w=area_w//cols
    block_h=area_h//rows

    if len(years) == 1:
        month_cols = 3
        month_rows = 4
    else:
        month_cols = 4
        month_rows = 3

    max_month_w = block_w // month_cols
    max_month_h = block_h // month_rows

    cell=min((max_month_w-10)//7,(max_month_h-18)//6)
    cell=max(2,int(cell*cfg.scale))

    for idx,year in enumerate(years):
        bx=pad["left"]+(idx%cols)*block_w
        by=pad["top"]+(idx//cols)*block_h

        draw.text((bx,by),str(year),fill=cfg.colors["text"],font=font)

        months = []
        for month in range(1,13):
            month_start = date(year, month, 1)
            if month == 12:
                month_end = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(year + 1, month + 1, 1) - timedelta(days=1)

            if month_end < start:
                continue

            if month_start > end:
                continue
            
            months.append(month)

            mx = bx + ((month - 1) % month_cols) * max_month_w
            my = by + 20 + ((month - 1) // month_rows) * max_month_h

            if cell >= 8:
                draw.text((mx,my-12),calendar.month_abbr[month],
                          fill=cfg.colors["text"],font=font)

            weeks=calendar.monthcalendar(year,month)

            for r,w in enumerate(weeks):
                for c,d in enumerate(w):
                    if d == 0:
                        continue

                    cur = date(year, month, d)

                    # Пропускаем даты вне диапазона
                    if cur < start:
                        continue
                    if cur > end:
                        continue

                    color = cfg.colors["future"]
                    if cur < today:
                        color = cfg.colors["past"]
                    elif cur == today:
                        color = cfg.colors["today"]

                    x = mx + c * cell
                    y = my + r * cell

                    circle_ratio = 0.7
                    diameter = int(cell * circle_ratio)
                    offset = (cell - diameter) // 2

                    if cfg.day_style=="circle":
                        draw.ellipse(
                            [
                                x + offset,
                                y + offset,
                                x + offset + diameter, #+cell-1,
                                y + offset + diameter #+cell-1
                            ],
                            fill=color
                        )
                    else:
                        draw.rectangle([x,y,x+cell-1,y+cell-1],fill=color)

                    if cfg.day_style=="number" and cell>=16:
                        draw.text((x+2,y+1),str(d),
                                  fill=cfg.colors["text"],font=font)

    elapsed,total,pct=calc_progress(start,end,today)
    txt=f"{elapsed}/{total} days ({pct:.1f}%)"
    draw.text((pad["left"],cfg.height-pad["bottom"]+50),
              txt,fill=cfg.colors["text"],font=font)

    buf=io.BytesIO()
    img.save(buf,"PNG")
    return base64.b64encode(buf.getvalue()).decode()
