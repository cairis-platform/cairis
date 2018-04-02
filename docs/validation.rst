Model Validation
================

CAIRIS has the ability to validate models for a given environment based on potential security and privacy design problems.  

To validate a current CAIRIS model, click on the Models/Validate menu and select the environment to check the CAIRIS model for.

.. figure:: MVForm.jpg
   :alt: Model Validation results


Security design checks
----------------------

The security design checks currently supported are as follows: 

================================= ======================================================================================================
Check                             Description
================================= ======================================================================================================
Composition/Aggregation Integrity For Hardware/Software/Information assets, checks head asset integrity isn't lower than the tail asset.
================================= ======================================================================================================


Privacy design checks
----------------------

If personal data has been introduced then the CAIRIS model is checked to ensure it doesn't violate any General Data Protection Regulation (GDPR) principles.  The checks carried out are described below:

======================================  =========================  =================================================================================================================================================
GDPR Principle                          Check                      Description
======================================  =========================  =================================================================================================================================================

Lawfulness, Fairness, and Transparency  Fair data processing       Checks data with privacy properties is processed only if it's recognised as personal data.
Lawfulness, Fairness, and Transparency  Lawful data handling       Checks at least one persona working with a task or use case involving personal data is fulfiling the role of a Data Processor or Data Controller.
Lawfulness, Fairness, and Tranaparency  Necessary processing       Checks any use case involving personal data is associated with a necessary goal or requirement.
Purpose Limitation                      Data purpose               Checks any use case involving personal data is associated with a necessary goal concerned with that personal data.
Data Minimisation                       Private data processing    Checks that data with privacy properties are accounted for in processes.
Accuracy                                Personal data integrity    Checks personal data has an Integrity security property.
Storage Limitation                      Unprocessed personal data  Checks for personal data in data stores that is not processed.
Integrity & Confidentiality             Unmitigated privacy risks  Checks for unmitigated risks where personal information has confidentiality, integrity, and privacy properties that threats target.
======================================  =========================  =================================================================================================================================================
