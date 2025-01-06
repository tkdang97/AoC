from utils.data import *


def parse(data):
    grid = {}
    lines = data.splitlines()
    outer_portals = set()
    for x, row in enumerate(lines):
        y = 0
        while y < len(row):
            if row[y].isalpha():
                if x < len(lines) - 1 and lines[x + 1][y].isalpha():  # vertical portal
                    if x == len(lines) - 2 or lines[x - 1][y] == ".":  # below opening
                        nx, ny = x - 1, y
                    else:
                        nx, ny = x + 2, y
                    grid[(nx, ny)] = lines[x][y] + lines[x + 1][y]
                    if x == 0 or x == len(lines) - 2:  # outer portal
                        outer_portals.add((nx, ny))
                elif y < len(row) - 1 and row[y + 1].isalpha():  # horizontal portal
                    if y == len(row) - 2 or row[y - 1] == ".":  # right of opening
                        nx, ny = x, y - 1
                    else:
                        nx, ny = x, y + 2
                    grid[(nx, ny)] = row[y] + row[y + 1]
                    if y == 0 or y == len(row) - 2:
                        outer_portals.add((nx, ny))
            elif row[y] in ".#" and (x, y) not in grid:
                grid[(x, y)] = row[y]
            y += 1

    portals = {}
    start = end = None
    for coord, val in grid.items():
        if val == "AA":
            start = coord
        elif val == "ZZ":
            end = coord
        elif val.isalpha():
            if val in portals:
                other = portals[val]
                portals[val] = {coord: other, other: coord}
            else:
                portals[val] = coord
    return grid, start, end, portals, outer_portals


def part1():
    seen = set()
    curr = [start]
    seen = {start}
    num_steps = 0
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
    while curr:
        nxt = []
        for coord in curr:
            x, y = coord
            if grid[coord] in portals:
                other = portals[grid[coord]][coord]
                if other not in seen:
                    nxt.append(other)
                    continue
            for dx, dy in dirs:
                next_coord = x + dx, y + dy
                if next_coord in grid:
                    if next_coord == end:
                        return num_steps + 1
                    val = grid[next_coord]
                    if (val == "." or val in portals) and next_coord not in seen:
                        nxt.append(next_coord)
                        seen.add(next_coord)
        curr = nxt
        num_steps += 1


def part2():
    seen = set()
    curr = [(start, 0)]
    seen = {(start, 0)}
    num_steps = 0
    dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
    while curr:
        nxt = []
        for coord, level in curr:
            x, y = coord
            if grid[coord] in portals:
                other = portals[grid[coord]][coord]
                if coord in outer_portals and level > 0 and (other, level - 1) not in seen:
                    nxt.append((other, level - 1))
                    continue
                elif coord not in outer_portals and (other, level + 1) not in seen:
                    nxt.append((other, level + 1))
                    continue
            for dx, dy in dirs:
                next_coord = x + dx, y + dy
                if next_coord in grid:
                    if next_coord == end and level == 0:
                        return num_steps + 1
                    val = grid[next_coord]
                    if (val == "." or val in portals) and (next_coord, level) not in seen:
                        nxt.append((next_coord, level))
                        seen.add((next_coord, level))
        curr = nxt
        num_steps += 1


test = """             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     
"""

data = get_and_write_data(20, 2019)
grid, start, end, portals, outer_portals = parse(data)
print_output(part1(), part2())
