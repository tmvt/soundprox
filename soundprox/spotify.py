import logging
import os
import random

import spotipy
from spotipy import SpotifyOAuth

from soundprox.networking import send_discord_message


class Spotify:
    scope = "user-read-playback-state,user-modify-playback-state"
    possible_device_names = os.getenv("SPOTIFY_DEVICE_NAMES", "").split(",")

    def __init__(self):
        # Initialize Spotify
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=self.scope, open_browser=False))
        self.device = None
        self.current_uri = None
        # Find device
        self._find_device()

    def _find_device(self):
        all_devices = self.sp.devices()["devices"]
        logging.debug(f"Spotify found following devices: {all_devices}")

        for device in all_devices:
            if device["name"] in self.possible_device_names:
                self.device = device["id"]
                logging.info(f"Found device {device['name']}")

        # No device found
        if self.device is None:
            logging.error(f"Unable to find matching Spotify device in provided list {self.possible_device_names}")
            send_discord_message("Soundprox was unable to find a matching Spotify Connect device.")

    def play_playlist(self, uri):
        # If the same uri is scanned twice in a row, pause the playback
        if uri == self.current_uri:
            try:
                self.sp.pause_playback(device_id=self.device)
            except spotipy.exceptions.SpotifyException as e:
                logging.error(f"Could not pause playback! Error: {e}")
            # Clear saved uri to allow resuming playback
            self.current_uri = None
            logging.info("Paused playback")
            return

        # Start playlist at random track between 0 and 20
        offset = random.randint(0, 20)
        try:
            self.sp.start_playback(context_uri=uri, device_id=self.device, offset={"position": offset})
        except spotipy.exceptions.SpotifyException as e:
            logging.error(f"Could not start playback! Error: {e}")

        # Enable shuffling
        try:
            self.sp.shuffle(state=True, device_id=self.device)
        except spotipy.exceptions.SpotifyException as e:
            logging.warning(f"Could not enable shuffling. Error message: {e}")

        self.current_uri = uri

        logging.info(f"Started playback for {uri} on {self.device} with offset {offset}")
