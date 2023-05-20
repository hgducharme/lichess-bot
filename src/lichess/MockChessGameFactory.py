from lichess.IChessGameFactory import IChessGameFactory

class MockChessGame:
    def __init__(self, game_info):
        self.game_info = game_info
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass

class MockChessGameFactory(IChessGameFactory):
    def __init__(self):
        pass

    def create_game(self, game_info):
        return MockChessGame(game_info)