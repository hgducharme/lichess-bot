import logging.config
from conf import settings
from LichessAPI import LichessAPI
from LichessCLI import LichessCLI

logger = logging.getLogger(__name__)

def main():
    logger.info("Program has started. Initalizing...")
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    api = LichessAPI(settings.API_TOKEN)
    cli = LichessCLI(api)
    logger.info("Running...")
    cli.run()

if __name__ == "__main__":
    main()