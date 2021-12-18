from __future__ import annotations

from typing import IO

import attr
import numpy as np


@attr.frozen
class Bingo:
    numbers: list[int]
    boards: np.ndarray[int]

    @classmethod
    def from_input(cls, input_path: str) -> np.ndarray[int]:
        with open(input_path) as f:

            # Read in the numbers
            numbers = [int(x) for x in f.readline().strip().split(",")]

            # Check for an empty line separating the boards.
            # If it's there read in a board, otherwise, we're done
            boards = []
            while f.readline():

                # Grab the next 5 lines to make a board
                boards.append(_single_bingo_array(f))

        # Stack all the boards in to a high dimensional array.
        return cls(numbers, np.dstack(boards))

    @property
    def num_boards(self) -> int:
        return self.boards.shape[-1]


def _single_bingo_array(f: IO) -> np.ndarray[int]:
    return np.array([[int(x) for x in next(f).strip().split()] for _ in range(5)])


def find_first_winner_score(bingo: Bingo) -> int:

    # Make a mask of what's been called in all the boards;
    # i.e. an all false mask to start
    called_boards = np.zeros(bingo.boards.shape, dtype=bool)

    # Iterate through the numbers and update the mask as we go.
    # If we find a bingo stop and grab the winning board.
    for num in bingo.numbers:

        # Update the called boards with the new number
        called_boards += bingo.boards == num

        # Sum the rows and columns to see if we have a bingo
        column_scores = called_boards.sum(axis=0)
        row_scores = called_boards.sum(axis=1)

        # Looking for a score of 5, which means bingo
        column_bingo = np.argwhere(column_scores == 5)
        row_bingo = np.argwhere(row_scores == 5)

        # If we actually found one
        if (column_winner := column_bingo.size > 0) or (
            row_winner := row_bingo.size > 0
        ):
            if column_winner:
                assert column_bingo.shape[0] == 1, "expected 1 column winner"
                assert not row_winner, "expected just column winner"
                winning_board_num = column_bingo[0][1]

            if row_winner:
                assert row_bingo.shape[0] == 1, "expected 1 row winner"
                assert not column_winner, "expected just row winner"
                winning_board_num = row_bingo[0][1]

            break

    # Using the winning board mask we can figure out the sum of the uncalled numbers.
    uncalled_sum = bingo.boards[:, :, winning_board_num][
        ~called_boards[:, :, winning_board_num]
    ].sum()

    # And lastly we multiply that sum by the last called number
    return uncalled_sum * num


def find_last_winner_score(bingo: Bingo) -> int:

    # Make a mask of what's been called in all the boards;
    # i.e. an all false mask to start
    called_boards = np.zeros(bingo.boards.shape, dtype=bool)

    # Let's make a data structure for holding the winners
    winners = set()

    # Iterate through the numbers and update the mask as we go.
    # Go until we find the last board's first bingo stop and grab that board.
    for num in bingo.numbers:

        # Update the called boards with the new number
        called_boards += bingo.boards == num

        # Sum the rows and columns to see if we have a bingo
        column_scores = called_boards.sum(axis=0)
        row_scores = called_boards.sum(axis=1)

        # Figure out which boards have column and/or row winners
        has_column_winners = set(np.argwhere(column_scores == 5)[:, 1])
        has_row_winners = set(np.argwhere(row_scores == 5)[:, 1])

        # Remember all current winners
        current_winners = has_column_winners | has_row_winners

        # Skip ahead if we haven't found any winners yet
        if not current_winners:
            continue

        # Check to see if everyone has won
        if len(winners) < bingo.num_boards:

            # Who are the new winners?
            new_winners = current_winners - winners

            # print(winners, new_winners)

            # If we just found the last winner let's quit
            if len(winners | new_winners) == bingo.num_boards:
                winning_board_num = next(iter(new_winners))
                break
            # Otherwise update the winners and move along
            else:
                winners |= new_winners

    # Using the winning board mask we can figure out the sum of the uncalled numbers.
    uncalled_sum = bingo.boards[:, :, winning_board_num][
        ~called_boards[:, :, winning_board_num]
    ].sum()

    # And lastly we multiply that sum by the last called number
    return uncalled_sum * num
