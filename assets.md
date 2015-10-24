---
layout: default
title: Assets
---


## Overview ##

Assets are tangible objects of value to stakeholders.  By defining an asset in CAIRIS, we implicitly state that this needs to be secured in light of risks which subsequently get defined.

Assets are situated in one or more environments.  Security properties are associated with each asset for every environment it can be found in.  These security properties are Confidentiality, Integrity, Availability, and Accountability.  Each of these properties is associated with the value of None, Low, Medium, or High.  The meaning of each of these values can be defined in CAIRIS from the Asset Values dialog; this is available via the Options/Asset values menu.

## Adding, updating, and deleting an asset ##

![fig:AssetDialog]({{ site.baseurl }}/assets/AssetDialog.png "Asset Dialog")

* Click on the Asset toolbar button to open the Assets dialog box, and click on the Add button to open the Asset dialog box.

* Enter the name of the environment, a short code, description, and significance.  The short-code is used to prefix requirement ids associated with an environment.

* If this asset is deemed critical, click on the Criticality tab, and click on the Critical Asset check-box.  A rationale for declaring this asset critical should also be added.  By declaring an asset critical, any risk which either threatens or exploits this asset will be maximised until the mitigations render the likelihood of the threat or the severity of the vulnerability inert.

* Right click on the environment window to bring up the environment speed menu.  Select the add option and, from the Add environment window, select an environment to situate the asset in.  This will add the new environment to the environment list.

* After ensuring the environment is selected in the environment window, add the security properties to this asset for this environment.  Security properties are added by selecting the Properties tab, right clicking on the properties list and selecting Add to open the Add Security Properties window.  From this window, a security property and its value can be added.

* Click on the Create button to add the new asset.

* Existing assets can be modified by double clicking on the asset in the Assets dialog box, making the necessary changes, and clicking on the Update button.

* To delete an asset, select the asset to delete in the Assets dialog box, and select the Delete button.  If any artifacts are dependent on this asset then a dialog box stating these dependencies are displayed.  The user has the option of selecting Yes to remove the asset dependencies and the asset itself, or No to cancel the deletion.


## Asset modelling ##

Understanding how assets can be associated with each other is a useful means of identifying where the weak links in a prospective architecture might be.  CAIRIS supports the association of assets, inconsistency checking between associated assets, and visualisation of asset models.

The CAIRIS asset model is based on UML class models.  Asset models can be viewed for each defined environment.  As well as explicitly defined asset associations, asset models will also contain associations implicitly defined.  For example, if a task has been defined, and this task concerns within an environment contain one or more assets, then the participating persona will be displayed as an actor, and an association between this actor and the asset will be displayed.  Additionally, if concern associations have been defined between goals and assets and/or associations then zooming into the model will display these concerns; the concerns are displayed as blue comment elements.

![fig:AddAssetAssociation]({{ site.baseurl }}/assets/AddAssetAssociation.png "Add Asset Association Dialog")

### Adding an asset association ###

* If creating or updating an asset, an association between that asset and another asset can be made by clicking on the Associations tab in the Asset Dialog and, from the right-click speed menu, selecting Add to open the Add Asset Dialog.

* From the Add Asset Dialog, set the adornments for the head and tail end of the association.  Possible adornment options are Inheritence, Association, Aggregation, and Composition; the semantics for these adornments are based on UML.

* Set the multiplicity (nry) for the head and tail ends of the association.  Possible multiplicity options are `1`, `*`, and `1..*`.

* Optional role names can also be set at the head or tail end of the association.

* Select the Create (or Edit if modifying an existing association) will add the association to the Asset Dialog.  The association will not be adde to the database until the asset itself is created or modified.

* Asset associations can also be added by selecting the Asset Associations tool-bar button.  Clicking this button opens the Asset Associations dialog, where new associations can be created or existing associations can be modified or removed.  The dialog for modifying associations is identical to the Asset Association dialog, with the addition of a combo box for selecting the environment to situate the association in.

![fig:AssetInconsistency]({{ site.baseurl }}/assets/AssetInconsistency.png "Asset Inconsistency warning")

* If an asset is associated with an asset with one or more security properties of a lower value, then an Asset Inconsistency dialog is displayed, warning about the details of the inconsistency.


### Viewing Asset models ###

Asset models can be viewed by clicking on the Asset Model toolbar button, and selecting the environment to view the environment for.

![fig:AssetModel]({{ site.baseurl }}/assets/AssetModel.png "Asset Model")

By changing the environment name in the environment combo box, the asset model for a different environment can be viewed.  The layout of the model can also be replaced by selecting a layout option in the Layout combo box at the foot of the model viewer window.

By clicking on a model element, information about that artifact can be viewed.
