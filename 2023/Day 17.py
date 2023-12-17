from utils.data import *
from heapq import heappop, heappush


def parse(data):
	return list(map(lambda x: list(map(int, x)), data.splitlines()))


def in_bounds(row, col, max_row, max_col):
	return 0 <= row < max_row and 0 <= col < max_col


def solve(grid, min_dist, max_dist):
	heap = [(0, 0, 0, -1)]
	seen = set()
	costs = {}
	n, m = len(grid), len(grid[0])
	dr = [0, 1, 0, -1]
	dc = [1, 0, -1, 0]
	while heap:
		cost, row, col, direction = heappop(heap)  # lowest cost position next
		if row == n - 1 and col == m - 1:  # target reached
			return cost
		if (row, col, direction) not in seen:
			seen.add((row, col, direction))
			for new_direction in range(4):
				additional_cost = 0
				if direction == new_direction or (new_direction + 2) % 4 == direction:
					# can't continue in this direction (no 180 degree turns)
					continue
				for distance in range(1, max_dist + 1):
					new_row = row + dr[new_direction] * distance
					new_col = col + dc[new_direction] * distance
					if not in_bounds(new_row, new_col, n, m):  # can't move further in this direction
						break
					additional_cost += grid[new_row][new_col]
					if distance >= min_dist:
						new_cost = cost + additional_cost
						if costs.get((new_row, new_col, new_direction), float("inf")) > new_cost:
							costs[(new_row, new_col, new_direction)] = new_cost
							heappush(heap, (new_cost, new_row, new_col, new_direction))


def part1(grid):
	return solve(grid, 1, 3)


def part2(grid):
	return solve(grid, 4, 10)


data = get_and_write_data(17, 2023)
grid = parse(data)
print_output(part1(grid), part2(grid))