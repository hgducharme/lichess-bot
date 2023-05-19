from conftest import *
from lichess.ChessGameManager import ChessGameManager
from lichess.LichessAPI import LichessAPI
from lichess.MockChessGameFactory import MockChessGameFactory
from lichess.EventStreamWatcher import EventStreamWatcher

@pytest.fixture(scope="module")
def lichess_api():
    api_session = requests.Session()
    api_session.headers.update({"Authorization": f"Bearer fake_oauth_token"})
    return LichessAPI(api_session)

@pytest.fixture(scope="module")
def mock_chess_game_factory():
    return MockChessGameFactory()

@pytest.fixture(scope="module")
def chess_game_manager(mock_chess_game_factory):
    return ChessGameManager(mock_chess_game_factory)

@pytest.fixture(scope="function")
def event_stream_watcher(request, lichess_api, chess_game_manager, mocked_responses):
    # Get the marker
    marker = request.node.get_closest_marker("set_fake_event")

    # Get the parameter passed into the marker
    fake_event = marker.args[0]

    # This turns fake_event_stream into a byte-like iterable object which 
    # is required to mock an API "stream" from the requests library
    fake_event_stream = str.encode(fake_event)

    # EventManager queries the API for the lichess profile information upon instantiation,
    # so we tell responses to expect this call and mock it
    mocked_responses.add(
        responses.GET,
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["get_my_profile"]),
        json = fake_profile_data,
        status = 200,
    )

    mocked_responses.add(
        responses.GET,
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_events"]),
        body = fake_event_stream,
        status = 200,
    )

    return EventStreamWatcher(lichess_api, chess_game_manager)

class TestEventStreamWatcher:

    @pytest.mark.set_fake_event(fake_gameStart)
    def test_gameStartEventCreatesNewGame(self, event_stream_watcher, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0

        event_stream_watcher.work()

        assert chess_game_manager.number_of_games() == 1

    @pytest.mark.set_fake_event(fake_gameFinish)
    def test_gameFinishEventDeletesGame(self, event_stream_watcher, chess_game_manager):
        assert chess_game_manager.number_of_games() == 1

        event_stream_watcher.work()

        assert chess_game_manager.number_of_games() == 0