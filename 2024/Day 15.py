from utils.data import *
from copy import deepcopy


def parse(data):
    layout, moves = data.split("\n\n")
    return list(map(list, layout.splitlines())), moves.replace("\n", "")


def do_move(layout, x, y, dx, dy, part2=False):
    nx, ny = x + dx, y + dy
    if layout[nx][ny] == ".":  # free space, just move
        layout[nx][ny] = "@"
        layout[x][y] = "."
        return nx, ny
    elif layout[nx][ny] == "#":  # wall, no move
        return x, y
    else:  # box
        if not part2:
            curr_x, curr_y = nx, ny
            while layout[curr_x][curr_y] == "O":  # check if there is a chain of boxes
                curr_x += dx
                curr_y += dy
            if layout[curr_x][curr_y] == "#":  # Wall behind the box(es), no move
                return x, y
            else:  # otherwise there is a free space to push the boxes
                layout[curr_x][curr_y] = "O"
                layout[nx][ny] = "@"
                layout[x][y] = "."
                return nx, ny
        else:
            curr_x, curr_y = nx, ny
            if dx == 0:  # no change in horizontal movement, since height is unchanged
                while layout[curr_x][curr_y] in "[]":  # check if there is a chain of boxes
                    curr_y += dy
                if layout[curr_x][curr_y] == "#":  # Wall behind the box(es), no move
                    return x, y
                else:  # otherwise there is a free space to push the boxes
                    if dy == 1:  # shift right
                        layout[curr_x][ny + 1 : curr_y + 1] = layout[curr_x][ny:curr_y]
                    else:  # shift left
                        layout[curr_x][curr_y:ny] = layout[curr_x][curr_y + 1 : ny + 1]
                    layout[nx][ny] = "@"
                    layout[x][y] = "."
                    return nx, ny
            else:  # vertical movement, need to account for shifted boxes
                moveable = True
                startbox = (ny, nx) if layout[nx][ny] == "[" else (ny - 1, nx)
                boxes_to_push = []
                row_boxes = {startbox}
                while row_boxes:
                    boxes_to_push.extend(row_boxes)
                    next_boxes = set()
                    for box_left, row in row_boxes:
                        if layout[row + dx][box_left] == "#" or layout[row + dx][box_left + 1] == "#":  # wall prevents push
                            moveable = False
                            next_boxes = set()
                            break
                        for py in range(box_left - 1, box_left + 2):
                            if layout[row + dx][py] == "[":
                                next_boxes.add((py, row + dx))
                    row_boxes = next_boxes

                if moveable:  # push is possible, execute moves
                    for box_left, row in reversed(boxes_to_push):
                        layout[row + dx][box_left] = "["
                        layout[row + dx][box_left + 1] = "]"
                        layout[row][box_left] = "."
                        layout[row][box_left + 1] = "."
                        layout[nx][ny] = "@"
                        layout[x][y] = "."
                    return nx, ny
                else:
                    return x, y


def part1(layout, moves):
    copy = deepcopy(layout)
    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    start = (0, 0)
    for i, row in enumerate(layout):
        for j, val in enumerate(row):
            if val == "@":
                start = (i, j)

    curr_x, curr_y = start
    for move in moves:
        dx, dy = directions[move]
        curr_x, curr_y = do_move(copy, curr_x, curr_y, dx, dy)
    result = 0
    for i, row in enumerate(copy):
        for j, val in enumerate(row):
            if val == "O":
                result += 100 * i + j
    return result


def part2(layout, moves):
    wide_map = []
    for line in layout:
        curr_line = []
        for c in line:
            match c:
                case "#":
                    curr_line.extend("##")
                case "O":
                    curr_line.extend("[]")
                case ".":
                    curr_line.extend("..")
                case "@":
                    curr_line.extend("@.")
        wide_map.append(curr_line)


    directions = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    start = (0, 0)
    for i, row in enumerate(wide_map):
        for j, val in enumerate(row):
            if val == "@":
                start = (i, j)
                

    curr_x, curr_y = start
    for move in moves:
        dx, dy = directions[move]
        curr_x, curr_y = do_move(wide_map, curr_x, curr_y, dx, dy, True)
        
        # print(f"Move {move}")
        # print("\n".join("".join(row) for row in wide_map))
        # print()
    # print("\n".join("".join(row) for row in wide_map))
    
    result = 0
    for i, row in enumerate(wide_map):
        for j, val in enumerate(row):
            if val == "[":
                result += 100 * i + j
    return result


test = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

data = get_and_write_data(15, 2024)
layout, moves = parse(data)
print_output(part1(layout, moves), part2(layout, moves))
