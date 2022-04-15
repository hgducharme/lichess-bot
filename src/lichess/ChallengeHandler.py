import json
import logging
from conf import settings
import threading

logger = logging.getLogger(__name__)
class ChallengeHandler(threading.Thread):
    def __init__(self, lichess_api, **kwargs):
        logger.info("Creating an instance of ChallengerHandler")
        threading.Thread.__init__(self, **kwargs)
        self.api = lichess_api
        self.terminate_flag = threading.Event()
        self.number_of_games = 0
        self.username_queue = []

    def run(self):
        logger.info("A ChallengeHandler thread has been started")

        while not self.terminate_flag.is_set():
            if self.number_of_games == settings.MAX_NUMBER_OF_GAMES:
                continue

            self._send_user_challenge()
            self._do_automatic_matchmaking()

    def challenge_user(self, username = None):
        self.username_queue.append(username)

    def _send_user_challenge(self):
        if len(self.username_queue) > 0:
            username = self.username_queue.pop(0)
            logger.info(f"Sending a challenege request to user {username}")
            response = self.api.create_challenge(username, settings.USER_CHALLENGE_PARAMS)
            logger.info(f"Response from challenge request to {username}: {response}")

    def _do_automatic_matchmaking(self):
        if settings.AUTO_MATCHMAKING == True:
            challenges_stream = self.api.stream_challenges()
            self.challenges = self._parse_stream(challenges_stream)
            if self._challenges_exist():
                self._accept_challenge()
            else:
                self._send_bot_challenge()

    def _parse_stream(self, stream):
        items_in_stream = []
        for line in stream:
            if line:
                line = json.loads(line)
                items_in_stream.append(line)

        if (len(items_in_stream) == 1):
            return items_in_stream[0]

        return tuple(items_in_stream)

    def _challenges_exist(self):
        incoming_challenges = self.challenges["in"]
        return (len(incoming_challenges) > 0)

    def _accept_challenge(self):
        return 0

    def _send_bot_challenge(self):
        online_bots = self.api.stream_online_bots()
        online_bots = self._parse_stream(online_bots)

    def stop(self):
        logger.debug(f"ChallengeHandler received a signal to terminate. Attempting to terminate...")
        self.terminate_flag.set()