import argparse

class UserInterface:
    def __init__(self):
        self.is_running = True

    def start(self):
        print("Welcome to the Lichess CLI tool. Please enter a command: ")

        while self.is_running:
            command = input()

            if (command == "abort"):
                self.__abort()
            elif (command == "matchmaking"):
                self.__matchmaking()
            elif (command == "challenge-ai"):
                self.__challenge_ai()
            elif (command == "quit"):
                self.__quit()
            else:
                print("Sorry, I don't understand that command. Please try again.")

    def __abort(self):
        return 0

    def __matchmaking(self):
        return 0

    def __challenge_ai(self):
        return 0
        
    def __quit(self):
        return 0