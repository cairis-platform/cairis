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
from cairis.core.Task import Task
from cairis.core.TaskEnvironmentProperties import TaskEnvironmentProperties
from cairis.test.CairisDaemonTestCase import CairisDaemonTestCase
import os
from cairis.mio.ModelImport import importModelFile
from cairis.tools.PseudoClasses import PersonaTaskCharacteristics
from cairis.tools.ModelDefinitions import ConcernAssociationModel

__author__ = 'Shamal Faily'


class TaskAPITests(CairisDaemonTestCase):

  @classmethod
  def setUpClass(cls):
    importModelFile(os.environ['CAIRIS_SRC'] + '/../examples/exemplars/NeuroGrid/NeuroGrid.xml',1,'test')

  
  def setUp(self):
    # region Class fields
    self.logger = logging.getLogger(__name__)

    self.existing_task_name = 'Upload data'
    self.existing_environment_name = 'Psychosis'
    self.existing_direct_flag=False
    self.existing_personas=[PersonaTaskCharacteristics('Claire','Medium','Medium','Low','Medium')]
    self.existing_assets=['Clinical data','Portal','Client workstation']
    self.existing_concern_associations=[ConcernAssociationModel('Portal','1','connects','Client workstation','1')]
    self.existing_narrative='Claire wants to analyse a data set, in relation to other data sets on NeuroGrid.  She anonymises her data to the extent that as much personalised data is removed as possible, but not to the extent that her analysis software will fail.  She then uploads this data, tagging this as available only to members of her exemplar.'
    self.existing_consequences='None'
    self.existing_benefits='None'
    self.existing_codes=[]

    task_class = Task.__module__+'.'+Task.__name__
    # endregion

  def test_get_all(self):
    method = 'test_get_all'
    rv = self.app.get('/api/tasks?session_id=test')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    tasks = jsonpickle.decode(responseData)
    self.assertIsNotNone(tasks, 'No results after deserialization')
    self.assertIsInstance(tasks, list, 'The result is not a list as expected')
    self.assertGreater(len(tasks), 0, 'No tasks in the list')
    self.logger.info('[%s] Tasks found: %d', method, len(tasks))
    task = tasks[0]
    self.logger.info('[%s] First task: %s\n', method, task['theName'])

  def test_get_by_name(self):
    method = 'test_get_by_name'
    url = '/api/tasks/name/%s?session_id=test' % quote(self.existing_task_name)
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    task = jsonpickle.decode(responseData)
    self.assertIsNotNone(task, 'No results after deserialization')
    self.logger.info('[%s] Task: %s\n', method, task['theName'])

  def test_load_by_name(self):
    method = 'test_load_by_name'
    url = '/api/tasks/name/' + quote(self.existing_task_name) + '/environment/Psychosis/load?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No results after deserialization')
    self.assertEqual(responseData,'5');

  def test_hindrance_by_name(self):
    method = 'test_hindrance_by_name'
    url = '/api/tasks/name/' + quote(self.existing_task_name) + '/environment/Psychosis/hindrance?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No results after deserialization')
    self.assertEqual(responseData,'1');

  def test_score_by_name(self):
    method = 'test_score_by_name'
    url = '/api/tasks/name/' + quote(self.existing_task_name) + '/environment/Psychosis/score?session_id=test'
    rv = self.app.get(url)
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No results after deserialization')
    self.assertEqual(responseData,'6');

  def test_delete(self):
    method = 'test_delete'
    url = '/api/tasks/name/%s?session_id=test' % quote(self.prepare_new_task().name())
    new_task_body = self.prepare_json()

    self.app.delete(url)
    self.logger.info('[%s] Object to delete: %s', method, new_task_body)
    self.app.post('/api/tasks', content_type='application/json', data=new_task_body)
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
    url = '/api/tasks'
    self.logger.info('[%s] URL: %s', method, url)
    new_task_body = self.prepare_json()

    self.app.delete('/api/tasks/name/%s?session_id=test' % quote(self.prepare_new_task().name()))
    rv = self.app.post(url, content_type='application/json', data=new_task_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertIsNotNone(msg, 'No message returned')
    self.logger.info('[%s] Message: %s\n', method, msg)

    rv = self.app.delete('/api/tasks/name/%s?session_id=test' % quote(self.prepare_new_task().name()))

  def test_put(self):
    method = 'test_put'
    url = '/api/tasks'
    self.logger.info('[%s] URL: %s', method, url)
    new_task_body = self.prepare_json()

    rv = self.app.delete('/api/tasks/name/%s?session_id=test' % quote(self.prepare_new_task().name()))
    rv = self.app.post(url, content_type='application/json', data=new_task_body)
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp, 'No results after deserialization')
    msg = json_resp.get('message', None)
    self.assertIsNotNone(msg, 'No message returned')
    self.logger.info('[%s] Message: %s', method, msg)

    task_to_update = self.prepare_new_task()
    task_to_update.theName = 'Edited test task'
    upd_env_body = self.prepare_json(task=task_to_update)
    rv = self.app.put('/api/tasks/name/%s?session_id=test' % quote(self.prepare_new_task().name()), data=upd_env_body, content_type='application/json')
    self.assertIsNotNone(rv.data, 'No response')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    json_resp = jsonpickle.decode(responseData)
    self.assertIsNotNone(json_resp)
    self.assertIsInstance(json_resp, dict)
    message = json_resp.get('message', None)
    self.assertIsNotNone(message, 'No message in response')
    self.logger.info('[%s] Message: %s', method, message)
    self.assertGreater(message.find('updated'), -1, 'The task was not successfully updated')

    rv = self.app.get('/api/tasks/name/%s?session_id=test' % quote(task_to_update.name()))
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    upd_task = jsonpickle.decode(responseData)
    self.assertIsNotNone(upd_task, 'Unable to decode JSON data')
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.logger.info('[%s] Task: %s\n', method, upd_task['theName'])

    rv = self.app.delete('/api/tasks/name/%s?session_id=test' % quote(task_to_update.theName))

  def test_misusability_model(self):
    url = '/api/tasks/model/misusability/Policy%20conflict/characteristic/all?session_id=test'
    method = 'test_misusability_model'
    self.logger.info('[%s] URL: %s', method, url)
    rv = self.app.get(url, content_type='application/json')
    if (sys.version_info > (3,)):
      responseData = rv.data.decode('utf-8')
    else:
      responseData = rv.data
    self.logger.debug('[%s] Response data: %s', method, responseData)
    self.assertIsNotNone(responseData, 'No results after deserialization')
    self.assertEqual(responseData.find('svg'),1)


  def prepare_new_task(self):
    new_task_props = [
      TaskEnvironmentProperties(
        environmentName=self.existing_environment_name,
        deps=self.existing_direct_flag,
        personas=self.existing_personas,
        assets=self.existing_assets,
        concs=self.existing_concern_associations,
        narrative=self.existing_narrative,
        consequences=self.existing_consequences,
        benefits=self.existing_benefits,
        tCodes=self.existing_codes
      )
    ]

    new_task = Task(
      tId=-1,
      tName='New task',
      tShortCode='NT',
      tObjt='New objective',
      isAssumption=True,
      tAuth='New Author',
      tags=[],
      cProps=[]
    )
    new_task.theEnvironmentProperties = new_task_props

    new_task.theEnvironmentDictionary = {}

    delattr(new_task, 'theEnvironmentDictionary')

    return new_task

  def prepare_dict(self, task=None):
    if task is None:
      task = self.prepare_new_task()
    else:
      assert isinstance(task, Task)

    return {
      'session_id': 'test',
      'object': task,
    }

  def prepare_json(self, data_dict=None, task=None):
    if data_dict is None:
      data_dict = self.prepare_dict(task=task)
    else:
      assert isinstance(data_dict, dict)
    new_task_body = jsonpickle.encode(data_dict, unpicklable=False)
    self.logger.info('JSON data: %s', new_task_body)
    return new_task_body
