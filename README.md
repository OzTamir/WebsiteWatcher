# WebsiteWatcher
 A dockerized telegram bot to watch for changes in websites

## How to use
0. [Create a telegram bot](https://core.telegram.org/bots) and get your token.
1. Clone the repository locally:
`$ git clone https://github.com/OzTamir/WebsiteWatcher.git`
2. Create a folder to store the bot's secrets:
`mkdir secrets`
3. Create the token file and the password file (the password is used to authenticate to the bot):
`$ echo 'MY_TELEGRAM_TOKEN' > secrets/token.txt`
`$ echo 'MY_SECRET_PASSWORD' > secrets/bot_password.txt`
4. Edit the config.json file with the desired sites watching settings (see example_config.json).
5. Build the Docker image from the directory:
`$ docker build --tag website-watcher-bot:1.0 .`
6. Run the continer:
`$ docker run --detach --name website-watcher website-watcher-bot:1.0`
7. Enjoy!
