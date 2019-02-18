import os
import sys
import time
import warnings

# 3rd party
from slackclient import SlackClient

# slackbot stuff
from core import logger
from core import persistence
from core.settings import Config
from core.handler import Handler

# Suppress InsecurePlatformWarning
warnings.filterwarnings("ignore")

log = logger.getLogger(name="bot.%s" % "Main".ljust(logger.DEFAULT_NAME_LENGTH,
                                                    ' ')[:logger.DEFAULT_NAME_LENGTH],
                       level=logger.DEFAULT_LOG_LEVEL)

# Load config
config = Config('settings.json')

# load local_settings if exist
try:
    from local_settings import *
except ImportError:
    pass

# instantiate Slack client
if os.environ.get('SLACKBOT_TOKEN') is not None:
    log.info("Using SLACKBOT_TOKEN from os.environ")
    slack_client = SlackClient(os.environ.get('SLACKBOT_TOKEN'))

elif 'SLACKBOT_TOKEN' in locals() and SLACKBOT_TOKEN is not None:
    log.info("Using SLACKBOT_TOKEN from local_settings.py")
    slack_client = SlackClient(SLACKBOT_TOKEN)

else:
    log.info("Using SLACKBOT_TOKEN from settings.json")
    slack_client = SlackClient(config.get('SLACKBOT_TOKEN'))

# Read bot's user ID by calling Web API method `auth.test`
try:
    config.set("SLACKBOT_ID", slack_client.api_call("auth.test")["user_id"])
except KeyError:
    sys.exit("Not authenticated ...")

config.set("SLACK_CLIENT", slack_client)
config.set("ROOT_LOGGER", log)

log.info("Starter Bot connected and running!")

# 1 second delay between reading from RTM
RTM_READ_DELAY = 1

if config.get('BOTMASTER_SLID') is None:
    log.warn("BOTMASTER_SLID is unset - BOTMASTER features disabled")
else:
    log.debug("BOTMASTER_SLID is {}".format(config.get('BOTMASTER_SLID')))

if config.get('BOTCHANNEL_ID') is None:
    log.warn("BOTCHANNEL_ID is unset - BOTCHANNEL features disabled")
else:
    log.debug("BOTCHANNEL_ID is {}".format(config.get('BOTCHANNEL_ID')))

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        try:
            handler = Handler(config)
            while True:
                handler.handle_events(slack_client.rtm_read())
                time.sleep(RTM_READ_DELAY)
        except KeyboardInterrupt:
            persistence.close_db()
            sys.exit(" ... exiting")

    else:
        print("Connection failed. Exception traceback printed above.")
