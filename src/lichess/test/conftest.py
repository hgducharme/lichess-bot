import pytest
import requests

# TODO: This is probably how we mock our Session() object:
# https://docs.pytest.org/en/latest/how-to/monkeypatch.html#monkeypatching-returned-objects-building-mock-classes

# @pytest.fixture
# def disable_network_calls(monkeypatch):
#     def stunted_get():
#         raise RuntimeError("Network access not allowed during testing!")
#     monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())

# TODO: Figure out how to raise a runtime error in this function similar to the above function.
@pytest.fixture(autouse=True)
def disable_network_calls(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")

def mock_requests_session(mocker):
    mock_session = mocker.patch.object(requests, 'Session', autospec=True)
    mock_session.return_value.__enter__.return_value = mock_session
    return mock_session

@pytest.fixture
def mock_oauth_token():
    return "mock_oauth_token"

class EngineStub:
    def __init__(self):
        pass

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
sample_profile_data = {'id': 'stockai', 'username': 'stockAI', 'perfs': {'blitz': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'bullet': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'correspondence': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'classical': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}, 'rapid': {'games': 0, 'rating': 2000, 'rd': 500, 'prog': 0, 'prov': True}}, 'title': 'BOT', 'createdAt': 1648830192548, 'seenAt': 1682201618956, 'playTime': {'total': 2820, 'tv': 0}, 'url': 'https://lichess.org/@/stockAI', 'count': {'all': 36, 'rated': 0, 'ai': 0, 'draw': 0, 'drawH': 0, 'loss': 6, 'lossH': 6, 'win': 30, 'winH': 30, 'bookmark': 0, 'playing': 0, 'import': 0, 'me': 0}, 'followable': True, 'following': False, 'blocking': False, 'followsYou': False}