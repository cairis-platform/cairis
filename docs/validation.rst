Model Validation
================

CAIRIS has the ability to validate models for a given environment based on potential design problems.  

To validate a current CAIRIS model, click on the Models/Validate menu and select the environment to check the CAIRIS model for.

.. figure:: MVForm.jpg
   :alt: Model Validation results

The model validation checks currently supported are as follows:

=================================================================== =======================================================================================================================================================
Check                                                               Description
=================================================================== =======================================================================================================================================================
Composition/Aggregation Integrity Check                             For Hardware/Software/Information assets, checks head asset integrity isn't lower than the tail asset.
Lawfulness, Fairness, and Transparency (GDPR): Fair data processing Checks data with privacy properties is processed only if it's recognised as personal data.
Lawfulness, Fairness, and Transparency (GDPR): Lawful data handling Checks at least one persona working with a task or use case involving personal data is fulfiling the role of a Data Processor or Data Controller.
Lawfulness, Fairness, and Tranaparency (GDPR): Necessary processing Checks any use case involving personal data is associated with a necessary goal or requirement.
Purpose Limitation (GDPR)                                           Checks any use case involving personal data is associated with a necessary goal concerned with that personal data.
Data Minimisation (GDPR)                                            Checks that data with privacy properties are accounted for in processes.
Accuracy (GDPR)                                                     Checks personal data has an Integrity security property.
Integrity & Confidentiality (GDPR)                                  Checks for unmitigated risks where personal information has confidentiality, integrity, and privacy properties that threats target.
=================================================================== =======================================================================================================================================================
