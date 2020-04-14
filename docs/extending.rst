Extending CAIRIS
================

Over the years, CAIRIS has evolved to support new concepts and types of model.  Its architecture has also evolved to make it easy for its [sadly] small development team to effectively maintain several hundred thousand lines of code.  As a corollary, it is comparatively easy to extend CAIRIS, provided you follow the steps below. 

1.  Define the database tables
------------------------------

Each CAIRIS model is stored in its own MySQL database, so any new concept needs it own table or collection of tables.  These tables need to be defined in `cairis/sql/init.sql <https://github.com/cairis-platform/cairis/blob/master/cairis/sql/init.sql>`_  .  This SQL script is called every time a new model is created, so it's important this script contains no errors.  In many cases, errors occur if you forget to delete tables before creating them, or you define a table with foreign keys before defining its dependent data.

2.  Define the database procedures
----------------------------------

You need to create stored procedures for manipulating with your model data.  These are defined in `cairis/sql/procs.sql <https://github.com/cairis-platform/cairis/blob/master/cairis/sql/procs.sql>`_.  As a rule, each model concept has stored procedures for (i) retrieving objects, (i) adding objects, (ii) updating objects, and (iii) deleting objects.  As most objects are environment specific, there may be multiple procedures for (i) - (iii) depending on how complex the model object is.  Take a look at some existing concepts like assets, attackers, and goals to see how these idioms are implemented.

3.  Update the Python database proxy
------------------------------------

`cairis/core/MySQLDatabaseProxy.py <https://github.com/cairis-platform/cairis/blob/master/cairis/core/MySQLDatabaseProxy.py>`_ is the module responsible for interacting with the model database, so you'll need to add methods for retrieving, adding, updating, and deleting objects.  Again, looking at how this implemented using other CAIRIS should be a good source of inspiration.

4.  Write your model object test case
-------------------------------------

Each model concept in CAIRIS should have its own test case in `cairis/test <https://github.com/cairis-platform/cairis/tree/master/cairis/test>`_.  This effectively tests your stored procedures and methods in `cairis/core/MySQLDatabaseProxy.py <https://github.com/cairis-platform/cairis/blob/master/cairis/core/MySQLDatabaseProxy.py>`_ work correctly.  The idiom used is to create test data in JSON, and to create a test case that retrieves, adds, updates and deletes model objects.   

5.  Update the CAIRIS DTDs
--------------------------

CAIRIS XML models are defined in DTDs within `cairis/config <https://github.com/cairis-platform/cairis/tree/master/cairis/config>`_.  If your concept needs to go in a standard CAIRIS model file, it will need to be defined in `cairis_model.dtd <https://github.com/cairis-platform/cairis/blob/master/cairis/config/cairis_model.dtd>`_, but you may want to update other DTDs too. Because of how  CAIRIS models are imported, the location of the concept in the DTD is important because you'll want to ensure any dependent objects are created first.

6.  Update the model import / export code
-----------------------------------------

To ensure your exported CAIRIS model contains your model object, you need to make a number of changes.

First, within `cairis/sql/procs.sql <https://github.com/cairis-platform/cairis/blob/master/cairis/sql/procs.sql>`_ are a collection of stored procedures for generating XML for model objects, e.g. *riskAnalysisToXml* for risk analysis related concepts.  You need to edit the appropriate procedures to include the SQL necessary for retrieving your model objects and adding them to the generated XML.  If you don't have to add a new stored procedure for your concept/s then this is all you need to do to ensure your exported model contains your new concept.

Second, CAIRIS uses SAX to parse model files during the import process.  The different content handler classes used by the parser can be found in `cairis/mio <https://github.com/cairis-platform/cairis/tree/master/cairis/mio>`_ , and the appropriate class will need to be modified to create CAIRIS python objects to represent your model concepts.  You will then need to update `cairis/mio/ModelImport.py <https://github.com/cairis-platform/cairis/blob/master/cairis/mio/ModelImport.py>`_ to ensure these objects are subsequently added to the CAIRIS database the model is being imported into.

Finally, depending on how fundamental your changes are, it might be sensible to also update the server-side `import <https://github.com/cairis-platform/cairis/blob/master/cairis/bin/cimport.py>`_ and `export <https://github.com/cairis-platform/cairis/blob/master/cairis/bin/cexport.py>`_ scripts too.  These will provide you with a quick way of testing your import and export logic before delving too deeply into your API changes.

7.  Implement the server end-points
-----------------------------------

At this stage, you can start thinking about implementing the code that will handle the API end-points.  This involves updating and creating a number of files.
First, you need to create a Data Access Object (DAO) objects for your model concept in `cairis/data <https://github.com/cairis-platform/cairis/tree/master/cairis/data>`_ . In addition to acting as a wrapper for the database proxy, these objects are also responsible for marshalling Python objects to JSON (when retrieving objects), and vice-versa (when creating, updating, and deleting objects).
Second, you need to define the object in `cairis/tools/ModelDefinitions.py <https://github.com/cairis-platform/cairis/blob/master/cairis/tools/ModelDefinitions.py>`_ so Flask understands how to work this object.
Third, you need to define the end-points themselves in `cairis/daemon/main/views.py <https://github.com/cairis-platform/cairis/blob/master/cairis/daemon/main/views.py>`_.
Associated with each end-point will be an appropriate controller object in `cairis/controllers <https://github.com/cairis-platform/cairis/tree/master/cairis/controllers>`_ .  The object you choose will depend on the methods (i.e. get, post, put, del) you need to implement, and parameters you intend to use.

8.  Write your API test case
----------------------------

At this point, you should add a test case to `cairis/test <https://github.com/cairis-platform/cairis/tree/master/cairis/test>`_ to test your model API.  If you look at other test cases, you'll see the norm is to import a CAIRIS model before kicking off your tests.  To test the model import is working as it should, you might want to add your new model concepts to a CAIRIS model, import that, and try retrieving these in the tests.  The other API tests should provide inspiration for how you should go about testing the different API end-points

9.  Update the UI
-----------------

Until now, all the changes made will have been to the `CAIRIS <https://github.com/cairis-platform/cairis>`_ GitHub repository.  However, to update the UI, you will need to update the code in the `cairis-ui <https://github.com/cairis-platform/cairis-ui>`_ repository. Once the UI changes have been pushed to that repo, you should run the `installUI.sh <https://github.com/cairis-platform/cairis/blob/master/cairis/bin/installUI.sh>`_ as described the cairis-ui repository `README <https://github.com/cairis-platform/cairis-ui/blob/master/README.md>`_.

10. Update the documentation generation process
-----------------------------------------------

`cairis/misc/DocumentBuilder.py <https://github.com/cairis-platform/cairis/blob/master/cairis/misc/DocumentBuilder.py>`_ is responsible for interacting with the Python database proxy to rendering a DocBook specification, which forms the basis of generated documentation.  This will need to update this to ensure your model objects appear in the specification.  The module contains helper functions for generating things like lists and tables, so looking at how other model objects are handled should give you the knowledge necessary for incorporating your objects too.
