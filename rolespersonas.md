---
layout: default
title: Roles and Personas
---


## Roles ##

Roles represent the abstract classes representing human agents; these also encapsulate behaviours and responsibilities.  CAIRIS supports 2 types of role: stakeholder and attacker.  Stakeholder roles represent human agents the system needs to be directly, or indirectly designed for.  Attackers are human agents the system should not be designed for.

### Adding, updating, and deleting a role ###

![fig:RoleDialog]({{ site.baseurl }}/images/RoleDialog.png "Role Dialog")

* Click on the Role toolbar button to open the Roles dialogue box, and click on the Add button to open the Role dialogue box.

* Enter a role name and description, and select the role type.

* Click on the Update button to Add the new role to the CAIRIS database.

* As responses and countermeasures are assigned to roles, the Role dialogue is automatically updated to reflect these new dependencies.  These dependencies cannot be modified from the Role dialogue.

* Existing roles can be modified by double-clicking on the role in the Roles dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a role, select the role to delete in the Roles dialogue box, and select the Delete button.  If any artefacts are dependent on this role then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the role dependencies and the role itself, or No to cancel the deletion.

### Responsibility modelling ###

Responsibility models can be viewed by clicking on the View Responsibility Model toolbar button and selecting the environment to view the environment for.

![fig:ResponsibilityModel]({{ site.baseurl }}/images/ResponsibilityModel.png "Responsibility Model")

By changing the environment name in the environment combo box, the responsibility model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artefact can be viewed.  

## Personas ##

Personas are specifications of archetypical users that the system needs to directly or indirectly cater for.
The system needs to be specified for Primary Personas, but Secondary Personas cannot be ignored as their thoughts or concerns provide insight into potential usability problems.

### Adding, updating, or deleting a persona ###

![fig:PersonaDialog]({{ site.baseurl }}/images/PersonaDialog.png "Persona Dialog")

* Click on the Persona toolbar button to open the Personas dialogue box, and click on the Add button to open the Persona dialogue box.

* Enter a persona name and select the persona type.

* If the persona is not derived from empirical data, then select the Assumption Persona check-box.  Ticking this box has the effect of pre-fixing the persona name with the &lt;&lt; assumption &gt;&gt; stereotype in any models where the persona is present.

* Click on the Activities tab and enter the activities carried out by the personas.

* Click on the Attitudes tab and enter the attitudes held by the persona, with respect to the problem domain the system will be situated in.

* Click on the Aptitudes tab and enter the persona's aptitudes, with respect to the problem domain the system will be situated in.

* Click on the Motivations tab and enter the persona's personal motivations.

* Click on the Skills tab and enter the persona's skill-set, with respect to the problem domain the system will be situated in.

* If you have decided to personalise the persona with a picture, this can be added by right-clicking on photo box next to the persona properties notebook, to bring up the Load Image option from the speed menu, and selecting Load Image.  Please note that the image itself is NOT imported into the database, only the file path to the picture.

* If you have decided to personalise your persona with a picture, this can be added by right-clicking on the photo

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the persona in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, click on the Summary tab.  Select the Direct/Indirect Persona check-box if the persona is a direct stakeholder with respect to the system being defined, and add roles fulfilled by the persona in the Roles list-box.  These roles can be added or deleted by right-clicking on the roles box to bring up the speed menu.

* Click on the Narrative tab and enter a narrative describing the persona's relationship with the problem domain or prospective system within the environment, and any environment specific concerns he or she might have.

* Click on the Create button to add the new persona.

* Existing personas can be modified by double-clicking on the persona in the Personas dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a persona, select the persona to delete in the Personas dialogue box, and select the Delete button.  If any artefacts are dependent on this persona then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the persona dependencies and the persona itself, or No to cancel the deletion.

### Recording persona assumptions ###

![fig:APModel]({{ site.baseurl }}/images/APModel.png "Assumption Persona model")

* From the Options/External Document directory, click on the Add button and add information about the source of any assumptions external to CAIRIS.  An example of such an *External Document* might be an interview transcript.  Alternatively, if assumptions are purely based on your own thoughts and feelings then an External Document can be created to make this explicit.

* Open up the Persona dialogue for the persona you want to add a characteristic to, and right click in the behavioural variable folder (e.g. Activities) you wish to add a Characteristic to.

* From the Persona Characteristics dialogue box, click on Add to add a new characteristic.

* From the General folder, add a description of the characteristic and a *Model Qualifier*; this word describes your confidence in the validity of the characteristic.  Possible qualifiers might include *always*, *usually*, or *perhaps*.

* Click on the Grounds tab to open the list of Grounds for this characteristic.  The grounds are evidence which supports the validity of the characteristic.  Right-click in the Reference box and select Add to add a Document Reference.  Select the concept type for this evidence and the name of a pre-existing concept or document reference on this grounds.  If one doesn't already exist, then select any artefact and, from the Reference combo box, select [New artefact reference] (for a document reference) or [New concept reference] (for a reference to an existing model object.  In both cases, a dialogue box will appear allowing you to enter a short description of the grounds proposition, together with more detailed rationale.  Clicking on Ok will add the new document or concept reference, and add this to the grounds list.

* Click on the Warrant tab to open the list of Warrants for this characteristic.  The warrants are inference rules which links the grounds to the characteristic.  The procedure for adding warrants is identical to the process for adding grounds.  After adding a warrant, however, a Backing entry for the warrant is automatically added.

* If you wish to add a Rebuttal -- a counterargument for the characteristic -- then click on the Rebuttals tab and add a rebuttal using the same procedure for Grounds and Warrants.

* Click on the Create button to create the new characteristic.

* Existing characteristics can be modified by double-clicking on the characteristics in the Persona Characteristic dialogue box, making the necessary changes, and clicking on the Edit button.
