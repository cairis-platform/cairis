CAIRIS server maintenance
=========================

If you have shell access to your CAIRIS host, there a number of scripts to aid in general server maintenance.  These can be found in cairis/cairis/bin directory.

Calling these scripts with the --help flag will provide detailed information on the parameters they take.


Account management
------------------

You can add new accounts using the *add_cairis_user.py* script.  Account names should be email addresses.

.. code-block:: bash

   ./add_cairis_user.py test@test.com test "Test user"

*cairis_users.py* provides a list of current users.

.. code-block:: bash

   ./cairis_users.py

*rm_cairis_user.py* can be used to remove accounts.  All accounts will be removed if the parameter used is 'all'.

.. code-block:: bash

   ./rm_cairis_user.py test@test.com

The default database associated with CAIRIS accounts can sometimes get corrupted due to destructive operations (e.g. importing models) being interrupted.  To re-create the default database for an account, you can use the *reset_cairis_user.py* script

.. code-block:: bash

   ./reset_cairis_user.py --reload 1 test@test.com

If you set the *reload* parameter 1 then CAIRIS will attempt to export the contents of the default database, and -- once the default database has been re-created -- attempt to re-import it.  This can sometimes fail if the model contains reserved characters, but this can be overridden by setting the *ignore_validity* parameter to 1.



Importing and exporting models
------------------------------

Models can be imported using the *cimport.py* script. The below command, which is run from cairis/cairis/bin, imports the ACME Water sample model into the default database of the test@test.com user. 

.. code-block:: bash

   ./cimport.py --user test@test.com --database default --type package --overwrite 1 ../../examples/exemplars/NeuroGrid.cairis

The *cexport.py* script can be used to export models.

.. code-block:: bash

   ./cexport.py --user test@test.com --database default --type package /tmp/NG.cairis


Backing up and restoring servers
--------------------------------

*backup_server.py* creates a tarball containing exported model packages for all the default databases on a CAIRIS server, and a copy of the password hashes for each account.


.. code-block:: bash

   ./backup_server.py /tmp/backup140221.tar

If you have a clean CAIRIS server (i.e. with no accounts setup), you can use *restore_server.py* to recreate the accounts and account contents from a backup tarball.

.. code-block:: bash

   ./restore_server.py /tmp/backup140221.tar
