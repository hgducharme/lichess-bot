import json
import logging
from conf import settings
from threading import Thread

logger = logging.getLogger(__name__)
class ChallengeHandler(Thread):
    def __init__(self, lichess_api, **kwargs):
        logger.info("Creating an instance of ChallengerHandler")
        Thread.__init__(self, **kwargs)
        self.api = lichess_api
        self.is_running = False
        self.number_of_games = 0
        self.username_queue = []

    def run(self):
        logger.info("A ChallengeHandler thread has been started")
        if self.is_running == False:
            self.is_running = True

        while self.is_running:
            if self.number_of_games == settings.MAX_NUMBER_OF_GAMES:
                continue

            self._send_user_challenge()
            self._handle_automatic_matchmaking()

    def challenge_user(self, username = None):
        self.username_queue.append(username)

    def _send_user_challenge(self):
        if len(self.username_queue) > 0:
            username = self.username_queue.pop(0)
            response = self.api.create_challenge(username, settings.CHALLENGE_PARAMS)
            logger.info(f"Sending a challenege request to user {username}")
            logger.debug(f"Response from challenge request to {username}: {response}")

    def _handle_automatic_matchmaking(self):
        if settings.MATCHMAKING == True:
            self.challenges = self._get_and_parse_challenges()
            if self._challenges_exist():
                self._accept_challenge()
            else:
                self._send_bot_challenge()

    def _get_and_parse_challenges(self):
        challenges = self.api.stream_challenges()
        
        for line in challenges:
            if line:
                challenges = json.loads(line)

        return challenges

    def _challenges_exist(self):
        incoming_challenges = self.challenges["in"]
        return (len(incoming_challenges) > 0)

    def _accept_challenge(self):
        return 0

    def _send_bot_challenge(self):
        return 0