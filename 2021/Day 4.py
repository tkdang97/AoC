from utils.data import *
from copy import deepcopy


def parse(data):
    split = data.split("\n\n")
    draws = list(map(int, split[0].split(",")))
    boards = []
    for board in split[1:]:
        boards.append([list(map(int, line.split())) for line in board.splitlines()])
    return draws, boards


def is_winner(board):
    return (any(all(val == -1 for val in row) for row in board)
            or any(all(val == -1 for val in col) for col in zip(*board)))


def mark_board(board, draw):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == draw:
                board[i][j] = -1
                return


def unmarked_sum(board):
    return sum(num for row in board for num in row if num != -1)


def part1(draws, boards):
    tmp_boards = deepcopy(boards)
    for draw in draws:
        for board in tmp_boards:
            mark_board(board, draw)
            if is_winner(board):
                return unmarked_sum(board) * draw
    assert False


def part2(draws, boards):
    tmp_boards = deepcopy(boards)
    finished = set()
    for draw in draws:
        for i, board in enumerate(tmp_boards):
            if i not in finished:
                mark_board(board, draw)
                if is_winner(board):
                    if len(finished) == len(tmp_boards) - 1:
                        return unmarked_sum(board) * draw
                    finished.add(i)
    assert False


data = get_and_write_data(4, 2021)
info = parse(data)
print_output(part1(*info), part2(*info))
