# This Python file uses the following encoding: utf-8

import os
import sys
import time
import warnings
import argparse

# 3rd party
from slackclient import SlackClient

# slackbot stuff
from core import logger
# from core import persistence
from core.settings import Config
from core.handler import Handler

# Suppress InsecurePlatformWarning
warnings.filterwarnings("ignore")

log = logger.getLogger(name="bot.%s" % "Main".ljust(logger.DEFAULT_NAME_LENGTH,
                                                    ' ')[:logger.DEFAULT_NAME_LENGTH],
                       level=logger.DEFAULT_LOG_LEVEL)

# Load config
script_path = os.path.dirname(os.path.abspath(__file__))

config = Config(os.path.join(script_path, 'settings.json'))
config.merge(os.path.join(script_path, 'local_settings.json'))
config.merge(os.path.join(script_path, 'slack_settings.json'))

parser = argparse.ArgumentParser(description='BotMessage')
parser.add_argument("--convo",    default=None,                type=str, help="send to conversation")
parser.add_argument("--message",  default=None,                type=str, help="message to send")
parser.add_argument("--username", default="MsgBot",            type=str, help="username for sender")
parser.add_argument("--emoji",    default="incoming_envelope", type=str, help="icon for sender")
args = parser.parse_args()

# instantiate Slack client
slack_client = SlackClient(config.get('slackbot.token'))

# Read bot's user ID by calling Web API method `auth.test`
try:
    config.set("slackbot.id", slack_client.api_call("auth.test")["user_id"])
except KeyError:
    sys.exit("Not authenticated ...")

config.set("slackbot.instance.client", slack_client, transient=True)

log.info("SlackBot connected and running!")

# 1 second delay between reading from RTM
RTM_READ_DELAY = 0.25

if args.convo is not None and args.message is not None:
    log.info("Convo:    %s" % args.convo)
    log.info("Message:  %s" % args.message)
    log.info("Username: %s" % args.username)
    slack_client.api_call("chat.postMessage",
                          as_user=False,
                          username=args.username,
                          icon_emoji=":%s:" % args.emoji,
                          channel=args.convo,
                          text=args.message)
    sys.exit(" ... exiting")

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        try:
            handler = Handler(config)
            while True:
                handler.handle_events(slack_client.rtm_read())
                time.sleep(RTM_READ_DELAY)
        except (KeyboardInterrupt, SystemExit) as e:
            config.pop('commands')
            config.pop('plugins')
            config.dump(os.path.join(script_path, 'slack_settings.json'))
            # persistence.close_db()

            slack_client.api_call("chat.postMessage",
                                  as_user=True,
                                  channel=config.get('slackbot.botchannel.id'),
                                  text='Bye bye ... Reason: %s' % str(e))

            sys.exit(" ... exiting")

    else:
        print("Connection failed. Exception traceback printed above.")
