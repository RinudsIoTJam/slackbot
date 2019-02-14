import re
import commands

REGEX_MENTION = "^<@(|[WU].+?)>(.*)"
REGEX_CHANCMD = "^(\w+?):(.*)"
REGEX_COMMAND = "^(\w+?)(\W+?)"

def handle_events(config, slack_events, **kwargs):
    """
        Handles a list of events coming from the Slack RTM API to find bot
        commands. If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    commands.load(config)

    # Default response is help text for the user
    default_response = "Not sure what you mean. Try `help`."

    for event in slack_events:
        response = None

        # Check event type
        if event["type"] == "message" and not "subtype" in event:
            # Message Event
            log(config).debug("MESSAGE - channel:'{}' from:'{}' text:'{}'"
                              .format(event["channel"],event["user"],event["text"]))

            # check: Bot got mentioned directly at message start in some channel
            user_id, message = parse_direct_mention(event["text"])
            if user_id == config["SLACKBOT_ID"]:
                log(config).debug("handle_direct_command {}".format(message))
                response = handle_direct_command(config, message, event)

            # check: Message in BotChannel
            elif event["channel"] == config["BOTCHANNEL_ID"]:
                log(config).debug("handle_direct_command {}".format(event["text"]))
                response = handle_direct_command(config, event["text"], event)

            else:
                # check: A channel command was given
                command, message = parse_channel_command(event["text"].lower())
                if command is not None:
                    log(config).debug("handle_channel_command {}".format(command))
                    response = handle_channel_command(config, command, message, event)
                else:
                    log(config).debug("Ignored this message.")

            if response is not None:
                # Sends the response back to the channel
                config["SLACK_CLIENT"].api_call(
                    "chat.postMessage",
                    channel=event["channel"],
                    text=response or default_response
                )

def parse_channel_command(message_text):
    """
        Finds a command (a command that is at the beginning followed by a :)
        in message text and returns the command was mentioned. If there is no
        channel command, returns None
    """
    matches = re.search(REGEX_CHANCMD, message_text)
    # the first group contains the command, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(REGEX_MENTION, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_channel_command(config, command, message, event):
    """
        Executes channel command if the command is known
    """
    # Finds and executes the given command, filling in response
    response = None

    try:
        response = config["commands"]["channel:cmnd:{}".format(command)](config, event)
    except KeyError:
        pass

    return response

def handle_direct_command(config, command, event):
    """
        Executes bot command if the command is known
    """
    # Finds and executes the given command, filling in response
    response = None

    try:
        response = config["commands"]["direct:cmnd:{}".format(command.split(' ', 1)[0])](config, event)
    except KeyError:
        pass

    return response

def log(config):
    return config["ROOT_LOGGER"].getChild(__name__)
