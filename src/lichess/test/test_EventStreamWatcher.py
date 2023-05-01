from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.EventStreamWatcher import EventStreamWatcher
from src.lichess.test.conftest import *

class TestEventStreamWatcher:
    def setup_method(self):
        # Setup dependencies
        self.api = LichessAPI(mock_requests_session)
        self.game_manager = GameManager(self.api, engine_stub)

        # Instantiate the class to test
        # TODO: Mock the self.username call inside the EventStreamWatcher constructor
        self.event_stream_watcher = EventStreamWatcher(self.api, self.game_manager)

    def teardown_method(self):
       pass

    def test_challengeUserGetsAddedToChallengeQueue(self):
        test_user = "testuser"
        self.event_stream_watcher.challenge_user(test_user)
        assert test_user in self.event_stream_watcher.username_queue

    def test_challengingEmptyUserDoesNothing(self):
        self.event_stream_watcher.challenge_user()
        assert len(self.event_stream_watcher.username_queue) == 0

    def test_acceptingAChallenge(self):
        pass

    def test_sendingABotChallenge(self):
        pass