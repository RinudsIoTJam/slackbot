# slackbot

Based on the starting point 
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html.

## Mission Statement

Create a chat based tool for software development teams.

The tool

- has to come with a core set of basic and controll functions,
- is easy to extend with new feature in the form of modules and
- can be fully controlled by chat (no CLI access needed)

## Vision

Having a extensible chat based tool that just fits. 

## Installation

Prerequisites

- python
- virtualenv 

```
git clone https://github.com/RinudsIoTJam/slackbot.git
virtualenv .venv
source .venv/bin/activate
pip install slackclient
```

## Runtime

```
source slackbot/bin/activate
SLACKBOT_TOKEN='xXxXxXxXxX' python app.py
```

Instead of passing the token as environment variable you can also create a
file `local_settings.py` in the repository top directory with the content
`SLACKBOT_TOKEN='xXxXxXxXxX'`.

Get the SLACKBOT_TOKEN from the field 'bot user oauth access token' in the
Development Workspace. (see mentioned URL above)
