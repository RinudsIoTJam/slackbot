Usage
-----

Starting the slackbot is as easy as:

.. code-block:: bash
    SLACK_BOT_TOKEN='xoxo-393952263286-sRsuiTOM645vtkGxoNbZkeVe' python app.py

If you prefer to safe the tocken in the config file:

.. code-block:: json
    :caption: settings.json
    :name: settings.json
    :emphasize-lines: 4
    {
      "BOTCHANNEL_ID": "D9JU01RKQ", 
      "BOTMASTER_SLID": "U8SJUF6KC", 
      "SLACKBOT_TOKEN": "xoxo-393952263286-sRsuiTOM645vtkGxoNbZkeVe",
      "plugins": {
        "bla": "plugins.bla"
      }
    }

and simply start the slackbot with:
    
.. code-block:: bash
    python app.py