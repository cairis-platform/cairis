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
import json
from cairis.tools.JsonConverter import json_deserialize
from cairis.core.PersonaCharacteristic import PersonaCharacteristic
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.PseudoClasses import CharacteristicReference
import os

__author__ = 'Shamal Faily'

class PersonaCharacteristicAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1,'test')


  def setUp(self):
    self.logger = logging.getLogger(__name__)
    self.new_pc = {
      "thePersonaName" : "Rick",
      "theModQual" : "Maybe",
      "theVariable" : "Activities",
      "theName" : "This is a test characteristic",
      "theGrounds" : [{"theReferenceName": "Line manager site authorisation", "theDimensionName": "document", "theCharacteristicType": "grounds" , "theReferenceDescription": "Can only access sites they have been authorised to; permission for authorisation changes need to be sought from the line manager.","theReferenceSynopsis":{"theActor" : "Rick", "theActorType" : "persona", "theSynopsis" : "Holds authorisation", "theDimension" : "goal"}, "theReferenceContribution" : {"theMeansEnd" : "means", "theContribution" : "SomePositive"}}],
      "theWarrant" : [{"theReferenceDescription": "Work reports are filed and sent to ACME monthly.", "theDimensionName": "document", "theCharacteristicType": "warrant", "theReferenceName": "Work reports are filed","theReferenceSynopsis":{"theActor" : "Rick", "theActorType" : "persona", "theSynopsis" : "Reports filed", "theDimension" : "goal"}, "theReferenceContribution" : {"theMeansEnd" : "means", "theContribution" : "SomePositive"}}],
      "theRebuttal" : [{"theReferenceDescription": "Everything that happens is logged.", "theDimensionName": "document", "theCharacteristicType": "rebuttal", "theReferenceName": "Everything is logged","theReferenceSynopsis":{"theActor" : "Risk", "theActorType" : "persona", "theSynopsis" : "Event logged", "theDimension" : "goal"}, "theReferenceContribution" : {"theMeansEnd" : "means", "theContribution" : "SomePositive"}}],
      "theBacking" : ['Business compliance GT concept'],
      "theCharacteristicSynopsis" : {"theActor" : "Rick", "theActorType" : "persona", "theSynopsis" : "Characteristic tested", "theDimension" : "goal"}
    }
    self.new_pc_dict = {
      'session_id' : 'test',
      'object': self.new_pc
    }
    self.existing_pc_name = 'Personal safety is an infosec hygiene factor'

  def test_get_all(self):
    method = 'test_get_persona_characteristics'
    url = '/api/persona_characteristics?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    pcs = jsonpickle.decode(responseData)
    self.assertIsNotNone(pcs, 'No results after deserialization')
    self.assertIsInstance(pcs, dict, 'The result is not a dictionary as expected')
    self.assertGreater(len(pcs), 0, 'No persona characteristics in the dictionary')
    self.logger.info('[%s] Persona characteristics found: %d', method, len(pcs))
    pc = list(pcs.values())[0]
    self.logger.info('[%s] First persona characteristic: %s', method, pc['theName'])

  def test_get_all_summary(self):
    method = 'test_get_all_summary'
    rv = self.app.get('/api/persona_characteristics/summary?session_id=test')
    if (sys.version_info > (3,)):
      pcs = json_deserialize(rv.data.decode('utf-8'))
    else:
      pcs = json_deserialize(rv.data)
    self.assertIsNotNone(pcs, 'No results after deserialization')
    self.assertGreater(len(pcs), 0, 'No persona characteristics summaries')
    self.assertIsInstance(pcs[0], dict)
    self.logger.info('[%s] Persona characteristics found: %d', method, len(pcs))
    self.logger.info('[%s] First persona characteristic summary: %s', method, pcs[0]['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/persona_characteristics/name/%s?session_id=test' % quote(self.existing_pc_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    pc = jsonpickle.decode(responseData)
    self.assertIsNotNone(pc, 'No results after deserialization')
    self.logger.info('[%s] Persona characteristic: %s \n', method, pc['theName'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/persona_characteristics', content_type='application/json', data=json.dumps(self.new_pc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('created'),-1,'PC not created')


  def test_put(self):
    method = 'test_put'
    self.new_pc_dict['object']['theName'] = 'Updated text segment'
    url = '/api/persona_characteristics/name/%s?session_id=test' % quote('This is a test characteristic')
    rv = self.app.put(url, content_type='application/json', data=json.dumps(self.new_pc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('updated'),-1,'PC not updated')


  def test_delete(self):
    method = 'test_delete'
    rv = self.app.post('/api/persona_characteristics', content_type='application/json', data=json.dumps(self.new_pc_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/persona_characteristics/name/%s?session_id=test' % quote('This is a test characteristic')
    rv = self.app.delete(url)

    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertGreater(ackMsg.find('deleted'),-1,'PC not deleted')
