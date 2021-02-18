import random
import sys
# sys.path.append('./')
from app.model import model

class game_service():
  def play_game(self, name, pos):
    db_model = model.model()
    user_data = db_model.read_db(name)
    if not user_data:
        return False
    
    return_data = {
        'is_victory': False,
        'card_value': [0,0,0,0,0,0,0,0,0,0,0,0]
    }
    op = user_data['success_opened'].copy()
    
    user_data['count'] = user_data['count'] + 1
    if (self.check_victory(user_data)):
        user_data['user_best_score'] = user_data['count']
        return_data['is_victory'] = True
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
        
    db_model.update_db(name, user_data)
    return return_data

  def check_victory(self, user_data):
    if(len(user_data['success_opened']) == 10 and user_data['current_stage'] == 1):
        return True
    else:
        return False
