Generating Documentation
========================

The current contents of the CAIRIS database can be generated as a
requirements specification by selecting the System/Documentation
menu.  After choosing the type of specification, the output file name, and the output type (PDF, RTF, ODT), clicking on Generate will generate and download the specification document.

.. figure:: GenerateDocumentationForm.jpg
   :alt: Generate Documentation form


CAIRIS currently supports the generation of 3 types of specification:

================================= =====================================================================================================================================================================================================================
Template                          Description
================================= =====================================================================================================================================================================================================================
Requirements                      A requirements specification that conform to the `Volere Requirements Specification Template <http://www.volere.co.uk/template.htm>`_
Personas                          A specification document for personas.
Data Protection Impact Assessment A DPIA specification that conforms with the `ICO Data Protection Impact Assessments draft template <https://ico.org.uk/media/about-the-ico/consultations/2258461/dpia-template-v04-post-comms-review-20180308.pdf>`_.
================================= =====================================================================================================================================================================================================================

Models in CAIRIS are rendered as SVG, and it can be useful to edit these models for improved readability.  You can extract these models directly from the web app by installing the `SVG Crowbar <http://nytimes.github.io/svg-crowbar>`_ bookmarklet in your browser.
The resulting SVG file can then be tweaked using an SVG editor like `Inkscape <https://inkscape.org>`_ , exported to the graphics format of your choice, and then added to your specification document.

If you plan to customise the specification, you may find it useful to generate ODT documentation; ODT files can be opened not only in Libre Office but also Word.  However, because certain models nodes (e.g. role and attacker figures) are xlinked to the CAIRIS server, you find empty spaces in some models where these figures should be.  In this case, you may wish to render the offending models in CAIRIS, and use SVG Crowbar as described about to re-generate the figure.
