from utils.data import get_and_write_data, print_output


moves = {(-1, 0): {"L": (0, -1), "F": (0, 1), "-": (-1, 0)}, (1, 0): {"J": (0, -1), "7": (0, 1), "-": (1, 0)},
         (0, -1): {"|": (0, -1), "7": (-1, 0), "F": (1, 0)}, (0, 1): {"|": (0, 1), "L": (1, 0), "J": (-1, 0)}}


def parse(data):
    res = data.splitlines()
    start = None
    for i, row in enumerate(res):
        for j, val in enumerate(row):
            if val == "S":
                return res, (i, j)
    return res, start


def part1(grid, start):
    visited = set()
    steps = 0
    explore = [(start, "", (0, 0))]
    n = len(grid)
    m = len(grid[0])
    while explore:
        tmp = []
        steps += 1
        for (pos_y, pos_x), item, direction in explore:
            visited.add((pos_y, pos_x))
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)] if item == "" else [moves[direction][item]]
            for dx, dy in dirs:
                x_pos = pos_x + dx
                y_pos = pos_y + dy
                if 0 <= y_pos < n and 0 <= x_pos < m and grid[y_pos][x_pos] in moves[(dx, dy)] and (y_pos, x_pos) not in visited:
                    tmp.append(((y_pos, x_pos), grid[y_pos][x_pos], (dx, dy)))
                    visited.add((y_pos, x_pos))
        explore = tmp
    return steps - 1, visited


def flood(grid, x, y):
    n = len(grid)
    m = len(grid[0])
    queue = [(x, y)]
    grid[y][x] = "O"
    while queue:
        next_x, next_y = queue.pop()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            y_pos = next_y + dy
            x_pos = next_x + dx
            if 0 <= y_pos < n and 0 <= x_pos < m and grid[y_pos][x_pos] == ".":
                grid[y_pos][x_pos] = "O"
                queue.append((x_pos, y_pos))


def part2(grid, path, start):
    doubled_grid = []
    for i, row in enumerate(grid):
        doubled_row = [[], []]
        for j, item in enumerate(row):
            if (i, j) == start:
                doubled_row[0].append("S")
                if (i + 1, j) in path:
                    doubled_row[1].extend("|.")
                else:
                    doubled_row[1].extend("..")
                if (i, j + 1) in path:
                    doubled_row[0].append("-")
            elif (i, j) in path:
                doubled_row[0].append(item)
                doubled_row[0].append("-" if item in "-FL" else ".")
                doubled_row[1].extend("|." if item in "|F7" else "..")
            else:
                doubled_row[0].extend("..")
                doubled_row[1].extend("..")
        doubled_grid += doubled_row
    flood(doubled_grid, 0, 0)
    total = 0
    for i in range(0, len(doubled_grid), 2):
        for j in range(0, len(doubled_grid[i]), 2):
            if doubled_grid[i][j] == ".":
                total += 1
    return total


data = get_and_write_data(10, 2023)
grid, start = parse(data)
p1, path = part1(grid, start)
print_output(p1, part2(grid, path, start))
