import logging
from ChessGame import ChessGame

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, lichess_api, engine):
        logger.debug(f"Creating an instance of {self.__class__.__name__}")
        self.api = lichess_api
        self.engine = engine
        self.games = {}
        self.accepting_games = True

    def start_new_game(self, game_info):
        game_id = game_info["game"]["fullId"]

        if (not self.accepting_games):
            logger.info(f"GameManager is not accepting games right now. Rejecting game {game_id}")
            return False

        logger.info(f"Starting a new game. Game info: {game_info}")
        game = ChessGame(self.api, self.engine, game_info)
        self.games[game_id] = game
        game.start()

        return True

    def do_games_exist(self):
        if (self.number_of_games() > 0):
            return True
        
        return False
    
    def number_of_games(self):
        return len(self.games)

    def terminate(self, wait = True):
        for game_id in list(self.games.keys()):
            self.terminate_game(game_id, wait)

    def terminate_game(self, game_id, wait = False):
        try:
            game = self.games[game_id]
        except KeyError as err:
            logger.error(f"Tried to terminate game {game_id}, but it is not saved in the list of games.")
            return

        if wait:
            logger.info(f"GameManager is waiting for game {game_id} to finish...")
        else:
            logger.info(f"GameManager is attempting to terminate game {game_id}...")
            game.stop()
            logger.debug(f"GameManager is blocking until game {game_id} thread has been killed...")

        # TODO: This hangs
        # https://stackoverflow.com/questions/47380442/joining-a-daemon-thread
        game.join()
        logger.info(f"Game {game_id} has ended.")
        
        del self.games[game_id]

    def stop_accepting_games(self):
        self.accepting_games = False