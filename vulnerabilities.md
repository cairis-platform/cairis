---
layout: default
title: Vulnerabilities
---

## Overview ##

Vulnerabilities are weaknesses of a system, which are liable to exploitation.

### Create a vulnerability ###

![fig:VulnerabilityDialog]({{ site.baseurl }}/images/VulnerabilityDialog.png "Vulnerability Dialog")

* Click on the Vulnerability toolbar button to open the Vulnerabilities dialogue box.

* Click on the Add button to open the Create Vulnerability dialogue box.

* Enter the vulnerability name and description, and select the vulnerability type from the combo box.

* Right-click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the vulnerability in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, select the vulnerability's severity for this environment, and add exposed assets by right-clicking on the asset box and selecting one or more assets from the selected environment.

* Click on the Create button to add the new vulnerability.

* Existing vulnerabilities can be modified by double-clicking on the vulnerability in the Vulnerabilities dialogue box, making the necessary changes, and clicking on the Update button.

* To delete a vulnerability, select the vulnerability to delete in the Vulnerabilities dialogue box, and select the Delete button.  If any artefacts are dependent on this vulnerability then a dialogue box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the vulnerability dependencies and the vulnerability itself, or No to cancel the deletion.

### Importing a vulnerability ###

![fig:ImportVulnerabilityDialog]({{ site.baseurl }}/images/ImportVulnerabilityDialog.png "Import Vulnerability")

The CAIRIS database is pre-loaded with a database of template vulnerabilities based on the Common Criteria.  To import one of these, select Import from the Vulnerabilities dialogue to open the Import Vulnerability dialogue. When a vulnerability is selected, the Vulnerability dialogue is opened, and pre-populated with information from the template.

![fig:ImportedVulnerabilityDialog]({{ site.baseurl }}/images/ImportedVulnerabilityDialog.png "Imported Vulnerability")
