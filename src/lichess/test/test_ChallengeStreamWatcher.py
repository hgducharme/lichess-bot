import pytest
import requests

from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.ChallengeStreamWatcher import ChallengeStreamWatcher
from src.lichess.conf import settings

@pytest.fixture
def mock_requests_session(mocker):
    mock_session = mocker.patch.object(requests, 'Session', autospec=True)
    mock_session.return_value.__enter__.return_value = mock_session
    return mock_session

class EngineMock:
    def __init__(self):
        pass

class TestChallengeStreamWatcher:
    
    mock_oath_token = "mock_oauth_token"

    @pytest.mark.usefixtures('mock_session')
    def setup_method(self):
        # Instantiate required instances for ChallengeStreamWatcher class
        self.api = LichessAPI(TestChallengeStreamWatcher.mock_oath_token)
        self.engine_mock = EngineMock()
        self.game_manager = GameManager(self.api, self.engine_mock)

        # Create the ChallengeStreamWatcher class
        self.challenge_stream_watcher = ChallengeStreamWatcher(self.api, self.game_manager)

        # Sample challenge data as how we see it from the lichess.com api
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

    def test_challengeUserGetsAddedToChallengeQueue(self):
        test_user = "testuser"
        self.challenge_stream_watcher.challenge_user(test_user)
        assert test_user in self.challenge_stream_watcher.username_queue

    def test_challengingEmptyUserDoesNothing(self):
        self.challenge_stream_watcher.challenge_user()
        assert len(self.challenge_stream_watcher.username_queue) == 0

    def test_acceptingAChallenge(self):
        pass

    def test_sendingABotChallenge(self):
        pass