import logging
import threading
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)

class ContinuousWorker(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        logger.debug("Creating an instance of {self.__class__.__name__}")
        self.Thread.__init__(args, kwargs)
        self.termiante_flag = threading.Event()

    def run(self):
        logger.debug(f"A {self.__class__.__name__} thread has been started")
        while not self.terminate_flag.is_set():
            self.work()

    @abstractmethod
    def work(self):
        return

    def stop(self):
        logger.debug(f"ChallengeHandler received a signal to terminate. Attempting to terminate...")
        self.terminate_flag.set()