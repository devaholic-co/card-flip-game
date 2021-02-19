import random
import sys
from app.model import model
from app.services import validation_service
from app.logger import logger

class game_service():

  def __init__(self, db_model = model.model(), validation_service = validation_service.validation_service(), logger = logger.logger()):
      self.db_model = db_model
      self.validation_service = validation_service
      self.logger = logger

  def get_global_best_score(self):
    return self.db_model.get_global_best_score()
  
  def get_default_return_data(self, user_data):
    return {
      'is_victory': False,
      'count': user_data['count'],
      'my_best': user_data['user_best_score'],
      'card_value': [0,0,0,0,0,0,0,0,0,0,0,0]
    }

  # TODO: Break Logic in this func to multiple service func
  def play_game(self, name, pos):
    # ========== 1. Get User Data From Database ==========
    user_data = self.db_model.read_db(name)
    if not user_data:
        return False
    
    return_data = self.get_default_return_data(user_data)
    open_position = user_data['success_opened'].copy()

    self.logger.info(name + " => try to open: " + str(pos))

    # ========== 2. Validate Input ==========
    if not self.validation_service.validate_open_card(pos, user_data):
      if(user_data['current_stage'] == 1):
        open_position.append(user_data['last_opened'])
      for known_position in open_position:
        return_data['card_value'][known_position] = user_data['all_card'][known_position]
      return return_data
    
    user_data['count'] = user_data['count'] + 1
    return_data['count'] = user_data['count']

    # ========== 3.1. Check Game End ==========
    if (self.check_victory(user_data)):
        user_data['user_best_score'] = self.get_best_score(user_data['count'], user_data['user_best_score'])
        self.db_model.set_global_best_score(user_data['user_best_score'])
        return_data['is_victory'] = True
        return_data['my_best'] = user_data['user_best_score']
        self.logger.info(name + " => victory with: " + str(user_data['count']))
    # ========== 3.2. Open new card without last pending ==========
    elif (user_data['current_stage'] == 0):
        user_data['current_stage'] = 1
        user_data['last_opened'] = pos
        open_position.append(pos)
    # ========== 3.3. Open new card and check with latest ==========
    else:
        last_opened = user_data['last_opened']
        if (user_data['all_card'][pos] == user_data['all_card'][last_opened]):
            user_data['success_opened'].append(pos)
            user_data['success_opened'].append(last_opened)
        user_data['current_stage'] = 0
        user_data['last_opened'] = 0
        open_position.append(pos)
        open_position.append(last_opened)
        
    # ========== 4. Return Open Card ==========
    for known_position in open_position:
        return_data['card_value'][known_position] = user_data['all_card'][known_position]
        
    self.db_model.update_db(name, user_data)
    return return_data

  def start_new_game(self, name):
    all_card = [1,1,2,2,3,3,4,4,5,5,6,6]
    random.shuffle(all_card)

    self.logger.info(name + " => new game: " + ','.join(str(e) for e in all_card))
    self.db_model.start_new_game(name, all_card)

    return True

  def check_victory(self, user_data):
    if(len(user_data['success_opened']) == 10 and user_data['current_stage'] == 1):
        return True
    else:
        return False

  def get_best_score(self, candidate_score, current_best_score):
    if(current_best_score == 0):
      return candidate_score
    else:
      return min(candidate_score, current_best_score)
