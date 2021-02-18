import random
import sys
# sys.path.append('./')
from model import model
from services import validation_service

class game_service():

  def __init__(self, db_model = model.model(), validation_service = validation_service.validation_service()):
      self.db_model = db_model
      self.validation_service = validation_service

  def play_game(self, name, pos):
    user_data = self.db_model.read_db(name)
    if not user_data:
        return False
    
    return_data = {
        'is_victory': False,
        'my_best': user_data['user_best_score'],
        'card_value': [0,0,0,0,0,0,0,0,0,0,0,0]
    }
    op = user_data['success_opened'].copy()

    if not self.validation_service.validate_open_card(pos, user_data):
      if(user_data['current_stage'] == 1):
        op.append(user_data['last_opened'])
      for p in op:
        return_data['card_value'][p] = user_data['all_card'][p]
      return return_data
    
    user_data['count'] = user_data['count'] + 1
    if (self.check_victory(user_data)):
        user_data['user_best_score'] = user_data['count']
        return_data['is_victory'] = True
        return_data['my_best'] = user_data['user_best_score']
    elif (user_data['current_stage'] == 0):
        user_data['current_stage'] = 1
        user_data['last_opened'] = pos
        op.append(pos)
    else:
        last_opened = user_data['last_opened']
        if (user_data['all_card'][pos] == user_data['all_card'][last_opened]):
            user_data['success_opened'].append(pos)
            user_data['success_opened'].append(last_opened)
        user_data['current_stage'] = 0
        user_data['last_opened'] = 0
        op.append(pos)
        op.append(last_opened)
        
    for p in op:
        return_data['card_value'][p] = user_data['all_card'][p]
        
    self.db_model.update_db(name, user_data)
    return return_data

  def start_new_game(self, name):
    all_card = [1,1,2,2,3,3,4,4,5,5,6,6]
    random.shuffle(all_card)
    self.db_model.start_new_game(name, all_card)

  def check_victory(self, user_data):
    if(len(user_data['success_opened']) == 10 and user_data['current_stage'] == 1):
        return True
    else:
        return False
