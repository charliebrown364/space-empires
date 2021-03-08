import sys
sys.path.append('game')
from game import *
sys.path.append('players')
from random_player import *
from custom_player import *

players = [CustomPlayer(), CustomPlayer()]
game = Game(players)

assert game.state['players'] == {
    1: {
        'scout_coords': (4, 1),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 7),
        'home_colony_coords': (4, 7)
    }
}

game.complete_movement_phase()

assert game.state['players'] == {
    1: {
        'scout_coords': (4, 2),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 6),
        'home_colony_coords': (4, 7)
    }
}

game.complete_combat_phase() # Nothing changes since no units occupy the same location=
game.complete_movement_phase()

assert game.state['players'] == {
    1: {
        'scout_coords': (4, 3),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 5),
        'home_colony_coords': (4, 7)
    }
}

game.complete_combat_phase() # Nothing changes since no units occupy the same location
game.complete_movement_phase()

assert game.state['players'] == {
    1: {
        'scout_coords': (4, 4),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 4),
        'home_colony_coords': (4, 7)
    }
}

game.complete_combat_phase() # One of the scouts is randomly selected to be destroyed.

possibility_1 = {
    1: {
        'scout_coords': None,
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': (4, 4),
        'home_colony_coords': (4, 7)
    }
}

possibility_2 = {
    1: {
        'scout_coords': (4, 4),
        'home_colony_coords': (4, 1)
    },
    2: {
        'scout_coords': None,
        'home_colony_coords': (4, 7)
    }
}

print("\ngame.state['players']:", game.state['players'])

num_wins = {1: 0, 2: 0, 'tie': 0}
for _ in range(200):
    players = [CustomPlayer(), CustomPlayer()]
    game = Game(players)
    game.run_to_completion()
    winner = game.state['winner']
    num_wins[winner] += 1

print("\nnum_wins:", num_wins)