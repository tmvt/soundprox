import logging
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()


class Reader:
    def __init__(self):
        self._terminate = False

    def read(self):
        try:
            while self._terminate is False:
                logging.debug("Started listening for tag")
                card_id, text = reader.read()
                logging.debug(f"Read Tag ID: {card_id} Text: {text}")
                return card_id, text
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise

    def stop(self):
        self._terminate = True
