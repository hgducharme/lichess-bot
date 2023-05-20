import json
import logging
from lichess.conf import settings
from lichess.ContinuousThread import ContinuousThread

logger = logging.getLogger(__name__)

class ChallengeStreamWatcher(ContinuousThread):
    def __init__(self, lichess_api, chess_game_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = lichess_api
        self.chess_game_manager = chess_game_manager
        self.username_queue = []
        
        # Initialize challenge stream upon instantiation of this class
        self.challenges_stream = self.api.stream_challenges()

    def work(self):
        if self.chess_game_manager.number_of_games() == settings.MAX_NUMBER_OF_GAMES:
            return

        if len(self.username_queue) > 0:
            self._send_user_challenge()

        if settings.AUTO_MATCHMAKING == True:
            challenges = self._parse_stream(self.challenges_stream)
            self._accept_and_send_challenges()

    def challenge_user(self, username = None):
        if (username is not None):
            self.username_queue.append(username)
        else:
            logger.debug(f"No username was passed into challenge_user, skipping challenge request")

    def _send_user_challenge(self):   
        username = self.username_queue.pop(0)
        logger.info(f"Sending a challenege request to user {username}")
        response = self.api.create_challenge(username, settings.CHALLENGE_PARAMS["real_time"])
        logger.info(f"Response from challenge request to {username}: {response}")

    def _parse_stream(self, stream):
        items_in_stream = []
        for line in stream:
            if line:
                line = json.loads(line)
                items_in_stream.append(line)

        if (len(items_in_stream) == 1):
            return items_in_stream[0]

        return tuple(items_in_stream)
    
    def _accept_and_send_challenges(self):
        if self.challenges_exist():
            self._accept_challenge()
        else:
            self._send_bot_challenge()

    def challenges_exist(self):
        incoming_challenges = self.challenges["in"]
        return (len(incoming_challenges) > 0)

    def _accept_challenge(self):
        return 0

    def _send_bot_challenge(self):
        online_bots = self.api.stream_online_bots()
        online_bots = self._parse_stream(online_bots)

    def _cleanup(self):
        # TODO: Cleanup resources
        return