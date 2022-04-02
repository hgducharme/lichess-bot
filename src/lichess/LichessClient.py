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

class LichessClient():
    def __init__(self, oauth_token):
        self.__oauth_token = oauth_token
        


    def get_profile(self):
        url = self.__construct_url(URL_ENDPOINTS["get_my_profile"])
        header = self.__get_authorization_header()

        request = requests.get(url, headers = header)

        return request.json()

    def __construct_url(self, endpoint_url, **kwargs):

        for parameter_name, value in kwargs.items():
            endpoint_url = self.__add_url_parameter(endpoint_url, parameter_name, str(value))

        return API_BASE_URL + endpoint_url

    def __add_url_parameter(self, url, name, value):
        regex = f"<{name}>"
        url = re.sub(regex, value, url)

        return url

    def __get_authorization_header(self):
        authorization_header = {
            "Authorization": f"Bearer {self.__oauth_token}"
        }

        return authorization_header

    def upgrade_to_bot(self):
        url = self.__construct_url(URL_ENDPOINTS["upgrade_to_bot_account"])
        header = self.__get_authorization_header()

        request = requests.post(url, headers = header)

        return request

    def is_bot_account(self):
        profile = self.get_profile()

        try:
            title = profile["title"]
        except KeyError as err:
            is_bot = False

        is_bot = title == "BOT"

        return is_bot

    def set_api_token(self, token):
        self.__oauth_token = token

    def get_api_token(self):
        return self.__oauth_token

    def move(self, gameId, move, offeringDraw = False):
        url = self.__construct_url(URL_ENDPOINTS["make_a_bot_move"], gameId = gameId, move = move, offeringDraw = offeringDraw)
        header = self.__get_authorization_header()

        request = requests.post(url, headers = header)

        return request

    def stream_game_state(self, gameId):
        url = self.__construct_url(URL_ENDPOINTS["stream_bot_game_state"], gameId = gameId)
        header = self.__get_authorization_header()

        request = requests.post(url, headers = header)

        return request

    def list_challenges(self):
        url = self.__construct_url(URL_ENDPOINTS["list_challenges"])
        header = self.__get_authorization_header()

        request = requests.get(url, headers = header)

        return request

    def create_challenge(self, username, request_body):
        url = self.__construct_url(URL_ENDPOINTS["create_challenge"], username = username)
        header = self.__get_authorization_header()

        request = requests.post(url, data = request_body, headers = header)

        return request

    def accept_challenge(self, challengeId):
        url = self.__construct_url(URL_ENDPOINTS["accept_challenge"], challengeId = challengeId)
        header = self.__get_authorization_header()

        request = requests.post(url, headers = header)

        return request

    def decline_challenge(self, challengeId, request_body):
        header = self.__get_authorization_header()
        url = self.__construct_url(URL_ENDPOINTS["decline_challenge"], challengeId = challengeId)

        request = requests.post(url, data = request_body, headers = header)

        return request

    def challenge_ai(self, request_body):
        url = self.__construct_url(URL_ENDPOINTS["challenge_ai"])
        header = self.__get_authorization_header()

        request = requests.post(url, data = request_body, headers = header)

        return request

    def create_seek(self, request_body):
        url = self.__construct_url(URL_ENDPOINTS["create_seek"])
        header = self.__get_authorization_header()

        request = requests.post(url, data = request_body, headers = header)