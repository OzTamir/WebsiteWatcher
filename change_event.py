"""
Define the ChangeEvent class 
"""

class ChangeEvent:
    """ A class to represents a change in the website """
    def __init__(self, url: str, did_change=False, whitelisted_words=[], blacklisted_words=[]):
        """Hold information about the change in a site

        Args:
            url (str): The URL for which this information applies
            did_change (bool, optional): Did the site changed from last time. Defaults to False.
            whitelisted_words (list, optional): Whitelisted words in the HTML. Defaults to [].
            blacklisted_words (list, optional): Blacklisted words in the HTML. Defaults to [].
        """
        self.url = url
        self.did_change = did_change
        self.new_whitelisted = whitelisted_words
        self.new_blacklisted = blacklisted_words