import re
import requests

API_BASE_URL = "https://lichess.org/api/"
URL_ENDPOINTS = {
    "get_my_profile": "account",
    "upgrade_to_bot_account": "bot/account/upgrade",
    "make_a_bot_move": "bot/game/<gameId>/move/<move>?offeringDraw=<offeringDraw>",
    "stream_bot_game_state": "bot/game/stream/<gameId>",
    "list_challenges": "challenge",
    "challenge_ai": "challenge/ai",
    "create_challenge": "challenge/<username>",
    "accept_challenge": "challenge/<challengeId>/accept",
    "decline_challenge": "challenge/<challengeId>/decline"
}

class LichessAPI():
    def __init__(self, oauth_token):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {oauth_token}"})

    def get_profile(self):
        url = self.__construct_url(URL_ENDPOINTS["get_my_profile"])
        request = self.session.get(url)

        return request

    def __construct_url(self, endpoint_url, **kwargs):

        for parameter_name, value in kwargs.items():
            endpoint_url = self.__add_url_parameter(endpoint_url, parameter_name, str(value))

        return API_BASE_URL + endpoint_url

    def __add_url_parameter(self, url, name, value):
        regex = f"<{name}>"
        url = re.sub(regex, value, url)

        return url

    def upgrade_to_bot(self):
        url = self.__construct_url(URL_ENDPOINTS["upgrade_to_bot_account"])
        request = self.session.post(url)

        return request

    def is_bot_account(self):
        profile = self.get_profile()

        try:
            title = profile["title"]
        except KeyError as err:
            is_bot = False

        is_bot = title == "BOT"

        return is_bot

    def move(self, gameId, move, offeringDraw = False):
        url = self.__construct_url(URL_ENDPOINTS["make_a_bot_move"], gameId = gameId, move = move, offeringDraw = offeringDraw)
        request = self.session.post(url)

        return request

    def stream_game_state(self, gameId):

        '''
        TODO: I think we need to stream like this?

        with requests.get(url, stream=True) as r:
            # Do things with the response here.

        '''
        url = self.__construct_url(URL_ENDPOINTS["stream_bot_game_state"], gameId = gameId)
        request = self.session.post(url)

        return request

    def list_challenges(self):
        url = self.__construct_url(URL_ENDPOINTS["list_challenges"])
        request = self.session.get(url)

        return request

    def create_challenge(self, username, request_body):
        url = self.__construct_url(URL_ENDPOINTS["create_challenge"], username = username)
        request = self.session.post(url, data = request_body)

        return request

    def accept_challenge(self, challengeId):
        url = self.__construct_url(URL_ENDPOINTS["accept_challenge"], challengeId = challengeId)
        request = self.session.post(url)

        return request

    def decline_challenge(self, challengeId, request_body):
        url = self.__construct_url(URL_ENDPOINTS["decline_challenge"], challengeId = challengeId)
        request = self.session.post(url, data = request_body)

        return request

    def challenge_ai(self, request_body):
        url = self.__construct_url(URL_ENDPOINTS["challenge_ai"])
        request = self.session.post(url, data = request_body)

        return request

    def create_seek(self, request_body):
        url = self.__construct_url(URL_ENDPOINTS["create_seek"])
        request = self.session.post(url, data = request_body)

        return request