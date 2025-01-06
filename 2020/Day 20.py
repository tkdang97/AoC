from utils.data import *
from collections import defaultdict


def parse(data):
    tiles = {}
    for tile in data.split("\n\n"):
        info, *grid = tile.splitlines()
        _, n = info.split()
        tile_num = int(n[:-1])
        tiles[tile_num] = grid
    return tiles


def get_neighbors(tiles):
    borders = {}
    for tile, grid in tiles.items():
        borders[tile] = (
            grid[0],
            "".join(grid[i][-1] for i in range(len(grid))),
            grid[-1],
            "".join(grid[i][0] for i in range(len(grid))),
        )
    matches = defaultdict(set)
    border_matches = defaultdict(dict)
    for tile, image_borders in borders.items():
        for tile2, image_borders2 in borders.items():
            if tile != tile2:
                for i, border in enumerate(image_borders):
                    flipped = border[::-1]
                    for j, border2 in enumerate(image_borders2):
                        flipped2 = border2[::-1]
                        if border == border2 or flipped == border2 or border == flipped2 or flipped == flipped2:
                            matches[tile].add(tile2)
                            matches[tile2].add(tile)
                            border_matches[tile][tile2] = i
                            border_matches[tile2][tile] = j
    return matches, border_matches


def part1(tiles):
    matches, _ = get_neighbors(tiles)
    corners = [tile for tile in matches if len(matches[tile]) == 2]
    res = 1
    for corner in corners:
        res *= corner
    return res


def flip(tile):
    return tile[::-1]


def rotate(tile):
    return list("".join(col[::-1]) for col in zip(*tile))  # clockwise rotation


def get_layout(matches, tiles, border_matches):
    corners = []
    edges = set()
    for tile, match in matches.items():
        if len(match) == 2:
            corners.append(tile)
        elif len(match) == 3:
            edges.add(tile)

    width = int(len(matches) ** 0.5)
    layout = [[0] * width for _ in range(width)]
    adjusted_tiles = [[None] * width for _ in range(width)]
    layout[0][0] = corners[0]
    done = {corners[0]}
    done_coords = {(0, 0)}
    right, down = tuple(matches[corners[0]])
    queue = [(right, 0, 0), (down, 0, 0)]

    # find correct rotation for first corner based on two neighbors
    border_r = border_matches[corners[0]][right]
    border_d = border_matches[corners[0]][down]
    tile = tiles[corners[0]]
    if border_r == (border_d + 1) % 4:
        tile = flip(tile)
        border_d = (border_d + 2) % 4
    while border_d != 2:
        tile = rotate(tile)
        border_d = (border_d + 1) % 4
    adjusted_tiles[0][0] = tile

    for tile, prev_x, prev_y in queue:
        if prev_x == 0 and prev_y == 0:  # start
            if (prev_x, prev_y + 1) not in done_coords:
                x = prev_x
                y = prev_y + 1
            else:
                x = prev_x + 1
                y = prev_y
        elif prev_x == 0 or prev_x == width - 1:  # top or bottom edge
            if (tile in edges or tile in corners) and prev_y != width - 1:
                x = prev_x
                y = prev_y + 1
            else:
                x = prev_x + 1
                y = prev_y
        elif tile in edges or tile in corners:  # left or right edge
            if prev_y == width - 2:
                x = prev_x
                y = prev_y + 1
            else:
                x = prev_x + 1
                y = prev_y
        else:  # inner
            if layout[prev_x - 1][prev_y + 1] in matches[tile]:
                x = prev_x
                y = prev_y + 1
            else:
                x = prev_x + 1
                y = prev_y
        
        layout[x][y] = tile
        done.add(tile)
        done_coords.add((x, y))

        # do the rotation/flips to adjust the new tile correctly
        prev_tile = adjusted_tiles[prev_x][prev_y]
        curr_tile = tiles[tile]
        if prev_x + 1 == x:  # compare to last row of upper tile
            for _ in range(4):
                if curr_tile[0] == prev_tile[-1]:
                    break
                curr_tile = flip(curr_tile)
                if curr_tile[0] == prev_tile[-1]:
                    break
                curr_tile = rotate(flip(curr_tile))
            adjusted_tiles[x][y] = curr_tile
        else:  # compare to right edge of left tile
            right = "".join(row[-1] for row in prev_tile)
            for _ in range(4):
                if "".join(row[0] for row in curr_tile) == right:
                    break
                curr_tile = flip(curr_tile)
                if "".join(row[0] for row in curr_tile) == right:
                    break
                curr_tile = rotate(flip(curr_tile))
            adjusted_tiles[x][y] = curr_tile

        for match in matches[tile]:
            if match not in done:
                done.add(match)
                queue.append((match, x, y))
    for i, row in enumerate(adjusted_tiles):
        for j, tile in enumerate(row):
            adjusted_tiles[i][j] = [row[1:-1] for row in tile[1:-1]]
    image = []
    for row in adjusted_tiles:
        for total_row in zip(*row):
            image.append("".join(total_row))
    return image


def find_monsters(image):
    total_pos = set()
    for x in range(len(image) - len(seamonster) + 1):
        for y in range(len(image[0]) - len(seamonster[0]) + 1):
            match = True
            pos = set()
            for px in range(len(seamonster)):
                if not match:
                    break
                for py in range(len(seamonster[0])):
                    if seamonster[px][py] == "#":
                        if image[x + px][y + py] != "#":
                            match = False
                            break
                        else:
                            pos.add((x + px, y + py))
            if match:
                total_pos |= pos
    return total_pos


def part2(tiles):
    matches, border_matches = get_neighbors(tiles)
    image = get_layout(matches, tiles, border_matches)
    res = 0
    for _ in range(4):
        pos = find_monsters(image)
        if len(pos):
            res = sum(
                1 for i in range(len(image)) for j in range(len(image[0])) if image[i][j] == "#" and (i, j) not in pos
            )
            # print("\n".join(image))
            break
        image = flip(image)
        pos = find_monsters(image)
        if len(pos):
            res = sum(
                1 for i in range(len(image)) for j in range(len(image[0])) if image[i][j] == "#" and (i, j) not in pos
            )
            # print("\n".join(image))
            break
        image = rotate(flip(image))
    return res


test = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""


data = get_and_write_data(20, 2020)
tiles = parse(data)
seamonster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".splitlines()
print_output(part1(tiles), part2(tiles))
