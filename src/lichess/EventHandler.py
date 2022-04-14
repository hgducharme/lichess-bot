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

    def run(self):
        logger.info("An EventHandler thread has been started")
        if self.is_running == False:
            self.is_running = True

        while self.is_running:
            event_stream = self.api.stream_events()
            event_stream = self._parse_stream(event_stream)
            logger.debug(f"Event stream output - {event_stream}")

    def _parse_stream(self, stream):
        items_in_stream = []
        for line in stream:
            if line:
                items_in_stream.append(json.loads(line))

        if len(items_in_stream) == 1:
            return tuple(items_in_stream[0])

        return tuple(items_in_stream)
