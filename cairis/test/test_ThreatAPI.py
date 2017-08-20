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
        threats = jsonpickle.decode(rv.data)
        self.assertIsNotNone(threats, 'No results after deserialization')
        self.assertIsInstance(threats, dict, 'The result is not a dictionary as expected')
        self.assertGreater(len(threats), 0, 'No threats in the dictionary')
        self.logger.info('[%s] Threats found: %d', method, len(threats))
        threat = list(threats.values())[0]
        self.logger.info('[%s] First threat: %s [%d]\n', method, threat['theThreatName'], threat['theId'])

    def test_get_by_name(self):
        method = 'test_get_by_name'
        url = '/api/threats/name/%s?session_id=test' % quote(self.existing_threat_name)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        threat = jsonpickle.decode(rv.data)
        self.assertIsNotNone(threat, 'No results after deserialization')
        self.logger.info('[%s] Threat: %s [%d]\n', method, threat['theThreatName'], threat['theId'])

    def test_delete(self):
        method = 'test_delete'
        url = '/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theThreatName)
        new_threat_body = self.prepare_json()

        self.app.delete(url)
        self.logger.info('[%s] Object to delete: %s', method, new_threat_body)
        self.app.post('/api/threats', content_type='application/json', data=new_threat_body)
        self.logger.info('[%s] URL: %s', method, url)
        rv = self.app.delete(url)
        self.logger.info('[%s] Response data: %s', method, rv.data)
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s\n', method, message)

    def test_post(self):
        method = 'test_post'
        url = '/api/threats'
        self.logger.info('[%s] URL: %s', method, url)
        new_threat_body = self.prepare_json()

        self.app.delete('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theThreatName))
        rv = self.app.post(url, content_type='application/json', data=new_threat_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('threat_id', None)
        self.assertIsNotNone(env_id, 'No threat ID returned')
        self.assertGreater(env_id, 0, 'Invalid threat ID returned [%d]' % env_id)
        self.logger.info('[%s] Threat ID: %d\n', method, env_id)

        rv = self.app.delete('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theThreatName))

    def test_put(self):
        method = 'test_put'
        url = '/api/threats'
        self.logger.info('[%s] URL: %s', method, url)
        new_threat_body = self.prepare_json()

        rv = self.app.delete('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theThreatName))
        rv = self.app.post(url, content_type='application/json', data=new_threat_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('threat_id', None)
        self.assertIsNotNone(env_id, 'No threat ID returned')
        self.assertGreater(env_id, 0, 'Invalid threat ID returned [%d]' % env_id)
        self.logger.info('[%s] Threat ID: %d', method, env_id)

        threat_to_update = self.prepare_new_threat()
        threat_to_update.theThreatName = 'Edited test threat'
        threat_to_update.theId = env_id
        upd_env_body = self.prepare_json(threat=threat_to_update)
        rv = self.app.put('/api/threats/name/%s?session_id=test' % quote(self.prepare_new_threat().theThreatName), data=upd_env_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully updated'), -1, 'The threat was not successfully updated')

        rv = self.app.get('/api/threats/name/%s?session_id=test' % quote(threat_to_update.theThreatName))
        upd_threat = jsonpickle.decode(rv.data)
        self.assertIsNotNone(upd_threat, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        self.logger.info('[%s] Threat: %s [%d]\n', method, upd_threat['theThreatName'], upd_threat['theId'])

        rv = self.app.delete('/api/threats/name/%s?session_id=test' % quote(threat_to_update.theThreatName))

    def test_types_get(self):
        method = 'test_types_get'
        rv = self.app.get('/api/threats/types?session_id=test')
        threats = jsonpickle.decode(rv.data)
        self.assertIsNotNone(threats, 'No results after deserialization')
        self.assertIsInstance(threats, list, 'The result is not a dictionary as expected')
        self.assertGreater(len(threats), 0, 'No threats in the dictionary')
        self.logger.info('[%s] Threat types found: %d', method, len(threats))
        threat_type = threats[0]
        self.logger.info('[%s] First threat type: %s [%d]\n', method, threat_type['theName'], threat_type['theId'])

    def test_types_delete(self):
        method = 'test_types_delete'
        url = '/api/threats/types/name/%s?session_id=test' % quote(self.prepare_new_threat_type().theName)
        new_threat_type_body = jsonpickle.encode(self.prepare_new_threat_type(), unpicklable=False)

        self.app.delete(url)
        self.logger.info('[%s] Object to delete: %s', method, new_threat_type_body)
        self.app.post('/api/threats/types', content_type='application/json', data=new_threat_type_body)
        self.logger.info('[%s] URL: %s', method, url)
        rv = self.app.delete(url)
        self.logger.info('[%s] Response data: %s', method, rv.data)
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_resp, dict, 'The response cannot be converted to a dictionary')
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s\n', method, message)

    def test_types_post(self):
        method = 'test_types_post'
        url = '/api/threats/types'
        self.logger.info('[%s] URL: %s', method, url)
        json_dict = {'session_id': 'test', 'object': self.prepare_new_threat_type()}
        new_threat_type_body = jsonpickle.encode(json_dict, unpicklable=False)
        self.logger.info('JSON data: %s', new_threat_type_body)

        self.app.delete('/api/threats/types/name/%s?session_id=test' % quote(self.prepare_new_threat_type().theName))
        rv = self.app.post(url, content_type='application/json', data=new_threat_type_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        ackMsg = json_resp.get('message', None)
        self.assertEqual(ackMsg, 'Threat type successfully added')

        rv = self.app.delete('/api/threats/types/name/%s?session_id=test' % quote(self.prepare_new_threat_type().theName))

    def test_types_put(self):
        method = 'test_types_put'
        url = '/api/threats/types'
        self.logger.info('[%s] URL: %s', method, url)
        json_dict = {'session_id': 'test', 'object': self.prepare_new_threat_type()}
        new_threat_type_body = jsonpickle.encode(json_dict)
        self.logger.info('JSON data: %s', new_threat_type_body)

        rv = self.app.delete('/api/threats/types/name/%s?session_id=test' % quote(self.prepare_new_threat_type().theName))
        rv = self.app.post(url, content_type='application/json', data=new_threat_type_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        ackMsg = json_resp.get('message', None)
        self.assertEqual(ackMsg, 'Threat type successfully added')

        type_to_update = self.prepare_new_threat_type()
        type_to_update.theName = 'Edited test threat type'
        json_dict = {'session_id': 'test', 'object': type_to_update}
        upd_type_body = jsonpickle.encode(json_dict)
        rv = self.app.put('/api/threats/types/name/%s?session_id=test' % quote(self.prepare_new_threat_type().theName), data=upd_type_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully updated'), -1, 'The threat was not successfully updated')

        rv = self.app.get('/api/threats/types/name/%s?session_id=test' % quote(type_to_update.theName))
        upd_threat_type = jsonpickle.decode(rv.data)
        self.assertIsNotNone(upd_threat_type, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        self.logger.info('[%s] Threat type: %s [%d]\n', method, upd_threat_type['theName'], upd_threat_type['theId'])

        rv = self.app.delete('/api/threats/types/name/%s?session_id=test' % quote(type_to_update.theName))

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
                syProperties=new_security_attrs,
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
            vType='threat-type'
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
