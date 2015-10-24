---
layout: default
title: Tasks
---

## Overview ##

Tasks model the work carried out by one or more personas.  This work is described in environemnt-specific narrative scenarios, which illustrate how the system is used to augment the work activity.

### Adding, updating, or deleting a task ###

![fig:TaskDialog]({{ site.baseurl }}/assets/TaskDialog.png "Task Dialog")

* Click on the Task toolbar button to open the Tasks dialog box, and click on the Add button to open the Task dialog box.

* Enter a task name, and the objective of carrying out the task.

* If the task is not derived from empirical data, then select the Asssumption Task check-box.  Ticking this box has the effect of pre-fixing the task name with an &lt;&lt; assumption &gt;&gt; stereotype in any models where the task is present.

* Right click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the persona in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, click on the Summary tab.  In the Summary page, enter any dependencies needing to hold before this task can take place.  

![fig:AddTaskPersona]({{ site.baseurl }}/assets/AddTaskPersona.png "Add Task Persona Dialog")

* Right click on the persona list box and select Add from the speed menu to associate a persona with this task.  In the Add Task Persona dialog box, select the person, the task duration (seconds, minutes, hours or longer), frequency (hourly or more, daily-weekly, monthly or less),demands (none, low, medium, high), and goal conflict (none, low, medium, high). The values for low, medium, and high should be agreed with participants before hand.  

* If any aspect of the task concerns one or more assets, then these can be added to the concern list.  Adding an asset concern causes a concern comment to be associated to the asset in the asset model.  If the task concerns an association between assets, the association can be added by clicking on the Concern Association tab and adding the source and target assets and association multiplicity to the concern association list.  In the asset model, this association is displayed and a concern comment is associated to each asset in the association.

* Right click on the Narrative tab and enter the task scenario in the text box.  This narrative should describe how the persona (or personas) carry out the task to achieve the pre-defined objective.

* Click on the Create button to add the new task.

* Existing tasks can be modified by double clicking on the task in the Tasks dialog box, making the necessary changes, and clicking on the Update button.

* To delete a task, select the task to delete in the Tasks dialog box, and select the Delete button.  If any artifacts are dependent on this task then a dialog box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the task dependencies and the task itself, or No to cancel the deletion.

### Task traceability ###

![fig:TraceabilityEditor]({{ site.baseurl }}/assets/TraceabilityEditor.png "Traceability Editor")

Tasks can be manually traced to certain artifacts via the Tasks dialog.  A task may contribute to an asset or a vulnerability, or be supported by requirement.  To add a traceability link, right click on the task name, and select Supported By or Contributes to.  This opens the Traceability Editor.  From this editor, select the object on the right hand side of the editor to trace to and click the Add button to add this link.

Manual traceability links can be removed by selecting the View/Traceability menu option, to open the Traceability Relations dialog.  In this dialog box, manual traceability relations be removed from specific environments.

### Visualising tasks ###

Task models can be viewed by clicking on the Task Model toolbar button, and selecting the environment to view the environment for.

![fig:TaskModel]({{ site.baseurl }}/assets/TaskModel.png "Task Model")

By changing the environment name in the environment combo box, the task model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artifact can be viewed.  
