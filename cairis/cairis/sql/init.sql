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

DROP VIEW IF EXISTS countermeasure_vulnerability_response_target;
DROP VIEW IF EXISTS countermeasure_threat_response_target;
DROP VIEW IF EXISTS redmine_requirement;
DROP VIEW IF EXISTS synopsis;
DROP VIEW IF EXISTS source_reference;
DROP VIEW IF EXISTS environment_role;
DROP VIEW IF EXISTS detection_mechanism;
DROP VIEW IF EXISTS concept_reference;
DROP VIEW IF EXISTS task_documentconcept_reference;
DROP VIEW IF EXISTS documentconcept_reference;
DROP VIEW IF EXISTS assumption_persona_model;
DROP VIEW IF EXISTS assumption_task_model;
DROP VIEW IF EXISTS environment_risk;
DROP VIEW IF EXISTS concept_map;

DROP TABLE IF EXISTS usecase_step_synopsis;
DROP TABLE IF EXISTS usecase_pc_contribution;
DROP TABLE IF EXISTS usecase_tc_contribution;
DROP TABLE IF EXISTS usecase_dr_contribution;
DROP TABLE IF EXISTS document_reference_contribution;
DROP TABLE IF EXISTS requirement_reference_contribution;
DROP TABLE IF EXISTS document_reference_synopsis;
DROP TABLE IF EXISTS requirement_reference_synopsis;
DROP TABLE IF EXISTS persona_characteristic_synopsis;
DROP TABLE IF EXISTS task_characteristic_synopsis;
DROP TABLE IF EXISTS contribution_end;
DROP TABLE IF EXISTS link_contribution;
DROP TABLE IF EXISTS asset_tag;
DROP TABLE IF EXISTS attacker_tag;
DROP TABLE IF EXISTS threat_tag;
DROP TABLE IF EXISTS vulnerability_tag;
DROP TABLE IF EXISTS risk_tag;

DROP TABLE IF EXISTS component_association;
DROP TABLE IF EXISTS component_interface;
DROP TABLE IF EXISTS interface;
DROP TABLE IF EXISTS component;

DROP TABLE IF EXISTS value_tension;
DROP TABLE IF EXISTS tension;
DROP TABLE IF EXISTS vulnerability_asset_countermeasure_effect;
DROP TABLE IF EXISTS threat_asset_countermeasure_effect;
DROP TABLE IF EXISTS asset_template_asset;
DROP TABLE IF EXISTS countermeasure_securitypattern;
DROP TABLE IF EXISTS securitypattern_classassociation;
DROP TABLE IF EXISTS securitypattern_requirement;
DROP TABLE IF EXISTS securitypattern;
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
DROP TABLE IF EXISTS domainproperty;
DROP TABLE IF EXISTS domainproperty_type;
DROP TABLE IF EXISTS usecase_step_goal_exception;
DROP TABLE IF EXISTS usecase_step_requirement_exception;
DROP TABLE IF EXISTS goal;
DROP TABLE IF EXISTS requirement_usecase;
DROP TABLE IF EXISTS requirement_requirement;
DROP TABLE IF EXISTS usecase_task;
DROP TABLE IF EXISTS usecase_conditions;
DROP TABLE IF EXISTS usecase_step;
DROP TABLE IF EXISTS usecase_role;
DROP TABLE IF EXISTS usecase;
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
DROP TABLE IF EXISTS tag;
DROP TABLE IF EXISTS asset_type;
DROP TABLE IF EXISTS asset_value;
DROP TABLE IF EXISTS environment;
DROP TABLE IF EXISTS security_property;
DROP TABLE IF EXISTS security_property_value;
DROP TABLE IF EXISTS securityusability_property_value;
DROP TABLE IF EXISTS countermeasure_value;
DROP TABLE IF EXISTS threat_value;

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
  name VARCHAR(50), 
  description VARCHAR(4000), 
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE environment(
  id INT NOT NULL, 
  name VARCHAR(50), 
  description VARCHAR(4000), 
  short_code VARCHAR(10) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE tension (
  id INT NOT NULL, 
  name VARCHAR(50), 
  description VARCHAR(4000), 
  short_code VARCHAR(10) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE asset_value (
  id INT NOT NULL, 
  name VARCHAR(50), 
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
  name VARCHAR(255),
  description VARCHAR(4000),
  rationale VARCHAR(255) NOT NULL,
  originator VARCHAR(100),
  fit_criterion VARCHAR(255) NOT NULL,
  priority INT NOT NULL,
  supporting_material VARCHAR(100),
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
  name VARCHAR(50) NOT NULL,
  short_code VARCHAR(10) NOT NULL,
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
  name VARCHAR(50) NOT NULL,
  threat_type_id INT NOT NULL,
  method VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(threat_type_id) REFERENCES threat_type(id)
) ENGINE=INNODB;
CREATE TABLE threat_directory (
  id INT NOT NULL,
  label VARCHAR(50) NOT NULL,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(4000) NOT NULL,
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
  label VARCHAR(50) NOT NULL,
  name VARCHAR(100) NOT NULL,
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
  activities VARCHAR(4000) NOT NULL,
  attitudes VARCHAR(4000) NOT NULL,
  aptitudes VARCHAR(4000) NOT NULL,
  motivations VARCHAR(4000) NOT NULL,
  skills VARCHAR(4000) NOT NULL,
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
CREATE TABLE requirement_requirement (
  from_id INT NOT NULL,
  to_id INT NOT NULL,
  label VARCHAR(255) NULL,
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
  name VARCHAR(50) NOT NULL,
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
  name VARCHAR(100) NOT NULL,
  threat_id INT NOT NULL,
  vulnerability_id INT NOT NULL,
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
  name VARCHAR(50) NOT NULL,
  goal_category_type_id INT NOT NULL,
  risk_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(goal_category_type_id) REFERENCES goal_category_type(id),
  FOREIGN KEY(risk_id) REFERENCES risk(id)
) ENGINE=INNODB;
CREATE TABLE countermeasure ( 
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
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
  originator VARCHAR(50) NOT NULL,
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
  PRIMARY KEY(obstacle_id,environment_id),
  FOREIGN KEY(obstacle_id) REFERENCES obstacle(id),
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
  originator VARCHAR(50) NOT NULL,
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
  definition VARCHAR(1000) NOT NULL,
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
CREATE TABLE template_asset (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  short_code VARCHAR(10) NOT NULL,
  description VARCHAR(1000),
  significance VARCHAR(1000),
  asset_type_id INT NOT NULL,
  is_critical INT NOT NULL,
  critical_rationale VARCHAR(1000),
  confidentiality_value_id INT NOT NULL,
  integrity_value_id INT NOT NULL,
  availability_value_id INT NOT NULL,
  accountability_value_id INT NOT NULL,
  anonymity_value_id INT NOT NULL,
  pseudonymity_value_id INT NOT NULL,
  unlinkability_value_id INT NOT NULL,
  unobservability_value_id INT NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(asset_type_id) REFERENCES asset_type(id),
  FOREIGN KEY(confidentiality_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(integrity_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(availability_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(accountability_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(anonymity_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(pseudonymity_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(unlinkability_value_id) REFERENCES security_property_value(id),
  FOREIGN KEY(unobservability_value_id) REFERENCES security_property_value(id)
) ENGINE=INNODB;
CREATE TABLE securitypattern (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  context VARCHAR(4000) NOT NULL,
  problem VARCHAR(4000) NOT NULL,
  solution VARCHAR(4000) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;
CREATE TABLE securitypattern_requirement(
  label INT NOT NULL,
  pattern_id INT NOT NULL,
  type_id INT NOT NULL,
  name VARCHAR(255),
  description VARCHAR(4000),
  rationale VARCHAR(255) NOT NULL,
  fit_criterion VARCHAR(255) NOT NULL,
  asset_id INT NOT NULL,
  PRIMARY KEY(label,pattern_id),
  FOREIGN KEY (pattern_id) REFERENCES securitypattern(id),
  FOREIGN KEY (type_id) REFERENCES requirement_type(id),
  FOREIGN KEY (asset_id) REFERENCES template_asset(id)
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
CREATE TABLE asset_template_asset (
  asset_id INT NOT NULL,
  template_asset_id INT NOT NULL,
  PRIMARY KEY(asset_id,template_asset_id),
  FOREIGN KEY(asset_id) REFERENCES asset(id),
  FOREIGN KEY(template_asset_id) REFERENCES template_asset(id)
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
  description VARCHAR(4444000) NOT NULL,
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

CREATE TABLE contribution_end (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE link_contribution (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE persona_characteristic_synopsis (
  characteristic_id INT NOT NULL,
  synopsis VARCHAR(1000) NOT NULL,
  dimension_id INT NOT NULL,
  PRIMARY KEY(characteristic_id),
  FOREIGN KEY(characteristic_id) REFERENCES persona_characteristic(id),
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
  PRIMARY KEY(id),
  FOREIGN KEY(reference_id) REFERENCES document_reference(id),
  FOREIGN KEY(dimension_id) REFERENCES trace_dimension(id),
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
  FOREIGN KEY(reference_id) REFERENCES document_reference_synopsis(id),
  FOREIGN KEY(end_id) REFERENCES contribution_end(id),
  FOREIGN KEY(contribution_id) REFERENCES link_contribution(id)
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

CREATE TABLE interface (
  id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=INNODB;

CREATE TABLE component_interface (
  component_id INT NOT NULL,
  interface_id INT NOT NULL,
  required_id INT NOT NULL,
  PRIMARY KEY(component_id,interface_id),
  FOREIGN KEY(component_id) REFERENCES component(id),
  FOREIGN KEY(interface_id) REFERENCES interface(id)
) ENGINE=INNODB;

CREATE TABLE component_association (
  from_component_id INT NOT NULL,
  from_interface_id INT NOT NULL,
  to_component_id INT NOT NULL,
  to_interface_id INT NOT NULL,
  PRIMARY KEY(from_component_id,from_interface_id,to_component_id,to_interface_id),
  FOREIGN KEY(from_component_id) REFERENCES component(id),
  FOREIGN KEY(from_interface_id) REFERENCES interface(id),
  FOREIGN KEY(to_component_id) REFERENCES component(id),
  FOREIGN KEY(to_interface_id) REFERENCES interface(id)
) ENGINE=INNODB;

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
  select id,synopsis,'usecase' synopsis_type from usecase_step_synopsis;


CREATE VIEW environment_risk as
  select r.id,et.environment_id from risk r, environment_threat et, environment_vulnerability ev where r.threat_id = et.threat_id and et.environment_id = ev.environment_id and ev.vulnerability_id = r.vulnerability_id
  union 
  select r.id,ev.environment_id from risk r, environment_vulnerability ev, environment_threat et where r.vulnerability_id = ev.vulnerability_id and ev.environment_id = et.environment_id and et.threat_id = r.threat_id;

CREATE VIEW environment_role as
  select distinct environment_id, subgoal_id role_id from responserole_goalassociation
  union
  select distinct environment_id, role_id from countermeasure_role;

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
  select rr.id,rr.name,'requirement' dimension_name,concat(a.short_code,'-',r.label) object_name,rr.description from requirement_reference rr, requirement r, asset a, asset_requirement ar where rr.requirement_id = r.id and r.id = ar.requirement_id and ar.asset_id = a.id and r.version = (select max(i.version) from requirement i where i.id = r.id)
  union
  select rr.id,rr.name,'requirement' dimension_name,concat(e.short_code,'-',r.label) object_name,rr.description from requirement_reference rr, requirement r, environment e, environment_requirement er where rr.requirement_id = r.id and r.id = er.requirement_id and er.environment_id = e.id and r.version = (select max(i.version) from requirement i where i.id = r.id)
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
  select concat('qual_',pc.description) from_name, 'qual' from_dim, pc.description to_name, 'task_characteristic' to_dim, p.name task_name, pc.description characteristic_name from task_characteristic pc, task p where pc.task_id = p.id;


CREATE VIEW assumption_persona_model as
  select pc.description from_name, 'persona_characteristic' from_dim, p.name to_name, 'persona' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona p, persona_characteristic pc, behavioural_variable bv where p.id = pc.persona_id and pc.variable_id = bv.id
  union
  select cr.name from_name, 'grounds' from_dim, concat('gwb_',pc.description) to_name, 'gwb' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_document pcc, document_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.characteristic_reference_type_id = 0 and pcc.reference_id = cr.id and pc.variable_id = bv.id and pc.persona_id = p.id
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
  select c.name from_name, 'backing' from_dim, cr.name to_name, 'warrant' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from external_document c, document_reference cr, persona_characteristic_document pcc, persona_characteristic pc, behavioural_variable bv, persona p where pcc.reference_id = cr.id and cr.document_id = c.id and pcc.characteristic_reference_type_id = 1 and pcc.characteristic_id = pc.id and pc.variable_id = bv.id and pc.persona_id = p.id
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
  select concat('qual_',pc.description) from_name, 'qual' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, behavioural_variable bv, persona p where pc.variable_id = bv.id and pc.persona_id = p.id
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
  select cr.name from_name, 'rebuttal' from_dim, pc.description to_name, 'persona_characteristic' to_dim, p.name persona_name, bv.name bv_name,pc.description characteristic_name from persona_characteristic pc, persona_characteristic_vulnerability pcc, vulnerability_reference cr, behavioural_variable bv, persona p where pc.id = pcc.characteristic_id and pcc.reference_id = cr.id and pcc.characteristic_reference_type_id = 2 and pc.variable_id = bv.id and pc.persona_id = p.id
  union
  select pc.qualifier from_name, 'qualifier' from_dim, concat('qual_',pc.description) to_name, 'qual' to_dim, p.name persona_name, bv.name bv_name, pc.description characteristic_name from persona_characteristic pc, behavioural_variable bv, persona p where pc.variable_id = bv.id and pc.persona_id = p.id;

CREATE VIEW concept_map as
  select fr.name from_name, tr.name to_name, rr.label from requirement fr, requirement tr, requirement_requirement rr where rr.from_id = fr.id and fr.version = (select max(i.version) from requirement i where i.id = fr.id) and rr.to_id = tr.id and tr.version = (select max(i.version) from requirement i where i.id = tr.id); 



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
INSERT INTO allowable_trace values(0,2);
INSERT INTO allowable_trace values(2,6);
INSERT INTO allowable_trace values(2,3);
INSERT INTO allowable_trace values(0,6);
INSERT INTO allowable_trace values(3,0);
INSERT INTO allowable_trace values(16,3);
INSERT INTO allowable_trace values(0,10);
INSERT INTO allowable_trace values(0,18);
INSERT INTO allowable_trace values(18,2);
INSERT INTO allowable_trace values(11,16);
INSERT INTO allowable_trace values(11,17);
INSERT INTO allowable_trace values(11,0);
INSERT INTO allowable_trace values(11,10);
INSERT INTO allowable_trace values(11,2);
INSERT INTO allowable_trace values(11,18);
INSERT INTO allowable_trace values(17,11);
INSERT INTO allowable_trace values(17,12);
INSERT INTO allowable_trace values(17,0);
INSERT INTO allowable_trace values(17,10);
INSERT INTO allowable_trace values(17,2);
INSERT INTO allowable_trace values(17,5);
INSERT INTO allowable_trace values(17,18);
INSERT INTO allowable_trace values(17,6);
INSERT INTO allowable_trace values(0,0);
INSERT INTO allowable_trace values(20,0);
INSERT INTO allowable_trace values(0,20);
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
INSERT INTO priority_type values (1,'Low');
INSERT INTO priority_type values (2,'Medium');
INSERT INTO priority_type values (3,'High');
INSERT INTO domainproperty_type values(0,'Hypothesis');
INSERT INTO domainproperty_type values(1,'Invariant');
INSERT INTO asset_type values(0,'Information','Documented (paper or electronic) data or Intellectual Property used to meet the mission of an organisation.');
INSERT INTO asset_type values(1,'Systems','Information Systems that process and store information (systems being a combination of information, software, and hardware assets and any host, client, or server being considered a system.');
INSERT INTO asset_type values(2,'Software','Software application and services -- such as operating systems, database applications, networking software, office applications, custom applications, etc. -- that process, store, or transmit information.');
INSERT INTO asset_type values(3,'Hardware','Information Technology physical devices -- such as workstations, servers, etc -- that normally focus solely on the replacement costs for physical devices.');
INSERT INTO asset_type values(4,'People','The people in an organisation who possess unique skills, knowledge, and experience that are difficult to replace.');
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
INSERT INTO behavioural_variable(id,name) values (0,'Activities');
INSERT INTO behavioural_variable(id,name) values (1,'Attitudes');
INSERT INTO behavioural_variable(id,name) values (2,'Aptitudes');
INSERT INTO behavioural_variable(id,name) values (3,'Motivations');
INSERT INTO behavioural_variable(id,name) values (4,'Skills');
INSERT INTO behavioural_variable(id,name) values (5,'Environment Narrative');
INSERT INTO characteristic_reference_type(id,name) values(0,'grounds');
INSERT INTO characteristic_reference_type(id,name) values(1,'warrant');
INSERT INTO characteristic_reference_type(id,name) values(2,'rebuttal');
INSERT INTO tension(id,name) values(-1,'Conflicting');
INSERT INTO tension(id,name) values(0,'None');
INSERT INTO tension(id,name) values(1,'Complementary');
insert into contribution_end (id,name) values (0,'means');
insert into contribution_end (id,name) values (1,'end');
insert into link_contribution (id,name) values (3,'Make');
insert into link_contribution (id,name) values (2,'SomePositive');
insert into link_contribution (id,name) values (1,'Help');
insert into link_contribution (id,name) values (-1,'Hurt');
insert into link_contribution (id,name) values (-2,'SomeNegative');
insert into link_contribution (id,name) values (-3,'Break');

