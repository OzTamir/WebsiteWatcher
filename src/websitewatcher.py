"""
WebsiteWatcher.py - Watch websites for changes and alert the human about it!
Author: OzTamir
URL: https://github.com/OzTamir/WebsiteWatcher
"""
import json
import logging
from configuration import Configuration
from watcher.watcher_manager import WatcherManager
from bot import Bot

logging.basicConfig(
    level=logging.INFO,
    format='[WebsiteWatcher][%(levelname)s][%(filename)s:%(funcName)s]: %(message)s')
CONFIG_FILE = 'config.json'

def read_configuration(config_path: str):
    """Read the configuration from the file and deserialize it

    Args:
        config_path (str): The path for config.json

    Returns:
        Configuration: The configuration as an object
    """
    logging.debug(f'Reading the configuration from {config_path}')
    with open(config_path, 'rb') as config_file:
        raw_json = config_file.read()
    config_dict = json.loads(raw_json)
    return Configuration(config_dict)


def telegram_mode(watcher: WatcherManager, config: Configuration):
    """Run the telegram bot

    Args:
        watcher (WatcherManager): A WatcherManager object, used to manage the watching of urls
        config (Configuration): A python representation of the config file on the disk
    """
    bot = Bot(watcher, config.token, config.password, config.tick_frequency)
    bot.run_bot()

def twilio_mode(watcher: WatcherManager, config: Configuration):
    pass

def main():
    logging.info('Starting...')
    # Setup the configuration and the WatcherManager, both of which are the same in both modes
    config = read_configuration(CONFIG_FILE)
    watcher_manager = WatcherManager(config.watchers_list)

    # Run in the configured mode
    if config.mode == Configuration.TELEGRAM:
        return telegram_mode(watcher_manager, config)
    elif config.mode == Configuration.TWILIO:
        return twilio_mode(watcher_manager, config)
    else:
        # This should never happen, as it is checked when the configuration is parsed that one mode is enabled
        raise NotImplementedError

if __name__ == '__main__':
    main()