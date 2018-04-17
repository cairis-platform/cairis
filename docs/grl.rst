Generating Goal-oriented Requirements Language models
=====================================================

`The Goal-oriented Requirements Language (GRL) <https://en.wikipedia.org/wiki/Goal-oriented_Requirements_Language>`_ is a language for modelling intentional relationships between goals.  Although CAIRIS does not support the visualisation of GRL models, it is possible to generate GRL models from CAIRIS that are compatible with `jUCMNav <http://jucmnav.softwareengineering.ca/foswiki/ProjetSEG>`_.  There are several reasons why generating GRL models from a CAIRIS model might be useful:

* Expressing persona data using GRL can help elicit intentional relationships that support or refute aspects of a persona’s behaviour.
* Agent-oriented goal modelling language like GRL are popular in Requirements Engineering, making a GRL model a potential vehicle for interchange between RE methods, techniques, and tools.
* GRL models provide an alternative way of contextualising personas, tasks, and use cases. This might make it possible to identify new requirements, threats, or vulnerabilities that results from cross-cutting concepts.

`This paper <https://www.researchgate.net/publication/221215412_Bridging_User-Centered_Design_and_Requirements_Engineering_with_GRL_and_Persona_Cases>`_ explains the alignment between GRL and CAIRIS concepts, which are summarised in the figure below:
 
.. figure:: pcToGrlMetaModel.jpg
   :alt: Conceptual model of CAIRIS and GRL elements

Pre-requisite activities
------------------------

To generate a GRL model, you need to create the CAIRIS model elements synonymous with the GRL model elements.  Typically, these will be persona characteristics and use cases.  You will also need to create a traceability association between a task that the personas of interest participate in, and the use cases.

For details on how to print asset models as SVG files, see :doc:`Traceability </traceability>`.

