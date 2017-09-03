Assets
======

Assets are tangible objects of value to stakeholders. By defining an
asset in CAIRIS, we implicitly state that this needs to be secured in
light of risks which subsequently get defined.

Assets are situated in one or more environments. Security properties are
associated with each asset for every environment it can be found in.
These security properties are Confidentiality, Integrity, Availability,
and Accountability. Each of these properties is associated with the
value of None, Low, Medium, or High. The meaning of each of these values
can be defined in CAIRIS from the Asset Values dialog; this is available
via the Options/Asset values menu.

Adding, updating, and deleting an asset
---------------------------------------

.. figure:: AssetForm.jpg
   :alt: Asset form


-  Select the Risks/Assets menu button to open the assets table, and
   click on the Add button to open a new asset form.

-  Enter the name of the asset, a short code, description, and
   significance. The short-code is used to prefix requirement ids
   associated with an environment.

-  If this asset is deemed critical, click on the Criticality tab, and
   click on the Critical Asset check-box. A rationale for declaring this
   asset critical should also be added. By declaring an asset critical,
   any risk which either threatens or exploits this asset will be
   maximised until the mitigations render the likelihood of the threat
   or the severity of the vulnerability inert.

-  Click on the Add button in the asset table, and select an environment to situate the asset in. This will add
   the new environment to the environment list.

-  After ensuring the environment is selected in the environment window,
   add the security properties to this asset for this environment.
   Security properties are added by clicking on the Add button in the properties table
   to open the Choose security property dialog. From this window, a security property, its value
   its value rationale can be added.

-  Click on the Create button to add the new asset.

-  Existing assets can be modified by double clicking on the asset in
   the Assets dialog box, making the necessary changes, and clicking on
   the Update button.

-  To delete an asset, select the asset to delete in the assets table
   box, and select the Delete button. If any artifacts are dependent on
   this asset then a dialog box stating these dependencies are
   displayed. The user has the option of selecting Yes to remove the
   asset dependencies and the asset itself, or No to cancel the
   deletion.

Asset modelling
---------------

Understanding how assets can be associated with each other is a useful
means of identifying where the weak links in a prospective architecture
might be. CAIRIS supports the association of assets, inconsistency
checking between associated assets, and visualisation of asset models.

The CAIRIS asset model is based on UML class models. Asset models can be
viewed for each defined environment. As well as explicitly defined asset
associations, asset models will also contain associations implicitly
defined. For example, if a task has been defined, and this task concerns
within an environment contain one or more assets, then the participating
persona will be displayed as an actor, and an association between this
actor and the asset will be displayed. Additionally, if concern
associations have been defined between goals and assets and/or
associations then zooming into the model will display these concerns;
the concerns are displayed as blue comment elements.

.. figure:: AddAssetAssociation.jpg
   :alt: Add Asset Association form

Adding an asset association
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  You can add an association between assets by selecting the Risk/Asset Association menu, and
   clicking on the Add button in the association table.

-  In the association form which is opened., set the adornments for the head and tail
   end of the association. Possible adornment options are Inheritence,
   Association, Aggregation, and Composition; the semantics for these
   adornments are based on UML.

-  Set the multiplicity (nry) for the head and tail ends of the
   association. Possible multiplicity options are ``1``, ``*``, and
   ``1..*``.

-  Optional role names can also be set at the head or tail end of the
   association.

-  Select the Create (or Update if modifying an existing association) will
   add the association to the CAIRIS model.

- You can also add associations between other assets from the environment Associations tab within the Asset form.
  You can add a new association by clicking on the Add button in the association table to open the association form.
  From this form, you can add details about the nature of the association between the asset you're working on and another [tail] asset.
  Once you click on Update, the association will be added to your working object, but won't be committed to the model until you click on the Update/Create button.

Viewing Asset models
~~~~~~~~~~~~~~~~~~~~

Asset models can be viewed by selecting the Models/Asset menu, and selecting the environment to view the environment for.

.. figure:: AssetModel.jpg
   :alt: Asset Model

By changing the environment name in the environment combo box, the asset
model for a different environment can be viewed.  The model can be filtered by selecting an asset.
This will display on the asset, and the other asset model elements immediately associated with it.
By default, concern associations are hidden.  These are UML comment nodes that indicate elements from other CAIRIS models associated with asset.
These concerns can be shown by changing the Hide Concerns combo box value to Yes.

By clicking on a model element, information about that artifact can be
viewed.

CAIRIS models are rendered in the web browser as SVG.  Although CAIRIS doesn't have any explicit functionality for printing models, you can use the `SVG Crowbar <http://nytimes.github.io/svg-crowbar/>`_ bookmarklet to download an SVG file based on any given graphical model.  This model can either be directly used, or edited using an appropriate SVG vector graphics editor, e.g. `Inkscape <https://inkscape.org>`_.
