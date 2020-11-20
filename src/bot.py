import logging

from telegram.ext import Updater, CommandHandler

from watcher.watcher_utils import parse_configuration
from watcher.watcher_manager import WatcherManager
from secrets import TELEGRAM_TOKEN, BOT_PASSWORD

logging.basicConfig(level=logging.INFO)
CONFIG_FILE = 'config.json'
TICK_FREQUENCY = 60

class Bot:
    manager: WatcherManager = None
    allowed_users: dict = dict()

    @classmethod
    def watch_tick(bot, context):
        """Run a round of WatcherManager and report any changes

        Args:
            bot (Bot): The bot class
            context (telegram.ext.callbackcontext.CallbackContext): Object used for interaction with Telegram
        """
        for watcher, change in bot.manager.watch():
            # Skip the logic if there was no change
            if not change.did_change:
                logging.debug(f'{watcher.url} did not change')
                continue
            # If the page changed, but no new words - alert only if 'AlertAnyChange' was set in the watcher's config
            if len(change.new_whitelisted) == 0 and len(change.new_blacklisted) == 0:
                if watcher.alert_any_change:
                    message = f"🔄 {watcher.url} changed (no new whitelisted/blacklisted words)"
                    context.bot.send_message(chat_id=context.job.context, text=message)
            if len(change.new_whitelisted) > 0:
                new_words = ', '.join(change.new_whitelisted)
                message = f"🆕 {watcher.url} changed (These words were added - {new_words})"
                context.bot.send_message(chat_id=context.job.context, text=message)
            # BUG: The blacklist isn't about removed words, its the same as the whitelist
            if len(change.new_blacklisted) > 0:
                new_words = ', '.join(change.new_blacklisted)
                message = f"❌ {watcher.url} changed (These words were removed - {new_words})"
                context.bot.send_message(chat_id=context.job.context, text=message)


    @classmethod
    def start_watching(class_obj, update, context):
        """ Start the JobQueue that ticks the watcher """
        logging.debug(f'Got /watch command from chat id {update.message.chat_id}')
        if Bot.allowed_users.get(update.message.chat_id, None) is None:
            context.bot.send_message(chat_id=update.message.chat_id, text="Unauthorized user! Please use the /unlock command and supply a password.")
            return
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Let's go! I will now run every {TICK_FREQUENCY} seconds.")
        context.job_queue.run_repeating(Bot.watch_tick, TICK_FREQUENCY, context=update.message.chat_id)


    @classmethod
    def stop_watching(class_obj, update, context):
        """ Stop the JobQueue that ticks the watcher """
        logging.debug(f'Got /stop command from chat id {update.message.chat_id}')
        if Bot.allowed_users.get(update.message.chat_id, None) is None:
            context.bot.send_message(chat_id=update.message.chat_id, text="Unauthorized user! Please use the /unlock command and supply a password.")
            return
        context.bot.send_message(chat_id=update.message.chat_id, text='OK, I will stop running now.')
        context.job_queue.stop()


    @classmethod
    def unlock(class_obj, update, context):
        """ Allow a user to authnticate """
        logging.debug(f'Got /unlock command from chat id {update.message.chat_id}')
        if len(context.args) != 1:
            context.bot.send_message(chat_id=update.message.chat_id, text='Usage: /unlock {password}')
            return
        if Bot.allowed_users.get(update.message.chat_id, None) is not None:
            context.bot.send_message(chat_id=update.message.chat_id, text="Already Authenticated! Use /watch to run me.")
            return
        if context.args[0] == BOT_PASSWORD:
            Bot.allowed_users[update.message.chat_id] = True
            context.bot.send_message(chat_id=update.message.chat_id, text='Authenticated! Use /watch to run me.')
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='Wrong password, please try again.')


    @classmethod
    def lock(class_obj, update, context):
        """ Remove a user from the authnticated users list """
        logging.debug(f'Got /lock command from chat id {update.message.chat_id}')
        if Bot.allowed_users.get(update.message.chat_id, None) is None:
            context.bot.send_message(chat_id=update.message.chat_id, text="Unauthorized user! Please use the /unlock command and supply a password.")
            return
        del Bot.allowed_users[update.message.chat_id]
        context.job_queue.stop()
        context.bot.send_message(chat_id=update.message.chat_id, text='Logged off and stopped. Bye!')

def setup_watchers():
    """ Setup the Bot class """
    logging.debug('Setting up the watcher...')
    with open(CONFIG_FILE, 'rb') as config_file:
        raw_json = config_file.read()
    watchers = parse_configuration(raw_json)
    Bot.manager = WatcherManager(watchers)


def setup_bot():
    """Setup the bot API and handlers

    Returns:
        telegram.ext.Updater: Used to interact with Telegram's API
    """
    logging.debug('Registering with Telegram...')
    updater = Updater(TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('unlock', Bot.unlock, pass_job_queue=True))
    updater.dispatcher.add_handler(CommandHandler('lock', Bot.lock, pass_job_queue=True))

    updater.dispatcher.add_handler(CommandHandler('watch', Bot.start_watching, pass_job_queue=True))
    updater.dispatcher.add_handler(CommandHandler('stop', Bot.stop_watching, pass_job_queue=True))
    return updater

def run_bot(updater):
    updater.start_polling()
    logging.info('Bot started! Waiting for messages...')
    updater.idle()

def main():
    logging.info('Starting the bot...')
    setup_watchers()
    updater = setup_bot()
    run_bot(updater)

if __name__ == '__main__':
    main()