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
        self._print_menu()

        while self.is_running:
            command = int(input("Enter your choice: "))

            if (command == 1):
                self._matchmaking()
            elif (command == 2):
                self._challenge_ai()
            elif (command == 3):
                self._print_menu()
            elif (command == 4):
                self._quit()
            else:
                print("Sorry, I don't understand that command. Please try again.")

    def _print_menu(self):
        for key in MENU_OPTIONS.keys():
            print(f"{key}. -- {MENU_OPTIONS[key]}")

    def _matchmaking(self):
        online_bots = self._get_and_parse_online_bots()
        challenges = self._get_and_parse_challenges()
        event_stream = self._get_and_parse_event_stream()

    def _get_and_parse_online_bots(self):
        online_bots = self.api.stream_online_bots()
        online_bots = self._parse_stream(online_bots)

        return online_bots

    def _get_and_parse_challenges(self):
        challenges = self.api.stream_challenges()
        challenges = self._parse_stream(challenges)

        return challenges

    def _get_and_parse_event_stream(self):
        event_stream = self.api.stream_events()
        event_stream = self._parse_stream(event_stream)

        return event_stream

    def _challenge_ai(self):
        return 0
        
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