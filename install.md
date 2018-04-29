---
layout: default
title: Getting started
---

{% include toc.html %}

# Live Demo

A live demo of CAIRIS is available to use on [demo.cairis.org](https://demo.cairis.org).  The username and password you need are *test* and *test*. Internet Explorer isn't supported by CAIRIS.  CAIRIS does, however, work well with Edge, Safari, Chrome, Firefox, and Opera.

The live demo comes with two example models: [NeuroGrid](https://cairis.org/NeuroGrid) and [ACME Water](https://cairis.org/ACME_Water).  To open these, select the System / Open Database menu, and choose the model to open.

The live demo is rebuilt every night based on the latest updates to CAIRIS, so please feel free to add, update, or remove elements in the example models, or even create new CAIRIS databases.  If anything is unclear, please take a look at the [documentation](https://cairis.readthedocs.io).  If anything in the documentation is unclear, or anything on the live demo appears broken then please [raise an issue in GitHub](https://github.com/failys/cairis/issues) and we'll look into it.


# Installing CAIRIS

## Installation via Docker

If you have Docker installed on your laptop or an available machine, the easiest way of getting up and running with the web application is to download the CAIRIS container from [Docker hub](https://hub.docker.com/r/shamalfaily/cairis/).  Like the live demo, this is built from the latest version of CAIRIS in GitHub, and uses [mod_wsgi-express](https://pypi.python.org/pypi/mod_wsgi) to deliver the CAIRIS web services.

* Download and run the container, and its linked mysql container:  
{% highlight bash %}
sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7
sudo docker run --name CAIRIS --link cairis-mysql:mysql -d -P -p 80:8000 --net=bridge shamalfaily/cairis
{% endhighlight %}


* From your web browser, connect to the CAIRIS URL, e.g. http://localhost
When asked for credentials, provide test/test

* If you want to interact with a pre-existing CAIRIS model, you can find some examples on the CAIRIS github, repository, e.g. [NeuroGrid](https://github.com/failys/cairis/blob/master/examples/exemplars/NeuroGrid/NeuroGrid.xml). You can import this from the System/Import menu, selecting type 'Model', and the model file to import. Allow a minute or two for this import to complete.

![fig:initStartup]({{ site.baseurl }}/images/CAIRIS_docker.jpg)

* Please feel free to use this container to evaluate CAIRIS, but do not use it for operational use without configuring the default credentials first.  The scripts used to build the container can be found on [GitHub](https://github.com/failys/cairis/tree/master/docker), and provides a useful template for getting started.


## Installation and configuration via GitHub

If you're happy to use the command line, you may like to install CAIRIS from the latest source code in GitHub.  CAIRIS can be installed on any platform that its open-source dependencies are available for.  The most tested platforms are [Ubuntu](http://www.ubuntu.com) or [Debian](https://www.debian.org) Linux.  Assuming you are using some flavour of Linux, just follow the steps below:

* Install the required applications and dependencies:

{% highlight bash %}
sudo apt-get install python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip python-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils python-setuptools
{% endhighlight %}

* Clone the latest version of the CAIRIS github repository, and use pip to install the dependencies in the root directory, i.e.

{% highlight bash %}
git clone https://github.com/failys/cairis
cd cairis
sudo pip install -r requirements.txt
{% endhighlight %}

* Run the CAIRIS quick setup initialisation script (which can be found in cairis/).  When you run this script, you should get the below form.

{% highlight bash %}
./quick_setup.py
{% endhighlight %}

![fig:quick_setup_db]({{ site.baseurl }}/images/quick_setup_db.jpg)

You can accept many of these defaults, except for the database root password, an initial username and password which need to be supplied.  If you want more diagnostic information logged, you find it useful to change the Log Level from *warning* to *debug*.  When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file; this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool and setup the necessary environment variables.

* Logout of your current account or, alternatively, reload your .bashrc file i.e.

{% highlight bash %}
source .bashrc
{% endhighlight bash%}

* Starting the cairisd

If you are the only person that plans to use CAIRIS, using the Flask development server to run CAIRIS services should be sufficient, so run `./cairisd.py runserver` (the script can be found in cairis/cairis/bin).   

* Starting mod_wsgi-express

If multiple users will be using CAIRIS, or you want to run CAIRIS in a production environment then it may be sensible to use mod_wsgi-express rather than the Flask development server.  To do this, you will need to install the requisite Apache2 packages.

{% highlight bash %}
sudo apt-get install apache2 apache2-dev
{% endhighlight %}

You will then need to use pip to install the requisite dependencies.

{% highlight bash %}
sudo pip install -r wsgi_requirements.txt
{% endhighlight %}

To start mod_wsgi-express, you should run `mod_wsgi-express start-server cairis.wsgi`; cairis.wsgi can also be found in cairis/cairis/bin.

* Use the application

You can now point your browser to http://SERVERNAME:PORT_NUMBER, depending on where `cairisd` is installed, and what port cairisd or mod_wsgi-express is listening to, e.g. http://myserver.org:7071.

* [Optional] Additional steps for developers

If you plan to customise CAIRIS, development extensions or fixes, you should install the requisite packages for running the tests in cairis/cairis/test.

{% highlight bash %}
sudo pip install -r test_requirements.txt
{% endhighlight %}

You should also set the `CAIRIS_SRC` and `CAIRIS_CFG_DIR` environment variables in your .bashrc file.

{% highlight bash %}
export CAIRIS_SRC=/home/cairisuser/cairis/cairis
export CAIRIS_CFG_DIR=${CAIRIS_SRC}/config
{% endhighlight %}
