Environments
============

An environment might represent a system operating at a particular time
of day, or in a particular physical location. Environments encapsulate
visible phenomena such as assets, tasks, personas, and attackers, as
well as invisible phenomena, such as goals, vulnerabilities, and
threats. Environments may be identified at any time, although these may
not become apparent until carrying out contextual inquiry and observing
how potential users reason about their context of use.

Adding a new environment
------------------------

.. figure:: EnvironmentForm.jpg
   :alt: Environment form

-  Select the UX/Environments menu to open the Environments
   form, and click on the Add button to open the new Environment
   form.

-  Enter the name of the environment, a short code, and a description.
   The short-code is used to prefix requirement ids associated with an
   environment.

-  If this environment is to be a composite environment, i.e. encompass
   artifacts of other environments, then click on the Add button the environment table, and select the environment to add.
   
-  It is possible an artifact may appear in multiple environments within a
   composite environment. It is, therefore, necessary to set duplication
   properties for composite environments. If the maximise radio button
   is selected, then the maximal values associated with that artifact
   will be adopted. This may be the highest likelihood value for a
   threat, or the highest security property values for an asset. If the
   override radio button is selected then CAIRIS will ensure that the
   artifact properties are used for the overriding environment.

.. note::
   Composite environments are an experimental feature and you may get errors when using them.
