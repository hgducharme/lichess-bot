from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.ChallengeStreamWatcher import ChallengeStreamWatcher
from src.lichess.test.conftest import *

class TestChallengeStreamWatcher:
    def setup_method(self):
        # Setup dependencies
        api = LichessAPI(mock_requests_session)
        game_manager = GameManager(api, engine_stub)

        # Instantiate the class to test
        self.challenge_stream_watcher = ChallengeStreamWatcher(api, game_manager)

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