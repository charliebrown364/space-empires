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

        all_distances = []
        for choice in choices:
            
            # print("\nmy_scout_coords:", my_scout_coords)
            
            my_coords = tuple(list(my_scout_coords.values()).copy())
            # print("my_coords:", my_coords)
            # print("len(my_coords):", len(my_coords))
            # print("choice:", choice)
            
            my_new_coords = []
            for coord in my_coords:
                new_coord = (coord[0] + choice[0], coord[1] + choice[1])
                my_new_coords.append(new_coord)
            my_new_coords = list(my_new_coords)

            distance = self.calc_coord_distance(my_new_coords, opponent_home_colony_coords)
            all_distances.append(distance)
        
        # print("\nall_distances:", all_distances)
        for i in range(len(all_distances)):
            if all_distances[i] == min(all_distances):
                best_translation = choices[i]
        
        return best_translation

    def calc_coord_distance(self, my_coords, opponent_coords):
        
        # print("\nmy_coords:", my_coords)
        # print("opponent_coords:", opponent_coords)
        
        coord_distances = []
        for coord in my_coords:
            # print("coord:", coord)
            x_change = (opponent_coords[0] - coord[0]) ** 2
            y_change = (opponent_coords[1] - coord[1]) ** 2
            coord_distance = (x_change + y_change) ** (1/2)
            coord_distances.append(coord_distance)
        
        return coord_distances