# queens.py
#
# ICS 33 Fall 2025
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self



Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'



class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position


    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'



class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position


    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'



class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    def __init__(self, rows: int, columns: int, queens: tuple[Position, ...] | None = None) -> None:
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        if not isinstance(rows, int) or not isinstance(columns, int) or rows <= 0 or columns <= 0:
            raise ValueError("rows and columns must be positive integers")
        self._rows = rows
        self._columns = columns
        self._queens: tuple[Position, ...] = tuple(queens) if queens is not None else tuple()

        seen = set()
        for q in self._queens:
            self._check_in_bounds(q)
            if q in seen:
                raise DuplicateQueenError(q)
            seen.add(q)

    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        return len(self._queens)


    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        return list(self._queens)


    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        return position in self._queens


    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""
        qs = self.queens()
        for i in range(len(qs)):
            q1 = qs[i]
            for j in range(i + 1, len(qs)):
                q2 = qs[j]
                same_rows = q1.row == q2.row
                same_columns = q1.column == q2.column
                same_diags = abs(q1.row - q2.row) == abs(q1.column - q2.column)
                if same_rows or same_columns or same_diags:
                    return True
        return False


    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions,
        without modifying 'self' in any way.  Raises a DuplicateQueenError when
        there is already a queen in at least one of the given positions."""
        current = set(self._queens)
        for q in positions:
            self._check_in_bounds(q)
            if q in current:
                raise DuplicateQueenError(q)
            current.add(q)
        return QueensState(self._rows, self._columns, tuple(sorted(current)))


    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions,
        without modifying 'self' in any way.  Raises a MissingQueenError when there
        is no queen in at least one of the given positions."""
        current = set(self._queens)
        for q in positions:
            if q not in current:
                raise MissingQueenError(q)
            current.remove(q)
        return QueensState(self._rows, self._columns, tuple(sorted(current)))

    def _check_in_bounds(self, p: Position) -> None:
        if not (0 <= p.row < self._rows and 0 <= p.column < self._columns):
            raise ValueError(f"position out of bounds: ({p.row}, {p.column})")
