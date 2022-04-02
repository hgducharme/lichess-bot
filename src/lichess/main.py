import json
from LichessAPI import LichessAPI
from LichessCLI import LichessCLI

def load_config(key):
    with open("/Users/hgducharme/Documents/repos/chessAI/config.json") as file:
        config = json.load(file)

    return config[key]

if __name__ == "__main__":
    lichess_token = load_config("lichessToken")
    api = LichessAPI(lichess_token)
    cli = LichessCLI(api)
    cli.run()