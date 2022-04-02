import json
from LichessAPI import LichessAPI
from UserInterface import UserInterface

if __name__ == "__main__":
    with open("/Users/hgducharme/Documents/repos/chessAI/config.json") as file:
        config = json.load(file)

    lichess_token = config["lichessToken"]
    api = LichessAPI(lichess_token)

    request_body = {
        "rated": "false",
        "time": "10",
        "increment": "0",
        "color": "random",
        "variant": "standard",
    }
    
    ui = UserInterface()
    ui.start()