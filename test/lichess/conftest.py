import json
import pytest
import requests
import responses

# This allows us to use monkeypatch in non-function scoped fixtures,
# specifically in disable_network_calls() so we can disable HTTP requests
# during the entire testing session
# see: https://github.com/pytest-dev/pytest/issues/363
@pytest.fixture(scope="session")
def monkeysession():
    with pytest.MonkeyPatch.context() as mp:
        yield mp

# This overrides the responses library so we can't use this. If we forget to mock the HTTP request
# with the responses library then the actual HTTP request will hit the remote server.
# @pytest.fixture(autouse=True, scope="session")
def disable_network_calls(monkeysession):
    """Disable all calls to requests.sessions.Session.request for all tests."""
    def disabled_request():
        raise RuntimeError("HTTP requests not allowed during testing!")
    monkeysession.setattr("requests.sessions.Session.request", lambda *args, **kwargs: disabled_request())

@pytest.fixture(scope="session")
def fake_oauth_token():
    return "fake_oauth_token"

@pytest.fixture(scope="session")
def engine_stub():
    class EngineStub:
        def __init__(self):
            pass
    
    return EngineStub()

# Sample challenge data as how we see it from the lichess api
mock_challenges = [
    {'type': 'challenge', 'challenge': {'id': 'A', 'url': 'https://lichess.org/A', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
    {'type': 'challenge', 'challenge': {'id': 'B', 'url': 'https://lichess.org/B', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
    {'type': 'challenge', 'challenge': {'id': 'C', 'url': 'https://lichess.org/C', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
    {'type': 'challenge', 'challenge': {'id': 'D', 'url': 'https://lichess.org/D', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
    {'type': 'challenge', 'challenge': {'id': 'E', 'url': 'https://lichess.org/E', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}},
    {'type': 'challenge', 'challenge': {'id': 'F', 'url': 'https://lichess.org/F', 'status': 'created', 'challenger': {'id': 'stockai', 'name': 'stockAI', 'title': 'BOT', 'rating': 2000, 'provisional': True, 'online': True}, 'destUser': {'id': 'hgducharme', 'name': 'hgducharme', 'title': None, 'rating': 893, 'online': True}, 'variant': {'key': 'standard', 'name': 'Standard', 'short': 'Std'}, 'rated': False, 'speed': 'bullet', 'timeControl': {'type': 'clock', 'limit': 60, 'increment': 0, 'show': '1+0'}, 'color': 'random', 'finalColor': 'black', 'perf': {'icon': '\ue047', 'name': 'Bullet'}}, 'compat': {'bot': True, 'board': False}}
]

# Sample profile data as how we see it from the lichess API
fake_profile_data = {'id': 'stockai', 'username': 'stockAI', 'perfs': {'blitz': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'bullet': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'correspondence': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'classical': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'rapid': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}}, 'title': 'BOT', 'createdAt': 1648830192548, 'seenAt': 1682201618956, 'playTime': {'total': 2820, 'tv': 0}, 'url': 'https://lichess.org/@/stockAI', 'count': {'all': 36, 'rated': 0, 'ai': 0, 'draw': 0, 'drawH': 0, 'loss': 6, 'lossH': 6, 'win': 30, 'winH': 30, 'bookmark': 0, 'playing': 0, 'import': 0, 'me': 0}, 'followable': True, 'following': False, 'blocking': False, 'followsYou': False}

# Sample events how we would see them from the Lichess API event stream
fake_challenge1 = """{"type": "challenge", "challenge": {"id": "SV0lgdph", "url": "https://lichess.org/SV0lgdph", "status": "created", "challenger": {"id": "stockai", "name": "stockAI", "title": "BOT", "rating": 2000, "provisional": true, "online": true}, "destUser": {"id": "hgducharme", "name": "hgducharme", "title": null, "rating": 867, "online": true}, "variant": {"key": "standard", "name": "Standard", "short": "Std"}, "rated": false, "speed": "bullet", "timeControl": {"type": "clock", "limit": 60, "increment": 0, "show": "1+0"}, "color": "random", "finalColor": "white", "perf": {"icon": "", "name": "Bullet"}}, "compat": {"bot": true, "board": false}}"""
fake_gameStart = """{"type": "gameStart", "game": {"fullId": "SV0lgdphuXLO", "gameId": "SV0lgdph", "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", "color": "white", "lastMove": "", "source": "friend", "variant": {"key": "standard", "name": "Standard"}, "speed": "bullet", "perf": "bullet", "rated": false, "hasMoved": false, "opponent": {"id": "hgducharme", "username": "hgducharme", "rating": 867}, "isMyTurn": true, "secondsLeft": 60, "compat": {"bot": true, "board": false}, "id": "SV0lgdph"}}"""
fake_gameFinish = """{"type": "gameFinish", "game": {"fullId": "SV0lgdphuXLO", "gameId": "SV0lgdph", "fen": "5rk1/p2n1ppp/b3pn2/2p5/7N/6P1/1q1NPPBP/1R1Q1RK1 b - - 1 15", "color": "white", "lastMove": "c1b1", "source": "friend", "variant": {"key": "standard", "name": "Standard"}, "speed": "bullet", "perf": "bullet", "rated": false, "hasMoved": true, "opponent": {"id": "hgducharme", "username": "hgducharme", "rating": 867}, "isMyTurn": false, "secondsLeft": 20, "compat": {"bot": true, "board": false}, "id": "SV0lgdph"}}"""
fake_challenge2 = """{"type": "challenge", "challenge": {"id": "FVDv868k", "url": "https://lichess.org/FVDv868k", "status": "created", "challenger": {"id": "stockai", "name": "stockAI", "title": "BOT", "rating": 2000, "provisional": true, "online": true}, "destUser": {"id": "hgducharme", "name": "hgducharme", "title": null, "rating": 880}, "variant": {"key": "standard", "name": "Standard", "short": "Std"}, "rated": false, "speed": "bullet", "timeControl": {"type": "clock", "limit": 60, "increment": 0, "show": "1+0"}, "color": "random", "finalColor": "white", "perf": {"icon": "", "name": "Bullet"}}, "compat": {"bot": true, "board": false}}"""
fake_challenge2Declined = """{"type": "challengeDeclined", "challenge": {"id": "FVDv868k", "url": "https://lichess.org/FVDv868k", "status": "declined", "challenger": {"id": "stockai", "name": "stockAI", "title": "BOT", "rating": 2000, "provisional": true, "online": true}, "destUser": {"id": "hgducharme", "name": "hgducharme", "title": null, "rating": 880, "online": true}, "variant": {"key": "standard", "name": "Standard", "short": "Std"}, "rated": false, "speed": "bullet", "timeControl": {"type": "clock", "limit": 60, "increment": 0, "show": "1+0"}, "color": "random", "finalColor": "white", "perf": {"icon": "", "name": "Bullet"}, "declineReason": "I'm not accepting challenges at the moment.", "declineReasonKey": "generic"}}"""

# Sample responses we would see from the Lichess API "stream bot game state" end point
fake_gameFull = """{"id":"aI1KG388","variant":{"key":"standard","name":"Standard","short":"Std"},"clock":{"initial":60000,"increment":0},"speed":"bullet","perf":{"name":"Bullet"},"rated":false,"createdAt":1683931685227,"white":{"id":"hgducharme","name":"hgducharme","title":null,"rating":853},"black":{"id":"stockai","name":"stockAI","title":"BOT","rating":2000,"provisional":true},"initialFen":"startpos","type":"gameFull","state":{"type":"gameState","moves":"","wtime":60000,"btime":60000,"winc":0,"binc":0,"status":"started"}}"""
fake_gameState = """{"type":"gameState","moves":"e2e4","wtime":60000,"btime":60000,"winc":0,"binc":0,"status":"started"}"""