import json
import logging
from conf import settings

from ChallengeHandler import ChallengeHandler
from EventHandler import EventHandler

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
        self.threads = []

        self.challenge_handler = ChallengeHandler(self.api, name = "challenge_handler_thread", daemon = True)
        self.challenge_handler.start()
        self.threads.append(self.challenge_handler)

        self.event_handler = EventHandler(self.api, name = "event_handler_thread", daemon = True)
        self.event_handler.start()
        self.threads.append(self.event_handler)

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
                user = input("Enter a username: ")
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
        self.challenge_handler.challenge_user(username)
        
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