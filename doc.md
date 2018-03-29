---
layout: default
title: Documentation
---
{% include toc.html %}

# Creating a new project #

The first stage of the design process involves establishing the scope of subsequent analysis.  CAIRIS supports this exercise by using the Project Settings notebook.

## Update project settings ##

![fig:projectSettings]({{ site.baseurl }}/images/projectSettings.png "Project Settings notebook")

* Click on the Project Settings button to open the Project Settings notebook.  By default, the notebook will open in the Background page.  Enter the project name and background on this page.

* Click on the Goals tab and enter the high-level goals that the system being specified needs to satisfy.

* Click on the Scope tab and enter the scope of the system being specified.

* If a rich picture or context diagram has been agreed, click on the Rich Picture tab and, by right-clicking on the page to bring up the Load Image option from the speed menu, select a rich picture to import.  Please note that the image itself is NOT imported into the database, only the file path to the picture.

* Names or terms that the readership of the specification may be unfamiliar with can be added to the project on an on-going basis.  To add a term, click on the Naming Conventions tab, right click on the name page, and select Add from the speed menu.  This opens a window which allows a name and a definition to be added to the naming convention list.  To modify an existing entry, double-click on the try and make the required modifications.  Entries can also be deleted from the right-click speed menu.

* Clicking on the Contributors tab opens the Contributors page.  To add a contributor, right click on the page and select Add from the speed menu to open the Add Contributor dialogue box.  Contributors can be either a participant, facilitator, or scribe; these reflect the roles that people take in participatory workshops.

# Environments #

An environment might represent a system operating at a particular time of day, or in a particular physical location.  Environments encapsulate visible phenomena such as assets, tasks, personas, and attackers, as well as invisible phenomena, such as goals, vulnerabilities, and threats.  Environments may be identified at any time, although these may not become apparent until carrying out a contextual inquiry and observing how potential users reason about their context of use.

## Adding a new environment ##

![fig:EnvironmentDialog]({{ site.baseurl }}/images/EnvironmentDialog.png "Environment Dialog")

* Click on the Environment toolbar button to open the Environments dialogue box, and click on the Add button to open the Environment dialogue box.

* Enter the name of the environment, a short code, and a description.  The short-code is used to prefix requirement ids associated with an environment.

* If this environment is to be a composite environment, i.e. encompass artefacts of other environments, then right click on the environment list, select Add from the speed menu, and select the environment/s to add.

* It is possible artefact may appear in multiple environments within a composite environment.  It is, therefore, necessary to set duplication properties for composite environments.  If the maximise radio button is selected, then the maximal values associated with that artefact will be adopted.  This may be the highest likelihood value for a threat or the highest security property values for an asset. If the override radio button is selected, then CAIRIS will ensure that the artefact properties are used for the overriding environment.

## On-the-fly environment creation ##

![fig:NewEnvironmentDialog]({{ site.baseurl }}/images/NewEnvironmentDialog.png "New Environment Dialog")

Most artefacts in CAIRIS are situated in one or more environments.  When creating or updating an artefact, it is usually possible to create a new environment on the fly by right-clicking on the environment list box in the artefact dialogue and selecting the New button.  This opens the New Environment dialogue box.  In this dialogue, an environment name, shortcode and description can be entered.  When the create button is selected, a new environment is added to the CAIRIS database and added to the environment list for the artefact.

## Environmental attribute inheritence ##

An artefact may be situated in one or more environments, but the differences between these environments may be slight.  To reflect this, it is possible for an artefact to inherit properties from another environment.  To do this, right-click on the artefact's environment list box and select the Inherit Environment option.  When prompted, select the environment to inherit from, followed by the environment to situated the artefact in.  In most cases, the properties of the inherited environment will be duplicated in this newly situated environment.  In the case of goals and obstacles, only the immediate refinement associations are retained when inheriting properties from an environment.

# Assets #

Assets are tangible objects of value to stakeholders.  By defining an asset in CAIRIS, we implicitly state that this needs to be secured in light of risks which subsequently get defined.

Assets are situated in one or more environments.  Security properties are associated with each asset for every environment it can be found in.  These security properties are Confidentiality, Integrity, Availability, and Accountability.  Each of these properties is associated with the value of None, Low, Medium, or High.  The meaning of each of these values can be defined in CAIRIS from the Asset Values dialogue; this is available via the Options/Asset values menu.

## Adding, updating, and deleting an asset ##

![fig:AssetDialog]({{ site.baseurl }}/images/AssetDialog.png "Asset Dialog")

* Click on the Asset toolbar button to open the Assets dialogue box, and click on the Add button to open the Asset dialogue box.

* Enter the name of the environment, a shortcode, description, and significance.  The short-code is used to prefix requirement ids associated with an environment.

* If this asset is deemed critical, click on the Criticality tab, and click on the Critical Asset check-box.  A rationale for declaring this asset critical should also be added.  By declaring an asset critical, any risk which either threatens or exploits this asset will be maximised until the mitigations render the likelihood of the threat or the severity of the vulnerability inert.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the asset in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, add the security properties to this asset for this environment.  Security properties are added by selecting the Properties tab, right-clicking on the properties list and selecting Add to open the Add Security Properties window.  From this window, a security property and its value can be added.

* Click on the Create button to add the new asset.

* Existing assets can be modified by double-clicking on the asset in the Assets dialogue box, making the necessary changes, and clicking on the Update button.

* To delete an asset, select the asset to delete in the Assets dialogue box, and select the Delete button.  If any artefacts are dependent on this asset then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the asset dependencies and the asset itself, or No to cancel the deletion.


## Asset modelling ##

Understanding how assets can be associated with each other is a useful means of identifying where the weak links in a prospective architecture might be.  CAIRIS supports the association of assets, inconsistency checking between associated assets, and visualisation of asset models.

The CAIRIS asset model is based on UML class models.  Asset models can be viewed for each defined environment.  As well as explicitly defined asset associations, asset models will also contain associations implicitly defined.  For example, if a task has been defined, and this task concerns within an environment contain one or more assets, then the participating persona will be displayed as an actor, and an association between this actor and the asset will be displayed.  Additionally, if concern associations have been defined between goals and assets and/or associations then zooming into the model will display these concerns; the concerns are displayed as blue comment elements.

![fig:AddAssetAssociation]({{ site.baseurl }}/images/AddAssetAssociation.png "Add Asset Association Dialog")

### Adding an asset association ###

* If creating or updating an asset, an association between that asset and another asset can be made by clicking on the Associations tab in the Asset Dialog and, from the right-click speed menu, selecting Add to open the Add Asset Dialog.

* From the Add Asset Dialog, set the adornments for the head and tail end of the association.  Possible adornment options are Inheritance, Association, Aggregation, and Composition; the semantics for these adornments are based on UML.

* Set the multiplicity (nry) for the head and tail ends of the association.  Possible multiplicity options are `1`, `*`, and `1..*`.

* Optional role names can also be set at the head or tail end of the association.

* Select the Create (or Edit if modifying an existing association) will add the association to the Asset Dialog.  The association will not be added to the database until the asset itself is created or modified.

* Asset associations can also be added by selecting the Asset Associations tool-bar button.  Clicking this button opens the Asset Associations dialogue, where new associations can be created or existing associations can be modified or removed.  The dialogue for modifying associations is identical to the Asset Association dialogue, with the addition of a combo box for selecting the environment to situate the association in.

![fig:AssetInconsistency]({{ site.baseurl }}/images/AssetInconsistency.png "Asset Inconsistency warning")

* If an asset is associated with an asset with one or more security properties of a lower value, then an Asset Inconsistency dialogue is displayed, warning about the details of the inconsistency.


### Viewing Asset models ###

Asset models can be viewed by clicking on the Asset Model toolbar button and selecting the environment to view the environment for.

![fig:AssetModel]({{ site.baseurl }}/images/AssetModel.png "Asset Model")

By changing the environment name in the environment combo box, the asset model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artefact can be viewed.

# Roles & Personas #

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

* From the General folder, add a description of the characters and a *Model Qualifier*; this word describes your confidence in the validity of the characteristic.  Possible qualifiers might include *always*, *usually*, or *perhaps*.

* Click on the Grounds tab to open the list of Grounds for this characteristic.  The grounds are evidence which supports the validity of the characteristic.  Right-click in the Reference box and select Add to add a Document Reference.  Select the concept type for this evidence and the name of a pre-existing concept or document reference on this grounds.  If one doesn't already exist, then select any artefact and, from the Reference combo box, select [New artefact reference] (for a document reference) or [New concept reference] (for a reference to an existing model object.  In both cases, a dialogue box will appear allowing you to enter a short description of the grounds proposition, together with more detailed rationale.  Clicking on Ok will add the new document or concept reference, and add this to the grounds list.

* Click on the Warrant tab to open the list of Warrants for this characteristic.  The warrants are inference rules which links the grounds to the characteristic.  The procedure for adding warrants is identical to the process for adding grounds.  After adding a warrant, however, a Backing entry for the warrant is automatically added.

* If you wish to add a Rebuttal -- a counterargument for the characteristic -- then click on the Rebuttals tab and add a rebuttal using the same procedure for Grounds and Warrants.

* Click on the Create button to create the new characteristic.

* Existing characteristics can be modified by double-clicking on the characteristics in the Persona Characteristic dialogue box, making the necessary changes, and clicking on the Edit button.

# Tasks #

Tasks model the work carried out by one or more personas.  This work is described in environment-specific narrative scenarios, which illustrate how the system is used to augment the work activity.

## Adding, updating, or deleting a task ##

![fig:TaskDialog]({{ site.baseurl }}/images/TaskDialog.png "Task Dialog")

* Click on the Task toolbar button to open the Tasks dialogue box, and click on the Add button to open the Task dialogue box.

* Enter a task name, and the objective of carrying out the task.

* If the task is not derived from empirical data, then select the Assumption Task check-box.  Ticking this box has the effect of pre-fixing the task name with an &lt;&lt; assumption &gt;&gt; stereotype in any models where the task is present.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the persona in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, click on the Summary tab.  In the Summary page, enter any dependencies needing to hold before this task can take place.  

![fig:AddTaskPersona]({{ site.baseurl }}/images/AddTaskPersona.png "Add Task Persona Dialog")

* Right-click on the persona list box and select Add from the speed menu to associate a persona with this task.  In the Add Task Persona dialog box, select the person, the task duration (seconds, minutes, hours or longer), frequency (hourly or more, daily-weekly, monthly or less),demands (none, low, medium, high), and goal conflict (none, low, medium, high). The values for low, medium, and high should be agreed with participants beforehand.  

* If any aspect of the task concerns one or more assets, then these can be added to the concern list.  Adding an asset concern causes a concerned comment to be associated with the asset in the asset model.  If the task concerns an association between assets, the association can be added by clicking on the Concern Association tab and adding the source and target assets and association multiplicity to the concern association list.  In the asset model, this association is displayed and a concerned comment is associated with each asset in the association.

* Right-click on the Narrative tab and enter the task scenario in the text box.  This narrative should describe how the persona (or personas) carry out the task to achieve the pre-defined objective.

* Click on the Create button to add the new task.

* Existing tasks can be modified by double-clicking on the task in the Tasks dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a task, select the task to delete in the Tasks dialogue box, and select the Delete button.  If any artefacts are dependent on this task then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the task dependencies and the task itself, or No to cancel the deletion.

## Task traceability ##

![fig:TraceabilityEditor]({{ site.baseurl }}/images/TraceabilityEditor.png "Traceability Editor")

Tasks can be manually traced to certain artefacts via the Tasks dialogue.  A task may contribute to an asset or a vulnerability, or be supported by the requirement.  To add a traceability link, right click on the task name, and select Supported By or Contributes to.  This opens the Traceability Editor.  From this editor, select the object on the right-hand side of the editor to trace to and click the Add button to add this link.

Manual traceability links can be removed by selecting the View/Traceability menu option, to open the Traceability Relations dialogue.  In this dialogue box, manual traceability relations be removed from specific environments.

## Visualising tasks ##

Task models can be viewed by clicking on the Task Model toolbar button, and selecting the environment to view the environment for.

![fig:TaskModel]({{ site.baseurl }}/images/TaskModel.png "Task Model")

By changing the environment name in the environment combo box, the task model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artefact can be viewed.

# Domain Properties #

Domain Properties are descriptive properties about the statement world.  Domain Properties may be either hypothesis or invariants.

## Adding, updating, and deleting a domain property ##

![fig:DomainPropertyDialog]({{ site.baseurl }}/images/DomainPropertyDialog.png "Domain Property Dialog")

* Click on the Domain Properties toolbar button to open the Domain Properties dialogue box, and click on the Add button to open the Domain Property dialogue box.

* Enter a domain property name, description, and select the type of domain property from the type combo box.

* Click on the Create button to add the new domain property.

* Existing domain properties can be modified by double-clicking on the domain property in the Domain Properties dialogue box, making the necessary changes, and clicking on the Update button.

# Goals, Requirements, and Obstacles #

In CAIRIS, a requirements specification is analogous to a safety case.  In a safety case, a system is only considered safe if its safety goals have been satisfied.  In a similar manner, requirements are leaf nodes in a goal tree and satisfying stakeholder needs is only possible if the high-level goals -- stipulated by stakeholders -- can be satisfied.

We define goals as prescriptive statements of system intent that are achievable by one or more agents.  Goals can be refined to requirements, which are achievable by the only agent. Goals and requirements may also be operationalised as tasks.  Alternatively, we may decide to specify tasks and ask what goals or requirements need to hold in order that a given task can be completed successfully.

To satisfy a goal, one or more sub-goals may need to be satisfied; satisfaction may require satisfying a conjunction of sub-goals, i.e. several AND goals, or a disjunction of sub-goals, i.e. several OR goals.

Goals or requirements may be obstructed by obstacles, which are conditions representing undesired behaviour; these prevent an associated goal from being achieved.  By progressively refining obstacles, we can obtain the origin of some undesired behaviour; this may be reflected as a vulnerability or a threat, and contribute to risk analysis.

## Adding, updating, and deleting a goal ##

![fig:GoalsDialog]({{ site.baseurl }}/images/GoalsDialog.png "Goals Dialog")

* Click on the Goal toolbar button to open the Goals dialogue box. As [fig:GoalsDialog] illustrates, next to goal name is the current *status* of the goal.  If a goal is defined as OK, then this goal is refined by a requirement, or by one or more goals.  Goals with the status *to refine* have yet to be refined or operationalised.  Goals with the status *Check* have been refined by one or more obstacle, and these should be examined to find a root threat or vulnerability.

![fig:GoalDialog]({{ site.baseurl }}/images/GoalDialog.png "Goal Dialog")

* Click on the Add button to open the Goal dialogue box, and enter the name of the goal.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the goal in.  This will add the new environment to the environment list.

* In the Definition page, enter the goal definition, and select the goal category and priority.  Possible goal categories are: Achieve, Maintain, Avoid, Improve, Increase, Maximise, and Minimise.  Possible priority values are Low, Medium, and High.

* Click on the Fit Criterion tab, and enter the criteria which must hold for the goal to be satisfied.

* Click on the Issue tab and enter any issues or comments relating to this goal.

![fig:AddGoalRefinement]({{ site.baseurl }}/images/AddGoalRefinement.png "Add Goal Refinement Dialog")

* If this goal refines a parent goal, click on the Goals tab, right-click on Goal refinement list, and select Add to open the Add Goal Refinement Dialog.  In this dialogue, select the Goal from the Type combo box, and select the Sub-goal, refinement type, and an Alternate value. Possible refinement types are: and, or, conflict, responsible, obstruct, and resolve.  The alternative value (Yes or No) indicates whether or not this goal affords a goal-tree for an alternate possibility for satisfying the parent goal.  It is also possible to enter a rationale for this goal refinement in the refinement text book.  Clicking on Add will add the refinement association to memory, but this will not be committed to the database until the goal is added or updated.

* If this goal refines to sub-goals already specified, Click on the Sub-Goals tab and add a goal refinement association as described in the previous step.  A goal may refine to artefacts other than goals, specifically tasks, requirements, obstacles, and domain properties.

* Goal refinements can also be specified independently of goal creation or modification via the Goal Associations tool-bar button.

* If any aspect of the goal concerns one or more assets, then these can be added by clicking on the Concerns add and adding the asset/s to the concern list.  Adding an asset concern causes a concerned comment to be associated with the asset in the asset model.  If the goal concerns an association between assets, the association can be added by clicking on the Concern Association tab and adding the source and target assets and association multiplicity to the concern association list.  In the asset model, this association is displayed and a concerned comment is associated with each asset in the association.

* Click on the Create button to add the new goal.

* Existing goals can be modified by double-clicking on the goal in the Goals dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a goal, select the goal to delete in the Goals dialogue box, and select the Delete button.  If any artefacts are dependent on this goal then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the goal dependencies and the goal itself, or No to cancel the deletion.

## Goal Modelling ##

Goal models can be viewed by clicking on the Goal Model toolbar button and selecting the environment to view the environment for.

![fig:GoalModel]({{ site.baseurl }}/images/GoalModel.png "Goal Model")

By changing the environment name in the environment combo box, the goal model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artefact can be viewed.  

Goal models can also be filtered by a goal.  Applying a filter causes the selected goal to be displayed as the root goal.  Consequently, goals are only displayed if they are direct or indirect leaves of the filtered goal.

Goals can also be refined from the goal model, albeit only for the environment is modified.  To refine a goal, right-click on the goal in the model viewer, and select And-Goal, or Or-Goal based on the refinement desired.  A simplified version of the Add Goal dialogue box is displayed and, when all the necessary information has been added, a new goal will be added to the database, complete with the desired refinement.  Please note, the model view needs to be refreshed to view the goal.  Goals may only be refined to other goals in the model viewer; for anything more elaborate, the usual goal refinement association procedure needs to be followed.


## Adding, updating, and deleting an obstacle ##

![fig:ObstacleDialog]({{ site.baseurl }}/images/ObstacleDialog.png "Obstacle Dialog")

* Click on the Obstacle toolbar button to open the Obstacles dialogue box, and click on the Add button to open the Obstacle dialogue box.

* Enter the name of the obstacle, and right click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the obstacle in.  This will add the new environment to the environment list.

* In the Definition page, enter the obstacle definition, and select the obstacle category.  Possible obstacle categories are: Confidentiality Threat, Integrity Threat, Availability Threat, Accountability Threat, Vulnerability, Duration, Frequency, Demands, and Goal Support.

* Like goals, obstacle refinements can be added via the Goals and Sub-Goals tabs.

* If any aspect of the obstacle concerns one or more assets, then these can be added by clicking on the Concerns add and adding the asset/s to the concern list.  Adding an asset concern causes a concerned comment to be associated with the asset in the asset model.

* Click on the Create button to add the new obstacle.

* Existing obstacles can be modified by double-clicking on the obstacle in the Obstacles dialogue box, making the necessary changes, and clicking on the Update button.

* To delete an obstacle, select the obstacle to delete in the Obstacles dialogue box, and select the Delete button.  If any artefacts are dependent on this obstacle then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the obstacle dependencies and the obstacle itself, or No to cancel the deletion.

## Obstacle Modelling ##

Obstacle models can be viewed by clicking on the Obstacle Model toolbar button and selecting the environment to view the environment for.

![fig:ObstacleModel]({{ site.baseurl }}/images/ObstacleModel.png "Obstacle Model")

In many ways, the obstacle model is very similar to the goal model.  The main differences are goal filtering is not possible, only the obstacle tree is displayed, and obstacles refine obstacles, as opposed to goals.

## Adding, updating, and deleting requirements ##

Requirements are added and edited using the Requirements Editor in the main CAIRIS window.  Each requirement is associated with an asset or an environment.  Requirements associated with assets may specify the asset, constrain the asset, or reference it in some way.  Requirements associated with an environment are considered transient and remain associated with an environment only until appropriate assets are identified.

* To add a requirement, press enter on an existing requirement or click on the Add Requirement toolbar button.  In both cases, a new requirement will appear beneath the row where the cursor is currently set.

* Enter the requirement description, rationale, fit criterion, and originator in the appropriate cells, select the priority (1,2, 3), and the requirement type (Functional, Data, Look and Feel, Usability, Performance, Operational, Maintainability, Portability, Security, Cultural and Political, and Legal).

* When the attributes have been entered, click on the Commit latest changes toolbar button to commit these requirement additions to the database.

* The order of requirements in the editor can be modified by left clicking on the row label and, while holding down the left mouse button, moving the row label to the appropriate position.  When the mouse button is released, the requirement labels are re-ordered accordingly.

* By changing the asset in the Assets combo box, or the Environment in the Environments combo box, the editor will be reloaded with the requirement associated with the selected asset or environment.  Please note, the Commit latest changes toolbar button should be clicked before changing the selected asset or environment, otherwise, any in-situ requirement changes will be lost.

* A requirement can be deleted by moving the cursor to the row to be deleted, and clicking the Delete Requirements toolbar button.  Deleting a requirement also has the effect of re-ordering the requirement labels.

## Requirement history ##

Every time a requirement is modified, a new version of the requirement is created.  To view the requirement history, right click on the requirement to view the Requirement History dialogue.  This dialogue contains the details of each version of the requirement stored in the database.

## Searching requirement text ##

It is possible to search for a requirement with a particular text string, by selecting the Requirement Management/Find menu option, to open the Find Requirement dialogue.  This Find dialogue is very similar to the Find dialogue found in many WYSIWYG applications.  This search function only works for requirements which are currently loaded in the Requirements editor.

## Requirements traceability ##

Normally requirements traceability is synonymous with adding a goal refinement association but, requirements may also contribute to vulnerabilities (as well as tasks), or be supported by assets or misuse cases.  Consequently, requirements can be manually traced to these artefacts in the same manner as tasks.

## Requirement association ##

A requirement associated with an environment can be associated with an asset, or a requirement associated with an asset can be associated with another asset.  To re-associate a requirement, right click on the requirement, select Asset re-association, and select the asset to re-associate the requirement with.

# Security Patterns #

Security Patterns are solution structures, which prescribe a solution to a security problem arising in a context.  Many components and connectors in secure system architectures are instances of security patterns but, in many cases, the reasoning for a given pattern's inclusion is not always clear.  The requirements needed to realise these patterns are also often omitted, making the job of reasoning about the consequences of situating the pattern difficult.  Moreover, security patterns may be described in a context, but not all collaborating assets in a security pattern may be evident in all possible contexts of a system's use.  The following sections describe how CAIRIS treats security patterns and deals with these weaknesses.

Security Patterns in CAIRIS consist of the following elements:

* A description of the context a pattern is relevant for.

* A problem statement motivating the need for the pattern.

* A solution statement describing the intrinsics of the pattern.

* The pattern structure, modelled as associations between collaborating asset classes.

* A set of requirements, which need to be fulfilled in order to realise the pattern.

Before a security pattern can be defined in CAIRIS, template assets -- which represent the collaborating asset classes -- need to be first defined.

Before a security pattern can be situated in CAIRIS environments, the environments themselves need to be first created.

## Create a template asset ##

![fig:TemplateAssetDialog]({{ site.baseurl }}/images/TemplateAssetDialog.png "Template Pattern Dialog")

Template assets can be best described as context-free assets.  When they are created, template assets do not form part of analysis unless they are implicitly introduced.  This 'implicit introduction' occurs when a security pattern is situated.

The Template Patterns dialogue can be opened by selecting the Options/Template Assets menu option.

The process for creating, updating, and deleting a template asset is almost identical to the processes uses for normal assets.  The only difference is the lack of environment-specific properties.  Security properties are only defined once for the asset.  

To situate an asset in an environment, right click on the template asset name in the Template Assets dialogue box, select the Situate option and specify the environments to situate the template asset in.  After a template asset is situated within an environment, these properties should be revised in the assets generated on the basis of these.  This is because the values associated with the template asset properties may not be inline with assumptions held about Low, Medium, and High assets in the specification being developed.


## Create a security pattern ##

![fig:SecurityPatternDialog]({{ site.baseurl }}/images/SecurityPatternDialog.png "Security Pattern Dialog")

* Select the Options/Security Patterns menu option to open the Security Patterns dialogue box, and click on the Add button to open the Security Pattern dialogue box.

* Enter the security pattern name, and, in the Context page, type in a description the security pattern is relevant for.

* Click on the Problem page, and type in a problem description motivating the security pattern.

* Click on the solution page, and type in the intrinsics of how the security pattern solves the pre-defined problem.

* Click on the Structure page, and right-click on the association list control to add associations between template assets; these associations form the collaborative structure for the pattern.  The procedure for entering associations is based on that used for associating assets.

* Click on the Requirements page, and right-click on the requirements list control to add requirements needing to be satisfied to realise the pattern.  The cells in the Add Pattern Requirement dialogue are a subset of those found in the CAIRIS requirements editor.

* Click on the Create button to add the new security pattern.

* Existing security patterns can be modified by double-clicking on the security pattern in the Security Patterns dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a security pattern, select the pattern to delete in the Security Patterns dialogue box, and select the Delete button.

## Situate a security pattern ##

![fig:SituatePatternDialog]({{ site.baseurl }}/images/SituatePatternDialog.png "Situate Pattern Dialog")

* To introduce a security pattern into the working project, open the Security Patterns dialogue box, right-click on the pattern, and select the Situate Pattern option from the speed menu.  This opens the Situate Pattern Dialog box.

* For each collaborating asset, click on the checkboxes that you wish to situate each asset in.  It may be that not all assets in the pattern are relevant for all contexts of use.  Therefore, all the pattern structure is retained in the project, the pattern structure displayed in each environment is based only on the assets situated.  For example, for the Packet Filter Pattern, an end-user context of use may only be concerned with the client workstation asset and the firewall.  A system administrator may be concerned about most of the pattern structure but may be less concerned about interactions with external hosts.

* Click on the Create button to situate the pattern.

Template assets will be instantiated as assets, and situate in the stipulated assets.  Requirements associated with the pattern will be introduced and associated with the stipulated assets in the pattern definition.  These assets will be ordered based on the order of definition in the pattern structure.

# Vulnerabilities #

Vulnerabilities are weaknesses of a system, which are liable to exploitation.

## Create a vulnerability ##

![fig:VulnerabilityDialog]({{ site.baseurl }}/images/VulnerabilityDialog.png "Vulnerability Dialog")

* Click on the Vulnerability toolbar button to open the Vulnerabilities dialogue box.

* Click on the Add button to open the Create Vulnerability dialogue box.

* Enter the vulnerability name and description, and select the vulnerability type from the combo box.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the vulnerability in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, select the vulnerability's severity for this environment, and add exposed assets by right-clicking on the asset box and selecting one or more assets from the selected environment.

* Click on the Create button to add the new vulnerability.

* Existing vulnerabilities can be modified by double-clicking on the vulnerability in the Vulnerabilities dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a vulnerability, select the vulnerability to delete in the Vulnerabilities dialogue box, and select the Delete button.  If any artefacts are dependent on this vulnerability then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the vulnerability dependencies and the vulnerability itself, or No to cancel the deletion.

## Importing a vulnerability ##

![fig:ImportVulnerabilityDialog]({{ site.baseurl }}/images/ImportVulnerabilityDialog.png "Import Vulnerability")

The CAIRIS database is pre-loaded with a database of template vulnerabilities based on the Common Criteria.  To import one of these, select Import from the Vulnerabilities dialogue to open the Import Vulnerability dialogue. When a vulnerability is selected, the Vulnerability dialogue is opened, and pre-populated with information from the template.

![fig:ImportedVulnerabilityDialog]({{ site.baseurl }}/images/ImportedVulnerabilityDialog.png "Imported Vulnerability")

# Attackers #

Attackers launch attacks in the form of threats. Attackers are similar to personas in that fulfil one or more roles and can be personalised with additional information.

Certain capabilities and motivations may be associated with attackers.  CAIRIS is pre-loaded with a selection of these, but these can be modified, or new capabilities and motivations created by selecting the Options/Capabilities or Options/Motivations menu options.

## Adding, updating, and deleting an attacker ##

![fig:AttackerDialog]({{ site.baseurl }}/images/AttackerDialog.png "Attacker Dialog")

* Click on the Attacker toolbar button to open the Attackers dialogue box, and click on the Add button to open the Attacker dialogue box.

* Enter the attacker name, and a description for the attacker.

* If you have decided to personalise the attacker with a picture, this can be added by right-clicking on photo box next to the attacker description, to bring up the Load Image option from the speed menu, and selecting Load Image.  Please note that the image itself is NOT imported into the database, only the file path to the picture.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the attacker in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, right-click on the Roles list, and select Add from the speed menu to associate one or more roles to the attacker.  

* Right-click on the Motive and Capability boxes and select Add to add one or more motive and capability values.  For the capability, a value of Low, Medium, or High also needs to be selected.  

* Click on the Create button to add the new attacker.

* Existing attackers can be modified by double-clicking on the attacker in the Attackers dialogue box, making the necessary changes, and clicking on the Update button.

* To delete an attacker, select the attacker to delete in the Attackers dialogue box, and select the Delete button.  If any artefacts are dependent on this attacker then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the attacker dependencies and the attacker itself, or No to cancel the deletion.

# Threats #

Threats are synonymous with attacks, and can therefore only be defined if an associated attacker has also been defined.  Like vulnerabilities, threats are associated with one or more assets.  However, threats may also target certain security properties as well, in line with security values that an attacker wishes to exploit.

A threat is also of a certain type.  CAIRIS is pre-loaded with a selection of these, but these can be modified, or new threat types created by selecting the Options/Threat Types menu option.

## Adding, updating, and deleting a threat ##

![fig:ThreatDialog]({{ site.baseurl }}/images/ThreatDialog.png "Threat Dialog")

* Click on the Threat toolbar button to open the Threats dialogue box, and click on the Add button to open the Threat dialogue box.

* Enter the threat name, the method is taken by an attacker to release the threat, and select the threat type.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the threat in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, select the threat's likelihood for this environment

* Associate attackers with this threat by right-clicking on the attacker box, selecting Add from the speed menu, and selecting one or more attackers associated with the environment.

* Add threatened assets by right-clicking on the asset box, selecting Add from the speed menu, and selecting one or more assets from the selected environment.

* Add the security properties to this threat by right-clicking on the properties list, and selecting Add from the speed menu to open the Add Security Properties window.  From this window, a security property and its value can be added.

* Click on the Create button to add the new threat.

* Existing threats can be modified by double-clicking on the threat in the Threats dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a threat, select the threat to delete in the Threats dialogue box, and select the Delete button.  If any artefacts are dependent on this attacker then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the threat dependencies and the threat itself, or No to cancel the deletion.

## Importing threats ##

![fig:ImportThreatDialog]({{ site.baseurl }}/images/ImportThreatDialog.png "Import Threat")

The CAIRIS database is pre-loaded with a database of template threats based on the Common Criteria.  To import one of these, select Import from the Threats dialogue to open the Import Threat dialogue. When a threat is selected, the Threat dialogue is opened, and pre-populated with information from the template.

# Risks #

Risks are defined as the detriment arising from an attacker launching an attack, in the form of a threat, exploiting a system weakness, in the form of a vulnerability.
Associated with each risk is a Misuse Case.  A Misuse Case describes how the attacker (or attackers) behind the risk's threat exploits the risk's vulnerability to realise the risk.

The current status of Risk Analysis can be quickly ascertained by viewing the Risk Analysis model.  This displays the current risks, the artefacts contributing to the risk, and the artefacts which potentially mitigate it.  

## Adding, updating, and deleting a risk ##

![fig:RiskDialog]({{ site.baseurl }}/images/RiskDialog.png "Risk Dialog")

* Click on the Risk toolbar button to open the Risks dialogue box, and click on the Add button to open the Risk dialogue box.

* Enter a risk name and select a threat and vulnerability from the respective combo boxes.  A risk is valid only if the threat and vulnerability exist within the same environment (or environments).

* Highlighting the environment name in the environment box displays a qualitative risk rating, and the mitigated and un-mitigated risk score associated with each risk response.  To see how this score is calculated, click on the Show Details button.

* Before a risk can be created, an associated Misuse Case needs to be defined.  To do this, click on the Create Misuse Case button to open the Misuse Case Dialog.

![fig:MisuseCaseDialog]({{ site.baseurl }}/images/MisuseCaseDialog.png "Misuse Case Dialog")

* Most of the fields in the Misuse Case dialogue have already been completed based on the risk analysis carried out up to this point.  Click on the Narrative tab and enter a scenario which describes how the attacker realises the associated risk, i.e. carries out the threat by exploiting the vulnerability.  The scenario was written should be written in line with the attributes and values displayed in the Summary tab.

* Click on the Create button to create the Misuse Case and close the Misuse Case Dialog.  Following this, click Create add the new risk.

* Existing risks can be modified by double-clicking on the risk in the Risks dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a risk, select the risk to delete in the Risks dialogue box, and select the Delete button.  If any artefacts are dependent on this risk then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the risk dependencies and the risk itself, or No to cancel the deletion.

## Risk Analysis model ##

Risk Analysis models can be viewed by clicking on the Risk Analysis Model toolbar button and selecting the environment to view the environment for.

![fig:RiskAnalysisModel]({{ site.baseurl }}/images/RiskAnalysisModel.png "Risk Analysis Model")

By changing the environment name in the environment combo box, the risk analysis model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artefact can be viewed.  

The risk analysis model can also be filtered by artefact type and artefact type.  Filtering by type displays only the artefacts of the filtered type and its directly associated assets.  Filtering by artefact name displays only the filtered artefact, and its directly associated artefacts.

# Risk Responses #

A risk can be treated in several ways.

By choosing to *Accept* a risk, we indicate that we are prepared to accept the consequences of the risk being realised.  Accepting the risk comes with a cost, and responsibility for accepting a risk must fall on one or more roles.

By choosing to *Transfer* a risk, we acknowledge that dealing with a risk is out of scope for this project. It may still, however, have a cost associated with it and, by accepting the risk, the risk must become the responsibility of one or more roles.

By choosing to *Mitigate* a risk, we may either Prevent, Deter, Detect, or React to a risk.  For detective responses, the response must detect the risk before, during, or after the risk's realisation.  For reactive responses, the response must be associated with a countermeasure asset derived from a detective response.

## Adding, updating, and deleting a response ##

![fig:ResponseDialog]({{ site.baseurl }}/images/ResponseDialog.png "Response Dialog")

* Click on the Response toolbar button to open the Responses dialogue box, and click on the Add button.  Select the response to take from the available options presented.

* Select the risk to associate this response with.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the response in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, select the response type.

* When the risk name and response type is selected, the response name is automatically generated.

* If an accept or transfer response was selected, a cost and rationale need to be entered.  For transfer responses, one or more roles also need to be associated with the response.

* If a Detect response is selected, select the Detection Point (Before, Medium, or After).

* If a React response is selected, right click on Detection Mechanism box, select Add from the speed menu and select a detection mechanism asset.

* Click on the Create button to add the new response.

* Existing responses can be modified by double-clicking on the response in the Responses dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a response, select the response to delete in the Responses dialogue box, and select the Delete button.  If any artefacts are dependent on this response then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the response dependencies and the response itself, or No to cancel the deletion.

## Generating goals ##

A goal can be generated from a response by right-clicking on the response name in the Responses dialogue box and selecting Generate Goal from the speed menu.  This causes a goal to be generated in each of the environments the response is situated in.  The goal name corresponds to the name of the response.

# Countermeasures #

After a response goal has been generated, goal modelling continues until one or more countermeasure requirements have been defined and associated with their parent goals.  Following this, a countermeasure can be defined.  Defining a countermeasure also has the effect of satisfying a response goal and resolving any obstacles associated with the underlying risk's threat or vulnerability.

Countermeasures target a risk's threat, vulnerability, or both.  Countermeasures also have a level of effectiveness.  This effectiveness level determines how much the countermeasure reduces the likelihood of the associated threat or severity of the associated vulnerability.

Countermeasures are associated with roles, who may be responsible for developing, maintaining or using the countermeasure.  Consequently, countermeasures are also associated with tasks and, when defining a countermeasure, it is also necessary to indicate how much the countermeasure helps or hinders the properties of associated tasks.

## Adding, updating, and deleting a countermeasure ##

![fig:CountermeasureDialogSecurity]({{ site.baseurl }}/images/CountermeasureDialogSecurity.png "Countermeasure Dialog: Security Page")

![fig:CountermeasureDialogUsability]({{ site.baseurl }}/images/CountermeasureDialogUsability.png "Countermeasure Dialog: Usability Page")

* Click on the Countermeasure toolbar button to open the Countermeasures dialogue box, and click on the Add button to open the Countermeasure dialogue box.

* Enter the countermeasure name and description, and select the countermeasure type.  A countermeasure may be one of the following type: Information, Systems, Software, Hardware, or People.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the countermeasure in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, select the countermeasure cost

* Click on the Security tab to display the security page.  Right-click in the Requirements box and select add from the speed menu to add the requirement (or requirements) this countermeasure refines.  Following this, right click on the Target list and select add to select the countermeasure's target/s, together with the countermeasure's effectiveness.  Finally, add the security properties fostered by this countermeasure via the security properties box at the bottom of the page.

* Click on the Usability tab to display the usability page.  Right click on the Roles box, and select add from the speed menu to add the roles associated with this countermeasure. Any tasks associated with these roles are automatically populated in the Task box at the bottom of the page, together with the person/s carrying out the task.  If the countermeasure helps or hinders a task, double-click on the task and modify the task's attributes accordingly.

* Click on the Create button to add the new countermeasure.

* Existing countermeasures can be modified by double-clicking on the countermeasure in the Countermeasures dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a countermeasure, select the countermeasure to delete in the Countermeasures dialogue box, and select the Delete button.  If any artefacts are dependent on this countermeasure then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the countermeasure dependencies and the countermeasure itself, or No to cancel the deletion.

## Generating countermeasure assets and security patterns ##

By right clicking on a countermeasure in the Countermeasures window, an associated asset can be generated.  If defined, this will retain the same security properties associated with the countermeasure.  The asset will be situated in whatever environments the countermeasure was situated in.  In the asset model, a &lt;&lt; safeguard &gt;&gt; the association is added to the countermeasure asset and any assets threatened or exposed by the risk the countermeasure helps mitigate.

Assets can be generated directly based on the countermeasure properties, or on the basis of a pre-existing template asset.  It is also possible to situate security patterns based on a countermeasure, rather than an asset.  To do this, select Situate Pattern from the speed menu, select the security pattern, followed by the countermeasure environments to situate the pattern assets in.

Security Patterns can be imported into the tool by using the Import/Import Security Patterns option and selecting the XML based patterns catalogue to import.  An example catalogue file, schumacher.xml, which incorporates a number of patterns from the Security Patterns text book by Schumacher et al is included in the cairis/sql directory.

## Associating countermeasures with pre-existing patterns ##

By right clicking on a countermeasure in the Countermeasures window, you can also associate a countermeasure with a pre-existing security pattern by selecting the 'Associate with situated Countermeasure Pattern' option.  However, a list of possible security patterns to choose from will only be displayed if the components of the security pattern are present in ALL of the environments the countermeasure is situated for.

## Weakening the effectiveness of countermeasures ##

Countermeasures mitigate risks by targetting its risk elements, i.e. its threats or vulnerabilities.  However, when one or more assets are generated from these countermeasures, several factors may weaken the effect of the countermeasure.

First, situating assets may cause you to look at the environments where the assets are situated in a different light.  Changing properties of assets, or existing threats or vulnerabilities could increase the potency of the risk, thereby weakening the effect of the countermeasure.

Existing threats or vulnerabilities can also explicitly weaken countermeasures.  If a countermeasure asset is associated with a threat or vulnerability then, when either artefact is created or modified, CAIRIS allows users to override the effectiveness of the related countermeasure.  The detail associated with the risk scores in the Risk Dialog box will indicate cases where countermeasures have been weakened by threats and/or vulnerabilities.

## Mitigating weakening effects ##

If a countermeasure is weakened, the weakness by removed by generating a new countermeasure which targets the weakening threat or vulnerability.  If this is carried out, the detail associated with the risk score in the Risk Dialog box will indicate cases where, although the effectiveness score for the countermeasure holds, this is by virtue of a countermeasure targetting the weakening threat or vulnerability.

Countermeasures cannot, however, be simply defined on the fly.  They arise as the result of rational risk analysis, so risks need to be defined based on the weakening threats or vulnerabilities.

# Generating Documentation #


The current contents of the CAIRIS database can be generated as a requirements specification by selecting the Generate Documentation toolbar button.  After the sections to be included are selected in the Generate Documentation dialogue box, the target directory is prompted, following which the specification is generated as HTML, RTF, or PDF, based on the output options selected.

![fig:GenerateDocumentationDialog]({{ site.baseurl }}/images/GenerateDocumentationDialog.png "Generate Documentation Dialog")
