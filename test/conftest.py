import pytest
import responses
import requests

from lichess.LichessAPI import LichessAPI
from lichess.MockChessGameFactory import MockChessGameFactory
from lichess.ChessGameManager import ChessGameManager

@pytest.fixture(scope='function')
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.fixture(scope = "session", autouse=True)
def empty_json_response():
    return "{}"

@pytest.fixture(scope="module")
def lichess_api():
    api_session = requests.Session()
    api_session.headers.update({"Authorization": f"Bearer fake_oauth_token"})
    return LichessAPI(api_session)


@pytest.fixture(scope="function")
def chess_game_manager(mock_chess_game_factory):
    yield ChessGameManager(mock_chess_game_factory)

    mock_chess_game_factory.create_game_counter = 0

@pytest.fixture(scope="session")
def mock_engine():
    class MockEngine:
        def __init__(self):
            pass

        def set_position(self, position):
            pass

        def get_best_move(self, wtime = None, btime = None):
            pass
    
    return MockEngine()

@pytest.fixture(scope = "session")
def mock_chess_game_factory():
    return MockChessGameFactory()

# Sample profile data as how we see it from the lichess API
fake_profile_data = {'id': 'stockai', 'username': 'stockAI', 'perfs': {'blitz': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'bullet': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'correspondence': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'classical': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'rapid': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}}, 'title': 'BOT', 'createdAt': 1648830192548, 'seenAt': 1682201618956, 'playTime': {'total': 2820, 'tv': 0}, 'url': 'https://lichess.org/@/stockAI', 'count': {'all': 36, 'rated': 0, 'ai': 0, 'draw': 0, 'drawH': 0, 'loss': 6, 'lossH': 6, 'win': 30, 'winH': 30, 'bookmark': 0, 'playing': 0, 'import': 0, 'me': 0}, 'followable': True, 'following': False, 'blocking': False, 'followsYou': False}
fake_non_bot_profile = {'id': 'stockai', 'username': 'stockAI', 'perfs': {'blitz': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'bullet': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'correspondence': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'classical': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'rapid': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}}, 'title': 'NM', 'createdAt': 1648830192548, 'seenAt': 1682201618956, 'playTime': {'total': 2820, 'tv': 0}, 'url': 'https://lichess.org/@/stockAI', 'count': {'all': 36, 'rated': 0, 'ai': 0, 'draw': 0, 'drawH': 0, 'loss': 6, 'lossH': 6, 'win': 30, 'winH': 30, 'bookmark': 0, 'playing': 0, 'import': 0, 'me': 0}, 'followable': True, 'following': False, 'blocking': False, 'followsYou': False}

# Sample events how we would see them from the "stream events" Lichess API end point
# NOTE: These are obvious python dictionaries. To generate more fake events, grab them from the lichess.log file
# These will ultimately get converted to proper JSON objects in order to mock the API response
# These are used to test the EventStreamDispatcher class
fake_gameStart = {'type': 'gameStart', 'game': {'fullId': 'SV0lgdphuXLO', 'gameId': 'SV0lgdph', 'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'color': 'white', 'lastMove': '', 'source': 'friend', 'variant': {'key': 'standard', 'name': 'Standard'}, 'speed': 'bullet', 'perf': 'bullet', 'rated': False, 'hasMoved': False, 'opponent': {'id': 'hgducharme', 'username': 'hgducharme', 'rating': 867}, 'isMyTurn': True, 'secondsLeft': 60, 'compat': {'bot': True, 'board': False}, 'id': 'SV0lgdph'}}
fake_gameFinish = {'type': 'gameFinish', 'game': {'fullId': 'SV0lgdphuXLO', 'gameId': 'SV0lgdph', 'fen': '5rk1/p2n1ppp/b3pn2/2p5/7N/6P1/1q1NPPBP/1R1Q1RK1 b - - 1 15', 'color': 'white', 'lastMove': 'c1b1', 'source': 'friend', 'variant': {'key': 'standard', 'name': 'Standard'}, 'speed': 'bullet', 'perf': 'bullet', 'rated': False, 'hasMoved': True, 'opponent': {'id': 'hgducharme', 'username': 'hgducharme', 'rating': 867}, 'isMyTurn': False, 'secondsLeft': 20, 'compat': {'bot': True, 'board': False}, 'id': 'SV0lgdph'}}
fake_outgoingChallenge = {'type': 'challenge', 'challenge': {'id': 'FVDv868k', 'url': 'https://lichess.org/FVDv868k', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 880}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}}
fake_outgoingChallengeDeclined = {'type': 'challengeDeclined', 'challenge': {'id': 'FVDv868k', 'url': 'https://lichess.org/FVDv868k', 'status': 'declined', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 880, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}, 'declineReason': "I'm not accepting challenges at the moment.", 'declineReasonKey': 'generic'}}
fake_incomingChallenge = {'type': 'challenge', 'challenge': {'id': 'fJmCV8Np', 'url': 'https://lichess.org/fJmCV8Np', 'status': 'created', 'challenger': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 853, 'online': True}, 'destUser': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}}
fake_incomingChallengeCancelled = {'type': 'challengeCanceled', 'challenge': {'id': 'fJmCV8Np', 'url': 'https://lichess.org/fJmCV8Np', 'status': 'canceled', 'challenger': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 853, 'online': True}, 'destUser': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}}

# Sample events from a game where the bot is black and does not move first. We would see these game states
# come in from the "stream bot game state" Lichess API end point
# These are used to test the ChessGame class
fake_game_colorBlack = {'type': 'gameStart', 'game': {'fullId': 'tGwDxEVKcfor', 'gameId': 'tGwDxEVK', 'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'color': 'black', 'lastMove': '', 'source': 'friend', 'variant': {'key': 'standard', 'name': 'Standard'}, 'speed': 'bullet', 'perf': 'bullet', 'rated': False, 'hasMoved': False, 'opponent': {'id': 'hgducharme', 'username': 'hgducharme', 'rating': 893}, 'isMyTurn': False, 'secondsLeft': 60, 'compat': {'bot': True, 'board': False}, 'id': 'tGwDxEVK'}}
fake_gameFull_colorBlack_isNotOurTurn = {'id': 'tGwDxEVK', 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'clock': {'initial': 60000, 'increment': 0}, 'speed': 'bullet', 'perf': {'name': 'Bullet'}, 'rated': False, 'createdAt': 1680120983124, 'white': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893}, 'black': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True}, 'initialFen': 'startpos', 'type': 'gameFull', 'state': {'type': 'gameState', 'moves': '', 'wtime': 60000, 'btime': 60000, 'winc': 0, 'binc': 0, 'status': 'started'}}
fake_gameState_colorBlack_isOurTurn = {'type': 'gameState', 'moves': 'e2e4', 'wtime': 60000, 'btime': 60000, 'winc': 0, 'binc': 0, 'status': 'started'}
fake_gameState_colorBlack_isNotOurTurn = {'type': 'gameState', 'moves': 'e2e4 e7e5', 'wtime': 60000, 'btime': 60000, 'winc': 0, 'binc': 0, 'status': 'started'}

fake_game_colorWhite = {'type': 'gameStart', 'game': {'fullId': 'SV0lgdphuXLO', 'gameId': 'SV0lgdph', 'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'color': 'white', 'lastMove': '', 'source': 'friend', 'variant': {'key': 'standard', 'name': 'Standard'}, 'speed': 'bullet', 'perf': 'bullet', 'rated': False, 'hasMoved': False, 'opponent': {'id': 'hgducharme', 'username': 'hgducharme', 'rating': 867}, 'isMyTurn': True, 'secondsLeft': 60, 'compat': {'bot': True, 'board': False}, 'id': 'SV0lgdph'}}
fake_gameFull_colorWhite_isOurTurn = {'id': 'SV0lgdph', 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'clock': {'initial': 60000, 'increment': 0}, 'speed': 'bullet', 'perf': {'name': 'Bullet'}, 'rated': False, 'createdAt': 1676764517600, 'white': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True}, 'black': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 867}, 'initialFen': 'startpos', 'type': 'gameFull', 'state': {'type': 'gameState', 'moves': '', 'wtime': 60000, 'btime': 60000, 'winc': 0, 'binc': 0, 'status': 'started'}}