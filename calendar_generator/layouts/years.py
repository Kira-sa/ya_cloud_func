def compute_year_grid(years):
    cols=min(3,max(1,len(years)))
    rows=(len(years)+cols-1)//cols
    return rows, cols
