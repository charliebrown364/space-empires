import sys
sys.path.append('level_0_0')
from game import *
from random_player import *
from custom_player import *

players = [RandomPlayer(), CustomPlayer()]
game = Game(players)

print("\ngame.game_state before any turns:", game.game_state)

"""
assert game.game_state == {
    'turn': 1,
    'board_size': [7,7],
    'players': {
        1: {
            'scout_coords': (4, 1),
            'home_colony_coords': (4, 1)
        },
        2: {
            'scout_coords': (4, 7),
            'home_colony_coords': (4, 7)
        }
    },
    'winner': None
}
"""

game.complete_turn()
print("\ngame.game_state after 1 turn:", game.game_state)

"""
assert game.game_state == {
    'turn': 2,
    'board_size': [7,7],
    'players': {
        1: {
            'scout_coords': (will vary),
            'home_colony_coords': (4, 1)
        },
        2: {
            'scout_coords': (4, 6),
            'home_colony_coords': (4, 7)
        }
    },
    'winner': None
}
"""

game.run_to_completion()
print("\ngame.game_state after completion:", game.game_state)

"""
assert game.game_state == {
    'turn': 7,
    'board_size': [7,7],
    'players': {
        1: {
            'scout_coords': (will vary),
            'home_colony_coords': (4, 1)
        },
        2: {
            'scout_coords': (4, 1),
            'home_colony_coords': (4, 7)
        }
    },
    'winner': 2
}

print("passed level_0_0")
"""