import json
import argparse

MENU_OPTIONS = {
    1: "Matchmaking",
    2: "Challenge the AI",
    3: "Help",
    4: "Quit"
}

class LichessCLI:
    def __init__(self, lichessAPI):
        self.is_running = True
        self.api = lichessAPI

    def run(self):
        print("Welcome to the Lichess CLI tool. Please select one of the commands below: ")
        self.__print_menu()

        while self.is_running:
            command = int(input("Enter your choice: "))

            if (command == 1):
                self.__matchmaking()
            elif (command == 2):
                self.__challenge_ai()
            elif (command == 3):
                self.__print_menu()
            elif (command == 4):
                self.__quit()
            else:
                print("Sorry, I don't understand that command. Please try again.")


    def __print_menu(self):
        for key in MENU_OPTIONS.keys():
            print(f"{key}. -- {MENU_OPTIONS[key]}")

    def __matchmaking(self):
        '''
        1) get list of bots online
        2) check for challenge requests
        3) prioritize challenge requests, so pull one off the stack that we want. For now, let's pick the first one.
        4) accept it
        5) read the game stream
        6) read the event stream
        '''

        online_bots = self.api.stream_online_bots()
        online_bots = self._parse_stream(online_bots)
        challenge_requests = self.api.stream_challenges()
        challenge_requests = self._parse_stream(challenge_requests)

    def __challenge_ai(self):
        return 0
        
    def __quit(self):
        self.is_running = False

    def _parse_stream(self, stream):
        items_in_stream = []
        for line in stream:
            if line:
                items_in_stream.append(json.loads(line))

        return tuple(items_in_stream)