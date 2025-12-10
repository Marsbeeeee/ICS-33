# test_queens.py
#
# ICS 33 Fall 2025
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_queen_count_is_zero_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import QueensState, Position, DuplicateQueenError, MissingQueenError
import unittest



class TestQueensState(unittest.TestCase):
    def test_queen_count_is_zero_initially(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test_init_invalid_rows_cols(self):
        with self.assertRaises(ValueError):
            QueensState(0, 8)
        with self.assertRaises(ValueError):
            QueensState(8, 0)
        with self.assertRaises(ValueError):
            QueensState(-1, 8)
        with self.assertRaises(ValueError):
            QueensState(8, -1)
        with self.assertRaises(ValueError):
            QueensState(7.5, 8)

    def test_init_with_queens_duplicate_or_oob(self):
        q = Position(1, 1)
        with self.assertRaises(DuplicateQueenError):
            QueensState(4, 4, queens = (q, q))
        with self.assertRaises(ValueError):
            QueensState(4, 4, queens = (Position(5, 0),))

    def test_queens_returns_list_copy(self):
        s = QueensState(4, 4)
        t = s.with_queens_added([Position(0, 0)])
        qs = t.queens()
        self.assertIsInstance(qs, list)
        qs.clear()
        self.assertEqual(t.queen_count(), 1)

    def test_has_queen_true_and_false(self):
        s = QueensState(4, 4)
        pos = Position(2, 3)
        t = s.with_queens_added([pos])
        self.assertFalse(s.has_queen(pos))
        self.assertTrue(t.has_queen(pos))

    def test_add_and_remove_are_immutable(self):
        s = QueensState(4, 4)
        pos = Position(1, 2)
        t = s.with_queens_added([pos])
        self.assertEqual(s.queen_count(), 0)
        self.assertEqual(t.queen_count(), 1)
        u = t.with_queens_removed([pos])
        self.assertEqual(t.queen_count(), 1)
        self.assertEqual(u.queen_count(), 0)

    def test_with_queens_added_duplicate_raises_and_message(self):
        pos = Position(0, 1)
        s = QueensState(4, 4).with_queens_added([pos])
        with self.assertRaises(DuplicateQueenError) as ctx:
            s.with_queens_added([pos])
        self.assertEqual(str(ctx.exception),
                         f'duplicate queen in row {pos.row} column {pos.column}')

    def test_with_queens_added_oob_raises(self):
        s = QueensState(4, 4)
        with self.assertRaises(ValueError):
            s.with_queens_added([Position(4, 0)])
        with self.assertRaises(ValueError):
            s.with_queens_added([Position(0, 4)])
        with self.assertRaises(ValueError):
            s.with_queens_added([Position(-1, 0)])

    def test_with_queens_removed_missing_raises_and_message(self):
        s = QueensState(4, 4)
        pos = Position(3, 3)
        with self.assertRaises(MissingQueenError) as ctx:
            s.with_queens_removed([pos])
        self.assertEqual(str(ctx.exception), f'missing queen in row {pos.row} column {pos.column}')

    def test_with_queens_removed_multiple(self):
        s = QueensState(4, 4).with_queens_added([Position(0, 0), Position(1, 1), Position(2, 2)])
        t = s.with_queens_removed([Position(0, 0), Position(2, 2)])
        self.assertTrue(t.has_queen(Position(1, 1)))
        self.assertFalse(t.has_queen(Position(0, 0)))
        self.assertFalse(t.has_queen(Position(2, 2)))

if __name__ == '__main__':
    unittest.main()
