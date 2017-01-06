#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import os
import httplib
from flask import send_from_directory, make_response, session
from flask_restful_swagger import swagger
from flask_restful import Api
from flask_security import login_required, http_auth_required
from jsonpickle import encode
from cairis.core.Borg import Borg
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from cairis.controllers import AssetController, AttackerController, CImportController, CExportController, DependencyController, \
    DimensionController, EnvironmentController, GoalController, MisuseCaseController, PersonaController, ProjectController, \
    RequirementController, ResponseController, RiskController, RoleController, TaskController, ThreatController, \
    UploadController, VulnerabilityController, ObstacleController, CountermeasureController, DomainPropertyController, UseCaseController, \
    DependencyController, DocumentationController, FindController, ExternalDocumentController, DocumentReferenceController, \
    PersonaCharacteristicController, ObjectDependencyController, ArchitecturalPatternController, ValueTypeController, TemplateGoalController, TemplateAssetController,TemplateRequirementController, LocationsController, RiskLevelController, TraceController
from cairis.daemon.main import main, api

__author__ = 'Robin Quetin, Shamal Faily'

def set_dbproxy():
  b = Borg()
  db_proxy = MySQLDatabaseProxy()
  pSettings = db_proxy.getProjectSettings()

  id = b.init_settings()
  db_proxy.close()
  session['session_id'] = id
  b.settings[id]['dbProxy'] = db_proxy
  b.settings[id]['dbUser'] = b.dbUser
  b.settings[id]['dbPasswd'] = b.dbPasswd
  b.settings[id]['dbHost'] = b.dbHost
  b.settings[id]['dbPort'] = b.dbPort
  b.settings[id]['dbName'] = b.dbName
  b.settings[id]['fontSize'] = pSettings['Font Size']
  b.settings[id]['apFontSize'] = pSettings['AP Font Size']
  b.settings[id]['fontName'] = pSettings['Font Name']
  b.settings[id]['jsonPrettyPrint'] = False
  return b.settings[id]

def make_session():
  s = set_dbproxy()
  resp_dict = {'session_id': s['session_id'], 'message': 'Session created'}
  resp = make_response(encode(resp_dict), httplib.OK)
  resp.headers['Content-type'] = 'application/json'
  return resp

@main.route('/')
@login_required
def home():
  return main.send_static_file('index.html')

@main.route('/make_session',methods=['POST'])
@login_required
def webapp_make_session():
  return make_session()

@main.route('/api/session',methods=['POST'])
@http_auth_required
def api_make_session():
  return make_session()

@main.route('/plugins/<path:path>')
def plugin_reroute(path):
  try:
    b = Borg()
    web_image_dir = os.path.join(b.staticDir, 'plugins')
    return send_from_directory(web_image_dir, path)
  except AttributeError:
    return send_from_directory('static/plugins', path)


@main.route('/fastTemplates/<path:path>')
def fast_templates_reroute(path):
  try:
    b = Borg()
    web_image_dir = os.path.join(b.staticDir, 'fastTemplates')
    return send_from_directory(web_image_dir, path)
  except AttributeError:
    return send_from_directory('static/fastTemplates', path)

@main.route('/dist/<path:path>')
def dist_reroute(path):
  try:
    b = Borg()
    web_image_dir = os.path.join(b.staticDir, 'dist')
    return send_from_directory(web_image_dir, path)
  except AttributeError:
    return send_from_directory('static/dist', path)

@main.route('/bootstrap/<path:path>')
def bootstrap_reroute(path):
  try:
    b = Borg()
    web_image_dir = os.path.join(b.staticDir, 'bootstrap')
    return send_from_directory(web_image_dir, path)
  except AttributeError:
    return send_from_directory('static/bootstrap', path)

@main.route('/assets/<path:path>')
def get_asset(path):
  try:
    b = Borg()
    web_image_dir = os.path.join(b.staticDir, 'assets')
    return send_from_directory(web_image_dir, path)
  except AttributeError:
    return send_from_directory('static/assets', path)

@main.route('/images/<path:path>')
def get_image(path):
  try:
    b = Borg()
    fixed_img_path = b.imageDir
    upload_img_path = b.uploadDir
  except AttributeError:
    image_dir = 'images'

  if os.path.exists(fixed_img_path):
    return send_from_directory(fixed_img_path, path)
  elif os.path.exists(upload_img_path):
    return send_from_directory(upload_img_path, path)
  else:
    try:
      b = Borg()
      web_img_dir = os.path.join(b.staticDir, 'images')
      return send_from_directory(web_img_dir, path)
    except AttributeError:
      return send_from_directory('static/images', path)


  return handle_error(err)

# Architectural Pattern routes
api.add_resource(ArchitecturalPatternController.ArchitecturalPatternsAPI, '/api/architectural_patterns', endpoint = 'architecturalpatterns')
api.add_resource(ArchitecturalPatternController.ArchitecturalPatternByNameAPI, '/api/architectural_patterns/name/<string:name>', endpoint='architecturalpattern')
api.add_resource(ArchitecturalPatternController.ComponentGoalModelAPI, '/api/architectural_patterns/component/goal/model/<string:component>', endpoint = 'componentgoals')
api.add_resource(ArchitecturalPatternController.ComponentAssetModelAPI, '/api/architectural_patterns/component/asset/model/<string:component>', endpoint = 'componentassets')

# Asset routes
api.add_resource(AssetController.AssetsAPI, '/api/assets',endpoint='assets')
api.add_resource(AssetController.AssetByNameAPI, '/api/assets/name/<string:name>',endpoint='assetbyname')
api.add_resource(AssetController.AssetByEnvironmentNamesAPI, '/api/assets/environment/<string:environment>/names',endpoint='assetbyenvironmentname')
api.add_resource(AssetController.AssetByIdAPI, '/api/assets/id/<int:id>',endpoint='assetbyid')
api.add_resource(AssetController.AssetNamesAPI, '/api/assets/all/names',endpoint='assetnames')
api.add_resource(AssetController.AssetTypesAPI, '/api/assets/types',endpoint='assettypes')
api.add_resource(AssetController.AssetTypeByNameAPI, '/api/assets/types/name/<string:name>',endpoint='assettypebyname')
api.add_resource(AssetController.AssetValuesAPI, '/api/environments/<string:environment_name>/asset-values',endpoint='assetvalues')
api.add_resource(AssetController.AssetValueByNameAPI, '/api/environments/<string:environment_name>/asset-values/name/<string:name>',endpoint='assetvaluebyname')
api.add_resource(AssetController.AssetModelAPI, '/api/assets/model/environment/<string:environment>/asset/<string:asset>',endpoint='assetmodel')
api.add_resource(AssetController.AssetEnvironmentPropertiesAPI, '/api/assets/name/<string:asset_name>/properties',endpoint='assetenvironmentproperties')
api.add_resource(AssetController.AssetAssociationAPI, '/api/assets/association',endpoint='assetassociation')
api.add_resource(AssetController.AssetAssociationByNameAPI, '/api/assets/association/environment/<string:environment_name>/head/<string:head_name>/tail/<string:tail_name>',endpoint='assetassociationbyname')

# Attacker routes
api.add_resource(AttackerController.AttackersAPI, '/api/attackers',endpoint='attackers')
api.add_resource(AttackerController.AttackerByNameAPI, '/api/attackers/name/<string:name>',endpoint='attackerbyname')
api.add_resource(AttackerController.AttackerCapabilitiesAPI, '/api/attackers/capabilities',endpoint='attackercapabilities')
api.add_resource(AttackerController.AttackerCapabilityByNameAPI, '/api/attackers/capabilities/name/<string:name>',endpoint='attackercapability')
api.add_resource(AttackerController.AttackerMotivationsAPI, '/api/attackers/motivations',endpoint='motivations')
api.add_resource(AttackerController.AttackerMotivationByNameAPI, '/api/attackers/motivations/name/<string:name>',endpoint='motivationbyname')

# Countermeasure routes
api.add_resource(CountermeasureController.CountermeasuresAPI, '/api/countermeasures',endpoint='countermeasures')
api.add_resource(CountermeasureController.CountermeasureByNameAPI, '/api/countermeasures/name/<string:name>',endpoint='countermeasure')
api.add_resource(CountermeasureController.GenerateAssetAPI, '/api/countermeasures/name/<string:name>/generate_asset',endpoint='countermeasure_generate_asset')
api.add_resource(CountermeasureController.TargetsAPI, '/api/countermeasures/targets/environment/<string:environment>',endpoint='targets')
api.add_resource(CountermeasureController.CountermeasureTasksAPI, '/api/countermeasures/tasks/environment/<string:environment>',endpoint='countermeasuretasks')


# Dependency routes
api.add_resource(DependencyController.DependenciesAPI, '/api/dependencies',endpoint='dependencies')
api.add_resource(DependencyController.DependencyByNameAPI, '/api/dependencies/environment/<environment>/depender/<depender>/dependee/<dependee>/dependency/<dependency>',endpoint='dependency')

# DimensionController
api.add_resource(DimensionController.DimensionsAPI, '/api/dimensions/table/<string:table>',endpoint='dimensions')
api.add_resource(DimensionController.DimensionNamesAPI, '/api/dimensions/table/<string:table>/environment/<string:environment>',endpoint='dimension')

# Document Reference routes
api.add_resource(DocumentReferenceController.DocumentReferencesAPI, '/api/document_references',endpoint='document_references')
api.add_resource(DocumentReferenceController.DocumentReferenceByNameAPI, '/api/document_references/name/<string:name>',endpoint='document_reference')

# Documentation route
api.add_resource(DocumentationController.DocumentationAPI, '/api/documentation/type/<string:doc_type>/format/<string:doc_format>',endpoint='documentation')

# Domain Property routes
api.add_resource(DomainPropertyController.DomainPropertiesAPI, '/api/domainproperties',endpoint='domain_properties')
api.add_resource(DomainPropertyController.DomainPropertiesByNameAPI, '/api/domainproperties/name/<string:name>',endpoint='domain_property')

# Environment routes
api.add_resource(EnvironmentController.EnvironmentsAPI, '/api/environments',endpoint='environments')
api.add_resource(EnvironmentController.EnvironmentNamesAPI, '/api/environments/names', '/api/environments/all/names',endpoint='environment_names')
api.add_resource(EnvironmentController.EnvironmentByNameAPI, '/api/environments/name/<string:name>',endpoint='environment')
api.add_resource(
  EnvironmentController.EnvironmentsByThreatVulnerability,
  '/api/environments/threat/<string:threat>/vulnerability/<string:vulnerability>',
  '/api/environments/vulnerability/<string:vulnerability>/threat/<string:threat>',endpoint='environments_tv'
)
api.add_resource(
  EnvironmentController.EnvironmentNamesByThreatVulnerability,
  '/api/environments/threat/<string:threat>/vulnerability/<string:vulnerability>/names',
  '/api/environments/vulnerability/<string:vulnerability>/threat/<string:threat>/names',endpoint='environment_names_tv'
)
api.add_resource(EnvironmentController.EnvironmentNamesByRisk,'/api/environments/risk/<string:risk>/names',endpoint='environment_names_risk')

# External Document routes
api.add_resource(ExternalDocumentController.ExternalDocumentsAPI, '/api/external_documents',endpoint='external_documents')
api.add_resource(ExternalDocumentController.ExternalDocumentByNameAPI, '/api/external_documents/name/<string:name>',endpoint='external_document')


# Goal routes
api.add_resource(GoalController.GoalsAPI, '/api/goals',endpoint='goals')
api.add_resource(GoalController.GoalByNameAPI, '/api/goals/name/<string:name>',endpoint='goal')
api.add_resource(GoalController.GoalByEnvironmentNamesAPI, '/api/goals/environment/<string:environment>/names',endpoint='goal_environment')
api.add_resource(GoalController.GoalModelAPI, '/api/goals/model/environment/<string:environment>/goal/<string:goal>/usecase/<string:usecase>',endpoint='goal_model')
api.add_resource(GoalController.ResponsibilityModelAPI, '/api/responsibility/model/environment/<string:environment>/role/<string:role>',endpoint='responsibility_model')
api.add_resource(GoalController.GoalAssociationAPI, '/api/goals/association',endpoint='goal_associations')
api.add_resource(GoalController.GoalAssociationByNameAPI, '/api/goals/association/environment/<string:environment_name>/goal/<string:goal_name>/subgoal/<string:subgoal_name>',endpoint='goal_association')

# Export route
api.add_resource(CExportController.CExportFileAPI, '/api/export/file',endpoint='export')

# Find route
api.add_resource(FindController.FindAPI, '/api/find/<string:search_string>',endpoint='find')

# Import routes
api.add_resource(CImportController.CImportTextAPI, '/api/import/text',endpoint='import_text')
api.add_resource(CImportController.CImportFileAPI, '/api/import/file/type/<string:type>',endpoint='import_file')

# Locations routes
api.add_resource(LocationsController.LocationsAPI, '/api/locations',endpoint='locations')
api.add_resource(LocationsController.LocationsByNameAPI, '/api/locations/name/<string:name>',endpoint='locations_name')
api.add_resource(LocationsController.LocationsModelAPI, '/api/locations/model/locations/<string:locations>/environment/<string:environment>',endpoint='locationsmodel')

# Misuse case routes
api.add_resource(MisuseCaseController.MisuseCasesAPI, '/api/misusecases',endpoint='misusecases')
api.add_resource(MisuseCaseController.MisuseCaseByRiskNameAPI, '/api/misusecases/risk/<string:risk_name>',endpoint='misusecase_risk')
api.add_resource(MisuseCaseController.MisuseCaseByNameAPI, '/api/misusecases/name/<string:misuse_case_name>',endpoint='misusecase')
api.add_resource(MisuseCaseController.MisuseCaseByTVAPI, '/api/misusecases/threat/<string:threat>/vulnerability/<string:vulnerability>',endpoint='misusecase_tv')

# Object dependency routes
api.add_resource(ObjectDependencyController.ObjectDependencyAPI, '/api/object_dependency/dimension/<string:dimension_name>/object/<string:object_name>',endpoint='object_dependency')

# Obstacle routes
api.add_resource(ObstacleController.ObstaclesAPI, '/api/obstacles',endpoint='obstacles')
api.add_resource(ObstacleController.ObstacleByNameAPI, '/api/obstacles/name/<string:name>',endpoint='obstacle')
api.add_resource(ObstacleController.ObstacleByEnvironmentNamesAPI, '/api/obstacles/environment/<string:environment>/names',endpoint='obstacle_environment')
api.add_resource(ObstacleController.ObstacleModelAPI, '/api/obstacles/model/environment/<string:environment>/obstacle/<string:obstacle>',endpoint='obstacle_model')

# Persona routes
api.add_resource(PersonaController.PersonasAPI, '/api/personas',endpoint='personas')
api.add_resource(PersonaController.PersonaNamesAPI, '/api/personas/names', '/api/personas/all/names',endpoint='persona_names')
api.add_resource(PersonaController.PersonaByNameAPI, '/api/personas/name/<string:name>',endpoint='persona')
api.add_resource(PersonaController.PersonaModelByNameAPI, '/api/personas/model/name/<string:persona>/variable/<string:variable>/characteristic/<string:characteristic>',endpoint='persona_model')
api.add_resource(PersonaController.PersonaCharacteristicsByNameAPI, '/api/personas/characteristics/name/<string:persona>/variable/<string:variable>/characteristic/<string:characteristic>',endpoint='persona_characteristic_persona')
api.add_resource(PersonaController.PersonaTypesAPI, '/api/personas/types',endpoint='persona_types')
api.add_resource(PersonaController.PersonaEnvironmentPropertiesAPI, '/api/personas/name/<string:persona_name>/properties','/persona_environment_properties',endpoint='persona_environment_properties')

# Persona Characteristic routes
api.add_resource(PersonaCharacteristicController.PersonaCharacteristicsAPI, '/api/persona_characteristics',endpoint='persona_characteristics')
api.add_resource(PersonaCharacteristicController.PersonaCharacteristicByNameAPI, '/api/persona_characteristics/name/<string:name>',endpoint='persona_characteristic')

# Project routes
api.add_resource(ProjectController.ProjectSettingsAPI, '/api/settings',endpoint='project_settings')
api.add_resource(ProjectController.ProjectCreateAPI, '/api/settings/create',endpoint='project_create')

# Requirement routes
api.add_resource(RequirementController.RequirementsAPI, '/api/requirements',endpoint='requirements')
api.add_resource(RequirementController.RequirementsByAssetAPI, '/api/requirements/asset/<string:name>',endpoint='requirements_assets')
api.add_resource(RequirementController.RequirementsByEnvironmentAPI, '/api/requirements/environment/<string:name>',endpoint='requirement_environments')
api.add_resource(RequirementController.RequirementByNameAPI, '/api/requirements/name/<string:name>',endpoint='requirement')
api.add_resource(RequirementController.RequirementByShortcodeAPI, '/api/requirements/shortcode/<string:shortcode>',endpoint='requirement_shortcode')

# Response routes
api.add_resource(ResponseController.ResponsesAPI, '/api/responses',endpoint='reponses')
api.add_resource(ResponseController.ResponseByNameAPI, '/api/responses/name/<string:name>',endpoint='response')
api.add_resource(ResponseController.ResponseByNameGenerateAPI, '/api/responses/name/<string:name>/generate_goal',endpoint='generate_goal')

# Risk routes
api.add_resource(RiskController.RisksAPI, '/api/risks',endpoint='risks')
api.add_resource(RiskController.RiskByNameAPI, '/api/risks/name/<string:name>',endpoint='risk')
api.add_resource(
  RiskController.RisksScoreByNameAPI,
  '/api/risks/name/<string:name>/threat/<string:threat>/vulnerability/<string:vulnerability>/environment/<string:environment>',
  '/api/risks/name/<string:name>/vulnerability/<string:vulnerability>/threat/<string:threat>/environment/<string:environment>',endpoint='risk_score')
api.add_resource(
  RiskController.RisksRatingByNameAPI,
  '/api/risks/threat/<string:threat>/vulnerability/<string:vulnerability>/environment/<string:environment>',
  '/api/risks/vulnerability/<string:vulnerability>/threat/<string:threat>/environment/<string:environment>',endpoint='risk_rating'
)
api.add_resource(RiskController.RiskAnalysisModelAPI, '/api/risks/model/environment/<string:environment>',endpoint='risk_model')
api.add_resource(RiskController.RiskAnalysisModelNamesAPI, '/api/risks/model/environment/<string:environment>/names',endpoint='risk_model_name')

# Risk Levels routes
api.add_resource(RiskLevelController.RiskLevelAPI, '/api/risk_level/asset/<string:name>',endpoint='risklevel')
api.add_resource(RiskLevelController.RiskThreatLevelAPI, '/api/risk_level/asset/<string:asset>/threat_type/<string:threat>',endpoint='riskthreatlevel')

# Role routes
api.add_resource(RoleController.RolesAPI, '/api/roles',endpoint='roles')
api.add_resource(RoleController.RolesByNameAPI, '/api/roles/name/<string:name>',endpoint='role')
api.add_resource(RoleController.RolesByIdAPI, '/api/roles/id/<int:id>',endpoint='roles_id')
api.add_resource(RoleController.RoleEnvironmentPropertiesAPI, '/api/roles/name/<string:name>/properties',endpoint='role_properties')

# Task routes
api.add_resource(TaskController.TasksAPI, '/api/tasks',endpoint='tasks')
api.add_resource(TaskController.TaskByNameAPI, '/api/tasks/name/<string:name>',endpoint='task')
api.add_resource(TaskController.TaskModelByNameAPI, '/api/tasks/model/environment/<string:environment>/task/<string:task>/misusecase/<string:misusecase>',endpoint='task_model')
api.add_resource(TaskController.TaskLoadByNameAPI, '/api/tasks/name/<string:task>/environment/<string:environment>/load',endpoint='task_load')
api.add_resource(TaskController.TaskHindranceByNameAPI, '/api/tasks/name/<string:task>/environment/<string:environment>/hindrance',endpoint='task_hindrance')
api.add_resource(TaskController.TaskScoreByNameAPI, '/api/tasks/name/<string:task>/environment/<string:environment>/score',endpoint='task_score')

# Template Asset routes
api.add_resource(TemplateAssetController.TemplateAssetsAPI, '/api/template_assets',endpoint='template_assets')
api.add_resource(TemplateAssetController.TemplateAssetByNameAPI, '/api/template_assets/name/<string:name>',endpoint='template_asset')

# Template Goal routes
api.add_resource(TemplateGoalController.TemplateGoalsAPI, '/api/template_goals',endpoint='template_goals')
api.add_resource(TemplateGoalController.TemplateGoalByNameAPI, '/api/template_goals/name/<string:name>',endpoint='template_goal')

# Template Requirement routes
api.add_resource(TemplateRequirementController.TemplateRequirementsAPI, '/api/template_requirements',endpoint='template_requirements')
api.add_resource(TemplateRequirementController.TemplateRequirementByNameAPI, '/api/template_requirements/name/<string:name>',endpoint='template_requirement')

# Threat routes
api.add_resource(ThreatController.ThreatAPI, '/api/threats',endpoint='threats')
api.add_resource(ThreatController.ThreatByIdAPI, '/api/threats/id/<int:id>',endpoint='threat_id')
api.add_resource(ThreatController.ThreatByNameAPI, '/api/threats/name/<string:name>',endpoint='threat')
api.add_resource(ThreatController.ThreatTypesAPI, '/api/threats/types',endpoint='threat_types')
api.add_resource(ThreatController.ThreatTypeByNameAPI, '/api/threats/types/name/<string:name>',endpoint='threat_type')

# Trace routes
api.add_resource(TraceController.TracesAPI, '/api/traces',endpoint='traces')
api.add_resource(TraceController.TraceByEnvironmentAPI, '/api/traces/environment/<string:environment_name>',endpoint='traces_environment')
api.add_resource(TraceController.TraceDimensionsAPI, '/api/traces/dimensions/<string:dimension_name>/is_from/<string:is_from>',endpoint='trace_dimensions')
api.add_resource(TraceController.TraceByNameAPI, '/api/traces/from_type/<string:from_object>/from_name/<string:from_name>/to_type/<string:to_object>/to_name/<string:to_name>',endpoint='traces_name')

# Upload controller
api.add_resource(UploadController.UploadImageAPI, '/api/upload/image',endpoint='upload')

# Use Case routes
api.add_resource(UseCaseController.UseCasesAPI, '/api/usecases',endpoint='usecases')
api.add_resource(UseCaseController.UseCaseByNameAPI, '/api/usecases/name/<string:name>',endpoint='usecase')

# Value Type routes
api.add_resource(ValueTypeController.ValueTypesAPI, '/api/value_types/type/<string:type_name>/environment/<string:environment_name>',endpoint='value_types')
api.add_resource(ValueTypeController.ValueTypesByNameAPI, '/api/value_types/type/<string:type_name>/environment/<string:environment_name>/name/<string:object_name>',endpoint='value_type')
api.add_resource(ValueTypeController.ValueTypesCreateAPI, '/api/value_types/',endpoint='create_value_type')

# Vulnerability routes
api.add_resource(VulnerabilityController.VulnerabilityAPI, '/api/vulnerabilities',endpoint='vulnerabilities')
api.add_resource(VulnerabilityController.VulnerabilityByIdAPI, '/api/vulnerabilities/id/<int:id>',endpoint='vulnerability_id')
api.add_resource(VulnerabilityController.VulnerabilityByNameAPI, '/api/vulnerabilities/name/<string:name>',endpoint='vulnerability')
api.add_resource(VulnerabilityController.VulnerabilityTypesAPI, '/api/vulnerabilities/types',endpoint='vulnerability_types')
api.add_resource(VulnerabilityController.VulnerabilityTypeByNameAPI, '/api/vulnerabilities/types/name/<string:name>',endpoint='vulnerability_type_name')
