# WebsiteWatcher
 A dockerized app to watch for changes in websites and update you via call (using Twilio) or IM (using Telegram)

## How to use
0. Get your API keys:
    - Token from Telegram
    or
    - Auth and SID tokens from Twilio
1. Clone the repository locally:
```bash
git clone https://github.com/OzTamir/WebsiteWatcher.git
```
2. Edit the config.json file with the desired sites watching settings (see example_config.json):
    - Be sure to set the Telegram/Twilio configuration with your API tokens
    - Notice that trying to mark both modes as enabled will raise an exception
3. Build the Docker image from the directory:
```bash
docker build --tag website-watcher-bot:1.0 .
```
4. Run the continer:
```bash
docker run --detach --name website-watcher website-watcher-bot:1.0
```
5. Enjoy!
