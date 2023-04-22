import logging

from src.lichess.conf import settings

logger = logging.getLogger(__name__)

# TODO: Maybe make this an enum?
MENU_OPTIONS = {
    1: f"Toggle automatic matchmaking",
    2: "Challenge the AI",
    3: "Challenge a user",
    4: "Help",
    5: "Quit"
}

class LichessCLI:
    def __init__(self, lichess_api, game_manager, challenge_stream_watcher, event_stream_watcher, threads):
        self.is_running = True
        self.api = lichess_api
        self.game_manager = game_manager
        self.challenge_stream_watcher = challenge_stream_watcher
        self.event_stream_watcher = event_stream_watcher
        self.threads = threads

    def run(self):
        print("Welcome to the Lichess CLI tool. Please select one of the commands below: ")

        while self.is_running:
            self._print_menu()
            command = int(input("Enter your choice: "))

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
                '''
                TODO:
                1) Detect Ctrl-C and route it to this option
                2) Gracefully shut down all threads and release their memory
                '''
                self._quit()
            else:
                print("Sorry, I don't understand that command. Please try again.")

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
        self.challenge_stream_watcher.challenge_user(username)
        
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
        if self.game_manager.do_games_exist():
            command = input(f"There are currently {self.game_manager.number_of_games()} game(s) being played. Do you want to terminate all games? [(Y)es, (N)o]: ")

            valid_commands = ("yes", "y", "no", "n")
            while (command.strip().lower() not in valid_commands):
                command = input("((Y)es, (N)o): ")
                command = command.strip().lower()

            if command == "y" or command == "yes":
                print("Terminating all games...")
                self.game_manager.terminate_all_games(wait = False)
            elif command == "n" or command == "no":
                print("The program will end once all games have finished...")
                # self.game_manager.terminate_all_games(wait = True)

    def _close_all_threads(self):
        for thread in self.threads:
            thread.stop()
        
        for thread in self.threads:
            thread.join(10)