import datetime

from core.commands import CommandBase


class CurrentTimeCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(CurrentTimeCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, "time")

    def help(self, config, event):
        return "The servers current time."

    def work(self, config, event):
        response = "<@{}> Servers date/time is *{}*.".format(event["user"],
                                                             datetime.datetime.now().replace(microsecond=0).isoformat())
        return response


