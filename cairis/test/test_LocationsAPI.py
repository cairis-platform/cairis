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
import json
import jsonpickle
from cairis.core.Location import Location
from cairis.core.Locations import Locations
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
from cairis.mio.ModelImport import importModelFile,importLocationsFile
from cairis.tools.JsonConverter import json_deserialize
import os

__author__ = 'Shamal Faily'

class LocationsAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/ACME_Water.xml',1,'test')
    importLocationsFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/ACME_Water/PooleWWTW.xml','test')

  def setUp(self):
    self.logger = logging.getLogger(__name__)
    f = open(os.environ['CAIRIS_SRC'] + '/test/locations.json')
    d = json.load(f)
    f.close()
    iLocations = d['locations']
    newLocsName = iLocations[1]['theName']
    newLocsDia = iLocations[1]['theDiagram']
    newLocations = []

    iLoc1 = iLocations[1]['theLocations'][0]
    iLoc1Name = iLoc1['theName']
    iLoc1AssetInstances = []
    iLoc1PersonaInstances = []
    iLoc1Links = iLoc1['theLinks']
    newLocations.append(Location(-1,iLoc1Name,iLoc1AssetInstances,iLoc1PersonaInstances,iLoc1Links))

    iLoc2 = iLocations[1]['theLocations'][1]
    iLoc2Name = iLoc2['theName']
    iLoc2AssetInstances = [{'theName':iLoc2['theAssetInstances'][0]['theName'],'theAsset':iLoc2['theAssetInstances'][0]['theAsset']}]
    iLoc2PersonaInstances = [{'theName':iLoc2['thePersonaInstances'][0]['theName'],'thePersona':iLoc2['thePersonaInstances'][0]['thePersona']}]
    iLoc2Links = iLoc2['theLinks']
    newLocations.append(Location(-1,iLoc2Name,iLoc2AssetInstances,iLoc2PersonaInstances,iLoc2Links))
    
    self.new_locs = Locations(
      locsId = '-1',
      locsName = newLocsName,
      locsDiagram = newLocsDia,
      locs = newLocations)
    self.new_locs_dict = {
      'session_id' : 'test',
      'object': self.new_locs
    }
    self.existing_locs_name = 'PooleWWTW'

  def test_get_all(self):
    method = 'test_get_locations'
    url = '/api/locations?session_id=test'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    locs = jsonpickle.decode(responseData)
    self.assertIsNotNone(locs, 'No results after deserialization')
    self.assertIsInstance(locs, list, 'The result is not a dictionary as expected')
    self.assertGreater(len(locs), 0, 'No Locations in the dictionary')
    self.logger.info('[%s] Locations found: %d', method, len(locs))
    locs = locs[0]
    self.logger.info('[%s] First locations: %s\n', method, locs['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/locations/name/%s?session_id=test' % quote(self.existing_locs_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    locs = jsonpickle.decode(responseData)
    self.assertIsNotNone(locs, 'No results after deserialization')
    self.logger.info('[%s] Locations: %s\n', method, locs['theName'])

  def test_post(self):
    method = 'test_post_new'
    rv = self.app.post('/api/locations', content_type='application/json', data=jsonpickle.encode(self.new_locs_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'SturminsterWTW created')

  def test_put(self):
    method = 'test_put'
    url = '/api/locations/name/%s?session_id=test' % quote(self.new_locs_dict['object'].theName)
    rv = self.app.put(url, content_type='application/json', data=jsonpickle.encode(self.new_locs_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'SturminsterWTW updated')

  def test_delete(self):
    method = 'test_delete'

    rv = self.app.post('/api/locations', content_type='application/json', data=jsonpickle.encode(self.new_locs_dict))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)

    url = '/api/locations/name/%s?session_id=test' % quote(self.new_locs.theName)
    rv = self.app.delete(url)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = json_deserialize(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    ackMsg = json_resp.get('message', None)
    self.assertEqual(ackMsg, 'SturminsterWTW deleted')

  def test_locations_model(self):
    method = 'test_locations_model'
    url = '/api/locations/model/locations/' + quote(self.existing_locs_name) + '/environment/Day?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
