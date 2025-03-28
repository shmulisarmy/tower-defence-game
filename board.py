from functools import cache
from typing import Iterable


board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 6, 7, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 8, 0, 0, 0, 0, 0],
[1, 2, 3, 0, 9, 10, 11, 12, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 13, 0, 0],
[0, 0, 19, 18, 17, 16, 15, 14, 0, 0],
[0, 0, 20, 0, 0, 0, 0, 0, 0, 0]
]


def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < len(board) and 0 <= col < len(board[0])


def get_neighbors(row: int, col: int) -> Iterable[tuple[int, int]]:
    for i in range(-1, 1+1):
        for j in range(-1, 1+1):
            if i == 0 and j == 0:
                continue
            if in_bounds(row + i, col + j):
                yield (row + i, col + j)


@cache 
def get_next_position(row: int, col: int) -> tuple[int, int] | None:
    for neighbor in get_neighbors(row, col):
        if board[neighbor[0]][neighbor[1]] == board[row][col] + 1:
            return neighbor
    return None

