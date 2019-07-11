Troubleshooting
===============

Log files
---------

The CAIRIS log files are a good place to look for signs of errors in the event of any problems.

If you are running Docker, you can get a live update of the log file with the following command:

.. code-block:: bash

   docker exec -t `docker ps | grep shamalfaily/cairis | head -1 | cut -d ' ' -f 1` tail -f /tmp/mod_wsgi-localhost:8000:0/error_log

If you are using the CAIRIS development server, i.e. running cairisd.py then the daemon will log directly to the console.

For detailed logging information, change the log_level value in cairis.cnf to *debug*.

Raising issues
--------------

If you experience any problems using CAIRIS then please raise an issue in GitHub.

When raising an issue, please provide the version of CAIRIS you are using.  You can find this by clicking on the System/About menu.
