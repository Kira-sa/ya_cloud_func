import io, base64, calendar
from datetime import datetime, date, timedelta

from PIL import Image, ImageDraw, ImageFont

from calendar_generator.config import CalendarConfig
from calendar_generator.layouts.years import compute_year_grid
from calendar_generator.progress import calc_progress


def render_png_base64(cfg: "CalendarConfig"):
    img=Image.new("RGB",(cfg.width,cfg.height),cfg.background_color)
    draw=ImageDraw.Draw(img)
    font=ImageFont.load_default(size=24)

    start=datetime.strptime(cfg.start_date,"%Y-%m-%d").date()
    end=datetime.strptime(cfg.end_date,"%Y-%m-%d").date()
    today=date.today()

    pad=cfg.padding
    area_w=cfg.width-pad["left"]-pad["right"]
    area_h=cfg.height-pad["top"]-pad["bottom"]-520

    years=list(range(start.year,end.year+1))
    rows,cols=compute_year_grid(years)

    block_w=area_w//cols
    block_h=area_h//rows

    if len(years) == 1:
        month_cols = 3  # столбцы 
        month_rows = 4  # строки
    else :
        month_cols = 4  # столбцы 
        month_rows = 3  # строки

    max_month_w = block_w // month_cols
    max_month_h = block_h // month_rows
    
    base_cell = min(
        (max_month_w - 10) // 7,
        (max_month_h - 18) // 6
    )

    cell = max(2, int(base_cell * cfg.scale))

    max_cell = min(
        (max_month_w - 10) // 7,
        (max_month_h - 18) // 6
    )

    cell = min(cell, max_cell)

    for idx,year in enumerate(years):
        bx=pad["left"]+(idx%cols)*block_w
        by=pad["top"]+(idx//cols)*block_h

        # Год
        # draw.text((bx,by),str(year),fill=cfg.colors["text"],font=font)

        months = []
        for month in range(1,13):
            month_start = date(year, month, 1)
            if month == 12:
                month_end = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(year, month + 1, 1) - timedelta(days=1)

            if month_end < start:
                continue

            if month_start > end:
                continue
            
            months.append(month)

            # Координаты месяца
            i_cols = (month - 1) % month_cols
            i_rows = (month - 1) // month_cols

            # ряд
            mx = bx + i_cols * max_month_w
            # столбец
            my = by + 20 + i_rows * max_month_h

            # Если много месяцев - подписываем
            # if cell >= 8:
            #     # Месяц
            #     draw.text((mx,my-12),calendar.month_abbr[month],
            #               fill=cfg.colors["text"],font=font)

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

                    circle_ratio = min(1.0, max(0.0, float(cfg.circle_ratio)))
                    diameter = max(1, int(cell * circle_ratio))
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
    draw.text((pad["left"],cfg.height-pad["bottom"]-40),
              txt,fill=cfg.colors["text"],font=font)

    buf=io.BytesIO()
    img.save(buf,"PNG")

    return base64.b64encode(buf.getvalue()).decode()


def render_png(cfg, filename):
    generated_img = render_png_base64(cfg)
    img = Image.open(io.BytesIO(base64.b64decode(generated_img)))
    img.save(filename, "PNG")

