import logging

from lichess.IChessGameFactory import IChessGameFactory
from lichess.ChessGame import ChessGame

logger = logging.getLogger(__name__)

class ChessGameFactory(IChessGameFactory):
    def __init__(self, lichess_api, engine):
        logger.debug(f"Creating an instance of {self.__class__.__name__}")
        self.api = lichess_api
        self.engine = engine

    def create_game(self, game_info):
        game = ChessGame(self.api, self.engine, game_info, daemon = False)

        return game