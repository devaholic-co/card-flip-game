import json
import os.path
from os import path

class model():
  def __init__(self):
      print('init')
      
  def read_db(self, name):
      user_path = './app/database/'+name+'.json'
      if not path.exists(user_path):
          return {}
      with open(user_path) as json_file:
          data = json.load(json_file)
      return data

#   def update_db(self, name, all_card, count, success_opened, last_opened, current_stage, user_best_score):
#       with open('./app/database/'+name+'.json', 'w') as outfile:
#           data = {}
#           data['all_card'] = all_card
#           data['count'] = count
#           data['success_opened'] = success_opened
#           data['last_opened'] = last_opened
#           data['current_stage'] = current_stage
#           data['user_best_score'] = user_best_score
#           json.dump(data, outfile)

  def update_db(self, name, user_data):
      with open('./app/database/'+name+'.json', 'w') as outfile:
          json.dump(user_data, outfile)

  def start_new_game(self, name, all_card):
      user_path = './app/database/'+name+'.json'
      data = {}
      data['all_card'] = all_card
      data['count'] = 0
      data['success_opened'] = []
      data['last_opened'] = 0
      data['current_stage'] = 0
      data['user_best_score'] = self.read_db(name)['user_best_score']
      if path.exists(user_path):
          data['user_best_score'] = self.read_db(name)['user_best_score']
      else:
          data['user_best_score'] = 0
      self.update_db(name, data)
    #   if path.exists(user_path):
    #       self.update_db(name, all_card, 0, [], 0, 0, self.read_db(name)['user_best_score'])
    #   else:
    #       self.update_db(name, all_card, 0, [], 0, 0, 0)