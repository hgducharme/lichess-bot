import json
import logging
import threading

logger = logging.getLogger(__name__)

class EventHandler(threading.Thread):
    def __init__(self, lichess_api, **kwargs):
        logger.info("Creating an instance of EventHandler")
        threading.Thread.__init__(self, **kwargs)
        self.api = lichess_api
        self.terminate_flag = threading.Event()
        self.username = self.api.get_profile().json()["username"]
        logger.debug(self.username)

    def run(self):
        logger.info("An EventHandler thread has been started")

        while not self.terminate_flag.is_set():
            event_stream = self.api.stream_events()

            for line in event_stream:
                if line:
                    logger.debug(f"line = {json.loads(line)}")
                    self._parse_line(line)

    def _parse_line(self, byte):
        line = self._parse_byte(byte)
        event_type = line["type"]
        if event_type == "challenge":
            if self.is_external_challenge(line):
                # TODO: Isn't this handled in the ChallengeHandler?
                return 0
            return 0
        if event_type == "challengeDeclined":
            return 0
        if event_type == "gameStart":
            return 0
        if event_type == "gameFinish":
            return 0
        if event_type == "challengeCancelled":
            return 0

    def _parse_byte(self, byte):
        return json.loads(str(byte, "utf-8"))

    def is_external_challenge(self, line):
        is_external_challenge = True
        challenger = line["challenge"]["challenger"]["name"]
        if challenger == self.username:
            is_external_challenge = False

        return is_external_challenge