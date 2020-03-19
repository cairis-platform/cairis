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
import sys
if (sys.version_info > (3,)):
  import http.client
  from http.client import OK
else:
  import httplib
  from httplib import OK
import MySQLdb
from flask import send_from_directory, send_file, make_response, session, request, render_template
from flask_restful import Api
from flask_security import login_required, http_auth_required
from flask_security.utils import logout_user
from flask_security.core import current_user
from jsonpickle import encode
from cairis.core.Borg import Borg
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy,canonicalDbUser,canonicalDbName
from cairis.controllers import ArchitecturalPatternController
from cairis.controllers import CExportController
from cairis.controllers import CImportController
from cairis.controllers import CountermeasureController
from cairis.controllers import DataFlowController
#from cairis.controllers import DirectoryController
from cairis.controllers import DocumentationController
from cairis.controllers import EnvironmentController
from cairis.controllers import GoalController
from cairis.controllers import GoalContributionController
from cairis.controllers import LocationsController
from cairis.controllers import MisuseCaseController
from cairis.controllers import ObjectController
from cairis.controllers import ObjectDependencyController
from cairis.controllers import ObstacleController
from cairis.controllers import PermissionsController
from cairis.controllers import PersonaController
from cairis.controllers import PersonaCharacteristicController
from cairis.controllers import ProjectController
from cairis.controllers import RequirementController
from cairis.controllers import ResponseController
from cairis.controllers import RiskController
from cairis.controllers import RiskLevelController
from cairis.controllers import RoleController
from cairis.controllers import SecurityPatternController
from cairis.controllers import SummaryController
from cairis.controllers import TaskController
from cairis.controllers import ThreatController
from cairis.controllers import TraceController
from cairis.controllers import UploadController
from cairis.controllers import UseCaseController
from cairis.controllers import UserGoalController
from cairis.controllers import ValidationController
from cairis.controllers import ValueTypeController
from cairis.controllers import VersionController
from cairis.controllers import VulnerabilityController

from cairis.daemon.main import main, api
from cairis.tools.SessionValidator import get_session_id
from base64 import b64decode
import io
import datetime

__author__ = 'Robin Quetin, Shamal Faily'

def set_dbproxy(dbUser,userName):
  b = Borg()
  dbPasswd = current_user.dbtoken

  dbUser = canonicalDbUser(dbUser)
  dbName = dbUser + '_default'
  db_proxy = MySQLDatabaseProxy(user=dbUser,passwd=dbPasswd,db=dbName)
  pSettings = db_proxy.getProjectSettings()

  id = b.init_settings()
  db_proxy.close()
  session['session_id'] = id
  b.settings[id]['dbProxy'] = db_proxy
  b.settings[id]['dbUser'] = dbUser
  b.settings[id]['userName'] = userName
  b.settings[id]['dbPasswd'] = dbPasswd
  b.settings[id]['dbHost'] = b.dbHost
  b.settings[id]['dbPort'] = b.dbPort
  b.settings[id]['dbName'] = dbName
  b.settings[id]['rPasswd'] = b.rPasswd
  b.settings[id]['fontSize'] = pSettings['Font Size']
  b.settings[id]['apFontSize'] = pSettings['AP Font Size']
  b.settings[id]['fontName'] = pSettings['Font Name']
  b.settings[id]['jsonPrettyPrint'] = False
  return b.settings[id]

def make_session():
  s = set_dbproxy(current_user.email,current_user.name)
  resp_dict = {'session_id': s['session_id'], 'message': 'Session created','user' : current_user.email}
  b = Borg()
  b.logger.info(str(datetime.datetime.now()) + ': ' + current_user.email + ' logged in.')
  resp = make_response(encode(resp_dict), OK)
  resp.headers['Content-type'] = 'application/json'
  return resp

@main.route('/')
@login_required
def home():
  request.args = {}
  return main.send_static_file('index.html')

@main.route('/disconnect')
@login_required
def logout():
  id = session['session_id']
  b = Borg()
  db_proxy = b.settings[id]['dbProxy']
  db_proxy.close()
  del b.settings[id]
  session.pop(id,None)
  logout_user()
  resp_dict = {'message': 'Logged out'}
  resp = make_response(encode(resp_dict), OK)
  resp.headers['Content-type'] = 'application/json'
  return resp


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
  b = Borg()
  session_id = get_session_id(session, request)
  db_proxy = b.settings[session_id]['dbProxy']
  imgDetails = db_proxy.getImage(path)
  if (imgDetails != None):
    fp = io.BytesIO(b64decode(imgDetails[0]))
    return send_file(fp,mimetype=imgDetails[1])
  else:
    distDir = b.staticDir
    return send_from_directory(distDir, 'default-avatar.png')

@main.route('/api/user')
def get_user_details():
  session_id = get_session_id(session, request)
  b = Borg()
  emailName = b.settings[session_id]['dbUser'] 
  userName = b.settings[session_id]['userName']
  user_dict = {'name' : userName, 'email' : emailName}
  resp = make_response(encode(user_dict), OK)
  resp.headers['Content-type'] = 'application/json'
  return resp

@main.route('/register')
def registerUser():
  b = Borg()
  if (b.mailServer != '' and b.mailPort != '' and b.mailUser != '' and b.mailPasswd != ''):
    return render_template('register_user.html')
  else:
    return render_template('no_self_service.html')

@main.route('/reset')
def resetUser():
  b = Borg()
  if (b.mailServer != '' and b.mailPort != '' and b.mailUser != '' and b.mailPasswd != ''):
    return render_template('forgot_password.html')
  else:
    return render_template('no_self_service.html')


# Architectural Pattern routes
api.add_resource(ObjectController.ObjectsAPI, '/api/architectural_patterns',endpoint='architecturalpatterns',resource_class_kwargs={'dao': 'ArchitecturalPatternDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/architectural_patterns/name/<path:name>',endpoint='architecturalpattern',resource_class_kwargs={'dao' : 'ArchitecturalPatternDAO'})
api.add_resource(ArchitecturalPatternController.ComponentGoalModelAPI, '/api/architectural_patterns/component/goal/model/<path:component>', endpoint = 'componentgoals')
api.add_resource(ArchitecturalPatternController.ComponentAssetModelAPI, '/api/architectural_patterns/component/asset/model/<path:component>', endpoint = 'componentassets')
api.add_resource(ArchitecturalPatternController.ComponentModelAPI, '/api/architectural_patterns/component/model/<path:ap_name>', endpoint = 'componentmodel')
api.add_resource(ArchitecturalPatternController.WeaknessAnalysisAPI, '/api/architectural_patterns/name/<path:architectural_pattern_name>/environment/<path:environment_name>/weakness_analysis', endpoint='architecturalweaknessanalysis')
api.add_resource(ArchitecturalPatternController.SituateArchitecturalPatternAPI, '/api/architectural_patterns/name/<path:architectural_pattern_name>/environment/<path:environment_name>/situate', endpoint='situatearchitecturalpattern')

# Asset routes
api.add_resource(ObjectController.ObjectsAPI, '/api/assets',endpoint='assets',resource_class_kwargs={'dao': 'AssetDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/assets/name/<path:name>',endpoint='asset',resource_class_kwargs={'dao' : 'AssetDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/assets/summary',endpoint='assetssummary',resource_class_kwargs={'dao' : 'AssetDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/assets/environment/<path:parameter_string>/names',endpoint='assetbyenvironmentname',resource_class_kwargs={'dao' : 'AssetDAO','get_method' : 'get_asset_names_by_environment'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/assets/all/names',endpoint='assetnames',resource_class_kwargs={'dao' : 'AssetDAO','get_method' : 'get_asset_names', 'path_parameters' : [('environment','')]})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/assets/types',endpoint='assettypes',resource_class_kwargs={'dao' : 'AssetDAO','get_method' : 'get_asset_types', 'post_method' : 'add_asset_type', 'path_parameters' : [('environment','')], 'isType' : True})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/assets/types/name/<path:parameter_string>',endpoint='assettypebyname',resource_class_kwargs={'dao' : 'AssetDAO','get_method' : 'get_asset_type_by_name', 'put_method' : 'update_asset_type','del_method' : 'delete_asset_type', 'path_parameters' : [('environment','')], 'isType' : True})
api.add_resource(ObjectController.ModelByTwoParametersAPI, '/api/assets/model/environment/<path:p1>/asset/<path:p2>',endpoint='assetmodel',resource_class_kwargs={'dao' : 'AssetDAO','get_method' : 'get_asset_model','renderer' : 'dot', 'path_parameters' : [('hide_concerns','1')]})

api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/assets/association',endpoint='assetassociation',resource_class_kwargs={'dao' : 'AssetAssociationDAO','get_method' : 'get_asset_associations', 'post_method' : 'add_asset_association'})
api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI, '/api/assets/association/environment/<path:p1>/head/<path:p2>/tail/<path:p3>',endpoint='assetassociationbyname',resource_class_kwargs={'dao' : 'AssetAssociationDAO','get_method' : 'get_asset_association', 'put_method' : 'update_asset_association','del_method' : 'delete_asset_association'})

# Attacker routes
api.add_resource(ObjectController.ObjectsAPI, '/api/attackers',endpoint='attackers',resource_class_kwargs={'dao': 'AttackerDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/attackers/name/<path:name>',endpoint='attackerbyname',resource_class_kwargs={'dao' : 'AttackerDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/attackers/summary',endpoint='attackerssummary',resource_class_kwargs={'dao' : 'AttackerDAO'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/attackers/capabilities',endpoint='attackercapabilities',resource_class_kwargs={'dao' : 'AttackerDAO','get_method' : 'get_attacker_capabilities','path_parameters' : [('environment_name','')]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/attackers/capabilities/name/<path:parameter_string>',endpoint='attackercapabilitiesbyname',resource_class_kwargs={'dao' : 'AttackerDAO','get_method' : 'get_attacker_capabilities','path_parameters' : [('environment_name','')]})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/attackers/motivations',endpoint='attackermotivations',resource_class_kwargs={'dao' : 'AttackerDAO','get_method' : 'get_attacker_motivations','path_parameters' : [('environment_name','')]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/attackers/motivations/name/<path:parameter_string>',endpoint='attackermotivationsbyname',resource_class_kwargs={'dao' : 'AttackerDAO','get_method' : 'get_attacker_capabilities','path_parameters' : [('environment_name','')]})

# Concept Reference routes
api.add_resource(ObjectController.ObjectsAPI, '/api/concept_references',endpoint='concept_reference',resource_class_kwargs={'dao': 'ConceptReferenceDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/concept_references/name/<path:name>',endpoint='concept_references',resource_class_kwargs={'dao' : 'ConceptReferenceDAO'})

# Countermeasure routes
api.add_resource(ObjectController.ObjectsAPI, '/api/countermeasures',endpoint='countermeasures',resource_class_kwargs={'dao': 'CountermeasureDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/countermeasures/name/<path:name>',endpoint='countermeasure',resource_class_kwargs={'dao' : 'CountermeasureDAO'})
api.add_resource(CountermeasureController.GenerateAssetAPI, '/api/countermeasures/name/<path:name>/generate_asset',endpoint='countermeasure_generate_asset')
api.add_resource(CountermeasureController.GenerateAssetFromTemplateAPI, '/api/countermeasures/name/<path:name>/template_asset/<path:template_asset_name>/generate_asset',endpoint='countermeasure_generate_asset_from_template')
api.add_resource(CountermeasureController.SituateCountermeasurePatternAPI, '/api/countermeasures/name/<path:name>/security_pattern/<path:security_pattern_name>/situate',endpoint='countermeasure_situate_countermeasure_pattern')
api.add_resource(CountermeasureController.AssociateSituatedPatternAPI, '/api/countermeasures/name/<path:name>/security_pattern/<path:security_pattern_name>/associate_situated',endpoint='associate_situated_pattern')
api.add_resource(CountermeasureController.RemoveSituatedPatternAPI, '/api/countermeasures/name/<path:name>/security_pattern/<path:security_pattern_name>/remove_situated',endpoint='remove_situated_pattern')
api.add_resource(CountermeasureController.TargetsAPI, '/api/countermeasures/targets/environment/<path:environment>',endpoint='targets')
api.add_resource(CountermeasureController.CountermeasureTasksAPI, '/api/countermeasures/tasks/environment/<path:environment>',endpoint='countermeasuretasks')
api.add_resource(CountermeasureController.CandidatePatternsAPI, '/api/countermeasures/name/<path:name>/candidate_patterns',endpoint='candidate_patterns')
api.add_resource(CountermeasureController.CountermeasurePatternsAPI, '/api/countermeasures/name/<path:name>/patterns',endpoint='countermeasure_patterns')

# Dataflow routes
api.add_resource(ObjectController.ObjectsAPI, '/api/dataflows',endpoint='dataflows',resource_class_kwargs={'dao': 'DataFlowDAO'})
api.add_resource(DataFlowController.DataFlowByNameAPI, '/api/dataflows/name/<path:dataflow_name>/environment/<path:environment_name>',endpoint='dataflow')
api.add_resource(DataFlowController.DataFlowDiagramAPI, '/api/dataflows/diagram/environment/<path:environment_name>/filter_type/<path:filter_type>/filter_name/<path:filter_element>',endpoint='dataflowdiagram')

# Dependency routes
api.add_resource(ObjectController.ObjectsAPI, '/api/dependencies',endpoint='dependencies',resource_class_kwargs={'dao': 'DependencyDAO'})
api.add_resource(ObjectController.ObjectByFourParametersAPI, '/api/dependencies/environment/<p1>/depender/<p2>/dependee/<p3>/dependency/<p4>',endpoint='dependency',resource_class_kwargs={'dao': 'DependencyDAO'})

# Dimension routes
api.add_resource(ObjectController.ConstrainedObjectsByNameAPI, '/api/dimensions/table/<path:parameter_string>',endpoint='dimensions',resource_class_kwargs={'dao' : 'DimensionDAO','constraint_parameter' : 'constraint_id'})
api.add_resource(ObjectController.ObjectsByTwoParametersAPI, '/api/dimensions/table/<path:p1>/environment/<path:p2>',endpoint='dimension',resource_class_kwargs={'dao' : 'DimensionDAO'})

# DirectoryController
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/directory/threat/<path:parameter_string>',endpoint='threatdirectory',resource_class_kwargs={'dao' : 'DirectoryDAO','get_method' : 'get_threat_directory'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/directory/vulnerability/<path:parameter_string>',endpoint='vulnerabilitydirectory',resource_class_kwargs={'dao' : 'DirectoryDAO','get_method' : 'get_vulnerability_directory'})
#api.add_resource(DirectoryController.ThreatDirectoryAPI, '/api/directory/threat/<path:entry_name>',endpoint='threatdirectory')
#api.add_resource(DirectoryController.VulnerabilityDirectoryAPI, '/api/directory/vulnerability/<path:entry_name>',endpoint='vulnerabilitydirectory')

# Document Reference routes
api.add_resource(ObjectController.ObjectsAPI, '/api/document_references',endpoint='document_reference',resource_class_kwargs={'dao': 'DocumentReferenceDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/document_references/name/<path:name>',endpoint='document_references',resource_class_kwargs={'dao' : 'DocumentReferenceDAO'})

# Documentation route
api.add_resource(DocumentationController.DocumentationAPI, '/api/documentation/type/<path:doc_type>/format/<path:doc_format>',endpoint='documentation')

# Domain Property routes
api.add_resource(ObjectController.ObjectsAPI, '/api/domainproperties',endpoint='domainproperties',resource_class_kwargs={'dao': 'DomainPropertyDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/domainproperties/name/<path:name>',endpoint='domainproperty',resource_class_kwargs={'dao' : 'DomainPropertyDAO'})

# Environment routes
api.add_resource(ObjectController.ObjectsAPI, '/api/environments',endpoint='environments',resource_class_kwargs={'dao': 'EnvironmentDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/environments/name/<path:name>',endpoint='environment',resource_class_kwargs={'dao' : 'EnvironmentDAO'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/environments/names','/api/environments/all/names',endpoint='environment_names',resource_class_kwargs={'dao' : 'EnvironmentDAO','get_method' : 'get_environment_names'})
api.add_resource(
  EnvironmentController.EnvironmentsByThreatVulnerability,
  '/api/environments/threat/<path:threat>/vulnerability/<path:vulnerability>',
  '/api/environments/vulnerability/<path:vulnerability>/threat/<path:threat>',endpoint='environments_tv'
)
api.add_resource(
  EnvironmentController.EnvironmentNamesByThreatVulnerability,
  '/api/environments/threat/<path:threat>/vulnerability/<path:vulnerability>/names',
  '/api/environments/vulnerability/<path:vulnerability>/threat/<path:threat>/names',endpoint='environment_names_tv'
)
api.add_resource(EnvironmentController.EnvironmentNamesByRisk,'/api/environments/risk/<path:risk>/names',endpoint='environment_names_risk')

# External Document routes
api.add_resource(ObjectController.ObjectsAPI, '/api/external_documents',endpoint='external_documents',resource_class_kwargs={'dao': 'ExternalDocumentDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/external_documents/name/<path:name>',endpoint='external_document',resource_class_kwargs={'dao' : 'ExternalDocumentDAO'})


# Goal routes
api.add_resource(GoalController.GoalsAPI, '/api/goals',endpoint='goals')
api.add_resource(GoalController.GoalByNameAPI, '/api/goals/name/<path:name>',endpoint='goal')
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/goals/summary',endpoint='goalssummary',resource_class_kwargs={'dao' : 'GoalDAO'})
api.add_resource(GoalController.GoalByEnvironmentNamesAPI, '/api/goals/environment/<path:environment>/names',endpoint='goal_environment')
api.add_resource(GoalController.GoalModelAPI, '/api/goals/model/environment/<path:environment>/goal/<path:goal>/usecase/<path:usecase>',endpoint='goal_model')
api.add_resource(GoalController.ResponsibilityModelAPI, '/api/responsibility/model/environment/<path:environment>/role/<path:role>',endpoint='responsibility_model')
api.add_resource(GoalController.GoalAssociationAPI, '/api/goals/association',endpoint='goal_associations')
api.add_resource(GoalController.GoalAssociationByNameAPI, '/api/goals/association/environment/<path:environment_name>/goal/<path:goal_name>/subgoal/<path:subgoal_name>',endpoint='goal_association')

# Goal contribution routes
api.add_resource(GoalContributionController.GoalContributionsAPI, '/api/goal_contributions',endpoint='goal_contributions')
api.add_resource(GoalContributionController.GoalContributionByNameAPI, '/api/goal_contributions/source/<sourceName>/target/<targetName>',endpoint='goal_contribution')

# Export route
api.add_resource(CExportController.CExportFileAPI, '/api/export/file',endpoint='export')
api.add_resource(CExportController.CExportArchitecturalPatternAPI, '/api/export/file/architectural_pattern/<path:architectural_pattern_name>',endpoint='exportarchitecturalpattern')
api.add_resource(CExportController.CExportSecurityPatternsAPI, '/api/export/file/security_patterns',endpoint='exportsecuritypatterns')
api.add_resource(CExportController.CExportGRLAPI, '/api/export/file/grl/task/<path:task_name>/persona/<path:persona_name>/environment/<path:environment_name>',endpoint='exportgrl')

# Find route
api.add_resource(ObjectController.ObjectsByNameAPI, '/api/find/<path:parameter_string>',endpoint='find',resource_class_kwargs={'dao' : 'FindDAO'})

# Import routes
api.add_resource(CImportController.CImportPackageAPI, '/api/import/package',endpoint='import_package')
api.add_resource(CImportController.CImportTextAPI, '/api/import/text',endpoint='import_text')
api.add_resource(CImportController.CImportFileAPI, '/api/import/file/type/<path:type>',endpoint='import_file')

# Locations routes
api.add_resource(ObjectController.ObjectsAPI, '/api/locations',endpoint='locations',resource_class_kwargs={'dao': 'LocationsDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/locations/name/<path:name>',endpoint='location',resource_class_kwargs={'dao' : 'LocationsDAO'})
api.add_resource(LocationsController.LocationsModelAPI, '/api/locations/model/locations/<path:locations>/environment/<path:environment>',endpoint='locationsmodel')

# Misuse case routes
api.add_resource(MisuseCaseController.MisuseCasesAPI, '/api/misusecases',endpoint='misusecases')
api.add_resource(MisuseCaseController.MisuseCaseByRiskNameAPI, '/api/misusecases/risk/<path:risk_name>',endpoint='misusecase_risk')
api.add_resource(MisuseCaseController.MisuseCaseByNameAPI, '/api/misusecases/name/<path:misuse_case_name>',endpoint='misusecase')
api.add_resource(MisuseCaseController.MisuseCaseByTVAPI, '/api/misusecases/threat/<path:threat>/vulnerability/<path:vulnerability>',endpoint='misusecase_tv')

# Object dependency routes
api.add_resource(ObjectDependencyController.ObjectDependencyAPI, '/api/object_dependency/dimension/<path:dimension_name>/object/<path:object_name>',endpoint='object_dependency')

# Obstacle routes

api.add_resource(ObjectController.ObjectsAPI, '/api/obstacles',endpoint='obstacles',resource_class_kwargs={'dao': 'ObstacleDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/obstacles/name/<path:name>',endpoint='obstacle',resource_class_kwargs={'dao' : 'ObstacleDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/obstacles/summary',endpoint='obstaclessummary',resource_class_kwargs={'dao' : 'ObstacleDAO'})
api.add_resource(ObstacleController.GenerateVulnerabilityAPI, '/api/obstacles/name/<path:name>/generate_vulnerability',endpoint='generatevulnerability')
api.add_resource(ObstacleController.ObstacleByEnvironmentNamesAPI, '/api/obstacles/environment/<path:environment>/names',endpoint='obstacle_environment')
api.add_resource(ObstacleController.ObstacleModelAPI, '/api/obstacles/model/environment/<path:environment>/obstacle/<path:obstacle>',endpoint='obstacle_model')

# Permissions routes
api.add_resource(PermissionsController.PermissionsAPI, '/api/permissions/database/<path:db_name>',endpoint='permissions')
api.add_resource(PermissionsController.ChangePermissionAPI, '/api/permissions/database/<path:db_name>/user/<path:user_id>/permission/<path:permission>',endpoint='changepermission')

# Persona routes
api.add_resource(ObjectController.ObjectsAPI, '/api/personas',endpoint='personas',resource_class_kwargs={'dao': 'PersonaDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/personas/name/<path:name>',endpoint='persona',resource_class_kwargs={'dao' : 'PersonaDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/personas/summary',endpoint='personassummary',resource_class_kwargs={'dao' : 'PersonaDAO'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/personas/names',endpoint='persona_names',resource_class_kwargs={'dao' : 'PersonaDAO','get_method' : 'get_persona_names'})
api.add_resource(PersonaController.PersonaModelByNameAPI, '/api/personas/model/name/<path:persona>/variable/<path:variable>/characteristic/<path:characteristic>',endpoint='persona_model')
api.add_resource(PersonaController.PersonaCharacteristicsByNameAPI, '/api/personas/characteristics/name/<path:persona>/variable/<path:variable>/characteristic/<path:characteristic>',endpoint='persona_characteristic_persona')
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/personas/types',endpoint='persona_types',resource_class_kwargs={'dao' : 'PersonaDAO','get_method' : 'get_persona_types'})

# Persona Characteristic routes
api.add_resource(PersonaCharacteristicController.PersonaCharacteristicsAPI, '/api/persona_characteristics',endpoint='persona_characteristics')
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/persona_characteristics/summary',endpoint='personacharacteristicssummary',resource_class_kwargs={'dao' : 'PersonaCharacteristicDAO'})
api.add_resource(PersonaCharacteristicController.PersonaCharacteristicByNameAPI, '/api/persona_characteristics/name/<path:name>',endpoint='persona_characteristic')

# Project routes
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/settings',endpoint='project_settings',resource_class_kwargs={'dao' : 'ProjectDAO','get_method' : 'get_settings','put_method' : 'apply_settings'})
api.add_resource(ProjectController.ProjectClearAPI, '/api/settings/clear',endpoint='project_clear')
api.add_resource(ProjectController.ProjectCreateDatabaseAPI, '/api/settings/database/<path:db_name>/create',endpoint='database_create')
api.add_resource(ProjectController.ProjectOpenDatabaseAPI, '/api/settings/database/<path:db_name>/open',endpoint='database_open')
api.add_resource(ProjectController.ProjectDeleteDatabaseAPI, '/api/settings/database/<path:db_name>/delete',endpoint='database_delete')
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/settings/databases',endpoint='show_databases',resource_class_kwargs={'dao' : 'ProjectDAO','get_method' : 'show_databases'})

# Requirement routes
api.add_resource(RequirementController.RequirementsAPI, '/api/requirements',endpoint='requirements')
api.add_resource(RequirementController.RequirementsByAssetAPI, '/api/requirements/asset/<path:name>',endpoint='requirements_assets')
api.add_resource(RequirementController.RequirementsByEnvironmentAPI, '/api/requirements/environment/<path:name>',endpoint='requirement_environments')
api.add_resource(RequirementController.RequirementNamesByAssetAPI, '/api/requirements/asset/<path:name>/names',endpoint='requirements_assets_names')
api.add_resource(RequirementController.RequirementNamesByEnvironmentAPI, '/api/requirements/environment/<path:name>/names',endpoint='requirement_environments_names')
api.add_resource(RequirementController.RequirementByNameAPI, '/api/requirements/name/<path:name>',endpoint='requirement')
api.add_resource(RequirementController.RequirementByNameAPI, '/api/requirements/shortcode/<path:name>',endpoint='requirementshortcode')
api.add_resource(RequirementController.ConceptMapModelAPI, '/api/requirements/model/environment/<path:environment>/requirement/<path:requirement>',endpoint='conceptmapmodel')

# Response routes
api.add_resource(ObjectController.ObjectsAPI, '/api/responses',endpoint='responses',resource_class_kwargs={'dao': 'ResponseDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/responses/name/<path:name>',endpoint='response',resource_class_kwargs={'dao' : 'ResponseDAO'})
api.add_resource(ResponseController.ResponseByNameGenerateAPI, '/api/responses/name/<path:name>/generate_goal',endpoint='generate_goal')

# Risk routes
api.add_resource(ObjectController.ObjectsAPI, '/api/risks',endpoint='risks',resource_class_kwargs={'dao': 'RiskDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/risks/name/<path:name>',endpoint='risk',resource_class_kwargs={'dao' : 'RiskDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/risks/summary',endpoint='riskssummary',resource_class_kwargs={'dao' : 'RiskDAO'})
api.add_resource(
  RiskController.RisksScoreByNameAPI,
  '/api/risks/name/<path:name>/threat/<path:threat>/vulnerability/<path:vulnerability>/environment/<path:environment>',
  '/api/risks/name/<path:name>/vulnerability/<path:vulnerability>/threat/<path:threat>/environment/<path:environment>',endpoint='risk_score')
api.add_resource(
  RiskController.RisksRatingByNameAPI,
  '/api/risks/threat/<path:threat>/vulnerability/<path:vulnerability>/environment/<path:environment>',
  '/api/risks/vulnerability/<path:vulnerability>/threat/<path:threat>/environment/<path:environment>',endpoint='risk_rating'
)
api.add_resource(RiskController.RiskAnalysisModelAPI, '/api/risks/model/environment/<path:environment>',endpoint='risk_model')
api.add_resource(RiskController.RiskAnalysisModelNamesAPI, '/api/risks/model/environment/<path:environment>/names',endpoint='risk_model_name')

# Risk Levels routes
api.add_resource(RiskLevelController.RiskLevelAPI, '/api/risk_level/asset/<path:name>',endpoint='risklevel')
api.add_resource(RiskLevelController.RiskLevelByEnvironmentAPI, '/api/risk_level/asset/<path:name>/environment/<path:environment>',endpoint='risklevelbyenvironment')
api.add_resource(RiskLevelController.RiskThreatLevelAPI, '/api/risk_level/asset/threat_type/<path:asset>/<path:threat>',endpoint='riskthreatlevel')
api.add_resource(RiskLevelController.RiskThreatLevelByEnvironmentAPI, '/api/risk_level/asset/threat_type/<path:asset>/<path:threat>/environment/<path:environment>',endpoint='riskthreatlevelbyenvironment')

# Role routes
api.add_resource(ObjectController.ObjectsAPI, '/api/roles',endpoint='roles',resource_class_kwargs={'dao': 'RoleDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/roles/name/<path:name>',endpoint='role',resource_class_kwargs={'dao' : 'RoleDAO'})
api.add_resource(RoleController.RoleEnvironmentPropertiesAPI, '/api/roles/name/<path:name>/properties',endpoint='role_properties')

# Security pattern routes
api.add_resource(ObjectController.ObjectsAPI, '/api/security_patterns',endpoint='securitypatterns',resource_class_kwargs={'dao': 'SecurityPatternDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/security_patterns/name/<path:name>',endpoint='securitypattern',resource_class_kwargs={'dao' : 'SecurityPatternDAO'})
api.add_resource(SecurityPatternController.SituateSecurityPatternAPI, '/api/security_patterns/name/<path:security_pattern_name>/environment/<path:environment_name>/situate', endpoint='situatesecuritypattern')

# Summary routes
api.add_resource(SummaryController.SummaryAPI, '/api/summary/dimension/<path:dimension_name>/environment/<path:environment_name>',endpoint='summary')

# Task routes
api.add_resource(ObjectController.ObjectsAPI, '/api/tasks',endpoint='tasks',resource_class_kwargs={'dao': 'TaskDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/tasks/name/<path:name>',endpoint='task',resource_class_kwargs={'dao' : 'TaskDAO'})
api.add_resource(TaskController.TaskModelByNameAPI, '/api/tasks/model/environment/<path:environment>/task/<path:task>/misusecase/<path:misusecase>',endpoint='task_model')
api.add_resource(TaskController.TaskLoadByNameAPI, '/api/tasks/name/<path:task>/environment/<path:environment>/load',endpoint='task_load')
api.add_resource(TaskController.TaskHindranceByNameAPI, '/api/tasks/name/<path:task>/environment/<path:environment>/hindrance',endpoint='task_hindrance')
api.add_resource(TaskController.TaskScoreByNameAPI, '/api/tasks/name/<path:task>/environment/<path:environment>/score',endpoint='task_score')
api.add_resource(TaskController.MisusabilityModelAPI, '/api/tasks/model/misusability/<path:mc_name>/characteristic/<path:tc_name>',endpoint='misusability_model')

# Task Characteristic routes
api.add_resource(ObjectController.ObjectsAPI, '/api/task_characteristics',endpoint='task_characteristics',resource_class_kwargs={'dao': 'TaskCharacteristicDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/task_characteristics/name/<path:name>',endpoint='task_characteristic',resource_class_kwargs={'dao' : 'TaskCharacteristicDAO'})

# Template Asset routes
api.add_resource(ObjectController.ObjectsAPI, '/api/template_assets',endpoint='template_assets',resource_class_kwargs={'dao': 'TemplateAssetDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/template_assets/name/<path:name>',endpoint='templateasset',resource_class_kwargs={'dao' : 'TemplateAssetDAO'})

# Template Goal routes
api.add_resource(ObjectController.ObjectsAPI, '/api/template_goals',endpoint='template_goals',resource_class_kwargs={'dao': 'TemplateGoalDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/template_goals/name/<path:name>',endpoint='templategoal',resource_class_kwargs={'dao' : 'TemplateGoalDAO'})

# Template Requirement routes
api.add_resource(ObjectController.ObjectsAPI, '/api/template_requirements',endpoint='template_requirements',resource_class_kwargs={'dao': 'TemplateRequirementDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/template_requirements/name/<path:name>',endpoint='template_requirement',resource_class_kwargs={'dao' : 'TemplateRequirementDAO'})

# Threat routes
api.add_resource(ObjectController.ObjectsAPI, '/api/threats',endpoint='threats',resource_class_kwargs={'dao': 'ThreatDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/threats/name/<path:name>',endpoint='threat',resource_class_kwargs={'dao' : 'ThreatDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/threats/summary',endpoint='threatssummary',resource_class_kwargs={'dao' : 'ThreatDAO'})
api.add_resource(ThreatController.ThreatTypesAPI, '/api/threats/types',endpoint='threat_types')
api.add_resource(ThreatController.ThreatTypeByNameAPI, '/api/threats/types/name/<path:name>',endpoint='threat_type')
api.add_resource(ThreatController.ThreatModelAPI, '/api/threats/model/environment/<path:environment_name>',endpoint='threat_model')

# Trace routes
api.add_resource(TraceController.TracesAPI, '/api/traces',endpoint='traces')
api.add_resource(TraceController.TraceByEnvironmentAPI, '/api/traces/environment/<path:environment_name>',endpoint='traces_environment')
api.add_resource(TraceController.TraceDimensionsAPI, '/api/traces/dimensions/<path:dimension_name>/is_from/<path:is_from>',endpoint='trace_dimensions')
api.add_resource(TraceController.TraceByNameAPI, '/api/traces/from_type/<path:from_object>/from_name/<path:from_name>/to_type/<path:to_object>/to_name/<path:to_name>',endpoint='traces_name')

# Trust Boundary routes
api.add_resource(ObjectController.ObjectsAPI, '/api/trust_boundaries',endpoint='trustboundaries',resource_class_kwargs={'dao': 'TrustBoundaryDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/trust_boundaries/name/<path:name>',endpoint='trustboundary',resource_class_kwargs={'dao' : 'TrustBoundaryDAO'})

# Upload controller
api.add_resource(UploadController.UploadImageAPI, '/api/upload/image',endpoint='upload')

# Use Case routes
api.add_resource(UseCaseController.UseCasesAPI, '/api/usecases',endpoint='usecases')
api.add_resource(UseCaseController.UseCaseByNameAPI, '/api/usecases/name/<path:name>',endpoint='usecase')
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/usecases/summary',endpoint='usecasessummary',resource_class_kwargs={'dao' : 'UseCaseDAO'})
api.add_resource(UseCaseController.UseCaseRequirementsByNameAPI, '/api/usecases/name/<path:usecase_name>/requirements',endpoint='usecaserequirements')
api.add_resource(UseCaseController.UseCaseGoalsByNameAPI, '/api/usecases/name/<path:usecase_name>/environment/<path:environment_name>/goals',endpoint='usecasegoals')

# User goal routes
api.add_resource(ObjectController.ObjectsAPI, '/api/user_goals',endpoint='user_goals',resource_class_kwargs={'dao': 'UserGoalDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/user_goals/name/<path:name>',endpoint='usergoal',resource_class_kwargs={'dao' : 'UserGoalDAO'})
api.add_resource(UserGoalController.UserGoalModelAPI, '/api/user_goals/model/environment/<path:environment_name>/filter_name/<path:filter_element>',endpoint='usergoalmodel')

# Validation route
api.add_resource(ValidationController.ValidationAPI, '/api/validation/environment/<path:name>',endpoint='environmentvalidation')

# Value Type routes
api.add_resource(ValueTypeController.ValueTypesAPI, '/api/value_types/type/<path:type_name>/environment/<path:environment_name>',endpoint='value_types')
api.add_resource(ValueTypeController.ValueTypesByNameAPI, '/api/value_types/type/<path:type_name>/environment/<path:environment_name>/name/<path:object_name>',endpoint='value_type')


api.add_resource(ValueTypeController.ValueTypesCreateAPI, '/api/value_types/',endpoint='create_value_type')

# Version route
api.add_resource(VersionController.VersionAPI, '/api/version',endpoint='version')

# Vulnerability routes
api.add_resource(ObjectController.ObjectsAPI, '/api/vulnerabilities',endpoint='vulnerabilities',resource_class_kwargs={'dao': 'VulnerabilityDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/vulnerabilities/name/<path:name>',endpoint='vulnerabilitiy',resource_class_kwargs={'dao' : 'VulnerabilityDAO'})
api.add_resource(VulnerabilityController.VulnerabilityTypesAPI, '/api/vulnerabilities/types',endpoint='vulnerability_types')
api.add_resource(VulnerabilityController.VulnerabilityTypeByNameAPI, '/api/vulnerabilities/types/name/<path:name>',endpoint='vulnerability_type_name')

