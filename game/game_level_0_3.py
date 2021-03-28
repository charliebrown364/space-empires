import random
import sys
sys.path.append('logs')
from logger import *

class Game():
  def __init__(self, players, random_seed, board_size=[7,7]):
    # self.logs = Logger('/home/runner/space-empires/logs/game-0.3-logs.txt')
    # self.logs.clear_log()
    self.players = players
    self.set_player_numbers()
    random.seed(random_seed)
    
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
    if 1 <= x and x <= board_x:
      if 1 <= y and y <= board_y:
        return True
    return False

  def check_if_translation_is_in_bounds(self, coords, translation):
    if coords == None:
      return False
    max_x, max_y = self.state['board_size']
    x, y = coords
    dx, dy = translation
    new_coords = (x+dx,y+dy)
    return self.check_if_coords_are_in_bounds(new_coords)

  def get_in_bounds_translations(self, coords):
    translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
    in_bounds_translations = []
    for translation in translations:
      if self.check_if_translation_is_in_bounds(coords, translation):
        in_bounds_translations.append(translation)
    return in_bounds_translations


  def complete_movement_phase(self):
    logger.write('\nBEGINNING OF TURN {} MOVEMENT PHASE\n\n'.format(self.state['turn']))

    for player in self.players:
      player_scouts =  self.state['players'][player.player_number]['scout_coords']
      opponent_player_scouts = self.state['players'][self.get_opponent_player_number(player.player_number)]['scout_coords']
      for scout_num in player_scouts:
        if player_scouts[scout_num] not in opponent_player_scouts.values():
          current_coords = self.state['players'][player.player_number]['scout_coords'][scout_num]
          potential_translations = self.get_in_bounds_translations(current_coords) 
          translation = player.choose_translation(self.state, potential_translations, scout_num)
          new_coords = (current_coords[0] + translation[0], current_coords[1] + translation[1])
          self.state['players'][player.player_number]['scout_coords'][scout_num] = new_coords
          logger.write('\tPlayer {} Scout {}: {} -> {}\n'.format(player.player_number, scout_num, current_coords, new_coords))

    logger.write('\nEND OF TURN {} MOVEMENT PHASE\n'.format(self.state['turn']))
    

  def complete_combat_phase(self):
    logger.write('\nBEGINNING OF TURN {} COMBAT PHASE\n'.format(self.state['turn']))
    combat_coords = self.combat_locations()
    if combat_coords != []:   
      logger.write('\n\tCombat Locations:\n')
    for coords in combat_coords:
      logger.write('\n\t\t' + str(coords) + '\n')
      for player in self.players:
        player_scouts = self.state['players'][player.player_number]['scout_coords']
        for scout_num in player_scouts:
          if player_scouts[scout_num] == coords:
            logger.write('\t\t\tPlayer {} Scout {}\n'.format(player.player_number, scout_num))

    for location in combat_coords:
      combat_order = []
      for player in self.players:
        player_scouts = self.state['players'][player.player_number]['scout_coords']
        for scout_num in player_scouts:
          if player_scouts[scout_num] == location:
            combat_order.append((player.player_number, scout_num))
      
      logger.write('\n\tCombat at {}\n'.format(location))
      while self.combat_locations() != []:
        for (player_number, scout_num) in combat_order:
          attacker = (player_number, scout_num)
          for potential_defender in combat_order:
            if potential_defender[0] == self.get_opponent_player_number(player_number):
              defender = potential_defender
              break 
          logger.write('\n\t\tAttacker: Player {} Scout {}\n'.format(attacker[0], attacker[1]))
          logger.write('\t\tDefender: Player {} Scout {}\n'.format(defender[0], defender[1]))
        
          hit_value = round(random.random())
          if hit_value == 0:
            logger.write('\t\t(Miss)\n')
          else:
            logger.write('\t\tHit!\n')
            combat_order.remove(defender)
            del self.state['players'][defender[0]]['scout_coords'][defender[1]]
            logger.write('\t\tPlayer {} Scout {} was destroyed\n'.format(defender[0], defender[1]))
    
    if combat_coords != []:    
      logger.write('\n\tSurvivors:\n')
    for coords in combat_coords:
      logger.write('\t\t' + str(coords) + '\n')
      for player in self.players:
        player_scouts = self.state['players'][player.player_number]['scout_coords']
        for scout_num in player_scouts:
          if player_scouts[scout_num] == coords:
            logger.write('\t\t\tPlayer {} Scout {}\n'.format(player.player_number, scout_num))

    logger.write('\nEND OF TURN {} COMBAT PHASE\n'.format(self.state['turn']))

  def run_to_completion(self):
    while self.state['winner'] == None:
      self.complete_movement_phase()
      self.complete_combat_phase()
      self.state['turn'] += 1
      self.state['winner'] = self.check_for_winner()

  def check_for_winner(self):
    p1_scouts = self.state['players'][1]['scout_coords']
    p1_home_colony = self.state['players'][1]['home_colony_coords']
    p2_scouts = self.state['players'][2]['scout_coords']
    p2_home_colony = self.state['players'][2]['home_colony_coords']

    if any(p1_scouts[key] == p2_home_colony for key in p1_scouts) and any(p2_scouts[key] == p1_home_colony for key in p2_scouts):
      logger.write('\nTIE GAME')
      return 'Tie' 
    elif any(p1_scouts[key] == p2_home_colony for key in p1_scouts):
      logger.write('\nWINNER: PLAYER 1')
      return 1
    elif any(p2_scouts[key] == p1_home_colony for key in p2_scouts):
      logger.write('\nWINNER: PLAYER 2')
      return 2
    else:
      return None
  
  def get_opponent_player_number(self, player_number):
    if player_number == None:
      return None
    elif player_number == 1:
      return 2
    elif player_number == 2:
      return 1
  
  def combat_locations(self):
    combat_locations = []
    for player in self.players:
      player_scouts =  self.state['players'][player.player_number]['scout_coords']
      opponent_player_scouts = self.state['players'][self.get_opponent_player_number(player.player_number)]['scout_coords']
      for scout_num in player_scouts:
        if player_scouts[scout_num] in opponent_player_scouts.values():
          combat_locations.append(player_scouts[scout_num])
          break
      break

    return combat_locations