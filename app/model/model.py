import json
import os.path
from os import path
from logger import logger

class model():
  def __init__(self, logger = logger.logger()):
      self.logger = logger
      
  def get_user_path(self, name):
      return './database/'+name+'.json'

  def read_db(self, name):
      user_path = self.get_user_path(name)

      if not path.exists(user_path):
          self.logger.warn("read_db not exist for: "+name)
          return {}

      with open(user_path) as json_file:
          data = json.load(json_file)
      return data

  def update_db(self, name, user_data):
      user_path = self.get_user_path(name)

      if not path.exists(user_path):
          self.logger.warn("update_db not exist for: "+name)
          return {}

      with open(user_path, 'w') as outfile:
          json.dump(user_data, outfile)

  def start_new_game(self, name, all_card):
      user_path = self.get_user_path(name)

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
