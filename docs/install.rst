Installing CAIRIS
=================

Installation via Docker
~~~~~~~~~~~~~~~~~~~~~~~

If you have Docker installed on your laptop or an available machine, the easiest way of getting up and running with the web application is to download the CAIRIS container from `Docker hub <https://hub.docker.com/r/shamalfaily/cairis/>`_.  Like the live demo, this is built from the latest version of CAIRIS in GitHub, and uses `mod_wsgi-express <https://pypi.python.org/pypi/mod_wsgi>`_ to deliver the CAIRIS web services.

Download and run the container, and its linked mysql container:

.. code-block:: bash
 
   sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7
   sudo docker run --name CAIRIS --link cairis-mysql:mysql -d -P -p 80:8000 --net=bridge shamalfaily/cairis

From your web browser, connect to the CAIRIS URL, e.g. http://localhost
When asked for credentials, provide test/test

If you want to interact with a pre-existing CAIRIS model, you can find some examples on the CAIRIS github, repository, e.g. `NeuroGrid <https://github.com/failys/cairis/blob/master/examples/exemplars/NeuroGrid/NeuroGrid.xml>`_. You can import this from the System/Import menu, selecting type 'Model', and the model file to import. Allow a minute or two for this import to complete.

.. figure:: CAIRIS_docker.jpg
   :alt: CAIRIS front page

Please feel free to use this container to evaluate CAIRIS, but do not use it for operational use without configuring the default credentials first.  The scripts used to build the container can be found on `GitHub <https://github.com/failys/cairis/tree/master/docker>`_, and provides a useful template for getting started.

Installation and configuration via GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're happy to use the command line, you may like to install CAIRIS from the latest source code in GitHub.  CAIRIS can be installed on any platform that its open-source dependencies are available for.  The most tested platforms are `Ubuntu <http://www.ubuntu.com>`_ or `Debian <https://www.debian.org>`_ .  Assuming you are using some flavour of Linux, just follow the steps below:

Begin by installing the required applications and dependencies:

.. code-block:: bash

   sudo apt-get install python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip python-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils python-setuptools

Clone the latest version of the CAIRIS github repository, and use pip to install the dependencies in the root directory, i.e.

.. code-block:: bash

   git clone https://github.com/failys/cairis
   cd cairis
   sudo pip install -r requirements.txt

Run the CAIRIS quick setup initialisation script (which can be found in cairis/).  When you run this script, you should get the below form.

.. code-block:: bash

   ./quick_setup.py

.. figure:: quick_setup_db.jpg
   :alt: Quick setup script

You can accept many of these defaults, except for the database root password, an initial username and password which need to be supplied.  If you want more diagnostic information logged, you find it useful to change the Log Level from *warning* to *debug*.  When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file; this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool and setup the necessary environment variables.

Logout of your current account or, alternatively, reload your .bashrc file i.e.

.. code-block:: bash

   source .bashrc

You should now start up your CAIRIS server.  If you are the only person that plans to use CAIRIS, using the Flask development server to run cairisd should be sufficient; you can find cairisd in the cairis/cairis/bin directory.

.. code-block:: bash

   ./cairisd.py runserver

[Optional] Multiple users using CAIRIS

If multiple users will be using CAIRIS, or you want to run CAIRIS in a production environment then it may be sensible to use mod_wsgi-express rather than cairisd.  
To do this, you will need to install the requisite Apache2 packages.

.. code-block:: bash

   sudo apt-get install apache2 apache2-dev

You will then need to use pip to install the requisite dependencies.

.. code-block:: bash

   sudo pip install -r wsgi_requirements.txt

You should then use mod_wsgi-express to run cairis.wsgi (also in cairis/cairis/bin):

.. code-block:: bash

   mod_wsgi-express start-server cairis.wsgi

[Optional] Additional steps for developers

If you plan to customise CAIRIS, development extensions or fixes, you should install the requisite packages for running the tests in cairis/cairis/test.

.. code-block:: bash

   sudo pip install -r test_requirements.txt

You should also set the `CAIRIS_SRC` and `CAIRIS_CFG_DIR` environment variables in your .bashrc file.

.. code-block:: bash

   export CAIRIS_SRC=/home/cairisuser/cairis/cairis
   export CAIRIS_CFG_DIR=${CAIRIS_SRC}/config
