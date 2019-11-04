class Constants:
    size = 9
    field = [[0, 2, 0, 2, 0, 2, 0, 2],
             [2, 0, 2, 0, 2, 0, 2, 0],
             [0, 2, 0, 2, 0, 2, 0, 2],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0]
             ]

    empty_field = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]
                   ]
    # down, up, left, right, is_opp

    up = lambda coords: (coords[0] - 1, coords[1])
    down = lambda coords: (coords[0] + 1, coords[1])
    left = lambda coords: (coords[0], coords[1] + 1)
    right = lambda coords: (coords[0], coords[1] - 1)
    is_opponent = lambda x: x.value == 4 or x.value == 2

    white_moves = [up, down, left, right, is_opponent]
    is_opponent = lambda x: x.value == 3 or x.value == 1
    black_moves = [down, up, right, left, is_opponent]