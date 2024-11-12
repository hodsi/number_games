from copy import deepcopy
from typing import Iterable

import numpy

from possible_number import PossibleNumber


class SumsBoard:
    def __init__(self, columns_sums: list[int], rows_sums: list[int], board_numbers: list[list[int]]) -> None:
        if len(rows_sums) != len(board_numbers):
            raise ValueError(
                f"The length of the rows sums ({len(rows_sums)}) "
                f"must be the same as the length of the board ({len(board_numbers)})"
            )
        for i, row in enumerate(board_numbers):
            if len(columns_sums) != len(row):
                raise ValueError(
                    f"The length of the rows must be the length of the columns sum ({rows_sums}). "
                    f"But row {i} length is {len(row)}"
                )
        self._columns_sums = deepcopy(columns_sums)
        self._rows_sums = deepcopy(rows_sums)
        self._board = numpy.array(
            [[PossibleNumber(number, None) for number in row] for row in board_numbers], PossibleNumber
        )

    @classmethod
    def _sum_check(cls, axis: Iterable[PossibleNumber], axis_sum: int, accurate: bool) -> bool:
        if accurate:
            return sum(n.accurate_value for n in axis) == axis_sum
        else:
            return sum(n.value for n in axis) >= axis_sum

    def columns_check(self, accurate: bool = False) -> bool:
        for i, column_sum in enumerate(self._columns_sums):
            column: Iterable[PossibleNumber] = self._board[:, i]
            if not self._sum_check(column, column_sum, accurate):
                return False
        return True

    def rows_check(self, accurate: bool = False) -> bool:
        for i, row_sum in enumerate(self._rows_sums):
            row: Iterable[PossibleNumber] = self._board[i]
            if not self._sum_check(row, row_sum, accurate):
                return False
        return True

    def board_check(self, accurate: bool = False) -> bool:
        return self.rows_check(accurate) and self.columns_check(accurate)

    @classmethod
    def _get_axis_possibilities(cls, axis: list[PossibleNumber], axis_sum: int) -> list[list[PossibleNumber]]:
        if axis_sum < 0:
            return []
        if len(axis) == 1:
            if axis[0].value == axis_sum:
                return [[axis[0].get_signed_number(True)]]
            if axis_sum == 0:
                return [[axis[0].get_signed_number(False)]]
            return []
        if cls._sum_check(axis, axis_sum, True):
            return [[number if number.signed else number.get_signed_number(False) for number in axis]]
        if not cls._sum_check(axis, axis_sum, False):
            return []

        return [
            *[
                [axis[0].get_signed_number(True), *possibilities]
                for possibilities in cls._get_axis_possibilities(axis[1:], axis_sum - axis[0].value)
            ],
            *[
                [axis[0].get_signed_number(False), *possibilities]
                for possibilities in cls._get_axis_possibilities(axis[1:], axis_sum)
            ],
        ]

    def fill_sure_signs(self) -> bool:
        did_fill_sign = False
        rows_possibilities = [
            self._get_axis_possibilities(row, row_sum) for row, row_sum in zip(self._board, self._rows_sums)
        ]
        columns_possibilities = [
            self._get_axis_possibilities(column, column_sum)
            for column, column_sum in zip(self._board.T, self._columns_sums)
        ]

        for i, row in enumerate(self._board):
            for j, number in enumerate(row):
                if number.signed:
                    continue
                number_possibilities: set[PossibleNumber] = {
                    row_possibility[j] for row_possibility in rows_possibilities[i]
                } & {column_possibility[i] for column_possibility in columns_possibilities[j]}

                if len(number_possibilities) == 1 and (possibility := number_possibilities.pop()).signed:
                    did_fill_sign = True
                    number.set_sign(possibility.sign)

        return did_fill_sign

    def try_solve(self) -> bool:
        while self.fill_sure_signs():
            pass
        return self.board_check(True)

    def solve(self) -> bool:
        if self.try_solve():
            return True

        for i, row in enumerate(self._board):
            for j, number in enumerate(row):
                if not number.signed:
                    dup_board = deepcopy(self)
                    dup_board._board[i, j].set_sign(True)
                    if dup_board.solve():
                        self._board = dup_board._board
                        return True
                    dup_board = deepcopy(self)
                    dup_board._board[i, j].set_sign(False)
                    if dup_board.solve():
                        self._board = dup_board._board
                        return True
                    return False
        return False

    def __str__(self) -> str:
        return "\n".join(" ".join(str(number.value) if number.sign else "·" for number in row) for row in self._board)
