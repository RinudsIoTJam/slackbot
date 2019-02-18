import re
import commands
import logger


class Handler:
    _config = None
    _logger = None
    _commands = None

    REGEX_MENTION = "^<@(|[WU].+?)>(.*)"
    REGEX_CHANCMD = "^(\w+?):(.*)"
    REGEX_COMMAND = "^(\w+?)(\W+?)"

    DEFAULT_RESPONSE = "Not sure what you mean. Try `help`."

    def __init__(self, config, level=logger.DEFAULT_LOG_LEVEL):
        self._config = config
        self._logger = logger.getLogger(name="bot.%s" % self.__class__.__name__.ljust(logger.DEFAULT_NAME_LENGTH,
                                                                                      ' ')[:logger.DEFAULT_NAME_LENGTH],
                                        level=level)

    def handle_events(self, slack_events):
        """
            Handles a list of events coming from the Slack RTM API to find bot
            commands. If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        if self._commands is None:
            self._commands = commands.load_core_commands()
            self._commands.update(commands.load_plugin_commands(self._logger, self._config))
            self._config.set("commands", self._commands)

        for event in slack_events:
            response = None

            # Check event type
            if event["type"] == "message" and "subtype" not in event:
                # Message Event
                self._logger.debug("MESSAGE - channel:'{}' from:'{}' text:'{}'"
                                   .format(event["channel"], event["user"], event["text"]))

                user_id, message = self.parse_mention(event)

                if user_id == self._config.get("SLACKBOT_ID") or event["channel"] == self._config.get("BOTCHANNEL_ID"):
                    # Bot got mentioned directly at message start in some channel or DM with (BotChannel)
                    response = self.handle_direct_command(event, message)

                else:
                    # check: A channel command was given
                    command, arguments = self.parse_channel_command(event["text"].lower())
                    if command is not None:
                        self._logger.debug("handle_channel_command {}".format(event["text"]))
                        response = self.handle_channel_command(event, command)
                    else:
                        self._logger.debug("Ignored this message.")

                if response is not None:
                    # Sends the response back to the channel
                    self._config.get("SLACK_CLIENT").api_call("chat.postMessage",
                                                              channel=event["channel"],
                                                              text=response)

    @classmethod
    def parse_channel_command(cls, message_text):
        """
            Finds a command (a command that is at the beginning followed by a :)
            in message text and returns the command was mentioned. If there is no
            channel command, returns None
        """
        matches = re.search(Handler.REGEX_CHANCMD, message_text)
        # the first group contains the command, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    @classmethod
    def parse_mention(cls, event):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(Handler.REGEX_MENTION, event["text"])
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_channel_command(self, event, command):
        """
            Executes channel command if the command is known
        """
        # Finds and executes the given command, filling in response
        response = Handler.DEFAULT_RESPONSE

        try:
            response = self._commands["c:%s" % command].work(self._config, event)
        except KeyError:
            pass

        return response

    def handle_direct_command(self, event, command=None):
        """
            Executes bot command if the command is known
        """
        # Finds and executes the given command, filling in response

        if command is None:
            command = event["text"]

        self._logger.debug("handle_direct_command %s" % command)

        try:
            response = self._commands["d:%s" % command.split(' ', 1)[0]].work(self._config, event)
        except KeyError:
            self._logger.warn("Unknown handle_direct_command %s" % command )
            response = Handler.DEFAULT_RESPONSE

        return response
