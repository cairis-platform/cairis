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
from StringIO import StringIO
import jsonpickle
from cairis.web_tests.CairisTests import CairisTests
from cairis.tools.PseudoClasses import ProjectSettings, Contributor, Revision

__author__ = 'Robin Quetin'


class ProjectTests(CairisTests):
    logger = logging.getLogger(__name__)
    xmlfile = '/home/cairisuser/cairis/examples/exemplars/NeuroGrid/NeuroGrid.xml'

    def test_settings_get(self):
        url = '/api/settings?session_id=test'
        method = 'test_settings_get'

        rv = self.app.get(url)
        self.assertIsNotNone(rv.data, 'No response')
        self.logger.debug('[%s] Response data: %s', method, rv.data)
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
        has_all_keys = all (k in json_dict for k in ProjectSettings.required)
        self.assertTrue(has_all_keys, 'The response is not a valid ProjectSettings object')
        self.logger.info('[%s] Project name: %s\n', method, json_dict['projectName'])

    def test_settings_put(self):
        url = '/api/settings?session_id=test'
        method = 'test_settings_put'
        rv = self.app.get(url)
        json_dict = jsonpickle.decode(rv.data)
        self.logger.info('[%s] Current project name: %s', method, json_dict['projectName'])

        settings = self.convert_to_obj(json_dict)
        settings.projectName = 'A new project name'
        new_json_dict = { 'session_id': 'test', 'object': settings }
        json_body = jsonpickle.encode(new_json_dict)
        rv = self.app.put(url, data=json_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        new_json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(new_json_dict, dict, 'Response is not a valid JSON dictionary')
        message = new_json_dict.get('message', None)
        self.assertIsNotNone(message)
        self.logger.info('[%s] Message: %s', method, message)

        rv = self.app.get(url)
        new_json_dict = jsonpickle.decode(rv.data)
        self.logger.info('[%s] New project name: %s\n', method, new_json_dict['projectName'])

        new_json_dict = { 'session_id': 'test', 'object': json_dict }
        json_body = jsonpickle.encode(new_json_dict)
        rv = self.app.put(url, data=json_body, content_type='application/json')

    def test_create_new_project(self):
        url = '/api/settings/create?session_id=test'
        import_url = '/api/import/file/type/all'
        method = 'test_create_new_project'
        rv = self.app.post(url)
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
        self.assertTrue(json_dict.has_key('message'), 'No message in reponse')
        message = str(json_dict['message'])
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('successfully'), -1, 'Failed to create new project')

        fs_xmlfile = open(self.xmlfile, 'rb')
        file_contents = fs_xmlfile.read()
        data = {
            'session_id': 'test',
            'file': (StringIO(file_contents), 'import.xml')
        }
        rv = self.app.post(import_url, data=data, content_type='multipart/form-data')
        self.assertIsNotNone(rv.data, 'No response after reimporting model')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'Response is not a valid JSON dictionary')
        assert isinstance(json_dict, dict)
        message = json_dict.get('message', None)
        self.assertIsNotNone(message, 'No message in response')
        self.assertGreater(message.find('Imported'), -1, 'Failed to import any data')
        self.logger.info('[%s] Successfully created new project and restored the example project\n', method)

    def convert_to_obj(self, json_dict):
        has_all_keys = all (k in json_dict for k in ProjectSettings.required)
        if has_all_keys:
            ps = ProjectSettings()
            ps.fontName = json_dict['fontName']
            ps.apFontSize = json_dict['apFontSize']
            ps.projectName = json_dict['projectName']
            ps.richPicture = json_dict['richPicture']
            ps.fontSize = json_dict['fontSize']
            ps.projectScope = json_dict['projectScope']
            ps.definitions = json_dict['definitions']
            ps.projectGoals = json_dict['projectGoals']
            ps.projectBackground = json_dict['projectBackground']
            ps.contributions = json_dict['contributions']
            ps.revisions = json_dict['revisions']

            for idx in range(0, len(ps.contributions)):
                ps.contributions[idx] = Contributor(
                    first_name=ps.contributions[idx]['firstName'],
                    surname=ps.contributions[idx]['surname'],
                    affliation=ps.contributions[idx]['affliation'],
                    role=ps.contributions[idx]['role']
                )

            for idx in range(0, len(ps.revisions)):
                ps.revisions[idx] = Revision(
                    id=ps.revisions[idx]['id'],
                    date=ps.revisions[idx]['date'],
                    description=ps.revisions[idx]['description']
                )

            return ps
        else:
            self.assertTrue(has_all_keys, 'Invalid object')
