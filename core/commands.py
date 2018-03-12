import calendar
import datetime
import logging
import re
import sys

from datetime import date

REGEX_CHANCMD = "^(\w+?):(.*)"

from persistence import *

def load(config):
  commands = {
    "channel:cmnd:note":  command_channel_note,
    "channel:help:note":  "Take a note",
    "channel:cmnd:notes": command_channel_notes,
    "channel:help:notes": "Show all notes",

    "direct:cmnd:help":   command_direct_help,
    "direct:help:help":   "This help",
    "direct:cmnd:time":   command_direct_time,
    "direct:help:time":   "The servers time",
    "direct:cmnd:cal":    command_direct_calendar,
    "direct:help:cal":    "Current calendar"

    #"direct:cmnd:test":  command_direct_test,
    #"direct:help:test":  "test"
  }
  config["commands"] = commands
  return config


def command_direct_help(config, event):
  response = "I understand channel and direct commands.\n" \
           "\n" \
           "Channel Commands:\n" \
           "{}" \
           "\n" \
           "Direct Commands (speaking with/to bot):\n" \
           "{}"
           
  channel_commands = ""
  for key in config["commands"]:
    if key.startswith("channel:cmnd:"):
      channel_commands = "{} `{}:` : {}\n".format(channel_commands, 
                                                  key.split(':')[2], 
                                                  config["commands"]["channel:help:{}".format(key.split(':')[2])])
      
  direct_commands = ""
  for key in config["commands"]:
    if key.startswith("direct:cmnd:"):
      direct_commands = "{} `{}` : {}\n".format(direct_commands, 
                                                key.split(':')[2], 
                                                config["commands"]["direct:help:{}".format(key.split(':')[2])])
      
  response = response.format( channel_commands, direct_commands)
  return response


def command_direct_time(config, event):
  response = "<@{}> Servers datetime is *{}*.".format(event["user"], datetime.datetime.now().replace(microsecond=0).isoformat())
  return response


def command_direct_calendar(config, event):
  response = "<@{}> I assume this year:\n```{}```.".format(event["user"], calendar.TextCalendar().formatyear(date.today().year))
  return response


def command_channel_notes(config, event):
  response = "<@{}> notes recorded till ```{}```:\n".format(event["user"], allNotes())
  return response

def command_channel_note(config, event):
  matches = re.search(REGEX_CHANCMD, event["text"])

  note = {
    "timestamp": datetime.datetime.now().replace(microsecond=0).isoformat(),
    "user":      event["user"],
    "channel":   event["channel"],
    "note":      matches.group(2).strip()
  }
  save(config, note)
  response = "<@{}> note recorded at {}".format(note["user"],note["timestamp"])
  return response


def hello_world(config, **kwargs):
  if 'text' in kwargs:
    log(config).info(kwargs.get("text"))
    return kwargs.get("text")
  else:
    log(config).debug("Hello World")
    return "Hello World"


def config_reload(config, **kwargs):
  return "Config reloaded"


#def log(config):
#  return config["ROOT_LOGGER"].getChild(__name__)
