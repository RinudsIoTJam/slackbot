import logging
import os
import sys
import time
import warnings

# 3rd party
from slackclient import SlackClient

# slackbot stuff
from core import handler
from core import logger
from core import settings
from core import persistence

# Supress InsecurePlatformWarning
warnings.filterwarnings("ignore")

log = logger.getLogger(name="slackbot.main", level=logging.DEBUG)

# Load config
config = settings.load('settings.json')

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
    slack_client = SlackClient(config['SLACKBOT_TOKEN'])

# Read bot's user ID by calling Web API method `auth.test`
try:
    config["SLACKBOT_ID"]  = slack_client.api_call("auth.test")["user_id"]
except KeyError:
    sys.exit("Not authenticated ...")

config["SLACK_CLIENT"] = slack_client
config["ROOT_LOGGER"] = log

log.info("Starter Bot connected and running!")

# constants
RTM_READ_DELAY  = 1 # 1 second delay between reading from RTM

if config['BOTMASTER_SLID'] is None:
    log.warn("BOTMASTER_SLID is unset - BOTMASTER features disabled")
else:
    log.debug("BOTMASTER_SLID is {}".format(config['BOTMASTER_SLID']))

if config['BOTCHANNEL_ID'] is None:
    log.warn("BOTCHANNEL_ID is unset - BOTCHANNEL features disabled")
else:
    log.debug("BOTCHANNEL_ID is {}".format(config['BOTCHANNEL_ID']))

#commands.hello_world(config, text="Hello World")
#commands.config_reload(config)

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        try:
            while True:
                handler.handle_events(config, slack_client.rtm_read())
                time.sleep(RTM_READ_DELAY)
        except KeyboardInterrupt:
            persistence.close_db()
            sys.exit(" ... exiting")

    else:
        print("Connection failed. Exception traceback printed above.")
