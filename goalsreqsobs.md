---
layout: default
title: Goals, Requirements, and Obstacles
---

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

* If this goal refines to sub-goals already specified, Click on the Sub-Goals tab and add a goal refinement association as described in the previous step.  A goal may refine to artefacts other than goals, specific tasks, requirements, obstacles, and domain properties.

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

Goals can also be refined from the goal model, albeit only for the environment is modified.  To refine a goal, right-click on the goal in the model viewer, and select And-Goal, or Or-Goal based on the refinement desired.  A simplified version of the Add Goal dialog box is displayed and, when all the necessary information has been added, a new goal will be added to the database, complete with the desired refinement.  Please note, the model view needs to be refreshed to view the goal.  Goals may only be refined to other goals in the model viewer; for anything more elaborate, the usual goal refinement association procedure needs to be followed.


## Adding, updating, and deleting an obstacle ##

![fig:ObstacleDialog]({{ site.baseurl }}/images/ObstacleDialog.png "Obstacle Dialog")

* Click on the Obstacle toolbar button to open the Obstacles dialogue box, and click on the Add button to open the Obstacle dialogue box.

* Enter the name of the obstacle, and right click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the obstacle in.  This will add the new environment to the environment list.

* In the Definition page, enter the obstacle definition, and select the obstacle category.  Possible obstacle categories are: Confidentiality Threat, Integrity Threat, Availability Threat, Accountability Threat, Vulnerability, Duration, Frequency, Demands, and Goal Support.

* Like goals, obstacle refinements can be added via the Goals and Sub-Goals tabs.

* If any aspect of the obstacle concerns one or more assets, then these can be added by clicking on the Concerns add and adding the asset/s to the concern list.  Adding an asset concern causes a concerned comment to be associated to the asset in the asset model.

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
