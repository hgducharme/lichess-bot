import pytest

from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.ChallengeStreamWatcher import ChallengeStreamWatcher

class TestChallengeStreamWatcher:
    def setup_class(self):
        # Be careful with this. The init function is going to make calls to request.
        # Figure out a way to mock this in the instantiation
        # self.api = LichessAPI()
        # self.game_manager = GameManager()
        # self.challenge_stream_watcher = ChallengeStreamWatcher()
        pass

    def test_maxGameLimit(self):
        assert False
