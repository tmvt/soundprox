import logging
import os

from dotenv import load_dotenv

from soundprox.soundprox import Soundprox

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
DOTENV_FILE = ".env"

load_dotenv(DOTENV_FILE)
logging.basicConfig(
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE")),
        logging.StreamHandler()
    ],
    level=int(os.getenv("LOG_LEVEL")),
    format=LOG_FORMAT)

if __name__ == '__main__':
    s = Soundprox()
