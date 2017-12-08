Threats
=======

Threats are synonymous with attacks, and can therefore only be defined
if an associated attacker has also been defined. Like vulnerabilities,
threats are associated with one or more assets. However, threats may
also target certain security properties as well, in line with security
values that an attacker wishes to exploit.

A threat is also of a certain type. CAIRIS is pre-loaded with a
selection of these, but these can be modified, or new threat types
created by selecting the Options/Threat Types menu option.

Adding, updating, and deleting a threat
---------------------------------------

.. figure:: ThreatForm.jpg
   :alt: Threat form


-  Select the Risks/Threats menu to open the Threats table,
   and click on the Add button to open the Threat form.

-  Enter the threat name, the method taken by an attacker to release the
   threat, and select the threat type.

-  Click on the Add button in the environment table, and select an environment to situate the threat in. This will add the new environment to the environment list.

-  Select the threat's likelihood for this environment

-  Associate attackers with this threat by clicking on the Add button above the Attacker table, and selecting one or more attackers specific to the environment.

-  Add threatened assets by clicking on the Add button above the Assets table, and selecting one or more assets specific to the environment.

-  Add the security properties to this threat by clicking on the Add button above the properties table, and selecting a security property, value, and rationale.

-  Click on the Create button to add the new threat.

-  Existing threats can be modified by clicking on the threat in
   the Threats table, making the necessary changes, and clicking on
   the Update button.

-  To delete a threat, click on the Delete button threat next to the threat to be removed in the Threats table.  If any artifacts are dependent on this attacker then a dialog box stating these dependencies are displayed. The user has the option of selecting Yes to remove the threat dependencies and the threat itself, or No to cancel the deletion.
