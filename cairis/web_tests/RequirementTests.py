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
from cairis.core.Requirement import Requirement
from cairis.web_tests.CairisTests import CairisTests

__author__ = 'Robin Quetin'


class RequirementTests(CairisTests):
    # region Class fields
    logger = logging.getLogger(__name__)
    existing_requirement_id = 490
    existing_requirement_name = 'Dataset policy'
    existing_asset_name = 'Analysis data'
    existing_environment_name = 'Core Technology'
    requirement_class = Requirement.__module__+'.'+Requirement.__name__
    new_requirement = Requirement(
        id=-1,
        label='TE-1',
        name='Test requirement',
        description='This is a test description',
        priority='1',
        rationale='This is to test the requirements controller',
        fitCriterion='None',
        originator='Student',
        type='Functional',
        asset='Analysis data'
    )
    new_requirement_dict = {
        'session_id': 'test',
        'object': new_requirement,
    }
    new_requirement_body = jsonpickle.encode(new_requirement_dict)
    to_delete_ids = []
    # endregion
    logger.info('JSON data: %s', new_requirement_body)

    def test_get_all(self):
        method = 'test_get_all'
        rv = self.app.get('/api/requirements?session_id=test')
        requirements_dict = jsonpickle.decode(rv.data)
        self.assertIsNotNone(requirements_dict, 'No results after deserialization')
        self.assertIsInstance(requirements_dict, dict, 'The result is not a dictionary as expected')
        assert isinstance(requirements_dict, dict)
        self.assertGreater(len(requirements_dict), 0, 'No requirements in the dictionary')
        requirements = requirements_dict.values()
        self.logger.info('[%s] Requirements found: %d', method, len(requirements))
        self.logger.info('[%s] First requirement: %s [%d]\n', method, requirements[0]['theName'], requirements[0]['theId'])

    def test_post(self):
        method = 'test_post'
        url = '/api/requirements?asset=%s' % quote(self.existing_asset_name)
        self.logger.info('[%s] URL: %s', method, url)
        rv = self.app.post(url, content_type='application/json', data=self.new_requirement_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        req_id = json_resp.get('requirement_id', None)
        self.assertIsNotNone(req_id, 'No requirement ID returned')
        self.logger.info('[%s] Requirement ID: %d', method, req_id)

        rv = self.app.get('/api/requirements/id/%d?session_id=test' % req_id)
        requirement = jsonpickle.decode(rv.data)
        self.logger.info('[%s] Requirement: %s [%d]\n', method, requirement['theName'], requirement['theId'])

    def test_get_id(self):
        method = 'test_get_id'
        url = '/api/requirements/id/%d?session_id=test' % self.existing_requirement_id
        self.logger.info('[%s] URL: %s', method, url)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        requirement = jsonpickle.decode(rv.data)
        self.assertIsNotNone(requirement, 'No results after deserialization')
        self.logger.info('[%s] Requirement: %s [%d]\n', method, requirement['theName'], requirement['theId'])

    def test_get_asset_name(self):
        method = 'test_asset_get_name'
        url = '/api/requirements/asset/%s?session_id=test' % quote(self.existing_asset_name)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        requirements = jsonpickle.decode(rv.data)
        self.assertIsNotNone(requirements, 'No results after deserialization')
        self.assertGreater(len(requirements), 0, 'No requirements found for this environment')
        self.logger.info('[%s] Requirement: %s [%d]\n', method, requirements[0]['theName'], requirements[0]['theId'])

    def test_get_environment_name(self):
        method = 'test_environment_get_name'
        url = '/api/requirements/environment/%s?session_id=test' % quote(self.existing_asset_name)
        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        requirements = jsonpickle.decode(rv.data)
        self.assertIsNotNone(requirements, 'No results after deserialization')
        if len(requirements) > 0:
            self.logger.info('[%s] Requirement: %s [%d]\n', method, requirements[0]['theName'], requirements[0]['theId'])

    def test_x_put(self):
        method = 'test_x_put'
        url = '/api/requirements'
        rv = self.app.get('/api/requirements?session_id=test')
        reqs = jsonpickle.decode(rv.data)
        requirement = reqs.get(self.new_requirement.theDescription)

        upd_requirement = self.new_requirement
        upd_requirement.theName = 'Test2'
        upd_requirement.theId = requirement['theId']
        upd_requirement_dict = self.new_requirement_dict
        upd_requirement_dict['object'] = upd_requirement
        upd_requirement_body = jsonpickle.encode(upd_requirement_dict)
        self.logger.info('[%s] JSON data: %s', method, upd_requirement_body)

        rv = self.app.put(url, content_type='application/json', data=upd_requirement_body)
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_resp = jsonpickle.decode(rv.data)
        self.assertIsNotNone(json_resp, 'No results after deserialization')
        message = json_resp.get('message', None)
        self.assertIsNotNone(message, 'No message returned')
        self.logger.info('Message: %s', message)

        rv = self.app.get('/api/requirements?session_id=test')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        requirements = jsonpickle.decode(rv.data)
        requirement = requirements.get(upd_requirement.theDescription, None)
        self.assertIsNotNone(requirement, 'Requirement not updated as expected')
        self.logger.info('[%s] Requirement: %s [%d]\n', method, requirement['theName'], requirement['theId'])

    def test_z_delete_id(self):
        method = 'test_delete_id'
        rv = self.app.get('/api/requirements?session_id=test')
        requirements_dict = jsonpickle.decode(rv.data)
        to_delete_reqs = [
            requirements_dict.get(self.new_requirement.theDescription, None)
        ]

        for to_delete_req in to_delete_reqs:
            if to_delete_req is not None:
                self.to_delete_ids.append(to_delete_req['theId'])

        for req_id in self.to_delete_ids:
            url = '/api/requirements/id/%d?session_id=test' % req_id
            self.logger.info('[%s] URL: %s', method, url)
            rv = self.app.delete(url)
            self.logger.debug('[%s] Response data: %s', method, rv.data)
            json_resp = jsonpickle.decode(rv.data)
            self.assertIsNotNone(json_resp, 'No results after deserialization')
            message = json_resp.get('message', None)
            self.assertIsNotNone(message, 'No message returned')
        self.logger.info('')
