from lichess.IChessGameFactory import IChessGameFactory

class MockChessGame:
    def __init__(self, game_info):
        self.game_info = game_info
        self.start_counter = 0
        self.stop_counter = 0
        self.join_counter = 0

    def start(self):
        self.start_counter += 1

    def stop(self):
        self.stop_counter += 1

    def join(self):
        self.join_counter +=1

class MockChessGameFactory(IChessGameFactory):
    def __init__(self):
        self.create_game_counter = 0

    def create_game(self, game_info):
        self.create_game_counter += 1
        return MockChessGame(game_info)