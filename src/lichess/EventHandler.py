import json
import logging
from ContinuousWorker import ContinuousWorker

logger = logging.getLogger(__name__)

class EventHandler(ContinuousWorker):
    def __init__(self, lichess_api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = lichess_api
        self.username = self.api.get_profile().json()["username"]

    def work(self):
        event_stream = self.api.stream_events()

        for line in event_stream:
            if line:
                logger.debug(f"line = {json.loads(line)}")
                self._parse_line(line)
    
    def _parse_line(self, byte):
        line = self._parse_byte(byte)
        event_type = line["type"]
        if event_type == "challenge":
            # The ChallengeHandler class handles all incoming and outgoing challenges, so we will skip this event type
            return
        if event_type == "challengeDeclined":
            return
        if event_type == "gameStart":
            # TODO: Spawn a GameHandler (?)
            return
        if event_type == "gameFinish":
            return
        if event_type == "challengeCancelled":
            return

    def _parse_byte(self, byte):
        return json.loads(str(byte, "utf-8"))