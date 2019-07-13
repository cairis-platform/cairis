Personas
========

Personas are specifications of archetypical users that the system needs
to directly or indirectly cater for. The system needs to be specified
for Primary Personas, but Secondary Personas cannot be ignored as their
thoughts or concerns provide insight into potential usability problems.

Adding, updating, or deleting a persona
---------------------------------------

.. figure:: PersonaForm.jpg
   :alt: Persona form


-  Select the UX/Personas menu to open the table of personas,
   and click on the Add button to open the new Persona form.

-  Enter a persona name and select the persona type.

-  If you have decided to personalise the persona with a picture, this
   can be added by clicking on avatar silhouette next to the persona
   description, and selecting a image to represent the persona. 

-  Click on the Activities tab and enter the activities carried out by
   the personas.

-  Click on the Attitudes tab and enter the attitudes held by the
   persona, with respect to the problem domain the system will be
   situated in.

-  Click on the Aptitudes tab and enter the persona's aptitudes, with
   respect to the problem domain the system will be situated in.

-  Click on the Motivations tab and enter the persona's personal
   motivations.

-  Click on the Skills tab and enter the persona's skill-set, with
   respect to the problem domain the system will be situated in.

-  Click on the Contextual Trust tab, and enter information about aspects of this
   persona with an impact on contextual trust warranting properties.

-  Click on the Contextual Trust tab, and enter information about aspects of this
   persona with an impact on intrinsic trust warranting properties.

-  If you have decided to personalise the persona with a picture, this
   can be added by clicking on avatar box next to the persona
   properties notebook, to select an image to associated with the persona.

-  Click on the Environment card, and click on the Add button to situate the persona in an environment.
   Selecting an environment from the modal will open up a new folder for
   information about persona roles, and an environment specific narrative.

-  After ensuring the environment is selected in the environment window,
   click on the Roles tab. Select the Direct User 
   check-box if the persona is a direct stakeholder with respect to the
   system being defined, and add roles fulfilled by the persona in the
   Roles list-box. These roles can be added by clicking on the add button in the role table,
   or deleted by clicking on the button next to the role to be removed.

-  Click on the Narrative tab and enter a narrative describing the
   persona's relationship with the problem domain or prospective system
   within the environment, and any environment specific concerns he or
   she might have.

-  Click on the Create button to add the new persona.

-  Existing personas can be modified by clicking on the persona
   in the UX/Personas table, making the necessary changes, and
   clicking on the Update button.

-  To delete a persona, click on the delete button next to persona to be removed
   in the personas table. If any artifacts are
   dependent on this persona then a dialog box stating these
   dependencies are displayed. The user has the option of selecting Yes
   to remove the persona dependencies and the persona itself, or No to
   cancel the deletion.

Assured personas with persona characteristics
---------------------------------------------

Overview
~~~~~~~~

Persona specifications are necessary, but not sufficient for indicating the validity of a persona; you should also describe the basis for each part of the persona specification too.
Personas might be created on the basis of some user research.  The results of this user research might be coded as a collection of factoids -- statements about the data that might be true or false -- before the user research makes sense of this data using an activity like affinity diagramming.  Clusters of factoids resulting from this exercise form the basis of each aspect of the persona.  Normally, however, this data and the results of the analysis are discarded once the persona is created, which means there is no rationale to justify the persona should questions of clarification of legitimacy be asked about them.

To overcome this problem, CAIRIS supports the creation of *persona characteristics*.  These are argumentation models where the *argument* is an individual persona characteristic.   

Justifying each characteristic is a one or more *grounds* that provide evidence to support the persona's validity, *warrants* that act as inference rules connecting the grounds to the characteristic, and *rebuttals* that act as counterarguments for the characteristic.  A *model qualifier* is also used to describe the confidence in the validity of the persona characteristic.

This approach for structuring persona characteristic elements is based on Toulmin's model of argumentation [#] and can be visualised in CAIRIS using the persona model, accessible from the Models/Persona menu.  As shown in the persona model below, a link can be seen between grounds element and their *backing*, the originating source of the grounds. 

.. [#] Toulmin, S. The uses of argument, updated ed. Cambridge University Press, 2003.

.. figure:: APModelKey.jpg
   :alt: Persona model

Creating persona characteristics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Select the UX/External Documents menu, and click on the Add button
   to add information about the source of any assumptions external to
   CAIRIS. An example of such an *External Document* might be an
   interview transcript. Alternatively, if assumptions are purely based
   on your own thoughts and feelings then an External Document can be
   created to make this explicit.  External documents are shown as backing elements in persona models.

-  Select the UX/Document References menu, and click on the Add button.
   Enter a name that summarises the *factoid* that acts as evidence for the persona characteristic.
   Select the external document from the Document combobox box to indicate the document that the factoid is taken from, and enter details of the person who elicited the assumption in the Contributor text box.  Finally, in the Excerpt box, enter the extract of text from the external document from which the factoid is based.

-  Select the UX/Persona Characteristics menu, and click on the Add button.

.. figure:: PersonaCharacteristicForm.jpg
   :alt: Persona characteristic form

-  From the Characteristic folder, enter a definition that summarises the characteristic, and select the Persona and behavioural variable that this characteristic will be associated with.  Possible Enter a *Model Qualifier*; this word describes your confidence in the validity of the characteristic. Possible qualifiers might include *always*, *usually*, or *perhaps*.

-  In the Grounds table, click on the Add button to add a grounds for the characteristic.
   Click on the Add button to add a new document reference that acts as grounds. When a document reference is selected, a read-only description of this document reference will also be shown. Clicking Ok will add the new document reference to the grounds list.

-  Repeat the above procedure for *Warrants* as appropriate.

-  If you wish to add a Rebuttal -- a counterargument for the
   characteristic -- then click on the Rebuttals tab and add a rebuttal
   using the same procedure for Grounds and Warrants.

-  Click on the Create button to create the new characteristic.

-  Existing characteristics can be modified by double clicking on the
   characteristics in the persona characteristics table, making the
   necessary changes, and clicking on the Update button.

Automating persona characteristic creation
------------------------------------------

In the ideal world, personas will be created by dedicated teams of research collecting empirical data, working collectively in one place to affinity diagram factoids, and persona characteristics that structure them.  In reality, team members might be working individually, remotely, and using open source intelligence or online sources of data.  To provide some automation for this activity, we have created some *helper* extensions and CAIRIS features.

Persona Helper
~~~~~~~~~~~~~~

The `Persona Helper <https://chrome.google.com/webstore/detail/persona-helper/mhojpjjecjmdbbooonpglohcedhnjkho>`_ Chrome Extension can be used to automatically create document references from highlighted text on a web page open in Chrome.  This might be useful when eliciting factoids from website.

Trello Import / Export
~~~~~~~~~~~~~~~~~~~~~~~~

CAIRIS also supports the ability to export document references to Trello for online affinity diagramming, and import affinity diagrams from Trello into CAIRIS as argumentation models.

Both the Persona Helper and the Trello import/export facilities are illustrated in this `video <https://vimeo.com/208162116>`_.
