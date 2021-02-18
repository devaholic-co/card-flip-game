class validation_service():
  def validate_open_card(self, pos, user_data):
    if(pos < 0 or pos > 11):
        return False
    elif(pos in user_data['success_opened']):
        return False
    elif(user_data['current_stage'] == 1 and pos == user_data['last_opened']):
        return False
    else:
        return True