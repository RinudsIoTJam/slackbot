# slackbot

Just a bot fitting our needs.

Based on the starting point https://www.fullstackpython.com/blog/build-first-slack-bot-python.html.

## Installation

```
git clone https://github.com/RinudsIoTJam/slackbot.git
virtualenv .venv
source .venv/bin/activate
pip install slackclient
```


## Runtime

```
source slackbot/bin/activate
SLACK_BOT_TOKEN='xXxXxXxXxX' python app.py
```

Get the SLACK_BOT_TOKEN from the field 'bot user oauth access token' in the
Development Workspace. (see mentioned URL above)
