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
from urllib import quote

import jsonpickle
import os
from cairis.core.MisuseCaseParameters import MisuseCaseParameters
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties

from cairis.core.RiskParameters import RiskParameters
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.tools.PseudoClasses import RiskScore
from cairis.mio.ModelImport import importModelFile

class RiskAPITests(CairisDaemonTestCase):
    # region Class fields
    logger = logging.getLogger(__name__)
    existing_risk_name = 'Unauthorised Certificate Access'
    existing_environment_name = 'Stroke'
    existing_threat_name = 'Trojan Horse'
    existing_vulnerability = 'Workflow channel'
    risk_class = RiskParameters.__module__+'.'+RiskParameters.__name__
    # endregion

    def setUp(self):
        importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

    def test_get_all(self):
        method = 'test_get_all'
        rv = self.app.get('/api/risks?session_id=test')
        risks = jsonpickle.decode(rv.data)
        self.assertIsNotNone(risks, 'No results after deserialization')
        self.assertIsInstance(risks, dict, 'The result is not a dictionary as expected')
        self.assertGreater(len(risks), 0, 'No risks in the dictionary')
        self.logger.info('[%s] Risks found: %d', method, len(risks))
        risk = risks.values()[0]
        self.logger.info('[%s] First risk: %s [%d]\n', method, risk['theName'], risk['theId'])

    def test_get_by_name(self):
        method = 'test_get_by_name'
        url = '/api/risks/name/%s?session_id=test' % quote(self.existing_risk_name)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        risk = jsonpickle.decode(rv.data)
        self.assertIsNotNone(risk, 'No results after deserialization')
        self.logger.info('[%s] Risk: %s [%d]\n', method, risk['theName'], risk['theId'])

    def test_delete(self):
        method = 'test_delete'
        url = '/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name())
        new_risk_body = self.prepare_json()

        self.app.delete(url)
        self.logger.info('[%s] Object to delete: %s', method, new_risk_body)
        self.app.post('/api/risks', content_type='application/json', data=new_risk_body)
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
        url = '/api/risks'
        self.logger.info('[%s] URL: %s', method, url)
        new_risk_body = self.prepare_json()

        self.app.delete('/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name()))
        rv = self.app.post(url, content_type='application/json', data=new_risk_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('risk_id', None)
        self.assertIsNotNone(env_id, 'No risk ID returned')
        self.assertGreater(env_id, 0, 'Invalid risk ID returned [%d]' % env_id)
        self.logger.info('[%s] Risk ID: %d\n', method, env_id)

        rv = self.app.delete('/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name()))

    def test_put(self):
        method = 'test_put'
        url = '/api/risks'
        self.logger.info('[%s] URL: %s', method, url)
        new_risk_body = self.prepare_json()

        rv = self.app.delete('/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name()))
        rv = self.app.post(url, content_type='application/json', data=new_risk_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('risk_id', None)
        self.assertIsNotNone(env_id, 'No risk ID returned')
        self.assertGreater(env_id, 0, 'Invalid risk ID returned [%d]' % env_id)
        self.logger.info('[%s] Risk ID: %d', method, env_id)

        risk_to_update = self.prepare_new_risk()
        risk_to_update.theName = 'Edited test risk'
        risk_to_update.theId = env_id
        upd_env_body = self.prepare_json(risk=risk_to_update)
        rv = self.app.put('/api/risks/name/%s?session_id=test' % quote(self.prepare_new_risk().name()), data=upd_env_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully updated'), -1, 'The risk was not successfully updated')

        rv = self.app.get('/api/risks/name/%s?session_id=test' % quote(risk_to_update.theName))
        upd_risk = jsonpickle.decode(rv.data)
        self.assertIsNotNone(upd_risk, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        self.logger.info('[%s] Risk: %s [%d]\n', method, upd_risk['theName'])

        rv = self.app.delete('/api/risks/name/%s?session_id=test' % quote(risk_to_update.theName))


    def test_get_rating_by_name(self):
        method = 'test_get_rating_by_tve'
        url = '/api/risks/threat/%s/vulnerability/%s/environment/%s?session_id=test' % (
            quote(self.existing_threat_name),
            quote(self.existing_vulnerability),
            quote(self.existing_environment_name)
        )
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        rating = jsonpickle.decode(rv.data)
        self.assertIsNotNone(rating, 'No results after deserialization')
        self.logger.info('[%s] Risk rating: %s\n', method, rating['rating'])

    def test_get_scoring_by_rtve(self):
        method = 'test_get_scoring_by_rtve'
        url = '/api/risks/name/%s/threat/%s/vulnerability/%s/environment/%s?session_id=test' % (
            quote(self.existing_risk_name),
            quote(self.existing_threat_name),
            quote(self.existing_vulnerability),
            quote(self.existing_environment_name)
        )
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        scores = jsonpickle.decode(rv.data)
        self.assertIsNotNone(scores, 'No results after deserialization')
        self.assertGreater(len(scores), 0, 'No results for current criteria')
        score = scores[0]
        has_all_keys = all (k in score.keys() for k in RiskScore.required)
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
