Sample models
=============

Exemplars
---------

CAIRIS comes with three complete system specifications.  These illustrate how CAIRIS can be used, and -- in some cases -- provide templates to inspire your own use of the platform.
These specifications are .cairis files can be found in the cairis/examples/exemplars directory, but their component model files and images can be found in sub-directories within that directory.

NeuroGrid
~~~~~~~~~

NeuroGrid is a a data grid for neuroscience research.  The sensitive of clinical data processed by NeuroGrid and its distributed nature drives the need to find secure and effective ways of accessing and managing it.  This exemplar is restricted to the upload and download of data to and from NeuroGrid.  This exemplar also comes with a physical locations file (Computing Laboratory) and an architectural pattern (WebDAV).


ACME Water
~~~~~~~~~~

ACME Water is a fictional water company concerned with the delivery of wastewater and cleanwater services in a specific geographic region of the UK.  This exemplar specifies a secure operating environment for SCADA, telemetry, and control systems associated with assets owned and operated by ACME.  This exemplar also comes with a physical localtions file (Poole Waste Water Treatment Works).

webinos
~~~~~~~

The `webinos <https://en.wikipedia.org/wiki/Webinos>`_ platform is a software runtime environment that allows the discovery of devices and services based on technical and contextual information.  It exposes a set of APIs that provide access to cross-user, cross-service, and cross-device functionality.  Unlike the other examples, the consistuent CAIRIS models were generated from a variety of formats including spreadsheets, text files, and multiple smaller CAIRIS model files.  You can find this design data and the scripts used to generate the model at `webinos-design-data GitHub repository <https://github.com/webinos/webinos-design-data>`_.  


Threat and Vulnerability Directories
------------------------------------

These are libraries of importable threats and vulnerabilities, and can be found in the cairis/examples/directories directory.

CWE/CAPEC
~~~~~~~~~

cwecapec_directory.xml contains a selection of threats and vulnerabilities from CWE and CAPEC.  To import this, it is first necessary to import cairis/examples/threat_vulnerability_types/cwecapec_tv_types.xml.

ICS Protection Profile
~~~~~~~~~~~~~~~~~~~~~~

ics_directory.xml contains a selection of threats and vulnerabilities from the System Protection Profile - Industrial Control Systems issued by NIST.  To import this, it is first necessary to import cairis/examples/threat_vulnerability_types/ics_tv_types.xml.

OWASP
~~~~~

owasp_directory.xml contains a selection of threats and vulnerabilties drawn from the OWASP body of knowledge.  To import this, it is first necessary to import cairis/examples/threat_vulnerability_types/owasp_tv_types.xml.
