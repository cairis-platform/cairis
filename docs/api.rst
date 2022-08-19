Using the CAIRIS API
====================

API documentation
-----------------

API documentation can be found on `SwaggerHub <https://app.swaggerhub.com/apis/failys/CAIRIS>`_. 

SwaggerHub provides a virtual server at https://virtserver.swaggerhub.com/failys/CAIRIS you can use to quickly test get/post/put/delete methods on end-points without setting up CAIRIS, authenticating, etc.


.. code-block:: bash
 
   curl https://virtserver.swaggerhub.com/failys/CAIRIS/1.0.9/api/attackers
   [ {
  "theName" : "Carol",
  "theImage" : "Carol.jpg",
  "theDescription" : "Carol is a freelance journalist working in the South East of England.  Having heard stories about data theft, she is currently investigating a number of e-Science projects, including NeuroGrid, to see if she can find a story.",
  "theTags" : [ ],
  "theEnvironmentProperties" : [ {
    "theMotives" : [ "Headlines/press" ],
    "theRoles" : [ "Social Engineer" ],
    "theCapabilities" : [ {
      "name" : "Resources/Personnel and Time",
      "value" : "Medium"
    }, {
      "name" : "Resources/Funding",
      "value" : "Low"
    } ],
    "theEnvironmentName" : "Psychosis"
  } ]
} ]

Authenticating with the CAIRIS server
-------------------------------------

For a more representative test, you'll want to run up cairisd and import a model. If you do this, the first thing you need to do is authentication to get a session. You can get this by posting to /api/session with your credentials. Let's assume our username and password is test@test.com and test:

.. code-block:: bash

   curl -u test@test.com -X POST http://localhost:7071/api/session
   Enter host password for user 'test@test.com':
   {"message": "Session created", "session_id": "S9A3U7XkKEzqPwjwzKqR8jPGPVK0dvtf", "user": "test@test.com"}

By default, the session will point to the user's default database, but posting to api/settings/database/{name}/open can change the database the session points to, where name is the name of the database you want to point to.

When using the API in production use, the session should be included in header but, for development, you can add session_id as a parameter to the URL, e.g

.. code-block:: bash

   curl http://localhost:7071/api/roles?session_id=S9A3U7XkKEzqPwjwzKqR8jPGPVK0dvtf
   [{"theDescription": "Authorises access requests for NeuroGrid and responsible for day-to-day administration.", "theName": "Certificate Authority", "theShortCode": "CA", "theType": "Stakeholder"}, {"theDescription": "Uses NeuroGrid data", "theName": "Data Consumer", "theShortCode": "DCON", "theType": "Stakeholder"}, {"theDescription": "Supplies data to NeuroGrid", "theName": "Data Provider", "theShortCode": "DPRO", "theType": "Stakeholder"}, {"theDescription": "Develops NeuroGrid applications based on the provided NeuroGrid API and services.", "theName": "Developer", "theShortCode": "DEV", "theType": "Stakeholder"}, {"theDescription": "Professional or semi-professional hacker", "theName": "Hacker", "theShortCode": "AKR", "theType": "Attacker"}, {"theDescription": "Uses and supplies data to NeuroGrid", "theName": "Researcher", "theShortCode": "RCHR", "theType": "Stakeholder"}, {"theDescription": "Uses human frailty to access computational resources.", "theName": "Social Engineer", "theShortCode": "SENG", "theType": "Stakeholder"}, {"theDescription": "Responsible for day-to-day administration of NeuroGrid, including authorisation of access requests.", "theName": "Sysadmin", "theShortCode": "SYSADMIN", "theType": "Stakeholder"}]

The cairis_test database
------------------------

As part of the quick setup process, a cairis_test database is created (password: cairis_test). Associated with this database is the session_id test . This database makes it possible to do general front-end development and testing without worrying about authentication.

You can import models directly into this database by using cimport.py without setting the user and database parameters. You can also use any end-points with this session_id, e.g.


.. code-block:: bash

   curl http://localhost:7071/api/requirements?session_id=test
   [
     {
       "theDescription": "Access to a NeuroGrid data-set shall be governed by an access control policy.",
       "theFitCriterion": "None",
       "theLabel": "AC-1",
       "theName": "Dataset policy",
       "theOriginator": "Interview data",
       "thePriority": 1,
       "theRationale": "Need to determine which users can do what.",
       "theType": "Functional"
     },
     {
       "theDescription": "Requests for NeuroGrid access shall be authorised by the nominated clinical exemplar sponsor.",
       "theFitCriterion": "None",
       "theLabel": "AC-2",
       "theName": "Access sponsor",
       "theOriginator": "Interview data",
       "thePriority": 1,
       "theRationale": "None",
       "theType": "Operational"
     }
   ]
