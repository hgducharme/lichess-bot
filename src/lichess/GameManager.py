import logging
from ChessGame import ChessGame

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, lichess_api):
        logger.debug(f"Creating an instance of {self.__class__.__name__}")
        self.api = lichess_api
        self.games = {}

    def start_new_game(self, game_info):
        logger.debug(f"Starting a new game. Game info: {game_info}")
        game = ChessGame(self.api, game_info)
        game_id = game_info["game"]["fullId"]
        self.games[game_id] = game

    def do_games_exist(self):
        if (self.number_of_games() > 0):
            return True
        
        return False
    
    def number_of_games(self):
        return len(self.games)

    def terminate_game(self, game_id):
        logger.info(f"GameManager is attempting to terminate game: {game_id}...")
        try:
            game = self.games[game_id]
            game.stop()
        except KeyError as err:
            logger.error(f"Tried to terminate game ID {game_id}, but it is not saved in the list of games.")
            pass