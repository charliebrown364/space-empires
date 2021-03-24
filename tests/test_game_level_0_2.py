import sys
sys.path.append('game')
from game_level_0_2 import *
sys.path.append('players')
from random_player import *
from custom_player import *

num_wins = {1: 0, 2: 0}
scouts_remaining = {1: 0, 2: 0}

num_times = 1000
for i in range(num_times):
    players = [CustomPlayer(), CustomPlayer()]
    game = Game(players)
    game.run_to_completion()
    winner = game.state['winner']
    scouts_remaining[winner] += len(game.state['players'][winner]['scout_coords'])
    num_wins[winner] += 1

print("\nnum_wins:", num_wins)

avg_scouts_remaining = {k:v/num_times for k,v in scouts_remaining.items()}
print("avg_scouts_remaining:", avg_scouts_remaining)