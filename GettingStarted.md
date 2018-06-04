---
layout: page
title: Getting Started
order: 1
discription : Install Guidance and Examples on How to Install Via Github or Docker
---

<h2>Live Demo</h2>
<p>A live demo of CAIRIS is available to use on <a href="https://demo.cairis.org">demo.cairis.org</a>.  The username and password you need are <em>test</em> and <em>test</em>.</p>
<p>The live demo comes with two example models: <a href="https://cairis.org/NeuroGrid">NeuroGrid</a> and <a href="https://cairis.org/ACME_Water">ACME Water</a>.  To open these, select the System / Open Database menu, and choose the model to open.</p>
<p>The live demo is rebuilt every night based on the latest updates to CAIRIS, so please feel free to add, update, or remove elements in the example models, or even create new CAIRIS databases.  If anything is unclear, please take a look at the <a href="https://cairis.readthedocs.io">documentation</a>.  If anything in the documentation is unclear, or anything on the live demo appears broken then please <a href="https://github.com/failys/cairis/issues">raise an issue in GitHub</a> and we’ll look into it.</p>
<hr />

<h2>Installing CAIRIS</h2>
<h3>Installation via Docker</h3>

If you have Docker installed on your laptop or an available machine, the easiest way of getting up and running with the web application is to download the CAIRIS container from [Docker hub](https://hub.docker.com/r/shamalfaily/cairis/).  This is built from the latest changes in github, and uses [mod_wsgi-express](https://pypi.python.org/pypi/mod_wsgi) to deliver the CAIRIS web services.

* Download and run the container, and its linked mysql container:  
{% highlight bash %}
$ sudo docker run --name cairis-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7
$ sudo docker run --name CAIRIS --link cairis-mysql:mysql -d -P -p 80:8000 --net=bridge shamalfaily/cairis
{% endhighlight %}

* From the web browser of your choice, connect to the CAIRIS URL, e.g. http://localhost
When asked for credentials, provide test/test

* If you want to interact with a pre-existing CAIRIS model, you can find some examples on the CAIRIS github, repository, e.g. [NeuroGrid](https://github.com/failys/cairis/blob/master/examples/exemplars/NeuroGrid/NeuroGrid.xml). You can import this from the System/Import menu, selecting type 'Model', and the model file to import. Allow a minute or two for this import to complete.

<p><img src="/images/CAIRIS_docker.jpg" alt="fig:initStartup" style="width:100%;height:100%;"/></p>

* Please feel free to use this container to evaluate CAIRIS, but do not use it for operational use. It uses all manner of default/easy-to-brute force credentials!

<h2 id="installation-and-configuration-via-github">Installation and configuration via GitHub</h2>

CAIRIS web services can be installed on any platform that its open-source dependencies are available for.  The most tested platforms are [Ubuntu](http://www.ubuntu.com) or [Debian](https://www.debian.org) Linux.

* Install the required applications and dependencies:

{% highlight bash %}
$ sudo apt-get install python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip python-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils inkscape libxml2-dev libxslt1-dev poppler-utils python-setuptools
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

You can accept many of these defaults, except for the database root password, an initial username and password which need to be supplied.  When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file; this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool and setup the necessary environment variables.

* Reload your .bashrc file i.e.

{% highlight bash %}
source .bashrc
{% endhighlight bash%}

* Starting the cairisd

If you want to run the Flask development server, run `./cairisd.py runserver` (the script can be found in cairis/cairis/bin).   

* Starting mod_wsgi-express

If you want to run CAIRIS in a production environment then it may be sensible to use mod_wsgi-express rather than the Flask development server.  To do this, you will need to install the requisite Apache2 packages.

{% highlight bash %}
$ sudo apt-get install apache2 apache2-dev
{% endhighlight %}

You will then need to use pip to install the requisite dependencies.

{% highlight bash %}
$ sudo pip install -r wsgi_requirements.txt
{% endhighlight %}

To start mod_wsgi-express, you should run `mod_wsgi-express start-server cairis.wsgi`; cairis.wsgi can also be found in cairis/cairis/bin.

* Use the application

You can now point your browser to http://SERVERNAME:PORT_NUMBER, depending on where `cairisd` is installed, and what port cairisd or mod_wsgi-express is listening to, e.g. http://myserver.org:7071.

* [Optional] Additional steps for developers

If you plan to develop for CAIRIS, you should install the requisite packages for running the tests in cairis/cairis/test.

{% highlight bash %}
$ sudo pip install -r test_requirements.txt
{% endhighlight %}

You should also set the `CAIRIS_SRC` and `CAIRIS_CFG_DIR` environment variables in your .bashrc file.

{% highlight bash %}
export CAIRIS_SRC=/home/cairisuser/cairis/cairis
export CAIRIS_CFG_DIR=${CAIRIS_SRC}/config
{% endhighlight %}
