from conftest import *
from lichess.GameManager import GameManager
from lichess.LichessAPI import LichessAPI
from lichess.EventStreamWatcher import EventStreamWatcher

@pytest.fixture(scope="module")
def lichess_api():
    api_session = requests.Session()
    api_session.headers.update({"Authorization": f"Bearer {fake_oauth_token}"})
    return LichessAPI(api_session)

@pytest.fixture(scope="module")
def game_manager(lichess_api):
    return GameManager(lichess_api, engine_stub)

@pytest.fixture(scope="function")
@responses.activate
def event_stream_watcher(lichess_api, game_manager, request):
    # Get the marker
    marker = request.node.get_closest_marker("set_fake_event")

    # Get the parameter passed into the marker
    fake_event = marker.args[0]

    # This turns fake_event_stream into a byte-like iterable object which 
    # is required to mock an API "stream" from the requests library
    fake_event_stream = str.encode(fake_event)

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

    # TODO: This mock isn't working for some reason. The ChessGame request is hitting the actual 
    # lichess servers
    responses.add(
        responses.GET,
        LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_bot_game_state"]),
        body = fake_gameFull,
        status = 200,
    )

    return EventStreamWatcher(lichess_api, game_manager)

class TestEventStreamWatcher:
    @pytest.mark.set_fake_event(fake_gameStart)
    def test_gameStartEventCreatesNewGameInGameManager(self, event_stream_watcher):
        event_stream_watcher.work()

    # def test_challengeUserGetsAddedToChallengeQueue(self, event_stream_watcher):
    #     pass
    #     test_user = "testuser"
    #     event_stream_watcher.challenge_user(test_user)
    #     assert test_user in self.event_stream_watcher.username_queue

    # def test_challengingEmptyUserDoesNothing(self, event_stream_watcher):
    #     pass
    #     event_stream_watcher.challenge_user()
    #     assert len(self.event_stream_watcher.username_queue) == 0

    # def test_acceptingAChallenge(self):
    #     pass

    # def test_sendingABotChallenge(self):
    #     pass