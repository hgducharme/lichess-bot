import json
import logging
from ContinuousWorker import ContinuousWorker

logger = logging.getLogger(__name__)

class ChessGame(ContinuousWorker):
    def __init__(self, lichess_api, engine, game_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = lichess_api
        self.engine = engine
        self.info = game_info
        self.color = game_info["game"]["color"]
        self.game_id = self.info["game"]["fullId"]

    def work(self):
        game_stream = self.api.stream_game_state(self.game_id)
        for byte in game_stream:
            if byte:
                logger.debug(f"From game stream: {json.loads(byte)}")
                line = self._parse_byte(byte)
                self._store_game_state(line)
                self._move()

    def _parse_byte(self, byte):
        return json.loads(str(byte, "utf-8"))

    def _store_game_state(self, line):
        line_type = line["type"]
        if line_type == "gameFull":
            self.full_game_info = line
            self.game_state = line["state"]
        elif line_type == "gameState":
            self.game_state = line
        else:
            pass

    def _move(self):
        # TODO: This for some reason isn't working if the first move is ours.
        if (self.is_our_turn()):
            logger.debug("It's our turn. Getting move from engine...")
            moves = self.get_moves()
            self.engine.set_position(moves)
            best_move = self.engine.get_best_move(wtime = self.game_state["wtime"], btime = self.game_state["btime"])
            logger.debug(f"Best move = {best_move}")
            self.api.move(self.game_id, best_move)

    def is_our_turn(self):
        # If we're white and there is an even number recorded of moves, then it's our turn.
        # If we're black and there is an odd number recorded of moves, then it's our turn.

        number_of_moves = self.get_number_of_moves()
        if (self.color == "white" and number_of_moves % 2 == 0):
            return True
        elif (self.color == "black" and number_of_moves % 2 != 0):
            return True

        return False

    def _cleanup(self):
        # If the game is currently running, then abort or resign. Otherwise, do nothing
        # TODO: This MIGHT be a race condition. If EventStreamWatcher tells us to terminate the game and we reach
        # this before ChessGame gets a new state that says the game is finished, this might try to execute
        if self.game_state["status"] == "started":
            self._abort_or_resign()

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
        # A "moves" string from the Lichess API will look like: "e2e4 c7c5 f2f4 d7d6 ..."
        # The first move will be an empty string: ""
        moves_string = self.game_state["moves"].strip()

        # If the string is empty then there hasn't been any moves
        # but if we .split() the string then we will get 1 entry into the moves tuple,
        # so if the string is empty we need to return an empty tuple
        if (moves_string == ""):
                return tuple()
        
        return tuple(moves_string.split(" "))