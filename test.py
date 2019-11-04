import unittest
from my_game import MyGame, Cell
from constants import Constants


class TestGame(unittest.TestCase):
    def test_copy(self):
        game = MyGame()
        copy = game.clone()
        self.assertEqual(game, copy)
        copy.field[0][0] = Cell.black_king
        self.assertNotEqual(game, copy)

    def test_get_moves_one_checker(self):
        game = MyGame()
        game.field[1][1] = Cell.white
        up, down, left, right = Constants.white_moves[:4]
        self.assertEqual({((1, 1), (0, 2)), ((1, 1), (0, 0))}, game.get_moves_for_checker((1, 1), up, down, left, right))

    def test_is_line_empty(self):
        game = MyGame()
        game.set((2, 2), Cell.white)
        game.set((6, 6), Cell.white)
        self.assertFalse(game.is_line_empty((2, 2), (6, 6), True, True))
        self.assertFalse(game.is_line_empty((2, 2), (6, 6), False, True))
        self.assertFalse(game.is_line_empty((2, 2), (6, 6), True, False))
        self.assertTrue(game.is_line_empty((2, 2), (6, 6), False, False))

    def test_get_moves_one_king(self):
        game = MyGame()
        game.set((2, 2), Cell.white_king)
        up, down, left, right = Constants.white_moves[:4]
        self.assertEqual({((2, 2), (0, 0)),
                         ((2, 2), (0, 4)),
                         ((2, 2), (1, 1)),
                         ((2, 2), (1, 3)),
                         ((2, 2), (3, 1)),
                         ((2, 2), (3, 3)),
                         ((2, 2), (4, 0)),
                         ((2, 2), (4, 4)),
                         ((2, 2), (5, 5)),
                         ((2, 2), (6, 6)),
                         ((2, 2), (7, 7)),
                         ((2, 2), (8, 8))},
                         game.get_moves_for_checker((2, 2), up, down, left, right))

    def test_get_attacks_one_checker(self):
        game = MyGame()
        game.set((2, 2), Cell.white)
        game.set((1, 1), Cell.black)
        game.set((3, 1), Cell.black_king)
        game.set((1, 3), Cell.black)
        game.set((0, 4), Cell.black)
        game.set((3, 3), Cell.white)
        # game.print_board()

        up, down, left, right, is_opp = Constants.white_moves
        self.assertEqual({(((2, 2), (4, 0)),), (((2, 2), (0, 0)),)},
                         game.get_attacks_for_checker((2, 2), up, down, left, right, is_opp))

    def test_get_valid_moves(self):
        game = MyGame()
        game.set((2, 2), Cell.white)
        game.set((1, 1), Cell.black)
        game.set((3, 1), Cell.black_king)
        game.set((5, 1), Cell.black)
        # game.print_board()

        self.assertEqual([(1, ((2, 2), (4, 0), (6, 2))),
                         (1, ((2, 2), (1, 3))),
                         (1, ((2, 2), (4, 0))),
                         (1, ((2, 2), (0, 0)))],
                         game.get_valid_moves(0))

        game.set((2, 2), Cell.empty)
        game.set((0, 4), Cell.white_king)
        # game.print_board()

        self.assertEqual([(1, ((0, 4), (4, 0), (8, 4))),
                         (1, ((0, 4), (4, 0))),
                         (1, ((0, 4), (1, 5))),
                         (1, ((0, 4), (2, 2))),
                         (1, ((0, 4), (4, 0), (6, 2))),
                         (1, ((0, 4), (2, 6))),
                         (1, ((0, 4), (1, 3))),
                         (1, ((0, 4), (4, 0), (7, 3))),
                         (1, ((0, 4), (4, 8))),
                         (1, ((0, 4), (3, 7)))],
                         game.get_valid_moves(0))

    def test_play_action(self):
        game = MyGame()
        game.set((2, 2), Cell.white)
        game.set((1, 1), Cell.black)
        game.set((3, 1), Cell.black_king)
        game.set((5, 1), Cell.black)
        # game.print_board()
        new_game = game.clone()
        game.play_action((1, ((2, 2), (4, 0), (6, 2))))
        new_game.set((3, 1), Cell.empty)
        new_game.set((5, 1), Cell.empty)
        new_game.set((2, 2), Cell.empty)
        new_game.set((6, 2), Cell.white)

        # game.print_board()
        self.assertEqual(game, new_game)
