import json
from conf import settings
from threading import Thread

class ChallengeHandler(Thread):
    def __init__(self, lichess_api, thread_name = None):
        Thread.__init__()
        self.api = lichess_api
        self.thread_name = thread_name
        self.is_running = True

    def run(self):
        while self.is_running:
            challenges = self._get_and_parse_challenges()
            incoming_challenges = challenges["in"]
            outgoing_challenges = challenges["out"]

            if len(incoming_challenges) == 0:
                self._send_challenge()

            if self.number_of_games == settings.MAX_NUMBER_OF_GAMES:
                continue
            else:
                self._accept_challenge()

    def _get_and_parse_challenges(self):
        challenges = self.api.stream_challenges()
        
        for line in challenges:
            if line:
                challenges = json.loads(line)

        return challenges

    def _send_challenge(self):
        return 0

    def _accept_challenge(self):
        return 0