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
from io import StringIO
import os
import jsonpickle
from cairis.core.ClassAssociation import ClassAssociation
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class AssetAssociationAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_assoc = ClassAssociation(
      associationId = '-1',
      envName = 'Psychosis',
      headName = 'Portal',
      headDim = 'asset',
      headNav = '0',
      headType = 'Association',
      headMultiplicity = '*',
      headRole = '',
      tailRole = '',
      tailMultiplicity = '*',
      tailType = 'Association',
      tailNav = '0',
      tailDim = 'asset',
      tailName = 'User certificate',
      rationale='None'
    )
    self.new_assoc_dict = {
      'session_id' : 'test',
      'object': self.new_assoc
    }

  def test_get_all(self):
    method = 'test_get_asset_associations'
    url = '/api/assets/association?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      assocs = jsonpickle.decode(rv.data.decode('utf-8'))
    else:
      assocs = jsonpickle.decode(rv.data)
    self.assertIsNotNone(assocs, 'No results after deserialization')
    self.assertEqual(len(assocs),39)

  def test_get(self):
    method = 'test_asset_association'
    url = '/api/assets/association/environment/Psychosis/head/Client%20workstation/tail/Web-browser?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      assoc = jsonpickle.decode(rv.data.decode('utf-8'))
    else:
      assoc = jsonpickle.decode(rv.data)
    self.assertIsNotNone(assoc, 'No results after deserialization')
    self.assertEqual(assoc['theHeadAsset'],'Client workstation')
    self.assertEqual(assoc['theTailAsset'],'Web-browser')

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/assets/association', content_type='application/json', data=jsonpickle.encode(self.new_assoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Psychosis / Portal / User certificate created')

  def test_put(self):
    method = 'test_put'

    self.new_assoc_dict['object'].theTailNavigation = '1'
    oldEnvName = self.new_assoc_dict['object'].theEnvironmentName
    oldHeadName = self.new_assoc_dict['object'].theHeadAsset
    oldTailName = self.new_assoc_dict['object'].theTailAsset
    rv = self.app.put('/api/assets/association/environment/' + oldEnvName + '/head/' + oldHeadName + '/tail/' + oldTailName, content_type='application/json', data=jsonpickle.encode(self.new_assoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Psychosis / Portal / User certificate updated')

  def test_delete(self):
    method = 'test_delete'
    rv = self.app.post('/api/assets/association', content_type='application/json', data=jsonpickle.encode(self.new_assoc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/assets/association/environment/Psychosis/head/Portal/tail/User%20certificate?session_id=test'
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'Psychosis / Portal / User certificate deleted')
