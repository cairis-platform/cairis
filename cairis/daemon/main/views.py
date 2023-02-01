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
from cairis.controllers import CImportController
from cairis.controllers import DocumentationController
from cairis.controllers import ObjectController
from cairis.controllers import UploadController
from cairis.core.dba import dbtoken

from cairis.daemon.main import main, api
from cairis.tools.SessionValidator import get_session_id
from base64 import b64decode
import io
import datetime

__author__ = 'Robin Quetin, Shamal Faily'

def set_dbproxy(dbUser,userName):
  b = Borg()
  dbPasswd = dbtoken(b.rPasswd,b.dbHost,b.dbPort,dbUser)
  userName = dbUser
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
api.add_resource(ObjectController.ModelByParameterAPI, '/api/architectural_patterns/component/goal/model/<path:parameter_string>',endpoint='componentgoals',resource_class_kwargs={'dao' : 'ArchitecturalPatternDAO','get_method' : 'get_component_goal_model','renderer' : 'dot'})
api.add_resource(ObjectController.ModelByParameterAPI, '/api/architectural_patterns/component/asset/model/<path:parameter_string>',endpoint='componentassets',resource_class_kwargs={'dao' : 'ArchitecturalPatternDAO','get_method' : 'get_component_asset_model','renderer' : 'dot'})
api.add_resource(ObjectController.ModelByParameterAPI, '/api/architectural_patterns/component/model/<path:parameter_string>',endpoint='componentmodel',resource_class_kwargs={'dao' : 'ArchitecturalPatternDAO','get_method' : 'get_component_model','renderer' : 'dot'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/architectural_patterns/name/<path:p1>/environment/<path:p2>/weakness_analysis',endpoint='weakness_analysis',resource_class_kwargs={'dao' : 'ArchitecturalPatternDAO','get_method' : 'get_weakness_analysis'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/architectural_patterns/name/<path:p1>/environment/<path:p2>/situate',endpoint='situate',resource_class_kwargs={'dao' : 'ArchitecturalPatternDAO','post_method' : 'situate_component_view','post_message' : 'Architectural Pattern successfully situated'})

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
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/countermeasures/name/<path:parameter_string>/generate_asset',endpoint='countermeasure_generate_asset', resource_class_kwargs={'dao' : 'CountermeasureDAO', 'post_method' : 'generate_asset'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/countermeasures/name/<path:p1>/template_asset/<path:p2>/generate_asset',endpoint='countermeasure_generate_asset_from_template', resource_class_kwargs={'dao' : 'CountermeasureDAO', 'post_method' : 'generate_asset_from_template'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/countermeasures/name/<path:p1>/security_pattern/<path:p2>/situate',endpoint='countermeasure_situate_countermeasure_pattern', resource_class_kwargs={'dao' : 'CountermeasureDAO', 'post_method' : 'situate_countermeasure_pattern'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/countermeasures/name/<path:p1>/security_pattern/<path:p2>/associate_situated',endpoint='associate_situated_pattern', resource_class_kwargs={'dao' : 'CountermeasureDAO', 'post_method' : 'associate_situated_pattern'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/countermeasures/name/<path:p1>/security_pattern/<path:p2>/remove_situated',endpoint='remove_situated_pattern', resource_class_kwargs={'dao' : 'CountermeasureDAO', 'del_method' : 'remove_situated_pattern'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/countermeasures/targets/environment/<path:parameter_string>',endpoint='targets',resource_class_kwargs={'dao' : 'CountermeasureDAO','get_method' : 'get_countermeasure_targets', 'path_parameters' : [('requirement',[])]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/countermeasures/tasks/environment/<path:parameter_string>',endpoint='countermeasuretasks',resource_class_kwargs={'dao' : 'CountermeasureDAO','get_method' : 'get_countermeasure_tasks', 'path_parameters' : [('role',[])]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/countermeasures/name/<path:parameter_string>/candidate_patterns',endpoint='candidate_patterns',resource_class_kwargs={'dao' : 'CountermeasureDAO', 'get_method' : 'candidate_countermeasure_patterns'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/countermeasures/name/<path:parameter_string>/patterns',endpoint='countermeasure_patterns', resource_class_kwargs={'dao':'CountermeasureDAO', 'get_method' : 'countermeasure_patterns'})

# Dataflow routes
api.add_resource(ObjectController.ObjectsAPI, '/api/dataflows',endpoint='dataflows',resource_class_kwargs={'dao': 'DataFlowDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndSixParametersAPI, '/api/dataflows/name/<path:p1>/from_name/<path:p2>/from_type/<path:p3>/to_name/<path:p4>/to_type/<path:p5>/environment/<path:p6>',endpoint='dataflow',resource_class_kwargs={'dao': 'DataFlowDAO','get_method' : 'get_object_by_name', 'put_method' : 'update_object', 'del_method' : 'delete_object'})
api.add_resource(ObjectController.ModelByThreeParametersAPI, '/api/dataflows/diagram/environment/<path:p1>/filter_type/<path:p2>/filter_name/<path:p3>',endpoint='dataflowdiagram',resource_class_kwargs={'dao' : 'DataFlowDAO','get_method' : 'get_dataflow_diagram','renderer' : 'dot', 'model_type' : 'dataflow'})
api.add_resource(ObjectController.ModelByTwoParametersAPI, '/api/dataflows/control_structure/environment/<path:p1>/filter_name/<path:p2>',endpoint='controlstructure',resource_class_kwargs={'dao' : 'DataFlowDAO','get_method' : 'get_control_structure','renderer' : 'dot', 'model_type' : 'control_structure'})

# Dependency routes
api.add_resource(ObjectController.ObjectsAPI, '/api/dependencies',endpoint='dependencies',resource_class_kwargs={'dao': 'DependencyDAO'})
api.add_resource(ObjectController.ObjectByFourParametersAPI, '/api/dependencies/environment/<p1>/depender/<p2>/dependee/<p3>/dependency/<p4>',endpoint='dependency',resource_class_kwargs={'dao': 'DependencyDAO'})

# Dimension routes
api.add_resource(ObjectController.ConstrainedObjectsByNameAPI, '/api/dimensions/table/<path:parameter_string>',endpoint='dimensions',resource_class_kwargs={'dao' : 'DimensionDAO','constraint_parameter' : 'constraint_id'})
api.add_resource(ObjectController.ObjectsByTwoParametersAPI, '/api/dimensions/table/<path:p1>/environment/<path:p2>',endpoint='dimension',resource_class_kwargs={'dao' : 'DimensionDAO'})

# DirectoryController
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/directory/threat/<path:parameter_string>',endpoint='threatdirectory',resource_class_kwargs={'dao' : 'DirectoryDAO','get_method' : 'get_threat_directory'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/directory/vulnerability/<path:parameter_string>',endpoint='vulnerabilitydirectory',resource_class_kwargs={'dao' : 'DirectoryDAO','get_method' : 'get_vulnerability_directory'})

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
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI,'/api/environments/threat/<path:p1>/vulnerability/<path:p2>/names',endpoint='environment_names_tv', resource_class_kwargs={'dao':'EnvironmentDAO',  'get_method' : 'get_environment_names_by_threat_vulnerability'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI,'/api/environments/vulnerability/<path:p1>/threat/<path:p2>/names',endpoint='environment_names_vt', resource_class_kwargs={'dao':'EnvironmentDAO',  'get_method' : 'get_environment_names_by_vulnerability_threat'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI,'/api/environments/risk/<path:parameter_string>/names',endpoint='environment_names_risk', resource_class_kwargs={'dao':'EnvironmentDAO',  'get_method' : 'get_environment_names_by_risk'})

# External Document routes
api.add_resource(ObjectController.ObjectsAPI, '/api/external_documents',endpoint='external_documents',resource_class_kwargs={'dao': 'ExternalDocumentDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/external_documents/name/<path:name>',endpoint='external_document',resource_class_kwargs={'dao' : 'ExternalDocumentDAO'})


# Goal routes
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/goals',endpoint='goals',resource_class_kwargs={'dao': 'GoalDAO', 'get_method' : 'get_objects', 'post_method' : 'add_object', 'path_parameters' : [('constraint_id',-1),('coloured',False)]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/goals/name/<path:parameter_string>',endpoint='goal',resource_class_kwargs={'dao' : 'GoalDAO', 'put_method' : 'update_object', 'get_method' : 'get_object_by_name', 'del_method' : 'delete_object', 'path_parameters' : [('constraint_id',-1),('coloured',False)]})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/goals/summary',endpoint='goalssummary',resource_class_kwargs={'dao' : 'GoalDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/goals/environment/<path:parameter_string>/names',endpoint='goal_environment',resource_class_kwargs={'dao' : 'GoalDAO', 'get_method' : 'get_goal_names'})
api.add_resource(ObjectController.ModelByThreeParametersAPI, '/api/goals/model/environment/<path:p1>/goal/<path:p2>/usecase/<path:p3>',endpoint='goalmodel',resource_class_kwargs={'dao' : 'GoalDAO','get_method' : 'get_goal_model','renderer' : 'dot', 'path_parameters' : [('top','0')], 'model_type' : 'goal'})
api.add_resource(ObjectController.ModelByTwoParametersAPI, '/api/responsibility/model/environment/<path:p1>/role/<path:p2>',endpoint='responsibilitymodel',resource_class_kwargs={'dao' : 'GoalDAO','get_method' : 'get_responsibility_model','renderer' : 'dot', 'model_type' : 'responsibility'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/goals/association',endpoint='goal_associations',resource_class_kwargs={'dao': 'GoalAssociationDAO', 'get_method' : 'get_goal_associations', 'post_method' : 'add_goal_association', 'path_parameters' : [('environment_name','')]})
api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI,'/api/goals/association/environment/<path:p1>/goal/<path:p2>/subgoal/<path:p3>',endpoint='goal_association',resource_class_kwargs={'dao' : 'GoalAssociationDAO', 'get_method' : 'get_goal_association', 'put_method' : 'update_goal_association', 'del_method' : 'delete_goal_association'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI,'/api/goals/name/<path:p1>/environment/<path:p2>/concerns',endpoint='goal_concerns',resource_class_kwargs={'dao' : 'GoalDAO', 'get_method' : 'get_goal_concerns'})


# Goal contribution routes
api.add_resource(ObjectController.ObjectsAPI, '/api/goal_contributions',endpoint='goal_contributions',resource_class_kwargs={'dao': 'GoalContributionDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/goal_contributions/source/<path:p1>/target/<path:p2>',endpoint='goal_contribution',resource_class_kwargs={'dao' : 'GoalContributionDAO','get_method' : 'get_objects', 'put_method' : 'update_object', 'del_method' : 'delete_object'})

# Export routes
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/export/file',endpoint='export',resource_class_kwargs={'dao' : 'ExportDAO', 'get_method' : 'file_export', 'path_parameters' : [('filename','model'),('fileType','xml')]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/export/file/architectural_pattern/<path:parameter_string>',endpoint='exportarchitecturalpattern', resource_class_kwargs={'dao' : 'ExportDAO', 'get_method' : 'architectural_pattern_export', 'path_parameters' : [('filename','')]})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/export/file/persona_characteristics',endpoint='exportpersonacharacteristics', resource_class_kwargs={'dao' : 'ExportDAO', 'get_method' : 'persona_characteristics_export', 'path_parameters' : [('filename','personaCharacteristics.xlsx')]})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/export/file/user_goals',endpoint='exportusergoals', resource_class_kwargs={'dao' : 'ExportDAO', 'get_method' : 'user_goals_export', 'path_parameters' : [('filename','userGoals.xlsx')]})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/export/file/security_patterns',endpoint='exportsecuritypatterns',resource_class_kwargs={'dao' : 'ExportDAO', 'get_method' : 'security_patterns_export', 'path_parameters' : [('filename','security_patterns.xml')]})
api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI, '/api/export/file/grl/task/<path:p1>/persona/<path:p2>/environment/<path:p3>',endpoint='exportgrl', resource_class_kwargs={'dao' : 'ExportDAO', 'get_method' : 'grl_export', 'path_parameters' : [('filename','')]})

# Find route
api.add_resource(ObjectController.ObjectsByNameAPI, '/api/find/<path:parameter_string>',endpoint='find',resource_class_kwargs={'dao' : 'FindDAO'})

# Import routes
api.add_resource(CImportController.CImportPackageAPI, '/api/import/package',endpoint='import_package')
api.add_resource(CImportController.CImportTextAPI, '/api/import/text',endpoint='import_text')
api.add_resource(CImportController.CImportFileAPI, '/api/import/file/type/<path:type>',endpoint='import_file')
api.add_resource(ObjectController.WorkbookUploadAPI, '/api/import/file/persona_characteristics',endpoint='import_persona_characteristics',resource_class_kwargs={'dao': 'ImportDAO','post_method' : 'import_persona_characteristics'})
api.add_resource(ObjectController.WorkbookUploadAPI, '/api/import/file/user_goals',endpoint='import_user_goals',resource_class_kwargs={'dao': 'ImportDAO','post_method' : 'import_user_goals'})

# Locations routes
api.add_resource(ObjectController.ObjectsAPI, '/api/locations',endpoint='locations',resource_class_kwargs={'dao': 'LocationsDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/locations/name/<path:name>',endpoint='location',resource_class_kwargs={'dao' : 'LocationsDAO'})
api.add_resource(ObjectController.ModelByTwoParametersAPI, '/api/locations/model/locations/<path:p1>/environment/<path:p2>',endpoint='locationmodel',resource_class_kwargs={'dao' : 'LocationsDAO','get_method' : 'get_locations_model','renderer' : 'dot'})

# Misuse case routes
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/misusecases',endpoint='misusecases',resource_class_kwargs={'dao': 'RiskDAO','get_method' : 'get_misuse_cases', 'path_parameters' : [('constraint_id',-1)]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/misusecases/name/<path:parameter_string>',endpoint='misusecase',resource_class_kwargs={'dao': 'RiskDAO','get_method' : 'get_misuse_case_by_name'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/misusecases/risk/<path:parameter_string>',endpoint='misusecase_risk',resource_class_kwargs={'dao': 'RiskDAO','get_method' : 'get_misuse_case_by_risk_name'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/misusecases/threat/<path:p1>/vulnerability/<path:p2>',endpoint='misusecase_tv',resource_class_kwargs={'dao' : 'RiskDAO','get_method' : 'get_misuse_case_by_threat_vulnerability'})

# Object dependency routes
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/object_dependency/dimension/<path:p1>/object/<path:p2>',endpoint='object_dependency',resource_class_kwargs={'dao' : 'ObjectDependencyDAO','get_method' : 'report_dependencies', 'del_method' : 'delete_dependencies', 'del_message' : 'Object dependencies successfully deleted'})

# Obstacle routes
api.add_resource(ObjectController.ObjectsAPI, '/api/obstacles',endpoint='obstacles',resource_class_kwargs={'dao': 'ObstacleDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/obstacles/name/<path:name>',endpoint='obstacle',resource_class_kwargs={'dao' : 'ObstacleDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/obstacles/summary',endpoint='obstaclessummary',resource_class_kwargs={'dao' : 'ObstacleDAO'})

api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/obstacles/name/<path:parameter_string>/generate_vulnerability',endpoint='generatevulnerability',resource_class_kwargs={'dao' : 'ObstacleDAO','post_method' : 'generate_vulnerability','post_message' : 'Vulnerability successfully generated'})
api.add_resource(ObjectController.ModelByTwoParametersAPI, '/api/obstacles/model/environment/<path:p1>/obstacle/<path:p2>',endpoint='obstaclemodel',resource_class_kwargs={'dao' : 'ObstacleDAO','get_method' : 'get_obstacle_model','renderer' : 'dot'})

# Permissions routes
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/permissions/database/<path:parameter_string>',endpoint='permissions', resource_class_kwargs={'dao' : 'PermissionsDAO', 'get_method' : 'get_permissions'})
api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI, '/api/permissions/database/<path:p1>/user/<path:p2>/permission/<path:p3>',endpoint='changepermission', resource_class_kwargs={'dao' : 'PermissionsDAO', 'post_method' : 'set_permission'})

# Persona routes
api.add_resource(ObjectController.ObjectsAPI, '/api/personas',endpoint='personas',resource_class_kwargs={'dao': 'PersonaDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/personas/name/<path:name>',endpoint='persona',resource_class_kwargs={'dao' : 'PersonaDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/personas/summary',endpoint='personassummary',resource_class_kwargs={'dao' : 'PersonaDAO'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/personas/names',endpoint='persona_names',resource_class_kwargs={'dao' : 'PersonaDAO','get_method' : 'get_persona_names'})
api.add_resource(ObjectController.ModelByThreeParametersAPI, '/api/personas/model/name/<path:p1>/variable/<path:p2>/characteristic/<path:p3>',endpoint='persona_model',resource_class_kwargs={'dao' : 'PersonaDAO','get_method' : 'get_persona_model','renderer' : 'dot', 'model_type' : 'persons'})

api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI,'/api/personas/characteristics/name/<path:p1>/variable/<path:p2>/characteristic/<path:p3>',endpoint='persona_characteristic_persona',resource_class_kwargs={'dao' : 'PersonaDAO', 'get_method' : 'get_persona_characteristics'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/personas/types',endpoint='persona_types',resource_class_kwargs={'dao' : 'PersonaDAO','get_method' : 'get_persona_types'})

# Persona Characteristic routes
api.add_resource(ObjectController.ObjectsAPI, '/api/persona_characteristics',endpoint='persona_characteristics',resource_class_kwargs={'dao': 'PersonaCharacteristicDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/persona_characteristics/name/<path:name>',endpoint='persona_characteristic',resource_class_kwargs={'dao' : 'PersonaCharacteristicDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/persona_characteristics/summary',endpoint='personacharacteristicssummary',resource_class_kwargs={'dao' : 'PersonaCharacteristicDAO'})

# Policy Statement routes
api.add_resource(ObjectController.ObjectsAPI, '/api/policy_statements',endpoint='policy_statements',resource_class_kwargs={'dao': 'PolicyStatementDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndFiveParametersAPI,'/api/policy_statements/goal/<path:p1>/environment/<path:p2>/subject/<path:p3>/access_type/<path:p4>/resource/<path:p5>',endpoint='policy_statement',resource_class_kwargs={'dao' : 'PolicyStatementDAO', 'get_method' : 'get_object_by_name', 'put_method' : 'update_object', 'del_method' : 'delete_object'})

# Project routes
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/settings',endpoint='project_settings',resource_class_kwargs={'dao' : 'ProjectDAO','get_method' : 'get_settings','put_method' : 'apply_settings'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/settings/clear',endpoint='project_clear', resource_class_kwargs={'dao' : 'ProjectDAO', 'post_method' : 'clear_project'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/settings/database/<path:parameter_string>/create',endpoint='database_create',resource_class_kwargs={'dao' : 'ProjectDAO', 'post_method' : 'create_new_database'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/settings/database/<path:parameter_string>/open',endpoint='database_open',resource_class_kwargs={'dao' : 'ProjectDAO', 'post_method' : 'open_database'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/settings/database/<path:parameter_string>/delete',endpoint='database_delete', resource_class_kwargs={'dao' : 'ProjectDAO', 'post_method' : 'delete_database'})
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/settings/databases',endpoint='show_databases',resource_class_kwargs={'dao' : 'ProjectDAO','get_method' : 'show_databases'})

# Requirement routes
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/requirements',endpoint='requirements', resource_class_kwargs={'dao' : 'RequirementDAO', 'get_method' : 'get_requirements', 'post_method' : 'add_requirement', 'path_parameters' : [('ordered',0),('constraint_id',''),('asset',None),('environment',None)]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/requirements/asset/<path:parameter_string>',endpoint='requirement_assets',resource_class_kwargs={'dao' : 'RequirementDAO', 'get_method' : 'get_requirements_by_asset','path_parameters' : [('ordered',1)]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/requirements/environment/<path:parameter_string>',endpoint='requirement_environments',resource_class_kwargs={'dao' : 'RequirementDAO', 'get_method' : 'get_requirements_by_environment','path_parameters' : [('ordered',1)]})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/requirements/asset/<path:parameter_string>/names',endpoint='requirements_assets_names',resource_class_kwargs={'dao' : 'RequirementDAO', 'get_method' : 'get_asset_requirement_names'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/requirements/environment/<path:parameter_string>/names',endpoint='requirement_environments_names',resource_class_kwargs={'dao' : 'RequirementDAO', 'get_method' : 'get_environment_requirement_names'})

api.add_resource(ObjectController.ObjectByNameAPI, '/api/requirements/name/<path:name>','/api/requirements/shortcode/<path:name>',endpoint='requirement',resource_class_kwargs={'dao' : 'RequirementDAO'})
api.add_resource(ObjectController.ModelByTwoParametersAPI, '/api/requirements/model/environment/<path:p1>/requirement/<path:p2>',endpoint='conceptmapmodel',resource_class_kwargs={'dao' : 'RequirementDAO','get_method' : 'get_concept_map_model','renderer' : 'dot','path_parameters' : [('asset','0')]})

# Response routes
api.add_resource(ObjectController.ObjectsAPI, '/api/responses',endpoint='responses',resource_class_kwargs={'dao': 'ResponseDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/responses/name/<path:name>',endpoint='response',resource_class_kwargs={'dao' : 'ResponseDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/responses/name/<path:parameter_string>/generate_goal',endpoint='generate_goal',resource_class_kwargs={'dao' : 'ResponseDAO','post_method' : 'generate_goal','post_message' : 'Goal successfully generated'})

# Risk routes
api.add_resource(ObjectController.ObjectsAPI, '/api/risks',endpoint='risks',resource_class_kwargs={'dao': 'RiskDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/risks/name/<path:name>',endpoint='risk',resource_class_kwargs={'dao' : 'RiskDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/risks/summary',endpoint='riskssummary',resource_class_kwargs={'dao' : 'RiskDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndFourParametersAPI,'/api/risks/name/<path:p1>/threat/<path:p2>/vulnerability/<path:p3>/environment/<path:p4>',endpoint='risk_score_rtve',resource_class_kwargs={'dao': 'RiskDAO', 'get_method' : 'get_scores_by_rtve'})
api.add_resource(ObjectController.ObjectsByMethodAndFourParametersAPI, '/api/risks/name/<path:p1>/vulnerability/<path:p2>/threat/<path:p3>/environment/<path:p4>',endpoint='risk_score_rvte', resource_class_kwargs={'dao' : 'RiskDAO','get_method' : 'get_scores_by_rvte'})
api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI,'/api/risks/threat/<path:p1>/vulnerability/<path:p2>/environment/<path:p3>',endpoint='risk_rating_tve',resource_class_kwargs={'dao' : 'RiskDAO', 'get_method' : 'get_risk_rating_by_tve'})
api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI,'/api/risks/vulnerability/<path:p1>/threat/<path:p2>/environment/<path:p3>',endpoint='risk_rating_vte',resource_class_kwargs={'dao' : 'RiskDAO', 'get_method' : 'get_risk_rating_by_vte'})
api.add_resource(ObjectController.ModelByParameterAPI, '/api/risks/model/environment/<path:parameter_string>',endpoint='risk_model',resource_class_kwargs={'dao' : 'RiskDAO','get_method' : 'get_risk_analysis_model', 'path_parameters' : [('dimension_name',''),('object_name',''),('tagged','0'),('orientation','Vertical'),('layout','Hierarchical')], 'model_type' : 'risk'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/risks/model/environment/<path:parameter_string>/names',endpoint='risk_model_name',resource_class_kwargs={'dao' : 'RiskDAO','get_method' : 'risk_model_elements'})

# Risk Levels routes
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/risk_level/asset/<path:parameter_string>',endpoint='risklevel',resource_class_kwargs={'dao' : 'RiskLevelDAO','get_method' : 'get_risk_level'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/risk_level/asset/<path:p1>/environment/<path:p2>',endpoint='risklevelbyenvironment',resource_class_kwargs={'dao' : 'RiskLevelDAO','get_method' : 'get_risk_level_by_environment'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/risk_level/asset/threat_type/<path:p1>/<path:p2>',endpoint='riskthreatlevel',resource_class_kwargs={'dao' : 'RiskLevelDAO','get_method' : 'get_risk_threat_level'})
api.add_resource(ObjectController.ObjectsByMethodAndThreeParametersAPI, '/api/risk_level/asset/threat_type/<path:p1>/<path:p2>/environment/<path:p3>',endpoint='riskthreatlevelbyenvironment',resource_class_kwargs={'dao' : 'RiskLevelDAO','get_method' : 'get_risk_threat_level_by_environment'})

# Role routes
api.add_resource(ObjectController.ObjectsAPI, '/api/roles',endpoint='roles',resource_class_kwargs={'dao': 'RoleDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/roles/name/<path:name>',endpoint='role',resource_class_kwargs={'dao' : 'RoleDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/roles/name/<path:parameter_string>/properties',endpoint='role_properties',resource_class_kwargs={'dao' : 'RoleDAO','get_method' : 'get_role_props'})

# Security pattern routes
api.add_resource(ObjectController.ObjectsAPI, '/api/security_patterns',endpoint='securitypatterns',resource_class_kwargs={'dao': 'SecurityPatternDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/security_patterns/name/<path:name>',endpoint='securitypattern',resource_class_kwargs={'dao' : 'SecurityPatternDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/security_patterns/name/<path:p1>/environment/<path:p2>/situate',endpoint='situatesecuritypattern',resource_class_kwargs={'dao' : 'SecurityPatternDAO','post_method' : 'situate_security_pattern','post_message' : 'Security Pattern successfully situated'})

# Summary routes
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/summary/dimension/<path:p1>/environment/<path:p2>',endpoint='summary',resource_class_kwargs={'dao' : 'SummaryDAO','get_method' : 'get_summary'})

# Task routes
api.add_resource(ObjectController.ObjectsAPI, '/api/tasks',endpoint='tasks',resource_class_kwargs={'dao': 'TaskDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/tasks/name/<path:name>',endpoint='task',resource_class_kwargs={'dao' : 'TaskDAO'})


api.add_resource(ObjectController.ModelByThreeParametersAPI, '/api/tasks/model/environment/<path:p1>/task/<path:p2>/misusecase/<path:p3>',endpoint='task_model',resource_class_kwargs={'dao' : 'TaskDAO','get_method' : 'get_task_model','renderer' : 'dot', 'model_type' : 'task'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/tasks/name/<path:p1>/environment/<path:p2>/load',endpoint='task_load',resource_class_kwargs={'dao' : 'TaskDAO','get_method' : 'task_load_by_name_environment'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/tasks/name/<path:p1>/environment/<path:p2>/hindrance',endpoint='task_hindrance',resource_class_kwargs={'dao' : 'TaskDAO','get_method' : 'task_hindrance_by_name_environment'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/tasks/name/<path:p1>/environment/<path:p2>/score',endpoint='task_score',resource_class_kwargs={'dao' : 'TaskDAO','get_method' : 'task_score_by_name_environment'})
api.add_resource(ObjectController.ModelByTwoParametersAPI, '/api/tasks/model/misusability/<path:p1>/characteristic/<path:p2>',endpoint='misusability_model',resource_class_kwargs={'dao' : 'TaskDAO','get_method' : 'get_misusability_model','renderer' : 'dot','model_type' : 'misusability'})

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
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/threats/model/environment/<path:parameter_string>',endpoint='threat_model',resource_class_kwargs={'dao' : 'ThreatDAO','get_method' : 'get_threat_model'})

# Trace routes
api.add_resource(ObjectController.ObjectsAPI, '/api/traces',endpoint='traces',resource_class_kwargs={'dao': 'TraceDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/traces/environment/<path:parameter_string>',endpoint='traces_environment', resource_class_kwargs={'dao' : 'TraceDAO', 'get_method' : 'get_traces'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/traces/dimensions/<path:p1>/is_from/<path:p2>',endpoint='trace_dimensions', resource_class_kwargs={'dao' : 'TraceDAO', 'get_method' : 'trace_dimensions'})
api.add_resource(ObjectController.ObjectsByMethodAndFourParametersAPI, '/api/traces/from_type/<path:p1>/from_name/<path:p2>/to_type/<path:p3>/to_name/<path:p4>',endpoint='traces_name',resource_class_kwargs={'dao' : 'TraceDAO','del_method' : 'delete_trace'})

# Trust Boundary routes
api.add_resource(ObjectController.ObjectsAPI, '/api/trust_boundaries',endpoint='trustboundaries',resource_class_kwargs={'dao': 'TrustBoundaryDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/trust_boundaries/name/<path:name>',endpoint='trustboundary',resource_class_kwargs={'dao' : 'TrustBoundaryDAO'})

# Upload controller
api.add_resource(UploadController.UploadImageAPI, '/api/upload/image',endpoint='upload')

# Use Case routes
api.add_resource(ObjectController.ObjectsAPI, '/api/usecases',endpoint='usecases',resource_class_kwargs={'dao': 'UseCaseDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/usecases/name/<path:name>',endpoint='usecase',resource_class_kwargs={'dao' : 'UseCaseDAO'})
api.add_resource(ObjectController.ObjectsSummaryAPI, '/api/usecases/summary',endpoint='usecasessummary',resource_class_kwargs={'dao' : 'UseCaseDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/usecases/name/<path:parameter_string>/requirements',endpoint='usecaserequirements',resource_class_kwargs={'dao' : 'UseCaseDAO', 'get_method' : 'get_usecase_requirements'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/usecases/name/<path:p1>/environment/<path:p2>/goals',endpoint='usecasegoals', resource_class_kwargs={'dao' : 'UseCaseDAO', 'get_method' : 'get_usecase_goals'})

# User goal routes
api.add_resource(ObjectController.ObjectsAPI, '/api/user_goals',endpoint='user_goals',resource_class_kwargs={'dao': 'UserGoalDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/user_goals/name/<path:name>',endpoint='usergoal',resource_class_kwargs={'dao' : 'UserGoalDAO'})
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/user_goals/role/<path:parameter_string>',endpoint='roleusergoals',resource_class_kwargs={'dao' : 'UserGoalDAO','get_method' : 'role_user_goals'})
api.add_resource(ObjectController.ObjectsByMethodAndTwoParametersAPI, '/api/user_goals/model/environment/<path:p1>/persona/<path:p2>/filters',endpoint='usergoalfilters',resource_class_kwargs={'dao' : 'UserGoalDAO','get_method' : 'user_goal_filters'})
api.add_resource(ObjectController.ModelByThreeParametersAPI, '/api/user_goals/model/environment/<path:p1>/persona/<path:p2>/filter_name/<path:p3>',endpoint='usergoalmodel',resource_class_kwargs={'dao' : 'UserGoalDAO','get_method' : 'get_user_goal_model','renderer' : 'dot'})

# User story routes
api.add_resource(ObjectController.ObjectsAPI, '/api/userstories',endpoint='userstories',resource_class_kwargs={'dao': 'UserStoryDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/userstories/name/<path:name>',endpoint='userstory',resource_class_kwargs={'dao' : 'UserStoryDAO'})

# Validation route
api.add_resource(ObjectController.ObjectsByMethodAndParameterAPI, '/api/validation/environment/<path:parameter_string>',endpoint='environmentvalidation',resource_class_kwargs={'dao' : 'ValidationDAO','get_method' : 'model_validation'})

# Value Type routes
api.add_resource(ObjectController.ObjectsByTwoParametersAPI, '/api/value_types/type/<path:p1>/environment/<path:p2>',endpoint='value_types',resource_class_kwargs={'dao' : 'ValueTypeDAO'})
api.add_resource(ObjectController.ObjectByThreeParametersAPI, '/api/value_types/type/<path:p1>/environment/<path:p2>/name/<path:p3>',endpoint='value_type',resource_class_kwargs={'dao' : 'ValueTypeDAO'})
api.add_resource(ObjectController.ObjectsAPI, '/api/value_types/',endpoint='create_value_types',resource_class_kwargs={'dao': 'ValueTypeDAO'})

# Version route
api.add_resource(ObjectController.ObjectsByMethodAPI, '/api/version',endpoint='version',resource_class_kwargs={'dao' : 'VersionDAO','get_method' : 'cairis_version'})

# Vulnerability routes
api.add_resource(ObjectController.ObjectsAPI, '/api/vulnerabilities',endpoint='vulnerabilities',resource_class_kwargs={'dao': 'VulnerabilityDAO'})
api.add_resource(ObjectController.ObjectByNameAPI, '/api/vulnerabilities/name/<path:name>',endpoint='vulnerabilitiy',resource_class_kwargs={'dao' : 'VulnerabilityDAO'})
