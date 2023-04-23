import logging
import threading
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)

class ContinuousThread(threading.Thread):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        logger.debug(f"Creating an instance of {self.__class__.__name__}")
        super().__init__(*args, **kwargs)
        self.terminate_flag = threading.Event()

    def run(self):
        logger.debug(f"{self.__class__.__name__} thread has been started")

        while not self.terminate_flag.is_set():
            self.work()

        logger.debug(f"{self.__class__.__name__} has terminated")

    @abstractmethod
    def work(self):
        return

    def stop(self):
        logger.debug(f"{self.__class__.__name__} received a signal to terminate. Terminating...")
        self._cleanup()
        self.terminate_flag.set()

    def _cleanup(self):
        return