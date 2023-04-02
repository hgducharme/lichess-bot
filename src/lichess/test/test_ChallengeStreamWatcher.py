import pytest
import requests

from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.ChallengeStreamWatcher import ChallengeStreamWatcher
from src.lichess.conf import settings

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

        self.mock_challenges = [
            {'type': 'challenge', 'challenge': {'id': 'A', 'url': 'https://lichess.org/A', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
            {'type': 'challenge', 'challenge': {'id': 'B', 'url': 'https://lichess.org/B', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
            {'type': 'challenge', 'challenge': {'id': 'C', 'url': 'https://lichess.org/C', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
            {'type': 'challenge', 'challenge': {'id': 'D', 'url': 'https://lichess.org/D', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
            {'type': 'challenge', 'challenge': {'id': 'E', 'url': 'https://lichess.org/E', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
            {'type': 'challenge', 'challenge': {'id': 'F', 'url': 'https://lichess.org/F', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}}
        ]

    def teardown_method(self):
       pass

    def test_maxGameLimit(self):
        # TODO: Call GameManager.start_new_game() n times, where n is the max nubmer of games.
        # and see if ChallengeStreamWatcher will reject new games once it hits its limit. We should probably setup
        # a settings file for testing, maybe we can just use the default one? Or one derived from the default one.

        # Create the max number of games allowed
        for i in range(0, settings.MAX_NUMBER_OF_GAMES):
            self.game_manager.start_new_game(self.mock_challenges[i])

        # Send a mock challenge to ChallengeStreamWatcher and verify that it doesn't create a new game
        # OR, should I instead setup the test suite just like how main.py sets it up, and then interface
        # with the code through the event and challenge streams? Instead of interacting on a more surgical level.

        assert False