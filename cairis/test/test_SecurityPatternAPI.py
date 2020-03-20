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
from io import StringIO
import jsonpickle
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile, importSecurityPatternsFile

__author__ = 'Shamal Faily'

def addSPDependentData(d):
  cairis.core.BorgFactory.initialise()
  b = Borg()
  for i in d['access_rights']:
    b.dbProxy.addValueType(ValueTypeParameters(i["theName"], i["theDescription"], 'access_right','',i["theValue"],i["theRationale"]))
  for i in d['surface_types']:
    b.dbProxy.addValueType(ValueTypeParameters(i["theName"], i["theDescription"], 'surface_type','',i["theValue"],i["theRationale"]))
  spValues = [0,0,0,0,0,0,0,0]
  srValues = ['None','None','None','None','None','None','None','None']
  for i in d['template_assets']:
    b.dbProxy.addTemplateAsset(TemplateAssetParameters(i["theName"], i["theShortCode"], i["theDescription"], i["theSignificance"],i["theType"],i["theSurfaceType"],i["theAccessRight"],spValues,srValues,[],[]))

class SecurityPatternAPITests(CairisDaemonTestCase):

  def setUp(self):
    # region Class fields
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')
    self.logger = logging.getLogger(__name__)
    # endregion

  def test_delete(self):
    importSecurityPatternsFile(os.environ['CAIRIS_SRC'] + '/../examples/architecture/schumacher_patterns.xml','test')
    url = '/api/security_patterns/name/Packet%20Filter%20Firewall?session_id=test'
    method = 'test_delete'
    rv = self.app.delete(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)

  def test_get(self):
    importSecurityPatternsFile(os.environ['CAIRIS_SRC'] + '/../examples/architecture/schumacher_patterns.xml','test')
    method = 'test_get'
    url = '/api/security_patterns?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    sps = jsonpickle.decode(responseData)
    sp = sps[0]
    self.assertIsInstance(sp, dict, 'Response is not a valid JSON object')
    self.assertEqual(len(sps),5)

  def test_get_by_name(self):
    importSecurityPatternsFile(os.environ['CAIRIS_SRC'] + '/../examples/architecture/schumacher_patterns.xml','test')
    url = '/api/security_patterns/name/Packet%20Filter%20Firewall?session_id=test'
    method = 'test_get_by_name'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    ap = jsonpickle.decode(responseData)
    self.assertIsInstance(ap, dict, 'Response is not a valid JSON object')
    self.assertEqual(ap['theName'],'Packet Filter Firewall')

  def test_post(self):
    url = '/api/security_patterns?session_id=test'
    method = 'test_post'
    self.logger.info('[%s] URL: %s', method, url)
    f = open(os.environ['CAIRIS_SRC'] + '/test/securitypattern.json')
    d = json.load(f)
    addSPDependentData(d)
    sp = d['security_patterns'][0]
    rv = self.app.post(url, content_type='application/json', data=self.prepare_json(sp))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertEqual(msg, 'TestPattern created')

  def test_put(self):
    url = '/api/security_patterns/name/TestPattern?session_id=test'
    method = 'test_put'
    self.logger.info('[%s] URL: %s', method, url)
    f = open(os.environ['CAIRIS_SRC'] + '/test/securitypattern.json')
    d = json.load(f)
    addSPDependentData(d)
    sp = d['security_patterns'][0]
    rv = self.app.post('/api/security_patterns?session_id=test', content_type='application/json', data=self.prepare_json(sp))
    sp['theProblem'] = 'Revised problem'
    rv = self.app.put(url, content_type='application/json', data=self.prepare_json(sp))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertEqual(msg, 'TestPattern updated')

  def test_situate_security_pattern(self):
    importSecurityPatternsFile(os.environ['CAIRIS_SRC'] + '/../examples/architecture/schumacher_patterns.xml','test')
    url = '/api/security_patterns/name/Demilitarized%20Zone/environment/Psychosis/situate?session_id=test'
    method = 'test_situate_security_pattern'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.post(url, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertEqual(msg, 'Security Pattern successfully situated')

  def prepare_json(self, sp):
    data_dict = {'session_id' : 'test','object' : sp}
    new_sp_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_sp_body)
    return new_sp_body
