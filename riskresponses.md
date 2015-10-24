---
layout: default
title: Risk Responses
---

A risk can be treated in several ways.

By choosing to *Accept* a risk, we indicate that we are prepared to accept the consequences of the risk being realised.  Accepting the risk comes with a cost, and responsibility for accepting a risk must fall on one or more roles.

By choosing to *Transfer* a risk, we acknowledge that dealing with a risk is out of scope for this project. It may still, however, have a cost associated with it and, by accepting the risk, the risk must become the responsibility of one or more roles.

By choosing to *Mitigate* a risk, we may either Prevent, Deter, Detect, or React to a risk.  For detective responses, the response must detect the risk before, during, or after the risk's realisation.  For reactive responses, the response must be associated with an countermeasure asset derived from a detective response.

## Adding, updating, and deleting a response ##

![fig:ResponseDialog]({{ site.baseurl }}/assets/ResponseDialog.png "Response Dialog")

* Click on the Response toolbar button to open the Responses dialog box, and click on the Add button.  Select the response to take from the available options presented.

* Select the risk to associate this response with.

* Right click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the  response in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, select the response type.

* When the risk name and response type is selected, the response name is automatically generated.

* If an accept or transfer response was selected, a cost and rationale needs to be entered.  For transfer responses, one or more roles also need to be associated with the response.

* If a Detect response is selected, select the Detection Point (Before, Medium, or After).

* If a React response is selected, right click on Detection Mechanism box, select Add from the speed menu, and select a detection mechanism asset.

* Click on the Create button to add the new response.

* Existing responses can be modified by double clicking on the response in the Responses dialog box, making the necessary changes, and clicking on the Update button.

* To delete a response, select the response to delete in the Responses dialog box, and select the Delete button.  If any artifacts are dependent on this response then a dialog box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the response dependencies and the response itself, or No to cancel the deletion.

## Generating goals ##

A goal can be generated from a response by right clicking on the response name in the Responses dialog box, and selecting Generate Goal from the speed menu.  This causes a goal to be generated in each of the environments the response is situated in.  The goal name corresponds to the name of the response.
