from core.commands import CommandBase


class QuitBotCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(QuitBotCommand, self).__init__(commands, CommandBase.TYPE_MASTER, "!quit")

    def help(self, config, event):
        return "Bot graceful but instant quit."

    def work(self, config, event):
        raise SystemExit('Quit requested!')


