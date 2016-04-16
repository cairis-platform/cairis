---
layout: default
title: Getting started
---

{% include toc.html %}

# Setting up CAIRIS

## Obtaining a virtual appliance

If you want to get up-and-running quickly, you can simply download an Ubuntu [pre-configured virtual machine disk file](https://drive.google.com/open?id=0Bx5c5XNaOMoTM1RsclRjYTVSSGs).  With this file, you can create a [custom virtual machine using VMWare](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=2010196), or create [a new VM in VirtualBox using the file as an existing hard disk](https://www.virtualbox.org/manual/ch01.html#gui-createvm).  When you login into the VM, you should find the CAIRIS icon available from the launcher.  Just click on the icon in the launcher, and you should be good to go.

The user name and password for this virtual machine is *cairis*; this is also the root password.  The root password for mysql is blank.  If you wish to use this virtual appliance in production, please ensure you change these default passwords first!

## Installing from source

In theory, CAIRIS can be installed on any platform that its open-source dependencies are available for.  In practice, CAIRIS is developed using Linux, and is most stable when running on [Ubuntu](http://www.ubuntu.com) or [Debian](https://www.debian.org) Linux.

Thanks go to [Robin Quetin](https://github.com/RobinQuetin) for putting these instructions together.

* Install the required applications and dependencies:

{% highlight bash %}
$ sudo apt-get install python-wxglade python-glade2 python-wxgtk2.8 python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip python-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils
{% endhighlight %}

* Install the Python extensions:

{% highlight bash %}
$ sudo pip install mysql-python==1.2.3 pyparsing==1.5.7 pydot
{% endhighlight %}

* Clone the CAIRIS repository into a directory, for example /opt/:

{% highlight bash %}
$ CAIRIS_DIR=/opt/cairis
$ sudo git clone https://github.com/failys/cairis.git $CAIRIS_DIR
{% endhighlight %}

* Create a new user group, and change permissions

{% highlight bash %}
$ CAIRIS_DIR=/opt/cairis
$ CAIRIS_USER=cairis
$ sudo useradd --no-create-home --system $CAIRIS_USER
$ sudo usermod -a -G $CAIRIS_USER $USER
$ sudo chown -R $CAIRIS_USER:$CAIRIS_USER $CAIRIS_DIR
$ sudo chmod -R 775 $CAIRIS_DIR
{% endhighlight %}

* Create a new database for CAIRIS with a MySQL user account which has full access to the database.  For this example, we assume our username is cairis, the password is cairis123, and database is called cairis:

{% highlight sql %}
> GRANT USAGE ON *.* TO 'cairis'@'localhost' IDENTIFIED BY 'cairis123' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0;
> CREATE DATABASE IF NOT EXISTS `cairis`;
> GRANT ALL PRIVILEGES ON `cairis`.* TO 'cairis'@'localhost';
{% endhighlight %}

* Create the database tables and stored procedures required by CAIRIS:

{% highlight bash %}
$ CAIRIS_SQL=$CAIRIS_DIR/cairis/sql
$ mysql --user=cairis –-password=cairis123 –-database=cairis < $CAIRIS_SQL/init.sql
$ mysql --user=cairis –-password=cairis123 –-database=cairis < $CAIRIS_SQL/procs.sql
{% endhighlight %}

* To view certain models in CAIRIS, change the maximum recursion depth for stored procedures to 255 from the default of 0.

{% highlight bash %}
$ mysql -h localhost -u root -p << !
set global max_sp_recursion_depth = 255; flush tables;
flush privileges;
!
{% endhighlight %}

* Create a configuration file for CAIRIS.  By default, CAIRIS looks for a configuration file in the home directory of the user.  You can use the template configuration file provided with CAIRIS as your base configuration.

{% highlight bash %}
$ mkdir -p ~/cairis/cairis/config/
$ cp $CAIRIS_DIR/cairis/config/cairis.cnf ~/cairis/cairis/config/
$ sudo chown -R $USER:$USER ~/cairis
{% endhighlight %}

* Change the values of the configuration file according to your installation.  Note that the 'root' is the directory of the CAIRIS application, which in our our case is `$CAIRIS_DIR/cairis`.

{% highlight bash %}
dbhost = 127.0.0.1
dbport = 3306
dbuser = cairis
dbpasswd = cairis123
dbname = cairis
tmp_dir = /tmp
root = /opt/cairis
default_image_dir = .
{% endhighlight %}


# Starting CAIRIS

To start CAIRIS, you can open a terminal window and go to `$CAIRIS_DIR/bin`.

{% highlight bash %}
$ python cairis_gui.py
{% endhighlight %}

This main CAIRIS window is split in 2 halves.  The bottom half is the taken up the requirements editor.  The top half of the screen is taken up by the menu and tool-bar buttons.

![fig:initStartup]({{ site.baseurl }}/images/CAIRIS_new.jpg)
*An empty CAIRIS project*

All the information entered into CAIRIS is stored in a single MySQL database, but all or part of a complete CAIRIS model can be imported and exported in XML.  CAIRIS comes with a several sample models; these can be found in `$CAIRIS_DIR/examples`.  This can be imported by clicking on the File/Import/Model menu, and selecting the model file to be imported.

Model files can also be imported from the command line by using the `cimport.py` script in `$CAIRIS_DIR/bin`.     

{% highlight bash %}
$ python cimport.py --type all --overwrite 1 --image_dir ../../examples/exemplars/NeuroGrid examples/exemplars/NeuroGrid/NeuroGrid.xml
{% endhighlight %}

The type `all` refers to a complete model file.  Individual parts of models can also be imported.  These might include models of individual personas, goal models, or risk analysis data.  Use the --help option to get a detailed list of importable model types.  

If the overwrite option is set then the import process will overwrite any existing data that might already be in the CAIRIS database.  This can be useful if you want to cleanly import a new model file.

If the image_dir option is set then CAIRIS will look for somewhere other than the default_image_dir location (specified in cairis.cnf) for any image files associated with the model.  Such image files include pictures for personas and attackers, or rich picture diagrams.
