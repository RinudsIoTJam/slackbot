# This Python file uses the following encoding: utf-8

import requests
import urllib

from core.commands import CommandBase


class RandomJokeCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(RandomJokeCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, "joke")

    def help(self, config, event):
        return "Tell a random geek joke from https://geek-jokes.sameerkumar.website/api."

    def work(self, config, event):
        try:
            response = urllib.unquote(requests.get("https://geek-jokes.sameerkumar.website/api").content)
        except IOError:
            response = "Hey <@{}>, you know Sum Ting Wong?".format(event["user"])
        return response


