# This Python file uses the following encoding: utf-8

import json
import os

from core.commands import CommandBase, HelpCommand

BOTMASTER_REGISTER = '!register'
BOTMASTER_BOTCHAN = "!botchan"
BOTMASTER_QUIT = '!quit'


class BotMasterCommands(CommandBase):
    """

    """

    def __init__(self, commands):
        super(BotMasterCommands, self).__init__(commands, CommandBase.TYPE_COMMANDSET, '')
        BotMasterRegisterCommand(commands)
        BotChannelRegisterCommand(commands)
        BotQuitCommand(commands)

    def help(self, config, event):
        return ''

    def work(self, config, event):
        return ''


class BotMasterRegisterCommand(CommandBase):
    """

    """

    master = None

    def __init__(self, commands):
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     '%s.json' % os.path.basename(__file__).split('.', 1)[0])

        try:
            with open(self.filename, 'r') as settings_file:
                self.master = json.load(settings_file)['botmaster.id']
        except IOError:
            pass
        except KeyError:
            pass

        if self.master is None:
            super(BotMasterRegisterCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, BOTMASTER_REGISTER)
        else:
            super(BotMasterRegisterCommand, self).__init__(commands, CommandBase.TYPE_MASTER, BOTMASTER_REGISTER)

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


class BotChannelRegisterCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(BotChannelRegisterCommand, self).__init__(commands, CommandBase.TYPE_MASTER, BOTMASTER_BOTCHAN)

    def help(self, config, event):
        return "Go into DM with bot and register then channel-id."

    def work(self, config, event):
        config.set('slackbot.botchannel.id', event["channel"])
        return "Registered channel `%s` as bot DM channel." % event["channel"]


class BotQuitCommand(CommandBase):
    """

    """

    def __init__(self, commands):
        super(BotQuitCommand, self).__init__(commands, CommandBase.TYPE_MASTER, BOTMASTER_QUIT)

    def help(self, config, event):
        return "Bot graceful but instant quit."

    def work(self, config, event):
        raise SystemExit('Quit requested!')
