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
import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote
import jsonpickle
from cairis.core.Threat import Threat
from cairis.tools.JsonConverter import json_deserialize
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.ValueType import ValueType
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.PseudoClasses import SecurityAttribute
import os
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'



class ThreatAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)
    self.existing_threat_name = 'Replay attack'
    self.existing_threat_type = 'Electronic/Hacking'
    self.existing_environment_name_1 = 'Stroke'
    self.existing_environment_name_2 = 'Psychosis'
    self.existing_asset_names = ['Clinical data', 'Data node']
    self.existing_attackers_names = ['Trudy', 'Yves']
    self.threat_class = Threat.__module__+'.'+Threat.__name__
    # endregion
    
  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/threats?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    threats = jsonpickle.decode(responseData)
    self.assertIsNotNone(threats, 'No results after deserialization')
    self.assertIsInstance(threats, list, 'The result is not a list as expected')
    self.assertGreater(len(threats), 0, 'No threats in the dictionary')
    self.logger.info('[%s] Threats found: %d', method, len(threats))
    threat = threats[0]
    self.logger.info('[%s] First threat: %s\n', method, threat['theName'])

  def test_get_all_summary(self):
    method = 'test_get_all_summary'
    rv = self.app.get('/api/threats/summary?session_id=test')
    if (sys.version_info > (3,)):
      thrs = json_deserialize(rv.data.decode('utf-8'))
    else:
      thrs = json_deserialize(rv.data)
    self.assertIsNotNone(thrs, 'No results after deserialization')
    self.assertGreater(len(thrs), 0, 'No threat summaries')
    self.assertIsInstance(thrs[0], dict)
    self.logger.info('[%s] Threats found: %d', method, len(thrs))
    self.logger.info('[%s] First threat summary: %s [%s]\n', method, thrs[0]['theName'])

  def test_get_threat_model(self):
    method = 'test_get_threat_model'
    rv = self.app.get('/api/threats/model/environment/Psychosis?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    tm = jsonpickle.decode(responseData)
    self.assertEqual(len(tm['theEntities']),1)
    self.assertEqual(len(tm['theDatastores']),1)
    self.assertEqual(len(tm['theProcesses']),0)
    self.assertEqual(len(tm['theDataflows']),0)

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/threats/name/%s?session_id=test' % quote(self.existing_threat_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    threat = jsonpickle.decode(responseData)
    self.assertIsNotNone(threat, 'No results after deserialization')
    self.logger.info('[%s] Threat: %s\n', method, threat['theName'])

  def test_delete(self):
    method = 'test_delete'
    url = '/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theName)
    new_threat_body = self.prepare_json()

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_threat_body)
    self.app.post('/api/threats', content_type='application/json', data=new_threat_body)
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.info('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No response')
    json_resp = jsonpickle.decode(responseData)
    self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s\n', method, message)

  def test_post(self):
    method = 'test_post'
    url = '/api/threats'
    self.logger.info('[%s] URL: %s', method, url)
    new_threat_body = self.prepare_json()

    self.app.delete('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theName))
    rv = self.app.post(url, content_type='application/json', data=new_threat_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertIsNotNone(msg, 'No message returned')
    self.logger.info('[%s] Message: %s\n', method, msg)
    rv = self.app.delete('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theName))

  def test_put(self):
    method = 'test_put'
    url = '/api/threats'
    self.logger.info('[%s] URL: %s', method, url)
    new_threat_body = self.prepare_json()

    rv = self.app.delete('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theName))
    rv = self.app.post(url, content_type='application/json', data=new_threat_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertIsNotNone(msg, 'No message returned')
    self.logger.info('[%s] Message: %s', method, msg)

    threat_to_update = self.prepare_new_threat()
    threat_to_update.theName = 'Edited test threat'
    upd_env_body = self.prepare_json(threat=threat_to_update)
    rv = self.app.put('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theName), data=upd_env_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertGreater(message.find('updated'), -1, 'The threat was not successfully updated')

    rv = self.app.get('/api/threats/name/%s?session_id=test' % quote(threat_to_update.theName))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_threat = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_threat, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Threat: %s\n', method, upd_threat['theName'])

    rv = self.app.delete('/api/threats/name/%s?session_id=test' % quote(threat_to_update.theName))

  def prepare_new_threat(self):
    new_security_attrs = [
      SecurityAttribute(
        name='Confidentiality',
        value='High',
        rationale='As a test'
      ),
      SecurityAttribute(
        name='Availability',
        value='Medium',
        rationale='Another test'
      )
    ]

    more_security_attrs = [SecurityAttribute(name='Confidentiality',value='High',rationale='Test')]


    new_threat_props = [
      ThreatEnvironmentProperties(
        environmentName=self.existing_environment_name_1,
        lhood='Incredible',
        assets=self.existing_asset_names,
        attackers=self.existing_attackers_names,
        syProperties=new_security_attrs,
        pRationale=[]
      ),
      ThreatEnvironmentProperties(
        environmentName=self.existing_environment_name_2,
        lhood='Improbable',
        assets=self.existing_asset_names,
        attackers=self.existing_attackers_names,
        syProperties=more_security_attrs,
        pRationale=[]
      )
    ]

    new_threat = Threat(
      threatId=-1,
      threatName='Test threat',
      threatType=self.existing_threat_type,
      threatMethod='',
      tags=[],
      cProps=[]
    )
    new_threat.theEnvironmentProperties = new_threat_props

    new_threat.theEnvironmentDictionary = {}
    new_threat.likelihoodLookup = {}
    new_threat.theThreatPropertyDictionary = {}

    delattr(new_threat, 'theEnvironmentDictionary')
    delattr(new_threat, 'likelihoodLookup')
    delattr(new_threat, 'theThreatPropertyDictionary')

    return new_threat

  def prepare_new_threat_type(self):
    new_type = ValueType(
      valueTypeId=-1,
      valueTypeName='Test threat type',
      valueTypeDescription='This is a test threat type',
      vType='threat-type',
      vEnv='all'
    )
    new_type.theEnvironmentName = 'all'
    return new_type

  def prepare_dict(self, threat=None):
    if threat is None:
      threat = self.prepare_new_threat()
    else:
      assert isinstance(threat, Threat)

    return {
      'session_id': 'test',
      'object': threat,
    }

  def prepare_json(self, data_dict=None, threat=None):
    if data_dict is None:
      data_dict = self.prepare_dict(threat=threat)
    else:
      assert isinstance(data_dict, dict)
    new_threat_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_threat_body)
    return new_threat_body
