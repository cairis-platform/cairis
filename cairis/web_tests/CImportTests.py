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

__author__ = 'Robin Quetin'


class CImportTests(CairisTests):
    xmlfile = '/home/cairisuser/cairis/examples/exemplars/NeuroGrid/NeuroGrid.xml'
    logger = logging.getLogger(__name__)

    def test_cimport_data_post(self):
        method = 'test_cimport_text_post'
        url = '/api/import/text'
        fs_xmlfile = open(self.xmlfile, 'rb')
        file_contents = fs_xmlfile.read()
        self.logger.info('[%s] URL: %s', method, url)
        self.logger.debug('[%s] XML file:\n%s', method, file_contents)

        urlenc_file_contents = quote(file_contents)
        json_dict = {
            'session_id': 'test',
            'object': {
                'urlenc_file_contents': urlenc_file_contents,
                'type': 'all'
            }
        }
        json_body = jsonpickle.encode(json_dict)
        rv = self.app.post(url, data=json_body, content_type='application/json')
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
        assert isinstance(json_dict, dict)
        message = json_dict.get('message')
        self.assertIsNotNone(message, 'Response does not contain a message')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('Imported'), -1, 'Nothing imported')

    def test_cimport_file_post(self):
        method = 'test_cimport_file_post'
        type = 'all'
        url = '/api/import/file/type/%s?session_id=test' % quote(type)
        fs_xmlfile = open(self.xmlfile, 'rb')
        file_contents = fs_xmlfile.read()
        self.logger.info('[%s] URL: %s', method, url)
        self.logger.debug('[%s] XML file:\n%s', method, file_contents)

        data = {
            'file': (StringIO(file_contents), 'import.xml'),
            'session_id': 'test'
        }
        rv = self.app.post(url, data=data, content_type='multipart/form-data')
        self.assertIsNotNone(rv.data, 'No response')
        json_dict = jsonpickle.decode(rv.data)
        self.assertIsInstance(json_dict, dict, 'The response is not a valid JSON dictionary')
        assert isinstance(json_dict, dict)
        message = json_dict.get('message')
        self.assertIsNotNone(message, 'Response does not contain a message')
        self.logger.info('[%s] Message: %s', method, message)
        self.assertGreater(message.find('Imported'), -1, 'Nothing imported')
