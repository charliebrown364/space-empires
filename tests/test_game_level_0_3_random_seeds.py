import sys
sys.path.append('game')
from game_level_0_3_random_seeds import *
sys.path.append('players')
from random_player import *
from custom_player import *

# python tests/test_game_level_0_3_random_seeds.py

"""

During combat, instead of choosing scouts randomly to be destroyed, construct a combat order in which the ships who occupied the grid space first come first in the order. 

- Assign a number to each ship, which represents whether it's the 1st, 2nd, 3rd, etc. ship in the spot it moved to. Update that number every time a ship moves.

- Then, loop through each ship in the combat order. Each ship will attack the first ENEMY ship that appears in the combat order.

- For each attack, generate a random number round(random.random()). If 0, then the attack misses and the defender lives. If 1, then the attack hits and the defender is destroyed.

- Important: After a ship is destroyed, it cannot attack or be attacked.

- Replace the destroyed ship with None in the combat order.

"""

players = [CustomPlayer(), CustomPlayer()]
game = Game(players, 1)
game.run_to_completion()

print("no errors")