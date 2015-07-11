---
layout: default
title: Running CAIRIS
---

To start CAIRIS, you can open a terminal window and go to the directory containing the source code of CAIRIS.  This is usually `$CAIRIS_DIR/cairis`.

        $ python cairis.py

This main CAIRIS window is split in 2 halves.  The bottom half is the taken up the requirements editor.  The top half of the screen is taken up by the menu and tool-bar buttons.

![fig:initStartup]({{ site.baseurl }}/assets/CAIRIS_new.jpg)
*An empty CAIRIS project*

All the information entered into CAIRIS is stored in a single MySQL database, but all or part of a complete CAIRIS model can be imported and exported in XML.  CAIRIS comes with a sample model (`completeExample.xml`) which can be found in `$CAIRIS_DIR/examples`.  This can be imported by clicking on the File/Import/Model menu, and selecting the model file to be imported.

Model files can also be imported from the command line by using the `cimport.py` script in the source code directory.  

        $ python cimport.py --type all --overwrite 1 ../examples/completeExample.xml

Although a little out of date, the [user manual]({{site.baseurl}}/assets/manual.pdf) describes how CAIRIS can be used to model and analyse security, usability, and requirements elements.
