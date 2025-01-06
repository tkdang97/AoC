class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def up(self):
        return Coordinate(self.x - 1, self.y)
    
    def right(self):
        return Coordinate(self.x, self.y + 1)
    
    def down(self):
        return Coordinate(self.x + 1, self.y)
    
    def left(self):
        return Coordinate(self.x, self.y - 1)
    
    def get_coords(self):
        return self.x, self.y


def neighbors4(x, y, x_lim, y_lim):
    for dx, dy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
        if 0 <= dx < x_lim and 0 <= dy < y_lim:
            yield dx, dy


def neighbors8(x, y, x_lim, y_lim):
    for dx, dy in ((x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y)
                   , (x + 1, y + 1), (x, y - 1), (x, y + 1)):
        if 0 <= dx < x_lim and 0 <= dy < y_lim:
            yield dx, dy
