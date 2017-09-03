Goals, Requirements, and Obstacles
==================================

In CAIRIS, a requirements specification is analogous to a safety case.
In a safety case, a system is only considered safe if its safety goals
have been satisfied. In a similar manner, requirements are leaf nodes in
a goal tree and satisfying stakeholder needs is only possible if the
high-level goals -- stipulated by stakeholders -- can be satisfied.

We define goals as prescriptive statements of system intent that are
achievable by one or more agents. Goals can be refined to requirements,
which are achievable by only agent. Goals and requirements may also be
operationalised as tasks. Alternatively, we may decide to specify tasks
and ask what goals or requirements need to hold in order that a given
task can be completed successfully.

To satisfy a goal, one or more sub-goals may need to be satisfied;
satisfaction may require satisfying a conjunction of sub-goals, i.e.
several AND goals, or a disjunction of sub-goals, i.e. several OR goals.

Goals or requirements may be obstructed by obstacles, which are
conditions representing undesired behaviour; these prevent an associated
goal from being achieved. By progressively refining obstacles, we can
obtain the origin of some undesired behaviour; this may be reflected as
a vulnerability or a threat, and contribute to risk analysis.

Adding, updating, and deleting a goal
-------------------------------------

.. figure:: GoalsTable.jpg
   :alt: Goals table


-  Click on the Requirements/Goals button to open the Goals table. As
   the above figure illustrates, next to goal name is the current
   *status* for the goal. If a goal is defined as OK, then this goal is
   refined by a requirement, or by one or more goals. Goals with the
   status *to refine* have yet to be refined or operationalised. Goals
   with the status *Check* have been refined by one or more obstacle,
   and these should be examined to find a root threat or vulnerability.

.. figure:: GoalForm.jpg
   :alt: Goal form

-  Click on the Add button to open the Goal form, and enter the
   name of the goal.

-  Click on the Add button in the environment table, and select an environment to situate the goal in. This will add the new environment to the environment list.

-  In the Definition page, enter the goal definition, and select the
   goal category and priority. Possible goal categories are: Achieve,
   Maintain, Avoid, Improve, Increase, Maximise, and Minimise. Possible
   priority values are Low, Medium, and High.

-  Click on the Fit Criterion folder, and enter the criteria which must
   hold for the goal to be satisfied.

-  Click on the Issue tab and enter any issues or comments relating to
   this goal.

.. figure:: AddGoalRefinement.jpg
   :alt: Add Goal Refinement form


-  If this goal refines a parent goal, click on the Goals tab,
   click on Add button in the goals table to to open the Add
   Goal Refinement form. In this form, select the Goal from the Type
   combo box, and select the Sub-goal, refinement type, and an Alternate
   value. Possible refinement types are: and, or, conflict, responsible,
   obstruct, and resolve. The alternative value (Yes or No) indicates
   whether or not this goal affords a goal-tree for an alternate
   possibility for satisfying the parent goal. It is also possible to
   enter a rationale for this goal refinement in the refinement text
   book. Clicking on Update will add the refinement association to memory,
   but this will not be committed to the database until the goal is
   added or updated.

-  If this goal refines to sub-goals already specified, Click on the
   Sub-Goals tab and add a goal refinement association as described in
   the previous step. A goal may refine to artifacts other than goals,
   specifically tasks, requirements, obstacles, and domain properties.

-  Goal refinements can also be specified independently of goal creation
   or modification via the Goal Associations tool-bar button.

-  If any aspect of the goal concerns one or more assets, then these can
   be added by clicking on the Concerns folder and adding the asset/s to
   the concern list. Adding an asset concern causes a concern comment to
   be associated to the asset in the asset model. If the goal concerns
   an association between assets, the association can be added by
   clicking on the Concern Association tab and adding the source and
   target assets and association multiplicity to the concern association
   list. In the asset model, this association is displayed and a concern
   comment is associated to each asset in the association.

-  Click on the Create button to add the new goal.

-  Existing goals can be modified by clicking on the goal name in the
   Goals table, making the necessary changes, and clicking on the
   Update button.

-  To delete a goal, select the goal to delete in the Goals table,
   and select the Delete button. If any artifacts are dependent on this
   goal then a dialog box stating these dependencies are displayed. The
   user has the option of selecting Yes to remove the goal dependencies
   and the goal itself, or No to cancel the deletion.

Goal Modelling
--------------

Goal models can be viewed by clicking on the Models/Goal menu option,
and selecting the environment to view the environment for.

.. figure:: GoalModel.jpg
   :alt: Goal Model

By changing the environment name in the environment combo box, the goal
model for a different environment can be viewed.

By clicking on a model element, information about that artifact can be
viewed.

Goal models can also be filtered by goal. Applying a filter causes the
selected goal to be displayed as the root goal. Consequently, goals are
only displayed if they are direct or indirect leafs of the filtered
goal.

For details on how to print models as SVG files, see the `Viewing Asset models`_ section.


Adding, updating, and deleting an obstacle
------------------------------------------

.. figure:: ObstacleForm.jpg
   :alt: Obstacle form


-  Click on the Requirements/Obstacle menu to open the Obstacles table
   box, and click on the Add button to open the Obstacle dform.

-  Enter the name of the obstacle, and click on the Add button in the environment table, and select an environment to situate the obstacle in. This will add the new environment to the environment list.

-  In the Definition page, enter the obstacle definition, and select the
   obstacle category. Possible obstacle categories are: Confidentiality
   Threat, Integrity Threat, Availability Threat, Accountability Threat,
   Vulnerability, Duration, Frequency, Demands, and Goal Support.

-  In the Probability page, enter a double-precision probability value (if known), together with a rationale statement justifying the value.

-  Like goals, obstacle refinements can be added via the Goals and
   Sub-Goals tabs.

-  If any aspect of the obstacle concerns one or more assets, then these
   can be added by clicking on the Concerns add and adding the asset/s
   to the concern list. Adding an asset concern causes a concern comment
   to be associated to the asset in the asset model.

-  Click on the Create button to add the new obstacle.

-  Existing obstacles can be modified by selecting the obstacle
   in the Obstacles table, making the necessary changes, and
   clicking on the Update button.

-  To delete an obstacle , select the obstacle to delete in the
   Obstacles table, and select the Delete button. If any artifacts
   are dependent on this obstacle then a dialog box stating these
   dependencies are displayed. The user has the option of selecting Yes
   to remove the obstacle dependencies and the obstacle itself, or No to
   cancel the deletion.

Obstacle Modelling
------------------

Obstacle models can be viewed by clicking on the Models/Obstacle menu
button, and selecting the environment to view the environment for.

.. figure:: ObstacleModel.jpg
   :alt: Obstacle Model

In many ways, the obstacle model is very similar to the goal model. The
main differences are goal filtering is not possible, only the obstacle
tree is displayed, and obstacles refine to obstacles, as opposed to
goals.

For details on how to print models as SVG files, see the `Viewing Asset models`_ section.


Adding, updating, and deleting requirements
-------------------------------------------

Requirements are added and edited using the Requirements Editor, which is accessible by selecting the Requirements/Requirements menu option. Each requirement is associated with an asset, or an
environment. Requirements associated with assets may specify the asset,
constrain the asset, or reference it in some way. Requirements
associated with an environment are considered transient, and remain
associated with an environment only until appropriate assets are
identified.

-  To add a requirement, select the asset or environment to associate the requirement with, and click on the Add button.  A new requirement will appear at the foot of the requirements table.

-  Enter the requirement description, rationale, fit criterion, and
   originator in the appropriate cells, select the priority (1,2, 3),
   and the requirement type (Functional, Data, Look and Feel, Usability,
   Performance, Operational, Maintainability, Portability, Security,
   Cultural and Political, and Legal).

-  When the attributes have been entered, press Enter to commit the requirement to the database.


-  By changing the asset in the Assets combo box, or the Environment in
   the Environments combo box, the editor will be reloaded with the
   requirement associated with the selected asset or environment.

-  A requirement can be deleting by right clicking on any cell in the row to be removed, and selecting Remove from the speed menu. Deleting a requirement also has the effect of re-ordering the
   requirement labels.


Searching requirement text
--------------------------

It is possible to search for a requirement or any other model object with a particular text
string from the Search box in the menu bar. This Find dialog is very similar to
the Find dialog found in many WYSIWYG applications.

Requirements traceability
-------------------------

Normally requirements traceability is synonymous with adding a goal
refinement association but, requirements may also contribute to
vulnerabilities (as well as tasks), or be supported by assets or misuse
cases. Consequently, requirements can be manually traced to these
artifacts in the same manner as tasks.
