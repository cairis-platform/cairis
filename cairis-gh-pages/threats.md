---
layout: default
title: Threats
---

## Overview ##

Threats are synonymous with attacks, and can therefore only be defined if an associated attacker has also been defined.  Like vulnerabilities, threats are associated with one or more assets.  However, threats may also target certain security properties as well, in line with security values that an attacker wishes to exploit.

A threat is also of a certain type.  CAIRIS is pre-loaded with a selection of these, but these can be modified, or new threat types created by selecting the Options/Threat Types menu option.

## Adding, updating, and deleting a threat ##

![fig:ThreatDialog]({{ site.baseurl }}/images/ThreatDialog.png "Threat Dialog")

* Click on the Threat toolbar button to open the Threats dialog box, and click on the Add button to open the Threat dialog box.

* Enter the threat name, the method taken by an attacker to release the threat, and select the threat type.

* Right click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the threat in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, select the threat's likelihood for this environment

* Associate attackers with this threat by right clicking on the attacker box, selecting Add from the speed menu, and selecting one or more attackers associated with the environment.

* Add threatened assets by right clicking on the asset box, selecting Add from the speed menu, and selecting one or more assets from the selected environment.

* Add the security properties to this threat by right clicking on the properties list, and selecting Add from the speed menu to open the Add Security Properties window.  From this window, a security property and its value can be added.

* Click on the Create button to add the new threat.

* Existing threats can be modified by double clicking on the threat in the Threats dialog box, making the necessary changes, and clicking on the Update button.

* To delete a threat, select the threat to delete in the Threats dialog box, and select the Delete button.  If any artifacts are dependent on this attacker then a dialog box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the threat dependencies and the threat itself, or No to cancel the deletion.

## Importing threats ##

![fig:ImportThreatDialog]({{ site.baseurl }}/images/ImportThreatDialog.png "Import Threat")

The CAIRIS database is pre-loaded with a database of template threats based on the Common Criteria.  To import one of these, select Import from the Threats dialog to open the Import Threat dialog. When a threat is selected, the Threat dialog is opened, and pre-populated with information from the template.
