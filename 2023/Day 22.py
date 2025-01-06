from collections import defaultdict
from utils.data import *


def str_to_ints(strs):
	return list(map(int, strs))


def parse(data):
	res = []
	for line in data.splitlines():
		frm, to = line.split("~")
		res.append((str_to_ints(frm.split(",")), str_to_ints(to.split(","))))
	return sorted(res, key=lambda x: x[0][2])


def check_disintegrate(bricks):
	highest_z = defaultdict(lambda: (0, -1))  # store pair of (highest z_coordinate, brick index) for all (x,y) coordinates
	necessary = set()  # store brick indices which can't be "safely" disintegrated
	graph = [[] for _ in range(len(bricks))]  # for part 2: store for each brick index, which other bricks it supports
	for i, ((x_from, y_from, z_from), (x_to, y_to, z_to)) in enumerate(bricks):
		max_height = -1
		support = set()
		for x in range(x_from, x_to + 1):
			for y in range(y_from, y_to + 1):
				z = highest_z[(x, y)]
				if z[0] + 1 > max_height:
					max_height = z[0] + 1
					support = {z[1]}
				elif z[0] + 1 == max_height:
					support.add(z[1])

		for idx in support:
			if idx != -1:
				graph[idx].append(i)

		if len(support) == 1:  # brick only resting on a single other brick --> other brick can't be safely disintegrated
			necessary.add(support.pop())

		z_diff = z_from - max_height
		if z_diff > 0:
			z_to -= z_diff

		for x in range(x_from, x_to + 1):
			for y in range(y_from, y_to + 1):
				highest_z[(x, y)] = (z_to, i)

	return necessary - {-1}, graph  # remove ground brick with index -1 from the necessary bricks


def part1(bricks, necessary):
	return len(bricks) - len(necessary)


def part2(graph):
	res = 0

	#  count how many other bricks a certain brick is supported by
	indegrees = [0 for _ in range(len(graph))]
	for supported in graph:
		for idx in supported:
			indegrees[idx] += 1

	for i in range(len(graph)):  # check all bricks
		tmp = indegrees[:]
		queue = [i]
		count = -1
		while queue:
			count += 1
			nxt = queue.pop()
			for idx in graph[nxt]:
				tmp[idx] -= 1
				if tmp[idx] == 0:  # check if a supported brick has no more supporting bricks after removing the current one
					queue.append(idx)
		res += count
	return res


data = get_and_write_data(22, 2023)
bricks = parse(data)
necessary, graph = check_disintegrate(bricks)
print_output(part1(bricks, necessary), part2(graph))
