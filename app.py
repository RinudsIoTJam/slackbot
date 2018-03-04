import os
import time
import re
import logging

from time import gmtime, strftime

from slackclient import SlackClient


# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY  = 1 # 1 second delay between reading from RTM
DIRECT_COMMAND_HELP    = "help"
DIRECT_COMMAND_UTCTIME = "utctime"
DIRECT_EXAMPLE_COMMAND = DIRECT_COMMAND_HELP

CHANNEL_COMMAND_NOTE = "note"

REGEX_MENTION = "^<@(|[WU].+?)>(.*)"
REGEX_CHANCMD = "^(\w+?):(.*)"

# create logger
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)

def handle_events(slack_events):
    """
        Handles a list of events coming from the Slack RTM API to find bot
        commands. If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        # Check event type
        if event["type"] == "message" and not "subtype" in event:
            # Message Event
            log.debug("MESSAGE - channel:'{}' from:'{}' text:'{}'"
                        .format(event["channel"],event["user"],event["text"]))

            # check: Bot got mentioned directly
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                handle_direct_command(message, event)

            # check: A channel command was given
            command, message = parse_channel_command(event["text"])
            if command is not None:
                handle_channel_command(command, message, event)

def parse_channel_command(message_text):
    """
        Finds a command (a command that is at the beginning followed by a :)
        in message text and returns the command was mentioned. If there is no
        channel command, returns None
    """
    matches = re.search(REGEX_CHANCMD, message_text)
    # the first group contains the command, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_channel_command(command, message, event):
    """
        Executes channel command if the command is known
    """
    # Finds and executes the given command, filling in response
    response = None

    # This is where you start to implement more channel commands!

    if command.startswith(CHANNEL_COMMAND_NOTE):
        response = "<@{}> I don't take notes for now... :grin:".format(event["user"])
        #TODO: Make notes persistent

    if response is not None:
        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=event["channel"],
            text=response or default_response
        )

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(REGEX_MENTION, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_direct_command(command, event):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(DIRECT_EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None

    # This is where you start to implement more direct commands!

    if command.startswith(DIRECT_COMMAND_HELP):

        response = "I understand channel and direct commands.\n" \
                   "\n" \
                   "Channel Commands:\n" \
                   " `{}` : Take a note\n" \
                   "\n" \
                   "Direct Commands:\n" \
                   " `{}` : This help\n" \
                   " `{}` : Return the servers time in UTC\n"

        response = response.format(CHANNEL_COMMAND_NOTE,DIRECT_COMMAND_HELP,
                    DIRECT_COMMAND_UTCTIME)

    elif command.startswith(DIRECT_COMMAND_UTCTIME):

        response = "<@{}> It is *{}*.".format(sender, strftime("%H:%M:%S/UTC",
                    gmtime()))

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=event["channel"],
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        log.info("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            handle_events(slack_client.rtm_read())
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
