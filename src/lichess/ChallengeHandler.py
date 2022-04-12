import json
from conf import settings
from threading import Thread

class ChallengeHandler(Thread):
    def __init__(self, lichess_api, **kwargs):
        Thread.__init__(self, **kwargs)
        self.api = lichess_api
        self.is_running = True
        self.number_of_games = 0
        self.username_queue = []

    def run(self):
        while self.is_running:
            self.challenges = self._get_and_parse_challenges()
            incoming_challenges = self.challenges["in"]
            outgoing_challenges = self.challenges["out"]

            if self.number_of_games == settings.MAX_NUMBER_OF_GAMES:
                continue

            if self._challenges_exist():
                self._accept_challenge()
            else:
                self._send_challenge()

    def challenge_user(self, username = None):
        self.username_queue.append(username)

    def _get_and_parse_challenges(self):
        challenges = self.api.stream_challenges()
        
        for line in challenges:
            if line:
                challenges = json.loads(line)

        return challenges

    def _challenges_exist(self):
        incoming_challenges = self.challenges["in"]
        return (len(incoming_challenges) > 0)

    def _send_challenge(self):
        # TODO: Do we have usernames in the user queue? If so, send those users a challenge.
        online_bots = self.api.stream_online_bots()
        # get an online bot
        # send the challenge

    def _accept_challenge(self):
        # accept first challenge
        return 0