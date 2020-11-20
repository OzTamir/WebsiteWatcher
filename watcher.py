import json
import logging
from watcher_class import Watcher, InvalidWatcherConfiguration

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