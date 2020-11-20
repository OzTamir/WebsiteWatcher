'''
Define a Python class to hold the watcher information
'''

class InvalidWatcherConfiguration(Exception):
    ''' Indicate the the configuration given to the watcher is invalid '''
    pass

class Watcher:
    ''' Hold information about a watcher '''
    def __init__(self, watcher_item: dict):
        '''Initiate a watcher object from the config file.

        Parameters
        ----------
        watcher_item : dict
            A dictionary from the JSON array in config.json

        Raises
        ------
        InvalidWatcherConfiguration
            If the configuration is incomplete.
        """
        '''
        try:
            self.url = watcher_item['URL']
            self.whitelist = watcher_item['Whitelist']
            self.blacklist = watcher_item['Blacklist']
            self.alert_changes = watcher_item['AlertAnyChange']
            self.md5 = None
        except KeyError as exception:
            invalid_key = exception.args[0]
            raise InvalidWatcherConfiguration(
                f'Invalid configuration! Key {invalid_key} was not supplied!'
            )
    

    def __hash__(self):
        ''' Return the known hash of the website '''
        return self.md5