from utils.data import *
from utils.grid import neighbors4, Coordinate


def parse(data):
    return data.splitlines()


def search(grid, x, y, seen, plant_type):
    if (x, y) not in seen:
        if grid[x][y] == plant_type:
            m = len(grid)
            n = len(grid[0])
            seen.add((x, y))
            perimeter = 4
            total_area = total_perimeter = total_corners = 0
            coord = Coordinate(x, y)
            corner_check = [
                (coord.up(), coord.right(), coord.up().right()),
                (coord.right(), coord.down(), coord.right().down()),
                (coord.down(), coord.left(), coord.down().left()),
                (coord.left(), coord.up(), coord.left().up()),
            ]
            corners = 0
            for side1, side2, corner in corner_check:
                x1, y1 = side1.get_coords()
                x2, y2 = side2.get_coords()
                xc, yc = corner.get_coords()
                side1_bounds = 0 <= x1 < m and 0 <= y1 < n
                side2_bounds = 0 <= x2 < m and 0 <= y2 < n
                if side1_bounds and side2_bounds:
                    if grid[x1][y1] != grid[x][y] and grid[x2][y2] != grid[x][y]:
                        corners += 1
                    elif grid[x1][y1] == grid[x][y] and grid[x2][y2] == grid[x][y] and grid[xc][yc] != grid[x][y]:
                        corners += 1
                elif (side1_bounds and grid[x1][y1] != grid[x][y]) or (side2_bounds and grid[x2][y2] != grid[x][y]):
                    corners += 1
                elif not side1_bounds and not side2_bounds:
                    corners += 1
            for nx, ny in neighbors4(x, y, m, n):
                if grid[nx][ny] == plant_type:
                    perimeter -= 1
                    next_area, next_perimeter, next_corners = search(grid, nx, ny, seen, plant_type)
                    total_area += next_area
                    total_perimeter += next_perimeter
                    total_corners += next_corners
            return total_area + 1, total_perimeter + perimeter, total_corners + corners
    return 0, 0, 0


def part1(grid):
    seen = set()
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            area, perimeter, _ = search(grid, x, y, seen, grid[x][y])
            res += area * perimeter
    return res


def part2(grid):
    seen = set()
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            area, _, corners = search(grid, x, y, seen, grid[x][y])
            res += area * corners
    return res


test = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

data = get_and_write_data(12, 2024)
grid = parse(data)
print_output(part1(grid), part2(grid))
