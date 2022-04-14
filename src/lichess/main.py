import logging.config
from conf import settings
from LichessAPI import LichessAPI
from LichessCLI import LichessCLI

if __name__ == "__main__":

    # Initalize logging
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    api = LichessAPI(settings.API_TOKEN)
    cli = LichessCLI(api)
    cli.run()