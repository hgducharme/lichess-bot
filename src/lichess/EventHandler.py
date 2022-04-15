import json
import logging
from threading import Thread

logger = logging.getLogger(__name__)

class EventHandler(Thread):
    def __init__(self, lichess_api, **kwargs):
        logger.info("Creating an instance of EventHandler")
        Thread.__init__(self, **kwargs)
        self.api = lichess_api
        self.is_running = False
        self.username = self.api.get_profile().json()["username"]
        logger.debug(self.username)

    def run(self):
        logger.info("An EventHandler thread has been started")

        self._toggle_running_flag()

        while self.is_running:
            event_stream = self.api.stream_events()

            for line in event_stream:
                if line:
                    logger.debug(f"line = {json.loads(line)}")
                    self._parse_line(line)

    def _toggle_running_flag(self):
        self.is_running = (self.is_running == False)

    def _parse_line(self, line):
        category = line["type"]
        if category == "challenge":
            if self.is_external_challenge(line):
                # TODO: Isn't this handled in the ChallengeHandler?
                return 0
            return 0
        if category == "challengeDeclined":
            return 0
        if category == "gameStart":
            return 0
        if category == "gameFinish":
            return 0
        if category == "challengeCancelled":
            return 0

    def is_external_challenge(self, line):
        is_external_challenge = True
        challenger = line["challenge"]["challenger"]["name"]
        if challenger == self.username:
            is_external_challenge = False

        return is_external_challenge