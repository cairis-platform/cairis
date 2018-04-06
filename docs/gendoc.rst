Generating Documentation
========================

The current contents of the CAIRIS database can be generated as a
requirements specification by selecting the System/Documentation
menu.  After choosing to generate requirements or persona documentation, and the output type (PDF or RTF), clicking on Generate will generate and download the specification document.

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

If you want to create a custom specification then you may wish to generate an RTF specification, and generate the graphical models directly from CAIRIS.
Models in CAIRIS are rendered as SVG, and you can extract these directly from the web app by installing the `SVG Crowbar <http://nytimes.github.io/svg-crowbar>`_ bookmarklet in your browser.
The resulting SVG file can then be tweaked using an SVG editor like `Inkscape <https://inkscape.org>`_ , exported to the graphics format of your choice, and then added to your specification document.
