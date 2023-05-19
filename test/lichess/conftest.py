import pytest
import responses

@pytest.fixture(scope='session')
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps

@pytest.fixture(scope = "session", autouse=True)
def empty_json_response():
    return "{}"

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

# Sample profile data as how we see it from the lichess API
fake_profile_data = {'id': 'stockai', 'username': 'stockAI', 'perfs': {'blitz': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'bullet': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'correspondence': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'classical': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'rapid': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}}, 'title': 'BOT', 'createdAt': 1648830192548, 'seenAt': 1682201618956, 'playTime': {'total': 2820, 'tv': 0}, 'url': 'https://lichess.org/@/stockAI', 'count': {'all': 36, 'rated': 0, 'ai': 0, 'draw': 0, 'drawH': 0, 'loss': 6, 'lossH': 6, 'win': 30, 'winH': 30, 'bookmark': 0, 'playing': 0, 'import': 0, 'me': 0}, 'followable': True, 'following': False, 'blocking': False, 'followsYou': False}

# Sample events how we would see them from the Lichess API event stream
# NOTE: These are obvious python dictionaries. To generate more fake events, grab them from the lichess.log file
# These will ultimately get converted to proper JSON objects in order to mock the API response
fake_gameStart = {'type': 'gameStart', 'game': {'fullId': 'SV0lgdphuXLO', 'gameId': 'SV0lgdph', 'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'color': 'white', 'lastMove': '', 'source': 'friend', 'variant': {'key': 'standard', 'name': 'Standard'}, 'speed': 'bullet', 'perf': 'bullet', 'rated': False, 'hasMoved': False, 'opponent': {'id': 'hgducharme', 'username': 'hgducharme', 'rating': 867}, 'isMyTurn': True, 'secondsLeft': 60, 'compat': {'bot': True, 'board': False}, 'id': 'SV0lgdph'}}
fake_gameFinish = {'type': 'gameFinish', 'game': {'fullId': 'SV0lgdphuXLO', 'gameId': 'SV0lgdph', 'fen': '5rk1/p2n1ppp/b3pn2/2p5/7N/6P1/1q1NPPBP/1R1Q1RK1 b - - 1 15', 'color': 'white', 'lastMove': 'c1b1', 'source': 'friend', 'variant': {'key': 'standard', 'name': 'Standard'}, 'speed': 'bullet', 'perf': 'bullet', 'rated': False, 'hasMoved': True, 'opponent': {'id': 'hgducharme', 'username': 'hgducharme', 'rating': 867}, 'isMyTurn': False, 'secondsLeft': 20, 'compat': {'bot': True, 'board': False}, 'id': 'SV0lgdph'}}
fake_outgoingChallenge = {'type': 'challenge', 'challenge': {'id': 'FVDv868k', 'url': 'https://lichess.org/FVDv868k', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 880}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}}
fake_outgoingChallengeDeclined = {'type': 'challengeDeclined', 'challenge': {'id': 'FVDv868k', 'url': 'https://lichess.org/FVDv868k', 'status': 'declined', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 880, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}, 'declineReason': "I'm not accepting challenges at the moment.", 'declineReasonKey': 'generic'}}
fake_incomingChallenge = {'type': 'challenge', 'challenge': {'id': 'fJmCV8Np', 'url': 'https://lichess.org/fJmCV8Np', 'status': 'created', 'challenger': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 853, 'online': True}, 'destUser': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}}
fake_incomingChallengeCancelled = {'type': 'challengeCanceled', 'challenge': {'id': 'fJmCV8Np', 'url': 'https://lichess.org/fJmCV8Np', 'status': 'canceled', 'challenger': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 853, 'online': True}, 'destUser': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'white', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}}

# Sample responses we would see from the Lichess API "stream bot game state" end point
fake_gameFull = {'id': 'aI1KG388', 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'clock': {'initial': 60000, 'increment': 0}, 'speed': 'bullet', 'perf': {'name': 'Bullet'}, 'rated': False, 'createdAt': 1683931685227, 'white': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 853}, 'black': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True}, 'initialFen': 'startpos', 'type': 'gameFull', 'state': {'type': 'gameState', 'moves': '', 'wtime': 60000, 'btime': 60000, 'winc': 0, 'binc': 0, 'status': 'started'}}
fake_gameState = {'type': 'gameState', 'moves': 'e2e4', 'wtime': 60000, 'btime': 60000, 'winc': 0, 'binc': 0, 'status': 'started'}