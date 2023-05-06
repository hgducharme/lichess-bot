import re
import logging

logger = logging.getLogger(__name__)

class LichessAPI():
    API_BASE_URL = "https://lichess.org/api/"

    URL_ENDPOINTS = {
        "get_my_profile": "account",
        "upgrade_to_bot_account": "bot/account/upgrade",
        "make_a_bot_move": "bot/game/<gameId>/move/<move>",
        "stream_bot_game_state": "bot/game/stream/<gameId>",
        "stream_challenges": "challenge",
        "challenge_ai": "challenge/ai",
        "create_challenge": "challenge/<username>",
        "accept_challenge": "challenge/<challengeId>/accept",
        "decline_challenge": "challenge/<challengeId>/decline",
        "stream_online_bots": "bot/online",
        "stream_events": "stream/event",
        "abort_game": "bot/game/<gameId>/abort",
        "resign_game": "bot/game/<gameId>/resign"
    }

    @classmethod
    def construct_url(cls, endpoint_url, **kwargs):
        for parameter_name, value in kwargs.items():
            endpoint_url = cls.add_url_parameter(endpoint_url, parameter_name, str(value))

        return LichessAPI.API_BASE_URL + endpoint_url

    @classmethod
    def add_url_parameter(cls, url, name, value):
        regex = f"<{name}>"
        url = re.sub(regex, value, url)
        return url

    def __init__(self, api_session):
        self.session = api_session

    def get_profile(self):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["get_my_profile"])
        response = self.session.get(url)

        return response

    def upgrade_to_bot(self):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["upgrade_to_bot_account"])
        response = self.session.post(url)

        return response

    def is_bot_account(self):
        profile = self.get_profile()

        try:
            title = profile["title"]
            is_bot = title == "BOT"
        except KeyError as err:
            is_bot = False

        return is_bot

    def move(self, gameId, move, offeringDraw = False):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["make_a_bot_move"], gameId = gameId, move = move)
        query_parameters = { "offeringDraw": offeringDraw }
        
        logger.debug(f"Sending move {move} to lichess.com")
        response = self.session.post(url)
        logger.debug(f"Lichess response: {response.json()}")

        return response

    def stream_game_state(self, gameId):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_bot_game_state"], gameId = gameId)
        response = self.session.get(url, stream = True)

        return response.iter_lines()

    def stream_challenges(self):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_challenges"])
        response = self.session.get(url, stream = True)

        return response.iter_lines()

    def create_challenge(self, username, request_body):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["create_challenge"], username = username)
        response = self.session.post(url, data = request_body)

        return response

    def accept_challenge(self, challengeId):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["accept_challenge"], challengeId = challengeId)
        response = self.session.post(url)

        return response

    def decline_challenge(self, challengeId, request_body):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["decline_challenge"], challengeId = challengeId)
        response = self.session.post(url, data = request_body)

        return response

    def challenge_ai(self, request_body):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["challenge_ai"])
        response = self.session.post(url, data = request_body)

        return response

    def stream_online_bots(self, number_of_bots_per_second = 50):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_online_bots"])
        query_parameters = { "nb": number_of_bots_per_second }
        response = self.session.get(url, params = query_parameters, stream = True)

        return response.iter_lines()

    def stream_events(self):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["stream_events"])
        response = self.session.get(url, stream = True)

        return response.iter_lines()

    def abort_game(self, gameId):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["abort_game"], gameId = gameId)
        response = self.session.post(url)

        status_code = response.status_code
        response_message = response.json()
        logger.debug(f"Abort game response: {status_code} - {response_message}")

        return response

    def resign_game(self, gameId):
        url = LichessAPI.construct_url(LichessAPI.URL_ENDPOINTS["resign_game"], gameId = gameId)
        response = self.session.post(url)

        status_code = response.status_code
        response_message = response.json()
        logger.debug(f"Resignation response: {status_code} - {response_message}")

        return response