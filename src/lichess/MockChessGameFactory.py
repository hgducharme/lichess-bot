from lichess.IChessGameFactory import IChessGameFactory

class MockChessGameFactory(IChessGameFactory):
    def __init__(self):
        pass

    def create_game(self, game_info):
        return {}