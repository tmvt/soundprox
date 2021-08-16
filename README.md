# Soundprox
Soundprox was born as a simple weekend project. It controls audio playback on Sonos Speakers using
RFID Cards and is designed to be used on a RaspberryPi with a [RC522](https://www.amazon.de/AZDelivery-Reader-Arduino-Raspberry-gratis/dp/B01M28JAAZ)
RFID card reader. 

The idea is basically that the card reader is hidden (e.g. below a desk) and the cards are used like digital album
or playlist "shortcuts", so that if a card is presented to the reader, the assigned album/playlist starts playing.
Currently, only Spotify is supported.

## Quick start
Simply run Soundprox on a RaspberryPi.

(Note that it is recommended to set up a [virtual environment](https://docs.python.org/3/library/venv.html) first)
```shell
git clone https://github.com/tmvt/soundprox.git
cd soundprox
pip install -r requirements.txt
python -m soundprox
```

## Configuration
Soundprox is configured mainly by using environment variables. The easiest way to configure those is by using a `.env` file.
To get an idea of how this file could be structured, take a look at the [example file](.env.example). It contains all available
configurations options.

Some of important options include:
- `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`: You can obtain these by creating an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
- `SPOTIFY_DEVICE_NAMES`: Contains the name(s) of the speakers music is supposed to be played on. *This has to be the name displayed in Spotify Connect!*
- `SONOS_SPEAKER_NAMES`: Pretty much the same as above, but this time referencing the Sonos speaker names.
- `DISCORD_ENABLED` and `DISCORD_WEBHOOK`: This project has a Discord integration (using webhooks) which surfaces important information in a Discord channel. If this integration is enabled, a webhook URL has to be provided.
