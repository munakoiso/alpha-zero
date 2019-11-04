from enum import Enum
from constants import Constants
from game import Game
from copy import deepcopy


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

    def is_king(self):
        return self == Cell.black_king or self == Cell.white_king

    @staticmethod
    def is_empty(x):
        return x.value == 0

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

    def set_field(self, field):
        self.field = deepcopy(field)

    def start(self):
        self.field = deepcopy(Constants.field)

    def set_to_king_if_possible(self, current_pos):
        self.set(current_pos, self.get(current_pos).to_king(current_pos[0], self.size))

    def clone(self):
        game = MyGame()
        game.set_field(self.field)
        game.size = self.size
        return game

    def get(self, coords):
        return self.field[coords[0]][coords[1]]

    def set(self, coords, value):
        self.field[coords[0]][coords[1]] = value

    def is_on_field(self, point):
        return 0 <= point[0] < self.size and 0 <= point[1] < self.size

    # check line from <frm> exclude to <to> include
    def is_line_empty(self, frm, to, include_frm, include_to):
        if not self.is_on_field(frm) or not self.is_on_field(to):
            return False
        for coords in zip([x for x in range(frm[0], to[0] + sign(- frm[0] + to[0]), sign(- frm[0] + to[0]))],
                          [y for y in range(frm[1], to[1] + sign(- frm[1] + to[1]), sign(- frm[1] + to[1]))]):
            if coords == frm and not include_frm:
                continue
            if coords == to and not include_to:
                continue
            if not Cell.is_empty(self.get(coords)):
                return False
        return True

    def get_attacks_for_checker(self, coords, up, down, left, right, is_opponent):
        attacks = set()
        max_dist = 2
        if self.get(coords).is_king():
            max_dist = self.size
        for vert, aside in self.get_possible_directions_for_checker(coords, up, down, left, right, True):
            move = lambda x: vert(aside(x))
            for dist_to_opp_pos in range(1, max_dist):
                for dist_to_finish_pos in range(dist_to_opp_pos + 1, max_dist + 1):
                    # x in coords . . . opp_pos . . . finish_pos
                    opp_pos = coords
                    for _ in range(dist_to_opp_pos):
                        opp_pos = move(opp_pos)
                    finish_pos = coords
                    for _ in range(dist_to_finish_pos):
                        finish_pos = move(finish_pos)
                    if self.is_on_field(finish_pos) and \
                            is_opponent(self.get(opp_pos)) and \
                            self.is_line_empty(coords, opp_pos, False, False) and \
                            self.is_line_empty(opp_pos, finish_pos, False, True):
                        current_pos = coords
                        game = self.clone()
                        game.play_action((1, (current_pos, finish_pos)))
                        attacks.add(((current_pos, finish_pos), ))
                        for future_attack in game.get_attacks_for_checker(finish_pos,
                                                                          up,
                                                                          down,
                                                                          left,
                                                                          right,
                                                                          is_opponent):
                            current_attack = [(current_pos, finish_pos)] + list(deepcopy(future_attack))
                            attacks.add(tuple(current_attack))

        return attacks

    def get_possible_directions_for_checker(self, coords, up, down, left, right, is_attack):
        if self.get(coords).is_king() or is_attack:
            return [(up, left), (up, right), (down, left), (down, right)]
        else:
            return [(up, left), (up, right)]

    def get_moves_for_checker(self, coords, up, down, left, right):
        max_dist = 1
        actions = set()
        if self.get(coords).is_king():
            max_dist = self.size
        for vert, aside in self.get_possible_directions_for_checker(coords, up, down, left, right, False):
            moved_to = coords
            for dist in range(max_dist):
                moved_to = vert(aside(moved_to))
                if self.is_line_empty(coords, moved_to, False, True):
                    actions.add((coords, moved_to))
                else:
                    break
        return actions

    def get_actions_for_checker(self, coords, player):
        if player == 0:
            if self.get(coords) != Cell.white_king and self.get(coords) != Cell.white:
                return []
            up, down, left, right, is_opponent = Constants.white_moves
        else:
            if self.get(coords) != Cell.black_king and self.get(coords) != Cell.black:
                return []
            up, down, left, right, is_opponent = Constants.black_moves

        actions = self.get_moves_for_checker(coords, up, down, left, right)

        for attack in self.get_attacks_for_checker(coords, up, down, left, right, is_opponent):
            actions.add(tuple([coords] + [e[1] for e in attack]))
        return list(actions)

    def get_valid_moves(self, player):
        actions = []
        for i in range(self.size):
            for j in range(self.size):
                act_for_checker = self.get_actions_for_checker((i, j), player)
                actions += [(1, e) for e in act_for_checker]

        # just one "not valid" move
        if len(actions) == 0:
            return [(0, )]
        return actions

    def check_game_over(self, player):
        # current player lost only if there is no possible actions for another player
        # current player wins only if there is no actions for current player at the NEXT STEP
        # (after any of another player's moves)
        actions_count = len(self.get_valid_moves(1 - player))
        if actions_count == 0:
            return True, -1
        return False, 0

    def print_board(self):
        print()
        for x in range(self.size):
            print(' '.join(str(e) for e in self.field[x]))
        print()

    def play_action(self, action):
        if action[0] == 0:
            return
        action_copy = action[1]
        current_pos = action_copy[0]
        cell_type = self.get(current_pos)
        for i in range(1, len(action_copy)):
            cell_type = cell_type.to_king(action_copy[i][0], self.size)
            for coords in zip([x for x in range(current_pos[0], action_copy[i][0] + sign(action_copy[i][0] - current_pos[0]),
                                                sign(action_copy[i][0] - current_pos[0]))],
                              [y for y in range(current_pos[1], action_copy[i][1] + sign(action_copy[i][1] - current_pos[1]),
                                                sign(action_copy[i][1] - current_pos[1]))]):
                self.set(coords, Cell.empty)
            current_pos = action_copy[i]
        cell_type = cell_type.to_king(action_copy[len(action_copy) - 1][0], self.size)
        self.set(current_pos, cell_type)

    def __eq__(self, other):
        if self.size != other.size:
            return False
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] != other.field[i][j]:
                    return False
        return True
