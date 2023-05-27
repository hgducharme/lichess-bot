from conftest import *

class TestChessGameManager:

    def test_startNewGame_addsGameToCollection(self, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0

        game_started = chess_game_manager.start_new_game(fake_gameStart)

        assert game_started == True
        assert chess_game_manager.number_of_games() == 1

    def test_doGamesExist_returnsTrueIfGamesExist(self, chess_game_manager):
        assert chess_game_manager.do_games_exist() == False

        game_started = chess_game_manager.start_new_game(fake_gameStart)

        assert game_started == True
        assert chess_game_manager.do_games_exist() == True

    def test_doGamesExist_returnsFalseIfNoGamesExist(self, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0
        assert chess_game_manager.do_games_exist() == False

    @pytest.mark.parametrize("n, expected", [(0, 0), (1, 1), (2, 2)])
    def test_numberOfGames_returnsCorrectAnswer(self, chess_game_manager, n, expected):
        for i in range(0, n):
            dummy_unique_game_info = {"game": {"fullId": i}}
            game_started = chess_game_manager.start_new_game(dummy_unique_game_info)
            assert game_started == True
        
        assert chess_game_manager.number_of_games() == expected

    def test_startNewGame_startsGameOnlyOnceIfGameWasAlreadyAdded(self, chess_game_manager, mock_chess_game_factory):
        game_started1 = chess_game_manager.start_new_game(fake_gameStart)
        game_started2 = chess_game_manager.start_new_game(fake_gameStart)        

        assert game_started1 == True
        assert game_started2 == True
        assert mock_chess_game_factory.create_game_counter == 1

    def test_startNewGame_rejectsGameIfNotAcceptingGamesIsTrue(self, chess_game_manager, mock_chess_game_factory):
        chess_game_manager.is_accepting_games = False

        game_started = chess_game_manager.start_new_game(fake_gameStart)

        assert game_started == False
        assert mock_chess_game_factory.create_game_counter == 0

    def test_terminateAllGames_deletesAllGames(self, chess_game_manager):
        import copy

        assert chess_game_manager.number_of_games() == 0

        game_id1 = fake_gameStart["game"]["fullId"]

        # Create a second game
        game_id2 = game_id1 + "2"
        fake_game2 = copy.deepcopy(fake_gameStart)
        fake_game2["game"]["fullId"]  = game_id2

        game_started1 = chess_game_manager.start_new_game(fake_gameStart)
        game_started2 = chess_game_manager.start_new_game(fake_game2)

        assert game_started1 == True
        assert game_started2 == True

        games = chess_game_manager.games

        chess_game_manager.terminate_all_games()

        assert chess_game_manager.number_of_games() == 0
        for game in games:
            assert game.stop_counter == 1
            assert game.join_counter == 1

    def test_terminateGame_stopsAndJoinsToThreadAndDeletesGameFromRepository(self, chess_game_manager):
        assert chess_game_manager.number_of_games() == 0

        game_id = fake_gameStart["game"]["fullId"]
        chess_game_manager.start_new_game(fake_gameStart)

        game = chess_game_manager.games[game_id]

        chess_game_manager.terminate_game(game_id)

        assert game.stop_counter == 1
        assert game.join_counter == 1
        assert chess_game_manager.number_of_games() == 0

    def test_terminateGame_doesNotThrowExceptionIfGameIsNotFound(self, chess_game_manager):
        game_id = fake_gameStart["game"]["fullId"]
        try:
            chess_game_manager.terminate_game(game_id)
        except KeyError as err:
            assert False, f"fake_gameStart with ID {game_id} raised a KeyError exception."

    @pytest.mark.parametrize("value", [1, "value", [], {}, ])
    def test_isAcceptingGamesProperty_onlyAllowsBooleanValues(self, chess_game_manager, value):
        with pytest.raises(TypeError):
            chess_game_manager.is_accepting_games = value

    def test_returnWhenAllGamesAreFinished_joinsToThread(self, chess_game_manager):
        chess_game_manager.start_new_game(fake_gameStart)

        game = chess_game_manager.games[fake_gameStart["game"]["fullId"]]

        chess_game_manager.return_when_all_games_are_finished()

        assert game.join_counter == 1