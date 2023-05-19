import logging

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, chess_game_factory):
        logger.debug(f"Creating an instance of {self.__class__.__name__}")
        self.chess_game_factory = chess_game_factory
        self.games = {}
        self.accepting_games = True

    def start_new_game(self, game_info):
        game_id = game_info["game"]["fullId"]

        if (not self.accepting_games):
            logger.info(f"GameManager is not accepting games right now. Rejecting game {game_id}")
            return False

        game = self.chess_game_factory.create_game(game_info)
        self.games[game_id] = game

        return True

    def do_games_exist(self):
        if (self.number_of_games() > 0):
            return True
        
        return False
    
    def number_of_games(self):
        return len(self.games)

    def terminate_all_games(self, wait = True):
        self.stop_accepting_games()
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

            # game.join()
            # TODO: We join to a game, waiting for it to finish, and when the event_stream_watcher
            # class gets a game finish it also trys to terminate the game, it stops it, then we resume right here,
            # and try to do everything again but the thread no longer exists, and we get an error when we 
            # try to "del self.games[game_id]"
        else:
            logger.info(f"GameManager is attempting to terminate game {game_id}...")
            game.stop()
            logger.debug(f"GameManager is blocking until game {game_id} thread has been killed...")
            game.join()
            logger.info(f"Game {game_id} has ended.")
            
            del self.games[game_id]

    def stop_accepting_games(self):
        self.accepting_games = False