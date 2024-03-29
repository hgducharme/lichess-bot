import logging

logger = logging.getLogger(__name__)

class ChessGameManager:
    def __init__(self, chess_game_factory):
        logger.debug(f"Creating an instance of {self.__class__.__name__}")
        self.chess_game_factory = chess_game_factory
        self._games = {}
        self._is_accepting_games = True

    def start_new_game(self, game_info):
        game_id = game_info["game"]["fullId"]

        if (not self.is_accepting_games):
            logger.info(f"ChessGameManager is not accepting games right now. Rejecting game {game_id}")
            return False
        
        # If the game already exists just return early
        if game_id in self.games:
            logger.info(f"Chess game {game_id} already exists!")
            return True

        game = self.chess_game_factory.create_game(game_info)
        game.start()
        self.games[game_id] = game

        return True

    def do_games_exist(self):
        return (self.number_of_games() > 0)
    
    def number_of_games(self):
        return len(self.games)
    
    def return_when_all_games_are_finished(self):
        for game_id in list(self.games.keys()):
            game = self.games[game_id]
            logger.info(f"ChessGameManager is waiting for game {game_id} to finish...")
            game.join()

    def terminate_all_games(self):
        self.is_accepting_games = False
        for game_id in list(self.games.keys()):
            self.terminate_game(game_id)

    def terminate_game(self, game_id):
        try:
            game = self.games[game_id]
        except KeyError as err:
            logger.error(f"Tried to terminate game {game_id}, but it is not saved in the list of games.")
            return

        logger.info(f"ChessGameManager is attempting to terminate game {game_id}...")
        game.stop()
        logger.debug(f"ChessGameManager is blocking until game {game_id} thread has been killed...")
        game.join()
        logger.info(f"Game {game_id} has ended.")       
        del self.games[game_id]

    @property
    def games(self):
        return self._games

    @property
    def is_accepting_games(self):
        return self._is_accepting_games
    
    @is_accepting_games.setter
    def is_accepting_games(self, value):
        if (not isinstance(value, bool)):
            raise TypeError("is_accepting_games can only be either 'True' or 'False'")
        self._is_accepting_games = value
