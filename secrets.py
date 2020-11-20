with open('secrets/token.txt', 'r') as secret:
    TELEGRAM_TOKEN = secret.read()

with open('secrets/bot_password.txt', 'r') as secret:
    BOT_PASSWORD = secret.read()