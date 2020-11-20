"""
Utility functions used in the Watcher codebase
"""

import json
import logging
import hashlib
from watcher import Watcher, InvalidWatcherConfiguration

def parse_configuration(json_config: str):
    """Parse the supplied json into a list of Watcher objects.

    Args:
        json_config (str): Raw JSON from config.json

    Returns:
        list: List of the configurations as Watcher objects
    """    
    config = json.loads(json_config)
    watcher_objects = []
    for idx, watcher_item in enumerate(config.get('watchers')):
        try:
            watcher_objects.append(
                Watcher(watcher_item)
            )
        except InvalidWatcherConfiguration:
            logging.error(f'Invalid Configuration (#{idx + 1})!')
    return watcher_objects


def calculate_md5(html: str):
    """Calculate the MD5 of the given HTML

    Args:
        html (str): The HTML to calculate MD5 for

    Returns:
        str: The MD5 of the given HTML string
    """
    return hashlib.md5(str)


def search_wordlist(words: list, html: str):
    """Return the words in a list that appear in the HTML

    Args:
        words (list): A list of words to look for
        html (str): The string to look for the words in

    Returns:
        list: The list of words from the list found in the HTML
    """
    return [word for word in words if word in html]