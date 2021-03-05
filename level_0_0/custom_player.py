from random import random
import math

class CustomPlayer():
    def __init__(self):
        self.player_number = None

    def set_player_number(self, n):
        self.player_number = n

    def get_opponent_player_number(self):
        if self.player_number == None:
            return None
        elif self.player_number == 1:
            return 2
        elif self.player_number == 2:
            return 1

    def choose_translation(self, game_state, choices):

        myself = game_state['players'][self.player_number]
        opponent_player_number = self.get_opponent_player_number()
        opponent = game_state['players'][opponent_player_number]

        my_scout_coords = myself['scout_coords']
        opponent_home_colony_coords = opponent['home_colony_coords']

        # you need to use `my_scout_coords` and
        # `opponent_home_colony_coords` to return the
        # translation that will bring you closest to
        # the opponent

        all_distances = []
        for choice in choices:
            my_coords = tuple(list(my_scout_coords).copy())
            my_new_coords = (my_coords[0] + choice[0], my_coords[1] + choice[1])
            distance = self.calc_coord_distance(my_new_coords, opponent_home_colony_coords)
            all_distances.append(distance)
        
        for i in range(len(all_distances)):
            if all_distances[i] == min(all_distances):
                best_translation = choices[i]
        
        return best_translation

    def calc_coord_distance(self, my_coords, opponent_coords):
        x_change = (opponent_coords[0] - my_coords[0]) ** 2
        y_change = (opponent_coords[1] - my_coords[1]) ** 2
        return (x_change + y_change) ** (1/2)