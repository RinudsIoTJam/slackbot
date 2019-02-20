*******
Plugins
*******

Abstract
========

Plugins extend the functionality of the bot. They are configured at the ``settings.json``
by adding the plugin name to the plugins list. There are 4 types of plugins:

.. hlist::
   :columns: 1

   * Channel Commands: Given in a channel in the form ``word:``
   * Direct Commands: Given to the bot in the form ``@bot word``
   * Botmaster Commands: Only available to the registered botmaster
   * CommandSets: A bundle of commands of whatever type

Plugins
-------

BotMasterCommands
~~~~~~~~~~~~~~~~~

Type::

    CommandSet of Botmaster commands


Adds the commands

.. hlist::
   :columns: 1

   * ``!botchan``
   * ``!register``
   * ``!quit``

``!botchan``: Messaging the bot in a direct chat ``@bot !botchan`` registers that
channel as the one the botmaster uses to communicate with the bot without the need
of prefixing direct commands with ``@bot``.

``!register``: Registers your Slack ID as the botmaster who is authorized to give
botmaster commands.

``!quit``: Instantly but graceful quit the bot.

RandomJokeCommand
~~~~~~~~~~~~~~~~~

Type::

    Direct Command

Adds the command

.. hlist::
   :columns: 1

   * ``joke``

Get you a random joke from https://geek-jokes.sameerkumar.website/api (mostly
Chuck Norris jokes)

CurrentCalendarCommand
~~~~~~~~~~~~~~~~~~~~~~

Type::

    Direct Command

Adds the command

.. hlist::
   :columns: 1

   * ``calendar``

Gives back a calendar of the current year.

CurrentTimeCommand
~~~~~~~~~~~~~~~~~~

Type::

    Direct Command

Adds the command

.. hlist::
   :columns: 1

   * ``calendar``

Tells the bots local date and time in ISO 8601 format, YYYY-MM-DDTHH:MM:SS.