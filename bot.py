from watcher.watcher_utils import parse_configuration
from watcher.watcher_manager import WatcherManager

CONFIG_FILE = 'example_config.json'

class Bot:
    manager: WatcherManager = None

    @classmethod
    def watch(bot):
        for watcher, change in bot.manager.watch():
            print(f'URL: {watcher.url}')
            print(f'Did change: {change.did_change}')
            print(f'New whitelisted words: {change.new_whitelisted}')
            print(f'New blacklisted words: {change.new_blacklisted}')

def main():
    with open(CONFIG_FILE, 'rb') as config_file:
        raw_json = config_file.read()
    watchers = parse_configuration(raw_json)
    Bot.manager = WatcherManager(watchers)
    for _ in range(10):
        Bot.watch()

if __name__ == '__main__':
    main()