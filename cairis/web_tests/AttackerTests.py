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
from cairis.core.Attacker import Attacker
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.web_tests.CairisTests import CairisTests

__author__ = 'Robin Quetin'


class AttackerTests(CairisTests):
    # region Class fields
    logger = logging.getLogger(__name__)
    existing_attacker_id = 150
    existing_attacker_name = 'Mallory'
    existing_environment_name_1 = 'Stroke'
    existing_environment_name_2 = 'Psychosis'
    existing_motive_names = ['Hactivism', 'Money']
    existing_role_names = ['Hacker', 'Developer']
    existing_capabilities = [
        {
            'name':'Resources/Equipment',
            'value': 'Low'
        },
        {
            'name': 'Knowledge/Methods',
            'value': 'High'
        }
    ]
    attacker_class = Attacker.__module__+'.'+Attacker.__name__
    # endregion

    def test_get_all(self):
        method = 'test_get_all'
        rv = self.app.get('/api/attackers?session_id=test')
        attackers = jsonpickle.decode(rv.data)
        self.assertIsNotNone(attackers, 'No results after deserialization')
        self.assertIsInstance(attackers, dict, 'The result is not a dictionary as expected')
        self.assertGreater(len(attackers), 0, 'No attackers in the dictionary')
        self.logger.info('[%s] Attackers found: %d', method, len(attackers))
        attacker = attackers.values()[0]
        self.logger.info('[%s] First attacker: %s [%d]\n', method, attacker['theName'], attacker['theId'])

    def test_get_by_name(self):
        method = 'test_get_by_name'
        url = '/api/attackers/name/%s?session_id=test' % quote(self.existing_attacker_name)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        attacker = jsonpickle.decode(rv.data)
        self.assertIsNotNone(attacker, 'No results after deserialization')
        self.logger.info('[%s] Attacker: %s [%d]\n', method, attacker['theName'], attacker['theId'])

    def test_delete(self):
        method = 'test_delete'
        url = '/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName)
        new_attacker_body = self.prepare_json()

        self.app.delete(url)
        self.logger.info('[%s] Object to delete: %s', method, new_attacker_body)
        self.app.post('/api/attackers', content_type='application/json', data=new_attacker_body)
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
        url = '/api/attackers'
        self.logger.info('[%s] URL: %s', method, url)
        new_attacker_body = self.prepare_json()

        self.app.delete('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName))
        rv = self.app.post(url, content_type='application/json', data=new_attacker_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('attacker_id', None)
        self.assertIsNotNone(env_id, 'No attacker ID returned')
        self.assertGreater(env_id, 0, 'Invalid attacker ID returned [%d]' % env_id)
        self.logger.info('[%s] Attacker ID: %d\n', method, env_id)

        rv = self.app.delete('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName))

    def test_put(self):
        method = 'test_put'
        url = '/api/attackers'
        self.logger.info('[%s] URL: %s', method, url)
        new_attacker_body = self.prepare_json()

        rv = self.app.delete('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName))
        rv = self.app.post(url, content_type='application/json', data=new_attacker_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        env_id = json_resp.get('attacker_id', None)
        self.assertIsNotNone(env_id, 'No attacker ID returned')
        self.assertGreater(env_id, 0, 'Invalid attacker ID returned [%d]' % env_id)
        self.logger.info('[%s] Attacker ID: %d', method, env_id)

        attacker_to_update = self.prepare_new_attacker()
        attacker_to_update.theName = 'Edited test attacker'
        attacker_to_update.theId = env_id
        upd_env_body = self.prepare_json(attacker=attacker_to_update)
        rv = self.app.put('/api/attackers/name/%s?session_id=test' % quote(self.prepare_new_attacker().theName), data=upd_env_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp)
        self.assertIsInstance(json_resp, dict)
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully updated'), -1, 'The attacker was not successfully updated')

        rv = self.app.get('/api/attackers/name/%s?session_id=test' % quote(attacker_to_update.theName))
        upd_attacker = jsonpickle.decode(rv.data)
        self.assertIsNotNone(upd_attacker, 'Unable to decode JSON data')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        self.logger.info('[%s] Attacker: %s [%d]\n', method, upd_attacker['theName'], upd_attacker['theId'])

        rv = self.app.delete('/api/attackers/name/%s?session_id=test' % quote(attacker_to_update.theName))

    def prepare_new_attacker(self):
        new_attacker_props = [
            AttackerEnvironmentProperties(
                environmentName=self.existing_environment_name_1,
                roles=self.existing_role_names,
                motives=self.existing_motive_names,
                capabilities=self.existing_capabilities
            ),
            AttackerEnvironmentProperties(
                environmentName=self.existing_environment_name_2,
                roles=self.existing_role_names,
                motives=self.existing_motive_names,
                capabilities=self.existing_capabilities
            )
        ]

        new_attacker = Attacker(
            attackerId=-1,
            attackerName='Test attacker',
            attackerDescription='This is a test attacker',
            attackerImage='',
            tags=['test', 'test123'],
            environmentProperties=[]
        )
        new_attacker.theEnvironmentProperties = new_attacker_props

        new_attacker.theEnvironmentDictionary = {}
        new_attacker.theAttackerPropertyDictionary = {}

        delattr(new_attacker, 'theEnvironmentDictionary')
        delattr(new_attacker, 'theAttackerPropertyDictionary')

        return new_attacker

    def prepare_dict(self, attacker=None):
        if attacker is None:
            attacker = self.prepare_new_attacker()
        else:
            assert isinstance(attacker, Attacker)

        return {
            'session_id': 'test',
            'object': attacker,
        }

    def prepare_json(self, data_dict=None, attacker=None):
        if data_dict is None:
            data_dict = self.prepare_dict(attacker=attacker)
        else:
            assert isinstance(data_dict, dict)
        new_attacker_body = jsonpickle.encode(data_dict, unpicklable=False)
        self.logger.info('JSON data: %s', new_attacker_body)
        return new_attacker_body
