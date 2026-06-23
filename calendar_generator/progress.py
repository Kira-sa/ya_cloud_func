def calc_progress(start,end,focus):
    total=(end-start).days+1
    if focus < start:
        elapsed=0
    elif focus > end:
        elapsed=total
    else:
        elapsed=(focus-start).days+1
    return elapsed,total,(elapsed/total*100 if total else 0)
