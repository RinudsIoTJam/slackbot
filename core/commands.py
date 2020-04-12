# This Python file uses the following encoding: utf-8

import abc
import collections
import importlib
import logger
# import tornado.template

# from persistence import *


class CommandBase(object):
    __metaclass__ = abc.ABCMeta

    TYPE_MASTER = '!:'
    TYPE_DIRECT = 'd:'
    TYPE_CHANNEL = 'c:'
    TYPE_COMMANDSET = 'cs'

    _command_type = None
    _command_word = None

    @abc.abstractmethod
    def __init__(self, commands_dict, command_type, command_word, level=logger.DEFAULT_LOG_LEVEL):
        if command_type == self.TYPE_COMMANDSET:
            return

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

    def __init__(self, commands):
        super(HelpCommand, self).__init__(commands, CommandBase.TYPE_DIRECT, "help")

    def help(self, config, event):
        return "This help."

    def work(self, config, event):

        commands = config.get('commands')

        longest_command = 0
        channel_commands = {}
        direct_commands = {}
        master_commands = {}

        for k, impl in commands.items():
            if len(impl.command()) > longest_command:
                longest_command = len(impl.command())

            if k.startswith(CommandBase.TYPE_CHANNEL):
                channel_commands[k] = impl
            elif k.startswith(CommandBase.TYPE_DIRECT):
                direct_commands[k] = impl
            else:
                master_commands[k] = impl

        response = "I understand the following commands.\n\n"

        # All channel commands (ordered alphabetically)
        response = "%s\n%s" % (response, "Channel Commands (first word in message, e.g. `foo:`):\n")
        ordered = collections.OrderedDict(sorted(channel_commands.items()))
        for k, impl in ordered.items():
            response = "%s `%s:` - %s\n" % (response,
                                            impl.command().ljust(longest_command, ' '),
                                            impl.help(config, event))

        # All direct commands (ordered alphabetically)
        response = "%s\n%s" % (response, "Direct Commands (speaking with/to bot):\n")
        ordered = collections.OrderedDict(sorted(direct_commands.items()))
        for k, impl in ordered.items():
            response = "%s `%s` - %s\n" % (response,
                                           impl.command().ljust(longest_command, ' '),
                                           impl.help(config, event))

        try:
            if config.get('slackbot.botmaster.id') == event["user"]\
                    and config.get('slackbot.botchannel.id') == event["channel"]:
                # All botmaster commands (ordered alphabetically)
                response = "%s\n%s" % (response, "BotMaster Commands (speaking with/to bot):\n")
                ordered = collections.OrderedDict(sorted(master_commands.items()))
                for k, impl in ordered.items():
                    response = "%s `%s` - %s\n" % (response,
                                                   impl.command().ljust(longest_command, ' '),
                                                   impl.help(config, event))
        except KeyError:
            pass

        return response


def load_core_commands():
    commands = {}
    HelpCommand(commands)
    return commands


def load_plugin_commands(log, config):
    commands = {}
    for plugin in config.get('plugins'):
        if not plugin.startswith('#'):
            try:
                class_ = getattr(importlib.import_module("plugins.%s" % plugin), plugin)
                class_(commands)
                log.info("Loaded plugin '%s'" % plugin)
            except ImportError:
                log.warn("Couldn't load plugin '%s'" % plugin)

    return commands
