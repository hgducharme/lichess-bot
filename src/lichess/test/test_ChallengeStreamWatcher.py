import pytest

from GameManager import GameManager
from LichessAPI import LichessAPI
from ChallengeStreamWatcher import ChallengeStreamWatcher

class TestChallengeStreamWatcher:
    def __init__(self):
        # Be careful with this. The init function is going to make calls to request.
        # Figure out a way to mock this in the instantiation
        # self.api = LichessAPI()
        self.game_manager = GameManager()
        self.challenge_stream_watcher = ChallengeStreamWatcher()

    def test_maxGameLimit(self):
        assert False
