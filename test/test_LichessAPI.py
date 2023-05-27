from responses import matchers

from conftest import *
from lichess.conf.settings import CHALLENGE_PARAMS

class TestLichessAPI:
    def test_getProfile(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["get_my_profile"])
        mocked_responses.add(
            responses.GET,
            url = url,
            json = fake_profile_data,
            status = 200,  
        )

        response = lichess_api.get_profile()

        assert mocked_responses.assert_call_count(url, 1) is True
        assert response.json() == fake_profile_data

    def test_upgradeToBot(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["upgrade_to_bot_account"])
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200,  
        )

        response = lichess_api.upgrade_to_bot()

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_isBotAccount_returnsTrueIfBot(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["get_my_profile"])
        fake_bot_profile = fake_profile_data
        mocked_responses.add(
            responses.GET,
            url = url,
            json = fake_bot_profile,
            status = 200,  
        )

        is_bot = lichess_api.is_bot_account()

        assert is_bot == True

    def test_isBotAccount_returnsFalseIfNotBot(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["get_my_profile"])
        mocked_responses.add(
            responses.GET,
            url = url,
            json = fake_non_bot_profile,
            status = 200,  
        )

        is_bot = lichess_api.is_bot_account()

        assert is_bot == False

    def test_move(self, lichess_api, mocked_responses):
        game_id = fake_gameStart["game"]["fullId"]
        move = "e2e4"
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["make_a_bot_move"], gameId = game_id, move = move)
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200,  
        )
        
        response = lichess_api.move(game_id, move)

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_streamBotGameState(self, lichess_api, mocked_responses):
        game_id = fake_gameStart["game"]["fullId"]
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_bot_game_state"], gameId = game_id)
        required_kwargs = { "stream": True }
        mocked_responses.add(
            responses.GET,
            url = url,
            json = "",
            status = 200,  
            match = [matchers.request_kwargs_matcher(required_kwargs)]
        )

        response = lichess_api.stream_bot_game_state(game_id)

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_streamChallenges(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_challenges"])
        required_kwargs = { "stream": True }
        mocked_responses.add(
            responses.GET,
            url = url,
            json = "",
            status = 200,  
            match = [matchers.request_kwargs_matcher(required_kwargs)]
        )

        response = lichess_api.stream_challenges()

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_createChallenge(self, lichess_api, mocked_responses):
        username = "username"
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["create_challenge"], username = username)
        expected_request_body = CHALLENGE_PARAMS["real_time"]
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200,
            match = [matchers.urlencoded_params_matcher(expected_request_body)],
        )

        response = lichess_api.create_challenge(username, CHALLENGE_PARAMS["real_time"])

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_acceptChallenge(self, lichess_api, mocked_responses):
        challenge_id = "challenge_id"
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["accept_challenge"], challengeId = challenge_id)
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200
        )

        response = lichess_api.accept_challenge(challenge_id)

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_declineChallenge(self, lichess_api, mocked_responses):
        challenge_id = "challenge_id"
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["decline_challenge"], challengeId = challenge_id)
        expected_request_body = {"reason": "generic"}
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200,
            match = [matchers.urlencoded_params_matcher(expected_request_body)],
        )

        decline_reason = {"reason": "generic"}
        response = lichess_api.decline_challenge(challenge_id, decline_reason)

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_challengeAI(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["challenge_ai"])
        expected_request_body = CHALLENGE_PARAMS["real_time"]
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200,
            match = [matchers.urlencoded_params_matcher(expected_request_body)],
        )

        response = lichess_api.challenge_ai(CHALLENGE_PARAMS["real_time"])

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_streamOnlineBots(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_online_bots"])
        required_kwargs = {"stream": True}
        number_of_bots_per_second = 60
        query_parameters = { "nb": number_of_bots_per_second }
        mocked_responses.add(
            responses.GET,
            url = url,
            json = "",
            status = 200,
            match = [matchers.request_kwargs_matcher(required_kwargs), matchers.query_param_matcher(query_parameters)]
        )

        response = lichess_api.stream_online_bots(number_of_bots_per_second = number_of_bots_per_second)

        expected_url = url + f"?nb={number_of_bots_per_second}"
        assert mocked_responses.assert_call_count(expected_url, 1) is True

    def test_streamEvents(self, lichess_api, mocked_responses):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_events"])
        required_kwargs = { "stream": True }
        mocked_responses.add(
            responses.GET,
            url = url,
            json = "",
            status = 200,  
            match=[matchers.request_kwargs_matcher(required_kwargs)]
        )

        response = lichess_api.stream_events()

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_abortGame(self, lichess_api, mocked_responses):
        game_id = fake_gameStart["game"]["fullId"]
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["abort_game"], gameId = game_id)
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200,  
        )

        response = lichess_api.abort_game(game_id)

        assert mocked_responses.assert_call_count(url, 1) is True

    def test_resignGame(self, lichess_api, mocked_responses):
        game_id = fake_gameStart["game"]["fullId"]
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["resign_game"], gameId = game_id)
        mocked_responses.add(
            responses.POST,
            url = url,
            json = "",
            status = 200,  
        )

        response = lichess_api.resign_game(game_id)

        assert mocked_responses.assert_call_count(url, 1) is True