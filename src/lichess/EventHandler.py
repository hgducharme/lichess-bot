import json
import logging
from threading import Thread

module_logger = logging.getLogger("lichess.event_handler")

class EventHandler(Thread):
    def __init__(self, lichess_api, **kwargs):
        Thread.__init__(self, **kwargs)
        self.logger = logging.getLogger("lichess.event_handler.EventHandler")
        self.logger.info("Creating an instance of EventHandler")
        self.api = lichess_api
        self.is_running = False

    def run(self):
        self.logger.info("An EventHandler thread has been started")
        if self.is_running == False:
            self.is_running == True

        while self.is_running:
            self.logger.debug("EventHandler thread is running")
            event_stream = self.api.stream_events()
            event_stream = self._parse_stream(event_stream)
            self.logger.info(event_stream)
            print(event_stream)

    def _parse_stream(self, stream):
        items_in_stream = []
        for line in stream:
            if line:
                items_in_stream.append(json.loads(line))

        if len(items_in_stream) == 1:
            return tuple(items_in_stream[0])

        return tuple(items_in_stream)
