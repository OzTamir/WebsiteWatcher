def read_secert(path: str):
    """ Read a secret from a file (or None if reading fails)

    Args:
        path (str): The path to a file containing the secret

    Returns:
        str: the secret from the file or None if something threw an exception
    """
    try:
        with open(path, 'r') as secret:
            return secret.read()
    except:
        return None

# For Telegram Mode
TELEGRAM_TOKEN = read_secert('secrets/bot_token.txt')
BOT_PASSWORD = read_secert('secrets/bot_password.txt')

# For Twilio Mode
TWILIO_SID = read_secert('secrets/twilio_sid.txt')
TWILIO_AUTH = read_secert('secrets/twilio_auth.txt')