import json
import logging
from ContinuousWorker import ContinuousWorker

logger = logging.getLogger(__name__)

class EventStreamWatcher(ContinuousWorker):
    def __init__(self, lichess_api, game_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = lichess_api
        self.game_manager = game_manager
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
            self.game_manager.start_new_game(line)
            return
        if event_type == "gameFinish":
            return
        if event_type == "challengeCancelled":
            return

    def _parse_byte(self, byte):
        return json.loads(str(byte, "utf-8"))