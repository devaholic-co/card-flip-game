import unittest
from unittest.mock import MagicMock
import sys
sys.path.append('../')

from app.services import game_service
from app.model import model

class TestGameService(unittest.TestCase):
    db_model = model.model()
    db_model.read_db = MagicMock(return_value = {
        "all_card": [2, 5, 6, 3, 1, 2, 4, 1, 4, 3, 6, 5], 
        "count": 17, 
        "success_opened": [0, 1, 2, 4, 5, 6, 7, 8, 10], 
        "last_opened": 9, 
        "current_stage": 1, 
        "user_best_score": 113
    })
    db_model.update_db = MagicMock()
    db_model.start_new_game = MagicMock()
    game_service_obj = game_service.game_service(db_model = db_model)
    
    def test_open_already_opened(self):
        res = self.game_service_obj.play_game("some-player", 0)
        self.assertEqual(res['count'], 17, "Open Already Opened should not increase count")

    def test_play_game_not_match_card(self):
        res = self.game_service_obj.play_game("some-player", 11)
        self.assertEqual(res['is_victory'], False, "Open New Card not victory")
        self.assertEqual(res['count'], 18, "Open New Card should increase count")

    # TODO: add test_play_game_match_card

    # TODO: add test play game with curremt stage 0

    def test_last_play_to_victory(self):
        db_model = model.model()
        db_model.read_db = MagicMock(return_value = {
            "all_card": [2, 5, 6, 3, 1, 2, 4, 1, 4, 3, 6, 5], 
            "count": 17, 
            "success_opened": [0, 1, 2, 3, 4, 5, 6, 7, 8, 10], 
            "last_opened": 9, 
            "current_stage": 1, 
            "user_best_score": 113
        })
        db_model.update_db = MagicMock()
        db_model.get_global_best_score = MagicMock(return_value = 15)
        db_model.set_global_best_score = MagicMock()
        game_service_obj = game_service.game_service(db_model = db_model)
        res = game_service_obj.play_game("some-player", 11)
        self.assertEqual(res['is_victory'], True, "Last Click to Victory")
        self.assertEqual(res['my_best'], 18, "Last Click to Victory should set new my best")
    
    # TODO: add test validation function return true

    # TODO: add test validation function return false for pos not in (0,11)

    # TODO: add test validation function return false for pos already opened

    # TODO: add test for check victory func

    def test_start_new_game(self):
        self.assertEqual(self.game_service_obj.start_new_game("some-player"), True, "Start New Game should return true")
        self.db_model.start_new_game.assert_called_once()

if __name__ == '__main__':
    unittest.main()