import logging
from conf import settings
from LichessAPI import LichessAPI
from LichessCLI import LichessCLI

if __name__ == "__main__":
    logger = logging.getLogger("lichess")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("lichess.log")
    file_handler.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    api = LichessAPI(settings.API_TOKEN)
    cli = LichessCLI(api)
    cli.run()