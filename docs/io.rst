Importing and Exporting models
==============================

Importing models
----------------

You can import models by selecting the System / Import Model menu, selecting the model type to import, and the model file itself.

.. figure:: ImportModel.jpg
   :alt: import model form

You will usually want to stick with the Model option, which imports a standard CAIRIS XML model file (as defined by the DTD in https://cairis.org/dtd/cairis_model.dtd).  You can, however, import other types of model into your current working project.

============================================= =============================== ============================================================================================================================
Model type                                    DTD (in https://cairis.org/dtd) Model elements
============================================= =============================== ============================================================================================================================
Project data                                  cairis.dtd                      Project background, goal, scope, rich picture, naming conventions, contributors, revisions
Requirements                                  goals.dtd                       domain properties, goals, obstacles, requirements, use cases, and countermeasures
Risk analysis                                 riskanalysis.dtd                roles, assets, vulnerabilities, attackers, threats, risks, responses, asset associations
Usability                                     usability.dtd                   personas, external documents, document references, concept references, persona characteristics, task characteristics, tasks
Misusability                                  misusability.dtd                concept references, task characteristics
Associations                                  associations.dtd                manual associations, goal associations, dependencies
Threat and Vulnerability Types                tvtypes.dtd                     vulnerability types, threat types
Domain Values                                 domainvalues.dtd                threat values, risk values, countermeasure values, security values, likelihood values, motivation values, capability values
Threat and Vulnerability Directory            directory.dtd                   vulnerability directory entries, threat directory entries
Security Pattern                              securitypattern.dtd             security patterns
Architectural Pattern                         architectural_pattern.dtd       architectural patterns
Attack Pattern                                attack_pattern.dtd              attack patterns
Synopsis                                      synopsis.dtd                    characteristic synopses, reference synopses, step synopses, reference contributions, usecase contributions
Assets                                        template_assets.dtd             template assets
Processes                                     processes.dtd                   CSP process elements (used by desktop application only)
Locations                                     locations.dtd                   locations
Dataflows                                     dataflow.dtd                    dataflows and trust boundaries 
Attack Tree (Dot)                             N/A                             Graphviz (Dot) representation of an attack tree
============================================= =============================== ============================================================================================================================

Exporting models
----------------

To export a model, select the System / Export Model option.  This will render the current CAIRIS database you are working with as a CAIRIS XML model (conforming to cairis_model.dtd).
