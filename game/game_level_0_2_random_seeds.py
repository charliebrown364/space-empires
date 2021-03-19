import random
import math

class Game():
  
    def __init__(self, players, random_seed, board_size=[7,7]):
        self.players = players
        random.seed(random_seed)
        self.set_player_numbers()

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': (mid_x, 1),
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': (mid_x, board_y),
                    'home_colony_coords': (mid_x, board_y)
                }
            },
            'winner': None
        }

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        x, y = coords
        board_x, board_y = self.state['board_size']
        return all([1 <= x, x <= board_x, 1 <= y, y <= board_y])

    def check_if_translation_is_in_bounds(self, coords, translation):
        max_x, max_y = self.state['board_size']
        x, y = coords
        dx, dy = translation
        new_coords = (x + dx, y + dy)
        return self.check_if_coords_are_in_bounds(new_coords)

    def get_in_bounds_translations(self, coords):
        translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = [translation for translation in translations if self.check_if_translation_is_in_bounds(coords, translation)]
        return in_bounds_translations

    def complete_movement_phase(self):

        player_1_coords = self.get_coords(1)
        player_2_coords = self.get_coords(2)
        players_coords = [player_1_coords, player_2_coords]

        if player_1_coords != player_2_coords:
            for player in self.players:
                coords = players_coords[player.player_number - 1]
                if coords != None:
                    in_bounds_translations = self.get_in_bounds_translations(coords)
                    translation = player.choose_translation(self.state, in_bounds_translations)
                    new_coords = (coords[0] + translation[0], coords[1] + translation[1])
                    self.state['players'][player.player_number]['scout_coords'] = new_coords
        
        self.state['turn'] += 1
    
    def complete_combat_phase(self):
        
        if self.get_coords(1) == self.get_coords(2):
            rand = 2 - round(random.random())
            self.state['players'][rand]['scout_coords'] = None

    def run_to_completion(self):

        while self.state['winner'] == None:

            self.complete_movement_phase()
            self.complete_combat_phase()

            player_1_scout_coords = self.get_coords(1)
            player_1_home_colony_coords = self.get_coords(1, 'home_colony_coords')

            player_2_scout_coords = self.get_coords(2)
            player_2_home_colony_coords = self.get_coords(2, 'home_colony_coords')

            player_1_wins = (player_1_scout_coords == player_2_home_colony_coords)
            player_2_wins = (player_2_scout_coords == player_1_home_colony_coords)

            if player_1_wins and not player_2_wins:
                self.state['winner'] = 1
            elif player_2_wins and not player_1_wins:
                self.state['winner'] = 2
            elif player_1_wins and player_2_wins:
                self.state['winner'] = 'tie'
    
    def get_coords(self, player_number, coords_type = 'scout_coords'):
        return self.state['players'][player_number][coords_type]