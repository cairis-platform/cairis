CAIRIS databases
======================

Default database
----------------

Each CAIRIS account comes with an *default* database.  If you or your team are using CAIRIS to work on a single project at any given time then you shouldn't need to worry about additional databases if you are using the same account.


Using other databases
---------------------

There might be times when it might be helpful to setup multiple databases.  For example, the live demo on https//demo.cairis.org has two exemplar databases that people can interact with to see different examples of CAIRIS projects.

To create a new database, select the System/Databases menu, click on the Add button in the databases table, and enter the name for a new database.  The name must not contain any spaces or reserved characters.  After a few moments, a new database will be created and your CAIRIS application will point to this database.  Any databases you create will be visible only to your account.

.. note::
   Based on the configuration of MySQL, you may find that - on creating a new database - you no longer see the default database in your database list.  If this is the case, you should logout of CAIRIS and log back in to return to the default database.

To open another database, select the System/Databases menu, and click on the table row corresponding with the name an existing database.   After a few moments, your CAIRIS application will point to the chosen database.

You can delete a database by selecting the System/Databases menu, and clicking on the Delete button next to the database you want to remove.  You cannot delete the database you currently have open.

To empty the contents of a currently open database, select the Systems/Databases menu and click on the Clear Current button.

Providing database access to other users
----------------------------------------

If you have a created a non *default* database, you can grant or revoke access to other users by clicking on the Permissions button.  Adding other users to the permissions list grants access, and removing them revokes access.

.. note::
   Based on the configuration of MySQL, you may find the list of users with permission to access the database may not always show correctly once a permission has been added.  If this is the case, and the user granted access to a database is unable to access it, you can manually grant or revoke permissions on the server using the dbctl.py script in cairis/cairis/bin, e.g. ``./dbctl.py --database MySharedDB --user shamal.faily@gmail.com --privilege grant`` .
