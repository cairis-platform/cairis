Installing CAIRIS
=================

Installation via Docker
~~~~~~~~~~~~~~~~~~~~~~~

If you have Docker installed on your laptop or an available machine, the easiest way of getting up and running with the web application is to download the CAIRIS container from `Docker hub <https://hub.docker.com/r/shamalfaily/cairis/>`_.  Like the live demo, this is built from the latest version of CAIRIS in GitHub, and uses `mod_wsgi-express <https://pypi.python.org/pypi/mod_wsgi>`_ to deliver the CAIRIS web services.

There are two options for running the container, a full install of everything or a smaller install which doesn't provide pdf export functionality:

For the full install (with pdf export functionality) download and run the container, the documentation container, and its linked mysql container:

.. code-block:: bash
 
   sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7 --thread_stack=256K
   sudo docker run --name cairis-docs -d -v cairisDocumentation:/tmpDocker -v cairisImage:/images -t shamalfaily/cairis-docs
   sudo docker run --name CAIRIS -d --link cairis-mysql:mysql --link cairis-docs:docs -P -p 80:8000 --net=bridge -v cairisDocumentation:/tmpDocker -v cairisImage:/images shamalfaily/cairis

For the smaller install (without pdf export functionality) download and run the container, and its linked mysql container:

.. code-block:: bash
 
   sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7 --thread_stack=256K
   sudo docker run --name CAIRIS --link cairis-mysql:mysql -d -P -p 80:8000 --net=bridge shamalfaily/cairis

The *docker run* commands will create and start-up CAIRIS, but you will need to create an account before you can use it.  To do this, run the below command - replacing test and test with your desired username and password. 

.. code-block:: bash

   docker exec -t `docker ps | grep shamalfaily/cairis | head -1 | cut -d ' ' -f 1` /addAccount.sh test test TestUser

Once the containers have been installed then, in the future, you should use *docker start* rather than *docker run* to start up the already downloaded containers.

.. code-block:: bash
 
   sudo docker start cairis-mysql 
   sudo docker start CAIRIS

The containers can be stopped using *docker stop*, i.e.

.. code-block:: bash

   sudo docker stop CAIRIS
   sudo docker stop cairis-mysql

To update your docker containers, stop the docker containers and run the below commands to remove any old containers and volume files. Following that, you can re-run the above *docker run* commands to install and run the container.  Don't forget to re-add your user account!

.. code-block:: bash

   sudo docker rm $(sudo docker ps -aq)
   sudo docker rmi --force $(sudo docker images -q)
   sudo docker volume rm $(docker volume ls)


Please feel free to use this container to evaluate CAIRIS, but do not use it for operational use without configuring the default credentials first.  The scripts used to build the container can be found on `GitHub <https://github.com/cairis-platform/cairis/tree/master/docker>`_, and provides a useful template for getting started.

Ubuntu CAIRIS Virtual Machine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have VMWare then you can download an Ubuntu CAIRIS virtual machine from `here <https://drive.google.com/open?id=1DT6B_3DaoZ1a8XAI8QAhigq8LPu7lrOJ>`_ .  This is Ubuntu VM was created using the quickInstall.sh script described in the section below.  To login to the VM, the username/password is cairisuser/cairisuser.  The account contains a short-cut to Chromium, which has the Persona Helper chrome extension installed.


Installation and configuration via GitHub (automated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a clean Ubuntu 19.04 VM, you can quickly install and configure CAIRIS and its dependencies with the command below, replacing my-secret-pw with your desired root password for MySQL.

.. code-block:: bash

   sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y && sudo apt install curl -y && sudo apt install net-tools -y && curl -s https://cairis.org/quickInstall.sh | bash -s my-secret-pw

In addition to configuring and installing CAIRIS, the script creates an initial user account (username: test, password: test), starts cairisd.py as a service, and restarts the VM.  You can use *journalctl* to check the CAIRIS log file.

.. code-block:: bash

   journalctl -u cairis.service -f

This script also adds an alias so, in future, you can update CAIRIS by running the below command:

.. code-block:: bash

   update_cairis

Installation and configuration via GitHub (manual)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're happy to use the command line, you may like to install CAIRIS from the latest source code in GitHub.  CAIRIS can be installed on any platform that its open-source dependencies are available for.  The most tested platforms are `Ubuntu <http://www.ubuntu.com>`_ or `Debian <https://www.debian.org>`_ .  Please note that these steps are currently not supported on Ubuntu 19.10 as MySQL 8 is not currently supported.  Assuming you are using some flavour of Linux, just follow the steps below:

Begin by installing the required applications and dependencies:

.. code-block:: bash

   sudo apt-get install python3-dev build-essential mysql-server mysql-client graphviz docbook dblatex python3-pip python3-mysqldb python3-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils python3-setuptools pandoc

If you are installing Ubuntu 18.04 LTS or later, or have not been prompted to set a root database password, you will need to set this manually.  You can find instructions on how to do that `here <https://linuxconfig.org/how-to-reset-root-mysql-password-on-ubuntu-18-04-bionic-beaver-linux>`_.

Clone the latest version of the CAIRIS github repository, and use pip to install the dependencies in the root directory, i.e.

.. code-block:: bash

   git clone https://github.com/cairis-platform/cairis
   cd cairis
   sudo pip3 install -r requirements.txt

Run the CAIRIS quick setup initialisation script (which can be found in cairis/).  When you run this script, you should get the below form.

.. code-block:: bash

   ./quick_setup.py

.. figure:: quick_setup_db.jpg
   :alt: Quick setup script

You can accept many of these defaults, except for the database root password, an initial username and password which need to be supplied.  Please note that the username *root* is reserved, so you should not use this.  

Details for the mail server only need to be set if you intend to provide self-service registration and reset of accounts.  This is typically only necessary if you plan to install CAIRIS to a server for multiple users.  When these settings are set, the mail server and port should be for out-going SSL traffic.

If you want more diagnostic information logged, you find it useful to change the Log Level from *warning* to *debug*.  

The static and directory and asset directory will point to the location of UI code, but these directories will not be created during this step. If you don't plan to customise your web server setup, you should retain these default values.

When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file; this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool and setup the necessary environment variables.


Logout of your current account or, alternatively, reload your .bashrc file i.e.

.. code-block:: bash

   source .bashrc

The final step entails installing the UI code by running the below script in cairis/cairis/bin

.. code-block:: bash

   sudo -E ./installUI.sh

The CAIRIS UI code is managed in the `cairis-ui github repository <https://github.com/cairis-platform/cairis-ui>`_.  Running this script will setup `node <https://nodejs.org>`_ and `yarn <https://yarnpkg>`_, download the github repo, create a production version of the latest UI code and deploy to cairis/cairis/dist.
The -E flag is required, as the CAIRIS_SRC environment variable needs to be visible to root.

You should now start up your CAIRIS server.  If you plan to develop with CAIRIS, you should skip this step as you'll find it more useful to manually start the development cairisd server.  For everyone else, create the following *cairis.service* file, substituting *cairisuser* for the name of your account.  Using sudo or root, copy this file to /etc/systemd/system.

.. code-block:: bash

   [Unit]
   Description=cairisd

   [Service]
   User=cairisuser
   WorkingDirectory=/home/cairisuser/cairis
   Environment="CAIRIS_CFG=/home/cairisuser/cairis.cnf"
   Environment="PYTHONPATH=${PYTHONPATH}:/home/cairisuser/cairis"
   ExecStart=/home/cairisuser/cairis/cairis/bin/cairisd.py runserver
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target

You can now launch cairisd as a system service:

.. code-block:: bash

   sudo systemctl enable --now /etc/systemd/system/cairis.service

[Optional] Multiple users using CAIRIS

cairisd relies on the Flask development server, which is fine for a single user, or development and troubleshooting.  However, if multiple users will use the same CAIRIS service at once, or you want to run CAIRIS in a production environment then it may be sensible to use mod_wsgi-express instead.
To do this, you will need to install the requisite Apache2 packages.

.. code-block:: bash

   sudo apt-get install apache2 apache2-dev

You will then need to use pip to install the requisite dependencies.

.. code-block:: bash

   sudo pip3 install -r wsgi_requirements.txt

You should then use mod_wsgi-express to run cairis.wsgi (also in cairis/cairis/bin):

.. code-block:: bash

   mod_wsgi-express start-server cairis.wsgi

Don't forget to modify *cairis.service* accordingly!

[Optional] Additional steps for developers

If you plan to customise CAIRIS, development extensions or fixes, you should install the requisite packages for running the tests in cairis/cairis/test.

.. code-block:: bash

   sudo pip3 install -r test_requirements.txt

To start the CAIRIS development server, run the cairisd.py script, i.e. from the cairis/cairis/bin directory

.. code-block:: bash

   ./cairisd.py runserver

All logged output is sent to the console where you started cairisd.py, which is useful when it come to diagnosing any problems.  Also, if you plan to use pytest to debug any CAIRIS server code (i.e. by adding import pytest and pytest.set_trace() before any code you want to debug), the debug prompt will appear in the console.
