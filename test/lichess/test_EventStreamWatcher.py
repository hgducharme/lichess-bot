from conftest import *
from lichess.GameManager import GameManager
from lichess.LichessAPI import LichessAPI
from lichess.EventStreamWatcher import EventStreamWatcher

@pytest.fixture(scope="module")
@responses.activate
def event_stream_watcher():
    # EventManager queries the API for the lichess profile information upon instantiation,
    # so we tell responses to expect this call and mock it
    responses.add(
        responses.GET,
        LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["get_my_profile"]),
        json = fake_profile_data,
        status = 200,
    )
    responses.add(
        responses.GET,
        LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_events"]),
        body = fake_event_stream,
        status = 200,
    )

    # Setup dependencies
    api_session = requests.Session()
    api_session.headers.update({"Authorization": f"Bearer {fake_oauth_token}"})
    api = LichessAPI(api_session)
    game_manager = GameManager(api, engine_stub)

    # Instantiate the class to test
    return EventStreamWatcher(api, game_manager)

class TestEventStreamWatcher:
    def test_challengeUserGetsAddedToChallengeQueue(self, event_stream_watcher):
        test_user = "testuser"
        event_stream_watcher.work()
        event_stream_watcher.challenge_user(test_user)
        assert test_user in self.event_stream_watcher.username_queue

    def test_challengingEmptyUserDoesNothing(self, event_stream_watcher):
        event_stream_watcher.challenge_user()
        assert len(self.event_stream_watcher.username_queue) == 0

    def test_acceptingAChallenge(self):
        pass

    def test_sendingABotChallenge(self):
        pass