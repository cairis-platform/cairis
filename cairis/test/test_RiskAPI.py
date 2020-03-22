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
import os
from cairis.tools.JsonConverter import json_deserialize
from cairis.core.MisuseCaseParameters import MisuseCaseParameters
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.RiskParameters import RiskParameters
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.PseudoClasses import RiskScore
from cairis.mio.ModelImport import importModelFile

__author__ = 'Robin Quetin, Shamal Faily'


class RiskAPITests(CairisDaemonTestCase):

    @classmethod
    def setUpClass(cls):
        importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


    def setUp(self):
        # region Class fields
        self.logger = logging.getLogger(__name__)
        self.existing_risk_name = 'Replay-based resource exploit'
        self.existing_environment_name = 'Core Technology'
        self.existing_threat_name = 'Replay attack'
        self.existing_vulnerability = 'Replay vulnerability'
        self.risk_class = RiskParameters.__module__+'.'+RiskParameters.__name__
        # endregion

    def test_get_all(self):
        method = 'test_get_all'
        rv = self.app.get('/api/risks?session_id=test')
        if (sys.version_info > (3,)):
          responseData = rv.data.decode('utf-8')
        else:
          responseData = rv.data
        risks = jsonpickle.decode(responseData)
        self.assertIsNotNone(risks, 'No results after deserialization')
        self.assertIsInstance(risks, list, 'The result is not a list as expected')
        self.assertGreater(len(risks), 0, 'No risks in the dictionary')
        self.logger.info('[%s] Risks found: %d', method, len(risks))
        risk = risks[0]
        self.logger.info('[%s] First risk: %s\n', method, risk['theName'])

    def test_get_all_summary(self):
        method = 'test_get_all_summary'
        rv = self.app.get('/api/risks/summary?session_id=test')
        if (sys.version_info > (3,)):
          risks = json_deserialize(rv.data.decode('utf-8'))
        else:
          risks = json_deserialize(rv.data)
        self.assertIsNotNone(risks, 'No results after deserialization')
        self.assertGreater(len(risks), 0, 'No risk summaries')
        self.assertIsInstance(risks[0], dict)
        self.logger.info('[%s] Risks found: %d', method, len(risks))
        self.logger.info('[%s] First risk summary: %s [%d]\n', method, risks[0]['theName'])


    def test_get_risk_model_elements(self):
        method = 'test_get_risk_model_elements'
        rv = self.app.get('/api/risks/model/environment/Psychosis/names?session_id=test')
        if (sys.version_info > (3,)):
          responseData = rv.data.decode('utf-8')
        else:
          responseData = rv.data
        elements = jsonpickle.decode(responseData)
        self.assertEqual(len(elements),66)

    def test_get_by_name(self):
        method = 'test_get_by_name'
        url = '/api/risks/name/%s?session_id=test' % quote(self.existing_risk_name)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        if (sys.version_info > (3,)):
          responseData = rv.data.decode('utf-8')
        else:
          responseData = rv.data
        self.logger.debug('[%s] Response data: %s', method, responseData)
        risk = jsonpickle.decode(responseData)
        self.assertIsNotNone(risk, 'No results after deserialization')
        self.logger.info('[%s] Risk: %s\n', method, risk['theName'])

    def test_delete(self):
        method = 'test_delete'
        url = '/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name())
        new_risk_body = self.prepare_json()

        self.app.delete(url)
        self.logger.info('[%s] Object to delete: %s', method, new_risk_body)
        self.app.post('/api/risks', content_type='application/json', data=new_risk_body)
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
        url = '/api/risks'
        self.logger.info('[%s] URL: %s', method, url)
        new_risk_body = self.prepare_json()

        rv = self.app.post(url, content_type='application/json', data=new_risk_body)
        if (sys.version_info > (3,)):
          responseData = rv.data.decode('utf-8')
        else:
          responseData = rv.data
        self.logger.debug('[%s] Response data: %s', method, responseData)
        json_resp = jsonpickle.decode(responseData)
        self.assertIsNotNone(json_resp, 'No results after deserialization')

        rv = self.app.delete('/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name()))

    def test_put(self):
        method = 'test_put'
        url = '/api/risks'
        self.logger.info('[%s] URL: %s', method, url)
        new_risk_body = self.prepare_json()

        rv = self.app.post(url, content_type='application/json', data=new_risk_body)
        if (sys.version_info > (3,)):
          responseData = rv.data.decode('utf-8')
        else:
          responseData = rv.data
        self.logger.debug('[%s] Response data: %s', method, responseData)
        json_resp = jsonpickle.decode(responseData)
        self.assertIsNotNone(json_resp, 'No results after deserialization')

        risk_to_update = self.prepare_new_risk()
        risk_to_update.theName = 'Edited test risk'
        upd_env_body = self.prepare_json(risk=risk_to_update)
        rv = self.app.put('/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name()), data=upd_env_body, content_type='application/json')
        if (sys.version_info > (3,)):
          responseData = rv.data.decode('utf-8')
        else:
          responseData = rv.data
        self.assertIsNotNone(responseData, 'No response')
        json_resp = jsonpickle.decode(responseData)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('updated'), -1, 'The risk was not successfully updated')

        rv = self.app.get('/api/risks/name/%s?session_id=test' % quote(risk_to_update.theName))
        if (sys.version_info > (3,)):
          responseData = rv.data.decode('utf-8')
        else:
          responseData = rv.data
        upd_risk = jsonpickle.decode(responseData)
        self.assertIsNotNone(upd_risk, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, responseData)
        self.logger.info('[%s] Risk: %s \n', method, upd_risk['theName'])

        rv = self.app.delete('/api/risks/name/%s?session_id=test' % quote(risk_to_update.theName))


    def test_get_rating_by_name(self):
        method = 'test_get_rating'
        url = '/api/risks/threat/%s/vulnerability/%s/environment/%s?session_id=test' % (
            quote(self.existing_threat_name),
            quote(self.existing_vulnerability),
            quote(self.existing_environment_name)
        )
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        responseData = rv.data.decode('utf-8')
        self.logger.debug('[%s] Response data: %s', method, responseData)
        rating = jsonpickle.decode(responseData)
        self.assertIsNotNone(rating, 'No results after deserialization')
        self.logger.info('[%s] Risk rating: %s\n', method, rating['rating'])

        url = '/api/risks/vulnerability/%s/threat/%s/environment/%s?session_id=test' % (
            quote(self.existing_vulnerability),
            quote(self.existing_threat_name),
            quote(self.existing_environment_name)
        )
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        responseData = rv.data.decode('utf-8')
        self.logger.debug('[%s] Response data: %s', method, responseData)
        rating = jsonpickle.decode(responseData)
        self.assertIsNotNone(rating, 'No results after deserialization')
        self.logger.info('[%s] Risk rating: %s\n', method, rating['rating'])



    def test_get_scoring(self):
        method = 'test_get_scoring'
        url = '/api/risks/name/%s/threat/%s/vulnerability/%s/environment/%s?session_id=test' % (
            quote(self.existing_risk_name),
            quote(self.existing_threat_name),
            quote(self.existing_vulnerability),
            quote(self.existing_environment_name)
        )
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        responseData = rv.data.decode('utf-8')
        self.logger.debug('[%s] Response data: %s', method, responseData)
        scores = jsonpickle.decode(responseData)
        self.assertIsNotNone(scores, 'No results after deserialization')
        self.assertGreater(len(scores), 0, 'No results for current criteria')
        score = scores[0]
        has_all_keys = all (k in list(score.keys()) for k in RiskScore.required)
        self.assertTrue(has_all_keys, 'Response is not a RiskScore object')
        self.logger.info('[%s] %s - %d - %d\n', method, score['responseName'], score['unmitScore'], score['mitScore'])

        url = '/api/risks/name/%s/vulnerability/%s/threat/%s/environment/%s?session_id=test' % (
            quote(self.existing_risk_name),
            quote(self.existing_vulnerability),
            quote(self.existing_threat_name),
            quote(self.existing_environment_name)
        )
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        responseData = rv.data.decode('utf-8')
        self.logger.debug('[%s] Response data: %s', method, responseData)
        scores = jsonpickle.decode(responseData)
        self.assertIsNotNone(scores, 'No results after deserialization')
        self.assertGreater(len(scores), 0, 'No results for current criteria')
        score = scores[0]
        has_all_keys = all (k in list(score.keys()) for k in RiskScore.required)
        self.assertTrue(has_all_keys, 'Response is not a RiskScore object')
        self.logger.info('[%s] %s - %d - %d\n', method, score['responseName'], score['unmitScore'], score['mitScore'])



    def prepare_new_risk(self):
        new_misuse_case = MisuseCaseParameters(
            scName='Test misuse case',
            cProps=[
                MisuseCaseEnvironmentProperties(self.existing_environment_name, '')
            ],
            risk='Test risk'
        )

        new_misuse_case.theEnvironmentDictionary = {}
        delattr(new_misuse_case, 'theEnvironmentDictionary')

        new_risk = RiskParameters(
            riskName='Test risk',
            threatName=self.existing_threat_name,
            vulName=self.existing_vulnerability,
            mc=new_misuse_case,
            rTags=[]
        )

        return new_risk

    def prepare_dict(self, risk=None):
        if risk is None:
            risk = self.prepare_new_risk()
        else:
            assert isinstance(risk, RiskParameters)

        return {
            'session_id': 'test',
            'object': risk,
        }

    def prepare_json(self, data_dict=None, risk=None):
        if data_dict is None:
            data_dict = self.prepare_dict(risk=risk)
        else:
            assert isinstance(data_dict, dict)
        new_risk_body = jsonpickle.encode(data_dict, unpicklable=False)
        self.logger.info('JSON data: %s', new_risk_body)
        return new_risk_body
