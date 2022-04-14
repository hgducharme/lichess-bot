import logging
from conf import settings
from LichessAPI import LichessAPI
from LichessCLI import LichessCLI

class ThreadFilter(logging.Filter):
    """
    This filter only shows log entries for the specified thread name
    """
    
    def __init__(self, thread_name, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)
        self.thread_name = thread_name

    def filter(self, record):
        return record.threadName == self.thread_name

if __name__ == "__main__":
    logger = logging.getLogger("lichess")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Log handlers
    challenge_handler_fh = logging.FileHandler("./src/lichess/logs/challenge_handler.log")
    event_handler_fh = logging.FileHandler("./src/lichess/logs/event_handler.log")
    lichess_fh = logging.FileHandler("./src/lichess/logs/lichess.log")
    file_handlers = [challenge_handler_fh, event_handler_fh, lichess_fh]

    # Add filters
    thread_filter = ThreadFilter()
    challenge_handler_fh.addFilter(ThreadFilter)
    event_handler_fh.addFilter(ThreadFilter)
    
    for file_handler in file_handlers:
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)

    api = LichessAPI(settings.API_TOKEN)
    cli = LichessCLI(api)
    cli.run()