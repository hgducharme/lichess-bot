import json
import argparse
from conf import settings

from ChallengeHandler import ChallengeHandler

# TODO: Maybe make this an enum?
MENU_OPTIONS = {
    1: "Automatic matchmaking",
    2: "Challenge the AI",
    3: "Challenge a user",
    4: "Help",
    5: "Quit"
}

class LichessCLI:
    def __init__(self, lichess_api):
        self.is_running = True
        self.api = lichess_api

    def run(self):
        print("Welcome to the Lichess CLI tool. Please select one of the commands below: ")
        self._print_menu()

        while self.is_running:
            command = int(input("Enter your choice: "))

            if (command == 1):
                self._matchmaking()
            elif (command == 2):
                self._challenge_ai()
            elif (command == 3):
                user = input("Enter the username: ")
                self._challenge_user(user)
            elif (command == 4):
                self._print_menu()
            elif (command == 5):
                '''
                TODO:
                1) Detect Ctrl-C and route it to this option
                2) Gracefully shut down all threads and release their memory
                '''
                self._quit()
            else:
                print("Sorry, I don't understand that command. Please try again.")

    def _print_menu(self):
        for key in MENU_OPTIONS.keys():
            print(f"{key}. -- {MENU_OPTIONS[key]}")

    def _matchmaking(self):
        challenge_handler = ChallengeHandler(self.api, name = "challenge_handler_thread", daemon = True)
        challenge_handler.start()

        online_bots = self._get_and_parse_online_bots()
        # event_stream = self._get_and_parse_event_stream()

    def _get_and_parse_online_bots(self):
        online_bots = self.api.stream_online_bots()
        online_bots = self._parse_stream(online_bots)

        return online_bots

    def _get_and_parse_event_stream(self):
        event_stream = self.api.stream_events()
        event_stream = self._parse_stream(event_stream)

        return event_stream

    def _challenge_ai(self):
        return 0

    def _challenge_user(self, username):
        response = self.api.create_challenge(username, settings.CHALLENGE_PARAMS)
        
        
    def _quit(self):
        self.is_running = False

    def _parse_stream(self, stream):
        items_in_stream = []
        for line in stream:
            if line:
                items_in_stream.append(json.loads(line))

        if len(items_in_stream) == 1:
            return items_in_stream[0]

        return tuple(items_in_stream)