---
layout: default
title: Getting started
---

{% include toc.html %}

# Installing CAIRIS

In theory, CAIRIS can be installed on any platform that its open-source dependencies are available for.  In practice, CAIRIS is developed using Linux, and is most stable when running on [Ubuntu](http://www.ubuntu.com) or [Debian](https://www.debian.org) Linux.

* Install the required applications and dependencies:

{% highlight bash %}
$ sudo apt-get install python-wxglade python-glade2 python-wxgtk3.0 python-dev build-essential mysql-server mysql-client graphviz docbook dblatex python-pip python-numpy git libmysqlclient-dev --no-install-recommends texlive-latex-extra docbook-utils
{% endhighlight %}

* Install CAIRIS:

{% highlight bash %}
$ sudo pip install cairis
{% endhighlight %}

* Run the CAIRIS database initialisation script.  When you run this script, you should get the below form.

{% highlight bash %}
$ configure_cairis_db.py
{% endhighlight %}

![fig:configure_cairis_db]({{ site.baseurl }}/images/configure_cairis_db.jpg)

Assuming you didn't customise the installation location of CAIRIS when running `pip`, you can usually accept all of these defaults, except for the name and location of the CAIRIS configuration file.  When you select `Ok`, the script will create a new CAIRIS database, and accompanying CAIRIS configuration file; this file will ensure that CAIRIS knows what database it needs to refer to when you start up the tool.

* Ensure the CAIRIS_CFG environment variable to points to your CAIRIS configuration file, and is persistent, i.e.

{% highlight bash %}
echo export CAIRIS_CFG=/home/cairisuser/cairis.cnf >> .bashrc
{% endhighlight %}

# Starting CAIRIS

To start CAIRIS, you can open a terminal window and run to `cairis_gui.py`.

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
