import abc

class IChessGameFactory(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def create_game(self, game_info):
        pass