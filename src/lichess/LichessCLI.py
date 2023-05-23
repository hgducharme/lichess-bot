import logging

from lichess.conf import settings

logger = logging.getLogger(__name__)

MENU_OPTIONS = {
    1: f"Toggle automatic matchmaking",
    2: "Challenge the AI",
    3: "Challenge a user",
    4: "Help",
    5: "Quit"
}

class LichessCLI:
    def __init__(self, lichess_api, chess_game_manager, challenge_sender, event_stream_watcher, threads):
        self.is_running = True
        self.api = lichess_api
        self.chess_game_manager = chess_game_manager
        self.challenge_sender = challenge_sender
        self.event_stream_watcher = event_stream_watcher
        self.threads = threads

    def run(self):
        print("Welcome to the Lichess CLI tool. Please select one of the commands below: ")

        while self.is_running:
            self._print_menu()
            try:
                command = int(input("Enter your choice: "))
            except ValueError as e:
                print("")
                print("ERROR: your command must be an integer")
                continue

            if (command == 1):
                self._toggle_automatic_matchmaking()
            elif (command == 2):
                self._challenge_ai()
            elif (command == 3):
                user = input("Enter a username: ")
                self._challenge_user(user)
            elif (command == 4):
                self._print_menu()
            elif (command == 5):
                self._quit()
            else:
                print("Sorry, that is not a valid option. Please try again.")

    def _print_menu(self):
        print("")
        for key in MENU_OPTIONS.keys():
            print(f"{key}. -- {MENU_OPTIONS[key]}")

    def _toggle_automatic_matchmaking(self):
        settings.AUTO_MATCHMAKING = not settings.AUTO_MATCHMAKING
        print(f"Automatic matchmaking set to: {settings.AUTO_MATCHMAKING}")

    def _challenge_ai(self):
        return 0

    def _challenge_user(self, username):
        self.challenge_sender.send_challenge(username, settings.CHALLENGE_PARAMS["real_time"])
        
    def _quit(self):
        continue_to_quit = self._confirm_quit_command()
        if continue_to_quit:
            logger.info("Quitting the program.")
            self._close_all_games()
            self._close_all_threads()
            self.is_running = False

    def _confirm_quit_command(self):
        command = input("Are you sure you want to quit? ((Y)es, (N)o): ")
        valid_commands = ("yes", "y", "no", "n")
        while (command.strip().lower() not in valid_commands):
            command = input("((Y)es, (N)o)): ")
            command = command.strip().lower()

        if command == "y" or command == "yes":
            return True
        else:
            return False

    def _close_all_games(self):
        if self.chess_game_manager.do_games_exist():
            command = input(f"There are currently {self.chess_game_manager.number_of_games()} game(s) being played. Do you want to terminate all games? [(Y)es, (N)o]: ")

            valid_commands = ("yes", "y", "no", "n")
            while (command.strip().lower() not in valid_commands):
                command = input("((Y)es, (N)o): ")
                command = command.strip().lower()

            if command == "y" or command == "yes":
                print("Terminating all games...")
                # TODO: This story wont work because chess_game_manager calls
                # chess_game.stop() and that sets the stop event flag, but the thread
                # is in an infinite loop reading from the game stream, so it won't
                # exit out to the loop inside ContinuousWorker and see the stop event flag
                # has been set. We might need to do the same thing we did in EventStreamDispatcher
                # with the next() function.
                self.chess_game_manager.terminate_all_games()

            elif command == "n" or command == "no":
                print("The program will end once all games have finished...")

                # Make sure no games get started or challenges get accepted
                settings.ACCEPTING_CHALLENGES = False
                settings.AUTO_MATCHMAKING = False

                self.chess_game_manager.return_when_all_games_are_finished()

    def _close_all_threads(self):
        for thread in self.threads:
            thread.stop()
        
        for thread in self.threads:
            thread.join(10)