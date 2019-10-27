from enum import Enum
from constants import Constants
from game import Game
from copy import copy


class Cell(Enum):
    empty = 0
    white = 1
    black = 2
    white_king = 3
    black_king = 4

    def to_king(self):
        if self == Cell.white:
            return Cell.white_king
        if self == Cell.black:
            return Cell.black_king
        return self

    def kill(self):
        return Cell.empty

    @staticmethod
    def is_empty(x):
        return x == 0

    def __str__(self):
        if self == Cell.empty:
            return '.'
        if self == Cell.white:
            return 'o'
        if self == Cell.white_king:
            return 'O'
        if self == Cell.black:
            return 'x'
        if self == Cell.black_king:
            return 'X'


# TODO kings actions
class MyGame(Game):
    def __init__(self):
        self.size = Constants.size
        #
        self.field = [[Cell.empty for _ in range(self.size)] for _ in range(self.size)]

    def start(self):
        self.field = copy(Constants.field)

    def clone(self):
        game = MyGame()
        game.field = copy(self.field)
        game.size = self.size
        return game

    def _cell(self, coords):
        return self.field[coords[0]][coords[1]]

    def _set(self, coords, value):
        self.field[coords[0]][coords[1]] = value

    def _get_all_possible_attacks(self, coords, up, down, left, right, is_opponent):
        attacks = []
        for vert, aside in [(up, left), (up, right), (down, left), (down, right)]:
            move = lambda x: vert(aside(x))
            if is_opponent(self._cell(move(coords))) and Cell.is_empty(self._cell(move(move(coords)))):
                current_position = move(move(coords))
                game = self.clone()
                game.field[move(coords)[0]][move(coords)[1]] = Cell.empty
                game.field[move(move(coords))[0]][move(move(coords))[1]] = Cell.empty
                for attacks_future in game._get_all_possible_attacks(current_position, up, down, left, right, is_opponent):
                    attacks.append(current_position + copy(attacks_future))

        return attacks

    def _get_actions_for_checker(self, coords, player):
        actions = []
        if player == 0:
            if self._cell(coords) != Cell.white_king and self._cell(coords) != Cell.white:
                return []
            down = lambda coords: (coords[0] + 1, coords[1])
            up = lambda coords: (coords[0] - 1, coords[1])
            left = lambda coords: (coords[0], coords[1] + 1)
            right = lambda coords: (coords[0], coords[1] - 1)
            is_opponent = lambda x: x == 4 or x == 2
        else:
            if self._cell(coords) != Cell.black_king and self._cell(coords) != Cell.black:
                return []
            down = lambda coords: (coords[0] - 1, coords[1])
            up = lambda coords: (coords[0] + 1, coords[1])
            left = lambda coords: (coords[0], coords[1] - 1)
            right = lambda coords: (coords[0], coords[1] + 1)
            is_opponent = lambda x: x == 3 or x == 1

        for up, aside in [(up, left), (up, right)]:
            if Cell.is_empty(self._cell(up(aside(coords)))):
                actions.append((coords, up(aside(coords))))

        actions += self._get_all_possible_attacks(coords, up, down, left, right, is_opponent)

        return actions

    def get_valid_moves(self, player):
        actions = []
        for i in range(self.size):
            for j in range(self.size):
                actions += self._get_actions_for_checker((i, j), player)

        return actions

    def check_game_over(self, player):
        return len(self.get_valid_moves(1 - player)) == 0

    def print_board(self):
        for x in range(self.size):
            print(' '.join(str(e) for e in self.field[x]))

    # TODO
    def play_action(self, action):
        pass

