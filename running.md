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

        $ python cimport.py --type all --overwrite 1 --image_dir ../examples ../examples/completeExample.xml


The type `all` refers to a complete model file.  Individual parts of models can also be imported.  These might include models of individual personas, goal models, or risk analysis data.  Use the --help option to get a detailed list of importable model types.  

If the overwrite option is set then the import process will overwrite any existing data that might already be in the CAIRIS database.  This can be useful if you want to cleanly import a new model file.

If the image_dir option is set then CAIRIS will look for somewhere other than the default_image_dir location (specified in cairis.cnf) for any image files associated with the model.  Such image files include pictures for personas and attackers, or rich picture diagrams.
