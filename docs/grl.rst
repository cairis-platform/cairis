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

For details on how to add traceability links, see :doc:`Traceability </traceability>`.

Adding GRL elements to persona characteristics
----------------------------------------------

GRL goals, soft goals, or tasks can be associated with persona characteristics, and their supporting grounds, warrants, or rebuttals.

- To add these GRL elements, open the persona characteristic you want to update and, in the General folder, click on the GRL Elements folder.
- Enter a synopsis for the persona characteristic that expresses the characteristic in intentional terms.

- Select the GRL element type for this synopsis; this can be either a goal, soft goal, or task.


.. figure:: pcGrl.jpg
   :alt: Associating GRL with persona characteristic

- For each appropriate grounds, warrant, and rebuttal reference, click on the reference to open the characteristic reference dialog.


.. figure:: crGrl.jpg
   :alt: Associating GRL with characteristic reference

- Enter a synopsis for the ground, warrrant, or rebuttal reference tat expresses the reference in intentional terms.

- Select the GRL element type for this synopsis this can be either a goal or software.

- Given the intentional relationship between this GRL element and the GRL goal, softgoal, or task associated with the persona characteristic, indicate whether this element is a means for achieving the characteristic element's end by selecting *Means* in the Means/End combo box.  Alternatively, if the characteristic's element is a means for achieving this GRL elements end then select *End*.

- Use the Contribution box to indicate how much this reference contributes to achieving its means or end.  Possible values are Make, SomePositive, Help, Hurt, SomeNegative, Break.

- Click on the Save button to close the dialog.

- Click on the Update button the persona characteristics form to update the persona characteristic.

