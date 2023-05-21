import json

from conftest import *
from lichess.ChessGame import ChessGame

@pytest.fixture(scope="function")
def chess_game(request, lichess_api, mock_engine, mocked_responses, empty_json_response):
    # Get the marker
    marker = request.node.get_closest_marker("set_fake_game_state")

    # Get the parameters passed into the marker
    game_info = marker.args[0]
    fake_game_state_event = marker.args[1]

    # This turns fake_event_stream into a byte-like iterable object which 
    # is required to mock an API "stream" from the requests library
    fake_game_state_stream = str.encode(json.dumps(fake_game_state_event))
    
    game_id = game_info["game"]["fullId"]
    mocked_responses.add(
        responses.GET,
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_bot_game_state"], gameId = game_id),
        body = fake_game_state_stream,
        status = 200,
    )

    return ChessGame(lichess_api, mock_engine, game_info)

class TestChessGame:

    @pytest.mark.set_fake_game_state(fake_game_colorBlack, fake_gameFull_colorBlack_isNotOurTurn)
    def test_gameState_isSetProperlyOnGameFullEvent(self, chess_game):
        chess_game.work()

        assert chess_game.full_game_info == fake_gameFull_colorBlack_isNotOurTurn
        assert chess_game.game_state == fake_gameFull_colorBlack_isNotOurTurn["state"]

    @pytest.mark.set_fake_game_state(fake_game_colorBlack, fake_gameState_colorBlack_isNotOurTurn)
    def test_gameState_isSetProperlyOnGameStateEvent(self, chess_game):
        chess_game.work()

        assert chess_game.game_state == fake_gameState_colorBlack_isNotOurTurn

    @pytest.mark.set_fake_game_state(fake_game_colorBlack, fake_gameState_colorBlack_isOurTurn)
    def test_blacksMoveIsSentToLichess(self, chess_game, mocked_responses, empty_json_response):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["make_a_bot_move"], gameId = chess_game.game_id, move = None)
        mocked_responses.add(
            responses.POST,
            url = url,
            body = empty_json_response,
            status = 200,
        )

        chess_game.work()

        assert mocked_responses.assert_call_count(url, 1) is True

    @pytest.mark.set_fake_game_state(fake_game_colorWhite, fake_gameFull_colorWhite_isOurTurn)
    def test_whitesMoveIsSentToLichess(self, chess_game, mocked_responses, empty_json_response):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["make_a_bot_move"], gameId = chess_game.game_id, move = None)
        mocked_responses.add(
            responses.POST,
            url = url,
            body = empty_json_response,
            status = 200,
        )

        chess_game.work()

        assert mocked_responses.assert_call_count(url, 1) is True

    @pytest.mark.set_fake_game_state(fake_game_colorBlack, fake_gameFull_colorBlack_isNotOurTurn)
    def test_abortOrResign_abortsIfGameHasNotStarted(self, chess_game, mocked_responses, empty_json_response):
        abort_url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["abort_game"], gameId = chess_game.game_id)
        resign_url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["resign_game"], gameId = chess_game.game_id)

        mocked_responses.add(
            responses.POST,
            url = abort_url,
            body = empty_json_response,
            status = 200,
        )

        chess_game.work()
        chess_game.abort_or_resign()

        assert mocked_responses.assert_call_count(abort_url, 1) is True
        assert mocked_responses.assert_call_count(resign_url, 0) is True

    @pytest.mark.set_fake_game_state(fake_game_colorBlack, fake_gameState_colorBlack_isNotOurTurn)
    def test_abortOrResign_resignsIfGameHasStarted(self, chess_game, mocked_responses, empty_json_response):
        abort_url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["abort_game"], gameId = chess_game.game_id)
        resign_url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["resign_game"], gameId = chess_game.game_id)

        mocked_responses.add(
            responses.POST,
            url = resign_url,
            body = empty_json_response,
            status = 200,
        )

        chess_game.work()
        chess_game.abort_or_resign()

        assert mocked_responses.assert_call_count(abort_url, 0) is True
        assert mocked_responses.assert_call_count(resign_url, 1) is True