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
git clone https://github.com/RindusIoTJam/slackbot.git
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Runtime

```
source slackbot/bin/activate
python app.py
```

Set the Slack bot token in the config file `settings.json` or
`local_settings.json` in the repository top directory with the content

```
{
  "slackbot.token": "xoxo-393952263286-sRsuiTOM645vtkGxoNbZkeVe"
  ...
}
```

Get the `slackbot.token` from the field 'bot user oauth access token' 
in the Slack Development Workspace. (see mentioned URL above)

## More on _Read the Docs_

https://rindus-slackbot.readthedocs.io/en/latest/index.html
