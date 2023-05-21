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
        self._create_game_counter = 0

    def create_game(self, game_info):
        self.create_game_counter += 1
        return MockChessGame(game_info)
    
    @property
    def create_game_counter(self):
        return self._create_game_counter
    
    @create_game_counter.setter
    def create_game_counter(self, value):
        if ( (not isinstance(value, int)) or (value < 0)):
            raise ValueError("create_game_counter must be an integer greater than or equal to zero")
        self._create_game_counter = value