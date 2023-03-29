import logging.config
from stockfish import Stockfish

from src.lichess.conf import settings
from src.lichess.ChallengeStreamWatcher import ChallengeStreamWatcher
from src.lichess.EventStreamWatcher import EventStreamWatcher
from src.lichess.GameManager import GameManager
from src.lichess.LichessAPI import LichessAPI
from src.lichess.LichessCLI import LichessCLI

logger = logging.getLogger(__name__)

def main():
    logger.info("Program has started. Initalizing...")
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # Initialize classes
    api = LichessAPI(settings.API_TOKEN)
    stockfish = Stockfish(path = settings.ENGINE["path"], parameters = settings.ENGINE["stockfish_parameters"])
    game_manager = GameManager(api, stockfish)
    challenge_stream_watcher = ChallengeStreamWatcher(api, game_manager, name = "challenge_stream_watcher", daemon = True)
    event_stream_watcher = EventStreamWatcher(api, game_manager, name = "event_stream_watcher", daemon = True)

    # Start threads
    event_stream_watcher.start()
    challenge_stream_watcher.start()

    # Keep track of threads
    threads = []
    threads.append(challenge_stream_watcher)
    threads.append(event_stream_watcher)

    # Initialize and run main program
    cli = LichessCLI(api, game_manager, challenge_stream_watcher, event_stream_watcher, threads)
    logger.info("Running...")
    cli.run()

if __name__ == "__main__":
    main()