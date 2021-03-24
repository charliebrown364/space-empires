import random
import math
import time
import sys
sys.path.append('logs')
from logger import *

class Game():
  
    def __init__(self, players, board_size=[7,7]):
        self.players = players
        self.set_player_numbers()

        board_x, board_y = board_size
        mid_x = (board_x + 1) // 2
        mid_y = (board_y + 1) // 2

        self.state = {
            'turn': 1,
            'board_size': board_size,
            'players': {
                1: {
                    'scout_coords': {
                        1: (mid_x, 1),
                        2: (mid_x, 1),
                        3: (mid_x, 1),
                    },
                    'home_colony_coords': (mid_x, 1)
                },
                2: {
                    'scout_coords': {
                        1: (mid_x, 7),
                        2: (mid_x, 7),
                        3: (mid_x, 7),
                    },
                    'home_colony_coords': (mid_x, board_y)
                }
            },
            'winner': None
        }

    def set_player_numbers(self):
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)

    def check_if_coords_are_in_bounds(self, coords):
        if coords == None:
            return False
        x, y = coords
        board_x, board_y = self.state['board_size']
        return all([1 <= x, x <= board_x, 1 <= y, y <= board_y])

    def check_if_translation_is_in_bounds(self, coords, translation):
        if coords == None:
          return False
        max_x, max_y = self.state['board_size']
        x, y = coords
        dx, dy = translation
        new_coords = (x + dx, y + dy)
        return self.check_if_coords_are_in_bounds(new_coords)

    def get_in_bounds_translations(self, coords):
        translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
        in_bounds_translations = [translation for translation in translations if self.check_if_translation_is_in_bounds(coords, translation)]
        return in_bounds_translations

    # python tests/test_game_level_0_2.py

    def complete_movement_phase(self):
        
        # print("\ncomplete_movement_phase")

        player_1_scout_coords = self.state['players'][1]['scout_coords']
        player_2_scout_coords = self.state['players'][2]['scout_coords']
        players_coords = [player_1_scout_coords, player_2_scout_coords]
        
        # print("\nplayer_1_scout_coords:", player_1_scout_coords)
        # print("player_2_scout_coords:", player_2_scout_coords)

        first_player_index = random.randint(1, 2)
        # print("\nfirst player:", first_player_index)
        first_player = self.players[first_player_index - 1]
        second_player = self.players[first_player_index % 2]
        ordered_player_list = [first_player, second_player]
        
        for player_index in range(2):

            player = ordered_player_list[player_index]
            player_coords = players_coords[player.player_number - 1]
            ordered_player_index = self.players.index(player) + 1
            
            # print("\n\nplayer_index:", player_index)
            # print("player_coords:", player_coords)
            # print("ordered_player_index:", ordered_player_index)

            for scout_index, scout_coords in list(player_coords.items()):
                
                # print("\nscout_index:", scout_index)
                # print("scout_coords:", scout_coords)

                in_bounds_translations = self.get_in_bounds_translations(scout_coords)
                translation = player.choose_translation(self.state, in_bounds_translations)
                new_coords = (scout_coords[0] + translation[0], scout_coords[1] + translation[1])
                self.state['players'][player.player_number]['scout_coords'][scout_index] = new_coords

                # print("translation:", translation)
                # print("new_coords:", new_coords)

                logger.write('\t\t\t\tPlayer {} Scout {}: {} -> {}\n'.format(ordered_player_index, scout_index, scout_coords, new_coords))
            
            # print("\nplayer_coords:", self.state['players'][ordered_player_index]['scout_coords'])

        self.state['turn'] += 1
        # time.sleep(25)

    # python tests/test_game_level_0_2.py

    def complete_combat_phase(self):
        
        # print("\n\n\n\ncomplete_combat_phase")

        player_1_scout_coords = self.state['players'][1]['scout_coords']
        player_2_scout_coords = self.state['players'][2]['scout_coords']

        # print("\nplayer_1_scout_coords:", player_1_scout_coords)
        # print("player_2_scout_coords:", player_2_scout_coords)
        
        combat_scout = self.find_combat()
        all_scouts = [combat_scout for _ in range(6)]

        # print("\ncombat_scout:", combat_scout)

        if self.find_combat() != None:
            logger.write('\n\t\t\t\tCombat at {}\n\n'.format(combat_scout))
            # print("\n\n\nCombat at", combat_scout)
        
        while self.find_combat() != None:
            
            # might need to change how we calculate rand_player so that the person who went last time doesn't go again.

            rand_player = ''
            rand_scout = ''
            while rand_player == '' or rand_scout == '':
                
                rand_player = random.randint(1, 2)
                rand_scout = random.randint(1, 3)
                
                if rand_player not in list(self.state['players'].keys()):
                    rand_player = ''
                if rand_scout not in list(self.state['players'][rand_player]['scout_coords'].keys()):
                    rand_scout = ''

            # print("\n\nrand_player:", rand_player)
            # print("list(self.state['players'].keys()):", list(self.state['players'].keys()))
            # print("\nrand_scout:", rand_scout)
            # print("list(self.state['players'][rand_player]['scout_coords'].keys()):", list(self.state['players'][rand_player]['scout_coords'].keys()))
            
            # print("\nself.state['players'] before:", self.state['players'])

            del self.state['players'][rand_player]['scout_coords'][rand_scout]

            # print("self.state['players'] after :", self.state['players'])

            logger.write('\t\t\t\t\t\t\t\tPlayer {} Scout {} was destroyed\n'.format(rand_player, rand_scout))

            # print("\nPlayer {} Scout {} was destroyed".format(rand_player, rand_scout))

        # print("\nplayer_1_scout_coords:", self.state['players'][1]['scout_coords'])
        # print("player_2_scout_coords:", self.state['players'][2]['scout_coords'])

    # python tests/test_game_level_0_2.py

    def find_combat(self):

        # print("\nfind_combat")

        player_1_scout_coords = list(self.state['players'][1]['scout_coords'].values())
        player_2_scout_coords = list(self.state['players'][2]['scout_coords'].values())

        # print("f player_1_scout_coords:", player_1_scout_coords)
        # print("f player_2_scout_coords:", player_2_scout_coords)

        if len(player_1_scout_coords) != 0 and len(player_2_scout_coords) != 0:
            if player_1_scout_coords[0] == player_2_scout_coords[0]:
                return player_1_scout_coords[0]
        return None

    # python tests/test_game_level_0_2.py

    def run_to_completion(self):

        logger.clear_log()
        turn = 1

        while self.state['winner'] == None:

            # time.sleep(2)

            logger.write('\nBEGINNING OF TURN {} MOVEMENT PHASE\n'.format(turn))
            self.complete_movement_phase()
            logger.write('\nEND OF TURN {} MOVEMENT PHASE\n'.format(turn))
            logger.write('\nBEGINNING OF TURN {} COMBAT PHASE\n'.format(turn))
            # print("\n\nself.complete_combat_phase() starting\n")
            self.complete_combat_phase()
            logger.write('\nEND OF TURN {} COMBAT PHASE\n'.format(turn))

            player_1_scout_coords = self.state['players'][1]['scout_coords']
            player_1_home_colony_coords = self.state['players'][1]['home_colony_coords']

            player_2_scout_coords = self.state['players'][2]['scout_coords']
            player_2_home_colony_coords = self.state['players'][2]['home_colony_coords']

            # print('\nplayer_1_scout_coords:', player_1_scout_coords)
            # print("player_2_home_colony_coords:", player_2_home_colony_coords)

            # print('player_2_scout_coords:', player_2_scout_coords)
            # print("player_1_home_colony_coords:", player_1_home_colony_coords)

            player_1_wins = (player_2_home_colony_coords in list(player_1_scout_coords.values()))
            player_2_wins = (player_1_home_colony_coords in list(player_2_scout_coords.values()))

            if player_1_wins and not player_2_wins:
                logger.write('\nWINNER: PLAYER 1')
                self.state['winner'] = 1
            elif player_2_wins and not player_1_wins:
                logger.write('\nWINNER: PLAYER 2')
                self.state['winner'] = 2
            elif player_1_wins and player_2_wins:
                logger.write('\nWINNER: TIE')
                self.state['winner'] = 'tie'

            turn += 1

# python tests/test_game_level_0_2.py