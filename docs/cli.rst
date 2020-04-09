**********************
Command Line Interface
**********************

You can use the CLI to send a message to a channel by
for example crontab.

CLI parameters help

.. code-block:: bash

    /opt/slackbot/venv/bin/python app.py -h

Example:

.. code-block:: bash

    /opt/slackbot/venv/bin/python app.py --convo G0124GFUAQY 
                                         --message "Tür -> door" 
                                         --emoji "de" 
                                         --username "German Word Bot"
