import os
from enum import Enum, auto
import logging

import requests

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 20))


class RequestMethod(Enum):
    # Let Python assign the values
    GET = auto()
    POST = auto()


def send_request(url, json=None, method=RequestMethod.GET):
    """ Sends a request to given URL and provides basic error handling in
    one function.

    :param url: The URL which the request should be send to.
    :param json: Optional JSON data. (Only relevant when using POST method)
    :param method: The HTTP method to be used. Use the enum class RequestMethod for this!
    :return: Request object or None if the request failed.
    """

    # Init error tracking bool
    error = False

    res = None
    try:
        # Make request using specified method
        if method is RequestMethod.GET:
            res = requests.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        elif method is RequestMethod.POST:
            res = requests.post(url, timeout=REQUEST_TIMEOUT, json=json)
        else:
            logging.error("Unrecognized HTTP request method")
            return None
        res.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        logging.warning(f"Connection error occurred when connecting to page {url}. Error message: {e}")
        error = True
    except requests.exceptions.Timeout as e:
        logging.warning(f"Encountered Timout when trying to connect to page {url}. Error message: {e}")
        error = True
    except requests.exceptions.HTTPError as e:
        logging.warning(f"Got faulty status code from page {url}. Error message: {e}")
        error = True
    except requests.exceptions.MissingSchema as e:
        logging.warning(f"Given URL has wrong schema. Error message: {e}")
        error = True

    if res is None or error:
        # Update user that error occurred
        send_discord_message("Encountered error when sending request!")
        logging.error("Encountered error when sending request!")

    return res


def send_discord_message(message):
    if os.getenv("DISCORD_ENABLED", False) == "False":
        logging.debug("Skipped Discord message (Reason: Discord not enabled)")
        return

    data = {
        "content": message
    }

    send_request(os.getenv("DISCORD_WEBHOOK"), json=data, method=RequestMethod.POST)
    logging.debug(f"Send payload {data} to Discord webhook.")
