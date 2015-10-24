---
layout: default
title: Environments
---

An environment might represent a system operating at a particular time of day, or in a particular physical location.  Environments encapsulate visible phenomena such as assets, tasks, personas, and attackers, as well as invisible phenomena, such as goals, vulnerabilities, and threats.  Environments may be identified at any time, although these may not become apparent until carrying out contextual inquiry and observing how potential users reason about their context of use.

## Adding a new environment ##

![fig:EnvironmentDialog]({{ site.baseurl }}/assets/EnvironmentDialog.png "Environment Dialog")

* Click on the Environment toolbar button to open the Environments dialog box, and click on the Add button to open the Environment dialog box.

* Enter the name of the environment, a short code, and a description.  The short-code is used to prefix requirement ids associated with an environment.

* If this environment is to be a composite environment, i.e. encompass artifacts of other environments, then right click on the environment list, select Add from the speed menu, and select the environment/s to add.

* It is possible artifact may appear in multiple environments within a composite environment.  It is, therefore, necessary to set duplication properties for composite environments.  If the maximise radio button is selected, then the maximal values associated with that artifact will be adopted.  This may be the highest likelihood value for a threat, or the highest security property values for an asset. If the override radio button is selected, then CAIRIS will ensure that the artifact properties are used for the overriding environment.

## On-the-fly environment creation ##

![fig:NewEnvironmentDialog]({{ site.baseurl }}/assets/NewEnvironmentDialog.png "New Environment Dialog")

Most artifacts in CAIRIS are situated in one or more environments.  When creating or updating an artifact, it is usually possible to create a new environment on the fly by right-clicking on the environment list box in the artifact dialog and selecting the New button.  This opens the New Environment dialog box.  In this dialog, an environment name, short code and description can be entered.  When the create button is selected, a new environment is added to the CAIRIS database, and added to the environment list for the artifact.

## Environmental attribute inheritence ##

An artifact may be situated in one or more environments, but the differences between these environments may be slight.  To reflect this, it is possible for an artifact to inherit properties from another environment.  To do this, right-click on the artifact's environment list box and select the Inherit Environment option.  When prompted, select the environment to inherit from, followed by the environment to situated the artifact in.  In most cases, the properties of the inherited environment will be duplicated in this newly situated environment.  In the case of goals and obstacles, only the immediate refinement associations are retained when inheriting properties from an environment.
