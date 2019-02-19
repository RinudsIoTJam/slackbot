from core.commands import CommandBase


class JarvisInfoCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(JarvisInfoCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, "info")

    def help(self, config, event):
        return "Giving a little introduction about myself (the JarvisBot)"

    def work(self, config, event):
        response = "Hey <@{}>, nice that you ask. My name is Jarvis and I'm your " \
                   "friendly bot. You can even improve my understanding with creating "\
                   "new commands by participating a "\
                   "<https://github.com/RindusIoTJam/slackbot|RindusIoTJam/slackbot>."\
            .format(event["user"])
        return response


