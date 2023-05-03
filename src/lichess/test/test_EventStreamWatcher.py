from responses import _recorder

from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.EventStreamWatcher import EventStreamWatcher
from src.lichess.test.conftest import *
from src.lichess.conf import settings

@pytest.fixture(scope="module")
@responses.activate
def event_stream_watcher(engine_stub):
    responses.get()

    # Setup dependencies
    api_session = requests.Session()
    api_session.headers.update({"Authorization": f"Bearer {settings.API_TOKEN}"})
    api = LichessAPI(api_session)
    game_manager = GameManager(api, engine_stub)

    # Instantiate the class to test
    return EventStreamWatcher(api, game_manager)

class TestEventStreamWatcher:
    def test_challengeUserGetsAddedToChallengeQueue(self, event_stream_watcher):
        test_user = "testuser"
        event_stream_watcher.challenge_user(test_user)
        assert test_user in self.event_stream_watcher.username_queue

    def test_challengingEmptyUserDoesNothing(self, event_stream_watcher):
        event_stream_watcher.challenge_user()
        assert len(self.event_stream_watcher.username_queue) == 0

    def test_acceptingAChallenge(self):
        pass

    def test_sendingABotChallenge(self):
        pass