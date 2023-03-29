import pytest
import requests

from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.ChallengeStreamWatcher import ChallengeStreamWatcher

@pytest.fixture
def mock_session(mocker):
    mock_session = mocker.patch.object(requests, 'Session', autospec=True)
    mock_session.return_value.__enter__.return_value = mock_session
    return mock_session

class EngineMock:
    def __init__(self):
        pass


class TestChallengeStreamWatcher:
    
    mock_oath_token = "aaa"

    @pytest.mark.usefixtures('mock_session')
    def setup_method(self):   
        self.api = LichessAPI(TestChallengeStreamWatcher.mock_oath_token)
        self.engine_mock = EngineMock()
        self.game_manager = GameManager(self.api, self.engine_mock)
        self.challenge_stream_watcher = ChallengeStreamWatcher(self.api, self.game_manager)

    def teardown_method(self):
       pass

    def test_maxGameLimit(self):
        # TODO: Call GameManager.start_new_game() for n times, where n is the max nubmer of games + 1,
        # and see if GameManager will reject new games once it hits its limit. We should probably setup
        # a settings file for testing, maybe we can just use the default one? Or one derived from the default one.
        assert False