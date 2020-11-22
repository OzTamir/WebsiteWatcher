"""
WebsiteWatcher.py - Watch websites for changes and alert the human about it!
Author: OzTamir
URL: https://github.com/OzTamir/WebsiteWatcher
"""
import logging
import json
from watcher.watcher_utils import read_watchers_from_config
from watcher.watcher_manager import WatcherManager

logging.basicConfig(level=logging.INFO)
CONFIG_FILE = 'config.json'

def read_configuration(config_path: str):
    """Read the configuration from the file and deserialize it

    Args:
        config_path (str): The path for config.json

    Returns:
        dict: The configuration as an actual dictionary
    """
    logging.debug(f'Reading the configuration from {config_path}')
    with open(config_path, 'rb') as config_file:
        raw_json = config_file.read()
    return json.loads(raw_json)


def setup_watchers():
    """ Setup the Bot class """
    logging.debug('Setting up the watcher...')
    with open(CONFIG_FILE, 'rb') as config_file:
        raw_json = config_file.read()
    watchers = read_watchers_from_config(raw_json)
    return WatcherManager(watchers)

def main():
    logging.info('Starting the bot...')
    setup_watchers()
    updater = setup_bot()
    run_bot(updater)

if __name__ == '__main__':
    main()