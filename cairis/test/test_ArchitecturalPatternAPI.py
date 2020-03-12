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


import logging
import json
import jsonpickle
import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote
import jsonpickle
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.RoleParameters import RoleParameters
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.core.TemplateGoalParameters import TemplateGoalParameters
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile, importComponentViewFile

__author__ = 'Shamal Faily'


def addAPDependentData(d):
  cairis.core.BorgFactory.initialise()
  b = Borg()
  for i in d['roles']:
    b.dbProxy.addRole(RoleParameters(i["theName"], i["theType"], i["theShortCode"], i["theDescription"],[]))
  for i in d['access_rights']:
    b.dbProxy.addValueType(ValueTypeParameters(i["theName"], i["theDescription"], 'access_right','',i["theValue"],i["theRationale"]))
  for i in d['surface_types']:
    b.dbProxy.addValueType(ValueTypeParameters(i["theName"], i["theDescription"], 'surface_type','',i["theValue"],i["theRationale"]))
  for i in d['protocols']:
    b.dbProxy.addValueType(ValueTypeParameters(i["theName"], i["theDescription"], 'protocol','',i["theValue"],i["theRationale"]))
  for i in d['privileges']:
    b.dbProxy.addValueType(ValueTypeParameters(i["theName"], i["theDescription"], 'privilege','',i["theValue"],i["theRationale"]))
  spValues = [0,0,0,0,0,0,0,0]
  srValues = ['None','None','None','None','None','None','None','None']
  for i in d['template_assets']:
    b.dbProxy.addTemplateAsset(TemplateAssetParameters(i["theName"], i["theShortCode"], i["theDescription"], i["theSignificance"],i["theType"],i["theSurfaceType"],i["theAccessRight"],spValues,srValues,[],[]))
  for i in d['template_goals']:
    b.dbProxy.addTemplateGoal(TemplateGoalParameters(i["theName"],i["theDefinition"],i["theRationale"],i["theConcerns"],i["theResponsibilities"]))


class ArchitecturalPatternAPITests(CairisDaemonTestCase):

  def setUp(self):
    # region Class fields
    importModelFile(os.environ['CAIRIS_SRC'] + '/test/webinos_presituate.xml',1,'test')
    self.logger = logging.getLogger(__name__)
    # endregion

  def test_delete(self):
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml','test')
    url = '/api/architectural_patterns/name/Context%20Policy%20Management?session_id=test'
    method = 'test_delete'
    rv = self.app.delete(url)
    self.assertIsNotNone(rv.data, 'No response')
    json_resp = jsonpickle.decode(rv.data.decode('utf-8'))
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)

  def test_get(self):
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml','test')
    method = 'test_get'
    url = '/api/architectural_patterns?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    aps = jsonpickle.decode(rv.data.decode('utf-8'))
    ap = aps[0]
    self.assertIsInstance(ap, dict, 'Response is not a valid JSON object')
    self.assertEqual(ap['theName'],'Context Policy Management')

  def test_get_by_name(self):
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml','test')
    url = '/api/architectural_patterns/name/Context%20Policy%20Management?session_id=test'
    method = 'test_get_by_name'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    ap = jsonpickle.decode(rv.data.decode('utf-8'))
    self.assertIsInstance(ap, dict, 'Response is not a valid JSON object')
    self.assertEqual(ap['theName'],'Context Policy Management')

  def test_post(self):
    url = '/api/architectural_patterns?session_id=test'
    method = 'test_post'
    self.logger.info('[%s] URL: %s', method, url)
    f = open(os.environ['CAIRIS_SRC'] + '/test/componentviews.json')
    d = json.load(f)
    addAPDependentData(d)
    ap = d['architectural_patterns'][0]
    rv = self.app.post(url, content_type='application/json', data=self.prepare_json(ap))
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = jsonpickle.decode(rv.data.decode('utf-8'))
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertEqual(msg, 'Context Policy Management created')

  def test_put(self):
    url = '/api/architectural_patterns/name/Context%20Policy%20Management?session_id=test'
    method = 'test_put'
    self.logger.info('[%s] URL: %s', method, url)
    f = open(os.environ['CAIRIS_SRC'] + '/test/componentviews.json')
    d = json.load(f)
    addAPDependentData(d)
    ap = d['architectural_patterns'][0]
    rv = self.app.post('/api/architectural_patterns?session_id=test', content_type='application/json', data=self.prepare_json(ap))
    ap['theSynopsis'] = 'Revised synopsis'
    rv = self.app.put(url, content_type='application/json', data=self.prepare_json(ap))
    self.logger.debug('[%s] Response data: %s', method, rv.data)
    json_resp = jsonpickle.decode(rv.data.decode('utf-8'))
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertEqual(msg, 'Context Policy Management updated')

  def test_component_asset_model(self):
    url = '/api/architectural_patterns/component/asset/model/Policy%20Manager?session_id=test'
    method = 'test_asset_model'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    modelData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, modelData)
    self.assertIsNotNone(modelData, 'No results after deserialization')
    self.assertEqual(modelData.find('svg'),1)

  def test_component_goal_model(self):
    url = '/api/architectural_patterns/component/goal/model/Policy%20Manager?session_id=test'
    method = 'test_goal_model'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    modelData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, modelData)
    self.assertIsNotNone(modelData, 'No results after deserialization')
    self.assertEqual(modelData.find('svg'),1)

  def test_component_model(self):
    url = '/api/architectural_patterns/component/model/Context%20Policy%20Management?session_id=test'
    method = 'test_component_model'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    modelData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, modelData)
    self.assertIsNotNone(modelData, 'No results after deserialization')
    self.assertEqual(modelData.find('svg'),1)

  def test_weakness_analysis(self):
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml','test')
    url = '/api/architectural_patterns/name/Context%20Policy%20Management/environment/Complete/weakness_analysis?session_id=test'
    method = 'test_weakness_analysis'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    walm = jsonpickle.decode(rv.data.decode('utf-8'))
    self.logger.debug('[%s] Response data: %s', method, walm)
    self.assertIsNotNone(walm, 'No results after deserialization')

  def test_situate_component_view(self):
    importComponentViewFile(os.environ['CAIRIS_SRC'] + '/test/ContextPolicyManagement.xml','test')
    url = '/api/architectural_patterns/name/Context%20Policy%20Management/environment/Complete/situate?session_id=test'
    method = 'test_situate_component_view'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.post(url, content_type='application/json')
    modelData = rv.data.decode('utf-8')
    self.logger.debug('[%s] Response data: %s', method, modelData)
    json_resp = jsonpickle.decode(modelData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertEqual(msg, 'Architectural Pattern successfully situated')

  def prepare_json(self, ap):
    data_dict = {'session_id' : 'test','object' : ap}
    new_ap_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_ap_body)
    return new_ap_body
