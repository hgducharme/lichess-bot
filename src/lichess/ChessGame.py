import json
import logging
from ContinuousWorker import ContinuousWorker

logger = logging.getLogger(__name__)

class ChessGame(ContinuousWorker):
    def __init__(self, lichess_api, game_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = lichess_api
        self.info = game_info
        self.game_id = self.info["game"]["fullId"]

    def work(self):
        game_stream = self.api.stream_game_state(self.game_id)
        for line in game_stream:
            if line:
                logger.debug(f"From game stream: {json.loads(line)}")
                line = self._parse_byte(line)
                self._dispatch_action(line)

    def _parse_byte(self, byte):
        return json.loads(str(byte, "utf-8"))

    def _dispatch_action(self, line):
        line_type = line["type"]
        if line_type == "gameFull":
            pass
        elif line_type == "gameState":
            self.game_state = line
        return

    def _cleanup(self):
        # If the game is currently running, then abort or resign. Otherwise, do nothing
        if self.game_state["status"] == "started":
            self._resign_or_abort()

    def _abort_or_resign(self):
        number_of_moves = self.get_number_of_moves()
        if (number_of_moves > 1):
            logger.info(f"Resigning game {self.game_id}")
            response = self.api.resign_game(self.game_id)
        else:
            logger.info(f"Aborting game {self.game_id}")
            response = self.api.abort_game(self.game_id)

        # TODO: What should we do if the abort or resignation request was unsucessful?

    def get_number_of_moves(self):
        return len(self.get_moves())

    def get_moves(self):
        # Sample moves string from the Lichess API: "e2e4 c7c5 f2f4 d7d6 ..."
        moves = tuple(self.game_state["moves"].strip().split(" "))
        return moves