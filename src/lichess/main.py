import json
from LichessClient import LichessClient

if __name__ == "__main__":
    with open("/Users/hgducharme/Documents/repos/chessAI/config.json") as file:
        config = json.load(file)

    lichess_token = config["lichessToken"]
    lichessClient = LichessClient(lichess_token)