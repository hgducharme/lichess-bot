import requests

API_BASE_URL = "https://lichess.org/api/"
URL_ENDPOINTS = {
    "get_my_profile": "account",
    "upgrade_to_bot_account": "bot/account/upgrade"
}

class LichessClient():
    def __init__(self, oauth_token):
        self.__oauth_token = oauth_token

    def get_profile(self):
        url = self.__construct_url(URL_ENDPOINTS["get_my_profile"])
        header = self.__get_authorization_header()

        request = requests.get(url, headers = header)

        return request.json()

    def __construct_url(self, endpoint):
        return API_BASE_URL + endpoint

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