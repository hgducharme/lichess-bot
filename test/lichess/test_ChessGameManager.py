from conftest import *

class TestChessGameManager:

    def test_startNewGame_addsGameToCollection(self, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0

        chess_game_manager.start_new_game(fake_gameStart)

        assert chess_game_manager.number_of_games() == 1

    def test_doGamesExist_returnsTrueIfGamesExist(self, chess_game_manager):
        assert chess_game_manager.do_games_exist() == False

        chess_game_manager.start_new_game(fake_gameStart)

        assert chess_game_manager.do_games_exist() == True

    def test_doGamesExist_returnsFalseIfNoGamesExist(self, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0
        assert chess_game_manager.do_games_exist() == False

    @pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 2)])
    def test_numberOfGames_returnsCorrectAnswer(self, chess_game_manager, n, expected):
        for i in range(0, n):
            dummy_unique_game_info = {"game": {"fullId": i}}
            chess_game_manager.start_new_game(dummy_unique_game_info)
        
        assert chess_game_manager.number_of_games() == expected

    def test_startNewGame_callsChessGameFactoryOnceIfGameWasAlreadyAdded(self, chess_game_manager, mock_chess_game_factory):
        chess_game_manager.start_new_game(fake_gameStart)
        chess_game_manager.start_new_game(fake_gameStart)

        assert mock_chess_game_factory.create_game_counter == 1