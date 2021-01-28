/* 
  Licensed to the Apache Software Foundation (ASF) under one
  or more contributor license agreements.  See the NOTICE file
  distributed with this work for additional information
  regarding copyright ownership.  The ASF licenses this file
  to you under the Apache License, Version 2.0 (the
  "License"); you may not use this file except in compliance
  with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing,
  software distributed under the License is distributed on an
  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
  KIND, either express or implied.  See the License for the
  specific language governing permissions and limitations
  under the License.
*/

drop function if exists internalDocumentQuotationString;
drop function if exists personaQuotationString;

DROP VIEW IF EXISTS value_type;
DROP VIEW IF EXISTS object_name;
DROP VIEW IF EXISTS entity;
DROP VIEW IF EXISTS datastore;
DROP VIEW IF EXISTS dataflows;
DROP VIEW IF EXISTS personal_dataflows;
DROP VIEW IF EXISTS countermeasure_vulnerability_response_target;
DROP VIEW IF EXISTS countermeasure_threat_response_target;
DROP VIEW IF EXISTS redmine_requirement;
DROP VIEW IF EXISTS synopsis;
DROP VIEW IF EXISTS contribution;
DROP VIEW IF EXISTS goal_contribution;
DROP VIEW IF EXISTS goal_contribution_table;
DROP VIEW IF EXISTS source_reference;
DROP VIEW IF EXISTS environment_role;
DROP VIEW IF EXISTS detection_mechanism;
DROP VIEW IF EXISTS concept_reference;
DROP VIEW IF EXISTS task_documentconcept_reference;
DROP VIEW IF EXISTS documentconcept_reference;
DROP VIEW IF EXISTS assumption_persona_model;
DROP VIEW IF EXISTS assumption_task_model;
DROP VIEW IF EXISTS environment_risk;
DROP VIEW IF EXISTS environment_trust_boundary;
DROP VIEW IF EXISTS concept_map;
DROP VIEW IF EXISTS component_interfaces;
DROP VIEW IF EXISTS connectors;
DROP VIEW IF EXISTS component_asset;
DROP VIEW IF EXISTS asset_template_asset;
DROP VIEW IF EXISTS securitypattern_requirement;
DROP VIEW IF EXISTS component_requirement;
DROP VIEW IF EXISTS component_goal;
DROP VIEW IF EXISTS misusability_case;
DROP VIEW IF EXISTS usecase_step_synopsis_actor;
DROP VIEW IF EXISTS quotation;
DROP VIEW IF EXISTS personal_information;
DROP VIEW IF EXISTS process_asset;
DROP VIEW IF EXISTS process_personal_information;
DROP VIEW IF EXISTS datastore_asset;
DROP VIEW IF EXISTS datastore_personal_information;
DROP VIEW IF EXISTS personal_risk;
DROP VIEW IF EXISTS goal_associations;
DROP VIEW IF EXISTS riskModel_tagged;
DROP VIEW IF EXISTS conceptMapModel_all;
DROP TABLE IF EXISTS task_goal_contribution;
DROP TABLE IF EXISTS trust_boundary_usecase;
DROP TABLE IF EXISTS trust_boundary_asset;
DROP TABLE IF EXISTS trust_boundary_privilege;
DROP TABLE IF EXISTS trust_boundary_tag;
DROP TABLE IF EXISTS trust_boundary;
DROP TABLE IF EXISTS trust_boundary_type;
DROP TABLE IF EXISTS dataflow_process_process;
DROP TABLE IF EXISTS dataflow_entity_process;
DROP TABLE IF EXISTS dataflow_process_entity;
DROP TABLE IF EXISTS dataflow_process_datastore;
DROP TABLE IF EXISTS dataflow_datastore_process;
DROP TABLE IF EXISTS dataflow_asset;
DROP TABLE IF EXISTS dataflow_obstacle;
DROP TABLE IF EXISTS stpa_keyword;
DROP TABLE IF EXISTS dataflow_tag;
DROP TABLE IF EXISTS dataflow;
DROP TABLE IF EXISTS dataflow_type;
DROP TABLE IF EXISTS persona_instance;
DROP TABLE IF EXISTS asset_instance;
DROP TABLE IF EXISTS location_link;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS usecase_step_synopsis;
DROP TABLE IF EXISTS usecase_pc_contribution;
DROP TABLE IF EXISTS usecase_tc_contribution;
DROP TABLE IF EXISTS usecase_dr_contribution;
DROP TABLE IF EXISTS ice_ic_contribution;
DROP TABLE IF EXISTS user_system_goal_link;
DROP TABLE IF EXISTS document_reference_contribution;
DROP TABLE IF EXISTS requirement_reference_contribution;
DROP TABLE IF EXISTS document_reference_synopsis;
DROP TABLE IF EXISTS requirement_reference_synopsis;
DROP TABLE IF EXISTS persona_characteristic_synopsis;
DROP TABLE IF EXISTS task_characteristic_synopsis;
DROP TABLE IF EXISTS contribution_end;
DROP TABLE IF EXISTS link_contribution;
DROP TABLE IF EXISTS goal_satisfaction;
DROP TABLE IF EXISTS task_tag;
DROP TABLE IF EXISTS usecase_tag;
DROP TABLE IF EXISTS persona_tag;
DROP TABLE IF EXISTS asset_tag;
DROP TABLE IF EXISTS template_asset_tag;
DROP TABLE IF EXISTS attacker_tag;
DROP TABLE IF EXISTS threat_tag;
DROP TABLE IF EXISTS vulnerability_tag;
DROP TABLE IF EXISTS risk_tag;
DROP TABLE IF EXISTS goal_tag;
DROP TABLE IF EXISTS obstacle_tag;
DROP TABLE IF EXISTS domainproperty_tag;
DROP TABLE IF EXISTS countermeasure_tag;
DROP TABLE IF EXISTS response_tag;
DROP TABLE IF EXISTS component_view_component;
DROP TABLE IF EXISTS connector;
DROP TABLE IF EXISTS component_view;
DROP TABLE IF EXISTS component_interface;
DROP TABLE IF EXISTS asset_interface;
DROP TABLE IF EXISTS template_asset_interface;
DROP TABLE IF EXISTS interface;
DROP TABLE IF EXISTS component_asset_template_asset;
DROP TABLE IF EXISTS component_requirement_template_requirement;
DROP TABLE IF EXISTS component_goal_template_goal;
DROP TABLE IF EXISTS component_goalgoal_goalassociation;
DROP TABLE IF EXISTS component_classassociation;
DROP TABLE IF EXISTS component_template_requirement;
DROP TABLE IF EXISTS component_template_goal;
DROP TABLE IF EXISTS component_vulnerability_target;
DROP TABLE IF EXISTS component_threat_target;
DROP TABLE IF EXISTS document_reference_vulnerability;
DROP TABLE IF EXISTS document_reference_obstacle;
DROP TABLE IF EXISTS ice_ic_contribution;
DROP TABLE IF EXISTS implied_characteristic_element_intention;
DROP TABLE IF EXISTS implied_characteristic_element;
DROP TABLE IF EXISTS implied_characteristic_intention;
DROP TABLE IF EXISTS implied_characteristic;
DROP TABLE IF EXISTS internal_document_code_intention;
DROP TABLE IF EXISTS internal_document_code;
DROP TABLE IF EXISTS internal_document_memo;
DROP TABLE IF EXISTS internal_document;
DROP TABLE IF EXISTS persona_environment_code;
DROP TABLE IF EXISTS persona_code;
DROP TABLE IF EXISTS task_environment_code;
DROP TABLE IF EXISTS task_code;
DROP TABLE IF EXISTS artifact_section;
DROP TABLE IF EXISTS persona_implied_process_network;
DROP TABLE IF EXISTS persona_implied_process_channel;
DROP TABLE IF EXISTS persona_implied_process;
DROP TABLE IF EXISTS persona_code_network;
DROP TABLE IF EXISTS channel_parameter;
DROP TABLE IF EXISTS channel;
DROP TABLE IF EXISTS parameter;
DROP TABLE IF EXISTS memo;
DROP TABLE IF EXISTS code;
DROP TABLE IF EXISTS code_type;
DROP TABLE IF EXISTS relationship_type;
DROP TABLE IF EXISTS value_tension;
DROP TABLE IF EXISTS tension;
DROP TABLE IF EXISTS vulnerability_asset_countermeasure_effect;
DROP TABLE IF EXISTS threat_asset_countermeasure_effect;
DROP TABLE IF EXISTS securitypattern_asset_template_asset;
DROP TABLE IF EXISTS countermeasure_securitypattern;
DROP TABLE IF EXISTS securitypattern_classassociation;
DROP TABLE IF EXISTS securitypattern_template_requirement;
DROP TABLE IF EXISTS securitypattern;
DROP TABLE IF EXISTS template_asset_property;
DROP TABLE IF EXISTS template_requirement;
DROP TABLE IF EXISTS template_goal_responsibility;
DROP TABLE IF EXISTS template_goal_concern;
DROP TABLE IF EXISTS template_goal;
DROP TABLE IF EXISTS template_asset;
DROP TABLE IF EXISTS project_dictionary;
DROP TABLE IF EXISTS project_setting;
DROP TABLE IF EXISTS project_contributor;
DROP TABLE IF EXISTS project_revision;
DROP TABLE IF EXISTS allowable_trace;
DROP TABLE IF EXISTS reaction_detection_mechanism;
DROP TABLE IF EXISTS goal_label;
DROP TABLE IF EXISTS goal_definition;
DROP TABLE IF EXISTS goal_category;
DROP TABLE IF EXISTS goal_priority;
DROP TABLE IF EXISTS priority_type;
DROP TABLE IF EXISTS goal_fitcriterion;
DROP TABLE IF EXISTS goal_issue;
DROP TABLE IF EXISTS goalassociation;
DROP TABLE IF EXISTS goal_concernassociation;
DROP TABLE IF EXISTS task_concernassociation;
DROP TABLE IF EXISTS trace_dimension;
DROP TABLE IF EXISTS environment_goal;
DROP TABLE IF EXISTS environment_usecase;
DROP TABLE IF EXISTS response_goal;
DROP TABLE IF EXISTS requirement_role;
DROP TABLE IF EXISTS rolegoalrole_dependency;
DROP TABLE IF EXISTS roletaskrole_dependency;
DROP TABLE IF EXISTS roleassetrole_dependency;
DROP TABLE IF EXISTS goalgoal_goalassociation;
DROP TABLE IF EXISTS goalrequirement_goalassociation;
DROP TABLE IF EXISTS goaltask_goalassociation;
DROP TABLE IF EXISTS goalusecase_goalassociation;
DROP TABLE IF EXISTS requirementgoal_goalassociation;
DROP TABLE IF EXISTS requirementrequirement_goalassociation;
DROP TABLE IF EXISTS goalrole_goalassociation;
DROP TABLE IF EXISTS requirementrole_goalassociation;
DROP TABLE IF EXISTS responserole_goalassociation;
DROP TABLE IF EXISTS countermeasuretask_goalassociation;
DROP TABLE IF EXISTS goaldomainproperty_goalassociation;
DROP TABLE IF EXISTS goalobstacle_goalassociation;
DROP TABLE IF EXISTS domainpropertyobstacle_goalassociation;
DROP TABLE IF EXISTS obstacleobstacle_goalassociation;
DROP TABLE IF EXISTS obstaclegoal_goalassociation;
DROP TABLE IF EXISTS obstacledomainproperty_goalassociation;
DROP TABLE IF EXISTS obstaclerequirement_goalassociation;
DROP TABLE IF EXISTS requirementobstacle_goalassociation;
DROP TABLE IF EXISTS obstaclevulnerability_goalassociation;
DROP TABLE IF EXISTS obstaclethreat_goalassociation;
DROP TABLE IF EXISTS obstacletask_goalassociation;
DROP TABLE IF EXISTS obstacleusecase_goalassociation;
DROP TABLE IF EXISTS obstaclerole_goalassociation;
DROP TABLE IF EXISTS obstaclemisusecase_goalassociation;
DROP TABLE IF EXISTS goal_concern;
DROP TABLE IF EXISTS domainproperty_asset;
DROP TABLE IF EXISTS environment_obstacle;
DROP TABLE IF EXISTS obstacle_label;
DROP TABLE IF EXISTS obstacle_definition;
DROP TABLE IF EXISTS usecase_definition;
DROP TABLE IF EXISTS obstacle_category;
DROP TABLE IF EXISTS obstacle_concern;
DROP TABLE IF EXISTS requirement_task;
DROP TABLE IF EXISTS requirement_countermeasure;
DROP TABLE IF EXISTS requirement_vulnerability;
DROP TABLE IF EXISTS asset_requirement;
DROP TABLE IF EXISTS environment_requirement;
DROP TABLE IF EXISTS attributes;
DROP TABLE IF EXISTS task_persona;
DROP TABLE IF EXISTS task_narrative;
DROP TABLE IF EXISTS misusecase_narrative;
DROP TABLE IF EXISTS task_dependencies;
DROP TABLE IF EXISTS task_task;
DROP TABLE IF EXISTS task_asset;
DROP TABLE IF EXISTS usecase_asset;
DROP TABLE IF EXISTS task_vulnerability;
DROP TABLE IF EXISTS risk_vulnerability;
DROP TABLE IF EXISTS risk_threat;
DROP TABLE IF EXISTS misusecase_risk;
DROP TABLE IF EXISTS environment_task;
DROP TABLE IF EXISTS environment_misusecase;
DROP TABLE IF EXISTS countermeasure_task_persona;
DROP TABLE IF EXISTS countermeasure_task;
DROP TABLE IF EXISTS persona_role;
DROP TABLE IF EXISTS attacker_role;
DROP TABLE IF EXISTS environment_attacker;
DROP TABLE IF EXISTS environment_persona;
DROP TABLE IF EXISTS persona_characteristic_document;
DROP TABLE IF EXISTS persona_characteristic_asset;
DROP TABLE IF EXISTS persona_characteristic_attacker;
DROP TABLE IF EXISTS persona_characteristic_countermeasure;
DROP TABLE IF EXISTS persona_characteristic_domainproperty;
DROP TABLE IF EXISTS persona_characteristic_environment;
DROP TABLE IF EXISTS persona_characteristic_goal;
DROP TABLE IF EXISTS persona_characteristic_misusecase;
DROP TABLE IF EXISTS persona_characteristic_obstacle;
DROP TABLE IF EXISTS persona_characteristic_persona;
DROP TABLE IF EXISTS persona_characteristic_requirement;
DROP TABLE IF EXISTS persona_characteristic_response;
DROP TABLE IF EXISTS persona_characteristic_risk;
DROP TABLE IF EXISTS persona_characteristic_role;
DROP TABLE IF EXISTS persona_characteristic_task;
DROP TABLE IF EXISTS persona_characteristic_threat;
DROP TABLE IF EXISTS persona_characteristic_usecase;
DROP TABLE IF EXISTS persona_characteristic_vulnerability;
DROP TABLE IF EXISTS persona_characteristic;
DROP TABLE IF EXISTS task_characteristic_persona;
DROP TABLE IF EXISTS task_characteristic_usecase;
DROP TABLE IF EXISTS task_characteristic_document;
DROP TABLE IF EXISTS task_characteristic_requirement;
DROP TABLE IF EXISTS task_characteristic;
DROP TABLE IF EXISTS document_reference_requirement;
DROP TABLE IF EXISTS requirement_document_reference;
DROP TABLE IF EXISTS document_reference;
DROP TABLE IF EXISTS external_document;
DROP TABLE IF EXISTS asset_reference;
DROP TABLE IF EXISTS attacker_reference;
DROP TABLE IF EXISTS countermeasure_reference;
DROP TABLE IF EXISTS domainproperty_reference;
DROP TABLE IF EXISTS environment_reference;
DROP TABLE IF EXISTS goal_reference;
DROP TABLE IF EXISTS misusecase_reference;
DROP TABLE IF EXISTS obstacle_reference;
DROP TABLE IF EXISTS persona_reference;
DROP TABLE IF EXISTS requirement_reference;
DROP TABLE IF EXISTS response_reference;
DROP TABLE IF EXISTS risk_reference;
DROP TABLE IF EXISTS role_reference;
DROP TABLE IF EXISTS task_reference;
DROP TABLE IF EXISTS usecase_reference;
DROP TABLE IF EXISTS threat_reference;
DROP TABLE IF EXISTS vulnerability_reference;
DROP TABLE IF EXISTS behavioural_variable;
DROP TABLE IF EXISTS characteristic_reference_type;
DROP TABLE IF EXISTS domainproperty_task;
DROP TABLE IF EXISTS domainproperty;
DROP TABLE IF EXISTS domainproperty_type;
DROP TABLE IF EXISTS usecase_step_none_exception;
DROP TABLE IF EXISTS usecase_step_goal_exception;
DROP TABLE IF EXISTS usecase_step_requirement_exception;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS requirement_usecase;
DROP TABLE IF EXISTS requirement_requirement;
DROP TABLE IF EXISTS usecase_task;
DROP TABLE IF EXISTS component_usecase;
DROP TABLE IF EXISTS usecase_conditions;
DROP TABLE IF EXISTS usecase_step_tag;
DROP TABLE IF EXISTS usecase_step;
DROP TABLE IF EXISTS usecase_role;
DROP TABLE IF EXISTS usecase_property;
DROP TABLE IF EXISTS usecase_usecaseassociation;
DROP TABLE IF EXISTS usecase;
DROP TABLE IF EXISTS component;
DROP TABLE IF EXISTS reference_type;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS misusecase;
DROP TABLE IF EXISTS obstacle;
DROP TABLE IF EXISTS obstacle_category_type;
DROP TABLE IF EXISTS requirement;
DROP TABLE IF EXISTS requirement_type;
DROP TABLE IF EXISTS persona_direct;
DROP TABLE IF EXISTS persona_narrative;
DROP TABLE IF EXISTS persona;
DROP TABLE IF EXISTS persona_type;
DROP TABLE IF EXISTS response_role;
DROP TABLE IF EXISTS threat_attacker;
DROP TABLE IF EXISTS countermeasure_property;
DROP TABLE IF EXISTS mitigate_point;
DROP TABLE IF EXISTS environment_response;
DROP TABLE IF EXISTS environment_countermeasure;
DROP TABLE IF EXISTS countermeasure_cost;
DROP TABLE IF EXISTS response_description;
DROP TABLE IF EXISTS response_mitigate;
DROP TABLE IF EXISTS countermeasure_threat_target;
DROP TABLE IF EXISTS countermeasure_vulnerability_target;
DROP TABLE IF EXISTS target_effectiveness;
DROP TABLE IF EXISTS countermeasure_role;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS role_type;
DROP TABLE IF EXISTS countermeasure_asset;
DROP TABLE IF EXISTS countermeasure;
DROP TABLE IF EXISTS response_cost;
DROP TABLE IF EXISTS cost;
DROP TABLE IF EXISTS mitigate_type;
DROP TABLE IF EXISTS mitigate_point_type;
DROP TABLE IF EXISTS response;
DROP TABLE IF EXISTS goal_category_type;
DROP TABLE IF EXISTS risk;
DROP TABLE IF EXISTS score;
DROP TABLE IF EXISTS risk_class;
DROP TABLE IF EXISTS classassociation;
DROP TABLE IF EXISTS association_type;
DROP TABLE IF EXISTS multiplicity_type;
DROP TABLE IF EXISTS asset_threat;
DROP TABLE IF EXISTS asset_vulnerability;
DROP TABLE IF EXISTS threat_property;
DROP TABLE IF EXISTS environment_threat;
DROP TABLE IF EXISTS threat_directory;
DROP TABLE IF EXISTS threat_likelihood;
DROP TABLE IF EXISTS threat;
DROP TABLE IF EXISTS threat_type;
DROP TABLE IF EXISTS likelihood;
DROP TABLE IF EXISTS attacker_motivation;
DROP TABLE IF EXISTS attacker_capability;
DROP TABLE IF EXISTS motivation;
DROP TABLE IF EXISTS capability;
DROP TABLE IF EXISTS capability_value;
DROP TABLE IF EXISTS attacker;
DROP TABLE IF EXISTS environment_vulnerability;
DROP TABLE IF EXISTS vulnerability_directory;
DROP TABLE IF EXISTS vulnerability_severity;
DROP TABLE IF EXISTS vulnerability;
DROP TABLE IF EXISTS vulnerability_type;
DROP TABLE IF EXISTS severity;
DROP TABLE IF EXISTS asset_property;
DROP TABLE IF EXISTS environment_asset;
DROP TABLE IF EXISTS composite_environment_override;
DROP TABLE IF EXISTS composite_environment_property;
DROP TABLE IF EXISTS composite_environment;
DROP TABLE IF EXISTS duplicate_property;
DROP TABLE IF EXISTS asset;
DROP TABLE IF EXISTS access_right;
DROP TABLE IF EXISTS protocol;
DROP TABLE IF EXISTS privilege;
DROP TABLE IF EXISTS surface_type;
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS asset_type;
DROP TABLE IF EXISTS asset_value;
DROP TABLE IF EXISTS environment;
DROP TABLE IF EXISTS security_property;
DROP TABLE IF EXISTS security_property_value;
DROP TABLE IF EXISTS cognitive_attribute;
DROP TABLE IF EXISTS cognitive_attribute_value;
DROP TABLE IF EXISTS securityusability_property_value;
DROP TABLE IF EXISTS countermeasure_value;
DROP TABLE IF EXISTS threat_value;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS version;
DROP TABLE IF EXISTS image;

CREATE TABLE version(
  major INT NOT NULL,
  minor INT NOT NULL,
  patch INT NOT NULL,
  PRIMARY KEY(major,minor,patch)
) ENGINE=INNODB;
CREATE TABLE trace_dimension(
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE allowable_trace(
  from_dim INT NOT NULL,
  to_dim INT NOT NULL,
  PRIMARY KEY(from_dim,to_dim),
  FOREIGN KEY (from_dim) REFERENCES trace_dimension(id),
  FOREIGN KEY (to_dim) REFERENCES trace_dimension(id)
) ENGINE=INNODB;
CREATE TABLE project_dictionary (
  name VARCHAR(100) NOT NULL,
  description VARCHAR(4000) NOT NULL
) ENGINE=INNODB;
CREATE TABLE project_setting (
  id INT NOT NULL,
  name VARCHAR(100),
  description VARCHAR(4000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE project_contributor (
  firstname VARCHAR(100) NOT NULL,
  surname VARCHAR(100) NOT NULL,
  affiliation VARCHAR(100) NOT NULL,
  role VARCHAR(50) NOT NULL
) ENGINE=INNODB;
CREATE TABLE project_revision (
  revision_no INT NOT NULL,
  revision_date VARCHAR(50) NOT NULL,
  revision_remarks VARCHAR(1000) NOT NULL,
  PRIMARY KEY (revision_no)
) ENGINE=INNODB;
CREATE TABLE countermeasure_value (
  id INT NOT NULL, 
  name VARCHAR(50), 
  description VARCHAR(4000), 
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE threat_value (
  id INT NOT NULL, 
  name VARCHAR(200), 
  description VARCHAR(4000), 
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE environment(
  id INT NOT NULL, 
  name VARCHAR(100), 
  description VARCHAR(4000), 
  short_code VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE tension (
  id INT NOT NULL, 
  name VARCHAR(50), 
  description VARCHAR(4000), 
  short_code VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE asset_value (
  id INT NOT NULL, 
  name VARCHAR(100), 
  description VARCHAR(4000), 
  environment_id INT NOT NULL,
  PRIMARY KEY(id,environment_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE duplicate_property (
  id INT NOT NULL,
  name VARCHAR(50),
  PRIMARY KEY(id)
) ENGINE=INNODB; 
CREATE TABLE composite_environment_override (
  composite_environment_id INT NOT NULL,
  overriding_environment_id INT NOT NULL,
  PRIMARY KEY(composite_environment_id,overriding_environment_id),
  FOREIGN KEY(composite_environment_id) REFERENCES environment(id),
  FOREIGN KEY(overriding_environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE composite_environment (
  composite_environment_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(composite_environment_id,environment_id),
  FOREIGN KEY(composite_environment_id) REFERENCES environment(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE composite_environment_property (
  composite_environment_id INT NOT NULL,
  duplicate_property_id INT NOT NULL,
  PRIMARY KEY(composite_environment_id,duplicate_property_id),
  FOREIGN KEY(composite_environment_id) REFERENCES composite_environment(composite_environment_id),
  FOREIGN KEY(duplicate_property_id) REFERENCES duplicate_property(id)
) ENGINE=INNODB;
CREATE TABLE requirement_type (
  id INT NOT NULL,
  name VARCHAR(50),
  PRIMARY KEY (id)
) ENGINE=INNODB;
CREATE TABLE requirement(
  id INT NOT NULL,
  type INT NOT NULL,
  version INT NOT NULL,
  label INT NOT NULL,
  name LONGTEXT,
  description LONGTEXT,
  rationale LONGTEXT NOT NULL,
  originator LONGTEXT,
  fit_criterion LONGTEXT NOT NULL,
  priority INT NOT NULL,
  supporting_material LONGTEXT,
  update_date VARCHAR(20),
  PRIMARY KEY(id,version),
  FOREIGN KEY (type) REFERENCES requirement_type(id)
) ENGINE=INNODB;
CREATE TABLE environment_requirement (
  requirement_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(requirement_id,environment_id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE attributes (
  id INT,
  name VARCHAR(50)
) ENGINE=MYISAM;
CREATE TABLE severity (
  id INT,
  name VARCHAR(50),
  description VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE attacker (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(4000),
  image VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE motivation (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(4000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE attacker_motivation (
  attacker_id INT NOT NULL,
  motivation_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(attacker_id,motivation_id,environment_id),
  FOREIGN KEY(attacker_id) REFERENCES attacker(id),
  FOREIGN KEY(motivation_id) REFERENCES motivation(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE capability (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(4000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE capability_value (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE attacker_capability (
  attacker_id INT NOT NULL,
  capability_id INT NOT NULL,
  capability_value_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(attacker_id,capability_id,environment_id),
  FOREIGN KEY(attacker_id) REFERENCES attacker(id),
  FOREIGN KEY(capability_id) REFERENCES capability(id),
  FOREIGN KEY(capability_value_id) REFERENCES capability_value(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE environment_attacker (
  attacker_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(attacker_id,environment_id),
  FOREIGN KEY(attacker_id) REFERENCES attacker(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE security_property (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE security_property_value (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB; 
CREATE TABLE cognitive_attribute (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE cognitive_attribute_value (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE securityusability_property_value (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB; 
CREATE TABLE asset_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE asset (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  short_code VARCHAR(100) NOT NULL,
  description VARCHAR(1000),
  significance VARCHAR(1000),
  asset_type_id INT NOT NULL,
  is_critical INT NOT NULL,
  critical_rationale VARCHAR(1000),
  PRIMARY KEY(id),
  FOREIGN KEY(asset_type_id) REFERENCES asset_type(id)
) ENGINE=INNODB;
CREATE TABLE asset_property(
  asset_id INT NOT NULL,
  environment_id INT NOT NULL,
  property_id INT NOT NULL,
  property_value_id INT NOT NULL,
  property_rationale varchar(4000),
  PRIMARY KEY(asset_id,environment_id,property_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(property_id) REFERENCES security_property(id),
  FOREIGN KEY(property_value_id) REFERENCES security_property_value(id)
) ENGINE=INNODB;
CREATE TABLE asset_requirement (
  asset_id INT NOT NULL,
  requirement_id INT NOT NULL,
  PRIMARY KEY(asset_id,requirement_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id)
) ENGINE=INNODB;
CREATE TABLE association_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE multiplicity_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
 CREATE TABLE classassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  head_id INT NOT NULL,
  head_association_type_id INT NOT NULL,
  head_multiplicity_id INT NOT NULL,
  head_role_name VARCHAR(50) NOT NULL,
  tail_role_name VARCHAR(50) NOT NULL,
  tail_multiplicity_id INT NOT NULL,
  tail_association_type_id INT NOT NULL,
  tail_id INT NOT NULL,
  head_navigation INT NOT NULL default 0,
  tail_navigation INT NOT NULL default 0,
  rationale LONGTEXT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(head_id) REFERENCES asset(id),
  FOREIGN KEY(head_association_type_id) REFERENCES association_type(id),
  FOREIGN KEY(head_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(tail_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(tail_association_type_id) REFERENCES association_type(id),
  FOREIGN KEY(tail_id) REFERENCES asset(id)
) ENGINE=INNODB;
CREATE TABLE environment_asset (
  asset_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(asset_id,environment_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE likelihood (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE threat_type (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(4000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE threat (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  threat_type_id INT NOT NULL,
  method TEXT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(threat_type_id) REFERENCES threat_type(id)
) ENGINE=INNODB;
CREATE TABLE threat_directory (
  id INT NOT NULL,
  label VARCHAR(200) NOT NULL,
  name VARCHAR(200) NOT NULL,
  description TEXT NOT NULL,
  threat_type_id INT NOT NULL,
  reference VARCHAR(100) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(threat_type_id) REFERENCES threat_type(id)
) ENGINE=INNODB;
CREATE TABLE threat_likelihood (
  threat_id INT NOT NULL,
  environment_id INT NOT NULL,
  likelihood_id INT NOT NULL,
  PRIMARY KEY(threat_id,environment_id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(likelihood_id) REFERENCES likelihood(id)
) ENGINE=INNODB;
CREATE TABLE asset_threat (
  asset_id INT NOT NULL,
  threat_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(asset_id,threat_id,environment_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE environment_threat (
  threat_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(threat_id,environment_id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE threat_property (
  threat_id INT NOT NULL,
  environment_id INT NOT NULL,
  property_id INT NOT NULL,
  property_value_id INT NOT NULL,
  property_rationale varchar(4000),
  PRIMARY KEY(threat_id,environment_id,property_id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(property_id) REFERENCES security_property(id),
  FOREIGN KEY(property_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE vulnerability_type (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(4000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE vulnerability (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  vulnerability_type_id INT NOT NULL,
  description VARCHAR(4000),
  PRIMARY KEY(id),
  FOREIGN KEY(vulnerability_type_id) REFERENCES vulnerability_type(id)
) ENGINE=INNODB;
CREATE TABLE vulnerability_directory (
  id INT NOT NULL,
  label VARCHAR(200) NOT NULL,
  name VARCHAR(200) NOT NULL,
  description VARCHAR(4000) NOT NULL,
  vulnerability_type_id INT NOT NULL,
  reference VARCHAR(100) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(vulnerability_type_id) REFERENCES vulnerability_type(id)
) ENGINE=INNODB;
CREATE TABLE environment_vulnerability (
  vulnerability_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(vulnerability_id,environment_id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB; 
CREATE TABLE requirement_vulnerability (
  requirement_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  PRIMARY KEY(requirement_id,vulnerability_id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id)
) ENGINE=INNODB; 
CREATE TABLE vulnerability_severity (
  vulnerability_id INT NOT NULL,
  severity_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(vulnerability_id,severity_id,environment_id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id),
  FOREIGN KEY(severity_id) REFERENCES severity(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE asset_vulnerability (
  asset_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(asset_id,vulnerability_id,environment_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB; 
CREATE TABLE persona_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE persona (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  activities text NOT NULL,
  attitudes text NOT NULL,
  aptitudes text NOT NULL,
  motivations text NOT NULL,
  skills text NOT NULL,
  intrinsic text NOT NULL,
  contextual text NOT NULL,
  image VARCHAR(1000),
  assumption_id INT NOT NULL,
  persona_type_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_type_id) REFERENCES persona_type(id)
) ENGINE=INNODB; 
CREATE TABLE behavioural_variable (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE characteristic_reference_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE external_document (
  id INT NOT NULL,
  name VARCHAR(2000) NOT NULL,
  version VARCHAR(20),
  publication_date VARCHAR(100),
  authors VARCHAR(2000),
  description VARCHAR(2000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE document_reference (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  document_id INT NOT NULL,
  contributor VARCHAR(200) NOT NULL,
  excerpt VARCHAR(2000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(document_id) REFERENCES external_document(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic (
  id INT NOT NULL,
  persona_id INT NOT NULL,
  variable_id INT NOT NULL,
  qualifier varchar(100) NOT NULL,
  description varchar(2000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(variable_id) REFERENCES behavioural_variable(id)
) ENGINE=INNODB;
CREATE TABLE persona_direct (
  persona_id INT NOT NULL,
  environment_id INT NOT NULL,
  direct_flag BOOL NOT NULL,
  PRIMARY KEY(persona_id,environment_id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE persona_narrative (
  persona_id INT NOT NULL,
  environment_id INT NOT NULL,
  narrative VARCHAR(4000),
  PRIMARY KEY(persona_id,environment_id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE environment_persona (
  persona_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(persona_id,environment_id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE role_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE role (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  role_type_id INT NOT NULL,
  short_code VARCHAR(100) NOT NULL,
  description VARCHAR(1000),
  PRIMARY KEY(id),
  FOREIGN KEY(role_type_id) REFERENCES role_type(id)
) ENGINE=INNODB; 
CREATE TABLE persona_role (
  persona_id INT NOT NULL,
  role_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(persona_id,role_id,environment_id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(role_id) REFERENCES role(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB; 
CREATE TABLE attacker_role (
  attacker_id INT NOT NULL,
  role_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(attacker_id,role_id,environment_id),
  FOREIGN KEY(attacker_id) REFERENCES attacker(id),
  FOREIGN KEY(role_id) REFERENCES role(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB; 
CREATE TABLE threat_attacker (
  threat_id INT NOT NULL,
  attacker_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(threat_id,attacker_id,environment_id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(attacker_id) REFERENCES attacker(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE reference_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE task (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  short_code VARCHAR(100) NOT NULL,
  objective VARCHAR(2000) NOT NULL,
  assumption_id INT NOT NULL,
  author VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE task_characteristic (
  id INT NOT NULL,
  task_id INT NOT NULL,
  qualifier varchar(100) NOT NULL,
  description varchar(2000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(task_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE usecase (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  short_code VARCHAR(100) NOT NULL,
  author VARCHAR(255) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE usecase_property(
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  property_id INT NOT NULL,
  property_value_id INT NOT NULL,
  property_rationale varchar(4000),
  PRIMARY KEY(usecase_id,environment_id,property_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(property_id) REFERENCES cognitive_attribute(id),
  FOREIGN KEY(property_value_id) REFERENCES cognitive_attribute_value(id)
) ENGINE=INNODB;
CREATE TABLE requirement_requirement (
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  label VARCHAR(255),
  PRIMARY KEY(from_id,to_id,label),
  FOREIGN KEY(from_id) REFERENCES requirement(id),
  FOREIGN KEY(to_id) REFERENCES requirement(id)
) ENGINE=INNODB;
CREATE TABLE document_reference_requirement (
  document_reference_id INT NOT NULL,
  requirement_id INT NOT NULL,
  PRIMARY KEY(requirement_id,document_reference_id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id),
  FOREIGN KEY(document_reference_id) REFERENCES document_reference(id)
) ENGINE=INNODB;
CREATE TABLE requirement_document_reference (
  requirement_id INT NOT NULL,
  document_reference_id INT NOT NULL,
  PRIMARY KEY(document_reference_id,requirement_id),
  FOREIGN KEY(document_reference_id) REFERENCES document_reference(id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id)
) ENGINE=INNODB;
CREATE TABLE requirement_usecase (
  requirement_id INT NOT NULL,
  usecase_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  PRIMARY KEY(requirement_id,usecase_id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id)
) ENGINE=INNODB;
CREATE TABLE usecase_task (
  usecase_id INT NOT NULL,
  task_id INT NOT NULL,
  PRIMARY KEY(usecase_id,task_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(task_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE usecase_role (
  usecase_id INT NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY(usecase_id,role_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(role_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE usecase_conditions (
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  preconditions VARCHAR(2000) NOT NULL,
  postconditions VARCHAR(2000) NOT NULL,
  PRIMARY KEY(usecase_id,environment_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE usecase_step (
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  step_no INT NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(usecase_id,environment_id,step_no),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;


CREATE TABLE misusecase (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE task_persona (
  task_id INT NOT NULL,
  environment_id INT NOT NULL,
  persona_id INT NOT NULL,
  duration_id INT NOT NULL,
  frequency_id INT NOT NULL,
  demands_id INT NOT NULL,
  goalsupport_id INT NOT NULL,
  PRIMARY KEY(task_id,environment_id,persona_id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(duration_id) REFERENCES security_property_value(id),
  FOREIGN KEY(frequency_id) REFERENCES security_property_value(id),
  FOREIGN KEY(demands_id) REFERENCES security_property_value(id),
  FOREIGN KEY(goalsupport_id) REFERENCES security_property_value(id)
) ENGINE=INNODB;
CREATE TABLE task_narrative (
  task_id INT NOT NULL,
  environment_id INT NOT NULL,
  narrative VARCHAR(5000) NOT NULL,
  benefits VARCHAR(4000) NOT NULL,
  consequences VARCHAR(4000) NOT NULL,
  PRIMARY KEY(task_id,environment_id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE misusecase_narrative (
  misusecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  narrative VARCHAR(5000) NOT NULL,
  PRIMARY KEY(misusecase_id,environment_id),
  FOREIGN KEY(misusecase_id) REFERENCES misusecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE task_dependencies (
  task_id INT NOT NULL,
  environment_id INT NOT NULL,
  dependencies VARCHAR(4000) NOT NULL,
  PRIMARY KEY(task_id,environment_id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE requirement_task (
  requirement_id INT NOT NULL,
  task_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  PRIMARY KEY(requirement_id,task_id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id)
) ENGINE=INNODB;
CREATE TABLE task_task (
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  PRIMARY KEY(from_id,to_id),
  FOREIGN KEY(from_id) REFERENCES task(id),
  FOREIGN KEY(to_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE task_asset (
  task_id INT NOT NULL,
  asset_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(task_id,asset_id,environment_id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE usecase_asset (
  usecase_id INT NOT NULL,
  asset_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(usecase_id,asset_id,environment_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE task_vulnerability (
  task_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  PRIMARY KEY(task_id,vulnerability_id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id)
) ENGINE=INNODB;
CREATE TABLE environment_task (
  environment_id INT NOT NULL,
  task_id INT NOT NULL,
  PRIMARY KEY(environment_id,task_id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE environment_usecase (
  environment_id INT NOT NULL,
  usecase_id INT NOT NULL,
  PRIMARY KEY(environment_id,usecase_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE environment_misusecase (
  environment_id INT NOT NULL,
  misusecase_id INT NOT NULL,
  PRIMARY KEY(environment_id,misusecase_id),
  FOREIGN KEY(misusecase_id) REFERENCES misusecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE risk_class(
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(2000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE score (
  likelihood_id INT NOT NULL,
  severity_id INT NOT NULL,
  class_id INT NOT NULL,
  PRIMARY KEY(likelihood_id,severity_id),
  FOREIGN KEY (likelihood_id) REFERENCES likelihood(id),
  FOREIGN KEY (severity_id) REFERENCES severity(id),
  FOREIGN KEY (class_id) REFERENCES risk_class(id)
) ENGINE=INNODB;
CREATE TABLE risk (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  threat_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  intent VARCHAR(4000) DEFAULT '',
  PRIMARY KEY(id,threat_id,vulnerability_id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id)
) ENGINE=INNODB;
CREATE TABLE misusecase_risk (
  misusecase_id INT NOT NULL,
  risk_id INT NOT NULL,
  PRIMARY KEY(misusecase_id,risk_id),
  FOREIGN KEY(misusecase_id) REFERENCES misusecase(id),
  FOREIGN KEY(risk_id) REFERENCES risk(id)
) ENGINE=INNODB;
CREATE TABLE cost (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE goal_category_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE mitigate_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE mitigate_point_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE response ( 
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  goal_category_type_id INT NOT NULL,
  risk_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(goal_category_type_id) REFERENCES goal_category_type(id),
  FOREIGN KEY(risk_id) REFERENCES risk(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure ( 
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL,
  countermeasure_type_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(countermeasure_type_id) REFERENCES asset_type(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_asset ( 
  countermeasure_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,asset_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id)
) ENGINE=INNODB;
CREATE TABLE requirement_countermeasure ( 
  requirement_id INT NOT NULL,
  environment_id INT NOT NULL,
  countermeasure_id INT NOT NULL,
  PRIMARY KEY(requirement_id,environment_id,countermeasure_id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_cost (
  countermeasure_id INT NOT NULL,
  environment_id INT NOT NULL,
  cost_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,environment_id,cost_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(cost_id) REFERENCES cost(id)
) ENGINE=INNODB;
CREATE TABLE response_cost (
  response_id INT NOT NULL,
  environment_id INT NOT NULL,
  cost_id INT NOT NULL,
  PRIMARY KEY(response_id,environment_id,cost_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(cost_id) REFERENCES cost(id)
) ENGINE=INNODB;
CREATE TABLE response_description (
  response_id INT NOT NULL,
  environment_id INT NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY(response_id,environment_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE response_mitigate (
  response_id INT NOT NULL,
  environment_id INT NOT NULL,
  mitigate_type_id INT NOT NULL,
  PRIMARY KEY(response_id,environment_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(mitigate_type_id) REFERENCES mitigate_type(id)
) ENGINE=INNODB;
CREATE TABLE response_role (
  response_id INT NOT NULL,
  environment_id INT NOT NULL,
  role_id INT NOT NULL,
  cost_id INT NOT NULL,
  PRIMARY KEY(response_id,environment_id,role_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(role_id) REFERENCES role(id),
  FOREIGN KEY(cost_id) REFERENCES cost(id)
) ENGINE=INNODB; 
CREATE TABLE reaction_detection_mechanism (
  response_id INT NOT NULL,
  environment_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(response_id,environment_id,asset_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_property (
  countermeasure_id INT NOT NULL,
  environment_id INT NOT NULL,
  property_id INT NOT NULL,
  property_value_id INT NOT NULL,
  property_rationale varchar(4000),
  PRIMARY KEY(countermeasure_id,environment_id,property_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(property_id) REFERENCES security_property(id),
  FOREIGN KEY(property_value_id) REFERENCES security_property_value(id)
) ENGINE=INNODB;
CREATE TABLE target_effectiveness (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_threat_target (
  countermeasure_id INT NOT NULL,
  threat_id INT NOT NULL,
  effectiveness_id INT NOT NULL,
  environment_id INT NOT NULL,
  effectiveness_rationale VARCHAR(4000),
  PRIMARY KEY(countermeasure_id,threat_id,environment_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(effectiveness_id) REFERENCES target_effectiveness(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_vulnerability_target (
  countermeasure_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  effectiveness_id INT NOT NULL,
  environment_id INT NOT NULL,
  effectiveness_rationale VARCHAR(4000),
  PRIMARY KEY(countermeasure_id,vulnerability_id,environment_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id),
  FOREIGN KEY(effectiveness_id) REFERENCES target_effectiveness(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;

CREATE TABLE countermeasure_role (
  countermeasure_id INT NOT NULL,
  environment_id INT NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,environment_id,role_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(role_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_task (
  countermeasure_id INT NOT NULL,
  task_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,task_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(task_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_task_persona (
  countermeasure_id INT NOT NULL,
  environment_id INT NOT NULL,
  task_id INT NOT NULL,
  persona_id INT NOT NULL,
  duration_id INT NOT NULL,
  frequency_id INT NOT NULL,
  demands_id INT NOT NULL,
  goalsupport_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,environment_id,task_id,persona_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(duration_id) REFERENCES securityusability_property_value(id),
  FOREIGN KEY(frequency_id) REFERENCES securityusability_property_value(id),
  FOREIGN KEY(demands_id) REFERENCES securityusability_property_value(id),
  FOREIGN KEY(goalsupport_id) REFERENCES securityusability_property_value(id)
) ENGINE=INNODB;
CREATE TABLE mitigate_point (
  response_id INT NOT NULL,
  environment_id INT NOT NULL,
  mitigate_point_type_id INT NOT NULL,
  PRIMARY KEY(response_id,environment_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(mitigate_point_type_id) REFERENCES mitigate_point_type(id)
) ENGINE=INNODB;
CREATE TABLE environment_response (
  response_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(response_id,environment_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE environment_countermeasure (
  countermeasure_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,environment_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE domainproperty_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  primary KEY(id)
) ENGINE=INNODB;
CREATE TABLE obstacle (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  originator VARCHAR(100) NOT NULL,
  primary KEY(id)
) ENGINE=INNODB;
CREATE TABLE obstacle_category_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE obstacle_label (
  obstacle_id INT NOT NULL,
  environment_id INT NOT NULL,
  label VARCHAR(255) NOT NULL,
  PRIMARY KEY(obstacle_id,environment_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE obstacle_definition (
  obstacle_id INT NOT NULL,
  environment_id INT NOT NULL,
  definition VARCHAR(1000) NOT NULL,
  probability FLOAT DEFAULT 0.0,
  rationale VARCHAR (4000) DEFAULT 'None',
  PRIMARY KEY(obstacle_id,environment_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE usecase_definition (
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  average FLOAT DEFAULT 0,
  PRIMARY KEY(usecase_id,environment_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE obstacle_category (
  obstacle_id INT NOT NULL,
  environment_id INT NOT NULL,
  obstacle_category_type_id INT NOT NULL,
  PRIMARY KEY(obstacle_id,environment_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(obstacle_category_type_id) REFERENCES obstacle_category_type(id)
) ENGINE=INNODB;
CREATE TABLE obstacle_concern (
  obstacle_id INT NOT NULL,
  environment_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(obstacle_id,environment_id,asset_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id)
) ENGINE=INNODB;
CREATE TABLE environment_obstacle (
  obstacle_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(obstacle_id,environment_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE domainproperty (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(1000) NOT NULL,
  domainproperty_type_id INT NOT NULL,
  originator VARCHAR(100) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(domainproperty_type_id) REFERENCES domainproperty_type(id)
) ENGINE=INNODB;
CREATE TABLE domainproperty_task (
  domainproperty_id INT NOT NULL,
  task_id INT NOT NULL,
  PRIMARY KEY(domainproperty_id,task_id),
  FOREIGN KEY(domainproperty_id) REFERENCES domainproperty(id),
  FOREIGN KEY(task_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE domainproperty_asset (
  domainproperty_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(domainproperty_id,asset_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(domainproperty_id) REFERENCES domainproperty(id)
) ENGINE=INNODB;
CREATE TABLE goal (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  originator VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE response_goal(
  response_id INT NOT NULL,
  goal_id INT NOT NULL,
  PRIMARY KEY(response_id,goal_id),
  FOREIGN KEY(response_id) REFERENCES response(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id)
) ENGINE=INNODB;
CREATE TABLE requirement_role(
  requirement_id INT NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY(requirement_id,role_id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id),
  FOREIGN KEY(role_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE environment_goal (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  PRIMARY KEY(goal_id,environment_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE goal_label (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  label VARCHAR(255) NOT NULL,
  PRIMARY KEY(goal_id,environment_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE goal_definition (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  definition VARCHAR(4000) NOT NULL,
  PRIMARY KEY(goal_id,environment_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE goal_category (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY(goal_id,environment_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(category_id) REFERENCES goal_category_type(id)
) ENGINE=INNODB;
CREATE TABLE priority_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE goal_priority (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  priority_id INT NOT NULL,
  PRIMARY KEY(goal_id,environment_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(priority_id) REFERENCES priority_type(id)
) ENGINE=INNODB;
CREATE TABLE goal_fitcriterion (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  fitcriterion VARCHAR(1000) NOT NULL,
  PRIMARY KEY(goal_id,environment_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE goal_issue (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  issue VARCHAR(1000) NOT NULL,
  PRIMARY KEY(goal_id,environment_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE goalgoal_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES goal(id)
) ENGINE=INNODB;
CREATE TABLE usecase_usecaseassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  usecase_id INT NOT NULL,
  subUsecase_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(subUsecase_id) REFERENCES usecase(id)
) ENGINE=INNODB;
CREATE TABLE goalrequirement_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES requirement(id)
) ENGINE=INNODB;
CREATE TABLE goaltask_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE goalusecase_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES usecase(id)
) ENGINE=INNODB;
CREATE TABLE obstaclemisusecase_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES misusecase(id)
) ENGINE=INNODB;
CREATE TABLE requirementgoal_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES requirement(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES goal(id)
) ENGINE=INNODB;
CREATE TABLE requirementrequirement_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES requirement(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES requirement(id)
) ENGINE=INNODB;
CREATE TABLE goalrole_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE requirementrole_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES requirement(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE responserole_goalassociation (
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  cost_id INT NOT NULL,
  PRIMARY KEY(goal_id,subgoal_id,environment_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES response(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES role(id),
  FOREIGN KEY(cost_id) REFERENCES cost(id)
) ENGINE=INNODB;
CREATE TABLE countermeasuretask_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES countermeasure(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE goaldomainproperty_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES domainproperty(id)
) ENGINE=INNODB;
CREATE TABLE goalobstacle_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES obstacle(id)
) ENGINE=INNODB;
CREATE TABLE domainpropertyobstacle_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES domainproperty(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES obstacle(id)
) ENGINE=INNODB;
CREATE TABLE obstacleobstacle_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES obstacle(id)
) ENGINE=INNODB;
CREATE TABLE obstaclegoal_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES goal(id)
) ENGINE=INNODB;
CREATE TABLE obstacledomainproperty_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES domainproperty(id)
) ENGINE=INNODB;
CREATE TABLE obstaclerequirement_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES requirement(id)
) ENGINE=INNODB;
CREATE TABLE requirementobstacle_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES requirement(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES obstacle(id)
) ENGINE=INNODB;
CREATE TABLE obstaclethreat_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES threat(id)
) ENGINE=INNODB;
CREATE TABLE obstaclevulnerability_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES vulnerability(id)
) ENGINE=INNODB;
CREATE TABLE obstacletask_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE obstacleusecase_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES usecase(id)
) ENGINE=INNODB;
CREATE TABLE obstaclerole_goalassociation (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  alternative_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES obstacle(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE goal_concernassociation (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  source_id INT NOT NULL,
  source_multiplicity_id INT NOT NULL,
  link VARCHAR(100)  NOT NULL,
  target_id INT NOT NULL,
  target_multiplicity_id INT NOT NULL,
  PRIMARY KEY(goal_id,environment_id,source_id,target_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(source_id) REFERENCES asset(id),
  FOREIGN KEY(target_id) REFERENCES asset(id),
  FOREIGN KEY(source_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(target_multiplicity_id) REFERENCES multiplicity_type(id)
) ENGINE=INNODB;
CREATE TABLE task_concernassociation (
  task_id INT NOT NULL,
  environment_id INT NOT NULL,
  source_id INT NOT NULL,
  source_multiplicity_id INT NOT NULL,
  link VARCHAR(100)  NOT NULL,
  target_id INT NOT NULL,
  target_multiplicity_id INT NOT NULL,
  PRIMARY KEY(task_id,environment_id,source_id,target_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(source_id) REFERENCES asset(id),
  FOREIGN KEY(target_id) REFERENCES asset(id),
  FOREIGN KEY(source_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(target_multiplicity_id) REFERENCES multiplicity_type(id)
) ENGINE=INNODB;
CREATE TABLE goal_concern (
  goal_id INT NOT NULL,
  environment_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(goal_id,environment_id,asset_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id)
) ENGINE=INNODB;
CREATE TABLE rolegoalrole_dependency (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  depender_id INT NOT NULL,
  dependency_id INT NOT NULL, 
  dependee_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id,environment_id,depender_id,dependency_id,dependee_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(depender_id) REFERENCES role(id),
  FOREIGN KEY(dependency_id) REFERENCES goal(id),
  FOREIGN KEY(dependee_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE roletaskrole_dependency (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  depender_id INT NOT NULL,
  dependency_id INT NOT NULL, 
  dependee_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id,environment_id,depender_id,dependency_id,dependee_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(depender_id) REFERENCES role(id),
  FOREIGN KEY(dependency_id) REFERENCES task(id),
  FOREIGN KEY(dependee_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE roleassetrole_dependency (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  depender_id INT NOT NULL,
  dependency_id INT NOT NULL,
  dependee_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(id,environment_id,depender_id,dependency_id,dependee_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(depender_id) REFERENCES role(id),
  FOREIGN KEY(dependency_id) REFERENCES asset(id),
  FOREIGN KEY(dependee_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE access_right (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(1000),
  value INT NOT NULL,
  rationale VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE protocol (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(1000),
  value INT NOT NULL,
  rationale VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE privilege (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(1000),
  value INT NOT NULL,
  rationale VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE surface_type (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  description VARCHAR(1000),
  value INT NOT NULL,
  rationale VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE template_asset (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  short_code VARCHAR(100) NOT NULL,
  description VARCHAR(1000),
  significance VARCHAR(1000),
  asset_type_id INT NOT NULL,
  surface_type_id INT NOT NULL,
  access_right_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(asset_type_id) REFERENCES asset_type(id),
  FOREIGN KEY(surface_type_id) REFERENCES surface_type(id),
  FOREIGN KEY(access_right_id) REFERENCES access_right(id)
) ENGINE=INNODB;
CREATE TABLE template_asset_property (
  template_asset_id INT NOT NULL,
  property_id INT NOT NULL,
  property_value_id INT NOT NULL,
  property_rationale varchar(4000),
  PRIMARY KEY(template_asset_id,property_id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id),
  FOREIGN KEY(property_id) REFERENCES security_property(id),
  FOREIGN KEY(property_value_id) REFERENCES security_property_value(id)
) ENGINE=INNODB;
CREATE TABLE securitypattern (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  context VARCHAR(4000) NOT NULL,
  problem VARCHAR(4000) NOT NULL,
  solution VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE template_requirement(
  id INT NOT NULL,
  name VARCHAR(255),
  type_id INT NOT NULL,
  description VARCHAR(4000),
  rationale VARCHAR(255) NOT NULL,
  fit_criterion VARCHAR(4000) NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (type_id) REFERENCES requirement_type(id),
  FOREIGN KEY (asset_id) REFERENCES template_asset(id)
) ENGINE=INNODB;
CREATE TABLE template_goal(
  id INT NOT NULL,
  name VARCHAR(255),
  definition VARCHAR(4000),
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=INNODB;
CREATE TABLE template_goal_concern (
  template_goal_id INT NOT NULL,
  template_asset_id INT NOT NULL,
  PRIMARY KEY(template_goal_id,template_asset_id),
  FOREIGN KEY(template_goal_id) REFERENCES template_goal(id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id)
) ENGINE=INNODB;
CREATE TABLE template_goal_responsibility (
  template_goal_id INT NOT NULL,
  role_id INT NOT NULL,
  PRIMARY KEY(template_goal_id,role_id),
  FOREIGN KEY(template_goal_id) REFERENCES template_goal(id),
  FOREIGN KEY(role_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE securitypattern_template_requirement (
  template_requirement_id INT NOT NULL,
  pattern_id INT NOT NULL,
  label INT NOT NULL,
  PRIMARY KEY(template_requirement_id,pattern_id),
  FOREIGN KEY (pattern_id) REFERENCES securitypattern(id),
  FOREIGN KEY (template_requirement_id) REFERENCES template_requirement(id)
) ENGINE=INNODB;


CREATE TABLE securitypattern_classassociation (
  id INT NOT NULL,
  pattern_id INT NOT NULL,
  head_id INT NOT NULL,
  head_association_type_id INT NOT NULL,
  head_multiplicity_id INT NOT NULL,
  head_role_name VARCHAR(50) NOT NULL,
  tail_role_name VARCHAR(50) NOT NULL,
  tail_multiplicity_id INT NOT NULL,
  tail_association_type_id INT NOT NULL,
  tail_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(pattern_id) REFERENCES securitypattern(id),
  FOREIGN KEY(head_id) REFERENCES template_asset(id),
  FOREIGN KEY(head_association_type_id) REFERENCES association_type(id),
  FOREIGN KEY(head_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(tail_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(tail_association_type_id) REFERENCES association_type(id),
  FOREIGN KEY(tail_id) REFERENCES template_asset(id)
) ENGINE=INNODB;
CREATE TABLE securitypattern_asset_template_asset (
  asset_id INT NOT NULL,
  template_asset_id INT NOT NULL,
  pattern_id INT NOT NULL,
  PRIMARY KEY(asset_id,template_asset_id,pattern_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id),
  FOREIGN KEY(pattern_id) REFERENCES securitypattern(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_securitypattern ( 
  countermeasure_id INT NOT NULL,
  pattern_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,pattern_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(pattern_id) REFERENCES securitypattern(id)
) ENGINE=INNODB;
CREATE TABLE vulnerability_asset_countermeasure_effect (
  vulnerability_id INT NOT NULL,
  asset_id INT NOT NULL,
  environment_id INT NOT NULL,
  countermeasure_id INT NOT NULL,
  effectiveness_id INT NOT NULL,
  PRIMARY KEY(vulnerability_id,asset_id,environment_id,countermeasure_id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(effectiveness_id) REFERENCES target_effectiveness(id) 
) ENGINE=INNODB;
CREATE TABLE threat_asset_countermeasure_effect (
  threat_id INT NOT NULL,
  asset_id INT NOT NULL,
  environment_id INT NOT NULL,
  countermeasure_id INT NOT NULL,
  effectiveness_id INT NOT NULL,
  PRIMARY KEY(threat_id,asset_id,environment_id,countermeasure_id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id),
  FOREIGN KEY(effectiveness_id) REFERENCES target_effectiveness(id) 
) ENGINE=INNODB;
CREATE TABLE asset_reference (
  id INT NOT NULL,
  asset_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id)
) ENGINE=INNODB;
CREATE TABLE attacker_reference (
  id INT NOT NULL,
  attacker_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(attacker_id) REFERENCES attacker(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure_reference (
  id INT NOT NULL,
  countermeasure_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id)
) ENGINE=INNODB;
CREATE TABLE domainproperty_reference (
  id INT NOT NULL,
  domainproperty_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(domainproperty_id) REFERENCES domainproperty(id)
) ENGINE=INNODB;
CREATE TABLE environment_reference (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE goal_reference (
  id INT NOT NULL,
  goal_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id)
) ENGINE=INNODB;
CREATE TABLE misusecase_reference (
  id INT NOT NULL,
  misusecase_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(misusecase_id) REFERENCES misusecase(id)
) ENGINE=INNODB;
CREATE TABLE obstacle_reference (
  id INT NOT NULL,
  obstacle_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id)
) ENGINE=INNODB;
CREATE TABLE persona_reference (
  id INT NOT NULL,
  persona_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id) REFERENCES persona(id)
) ENGINE=INNODB;
CREATE TABLE requirement_reference (
  id INT NOT NULL,
  requirement_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(requirement_id) REFERENCES requirement(id)
) ENGINE=INNODB;
CREATE TABLE response_reference (
  id INT NOT NULL,
  response_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(response_id) REFERENCES response(id)
) ENGINE=INNODB;
CREATE TABLE risk_reference (
  id INT NOT NULL,
  risk_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(risk_id) REFERENCES risk(id)
) ENGINE=INNODB;
CREATE TABLE role_reference (
  id INT NOT NULL,
  role_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(role_id) REFERENCES role(id)
) ENGINE=INNODB;
CREATE TABLE task_reference (
  id INT NOT NULL,
  task_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(task_id) REFERENCES task(id)
) ENGINE=INNODB;
CREATE TABLE usecase_reference (
  id INT NOT NULL,
  usecase_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id)
) ENGINE=INNODB;
CREATE TABLE threat_reference (
  id INT NOT NULL,
  threat_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(threat_id) REFERENCES threat(id)
) ENGINE=INNODB;
CREATE TABLE vulnerability_reference (
  id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  name VARCHAR(200),
  description VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_document (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES document_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_asset (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES asset_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_attacker (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES attacker_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_countermeasure (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES countermeasure_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_domainproperty (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES domainproperty_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_environment (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES environment_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_goal (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES goal_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_misusecase (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES misusecase_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_obstacle (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES obstacle_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_persona (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES persona_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_requirement (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES requirement_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_response (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES response_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_risk (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES risk_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_role (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES role_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_task (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES task_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_threat (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES threat_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_usecase (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES usecase_reference(id)
) ENGINE=INNODB;
CREATE TABLE persona_characteristic_vulnerability (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES vulnerability_reference(id)
) ENGINE=INNODB;
CREATE TABLE usecase_step_none_exception (
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  step_no INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(usecase_id,environment_id,step_no,name),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
CREATE TABLE usecase_step_goal_exception (
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  step_no INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  goal_id INT NOT NULL,
  category_type_id INT NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(usecase_id,environment_id,step_no,name),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES goal(id),
  FOREIGN KEY(category_type_id) REFERENCES obstacle_category_type(id)
) ENGINE=INNODB;
CREATE TABLE usecase_step_requirement_exception (
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  step_no INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  goal_id INT NOT NULL,
  category_type_id INT NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(usecase_id,environment_id,step_no,name),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(goal_id) REFERENCES requirement(id),
  FOREIGN KEY(category_type_id) REFERENCES obstacle_category_type(id)
) ENGINE=INNODB;
CREATE TABLE task_characteristic_document (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES task_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES document_reference(id)
) ENGINE=INNODB;
CREATE TABLE task_characteristic_persona (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES task_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES persona_reference(id)
) ENGINE=INNODB;
CREATE TABLE task_characteristic_usecase (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES task_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES usecase_reference(id)
) ENGINE=INNODB;
CREATE TABLE task_characteristic_requirement (
  characteristic_id INT NOT NULL,
  reference_id INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id,reference_id),
  FOREIGN KEY(characteristic_id) REFERENCES task_characteristic(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id),
  FOREIGN KEY(reference_id) REFERENCES requirement_reference(id)
) ENGINE=INNODB;
CREATE TABLE value_tension (
  environment_id INT NOT NULL,
  security_property_id INT NOT NULL,
  privacy_property_id INT NOT NULL,
  tension_id INT NOT NULL,
  tension_rationale VARCHAR(4000) NOT NULL,
  PRIMARY KEY(environment_id,security_property_id,privacy_property_id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(security_property_id) REFERENCES security_property(id),
  FOREIGN KEY(privacy_property_id) REFERENCES security_property(id),
  FOREIGN KEY(tension_id) REFERENCES tension(id) 
) ENGINE=INNODB;

CREATE TABLE tag (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE asset_tag (
  asset_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(asset_id,tag_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE template_asset_tag (
  template_asset_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(template_asset_id,tag_id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE attacker_tag (
  attacker_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(attacker_id,tag_id),
  FOREIGN KEY(attacker_id) REFERENCES attacker(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE threat_tag (
  threat_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(threat_id,tag_id),
  FOREIGN KEY(threat_id) REFERENCES threat(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE vulnerability_tag (
  vulnerability_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(vulnerability_id,tag_id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE risk_tag (
  risk_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(risk_id,tag_id),
  FOREIGN KEY(risk_id) REFERENCES risk(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE task_tag (
  task_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(task_id,tag_id),
  FOREIGN KEY(task_id) REFERENCES task(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE usecase_tag (
  usecase_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(usecase_id,tag_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE usecase_step_tag (
  usecase_id INT NOT NULL,
  environment_id INT NOT NULL,
  step_no INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(usecase_id,environment_id,step_no,tag_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE persona_tag (
  persona_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(persona_id,tag_id),
  FOREIGN KEY(persona_id) REFERENCES persona(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE goal_tag (
  goal_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(goal_id,tag_id),
  FOREIGN KEY(goal_id) REFERENCES goal(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE obstacle_tag (
  obstacle_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(obstacle_id,tag_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE domainproperty_tag (
  domainproperty_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(domainproperty_id,tag_id),
  FOREIGN KEY(domainproperty_id) REFERENCES domainproperty(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE countermeasure_tag (
  countermeasure_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(countermeasure_id,tag_id),
  FOREIGN KEY(countermeasure_id) REFERENCES countermeasure(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE response_tag (
  response_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(response_id,tag_id),
  FOREIGN KEY(response_id) REFERENCES response(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;


CREATE TABLE contribution_end (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE link_contribution (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  value INT NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE goal_satisfaction (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  value INT NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE persona_characteristic_synopsis (
  characteristic_id INT NOT NULL,
  synopsis VARCHAR(1000) NOT NULL,
  dimension_id INT NOT NULL,
  satisfaction INT NOT NULL DEFAULT 0,
  PRIMARY KEY(characteristic_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
  FOREIGN KEY(satisfaction) REFERENCES goal_satisfaction(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE task_characteristic_synopsis (
  characteristic_id INT NOT NULL,
  synopsis VARCHAR(1000) NOT NULL,
  dimension_id INT NOT NULL,
  actor_id INT NOT NULL,
  actor_type_id INT NOT NULL,
  PRIMARY KEY(characteristic_id),
  FOREIGN KEY(characteristic_id) REFERENCES task_characteristic(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id),
  FOREIGN KEY(actor_type_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE document_reference_synopsis (
  id INT NOT NULL,
  reference_id INT NOT NULL,
  synopsis VARCHAR(1000) NOT NULL,
  dimension_id INT NOT NULL,
  actor_id INT NOT NULL,
  actor_type_id INT NOT NULL,
  satisfaction INT NOT NULL DEFAULT 0,
  PRIMARY KEY(id),
  FOREIGN KEY(reference_id) REFERENCES document_reference(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id),
  FOREIGN KEY(satisfaction) REFERENCES goal_satisfaction(id),
  FOREIGN KEY(actor_type_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE requirement_reference_synopsis (
  id INT NOT NULL,
  reference_id INT NOT NULL,
  synopsis VARCHAR(1000) NOT NULL,
  dimension_id INT NOT NULL,
  actor_id INT NOT NULL,
  actor_type_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(reference_id) REFERENCES requirement_reference(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id),
  FOREIGN KEY(actor_type_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE usecase_pc_contribution (
  usecase_id INT NOT NULL,
  characteristic_id INT NOT NULL,
  end_id INT NOT NULL,
  contribution_id INT NOT NULL,
  PRIMARY KEY(usecase_id,characteristic_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic_synopsis(characteristic_id),
  FOREIGN KEY(end_id) REFERENCES contribution_end(id),
  FOREIGN KEY(contribution_id) REFERENCES link_contribution(id)
) ENGINE=INNODB;


CREATE TABLE usecase_tc_contribution (
  usecase_id INT NOT NULL,
  characteristic_id INT NOT NULL,
  end_id INT NOT NULL,
  contribution_id INT NOT NULL,
  PRIMARY KEY(usecase_id,characteristic_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(characteristic_id) REFERENCES task_characteristic_synopsis(characteristic_id),
  FOREIGN KEY(end_id) REFERENCES contribution_end(id),
  FOREIGN KEY(contribution_id) REFERENCES link_contribution(id)
) ENGINE=INNODB;

CREATE TABLE usecase_dr_contribution (
  usecase_id INT NOT NULL,
  reference_id INT NOT NULL,
  end_id INT NOT NULL,
  contribution_id INT NOT NULL,
  PRIMARY KEY(usecase_id,reference_id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(reference_id) REFERENCES document_reference_synopsis(id),
  FOREIGN KEY(end_id) REFERENCES contribution_end(id),
  FOREIGN KEY(contribution_id) REFERENCES link_contribution(id)
) ENGINE=INNODB;

CREATE TABLE usecase_step_synopsis (
  id INT NOT NULL,
  usecase_id INT NOT NULL,
  step_no INT NOT NULL,
  environment_id INT NOT NULL,
  synopsis VARCHAR(500) NOT NULL,
  actor_id INT NOT NULL,
  actor_type_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(actor_type_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE document_reference_contribution (
  reference_id INT NOT NULL,
  characteristic_id INT NOT NULL,
  end_id INT NOT NULL,
  contribution_id INT NOT NULL,
  PRIMARY KEY(reference_id,characteristic_id),
  FOREIGN KEY(end_id) REFERENCES contribution_end(id),
  FOREIGN KEY(contribution_id) REFERENCES link_contribution(id)
) ENGINE=INNODB;

CREATE TABLE user_system_goal_link (
  user_goal_id INT NOT NULL,
  system_goal_id INT NOT NULL,
  PRIMARY KEY(user_goal_id,system_goal_id),
  FOREIGN KEY(system_goal_id) REFERENCES goal(id)
) ENGINE=INNODB;

CREATE TABLE requirement_reference_contribution (
  reference_id INT NOT NULL,
  characteristic_id INT NOT NULL,
  end_id INT NOT NULL,
  contribution_id INT NOT NULL,
  PRIMARY KEY(reference_id,characteristic_id),
  FOREIGN KEY(reference_id) REFERENCES requirement_reference_synopsis(id),
  FOREIGN KEY(end_id) REFERENCES contribution_end(id),
  FOREIGN KEY(contribution_id) REFERENCES link_contribution(id)
) ENGINE=INNODB;

CREATE TABLE component (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE component_usecase (
  component_id INT NOT NULL,
  usecase_id INT NOT NULL,
  PRIMARY KEY(component_id,usecase_id),
  FOREIGN KEY(component_id) REFERENCES component(id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id)
) ENGINE=INNODB;

CREATE TABLE interface (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE component_interface (
  component_id INT NOT NULL,
  interface_id INT NOT NULL,
  required_id INT NOT NULL,
  access_right_id INT NOT NULL,
  privilege_id INT NOT NULL,
  PRIMARY KEY(component_id,interface_id),
  FOREIGN KEY(component_id) REFERENCES component(id),
  FOREIGN KEY(interface_id) REFERENCES interface(id),
  FOREIGN KEY(access_right_id) REFERENCES access_right(id),
  FOREIGN KEY(privilege_id) REFERENCES privilege(id)
) ENGINE=INNODB;


CREATE TABLE component_asset_template_asset (
  asset_id INT NOT NULL,
  template_asset_id INT NOT NULL,
  component_id INT NOT NULL,
  PRIMARY KEY(asset_id,template_asset_id,component_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id),
  FOREIGN KEY(component_id) REFERENCES component(id)
) ENGINE=INNODB;

CREATE TABLE asset_interface (
  asset_id INT NOT NULL,
  interface_id INT NOT NULL,
  required_id INT NOT NULL,
  access_right_id INT NOT NULL,
  privilege_id INT NOT NULL,
  PRIMARY KEY(asset_id,interface_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(interface_id) REFERENCES interface(id),
  FOREIGN KEY(access_right_id) REFERENCES access_right(id),
  FOREIGN KEY(privilege_id) REFERENCES privilege(id)
) ENGINE=INNODB;

CREATE TABLE template_asset_interface (
  template_asset_id INT NOT NULL,
  interface_id INT NOT NULL,
  required_id INT NOT NULL,
  access_right_id INT NOT NULL,
  privilege_id INT NOT NULL,
  PRIMARY KEY(template_asset_id,interface_id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id),
  FOREIGN KEY(interface_id) REFERENCES interface(id),
  FOREIGN KEY(access_right_id) REFERENCES access_right(id),
  FOREIGN KEY(privilege_id) REFERENCES privilege(id)
) ENGINE=INNODB;

CREATE TABLE component_view(
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  synopsis VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE connector (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  component_view_id INT NOT NULL,
  from_component_id INT NOT NULL,
  from_role VARCHAR(255) NOT NULL,
  from_interface_id INT NOT NULL,
  to_component_id INT NOT NULL,
  to_interface_id INT NOT NULL,
  to_role VARCHAR(255) NOT NULL,
  template_asset_id INT NOT NULL,
  protocol_id INT NOT NULL,
  access_right_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(component_view_id) REFERENCES component_view(id),
  FOREIGN KEY(from_component_id) REFERENCES component(id),
  FOREIGN KEY(from_interface_id) REFERENCES interface(id),
  FOREIGN KEY(to_component_id) REFERENCES component(id),
  FOREIGN KEY(to_interface_id) REFERENCES interface(id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id),
  FOREIGN KEY(protocol_id) REFERENCES protocol(id),
  FOREIGN KEY(access_right_id) REFERENCES access_right(id)
) ENGINE=INNODB;


CREATE TABLE component_classassociation (
  id INT NOT NULL,
  component_id INT NOT NULL,
  head_id INT NOT NULL,
  head_association_type_id INT NOT NULL,
  head_navigation INT NOT NULL default 0,
  head_multiplicity_id INT NOT NULL,
  head_role_name VARCHAR(50) NOT NULL,
  tail_role_name VARCHAR(50) NOT NULL,
  tail_multiplicity_id INT NOT NULL,
  tail_navigation INT NOT NULL default 0,
  tail_association_type_id INT NOT NULL,
  tail_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(component_id) REFERENCES component(id),
  FOREIGN KEY(head_id) REFERENCES template_asset(id),
  FOREIGN KEY(head_association_type_id) REFERENCES association_type(id),
  FOREIGN KEY(head_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(tail_multiplicity_id) REFERENCES multiplicity_type(id), 
  FOREIGN KEY(tail_association_type_id) REFERENCES association_type(id),
  FOREIGN KEY(tail_id) REFERENCES template_asset(id)
) ENGINE=INNODB;


CREATE TABLE component_template_requirement (
  template_requirement_id INT NOT NULL,
  component_id INT NOT NULL,
  label INT NOT NULL,
  PRIMARY KEY(template_requirement_id,component_id),
  FOREIGN KEY (component_id) REFERENCES component(id),
  FOREIGN KEY (template_requirement_id) REFERENCES template_requirement(id)
) ENGINE=INNODB;

CREATE TABLE component_template_goal (
  template_goal_id INT NOT NULL,
  component_id INT NOT NULL,
  PRIMARY KEY(template_goal_id,component_id),
  FOREIGN KEY (component_id) REFERENCES component(id),
  FOREIGN KEY (template_goal_id) REFERENCES template_goal(id)
) ENGINE=INNODB;

CREATE TABLE component_requirement_template_requirement (
  requirement_id INT NOT NULL,
  template_requirement_id INT NOT NULL,
  component_id INT NOT NULL,
  PRIMARY KEY(requirement_id,template_requirement_id,component_id),
  FOREIGN KEY (requirement_id) REFERENCES requirement(id),
  FOREIGN KEY (component_id) REFERENCES component(id),
  FOREIGN KEY (template_requirement_id) REFERENCES template_requirement(id)
) ENGINE=INNODB;

CREATE TABLE component_goal_template_goal (
  goal_id INT NOT NULL,
  template_goal_id INT NOT NULL,
  component_id INT NOT NULL,
  PRIMARY KEY(goal_id,template_goal_id,component_id),
  FOREIGN KEY (goal_id) REFERENCES goal(id),
  FOREIGN KEY (component_id) REFERENCES component(id),
  FOREIGN KEY (template_goal_id) REFERENCES template_goal(id)
) ENGINE=INNODB;

CREATE TABLE component_goalgoal_goalassociation (
  component_id INT NOT NULL,
  goal_id INT NOT NULL,
  ref_type_id INT NOT NULL,
  subgoal_id INT NOT NULL,
  rationale VARCHAR(1000) NOT NULL,
  PRIMARY KEY(component_id,goal_id,ref_type_id,subgoal_id),
  FOREIGN KEY(goal_id) REFERENCES template_goal(id),
  FOREIGN KEY(ref_type_id) REFERENCES reference_type(id),
  FOREIGN KEY(subgoal_id) REFERENCES template_goal(id)
) ENGINE=INNODB;

CREATE TABLE component_view_component(
  component_view_id INT NOT NULL,
  component_id INT NOT NULL,
  PRIMARY KEY(component_view_id,component_id),
  FOREIGN KEY (component_view_id) REFERENCES component_view(id),
  FOREIGN KEY (component_id) REFERENCES component(id)
) ENGINE=INNODB;

CREATE TABLE component_vulnerability_target (
  component_id INT NOT NULL,
  asset_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  effectiveness_id INT NOT NULL,
  environment_id INT NOT NULL,
  effectiveness_rationale VARCHAR(4000),
  PRIMARY KEY(component_id,vulnerability_id,environment_id),
  FOREIGN KEY(component_id) REFERENCES component(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id),
  FOREIGN KEY(effectiveness_id) REFERENCES target_effectiveness(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;

CREATE TABLE component_threat_target (
  component_id INT NOT NULL,
  asset_id INT NOT NULL,
  threat_id INT NOT NULL,
  effectiveness_id INT NOT NULL,
  environment_id INT NOT NULL,
  effectiveness_rationale VARCHAR(4000),
  PRIMARY KEY(component_id,threat_id,environment_id),
  FOREIGN KEY(component_id) REFERENCES component(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(threat_id) REFERENCES threat(id),
  FOREIGN KEY(effectiveness_id) REFERENCES target_effectiveness(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;

CREATE TABLE relationship_type (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE code_type (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE memo (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE code (
  id INT NOT NULL,
  code_type_id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  inclusion_criteria VARCHAR(2000) NOT NULL,
  example VARCHAR(2000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(code_type_id) REFERENCES code_type(id)
) ENGINE=INNODB;

CREATE TABLE parameter (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE channel (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE channel_parameter (
  channel_id INT NOT NULL,
  code_id INT NOT NULL,
  parameter_id INT NOT NULL,
  PRIMARY KEY(channel_id,code_id,parameter_id),  
  FOREIGN KEY(channel_id) REFERENCES channel(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(parameter_id) REFERENCES parameter(id)
) ENGINE=INNODB;

CREATE TABLE persona_code_network (
  id INT NOT NULL,
  persona_id INT NOT NULL,
  from_code_id INT NOT NULL,
  to_code_id INT NOT NULL,
  relationship_type_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(from_code_id) REFERENCES code(id),
  FOREIGN KEY(to_code_id) REFERENCES code(id),
  FOREIGN KEY(relationship_type_id) REFERENCES relationship_type(id),
  FOREIGN KEY(persona_id) REFERENCES persona(id)
) ENGINE=INNODB;

CREATE TABLE implied_characteristic (
  id INT NOT NULL,
  persona_code_network_id INT NOT NULL,
  synopsis VARCHAR(2000) NOT NULL,
  qualifier VARCHAR(1000) NOT NULL,
  variable_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_code_network_id) REFERENCES persona_code_network(id),
  FOREIGN KEY(variable_id) REFERENCES behavioural_variable(id)
) ENGINE=INNODB;

CREATE TABLE implied_characteristic_intention (
  characteristic_id INT NOT NULL,
  synopsis VARCHAR(1000) NOT NULL,
  dimension_id INT NOT NULL,
  PRIMARY KEY(characteristic_id),
  FOREIGN KEY(characteristic_id) REFERENCES implied_characteristic(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE persona_implied_process (
  id INT NOT NULL,
  name VARCHAR(200) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  persona_id INT NOT NULL,
  specification VARCHAR(2000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id) REFERENCES persona(id)
) ENGINE=INNODB;

CREATE TABLE persona_implied_process_network (
  persona_implied_process_id INT NOT NULL,
  persona_code_network_id INT NOT NULL,
  PRIMARY KEY(persona_implied_process_id,persona_code_network_id),
  FOREIGN KEY(persona_implied_process_id) REFERENCES persona_implied_process(id),
  FOREIGN KEY(persona_code_network_id) REFERENCES persona_code_network(id)
) ENGINE=INNODB;

CREATE TABLE persona_implied_process_channel (
  persona_implied_process_id INT NOT NULL,
  channel_name VARCHAR(200) NOT NULL,
  data_type_name VARCHAR(200) NOT NULL,
  PRIMARY KEY(persona_implied_process_id,channel_name),
  FOREIGN KEY(persona_implied_process_id) REFERENCES persona_implied_process(id)
) ENGINE=INNODB;

CREATE TABLE internal_document (
  id INT NOT NULL,
  name VARCHAR(2000) NOT NULL,
  description VARCHAR(2000) NOT NULL,
  content LONGTEXT,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE internal_document_code (
  internal_document_id INT NOT NULL,
  code_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  synopsis VARCHAR(1000),
  label VARCHAR(200),
  PRIMARY KEY(internal_document_id,code_id,start_index,end_index),
  FOREIGN KEY(internal_document_id) REFERENCES internal_document(id),
  FOREIGN KEY(code_id) REFERENCES code(id)
) ENGINE=INNODB;

CREATE TABLE internal_document_code_intention (
  internal_document_id INT NOT NULL,
  code_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  intention VARCHAR(1000),
  dimension_id INT NOT NULL,
  actor_id INT NOT NULL,
  actor_type_id INT NOT NULL,
  PRIMARY KEY(internal_document_id,code_id,start_index,end_index),
  FOREIGN KEY(internal_document_id) REFERENCES internal_document(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id),
  FOREIGN KEY(actor_type_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE implied_characteristic_element (
  implied_characteristic_id INT NOT NULL,
  internal_document_id INT NOT NULL,
  code_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  characteristic_reference_type_id INT NOT NULL,
  PRIMARY KEY(implied_characteristic_id,internal_document_id,code_id,start_index,end_index,characteristic_reference_type_id),
  FOREIGN KEY(implied_characteristic_id) REFERENCES implied_characteristic(id),
  FOREIGN KEY(internal_document_id) REFERENCES internal_document(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(characteristic_reference_type_id) REFERENCES characteristic_reference_type(id)
) ENGINE=INNODB;

CREATE TABLE implied_characteristic_element_intention (
  id INT NOT NULL,
  implied_characteristic_id INT NOT NULL,
  internal_document_id INT NOT NULL,
  code_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  synopsis VARCHAR(1000) NOT NULL,
  dimension_id INT NOT NULL,
  actor_id INT NOT NULL,
  actor_type_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(implied_characteristic_id) REFERENCES implied_characteristic(id),
  FOREIGN KEY(internal_document_id) REFERENCES internal_document(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id),
  FOREIGN KEY(actor_type_id) REFERENCES trace_dimension(id)
) ENGINE=INNODB;

CREATE TABLE ice_ic_contribution (
  implied_characteristic_element_intention_id INT NOT NULL,
  implied_characteristic_id INT NOT NULL,
  end_id INT NOT NULL,
  contribution_id INT NOT NULL,
  PRIMARY KEY(implied_characteristic_element_intention_id,implied_characteristic_id),
  FOREIGN KEY(implied_characteristic_element_intention_id) REFERENCES implied_characteristic_element_intention(id),
  FOREIGN KEY(implied_characteristic_id) REFERENCES implied_characteristic(id),
  FOREIGN KEY(end_id) REFERENCES contribution_end(id),
  FOREIGN KEY(contribution_id) REFERENCES link_contribution(id)
) ENGINE=INNODB;

CREATE TABLE internal_document_memo (
  internal_document_id INT NOT NULL,
  memo_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  PRIMARY KEY(internal_document_id,memo_id,start_index,end_index),
  FOREIGN KEY(internal_document_id) REFERENCES internal_document(id),
  FOREIGN KEY(memo_id) REFERENCES memo(id)
) ENGINE=INNODB;

CREATE TABLE artifact_section (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE persona_code (
  persona_id INT NOT NULL,
  code_id INT NOT NULL,
  section_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  synopsis VARCHAR(1000),
  label VARCHAR(200),
  PRIMARY KEY(persona_id,code_id,section_id,start_index,end_index),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(section_id) REFERENCES artifact_section(id)
) ENGINE=INNODB;

CREATE TABLE persona_environment_code (
  persona_id INT NOT NULL,
  environment_id INT NOT NULL,
  code_id INT NOT NULL,
  section_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  PRIMARY KEY(persona_id,environment_id,code_id,section_id,start_index,end_index),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(section_id) REFERENCES artifact_section(id)
) ENGINE=INNODB;

CREATE TABLE task_code (
  task_id INT NOT NULL,
  code_id INT NOT NULL,
  section_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  synopsis VARCHAR(1000),
  label VARCHAR(200),
  PRIMARY KEY(task_id,code_id,section_id,start_index,end_index),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(section_id) REFERENCES artifact_section(id)
) ENGINE=INNODB;

CREATE TABLE task_environment_code (
  task_id INT NOT NULL,
  environment_id INT NOT NULL,
  code_id INT NOT NULL,
  section_id INT NOT NULL,
  start_index INT NOT NULL,
  end_index INT NOT NULL,
  PRIMARY KEY(task_id,environment_id,code_id,section_id,start_index,end_index),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(code_id) REFERENCES code(id),
  FOREIGN KEY(section_id) REFERENCES artifact_section(id)
) ENGINE=INNODB;


DROP TABLE IF EXISTS locations;

CREATE TABLE locations (
  id INT NOT NULL,
  name VARCHAR(1000),
  diagram VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE location (
  id INT NOT NULL,
  locations_id INT NOT NULL,
  name VARCHAR(1000),
  PRIMARY KEY(id),
  FOREIGN KEY(locations_id) REFERENCES locations(id)
) ENGINE=INNODB;

CREATE TABLE location_link (
  locations_id INT NOT NULL,
  head_location_id INT NOT NULL,
  tail_location_id INT NOT NULL,
  PRIMARY KEY(locations_id,head_location_id,tail_location_id),
  FOREIGN KEY(locations_id) REFERENCES locations(id),
  FOREIGN KEY(head_location_id) REFERENCES location(id),
  FOREIGN KEY(tail_location_id) REFERENCES location(id)
) ENGINE=INNODB;

CREATE TABLE asset_instance (
  id INT NOT NULL,
  name VARCHAR(1000),
  location_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(location_id) REFERENCES location(id)
) ENGINE=INNODB;

CREATE TABLE persona_instance (
  id INT NOT NULL,
  name VARCHAR(1000),
  location_id INT NOT NULL,
  persona_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(persona_id) REFERENCES persona(id),
  FOREIGN KEY(location_id) REFERENCES location(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_type (
  id INT NOT NULL,
  name VARCHAR(255),
  description VARCHAR(1000),
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE dataflow (
  id INT NOT NULL,
  environment_id INT NOT NULL,
  dataflow_type_id INT NOT NULL,
  name VARCHAR(255),
  PRIMARY KEY(id,environment_id,name),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(dataflow_type_id) REFERENCES dataflow_type(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_asset (
  dataflow_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(dataflow_id,asset_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id)
) ENGINE=INNODB;

CREATE TABLE stpa_keyword (
  id INT NOT NULL,
  name VARCHAR(255),
  description VARCHAR(4000),
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_obstacle (
  dataflow_id INT NOT NULL,
  obstacle_id INT NOT NULL,
  stpa_keyword_id INT NOT NULL,
  context VARCHAR(4000),
  PRIMARY KEY(dataflow_id,obstacle_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id),
  FOREIGN KEY(stpa_keyword_id) REFERENCES stpa_keyword(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_tag (
  dataflow_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(dataflow_id,tag_id),
  FOREIGN KEY(dataflow_id) REFERENCES dataflow(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_process_process (
  dataflow_id INT NOT NULL,
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  PRIMARY KEY(dataflow_id,from_id,to_id),
  FOREIGN KEY(dataflow_id) REFERENCES dataflow(id),
  FOREIGN KEY(from_id) REFERENCES usecase(id),
  FOREIGN KEY(to_id) REFERENCES usecase(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_entity_process (
  dataflow_id INT NOT NULL,
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  PRIMARY KEY(dataflow_id,from_id,to_id),
  FOREIGN KEY(dataflow_id) REFERENCES dataflow(id),
  FOREIGN KEY(from_id) REFERENCES asset(id),
  FOREIGN KEY(to_id) REFERENCES usecase(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_process_entity (
  dataflow_id INT NOT NULL,
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  PRIMARY KEY(dataflow_id,from_id,to_id),
  FOREIGN KEY(dataflow_id) REFERENCES dataflow(id),
  FOREIGN KEY(from_id) REFERENCES usecase(id),
  FOREIGN KEY(to_id) REFERENCES asset(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_process_datastore (
  dataflow_id INT NOT NULL,
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  PRIMARY KEY(dataflow_id,from_id,to_id),
  FOREIGN KEY(dataflow_id) REFERENCES dataflow(id),
  FOREIGN KEY(from_id) REFERENCES usecase(id),
  FOREIGN KEY(to_id) REFERENCES asset(id)
) ENGINE=INNODB;

CREATE TABLE dataflow_datastore_process (
  dataflow_id INT NOT NULL,
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  PRIMARY KEY(dataflow_id,from_id,to_id),
  FOREIGN KEY(dataflow_id) REFERENCES dataflow(id),
  FOREIGN KEY(from_id) REFERENCES asset(id),
  FOREIGN KEY(to_id) REFERENCES usecase(id)
) ENGINE=INNODB;

CREATE TABLE trust_boundary_type (
  id INT NOT NULL,
  name VARCHAR(255),
  description VARCHAR(4000),
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE trust_boundary (
  id INT NOT NULL,
  name VARCHAR(50), 
  trust_boundary_type_id INT NOT NULL,
  description VARCHAR(4000), 
  PRIMARY KEY(id),
  FOREIGN KEY(trust_boundary_type_id) REFERENCES trust_boundary_type(id)
) ENGINE=INNODB;

CREATE TABLE trust_boundary_usecase (
  trust_boundary_id INT NOT NULL,
  environment_id INT NOT NULL,
  usecase_id INT NOT NULL,
  PRIMARY KEY(trust_boundary_id,environment_id,usecase_id),
  FOREIGN KEY(trust_boundary_id) REFERENCES trust_boundary(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(usecase_id) REFERENCES usecase(id)
) ENGINE=INNODB;

CREATE TABLE trust_boundary_asset (
  trust_boundary_id INT NOT NULL,
  environment_id INT NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(trust_boundary_id,environment_id,asset_id),
  FOREIGN KEY(trust_boundary_id) REFERENCES trust_boundary(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id),
  FOREIGN KEY(asset_id) REFERENCES asset(id)
) ENGINE=INNODB;

CREATE TABLE trust_boundary_privilege (
  trust_boundary_id INT NOT NULL,
  environment_id INT NOT NULL,
  privilege_value INT NOT NULL,
  PRIMARY KEY(trust_boundary_id,environment_id,privilege_value),
  FOREIGN KEY(trust_boundary_id) REFERENCES trust_boundary(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;

CREATE TABLE trust_boundary_tag (
  trust_boundary_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(trust_boundary_id,tag_id),
  FOREIGN KEY(trust_boundary_id) REFERENCES trust_boundary(id), 
  FOREIGN KEY(tag_id) REFERENCES tag(id)
) ENGINE=INNODB;

CREATE TABLE risk_vulnerability (
  risk_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  PRIMARY KEY(risk_id,vulnerability_id),
  FOREIGN KEY(risk_id) REFERENCES risk(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id)
) ENGINE=INNODB;

CREATE TABLE risk_threat (
  risk_id INT NOT NULL,
  threat_id INT NOT NULL,
  PRIMARY KEY(risk_id,threat_id),
  FOREIGN KEY(risk_id) REFERENCES risk(id),
  FOREIGN KEY(threat_id) REFERENCES threat(id)
) ENGINE=INNODB;

CREATE TABLE image (
  name VARCHAR(255) NOT NULL,
  content LONGBLOB NOT NULL,
  mimetype VARCHAR(100),
  PRIMARY KEY(name)
) ENGINE=INNODB;

CREATE TABLE task_goal_contribution (
  task_id INT NOT NULL,
  environment_id INT NOT NULL,
  reference_id INT NOT NULL,
  contribution_id INT NOT NULL,
  PRIMARY KEY (task_id,environment_id,reference_id),
  FOREIGN KEY(task_id) REFERENCES task(id),
  FOREIGN KEY(environment_id) REFERENCES environment(id)
) ENGINE=INNODB;
  
CREATE TABLE document_reference_vulnerability (
  document_reference_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
  PRIMARY KEY(document_reference_id,vulnerability_id),
  FOREIGN KEY(document_reference_id) REFERENCES document_reference(id),
  FOREIGN KEY(vulnerability_id) REFERENCES vulnerability(id)
) ENGINE=INNODB; 

CREATE TABLE document_reference_obstacle (
  document_reference_id INT NOT NULL,
  obstacle_id INT NOT NULL,
  PRIMARY KEY(document_reference_id,obstacle_id),
  FOREIGN KEY(document_reference_id) REFERENCES document_reference(id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id)
) ENGINE=INNODB; 

delimiter //

create function internalDocumentQuotationString(idName text, startIdx int, endIdx int) 
returns varchar(4000)
deterministic 
begin
  declare idId int;
  declare quote varchar(4000);
  select id into idId from internal_document where name = idName limit 1;
  select substr(content,startIdx,endIdx - startIdx) into quote from internal_document where id = idId;
  return quote;
end
//

create function personaQuotationString(pName text, sectName text, envName text, startIdx int, endIdx int) 
returns varchar(4000)
deterministic 
begin
  declare pId int;
  declare envId int;
  declare quote varchar(4000);
  select id into pId from persona where name = pName limit 1;

  if sectName = 'activities'
  then
    select substr(activities,startIdx,endIdx - startIdx) into quote from persona where id = pId;
  elseif sectName = 'attitudes'
  then
    select substr(attitudes,startIdx,endIdx - startIdx) into quote from persona where id = pId;
  elseif sectName = 'aptitudes'
  then
    select substr(aptitudes,startIdx,endIdx - startIdx) into quote from persona where id = pId;
  elseif sectName = 'motivations'
  then
    select substr(motivations,startIdx,endIdx - startIdx) into quote from persona where id = pId;
  elseif sectName = 'skills'
  then
    select substr(skills,startIdx,endIdx - startIdx) into quote from persona where id = pId;
  elseif sectName = 'intrinsic'
  then
    select substr(intrinsic,startIdx,endIdx - startIdx) into quote from persona where id = pId;
  elseif sectName = 'contextual'
  then
    select substr(contextual,startIdx,endIdx - startIdx) into quote from persona where id = pId;
  else
    select id into envId from environment where name = envName limit 1;
    select substr(narrative,startIdx,endIdx - startIdx) into quote from persona_narrative where persona_id = pId and environment_id = envId;
  end if;

  return quote;
end
//

delimiter ; 

CREATE VIEW value_type as
  select id, name from asset_type
  union
  select id, name from access_right
  union
  select id, name from protocol
  union
  select id, name from privilege
  union
  select id, name from surface_type
  union
  select id, name from vulnerability_type
  union
  select id, name from severity
  union
  select id, name from capability
  union
  select id, name from motivation
  union
  select id, name from threat_type
  union
  select id, name from likelihood;

CREATE VIEW object_name as
  select name from requirement
  union
  select name from domainproperty
  union
  select name from goal
  union
  select name from obstacle
  union
  select name from usecase
  union
  select name from role
  union
  select name from asset
  union
  select name from threat
  union
  select name from vulnerability
  union
  select name from risk
  union
  select name from response
  union
  select name from countermeasure
  union 
  select name from environment
  union
  select name from persona
  union
  select name from task
  union 
  select name from locations
  union
  select name from location
  union
  select description name from persona_characteristic
  union
  select description name from task_characteristic;

CREATE VIEW entity as
  select id,name,short_code,description,significance,asset_type_id,is_critical,critical_rationale from asset where asset_type_id in (1,3,4);

CREATE VIEW datastore as
  select id,name,short_code,description,significance,asset_type_id,is_critical,critical_rationale from asset where asset_type_id = 0;

CREATE VIEW dataflows as
  select d.name dataflow, dt.name dataflow_type, e.name environment,fp.name from_name,'process' from_type,tp.name to_name,'process' to_type from dataflow d, dataflow_process_process dpp, usecase fp, usecase tp, environment e, dataflow_type dt where d.id = dpp.dataflow_id and d.environment_id = e.id and dpp.from_id = fp.id and dpp.to_id = tp.id and d.dataflow_type_id = dt.id
  union
  select d.name dataflow, dt.name dataflow_type, e.name environment, fe.name from_name, 'entity' from_type, tp.name to_name, 'process' to_type from dataflow d, dataflow_entity_process dep, asset fe, usecase tp, environment e, dataflow_type dt where d.id = dep.dataflow_id and d.environment_id = e.id and dep.from_id = fe.id and dep.to_id = tp.id and d.dataflow_type_id = dt.id
  union
  select d.name dataflow, dt.name dataflow_type, e.name environment, fp.name from_name, 'process' from_type, te.name to_name, 'entity' to_type from dataflow d, dataflow_process_entity dpe, usecase fp, asset te, environment e, dataflow_type dt where d.id = dpe.dataflow_id and d.environment_id = e.id and dpe.from_id = fp.id and dpe.to_id = te.id and d.dataflow_type_id = dt.id
  union
  select d.name dataflow, dt.name dataflow_type, e.name environment, fd.name from_name, 'datastore' from_type, tp.name to_name, 'process' to_type from dataflow d, dataflow_datastore_process ddp, asset fd, usecase tp, environment e, dataflow_type dt where d.id = ddp.dataflow_id and d.environment_id = e.id and ddp.from_id = fd.id and ddp.to_id = tp.id and d.dataflow_type_id = dt.id
  union
  select d.name dataflow, dt.name dataflow_type, e.name environment, fp.name from_name, 'process' from_type, td.name to_name, 'datastore' to_type from dataflow d, dataflow_process_datastore dpd, usecase fp, asset td, environment e, dataflow_type dt where d.id = dpd.dataflow_id and d.environment_id = e.id and dpd.from_id = fp.id and dpd.to_id = td.id and d.dataflow_type_id = dt.id;


CREATE VIEW countermeasure_vulnerability_response_target as 
  select distinct cvt.countermeasure_id,re.id response_id,cvt.vulnerability_id,cvt.environment_id from countermeasure_vulnerability_target cvt, environment_vulnerability ev, risk ri,response re where cvt.vulnerability_id = ev.vulnerability_id and cvt.environment_id = ev.environment_id and ev.vulnerability_id = ri.vulnerability_id and ri.id = re.risk_id;

CREATE VIEW countermeasure_threat_response_target as 
  select distinct ctt.countermeasure_id,re.id response_id,ctt.threat_id,ctt.environment_id from countermeasure_threat_target ctt, environment_threat et, risk ri,response re where ctt.threat_id = et.threat_id and ctt.environment_id = et.environment_id and et.threat_id = ri.threat_id and ri.id = re.risk_id;

CREATE VIEW redmine_requirement as
  select o.name name,o.originator,o.priority priority,o.rationale comments, o.description description,rm.short_code environment_code,rm.name environment from requirement o, environment_requirement rmr, environment rm where o.version = (select max(i.version) from requirement i where i.id = o.id) and o.id = rmr.requirement_id and rmr.environment_id = rm.id;

CREATE VIEW synopsis as
  select characteristic_id id,synopsis,'persona' synopsis_type from persona_characteristic_synopsis 
  union 
  select characteristic_id id,synopsis,'task' synopsis_type from task_characteristic_synopsis 
  union 
  select id,synopsis,'document' synopsis_type from document_reference_synopsis 
  union 
  select id,synopsis,'requirement' synopsis_type from requirement_reference_synopsis
  union
  select id,synopsis,'usecase' synopsis_type from usecase_step_synopsis
  union
  select characteristic_id,synopsis,'persona' synopsis_type from implied_characteristic_intention
  union
  select id,synopsis,'document' synopsis_type from implied_characteristic_element_intention;

CREATE VIEW contribution as
  select reference_id, characteristic_id, end_id, contribution_id from document_reference_contribution
  union
  select reference_id, characteristic_id, end_id, contribution_id from requirement_reference_contribution
  union
  select reference_id, usecase_id, end_id, contribution_id from usecase_dr_contribution
  union
  select usecase_id, characteristic_id, end_id, contribution_id from usecase_pc_contribution
  union
  select usecase_id, characteristic_id, end_id, contribution_id from usecase_tc_contribution;

CREATE VIEW goal_contribution as
  select e.name environment, drs.synopsis source, 'document_reference' source_type, tds.name source_dimension, sp.name source_persona, pcs.synopsis target, 'persona_characteristic' target_type, tdd.name target_dimension, tp.name target_persona, ce.name means_end, lc.name contribution from document_reference_contribution drc, document_reference_synopsis drs, persona_characteristic_synopsis pcs, trace_dimension tds, trace_dimension tdd, contribution_end ce, link_contribution lc, persona_characteristic pc, environment_persona ep, environment e, persona sp, persona tp where drc.reference_id = drs.id and drc.characteristic_id = pcs.characteristic_id and drs.dimension_id = tds.id and pcs.dimension_id = tdd.id and drc.end_id = ce.id and drc.contribution_id = lc.id and pcs.characteristic_id = pc.id and pc.persona_id = ep.persona_id and ep.environment_id = e.id and drs.actor_id = sp.id and ep.persona_id = tp.id
  union
  select e.name environment, pcs.synopsis source, 'persona_characteristic' source_type, tds.name source_dimension, sp.name source_persona, drs.synopsis target, 'document_reference' target_type, tdd.name target_dimension, tp.name target_persona, ce.name means_end, lc.name contribution from document_reference_contribution drc, document_reference_synopsis drs, persona_characteristic_synopsis pcs, trace_dimension tds, trace_dimension tdd, contribution_end ce, link_contribution lc, persona_characteristic pc, environment_persona ep, environment e, persona sp, persona tp where drc.characteristic_id = drs.id and drc.reference_id = pcs.characteristic_id and drs.dimension_id = tdd.id and pcs.dimension_id = tds.id and drc.end_id = ce.id and drc.contribution_id = lc.id and pcs.characteristic_id = pc.id and pc.persona_id = ep.persona_id and ep.environment_id = e.id and ep.persona_id = sp.id and drs.actor_id = tp.id
  union
  select '' environment, drs.synopsis source, 'document_reference' source_type, tds.name source_dimension, sp.name source_persona, drst.synopsis target, 'document_reference' target_type, tdd.name target_dimension, tp.name target_persona, ce.name means_end, lc.name contribution from document_reference_contribution drc, document_reference_synopsis drs, document_reference_synopsis drst, trace_dimension tds, trace_dimension tdd, contribution_end ce, link_contribution lc, persona sp, persona tp where drc.reference_id = drs.id and drc.characteristic_id = drst.id and drs.dimension_id = tds.id and drst.dimension_id = tdd.id and drc.end_id = ce.id and drc.contribution_id = lc.id and drs.actor_id = sp.id and drst.actor_id = tp.id
  union
  select e.name environment, pcs2.synopsis source, 'persona_characteristic' source_type, tds.name source_dimension, sp.name source_persona, pcs.synopsis target, 'persona_characteristic' target_type, tdd.name target_dimension, tp.name target_persona, ce.name means_end, lc.name contribution from document_reference_contribution drc, persona_characteristic_synopsis pcs2, persona_characteristic_synopsis pcs, trace_dimension tds, trace_dimension tdd, contribution_end ce, link_contribution lc, persona_characteristic pc, persona_characteristic pc2, environment_persona ep, environment_persona ep2, environment e, persona sp, persona tp where drc.reference_id = pcs2.characteristic_id and drc.characteristic_id = pcs.characteristic_id and pcs2.dimension_id = tds.id and pcs.dimension_id = tdd.id and drc.end_id = ce.id and drc.contribution_id = lc.id and pcs.characteristic_id = pc.id and pcs2.characteristic_id = pc2.id and pc.persona_id = ep.persona_id and pc2.persona_id = ep2.persona_id and ep2.environment_id = ep.environment_id and ep.environment_id = e.id and ep2.persona_id = sp.id and ep.persona_id = tp.id
  union
  select e.name environment, t.name source, 'task' source_type, 'task' source_dimension, '' source_persona, drs.synopsis target, 'document_reference' target_type, tdd.name target_dimension, tp.name target_persona,  'means' means_end, lc.name contribution from task_goal_contribution tgc, task t, environment e, environment_task et, trace_dimension tdd, link_contribution lc, document_reference_synopsis drs, persona tp where et.environment_id = e.id and et.task_id = t.id and tgc.task_id = et.task_id and tgc.environment_id = et.environment_id and tgc.reference_id = drs.id and tgc.contribution_id = lc.id and drs.dimension_id = tdd.id and drs.actor_id = tp.id
  union
  select e.name environment, t.name source, 'task' source_type, 'task' source_dimension, '' source_persona, pcs.synopsis target, 'persona_characteristic' target_type, tdd.name target_dimension, tp.name target_persona,  'means' means_end, lc.name contribution from task_goal_contribution tgc, task t, environment e, environment_task et, trace_dimension tdd, link_contribution lc, persona_characteristic_synopsis pcs, persona_characteristic pc, persona tp where et.environment_id = e.id and et.task_id = t.id and tgc.task_id = et.task_id and tgc.environment_id = et.environment_id and tgc.reference_id = pcs.characteristic_id and tgc.contribution_id = lc.id and pcs.dimension_id = tdd.id and pcs.characteristic_id = pc.id and pc.persona_id = tp.id;

CREATE VIEW goal_contribution_table as
  select drs.synopsis source, 'document_reference' source_type, pcs.synopsis target, 'persona_characteristic' target_type, ce.name means_end, lc.name contribution from document_reference_contribution drc, document_reference_synopsis drs, persona_characteristic_synopsis pcs, contribution_end ce, link_contribution lc where drc.reference_id = drs.id and drc.characteristic_id = pcs.characteristic_id and drc.end_id = ce.id and drc.contribution_id = lc.id
  union
  select pcs.synopsis source, 'persona_characteristic' source_type, drs.synopsis target, 'document_reference' target_type, ce.name means_end, lc.name contribution from document_reference_contribution drc, document_reference_synopsis drs, persona_characteristic_synopsis pcs, contribution_end ce, link_contribution lc where drc.characteristic_id = drs.id and drc.reference_id = pcs.characteristic_id and drc.end_id = ce.id and drc.contribution_id = lc.id
  union
  select drs.synopsis source, 'document_reference' source_type, drst.synopsis target, 'document_reference' target_type, ce.name means_end, lc.name contribution from document_reference_contribution drc, document_reference_synopsis drs, document_reference_synopsis drst, contribution_end ce, link_contribution lc where drc.reference_id = drs.id and drc.characteristic_id = drst.id and drc.end_id = ce.id and drc.contribution_id = lc.id
  union
  select pcs2.synopsis source, 'persona_characteristic' source_type, pcs.synopsis target, 'persona_characteristic' target_type, ce.name means_end, lc.name contribution from document_reference_contribution drc, persona_characteristic_synopsis pcs2, persona_characteristic_synopsis pcs, contribution_end ce, link_contribution lc where drc.reference_id = pcs2.characteristic_id and drc.characteristic_id = pcs.characteristic_id and drc.end_id = ce.id and drc.contribution_id = lc.id;

CREATE VIEW usecase_step_synopsis_actor as
  select uss.id,uss.usecase_id,uss.step_no,uss.environment_id,uss.synopsis,r.name actor,td.name actor_type from usecase_step_synopsis uss, role r, trace_dimension td where uss.actor_id = r.id and uss.actor_type_id = td.id
  union
  select uss.id,uss.usecase_id,uss.step_no,uss.environment_id,uss.synopsis,a.name actor,td.name actor_type from usecase_step_synopsis uss, asset a, trace_dimension td where uss.actor_id = a.id and uss.actor_type_id = td.id
  union
  select uss.id,uss.usecase_id,uss.step_no,uss.environment_id,uss.synopsis,c.name actor,td.name actor_type from usecase_step_synopsis uss, component c, trace_dimension td where uss.actor_id = c.id and uss.actor_type_id = td.id;


CREATE VIEW environment_risk as
  select r.id,et.environment_id from risk r, environment_threat et, environment_vulnerability ev where r.threat_id = et.threat_id and et.environment_id = ev.environment_id and ev.vulnerability_id = r.vulnerability_id
  union 
  select r.id,ev.environment_id from risk r, environment_vulnerability ev, environment_threat et where r.vulnerability_id = ev.vulnerability_id and ev.environment_id = et.environment_id and et.threat_id = r.threat_id;

CREATE VIEW environment_trust_boundary as
  select distinct environment_id, trust_boundary_id from trust_boundary_asset
  union
  select distinct environment_id, trust_boundary_id from trust_boundary_usecase;

CREATE VIEW environment_role as
  select distinct environment_id, subgoal_id role_id from responserole_goalassociation
  union
  select distinct environment_id, role_id from countermeasure_role
  union
  select distinct environment_id, role_id from persona_role
  union
  select distinct environment_id, depender_id from rolegoalrole_dependency
  union
  select distinct environment_id, dependee_id from rolegoalrole_dependency
  union
  select distinct environment_id, depender_id from roleassetrole_dependency
  union
  select distinct environment_id, dependee_id from roleassetrole_dependency
  union
  select distinct environment_id, depender_id from roletaskrole_dependency
  union
  select distinct environment_id, dependee_id from roletaskrole_dependency
  union
  select distinct environment_id, subgoal_id role_id from goalrole_goalassociation
  union
  select distinct environment_id, subgoal_id role_id from obstaclerole_goalassociation
  union
  select distinct environment_id, subgoal_id role_id from requirementrole_goalassociation;


CREATE VIEW detection_mechanism as
  select rm.response_id response_id,rm.environment_id environment_id,ca.asset_id asset_id from response_mitigate rm, countermeasure_threat_response_target ctrt, countermeasure_asset ca where rm.mitigate_type_id = 2 and rm.response_id = ctrt.response_id and rm.environment_id = ctrt.environment_id and ctrt.countermeasure_id = ca.countermeasure_id
  union
  select rm.response_id response_id,rm.environment_id environment_id,ca.asset_id asset_id from response_mitigate rm, countermeasure_vulnerability_response_target cvrt, countermeasure_asset ca where rm.mitigate_type_id = 2 and rm.response_id = cvrt.response_id and rm.environment_id = cvrt.environment_id and cvrt.countermeasure_id = ca.countermeasure_id;


CREATE VIEW concept_reference as
  select ar.id,ar.name,'asset' dimension_name,a.name object_name,ar.description from asset_reference ar, asset a where ar.asset_id = a.id
  union
  select ar.id,ar.name,'attacker' dimension_name,a.name object_name,ar.description from attacker_reference ar, attacker a where ar.attacker_id = a.id
  union
  select cr.id,cr.name,'countermeasure' dimension_name,c.name object_name,cr.description from countermeasure_reference cr, countermeasure c where cr.countermeasure_id = c.id
  union
  select dr.id,dr.name,'domainproperty' dimension_name,d.name object_name,dr.description from domainproperty_reference dr, domainproperty d where dr.domainproperty_id = d.id
  union
  select er.id,er.name,'environment' dimension_name,e.name object_name,er.description from environment_reference er, environment e where er.environment_id = e.id
  union
  select gr.id,gr.name,'goal' dimension_name,g.name object_name,gr.description from goal_reference gr, goal g where gr.goal_id = g.id
  union
  select mr.id,m.name,'misusecase' dimension_name,m.name object_name,mr.description from misusecase_reference mr, misusecase m where mr.misusecase_id = m.id
  union
  select obr.id,obr.name,'obstacle' dimension_name,o.name object_name,obr.description from obstacle_reference obr, obstacle o where obr.obstacle_id = o.id
  union
  select pr.id,pr.name,'persona' dimension_name,p.name object_name,pr.description from persona_reference pr, persona p where pr.persona_id = p.id
  union
  select rr.id,rr.name,'requirement' dimension_name,r.name object_name,rr.description from requirement_reference rr, requirement r, asset a, asset_requirement ar where rr.requirement_id = r.id and r.id = ar.requirement_id and ar.asset_id = a.id and r.version = (select max(i.version) from requirement i where i.id = r.id)
  union
  select rr.id,rr.name,'requirement' dimension_name,r.name object_name,rr.description from requirement_reference rr, requirement r, environment e, environment_requirement er where rr.requirement_id = r.id and r.id = er.requirement_id and er.environment_id = e.id and r.version = (select max(i.version) from requirement i where i.id = r.id)
  union
  select rr.id,rr.name,'risk' dimension_name,r.name object_name,rr.description from risk_reference rr, risk r where rr.risk_id = r.id
  union
  select rr.id,rr.name,'response' dimension_name,r.name object_name,rr.description from response_reference rr, response r where rr.response_id = r.id
  union
  select rr.id,rr.name,'role' dimension_name,r.name object_name,rr.description from role_reference rr, role r where rr.role_id = r.id
  union
  select tr.id,tr.name,'task' dimension_name,t.name object_name,tr.description from task_reference tr, task t where tr.task_id = t.id
  union
  select ur.id,ur.name,'usecase' dimension_name,u.name object_name,ur.description from usecase_reference ur, usecase u where ur.usecase_id = u.id
  union
  select tr.id,tr.name,'threat' dimension_name,t.name object_name,tr.description from threat_reference tr, threat t where tr.threat_id = t.id
  union
  select vr.id,vr.name,'vulnerability' dimension_name,v.name object_name,vr.description from vulnerability_reference vr, vulnerability v where vr.vulnerability_id = v.id;

CREATE VIEW source_reference as
  select id from document_reference
  union
  select id from concept_reference;

CREATE VIEW task_documentconcept_reference as
  select dr.id,t.name task_name, dr.name,'document' dimension_name,ed.name object_name, dr.excerpt description,crt.name reference_type from document_reference dr, external_document ed,characteristic_reference_type crt, task_characteristic_document tcd, task t, task_characteristic tc where dr.document_id = ed.id and dr.id = tcd.reference_id and tcd.characteristic_reference_type_id = crt.id and tcd.characteristic_id = tc.id and tc.task_id = t.id
  union
  select pr.id,t.name task_name, pr.name,'persona' dimension_name,p.name object_name,pr.description,crt.name reference_type from persona_reference pr, task t, persona p, characteristic_reference_type crt, task_characteristic_persona tcp, task_characteristic tc where pr.persona_id = p.id and pr.id = tcp.reference_id and tcp.characteristic_reference_type_id = crt.id and tcp.characteristic_id = tc.id and tc.task_id = t.id
  union
  select ur.id,t.name task_name, ur.name,'usecase' dimension_name,u.name object_name,ur.description,crt.name reference_type from usecase_reference ur, task t, usecase u, characteristic_reference_type crt, task_characteristic_usecase tcu, task_characteristic tc where ur.usecase_id = u.id and ur.id = tcu.reference_id and tcu.characteristic_reference_type_id = crt.id and tcu.characteristic_id = tc.id and tc.task_id = t.id
  union
  select rr.id,t.name task_name, rr.name,'requirement' dimension_name,concat(a.short_code,'-',r.label) object_name,rr.description,crt.name reference_type from requirement_reference rr, requirement r, asset a, asset_requirement ar, characteristic_reference_type crt, task_characteristic_requirement tcr, task_characteristic tc, task t where rr.requirement_id = r.id and r.id = ar.requirement_id and ar.asset_id = a.id and r.version = (select max(i.version) from requirement i where i.id = r.id) and rr.id = tcr.reference_id and tcr.characteristic_reference_type_id = crt.id and tcr.characteristic_id = tc.id and tc.task_id = t.id
  union
  select rr.id,t.name task_name, rr.name,'requirement' dimension_name,concat(e.short_code,'-',r.label) object_name,rr.description,crt.name reference_type from requirement_reference rr, requirement r, environment e, environment_requirement er, characteristic_reference_type crt, task_characteristic_requirement tcr, task_characteristic tc, task t where rr.requirement_id = r.id and r.id = er.requirement_id and er.environment_id = e.id and r.version = (select max(i.version) from requirement i where i.id = r.id) and rr.id = tcr.reference_id and tcr.characteristic_reference_type_id = crt.id and tcr.characteristic_id = tc.id and tc.task_id = t.id;

CREATE VIEW documentconcept_reference as
  select dr.id,p.name persona_name, dr.name,'document' dimension_name,ed.name object_name, dr.excerpt description,crt.name reference_type, bv.name variable_name from document_reference dr, external_document ed,characteristic_reference_type crt, persona_characteristic_document pcd, persona p, persona_characteristic pc, behavioural_variable bv where dr.document_id = ed.id and dr.id = pcd.reference_id and pcd.characteristic_reference_type_id = crt.id and pcd.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select ar.id,p.name persona_name, ar.name,'asset' dimension_name,a.name object_name,ar.description,crt.name reference_type, bv.name variable_name from asset_reference ar, asset a, characteristic_reference_type crt, persona_characteristic_asset pca, persona_characteristic pc, persona p, behavioural_variable bv where ar.asset_id = a.id and ar.id = pca.reference_id and pca.characteristic_reference_type_id = crt.id and pca.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select ar.id,p.name persona_name, ar.name,'attacker' dimension_name,a.name object_name,ar.description,crt.name reference_type, bv.name variable_name from attacker_reference ar, attacker a, characteristic_reference_type crt, persona_characteristic_attacker pca, persona_characteristic pc, persona p, behavioural_variable bv where ar.attacker_id = a.id and ar.id = pca.reference_id = pca.characteristic_reference_type_id = crt.id and pca.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select cr.id,p.name persona_name, cr.name,'countermeasure' dimension_name,c.name object_name,cr.description,crt.name reference_type, bv.name variable_name from countermeasure_reference cr, countermeasure c, characteristic_reference_type crt, persona_characteristic_countermeasure pcc, persona_characteristic pc, persona p, behavioural_variable bv where cr.countermeasure_id = c.id and cr.id = pcc.reference_id and pcc.characteristic_reference_type_id = crt.id and pcc.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select dr.id,p.name persona_name, dr.name,'domainproperty' dimension_name,d.name object_name,dr.description,crt.name reference_type, bv.name variable_name from domainproperty_reference dr, domainproperty d, characteristic_reference_type crt, persona_characteristic_domainproperty pcd, persona_characteristic pc, persona p, behavioural_variable bv where dr.domainproperty_id = d.id and dr.id = pcd.reference_id and pcd.characteristic_reference_type_id = crt.id and pcd.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select er.id,p.name persona_name, er.name,'environment' dimension_name,e.name object_name,er.description,crt.name reference_type, bv.name variable_name from environment_reference er, environment e,characteristic_reference_type crt, persona_characteristic_environment pce, persona_characteristic pc, persona p, behavioural_variable bv where er.environment_id = e.id and er.id = pce.reference_id and pce.characteristic_reference_type_id = crt.id and pce.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select gr.id,p.name persona_name, gr.name,'goal' dimension_name,g.name object_name,gr.description,crt.name reference_type, bv.name variable_name from goal_reference gr, goal g,characteristic_reference_type crt,persona_characteristic_goal pcg, persona_characteristic pc, persona p, behavioural_variable bv where gr.goal_id = g.id and gr.id = pcg.reference_id  and pcg.characteristic_reference_type_id = crt.id and pcg.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select mr.id,p.name persona_name, m.name,'misusecase' dimension_name,m.name object_name,mr.description,crt.name reference_type, bv.name variable_name from misusecase_reference mr, misusecase m, characteristic_reference_type crt, persona_characteristic_misusecase pcm, persona_characteristic pc, persona p, behavioural_variable bv where mr.misusecase_id = m.id and mr.id = pcm.reference_id and pcm.characteristic_reference_type_id = crt.id and pcm.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select obr.id,p.name persona_name, obr.name,'obstacle' dimension_name,o.name object_name,obr.description,crt.name reference_type, bv.name variable_name from obstacle_reference obr, obstacle o, characteristic_reference_type crt, persona_characteristic_obstacle pco, persona_characteristic pc, persona p, behavioural_variable bv where obr.obstacle_id = o.id and obr.id = pco.reference_id and pco.characteristic_reference_type_id = crt.id and pco.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select pr.id,p.name persona_name, pr.name,'persona' dimension_name,p.name object_name,pr.description,crt.name reference_type, bv.name variable_name from persona_reference pr, persona p, characteristic_reference_type crt, persona_characteristic_persona pcp, persona_characteristic pc, behavioural_variable bv where pr.persona_id = p.id and pr.id = pcp.reference_id and pcp.characteristic_reference_type_id = crt.id and pcp.characteristic_id = pc.id and pc.variable_id = bv.id
  union
  select rr.id,p.name persona_name, rr.name,'requirement' dimension_name,concat(a.short_code,'-',r.label) object_name,rr.description,crt.name reference_type, bv.name variable_name from requirement_reference rr, requirement r, asset a, asset_requirement ar, characteristic_reference_type crt, persona_characteristic_requirement pcr, persona_characteristic pc, persona p, behavioural_variable bv where rr.requirement_id = r.id and r.id = ar.requirement_id and ar.asset_id = a.id and r.version = (select max(i.version) from requirement i where i.id = r.id) and rr.id = pcr.reference_id and pcr.characteristic_reference_type_id = crt.id and pcr.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select rr.id,p.name persona_name, rr.name,'requirement' dimension_name,concat(e.short_code,'-',r.label) object_name,rr.description,crt.name reference_type, bv.name variable_name from requirement_reference rr, requirement r, environment e, environment_requirement er, characteristic_reference_type crt, persona_characteristic_requirement pcr, persona_characteristic pc, persona p, behavioural_variable bv where rr.requirement_id = r.id and r.id = er.requirement_id and er.environment_id = e.id and r.version = (select max(i.version) from requirement i where i.id = r.id) and rr.id = pcr.reference_id and pcr.characteristic_reference_type_id = crt.id and pcr.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select rr.id,p.name persona_name, rr.name,'risk' dimension_name,r.name object_name,rr.description,crt.name reference_type, bv.name variable_name from risk_reference rr, risk r, characteristic_reference_type crt, persona_characteristic_risk pcr, persona_characteristic pc, persona p, behavioural_variable bv where rr.risk_id = r.id and rr.id = pcr.reference_id and pcr.characteristic_reference_type_id = crt.id and pcr.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select rr.id,p.name persona_name, rr.name,'response' dimension_name,r.name object_name,rr.description,crt.name reference_type, bv.name variable_name from response_reference rr, response r, characteristic_reference_type crt, persona_characteristic_response pcr, persona_characteristic pc, persona p, behavioural_variable bv where rr.response_id = r.id and rr.id = pcr.reference_id and pcr.characteristic_reference_type_id = crt.id and pcr.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select rr.id,p.name persona_name, rr.name,'role' dimension_name,r.name object_name,rr.description,crt.name reference_type, bv.name variable_name from role_reference rr, role r, characteristic_reference_type crt, persona_characteristic_role pcr, persona_characteristic pc, persona p, behavioural_variable bv where rr.role_id = r.id and rr.id = pcr.reference_id and pcr.characteristic_reference_type_id = crt.id and pcr.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select tr.id,p.name persona_name, tr.name,'task' dimension_name,t.name object_name,tr.description,crt.name reference_type, bv.name variable_name from task_reference tr, task t, characteristic_reference_type crt, persona_characteristic_task pct, persona_characteristic pc, persona p, behavioural_variable bv where tr.task_id = t.id and tr.id = pct.reference_id and pct.characteristic_reference_type_id = crt.id and pct.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select tr.id,p.name persona_name, tr.name,'usecase' dimension_name,t.name object_name,tr.description,crt.name reference_type, bv.name variable_name from usecase_reference tr, task t, characteristic_reference_type crt, persona_characteristic_usecase pct, persona_characteristic pc, persona p, behavioural_variable bv where tr.usecase_id = t.id and tr.id = pct.reference_id and pct.characteristic_reference_type_id = crt.id and pct.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select tr.id,p.name persona_name, tr.name,'threat' dimension_name,t.name object_name,tr.description,crt.name reference_type, bv.name variable_name from threat_reference tr, threat t, characteristic_reference_type crt, persona_characteristic_threat pct, persona_characteristic pc, persona p, behavioural_variable bv where tr.threat_id = t.id and tr.id = pct.reference_id and pct.characteristic_reference_type_id = crt.id and pct.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id
  union
  select vr.id,p.name persona_name, vr.name,'vulnerability' dimension_name,v.name object_name,vr.description,crt.name reference_type, bv.name variable_name from vulnerability_reference vr, vulnerability v, characteristic_reference_type crt, persona_characteristic_vulnerability pcv, persona p, persona_characteristic pc, behavioural_variable bv where vr.vulnerability_id = v.id and vr.id = pcv.reference_id and pcv.characteristic_reference_type_id = crt.id and pcv.characteristic_id = pc.id and pc.persona_id = p.id and pc.variable_id = bv.id;


CREATE VIEW assumption_task_model as
  select pc.description from_name, 'task_characteristic' from_dim, p.name to_name, 'task' to_dim, p.name task_name, pc.description characteristic_name from task p, task_characteristic pc where p.id = pc.task_id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name,pc.description characteristic_name from task_characteristic pc, task_characteristic_document pcc, document_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.task_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_persona pcc, persona_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.task_id = p.id 
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_usecase pcc, usecase_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.task_id = p.id 
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_requirement pcc, requirement_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.task_id = p.id 
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name,pc.description characteristic_name from task_characteristic pc, task_characteristic_document pcc, document_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.task_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_persona pcc, persona_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.task_id = p.id 
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_usecase pcc, usecase_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.task_id = p.id 
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_requirement pcc, requirement_reference cr, task p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.task_id = p.id 
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name task_name, pc.description characteristic_name from external_document c, document_reference cr, task_characteristic_document pcc, task_characteristic pc, task p where pcc.reference_id = cr.id and cr.document_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.task_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name task_name, pc.description characteristic_name from persona c, persona_reference cr, task_characteristic_persona pcc, task_characteristic pc, task p where pcc.reference_id = cr.id and cr.persona_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.task_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name task_name, pc.description characteristic_name from usecase c, usecase_reference cr, task_characteristic_usecase pcc, task_characteristic pc, task p where pcc.reference_id = cr.id and cr.usecase_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.task_id = p.id
  union
  select concat(a.short_code,'-',c.label) from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name task_name, pc.description characteristic_name from requirement c, requirement_reference cr, task_characteristic_requirement pcc, task_characteristic pc, task p, asset a, asset_requirement ar where pcc.reference_id = cr.id and cr.requirement_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.task_id = p.id and c.id = ar.requirement_id and ar.asset_id = a.id and c.version = (select max(i.version) from requirement i where i.id = c.id)
  union
  select concat(e.short_code,'-',c.label) from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name task_name, pc.description characteristic_name from requirement c, requirement_reference cr, task_characteristic_requirement pcc, task_characteristic pc, task p, environment e, environment_requirement er where pcc.reference_id = cr.id and cr.requirement_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.task_id = p.id and c.id = er.requirement_id and er.environment_id = e.id and c.version = (select max(i.version) from requirement i where i.id = c.id)
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'task_characteristic' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_document pcc, document_reference cr, task p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.task_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'task_characteristic' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_persona pcc, persona_reference cr, task p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.task_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'task_characteristic' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_usecase pcc, usecase_reference cr, task p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.task_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'task_characteristic' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task_characteristic_requirement pcc, requirement_reference cr, task p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.task_id = p.id
  union
  select pc.qualifier from_name, 'qualifier' from_dim, concat('qual_',pc.description) to_name, 'qual' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task p where pc.task_id = p.id
  union
  select concat('gwb_',pc.description) from_name, 'gwb' from_dim, concat('qual_',pc.description) to_name, 'qual' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task p where pc.task_id = p.id
  union
  select concat('qual_',pc.description) from_name, 'qual' from_dim, pc.description to_name, 'task_characteristic' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task p where pc.task_id = p.id
  union
  select t.name from_name, 'task' from_dim, dp.name to_name, 'domainproperty' to_dim, t.name task_name, '' characteristic_name from task t, domainproperty dp,domainproperty_task dt where dt.task_id = t.id and dt.task_id = dt.task_id and dt.domainproperty_id = dp.id;


CREATE VIEW assumption_persona_model as
  select pc.description from_name, 'persona_characteristic' from_dim, p.name to_name, 'persona' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona p, persona_characteristic pc, behavioural_variable bv where p.id = pc.persona_id and pc.variable_id = bv.id
  union
  select ic.synopsis from_name,'implied_characteristic' from_dim, p.name to_name, 'persona' to_dim, p.name persona_name, bv.name bv_name,ic.synopsis characteristic_name from persona p, implied_characteristic ic, behavioural_variable bv, persona_code_network pcn where p.id = pcn.persona_id and pcn.id = ic.persona_code_network_id and ic.variable_id = bv.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_document pcc, document_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select idc.label from_name, 'grounds' from_dim, concat('gwb_',ic.synopsis) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,ic.synopsis characteristic_name from implied_characteristic ic, internal_document_code idc, implied_characteristic_element ice, behavioural_variable bv, persona p, persona_code_network pcn where p.id = pcn.persona_id and pcn.id = ic.persona_code_network_id and ic.variable_id = bv.id and ic.id = ice.implied_characteristic_id and ice.internal_document_id = idc.internal_document_id and ice.code_id = idc.code_id and ice.start_index = idc.start_index and ice.end_index = idc.end_index and ice.characteristic_reference_type_id = 0
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_asset pcc, asset_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_attacker pcc, attacker_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_countermeasure pcc, countermeasure_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_domainproperty pcc, domainproperty_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_environment pcc, environment_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_goal pcc, goal_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_misusecase pcc, misusecase_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_obstacle pcc, obstacle_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_persona pcc, persona_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_requirement pcc, requirement_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_response pcc, response_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_risk pcc, risk_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_role pcc, role_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_task pcc, task_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_usecase pcc, usecase_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_threat pcc, threat_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_vulnerability pcc, vulnerability_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_document pcc,document_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_asset pcc,asset_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_attacker pcc,attacker_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_countermeasure pcc,countermeasure_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_domainproperty pcc, domainproperty_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_environment pcc, environment_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_goal pcc, goal_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_misusecase pcc, misusecase_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_obstacle pcc, obstacle_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_persona pcc, persona_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_requirement pcc, requirement_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_response pcc, response_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_risk pcc, risk_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_role pcc, role_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_task pcc, task_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_usecase pcc, usecase_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_threat pcc, threat_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'warrant' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_vulnerability pcc, vulnerability_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 1 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select idc.label from_name, 'warrant' from_dim, concat('gwb_',ic.synopsis) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,ic.synopsis characteristic_name from implied_characteristic ic, internal_document_code idc, implied_characteristic_element ice, behavioural_variable bv, persona p, persona_code_network pcn where p.id = pcn.persona_id and pcn.id = ic.persona_code_network_id and ic.variable_id = bv.id and ic.id = ice.implied_characteristic_id and ice.internal_document_id = idc.internal_document_id and ice.code_id = idc.code_id and ice.start_index = idc.start_index and ice.end_index = idc.end_index and ice.characteristic_reference_type_id = 1
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from external_document c, document_reference cr, persona_characteristic_document pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.document_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, idc.label to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,ic.synopsis characteristic_name from internal_document c, internal_document_code idc, implied_characteristic_element ice, implied_characteristic ic, persona_code_network pcn, persona p, behavioural_variable bv where idc.internal_document_id = c.id and idc.internal_document_id = ice.internal_document_id and idc.code_id = ice.code_id and idc.start_index = ice.start_index and idc.end_index = ice.end_index and ice.implied_characteristic_id = ic.id and ic.persona_code_network_id = pcn.id and pcn.persona_id = p.id and ic.variable_id = bv.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from asset c, asset_reference cr, persona_characteristic_asset pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.asset_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from attacker c, attacker_reference cr, persona_characteristic_attacker pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.attacker_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from countermeasure c, countermeasure_reference cr, persona_characteristic_countermeasure pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.countermeasure_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from domainproperty c, domainproperty_reference cr, persona_characteristic_domainproperty pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.domainproperty_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from environment c, environment_reference cr, persona_characteristic_environment pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.environment_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from goal c, goal_reference cr, persona_characteristic_goal pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.goal_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from misusecase c, misusecase_reference cr, persona_characteristic_misusecase pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.misusecase_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from obstacle c, obstacle_reference cr, persona_characteristic_obstacle pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.obstacle_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona c, persona_reference cr, persona_characteristic_persona pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.persona_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select concat(a.short_code,'-',c.label) from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from requirement c, asset a, asset_requirement ar, requirement_reference cr, persona_characteristic_requirement pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.requirement_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id and c.id = ar.requirement_id and ar.asset_id = a.id and c.version = (select max(i.version) from requirement i where i.id = c.id)
  union
  select concat(e.short_code,'-',c.label) from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from requirement c, environment e, environment_requirement er, requirement_reference cr, persona_characteristic_requirement pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.requirement_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id and c.id = er.requirement_id and er.environment_id = e.id and c.version = (select max(i.version) from requirement i where i.id = c.id)
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from response c, response_reference cr, persona_characteristic_response pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.response_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from risk c, risk_reference cr, persona_characteristic_risk pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.risk_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from role c, role_reference cr, persona_characteristic_role pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.role_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from task c, task_reference cr, persona_characteristic_task pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.task_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from usecase c, usecase_reference cr, persona_characteristic_usecase pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.usecase_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from threat c, threat_reference cr, persona_characteristic_threat pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.threat_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from vulnerability c, vulnerability_reference cr, persona_characteristic_vulnerability pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.vulnerability_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select concat('gwb_',pc.description) from_name, 'gwb' from_dim, concat('qual_',pc.description) to_name, 'qual' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, behavioural_variable bv, persona p where pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select concat('gwb_',ic.synopsis) from_name, 'gwb' from_dim, concat('qual_',ic.synopsis) to_name, 'qual' to_dim, p.name persona_name, bv.name bv_name,ic.synopsis characteristic_name from implied_characteristic ic, behavioural_variable bv, persona p,persona_code_network pcn where ic.variable_id = bv.id and ic.persona_code_network_id = pcn.id and pcn.persona_id = p.id
  union
  select concat('qual_',pc.description) from_name, 'qual' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, behavioural_variable bv, persona p where pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select concat('qual_',ic.synopsis) from_name, 'qual' from_dim, ic.synopsis to_name, 'implied_characteristic' to_dim, p.name persona_name, bv.name bv_name,ic.synopsis characteristic_name from implied_characteristic ic, behavioural_variable bv, persona p, persona_code_network pcn where ic.variable_id = bv.id and ic.persona_code_network_id = pcn.id and pcn.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_document pcc, document_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_asset pcc, asset_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_attacker pcc, attacker_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_countermeasure pcc, countermeasure_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_domainproperty pcc, domainproperty_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_environment pcc, environment_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_goal pcc, goal_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_misusecase pcc, misusecase_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_obstacle pcc, obstacle_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_persona pcc, persona_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_requirement pcc, requirement_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_response pcc, response_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_risk pcc, risk_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_role pcc, role_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_task pcc, task_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_usecase pcc, usecase_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_threat pcc, threat_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select idc.label from_name, 'rebuttal' from_dim, ic.synopsis to_name, 'implied_characteristic' to_dim, p.name persona_name, bv.name bv_name,ic.synopsis characteristic_name from implied_characteristic ic, internal_document_code idc, implied_characteristic_element ice, behavioural_variable bv, persona p, persona_code_network pcn where p.id = pcn.persona_id and pcn.id = ic.persona_code_network_id and ic.variable_id = bv.id and ic.id = ice.implied_characteristic_id and ice.internal_document_id = idc.internal_document_id and ice.code_id = idc.code_id and ice.start_index = idc.start_index and ice.end_index = idc.end_index and ice.characteristic_reference_type_id = 2
  union
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_vulnerability pcc, vulnerability_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select pc.qualifier from_name, 'qualifier' from_dim, concat('qual_',pc.description) to_name, 'qual' to_dim, p.name persona_name, bv.name bv_name, pc.description characteristic_name from persona_characteristic pc, behavioural_variable bv, persona p where pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select ic.qualifier from_name, 'qualifier' from_dim, concat('qual_',ic.synopsis) to_name, 'qual' to_dim, p.name persona_name, bv.name bv_name, ic.synopsis characteristic_name from implied_characteristic ic, persona_code_network pcn, behavioural_variable bv, persona p where ic.variable_id = bv.id and ic.persona_code_network_id = pcn.id and pcn.persona_id = p.id;

CREATE VIEW concept_map as
  select fr.name from_name, tr.name to_name, rr.label from requirement fr, requirement tr, requirement_requirement rr where rr.from_id = fr.id and fr.version = (select max(i.version) from requirement i where i.id = fr.id) and rr.to_id = tr.id and tr.version = (select max(i.version) from requirement i where i.id = tr.id); 

CREATE VIEW component_interfaces as
  select c.name component,i.name interface,ci.required_id from component c, interface i, component_interface ci where ci.component_id = c.id and ci.interface_id = i.id;

CREATE VIEW connectors as
  select ca.name connector, fc.name from_name, fi.name from_interface, tc.name to_name, ti.name to_interface from connector ca, component fc, component tc, interface fi, interface ti where ca.from_component_id = fc.id and ca.from_interface_id = fi.id and ca.to_component_id = tc.id and ca.to_interface_id = ti.id;

CREATE VIEW component_asset as
  select component_id, head_id asset_id from component_classassociation
  union
  select component_id, tail_id asset_id from component_classassociation;

CREATE VIEW asset_template_asset as
  select template_asset_id, asset_id from component_asset_template_asset
  union
  select template_asset_id, asset_id from securitypattern_asset_template_asset;

CREATE VIEW component_requirement as
  select ctr.label, ctr.component_id, tr.type_id, tr.name, tr.description, tr.rationale, tr.fit_criterion, tr.asset_id from component_template_requirement ctr, template_requirement tr where ctr.template_requirement_id = tr.id;

CREATE VIEW component_goal as
  select ctg.component_id, tg.name, tg.definition, tg.rationale from component_template_goal ctg, template_goal tg where ctg.template_goal_id = tg.id;

CREATE VIEW securitypattern_requirement as
  select str.label, str.pattern_id, tr.type_id, tr.name, tr.description, tr.rationale, tr.fit_criterion, tr.asset_id from securitypattern_template_requirement str, template_requirement tr where str.template_requirement_id = tr.id;

CREATE VIEW misusability_case as
  select id,name from task where id in (select task_id from task_characteristic);

CREATE VIEW quotation as
   select c.name code,'internal_document' artifact_type,ind.name artifact_name,'None' section,idc.start_index,idc.end_index,internalDocumentQuotationString(ind.name,idc.start_index,idc.end_index) quote,idc.synopsis,idc.label from code c, internal_document ind, internal_document_code idc where c.id = idc.code_id and ind.id = idc.internal_document_id
   union
   select c.name code,'persona' artifact_type,p.name artifact_name,'Activities' section,pc.start_index,pc.end_index,personaQuotationString(p.name,'activities',pc.start_index,pc.end_index) quote,pc.synopsis,pc.label from code c, persona p, persona_code pc where c.id = pc.code_id and p.id = pc.persona_id
   union
   select c.name code,'persona' artifact_type,p.name artifact_name,'Attitudes' section,pc.start_index,pc.end_index,personaQuotationString(p.name,'attitudes',pc.start_index,pc.end_index) quote,pc.synopsis,pc.label from code c, persona p, persona_code pc where c.id = pc.code_id and p.id = pc.persona_id
   union
   select c.name code,'persona' artifact_type,p.name artifact_name,'Aptitudes' section,pc.start_index,pc.end_index,personaQuotationString(p.name,'attitudes',pc.start_index,pc.end_index) quote,pc.synopsis,pc.label from code c, persona p, persona_code pc where c.id = pc.code_id and p.id = pc.persona_id
   union
   select c.name code,'persona' artifact_type,p.name artifact_name,'Motivations' section,pc.start_index,pc.end_index,personaQuotationString(p.name,'motivations',pc.start_index,pc.end_index) quote,pc.synopsis,pc.label from code c, persona p, persona_code pc where c.id = pc.code_id and p.id = pc.persona_id
   union
   select c.name code,'persona' artifact_type,p.name artifact_name,'Skills' section,pc.start_index,pc.end_index,personaQuotationString(p.name,'skills',pc.start_index,pc.end_index) quote,pc.synopsis,pc.label from code c, persona p, persona_code pc where c.id = pc.code_id and p.id = pc.persona_id
   union
   select c.name code,'persona' artifact_type,p.name artifact_name,'Intrinsic' section,pc.start_index,pc.end_index,personaQuotationString(p.name,'intrinsic',pc.start_index,pc.end_index) quote,pc.synopsis,pc.label from code c, persona p, persona_code pc where c.id = pc.code_id and p.id = pc.persona_id
   union
   select c.name code,'persona' artifact_type,p.name artifact_name,'Contextual' section,pc.start_index,pc.end_index,personaQuotationString(p.name,'contextual',pc.start_index,pc.end_index) quote,pc.synopsis,pc.label from code c, persona p, persona_code pc where c.id = pc.code_id and p.id = pc.persona_id order by 1;

CREATE VIEW personal_information as
  select a.id asset_id, rar.environment_id environment_id from asset a, asset_type at, roleassetrole_dependency rar,role dr, role_type drt, role de, role_type det where rar.dependency_id = a.id and rar.depender_id = dr.id and dr.role_type_id = drt.id and drt.name = 'Data Controller' and rar.dependee_id = de.id and de.role_type_id = det.id and det.name = 'Data Subject' and a.asset_type_id = at.id and at.name = 'Information';

CREATE VIEW process_asset as
  select dpp.to_id usecase_id,dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_process_process dpp where df.id = dfa.dataflow_id and df.id = dpp.dataflow_id
  union
  select dep.to_id usecase_id, dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_entity_process dep where df.id = dfa.dataflow_id and df.id = dep.dataflow_id
  union
  select ddp.to_id usecase_id, dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_datastore_process ddp where df.id = dfa.dataflow_id and df.id = ddp.dataflow_id;

CREATE VIEW process_personal_information as
  select dpp.to_id usecase_id,dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_process_process dpp, personal_information pi where df.id = dfa.dataflow_id and df.id = dpp.dataflow_id and df.environment_id = pi.environment_id and dfa.asset_id = pi.asset_id
  union
  select dep.to_id usecase_id, dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_entity_process dep, personal_information pi where df.id = dfa.dataflow_id and df.id = dep.dataflow_id and df.environment_id = pi.environment_id and dfa.asset_id = pi.asset_id
  union
  select ddp.to_id usecase_id, dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_datastore_process ddp, personal_information pi where df.id = dfa.dataflow_id and df.id = ddp.dataflow_id and df.environment_id = pi.environment_id and dfa.asset_id = pi.asset_id;


CREATE VIEW datastore_asset as
  select dpd.to_id datastore_id, dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_process_datastore dpd where df.id = dfa.dataflow_id and df.id = dpd.dataflow_id;


CREATE VIEW datastore_personal_information as
  select dpd.to_id datastore_id, dfa.asset_id asset_id,df.environment_id environment_id from dataflow df, dataflow_asset dfa, dataflow_process_datastore dpd, personal_information pi where df.id = dfa.dataflow_id and df.id = dpd.dataflow_id and dfa.asset_id = pi.asset_id and df.environment_id = pi.environment_id;

CREATE VIEW personal_dataflows as
  select d.name dataflow, e.name environment,fp.name from_name,'process' from_type,tp.name to_name,'process' to_type from dataflow d, dataflow_process_process dpp, usecase fp, usecase tp, environment e, dataflow_asset dfa, personal_information pi where d.id = dpp.dataflow_id and d.environment_id = e.id and dpp.from_id = fp.id and dpp.to_id = tp.id and d.id = dfa.dataflow_id and dfa.asset_id = pi.asset_id and d.environment_id = pi.environment_id
  union
  select d.name dataflow, e.name environment, fe.name from_name, 'entity' from_type, tp.name to_name, 'process' to_type from dataflow d, dataflow_entity_process dep, asset fe, usecase tp, environment e, dataflow_asset dfa, personal_information pi where d.id = dep.dataflow_id and d.environment_id = e.id and dep.from_id = fe.id and dep.to_id = tp.id and d.id = dfa.dataflow_id and dfa.asset_id = pi.asset_id and d.environment_id = pi.environment_id
  union
  select d.name dataflow, e.name environment, fp.name from_name, 'process' from_type, te.name to_name, 'entity' to_type from dataflow d, dataflow_process_entity dpe, usecase fp, asset te, environment e, dataflow_asset dfa, personal_information pi where d.id = dpe.dataflow_id and d.environment_id = e.id and dpe.from_id = fp.id and dpe.to_id = te.id and d.id = dfa.dataflow_id and dfa.asset_id = pi.asset_id and d.environment_id = pi.environment_id
  union
  select d.name dataflow, e.name environment, fd.name from_name, 'datastore' from_type, tp.name to_name, 'process' to_type from dataflow d, dataflow_datastore_process ddp, asset fd, usecase tp, environment e, dataflow_asset dfa, personal_information pi where d.id = ddp.dataflow_id and d.environment_id = e.id and ddp.from_id = fd.id and ddp.to_id = tp.id and d.id = dfa.dataflow_id and dfa.asset_id = pi.asset_id and d.environment_id = pi.environment_id
  union
  select d.name dataflow, e.name environment, fp.name from_name, 'process' from_type, td.name to_name, 'datastore' to_type from dataflow d, dataflow_process_datastore dpd, usecase fp, asset td, environment e, dataflow_asset dfa, personal_information pi where d.id = dpd.dataflow_id and d.environment_id = e.id and dpd.from_id = fp.id and dpd.to_id = td.id and d.id = dfa.dataflow_id and dfa.asset_id = pi.asset_id and d.environment_id = pi.environment_id;

CREATE VIEW personal_risk as
  select r.id,r.name,r.threat_id,r.vulnerability_id,r.intent from risk r, asset_threat at, personal_information pi where r.threat_id = at.threat_id and at.asset_id = pi.asset_id and at.environment_id = pi.environment_id
  union
  select r.id,r.name,r.threat_id,r.vulnerability_id,r.intent from risk r, asset_vulnerability av, personal_information pi where r.vulnerability_id = av.vulnerability_id and av.asset_id = pi.asset_id and av.environment_id = pi.environment_id;

CREATE VIEW goal_associations as
  select ga.id, e.name environment, hg.name goal, 'goal' goal_dim, rt.name ref_type, tg.name subgoal, 'goal' subgoal_dim, ga.alternative_id, ga.rationale from goalgoal_goalassociation ga, environment e, goal hg, goal tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'goal' goal_dim, rt.name ref_type, tg.name subgoal, 'requirement' subgoal_dim, ga.alternative_id, ga.rationale from goalrequirement_goalassociation ga, environment e, goal hg, requirement tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'goal' goal_dim, rt.name ref_type, tg.name subgoal, 'task' subgoal_dim, ga.alternative_id, ga.rationale from goaltask_goalassociation ga, environment e, goal hg, task tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'goal' goal_dim, rt.name ref_type, tg.name subgoal, 'usecase' subgoal_dim, ga.alternative_id, ga.rationale from goalusecase_goalassociation ga, environment e, goal hg, usecase tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'misusecase' subgoal_dim, ga.alternative_id, ga.rationale from obstaclemisusecase_goalassociation ga, environment e, obstacle hg, misusecase tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'requirement' goal_dim, rt.name ref_type, tg.name subgoal, 'goal' subgoal_dim, ga.alternative_id, ga.rationale from requirementgoal_goalassociation ga, environment e, requirement hg, goal tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'requirement' goal_dim, rt.name ref_type, tg.name subgoal, 'requirement' subgoal_dim, ga.alternative_id, ga.rationale from requirementrequirement_goalassociation ga, environment e, requirement hg, requirement tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'goal' goal_dim, rt.name ref_type, tg.name subgoal, 'role' subgoal_dim, ga.alternative_id, ga.rationale from goalrole_goalassociation ga, environment e, goal hg, role tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'requirement' goal_dim, rt.name ref_type, tg.name subgoal, 'role' subgoal_dim, ga.alternative_id, ga.rationale from requirementrole_goalassociation ga, environment e, requirement hg, role tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select -1, e.name environment, hg.name goal, 'response' goal_dim, rt.name ref_type, tg.name subgoal, 'role' subgoal_dim, ga.alternative_id, ga.rationale from responserole_goalassociation ga, environment e, response hg, role tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'countermeasure' goal_dim, rt.name ref_type, tg.name subgoal, 'task' subgoal_dim, ga.alternative_id, ga.rationale from countermeasuretask_goalassociation ga, environment e, countermeasure hg, task tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'goal' goal_dim, rt.name ref_type, tg.name subgoal, 'domainproperty' subgoal_dim, ga.alternative_id, ga.rationale from goaldomainproperty_goalassociation ga, environment e, goal hg, domainproperty tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'goal' goal_dim, rt.name ref_type, tg.name subgoal, 'obstacle' subgoal_dim, ga.alternative_id, ga.rationale from goalobstacle_goalassociation ga, environment e, goal hg, obstacle tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'domainproperty' goal_dim, rt.name ref_type,  tg.name subgoal, 'obstacle' subgoal_dim, ga.alternative_id, ga.rationale from domainpropertyobstacle_goalassociation ga, environment e, domainproperty hg, obstacle tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'obstacle' subgoal_dim, ga.alternative_id, ga.rationale from obstacleobstacle_goalassociation ga, environment e, obstacle hg, obstacle tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'goal' subgoal_dim, ga.alternative_id, ga.rationale from obstaclegoal_goalassociation ga, environment e, obstacle hg, goal tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'domainproperty' subgoal_dim, ga.alternative_id, ga.rationale from obstacledomainproperty_goalassociation ga, environment e, obstacle hg, domainproperty tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'requirement' subgoal_dim, ga.alternative_id, ga.rationale from obstaclerequirement_goalassociation ga, environment e, obstacle hg, requirement tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'requirement' goal_dim, rt.name ref_type, tg.name subgoal, 'obstacle' subgoal_dim, ga.alternative_id, ga.rationale from requirementobstacle_goalassociation ga, environment e, requirement hg, obstacle tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'threat' subgoal_dim, ga.alternative_id, ga.rationale from obstaclethreat_goalassociation ga, environment e, obstacle hg, threat tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'vulnerability' subgoal_dim, ga.alternative_id, ga.rationale from obstaclevulnerability_goalassociation ga, environment e, obstacle hg, vulnerability tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'task' subgoal_dim, ga.alternative_id, ga.rationale from obstacletask_goalassociation ga, environment e, obstacle hg, task tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'usecase' subgoal_dim, ga.alternative_id, ga.rationale from obstacleusecase_goalassociation ga, environment e, obstacle hg, usecase tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id
  union
  select ga.id, e.name environment, hg.name goal, 'obstacle' goal_dim, rt.name ref_type, tg.name subgoal, 'role' subgoal_dim, ga.alternative_id, ga.rationale from obstaclerole_goalassociation ga, environment e, obstacle hg, role tg, reference_type rt where ga.environment_id = e.id and ga.goal_id = hg.id and ga.subgoal_id = tg.id and ga.ref_type_id = rt.id;

CREATE VIEW riskModel_tagged as
  select t.name tag, a.name object, e.name environment from attacker_tag at, attacker a, tag t, environment_attacker ea, environment e where t.id = at.tag_id and a.id = at.attacker_id and at.attacker_id = ea.attacker_id and ea.environment_id = e.id
  union
  select t.name tag, a.name object, e.name environment from asset_tag at, asset a, tag t, environment_asset ea, environment e where t.id = at.tag_id and a.id = at.asset_id and at.asset_id = ea.asset_id and ea.environment_id = e.id
  union
  select t.name tag, v.name object, e.name environment from vulnerability_tag vt, vulnerability v, tag t, environment_vulnerability  ev, environment e where t.id = vt.tag_id and v.id = vt.vulnerability_id and vt.vulnerability_id = ev.vulnerability_id and ev.environment_id = e.id
  union
  select t.name tag, th.name object, e.name environment from threat_tag tt, threat th, tag t, environment_threat et, environment e where t.id = tt.tag_id and th.id = tt.threat_id and tt.threat_id = et.threat_id and et.environment_id = e.id
  union
  select t.name tag, r.name object, e.name environment from risk_tag rt, risk r, tag t, environment_risk er, environment e where t.id = rt.tag_id and r.id = rt.risk_id and rt.risk_id = er.id and er.environment_id = e.id;

CREATE VIEW conceptMapModel_all as
  select fr.name from_name, tr.name to_name, rr.label,e.name from_objt,te.name to_objt from requirement fr, requirement tr, requirement_requirement rr,environment_requirement er, environment_requirement fer, environment e, environment te where rr.from_id = fr.id and fr.version = (select max(i.version) from requirement i where i.id = fr.id) and tr.version = (select max(i.version) from requirement i where i.id = tr.id) and rr.to_id = tr.id and tr.version = (select max(i.version) from requirement i where i.id = tr.id) and tr.id = er.requirement_id and rr.from_id = fer.requirement_id and fer.environment_id = e.id and rr.to_id = er.requirement_id and er.environment_id = te.id
  union
  select fr.name from_name, tr.name to_name, rr.label,fe.name from_objt,e.name to_objt from requirement fr, requirement tr, requirement_requirement rr,environment_requirement er, environment_requirement fer, environment fe, environment e where rr.from_id = fr.id and fr.version = (select max(i.version) from requirement i where i.id = fr.id) and tr.version = (select max(i.version) from requirement i where i.id = tr.id) and rr.to_id = tr.id and tr.version = (select max(i.version) from requirement i where i.id = tr.id) and fr.id = er.requirement_id and rr.to_id = fer.requirement_id and fer.environment_id = e.id and rr.from_id = er.requirement_id and er.environment_id = fe.id
  union
  select fr.name from_name, tr.name to_name, rr.label,fa.name from_objt,ta.name to_objt from requirement fr, requirement tr, requirement_requirement rr,asset_requirement far, asset_requirement tar, asset fa, asset ta, environment_asset fea, environment_asset tea where rr.from_id = fr.id and fr.version = (select max(i.version) from requirement i where i.id = fr.id) and fr.id = far.requirement_id and far.asset_id = fa.id and fa.id = fea.asset_id and rr.to_id = tr.id and tr.version = (select max(i.version) from requirement i where i.id = tr.id) and tr.id = tar.requirement_id and tar.asset_id = ta.id and ta.id = tea.asset_id
  union
  select fr.name from_name, tr.name to_name, rr.label,fe.name from_objt,ta.name to_objt from requirement fr, requirement tr, requirement_requirement rr,environment_requirement fer, asset_requirement tar, environment fe, asset ta, environment_asset tea where rr.from_id = fr.id and fr.version = (select max(i.version) from requirement i where i.id = fr.id) and fr.id = fer.requirement_id and fer.environment_id = fe.id and rr.to_id = tr.id and tr.version = (select max(i.version) from requirement i where i.id = tr.id) and tr.id = tar.requirement_id and tar.asset_id = ta.id and ta.id = tea.asset_id
  union
  select fr.name from_name, tr.name to_name, rr.label,fa.name from_objt,te.name to_objt from requirement fr, requirement tr, requirement_requirement rr, asset_requirement far, asset fa, environment_asset fea, environment_requirement ter, environment te where rr.from_id = fr.id and fr.version = (select max(i.version) from requirement i where i.id = fr.id) and fr.id = far.requirement_id and far.asset_id = fa.id and fa.id = fea.asset_id and rr.to_id = tr.id and tr.version = (select max(i.version) from requirement i where i.id = tr.id) and tr.id = ter.requirement_id and ter.environment_id = te.id order by 1,2;





INSERT INTO version (major,minor,patch) VALUES (2,3,3);
INSERT INTO attributes (id,name) VALUES (103,'did');
INSERT INTO trace_dimension values (0,'requirement');
INSERT INTO trace_dimension values (1,'persona');
INSERT INTO trace_dimension values (2,'task');
INSERT INTO trace_dimension values (3,'asset');
INSERT INTO trace_dimension values (4,'attacker');
INSERT INTO trace_dimension values (5,'threat');
INSERT INTO trace_dimension values (6,'vulnerability');
INSERT INTO trace_dimension values (7,'risk');
INSERT INTO trace_dimension values (8,'response');
INSERT INTO trace_dimension values (9,'environment');
INSERT INTO trace_dimension values (10,'role');
INSERT INTO trace_dimension values (11,'goal');
INSERT INTO trace_dimension values (12,'misusecase');
INSERT INTO trace_dimension values (13,'countermeasure');
INSERT INTO trace_dimension values (14,'classassociation');
INSERT INTO trace_dimension values (15,'goalassociation');
INSERT INTO trace_dimension values (16,'domainproperty');
INSERT INTO trace_dimension values (17,'obstacle');
INSERT INTO trace_dimension values (18,'usecase');
INSERT INTO trace_dimension values (19,'softgoal');
INSERT INTO trace_dimension values (20,'document_reference');
INSERT INTO trace_dimension values (21,'component');
INSERT INTO trace_dimension values (22,'belief');
INSERT INTO severity values (0,'Negligible','');
INSERT INTO severity values (1,'Marginal','');
INSERT INTO severity values (2,'Critical','');
INSERT INTO severity values (3,'Catastrophic','');
INSERT INTO likelihood values(0,'Incredible','');
INSERT INTO likelihood values(1,'Improbable','');
INSERT INTO likelihood values(2,'Remote','');
INSERT INTO likelihood values(3,'Occasional','');
INSERT INTO likelihood values(4,'Probable','');
INSERT INTO likelihood values(5,'Frequent','');
INSERT INTO risk_class values(1,'Negligible','');
INSERT INTO risk_class values(2,'Tolerable','');
INSERT INTO risk_class values(3,'Undesirable','');
INSERT INTO risk_class values(4,'Intolerable','');
INSERT INTO score values(5,3,4);
INSERT INTO score values(5,2,4);
INSERT INTO score values(5,1,4);
INSERT INTO score values(5,0,3);
INSERT INTO score values(4,3,4);
INSERT INTO score values(4,2,4);
INSERT INTO score values(4,1,3);
INSERT INTO score values(4,0,2);
INSERT INTO score values(3,3,4);
INSERT INTO score values(3,2,3);
INSERT INTO score values(3,1,2);
INSERT INTO score values(3,0,2);
INSERT INTO score values(2,3,3);
INSERT INTO score values(2,2,2);
INSERT INTO score values(2,1,2);
INSERT INTO score values(2,0,1);
INSERT INTO score values(1,3,2);
INSERT INTO score values(1,2,2);
INSERT INTO score values(1,1,1);
INSERT INTO score values(1,0,1);
INSERT INTO score values(0,3,1);
INSERT INTO score values(0,2,1);
INSERT INTO score values(0,1,1);
INSERT INTO score values(0,0,1);
INSERT INTO cost values(0,'Low');
INSERT INTO cost values(1,'Medium');
INSERT INTO cost values(2,'High');
INSERT INTO cost values(3,'None');
INSERT INTO goal_category_type values(0,'Achieve');
INSERT INTO goal_category_type values(1,'Maintain');
INSERT INTO goal_category_type values(2,'Avoid');
INSERT INTO goal_category_type values(3,'Improve');
INSERT INTO goal_category_type values(4,'Increase');
INSERT INTO goal_category_type values(5,'Maximise');
INSERT INTO goal_category_type values(6,'Minimise');
INSERT INTO goal_category_type values(7,'Accept');
INSERT INTO goal_category_type values(8,'Transfer');
INSERT INTO goal_category_type values(9,'Mitigate');
INSERT INTO goal_category_type values(10,'Deter');
INSERT INTO goal_category_type values(11,'Prevent');
INSERT INTO goal_category_type values(12,'Detect');
INSERT INTO goal_category_type values(13,'React');
INSERT INTO mitigate_type values(0,'Deter');
INSERT INTO mitigate_type values(1,'Prevent');
INSERT INTO mitigate_type values(2,'Detect');
INSERT INTO mitigate_type values(3,'React');
INSERT INTO mitigate_point_type values(0,'Before');
INSERT INTO mitigate_point_type values(1,'At');
INSERT INTO mitigate_point_type values(2,'After');
INSERT INTO security_property_value values (0,'None');
INSERT INTO security_property_value values (1,'Low');
INSERT INTO security_property_value values (2,'Medium');
INSERT INTO security_property_value values (3,'High');
INSERT INTO cognitive_attribute_value values (0,'None');
INSERT INTO cognitive_attribute_value values (1,'Low');
INSERT INTO cognitive_attribute_value values (2,'Medium');
INSERT INTO cognitive_attribute_value values (3,'High');
INSERT INTO securityusability_property_value values (-3,'High Help');
INSERT INTO securityusability_property_value values (-2,'Medium Help');
INSERT INTO securityusability_property_value values (-1,'Low Help');
INSERT INTO securityusability_property_value values (0,'None');
INSERT INTO securityusability_property_value values (1,'Low Hindrance');
INSERT INTO securityusability_property_value values (2,'Medium Hindrance');
INSERT INTO securityusability_property_value values (3,'High Hindrance');
INSERT INTO security_property values (0,'Confidentiality');
INSERT INTO security_property values (1,'Integrity');
INSERT INTO security_property values (2,'Availability');
INSERT INTO security_property values (3,'Accountability');
INSERT INTO security_property values (4,'Anonymity');
INSERT INTO security_property values (5,'Pseudonymity');
INSERT INTO security_property values (6,'Unlinkability');
INSERT INTO security_property values (7,'Unobservability');
INSERT INTO cognitive_attribute values (0,'Vigilance');
INSERT INTO cognitive_attribute values (1,'Situation Awareness');
INSERT INTO cognitive_attribute values (2,'Workload');
INSERT INTO cognitive_attribute values (3,'Stress');
INSERT INTO cognitive_attribute values (4,'Risk Awareness');
INSERT INTO allowable_trace values(0,2);
INSERT INTO allowable_trace values(2,6);
INSERT INTO allowable_trace values(0,6);
INSERT INTO allowable_trace values(3,0);
INSERT INTO allowable_trace values(0,10);
INSERT INTO allowable_trace values(0,18);
INSERT INTO allowable_trace values(18,2);
INSERT INTO allowable_trace values(0,0);
INSERT INTO allowable_trace values(0,20);
INSERT INTO allowable_trace values(21,18);
INSERT INTO allowable_trace values(16,2);
INSERT INTO allowable_trace values(7,5);
INSERT INTO allowable_trace values(7,6);
INSERT INTO allowable_trace values(20,6);
INSERT INTO allowable_trace values(20,17);
INSERT INTO requirement_type values(0,'Functional');
INSERT INTO requirement_type values(1,'Data');
INSERT INTO requirement_type values(2,'Look and Feel');
INSERT INTO requirement_type values(3,'Usability');
INSERT INTO requirement_type values(4,'Performance');
INSERT INTO requirement_type values(5,'Operational');
INSERT INTO requirement_type values(6,'Maintainability');
INSERT INTO requirement_type values(7,'Portability');
INSERT INTO requirement_type values(8,'Security');
INSERT INTO requirement_type values(9,'Cultural and Political');
INSERT INTO requirement_type values(10,'Legal');
INSERT INTO requirement_type values(11,'Privacy');
INSERT INTO target_effectiveness values(0,'None');
INSERT INTO target_effectiveness values(1,'Low');
INSERT INTO target_effectiveness values(2,'Medium');
INSERT INTO target_effectiveness values(3,'High');
INSERT INTO motivation values(0,'Hactivism','The nonviolent use of illegal or legally ambiguous digital tools in the pursuit of political ends.');
INSERT INTO motivation values(1,'Cyber-extortion','To be defined');
INSERT INTO motivation values(2,'Defamation','To be defined');
INSERT INTO motivation values(3,'Cyber-tagging','To be defined');
INSERT INTO motivation values(4,'Headlines/press','To be defined');
INSERT INTO motivation values(5,'Data theft','To be defined');
INSERT INTO motivation values(6,'Data destruction','To be defined');
INSERT INTO motivation values(7,'Data modification','To be defined');
INSERT INTO motivation values(8,'System resource theft','To be defined');
INSERT INTO motivation values(9,'Network resource theft','To be defined');
INSERT INTO motivation values(10,'Revenge','To be defined');
INSERT INTO motivation values(11,'Improved organisational position','To be defined');
INSERT INTO motivation values(12,'Improved esteem','To be defined');
INSERT INTO motivation values(13,'Thrill-seeking','To be defined');
INSERT INTO motivation values(14,'Fraud','To be defined');
INSERT INTO motivation values(15,'Disruption','To be defined');
INSERT INTO motivation values(16,'Accident','To be defined');
INSERT INTO motivation values(17,'Indifference','To be defined');
INSERT INTO motivation values(18,'Money','financial gain');
INSERT INTO motivation values(19,'Productivity','financial gain');
INSERT INTO capability values (0,'Resources/Equipment','To be defined');
INSERT INTO capability values (1,'Resources/Facilities','To be defined');
INSERT INTO capability values (2,'Resources/Personnel and Time','To be defined');
INSERT INTO capability values (3,'Resources/Funding','To be defined');
INSERT INTO capability values (4,'Technology','To be defined');
INSERT INTO capability values (5,'Software','To be defined');
INSERT INTO capability values (6,'Knowledge/Education and Training','To be defined');
INSERT INTO capability values (7,'Knowledge/Books and Manuals','To be defined');
INSERT INTO capability values (8,'Knowledge/Methods','To be defined');
INSERT INTO capability_value values (0,'None');
INSERT INTO capability_value values (1,'Low');
INSERT INTO capability_value values (2,'Medium');
INSERT INTO capability_value values (3,'High');
INSERT INTO duplicate_property values (0,'Override');
INSERT INTO duplicate_property values (1,'Maximise');
INSERT INTO association_type values (0,'Association');
INSERT INTO association_type values (1,'Aggregation');
INSERT INTO association_type values (2,'Composition');
INSERT INTO association_type values (3,'Inheritance');
INSERT INTO association_type values (4,'Dependency');
INSERT INTO multiplicity_type values (0,'1');
INSERT INTO multiplicity_type values (1,'*');
INSERT INTO multiplicity_type values (2,'1..*');
INSERT INTO reference_type values(0,'and');
INSERT INTO reference_type values(1,'or');
INSERT INTO reference_type values(2,'conflict');
INSERT INTO reference_type values(3,'responsible');
INSERT INTO reference_type values(4,'obstruct');
INSERT INTO reference_type values(5,'resolve');
INSERT INTO reference_type values(6,'depend');
INSERT INTO reference_type values(7,'supports');
INSERT INTO priority_type values (1,'Low');
INSERT INTO priority_type values (2,'Medium');
INSERT INTO priority_type values (3,'High');
INSERT INTO domainproperty_type values(0,'Hypothesis');
INSERT INTO domainproperty_type values(1,'Invariant');
INSERT INTO asset_type values(0,'Information','Documented (paper or electronic) data or Intellectual Property used to meet the mission of an organisation.');
INSERT INTO asset_type values(1,'Systems','Information Systems that process and store information (systems being a combination of information, software, and hardware assets and any host, client, or server being considered a system).');
INSERT INTO asset_type values(2,'Software','Software application and services -- such as operating systems, database applications, networking software, office applications, custom applications, etc. -- that process, store, or transmit information.');
INSERT INTO asset_type values(3,'Hardware','Information Technology physical devices -- such as workstations, servers, etc -- that normally focus solely on the replacement costs for physical devices.');
INSERT INTO asset_type values(4,'People','The people in an organisation who possess unique skills, knowledge, and experience that are difficult to replace.');
INSERT INTO asset_type values(5,'Systems - General','Organisational, Groups, and Social Systems, of which may have, use, manage, and operate Information Systems that process, store, or transmit information.');
INSERT INTO asset_type values(6,'System of Systems','The combination of Independent Systems (collaborating to achieve a new combined purpose and goal).');
INSERT INTO obstacle_category_type values(0,'Confidentiality Threat');
INSERT INTO obstacle_category_type values(1,'Integrity Threat');
INSERT INTO obstacle_category_type values(2,'Availability Threat');
INSERT INTO obstacle_category_type values(3,'Accountability Threat');
INSERT INTO obstacle_category_type values(4,'Vulnerability');
INSERT INTO obstacle_category_type values(5,'Duration');
INSERT INTO obstacle_category_type values(6,'Frequency');
INSERT INTO obstacle_category_type values(7,'Demands');
INSERT INTO obstacle_category_type values(8,'Goal Support');
INSERT INTO obstacle_category_type values(9,'Anonymity Threat');
INSERT INTO obstacle_category_type values(10,'Pseudonymity Threat');
INSERT INTO obstacle_category_type values(11,'Unlinkability Threat');
INSERT INTO obstacle_category_type values(12,'Unobservability Threat');
INSERT INTO obstacle_category_type values(13,'Threat');
INSERT INTO obstacle_category_type values(14,'Loss');
INSERT INTO obstacle_category_type values(15,'Hazard');
INSERT INTO project_setting values(0,'Project Name','New Project');
INSERT INTO project_setting values(1,'Project Background','None');
INSERT INTO project_setting values(2,'Project Goals','None');
INSERT INTO project_setting values(3,'Project Scope','None');
INSERT INTO project_setting values(4,'Rich Picture','');
INSERT INTO project_setting values(5,'Font Name','Times New Roman');
INSERT INTO project_setting values(6,'Font Size','7.5');
INSERT INTO project_setting values(7,'AP Font Size','13');
INSERT INTO countermeasure_value(id,name,description) values(0,'None','To be defined');
INSERT INTO countermeasure_value(id,name,description) values(1,'Low','To be defined');
INSERT INTO countermeasure_value(id,name,description) values(2,'Medium','To be defined');
INSERT INTO countermeasure_value(id,name,description) values(3,'High','To be defined');
INSERT INTO threat_value(id,name,description) values(0,'None','To be defined');
INSERT INTO threat_value(id,name,description) values(1,'Low','To be defined');
INSERT INTO threat_value(id,name,description) values(2,'Medium','To be defined');
INSERT INTO threat_value(id,name,description) values(3,'High','To be defined');
INSERT INTO persona_type(id,name) values(0,'Primary');
INSERT INTO persona_type(id,name) values(1,'Secondary');
INSERT INTO persona_type(id,name) values(2,'Supplemental');
INSERT INTO persona_type(id,name) values(3,'Customer');
INSERT INTO persona_type(id,name) values(4,'Served');
INSERT INTO persona_type(id,name) values(5,'Negative');
INSERT INTO role_type(id,name) values(0,'Stakeholder');
INSERT INTO role_type(id,name) values(1,'Attacker');
INSERT INTO role_type(id,name) values(2,'Data Controller');
INSERT INTO role_type(id,name) values(3,'Data Processor');
INSERT INTO role_type(id,name) values(4,'Data Subject');
INSERT INTO behavioural_variable(id,name) values (0,'Activities');
INSERT INTO behavioural_variable(id,name) values (1,'Attitudes');
INSERT INTO behavioural_variable(id,name) values (2,'Aptitudes');
INSERT INTO behavioural_variable(id,name) values (3,'Motivations');
INSERT INTO behavioural_variable(id,name) values (4,'Skills');
INSERT INTO behavioural_variable(id,name) values (5,'Environment Narrative');
INSERT INTO behavioural_variable(id,name) values (6,'Intrinsic');
INSERT INTO behavioural_variable(id,name) values (7,'Contextual');
INSERT INTO characteristic_reference_type(id,name) values(0,'grounds');
INSERT INTO characteristic_reference_type(id,name) values(1,'warrant');
INSERT INTO characteristic_reference_type(id,name) values(2,'rebuttal');
INSERT INTO tension(id,name,short_code) values(-1,'Conflicting','conflicting');
INSERT INTO tension(id,name,short_code) values(0,'None','none');
INSERT INTO tension(id,name,short_code) values(1,'Complementary','complementary');
insert into contribution_end (id,name) values (0,'means');
insert into contribution_end (id,name) values (1,'end');
insert into link_contribution (id,name,value) values (3,'Make',100);
insert into link_contribution (id,name,value) values (2,'SomePositive',50);
insert into link_contribution (id,name,value) values (1,'Help',25);
insert into link_contribution (id,name,value) values (-1,'Hurt',-25);
insert into link_contribution (id,name,value) values (-2,'SomeNegative',-50);
insert into link_contribution (id,name,value) values (-3,'Break',-100);
insert into goal_satisfaction (id,name,value) values (2,'Satisfied',100);
insert into goal_satisfaction (id,name,value) values (1,'Weakly Satisfied',50);
insert into goal_satisfaction (id,name,value) values (0,'None',0);
insert into goal_satisfaction (id,name,value) values (-1,'Weakly Denied',-50);
insert into goal_satisfaction (id,name,value) values (-2,'Denied',-100);
insert into artifact_section (id,name) values (-1,'none');
insert into artifact_section (id,name) values (0,'activities');
insert into artifact_section (id,name) values (1,'attitudes');
insert into artifact_section (id,name) values (2,'aptitudes');
insert into artifact_section (id,name) values (3,'motivations');
insert into artifact_section (id,name) values (4,'skills');
insert into artifact_section (id,name) values (5,'narrative');
insert into artifact_section (id,name) values (6,'benefits');
insert into artifact_section (id,name) values (7,'consequences');
insert into artifact_section (id,name) values (8,'intrinsic');
insert into artifact_section (id,name) values (9,'contextual');
insert into relationship_type (id,name) values(0,'associated');
insert into relationship_type (id,name) values(1,'implies');
insert into relationship_type (id,name) values(2,'conflict');
insert into relationship_type (id,name) values(3,'part-of');
insert into code_type (id,name) values (0,'event');
insert into code_type (id,name) values (1,'context');
insert into access_right (id,name,description,value,rationale) values (0,'None','No access rights',1,'Default');
insert into privilege (id,name,description,value,rationale) values (0,'None','No privileges',10,'Default');
INSERT INTO dataflow_type values(0,'Information','Information flow');
INSERT INTO dataflow_type values(1,'Control','Control action');
INSERT INTO dataflow_type values(2,'Feedback','Feedback action');
INSERT INTO trust_boundary_type values(0,'Controller','Controller');
INSERT INTO trust_boundary_type values(1,'Controlled Process','Controlled Process');
INSERT INTO trust_boundary_type values(2,'Sensor','Sensor');
INSERT INTO trust_boundary_type values(3,'Actuator','Actuator');
INSERT INTO trust_boundary_type values(4,'General','General');
INSERT INTO stpa_keyword values(0,'does not provide','Not providing causes hazards');
INSERT INTO stpa_keyword values(1,'provides','Providing causes hazards');
INSERT INTO stpa_keyword values(2,'provides too early','Incorrect timing / order');
INSERT INTO stpa_keyword values(3,'provides too late','Incorrect timing / order');
INSERT INTO stpa_keyword values(4,'provides out of order','Incorrect timing / order');
INSERT INTO stpa_keyword values(5,'stopped too soon','Stopped too soon / applied to long');
INSERT INTO stpa_keyword values(6,'applied too long','Stopped too soon / applied to long');
INSERT INTO stpa_keyword values(7,'not applicable','Not applicable');
