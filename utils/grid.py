def neighbors4(x, y, x_lim, y_lim):
    for dx, dy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= dx < x_lim and 0 <= dy < y_lim:
            yield dx, dy
