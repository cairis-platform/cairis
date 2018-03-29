---
layout: default
title: Tasks
---

## Overview ##

Tasks model the work carried out by one or more personas.  This work is described in environment-specific narrative scenarios, which illustrate how the system is used to augment the work activity.

### Adding, updating, or deleting a task ###

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

### Task traceability ###

![fig:TraceabilityEditor]({{ site.baseurl }}/images/TraceabilityEditor.png "Traceability Editor")

Tasks can be manually traced to certain artefacts via the Tasks dialogue.  A task may contribute to an asset or a vulnerability, or be supported by the requirement.  To add a traceability link, right click on the task name, and select Supported By or Contributes to.  This opens the Traceability Editor.  From this editor, select the object on the right-hand side of the editor to trace to and click the Add button to add this link.

Manual traceability links can be removed by selecting the View/Traceability menu option, to open the Traceability Relations dialogue.  In this dialogue box, manual traceability relations be removed from specific environments.

### Visualising tasks ###

Task models can be viewed by clicking on the Task Model toolbar button and selecting the environment to view the environment for.

![fig:TaskModel]({{ site.baseurl }}/images/TaskModel.png "Task Model")

By changing the environment name in the environment combo box, the task model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artefact can be viewed.  
