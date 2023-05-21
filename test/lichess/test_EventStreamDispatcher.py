import json
from responses import matchers

from conftest import *
from lichess.conf import settings
from lichess.EventStreamDispatcher import EventStreamDispatcher

@pytest.fixture(scope="function")
def event_stream_dispatcher(request, lichess_api, chess_game_manager, mocked_responses):
    # Get the marker
    marker = request.node.get_closest_marker("set_fake_event")

    # Get the parameter passed into the marker
    fake_event = marker.args[0]

    # This turns fake_event_stream into a byte-like iterable object which 
    # is required to mock an API "stream" from the requests library
    fake_event_stream = str.encode(json.dumps(fake_event))

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

    return EventStreamDispatcher(lichess_api, chess_game_manager)

class TestEventStreamDispatcher:

    @pytest.mark.set_fake_event(fake_gameStart)
    def test_gameStartEventCreatesNewGame(self, event_stream_dispatcher, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0

        event_stream_dispatcher.work()

        assert chess_game_manager.number_of_games() == 1

    @pytest.mark.set_fake_event(fake_gameFinish)
    def test_gameFinishEventDeletesGame(self, event_stream_dispatcher, chess_game_manager):
        chess_game_manager.start_new_game(fake_gameStart)
        assert chess_game_manager.number_of_games() == 1

        event_stream_dispatcher.work()

        assert chess_game_manager.number_of_games() == 0

    @pytest.mark.set_fake_event(fake_outgoingChallenge)
    def test_outgoingChallengeEventCreatedByTheBotDoesNothing(self, event_stream_dispatcher, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0

        event_stream_dispatcher.work()

        assert chess_game_manager.number_of_games() == 0

    @pytest.mark.set_fake_event(fake_outgoingChallengeDeclined)
    def test_challengeDeclinedEventDoesNothing(self, event_stream_dispatcher, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0
        
        event_stream_dispatcher.work()

        assert chess_game_manager.number_of_games() == 0

    @pytest.mark.set_fake_event(fake_incomingChallengeCancelled)
    def test_incomingChallengeCanceledEventDoesNothing(self, event_stream_dispatcher, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0

        event_stream_dispatcher.work()

        assert chess_game_manager.number_of_games() == 0

    @pytest.mark.set_fake_event(fake_incomingChallenge)
    def test_incomingChallengeGetsAcceptedIfAcceptingChallengesFlagIsTrue(self, mocked_responses, event_stream_dispatcher, empty_json_response):
        settings.ACCEPTING_CHALLENGES = True

        fake_challenge_id = fake_incomingChallenge["challenge"]["id"]
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["accept_challenge"], challengeId = fake_challenge_id)
        mocked_responses.add(
            responses.POST,
            url = url,
            json = empty_json_response,
            status = 200,
        )

        event_stream_dispatcher.work()

        assert mocked_responses.assert_call_count(url, 1) is True


    @pytest.mark.set_fake_event(fake_incomingChallenge)
    def test_incomingChallengeGetsDeclinedIfAcceptingChallengesFlagIsFalse(self, mocked_responses, event_stream_dispatcher, empty_json_response):
        settings.ACCEPTING_CHALLENGES = False

        fake_challenge_id = fake_incomingChallenge["challenge"]["id"]
        expected_request_body = {"reason": "generic"}
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["decline_challenge"], challengeId = fake_challenge_id)
        mocked_responses.add(
            responses.POST,
            url = url,
            json = empty_json_response,
            status = 200,
            # This asserts that the request body is the same as expected_request_body
            match = [matchers.urlencoded_params_matcher(expected_request_body)],
        )

        event_stream_dispatcher.work()

        assert mocked_responses.assert_call_count(url, 1) is True