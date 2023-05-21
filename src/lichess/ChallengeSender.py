import logging

logger = logging.getLogger(__name__)

class ChallengeSender:
    def __init__(self, lichess_api):
        self.api = lichess_api

    def send_challenge(self, username, challenge_settings):
        logger.info(f"Sending a challenege request to user {username}")
        response = self.api.create_challenge(username, challenge_settings)
        logger.info(f"Response from challenge request to {username}: {response}")