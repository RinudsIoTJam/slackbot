import abc
import collections
import importlib
import logger
# import tornado.template

# from persistence import *
from datetime import date


class CommandBase(object):
    __metaclass__ = abc.ABCMeta

    TYPE_DIRECT = 'd:'
    TYPE_CHANNEL = 'c:'

    _command_type = None
    _command_word = None

    @abc.abstractmethod
    def __init__(self, commands_dict, command_type, command_word, level=logger.DEFAULT_LOG_LEVEL):
        self._logger = logger.getLogger(name="cmd.%s" % self.__class__.__name__.ljust(logger.DEFAULT_NAME_LENGTH,
                                                                                      ' ')[:logger.DEFAULT_NAME_LENGTH],
                                        level=level)
        self._command_type = command_type
        self._command_word = command_word
        commands_dict["%s%s" % (command_type, command_word)] = self
        self._logger.debug("Initialized")

    @abc.abstractmethod
    def help(self, config, event):
        """Return a string with a helpful description"""
        return "No help available."

    @abc.abstractmethod
    def work(self, config, event):
        """Return a string with the work output"""
        return "You should never see this."

    def command(self):
        return self._command_word


class HelpCommand(CommandBase):

    response = None

    def __init__(self, commands):
        super(HelpCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, "help")

    def help(self, config, event):
        return "This help."

    def work(self, config, event):

        if self.response is None:
            commands = config.get('commands')

            longest_command = 0
            channel_commands = {}
            direct_commands = {}

            for k, impl in commands.items():
                if len(impl.command()) > longest_command:
                    longest_command = len(impl.command())

                if k.startswith(CommandBase.TYPE_CHANNEL):
                    channel_commands[k] = impl
                else:
                    direct_commands[k] = impl

            response = "I understand channel and direct commands.\n" \
                       "\n" \
                       "Channel Commands (first word in message, e.g. `foo:`):\n"

            scc = collections.OrderedDict(sorted(channel_commands.items()))
            for k, impl in scc.items():
                if k.startswith(CommandBase.TYPE_CHANNEL):
                    response = "%s `%s:` - %s\n" % (response,
                                                    impl.command().ljust(longest_command, ' '),
                                                    impl.help(config, event))

            response = "%s\n%s" % (response, "Direct Commands (speaking with/to bot):\n")

            sdc = collections.OrderedDict(sorted(direct_commands.items()))
            for k, impl in sdc.items():
                if k.startswith(CommandBase.TYPE_DIRECT):
                    response = "%s `%s` - %s\n" % (response,
                                                   impl.command().ljust(longest_command, ' '),
                                                   impl.help(config, event))
            self.response = response
            self._logger.debug("Help initially generated.")

        return self.response


def load_core_commands():
    commands = {}
    HelpCommand(commands)
    return commands


def load_plugin_commands(log, config):
    commands = {}
    for plugin in config.get('plugins'):
        try:
            class_ = getattr(importlib.import_module("plugins.%s" % plugin), plugin)
            class_(commands)
            log.info("Loaded plugin '%s'" % plugin)
        except ImportError:
            log.warn("Couldn't load plugin '%s'" % plugin)

    return commands
