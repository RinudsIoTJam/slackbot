*****
Usage
*****

Production setup
================

You set the Slack bot token in the config file

.. code-block:: json
    :caption: settings.json
    :name: settings.json
    :emphasize-lines: 2
    
    {
      "slackbot.token": "XXXX-325920249586-tkG2oNbZlOMrsjvkeVesRsO4",
      "plugins": [
        "#-- BotMaster Commands ---------",
        "BotMasterCommands",
        "#-- Direct Commands ------------",
        "BotInfoCommand",
        "CurrentCalendarCommand",
        "CurrentTimeCommand",
        "RandomJokeCommand",
        "#-- Channel Commands -----------"
      ]
    }

and simply start the slackbot with
    
.. code-block:: bash

    python app.py

The ``help`` command is the only build-in command of the bot.

.. caution::
   If the BotMasterCommands plugin is enabled, then you should as soon as possible open
   a direct chat with the bot and enter the following chat messages (replacing ``@bot``
   with the ``@`` and the bots name:

.. code-block:: bash

    @bot !botchan
    !register

The first message this DM between you and the bot as a channel where you don't have to
put ``@bot`` in front of all commands. The second command registers your SlackID as the
ID that has BotMaster rights.


Development setup
=================

You can create a ``local_settings.json`` file, that is git ignored and just consists
of one relevant line staring with ``slackbot.token``. It is anyway overwriting every
setting made in the ``settings.json`` with the settings made there.

.. code-block:: json
    :caption: local_settings.json
    :name: local_settings.json
    :emphasize-lines: 2
    
    {
      "slackbot.token": "xoxo-393952263286-sRsuiTOM645vtkGxoNbZkeVe"
    }
