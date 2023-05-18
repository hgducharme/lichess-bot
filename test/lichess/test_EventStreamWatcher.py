import time

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
def game_manager(lichess_api, engine_stub):
    return GameManager(lichess_api, engine_stub)

@pytest.fixture(scope='module')
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.fixture(scope="function")
@responses.activate
def event_stream_watcher(request, lichess_api, game_manager):
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
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["get_my_profile"]),
        json = fake_profile_data,
        status = 200,
    )

    responses.add(
        responses.GET,
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_events"]),
        body = fake_event_stream,
        status = 200,
    )

    # api_session = requests.Session()
    # api_session.headers.update({"Authorization": f"Bearer {fake_oauth_token}"})
    # api = LichessAPI(api_session)
    # game_manager = GameManager(api, engine_stub)

    return EventStreamWatcher(lichess_api, game_manager)

class TestEventStreamWatcher:

    @pytest.mark.set_fake_event(fake_gameStart)
    @responses.activate
    def test_gameStartEventCreatesNewGameInGameManager(self, event_stream_watcher, empty_json_response):
        assert len(event_stream_watcher.game_manager.games) == 0

        fake_gameId = json.loads(fake_gameStart)["game"]["fullId"]
        responses.add(
            responses.GET,
            LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_bot_game_state"], gameId = fake_gameId),
            body = str.encode(fake_gameFull),
            status = 200,
        )

        fake_move = None
        responses.add(
            responses.POST,
            LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["make_a_bot_move"], gameId = fake_gameId, move = fake_move),
            body = empty_json_response,
            status = 200,
        )

        event_stream_watcher.work()

        time.sleep(2)

        assert len(event_stream_watcher.game_manager.games) == 1

        responses.add(
            responses.POST,
            LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["abort_game"], gameId = fake_gameId),
            body = empty_json_response,
            status = 200,
        )

        event_stream_watcher.game_manager.terminate_game(fake_gameId)