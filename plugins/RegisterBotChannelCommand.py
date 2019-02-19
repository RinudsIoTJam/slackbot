from core.commands import CommandBase


class RegisterBotChannelCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(RegisterBotChannelCommand, self).__init__(commands, CommandBase.TYPE_MASTER, "!botchan")

    def help(self, config, event):
        return "Go into DM with bot and register then channel-id."

    def work(self, config, event):
        config.set('slackbot.botchannel.id', event["channel"])
        return "Registered channel `%s` as bot DM channel." % event["channel"]


