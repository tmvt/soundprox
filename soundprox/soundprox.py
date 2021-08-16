import logging
import os
import re
import sys
from time import sleep

from soundprox.reader import Reader
from soundprox.sonos import Sonos
from soundprox.spotify import Spotify


class Soundprox:
    def __init__(self):
        self.reader = Reader()
        self.lock_file = os.getenv("LOCK_FILE")
        self.sonos = Sonos()
        self.spotify = Spotify()

        self.start()
        self.stop()
        # parser = argparse.ArgumentParser(description="Custom Sonos controller", prog="soundprox")
        # sp = parser.add_subparsers()
        # sp_start = sp.add_parser('start', help='Starts %(prog)s daemon')
        # sp_stop = sp.add_parser('stop', help='Stops %(prog)s daemon')
        #
        # sp_start.set_defaults(func=self.start)
        # sp_stop.set_defaults(func=self.stop)
        #
        # signal.signal(signal.SIGTERM, self.terminate_process)
        #
        # args = parser.parse_args()
        # args.func(args)

    def init_lock(self):
        if os.path.exists(self.lock_file):
            logging.error("Another soundprox process is already running!")
            sys.exit(2)

        # Create lock file and write this pid to it
        with open(self.lock_file, mode="x") as f:
            f.write(str(os.getpid()))

        logging.info(f"Created lock file at {self.lock_file}")

    def remove_lock(self):
        logging.debug(f"Attempting to remove lock at {self.lock_file}")
        if os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
                logging.debug("Removed lock file")
            except TypeError:
                logging.error("Could not remove lock file! Encountered TypeError")
        else:
            logging.warning(f"Lock at {self.lock_file} does not exist!")

    def listen(self, spotify):
        card_id, text = self.reader.read()
        text = text.strip()

        playlist_pattern = re.compile(r"spotify:playlist:[\w\d]{22}")
        if playlist_pattern.search(text):
            # We got a spotify playlist uri
            spotify.play_playlist(text)
        else:
            logging.warning("Could not find matching action")

    def stop(self, args=None):
        logging.info("Shutting down process")
        self.remove_lock()
        self.reader.stop()
        sys.exit(0)

    def terminate_process(self, signal, frame):
        logging.info("Received SIGTERM")
        self.stop()

    def start(self, args=None):
        self.init_lock()

        # Start listening for tags
        try:
            while True:
                self.listen(self.spotify)
                sleep(5)
        except KeyboardInterrupt:
            logging.info("Received KeyboardInterrupt, shutting down.")
            self.stop()
