Security Patterns
=================

Security Patterns are solution structures, which prescribe a solution to
a security problem arising in a context. Many components and connectors
in secure system architectures are instances of security patterns but,
in many cases, the reasoning for a given pattern's inclusion is not
always clear. The requirements needed to realise these patterns are also
often omitted, making the job of reasoning about the consequences of
situating the pattern difficult. Moreover, security patterns may be
described in a context, but not all collaborating assets in a security
pattern may be evident in all possible contexts of a system's use. The
following sections describe how CAIRIS treats security patterns and
deals with these weaknesses.

Security Patterns in CAIRIS consist of the following elements:

-  A description of the context a pattern is relevant for.

-  A problem statement motivating the need for the pattern.

-  A solution statement describing the intrinsics of the pattern.

-  The pattern structure, modelled as associations between collaborating
   asset classes.

-  A set of requirements, which need to be fulfilled in order to realise
   the pattern.  These requirements are based on template requirements.

Before a security pattern can be defined in CAIRIS, template assets --
which represent the collaborating asset classes -- need to be first
defined.

Before a security pattern can be situated in CAIRIS environments, the
environments themselves need to be first created.

Create a template asset
-----------------------

.. figure:: TemplateAssetForm.jpg
   :alt: Template Asset form

Template assets can be best described as context-free assets. When they
are created, template assets do not form part of analysis unless they
are implicitly introduced. This 'implicit introduction' occurs when a
security pattern is situated.

The Template Patterns dialog can be opened by selecting the
Options/Template Assets menu option.

The process for creating, updating, and deleting a template asset is
almost identical to the processes uses for normal assets. The only
difference is the lack of environment-specific properties. Security
properties are only defined once for the asset.

To situate an asset in an environment, click on the situate button in the template assets list, and
specify the environments to situate the template asset in. After a
template asset is situated within an environment, these properties
should be revised in the assets generated on the basis of these. This is
because the values associated with the template asset properties may not
be inline with assumptions held about Low, Medium, and High assets in
the specification being developed.

Create a security pattern
-------------------------

.. figure:: SecurityPatternForm.jpg
   :alt: Security Pattern form


-  Select the Risks/Security Patterns menu option to open the Security
   Patterns table, and click on the Add button to open the Security
   Pattern dialog form.

-  Enter the security pattern name, and description of the context the security pattern is relevant for, 
-  a problem description motivationg the security pattern, and the intrinsics of how the security pattern
   solves the pre-defined problem.

-  Click on the Structure tab, and the Add button in the associations table to add associations between template assets; these associations form the collaborative structure for the pattern. The procedure for entering associations is based on that used for associating assets.

-  Click on the Requirements tab, and the Add button in the requirements
   table to add names of template requirements needing to be satisfied to realise
   the pattern.
   
-  Click on the Create button to add the new security pattern.

-  Existing security patterns can be modified by double clicking on the
   security pattern in the security patterns table, making the
   necessary changes, and clicking on the Update button.

-  To delete a security pattern, click on the Delete button besides pattern to delete in the
   security patterns table.

Situate a security pattern
--------------------------

-  To introduce a security pattern into the working project, select the Risks/Security Patterns menu, click on the situate button for the pattern to be situated.

-  Select the environment to situate the environment in, and click on Ok to situate the pattern.

Template assets will be instantiated as assets, and situate in the
stipulated assets. Requirements associated with the pattern, will be
introduce and associated with the stipulated assets in the pattern
definition. These assets will be ordered based on the order of
definition in the pattern structure.
