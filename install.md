---
layout: default
title: Getting started
---

{% include toc.html %}

# Installing CAIRIS

## Web application

CAIRIS web services can be installed on any platform that its open-source dependencies are available for.  The most tested platforms are [Ubuntu](http://www.ubuntu.com) or [Debian](https://www.debian.org) Linux.  The web application itself should run on all good web browsers, irrespective of platform.

### Docker Hub

The easiest way of getting up and running with the web application is to download the CAIRIS container from [Docker hub](https://hub.docker.com/r/shamalfaily/cairis/).  This is built from the latest changes in github, and uses [mod_wsgi-express](https://pypi.python.org/pypi/mod_wsgi) to deliver the CAIRIS web services.

* Download and run the container, and its linked mysql container:  
{% highlight bash %}
$ sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.5
$ sudo docker run --name CAIRIS --link cairis-mysql:mysql -d -P -p 80:8000 --net=bridge shamalfaily/cairis
{% endhighlight %}


* From the web browser of your choice, connect to the CAIRIS URL, e.g. http://localhost
When asked for credentials, provide test/test

* If you want to interact with a pre-existing CAIRIS model, you can find some examples on the CAIRIS github, repository, e.g. [NeuroGrid](https://github.com/failys/cairis/blob/master/examples/exemplars/NeuroGrid/NeuroGrid.xml). You can import this from the System/Import menu, selecting type 'Model', and the model file to import. Allow a minute or two for this import to complete.

![fig:initStartup]({{ site.baseurl }}/images/CAIRIS_docker.jpg)

* Please feel free to use this container to evaluate CAIRIS, but do not use it for operational use. It uses all manner of default/easy-to-brute force credentials!

### Source installation and configuration

* Install the required applications and dependencies:

{% highlight bash %}
$ sudo apt-get install python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip python-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils
{% endhighlight %}

* Clone the latest version of the CAIRIS github repository, and use pip to install the dependencies in the root directory, i.e.

{% highlight bash %}
$ git clone https://github.com/failys/cairis
$ cd cairis
$ sudo pip install -r requirements.txt
{% endhighlight %}

* Run the CAIRIS quick setup initialisation script (which can be found in cairis/).  When you run this script, you should get the below form.

{% highlight bash %}
$ ./quick_setup.py
{% endhighlight %}

![fig:quick_setup_db]({{ site.baseurl }}/images/quick_setup_db.jpg)

You can accept many of these defaults, except for the database root password.  When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file; this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool and setup the necessary environment variables. The form below will then be displayed.

![fig:quick_setup_user]({{ site.baseurl }}/images/quick_setup_user.jpg)

You will need to supply a username and password here. When you select `Ok`, the script will add a user to the CAIRIS database.

* Reload your .bashrc file i.e.

{% highlight bash %}
source .bashrc
{% endhighlight bash%}

* Starting cairisd

If you want to run the Flask development servier, run `./cairisd.py runserver` (the script can be found in cairis/cairis/bin).  However, before doing this, you need to ensure CAIRIS has been installed to a location that the process running `cairisd` has write access to. Alternatively, if you want to web services to be accessed via mod_wsgi-express run `mod_wsgi-express start-server cairis.wsgi`; cairis.wsgi can also be found in cairis/cairis/bin.

* Use the application

You can now point your browser to http://SERVERNAME:PORT_NUMBER, depending on where `cairisd` is installed, and what port cairisd or mod_wsgi-express is listening to, e.g. http://myserver.org:7071.  Once you have authenticated, the application should load.

## Alternatively:

* Run the CAIRIS quick setup initialisation script (which can be found in cairis/).  When you run this script, you should get the below form.

{% highlight bash %}
$ ./quick_setup.py
{% endhighlight %}

![fig:configure_cairis_db]({{ site.baseurl }}/images/configure_cairis_db.jpg)

You can usually accept many of these defaults, you will however need to modify the location of the root directory and the static directory to reflect the location of the CAIRIS files. For example if you cloned the repository to the root directory you would change the root and static directories to look like the below.

![fig:change_configure_cairis_db]({{ site.baseurl }}/images/change_configure_cairis_db.jpg)

When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file;
this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool.

* Ensure the CAIRIS_CFG environment variable points to your CAIRIS configuration file, and is persistent, i.e.

{% highlight bash %}
$ echo export CAIRIS_CFG=/home/cairisuser/cairis.cnf >> .bashrc
{% endhighlight %}

* Ensure the PYTHONPATH environment variable points to your CAIRIS application location, and is persistent, i.e.

{% highlight bash %}
$ echo export PYTHONPATH=/home/cairisuser/cairis >> .bashrc
{% endhighlight %}

* Reload your .bashrc file i.e.

{% highlight bash %}
source .bashrc
{% endhighlight bash%}

* Add a user account

Run the `add_cairis_user` script in cairis/cairis/bin (run `add_cairis_user --help` to check the parameters you need to provide).

{% highlight bash %}
./add_cairis_user test test
{% endhighlight %}

* Starting cairisd

If you want to run the Flask development servier, run `./cairisd.py runserver` (the script can be found in cairis/cairis/bin).  However, before doing this, you need to ensure CAIRIS has been installed to a location that the process running `cairisd` has write access to. Alternatively, if you want to web services to be accessed via mod_wsgi-express run `mod_wsgi-express start-server cairis.wsgi`; cairis.wsgi can also be found in cairis/cairis/bin.

* Use the application

You can now point your browser to http://SERVERNAME:PORT_NUMBER, depending on where `cairisd` is installed, and what port cairisd or mod_wsgi-express is listening to, e.g. http://myserver.org:7071.  Once you have authenticated, the application should load.

## Desktop application (deprecated)

In theory, the desktop CAIRIS application can be installed on any platform that its open-source dependencies are available for.  In practice, CAIRIS has found to be most stable when running on [Ubuntu](http://www.ubuntu.com) or [Debian](https://www.debian.org) Linux.

### PyPI

* Install the required applications and dependencies:

{% highlight bash %}
$ sudo apt-get install python-wxglade python-glade2 python-wxgtk3.0 python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip python-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils
{% endhighlight %}


* Install CAIRIS:

{% highlight bash %}
$ sudo pip install cairis
{% endhighlight %}

* Run the CAIRIS database initialisation script `configure_cairis_db.py`.  You should be presented with the below form.

![fig:configure_cairis_db]({{ site.baseurl }}/images/configure_cairis_db.jpg)

Assuming you didn't customise the installation location of CAIRIS when running `pip`, you can usually accept many of these defaults, except for the name and location of the CAIRIS configuration file. When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file; this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool.

* Ensure the CAIRIS_CFG environment variable to points to your CAIRIS configuration file, and is persistent, i.e.

{% highlight bash %}
$ echo export CAIRIS_CFG=/home/cairisuser/cairis.cnf >> .bashrc
{% endhighlight %}

* Starting the CAIRIS desktop application

Open a terminal window and run `cairis_gui.py`.

{% highlight bash %}
cairis_gui.py
{% endhighlight %}

This main CAIRIS window is split in 2 halves.  The bottom half is the taken up the requirements editor.  The top half of the screen is taken up by the menu and tool-bar buttons.

![fig:initStartup]({{ site.baseurl }}/images/CAIRIS_new.jpg)

All the information entered into CAIRIS is stored in a single MySQL database, but all or part of a complete CAIRIS model can be imported and exported in XML.  CAIRIS comes with a several sample models; these can be found on github in the `cairis/examples` folder.  This can be imported by clicking on the File/Import/Model menu, and selecting the model file to be imported.

Model files can also be imported from the command line by using `cimport.py`.     

{% highlight bash %}
$ cimport.py --type all --overwrite 1 --image_dir . NeuroGrid.xml
{% endhighlight %}

The type `all` refers to a complete model file.  Individual parts of models can also be imported.  These might include models of individual personas, goal models, or risk analysis data.  Use the --help option to get a detailed list of importable model types.  

If the overwrite option is set then the import process will overwrite any existing data that might already be in the CAIRIS database.  This can be useful if you want to cleanly import a new model file.

If the image_dir option is set then CAIRIS will look for somewhere other than the default_image_dir location (specified in cairis.cnf) for any image files associated with the model.  Such image files include pictures for personas and attackers, or rich picture diagrams.

### Source installation and configuration

This is identical to the PyPI installation, but instead of install CAIRIS from PyPI, you instead need to clone the latest version of the CAIRIS repository, and install the dependent PyPI packages manually.

{% highlight bash %}
$ git clone https://github.com/failys/cairis
$ cd cairis
$ sudo pip install -r requirements.txt
{% endhighlight %}

Once the packages have been installed, you can run `configure_cairis_db.py`, and follow the rest of the PyPI instructions. All the scripts you need to run can be found in cairis/cairis/bin.
