import json
import os

from core.commands import CommandBase, HelpCommand


class RegisterBotMasterCommand(CommandBase):
    """

    """

    master = None

    def __init__(self, commands):
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), '%s.json' % self.__class__.__name__)

        try:
            with open(self.filename, 'r') as settings_file:
                self.master = json.load(settings_file)['botmaster.id']
        except IOError:
            pass
        except KeyError:
            pass

        if self.master is None:
            super(RegisterBotMasterCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, "!register")
        else:
            super(RegisterBotMasterCommand, self).__init__(commands, CommandBase.TYPE_MASTER, "!register")

    def help(self, config, event):
        if self.master is None:
            return "One-time registration of my master."
        else:
            return "One day maybe register more master."

    def work(self, config, event):
        if self.master is None:
            with open(self.filename, 'w') as settings_file:
                json.dump({'botmaster.id': event["user"]}, settings_file)

            # remove myself from commands
            config.get('commands').pop("%s%s" % (self._command_type,  self._command_word))

            # drop cached help response
            for k, impl in config.get('commands').items():
                if isinstance(impl, HelpCommand):
                    impl.response = None

            config.set('slackbot.botmaster.id', event["user"])

            HelpCommand.response = None

            response = "<@{}> Oh captain, my captain... You are now my registered master :+1::skin-tone-2:"\
                .format(event["user"])
        else:
            response = "Not implemented yet :face_with_rolling_eyes:"
        return response
