from conftest import *
from responses import matchers

from lichess.conf import settings
from lichess.ChallengeSender import ChallengeSender

@pytest.fixture
def challenge_sender(lichess_api):
    return ChallengeSender(lichess_api)

class TestChallengeSender:
    def test_sendChallenge_sendsChallengeToLichess(self, challenge_sender, mocked_responses, empty_json_response):
        username = "testuser"
        challenge_settings = settings.CHALLENGE_PARAMS["real_time"]
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["create_challenge"], username = username)
        
        expected_request_body = challenge_settings
        mocked_responses.add(
            responses.POST,
            url = url,
            body = empty_json_response,
            status = 200,
            # This asserts that the request body is the same as expected_request_body
            match = [matchers.urlencoded_params_matcher(expected_request_body)],
        )

        challenge_sender.send_challenge(username, settings.CHALLENGE_PARAMS["real_time"])

        assert mocked_responses.assert_call_count(url, 1) is True