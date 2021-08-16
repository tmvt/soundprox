import logging
import os

import soco


class Sonos:
    def __init__(self):
        # Get Sonos devices
        self.devices = []

        config_devices = os.getenv("SONOS_SPEAKER_NAMES").split(",")

        for device in config_devices:
            speaker = soco.discovery.by_name(device)
            if speaker is not None:
                self.devices.append(speaker)
            else:
                logging.warning(f"Could not find a SONOS speaker with name {device}")

        if os.getenv("SONOS_GROUP_ON_START"):
            self.group_devices()

    def group_devices(self):
        # Group devices if not already grouped
        number_of_devices = len(self.devices)
        if number_of_devices > 1:
            for i in range(1, number_of_devices):
                self.devices[0].join(self.devices[i])

        logging.info("Grouped sonos speakers")
