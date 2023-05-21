import logging.config
import requests
from stockfish import Stockfish

from lichess.conf import settings
from lichess.ChallengeSender import ChallengeSender
from lichess.EventStreamDispatcher import EventStreamDispatcher
from lichess.ChessGameManager import ChessGameManager
from lichess.LichessAPI import LichessAPI
from lichess.LichessCLI import LichessCLI
from lichess.ChessGameFactory import ChessGameFactory

logger = logging.getLogger(__name__)

def main():
    logger.info("Program has started. Initalizing...")
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # Initialize classes
    api_session = requests.Session()
    api_session.headers.update({"Authorization": f"Bearer {settings.API_TOKEN}"})
    api = LichessAPI(api_session)
    stockfish = Stockfish(path = settings.ENGINE["path"], parameters = settings.ENGINE["stockfish_parameters"])
    chess_game_factory = ChessGameFactory(api, stockfish)
    chess_game_manager = ChessGameManager(chess_game_factory)
    challenge_sender = ChallengeSender(api)
    event_stream_watcher = EventStreamDispatcher(api, chess_game_manager, name = "event_stream_watcher", daemon = True)

    # Start threads
    event_stream_watcher.start()

    # Keep track of threads
    threads = []
    threads.append(event_stream_watcher)

    # Initialize and run main program
    cli = LichessCLI(api, chess_game_manager, challenge_sender, event_stream_watcher, threads)
    logger.info("Running...")
    cli.run()

if __name__ == "__main__":
    main()