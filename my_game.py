from enum import Enum
from constants import Constants
from game import Game
from copy import copy


def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


class Cell(Enum):
    empty = 0
    white = 1
    black = 2
    white_king = 3
    black_king = 4

    def to_king(self, line, size):
        if self == Cell.white and line == 0:
            return Cell.white_king
        if self == Cell.black and line == size - 1:
            return Cell.black_king
        return self

    def kill(self):
        return Cell.empty

    def is_king(self):
        return self == Cell.black_king or self == Cell.white_king

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


class MyGame(Game):
    def __init__(self):
        self.size = Constants.size
        #
        self.field = [[Cell.empty for _ in range(self.size)] for _ in range(self.size)]

    def start(self):
        self.field = copy(Constants.field)

    def set_to_king_if_possible(self, current_pos):
        self._set(current_pos, self._get(current_pos).to_king(current_pos[1], self.size))

    def clone(self):
        game = MyGame()
        game.field = copy(self.field)
        game.size = self.size
        return game

    def _get(self, coords):
        return self.field[coords[0]][coords[1]]

    def _set(self, coords, value):
        self.field[coords[0]][coords[1]] = value

    def _is_on_field(self, point):
        return 0 <= point[0] < self.size and  0 <= point[1] < self.size

    # check line from <frm> exclude to <to> include
    def _is_line_empty(self, frm, to, include_frm, include_to):
        if not self._is_on_field(frm) or not self._is_on_field(to):
            return False
        for coords in zip([x for x in range(frm[0], to[0], sign(frm[0] - to[0]))],
                          [y for y in range(frm[1], to[1], sign(frm[1] - to[1]))]):
            if coords == frm and not include_frm:
                continue
            if coords == to and not include_to:
                continue
            if not Cell.is_empty(self._get(coords)):
                return False
        return True

    def _get_attacks_for_checker(self, coords, up, down, left, right, is_opponent):
        attacks = set()
        max_dist = 2
        if self._get(coords).is_king():
            max_dist = self.size
        for vert, aside in [(up, left), (up, right), (down, left), (down, right)]:
            move = lambda x: vert(aside(x))
            for dist_to_opp_pos in range(1, max_dist):
                for dist_to_finish_pos in range(dist_to_opp_pos + 1, max_dist + 1):
                    # x in coords . . . opp_pos . . . finish_pos
                    opp_pos = coords
                    for _ in range(dist_to_opp_pos - 1):
                        opp_pos = move(opp_pos)
                    finish_pos = coords
                    for _ in range(dist_to_finish_pos - 1):
                        finish_pos = move(finish_pos)

                    if is_opponent(self._get(move(opp_pos))) and \
                            self._is_line_empty(coords, opp_pos, False, False) and \
                            self._is_line_empty(opp_pos, finish_pos, False, True):
                        current_pos = coords
                        game = self.clone()
                        for _ in range(dist_to_finish_pos):
                            x = self._get(current_pos)
                            self._set(current_pos, Cell.empty)
                            current_pos = move(current_pos)
                            self._set(current_pos, x)
                        self.set_to_king_if_possible(current_pos)
                        for attacks_future in game._get_attacks_for_checker(current_pos,
                                                                            up,
                                                                            down,
                                                                            left,
                                                                            right,
                                                                            is_opponent):
                            attacks.add(tuple(current_pos + list(copy(attacks_future))))
        return attacks

    def _get_moves_for_checker(self, coords, up, down, left, right):
        max_dist = 1
        actions = set()
        if self._get(coords).is_king():
            max_dist = self.size
        for vert, aside in [(up, left), (up, right), (down, left), (down, right)]:
            moved_to = coords
            for dist in range(max_dist):
                moved_to = vert(aside(moved_to))
                if self._is_line_empty(coords, moved_to, False, True):
                    actions.add((coords, moved_to))
                else:
                    break
        return actions

    def _get_actions_for_checker(self, coords, player):
        actions = set()
        if player == 0:
            if self._get(coords) != Cell.white_king and self._get(coords) != Cell.white:
                return []
            down = lambda coords: (coords[0] + 1, coords[1])
            up = lambda coords: (coords[0] - 1, coords[1])
            left = lambda coords: (coords[0], coords[1] + 1)
            right = lambda coords: (coords[0], coords[1] - 1)
            is_opponent = lambda x: x == 4 or x == 2
        else:
            if self._get(coords) != Cell.black_king and self._get(coords) != Cell.black:
                return []
            down = lambda coords: (coords[0] - 1, coords[1])
            up = lambda coords: (coords[0] + 1, coords[1])
            left = lambda coords: (coords[0], coords[1] - 1)
            right = lambda coords: (coords[0], coords[1] + 1)
            is_opponent = lambda x: x == 3 or x == 1

        actions += self._get_moves_for_checker(coords, up, down, left, right)

        for attack in self._get_attacks_for_checker(coords, up, down, left, right, is_opponent):
            for i in range(1, len(attack)):
                actions.add(copy(attack[:i]))
        return list(actions)

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

    def play_action(self, action):
        current_pos = action[0]
        cell_type = self._get(current_pos)
        for i in range(1, len(action)):
            cell_type = cell_type.to_king(action[i][1], self.size)
            for coords in zip([x for x in range(current_pos[0], action[i][0], sign(action[i][0] - current_pos[0]))],
                              [y for y in range(current_pos[1], action[i][1], sign(action[i][1] - current_pos[1]))]):
                self._set(coords, Cell.empty)
            current_pos = action[i]
        self._set(current_pos, cell_type)
