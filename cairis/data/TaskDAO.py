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

from cairis.core.ARM import *
from cairis.core.TaskEnvironmentProperties import TaskEnvironmentProperties
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.Task import Task
from cairis.core.TaskParameters import TaskParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import TaskModel, TaskEnvironmentPropertiesModel
from cairis.tools.SessionValidator import check_required_keys
__author__ = 'Shamal Faily'


class TaskDAO(CairisDAO):

  def __init__(self, session_id):
    """
    :raise CairisHTTPError:
    """
    CairisDAO.__init__(self, session_id)

  def get_tasks(self, constraint_id=-1, simplify=True):
    """
    :rtype: dict[str,Task]
    :return
    :raise ARMHTTPError:
    """
    try:
      tasks = self.db_proxy.getTasks(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in tasks.items():
        tasks[key] = self.simplify(value)

    return tasks

  def get_task_by_name(self, name, simplify=True):
    """
    :rtype: Task
    :raise ObjectNotFoundHTTPError:
    """
    tasks = self.get_tasks(simplify=simplify)
    found_task = tasks.get(name, None)

    if found_task is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided task name')

    return found_task

  def add_task(self, task):
    """
    :type task: Task
    :rtype: int
    :raise ARMHTTPError:
    """
    task_params = TaskParameters(
      tName=task.name(),
      tSName=task.shortCode(),
      tObjt=task.objective(),
      isAssumption=task.assumption(),
      tAuth=task.author(),
      tags=task.tags(),
      cProps=task.environmentProperties()
    )

    try:
      if not self.check_existing_task(task.name()):
        new_id = self.db_proxy.addTask(task_params)
        return new_id
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=task.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_task(self, task, name):
    found_task = self.get_task_by_name(name, simplify=False)

    task_params = TaskParameters(
      tName=task.name(),
      tSName=task.shortCode(),
      tObjt=task.objective(),
      isAssumption=task.assumption(),
      tAuth=task.author(),
      tags=task.tags(),
      cProps=task.environmentProperties()
    )

    task_params.setId(found_task.id())

    try:
      self.db_proxy.updateTask(task_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_task(self, name):
    found_task = self.get_task_by_name(name, simplify=False)
    task_id = found_task.id()

    try:
      self.db_proxy.deleteTask(task_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_task(self, name):
    """
    :rtype: bool
    :raise: ARMHTTPError
    """
    try:
      self.db_proxy.nameCheck(name, 'task')
      return False
    except DatabaseProxyException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
        self.close()
        raise ARMHTTPError(ex)
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
        self.close()
        raise ARMHTTPError(ex)


  def from_json(self, request):
    """
    :rtype : Task
    :raise MalformedJSONHTTPError:
    """
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TaskModel.required)
    json_dict['__python_obj__'] = Task.__module__ + '.' + Task.__name__

    task_props = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    task = json_serialize(json_dict)
    task = json_deserialize(task)
    task.theEnvironmentProperties = task_props
    if not isinstance(task, Task):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return task

  def simplify(self, obj):
    assert isinstance(obj, Task)
    obj.theEnvironmentDictionary = {}

    delattr(obj, 'theEnvironmentDictionary')
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, TaskEnvironmentProperties)
          new_props.append(real_prop)
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, TaskEnvironmentPropertiesModel.required)
          new_prop = TaskEnvironmentProperties(
                       environmentName=fake_prop['theEnvironmentName'],
                       deps=fake_prop['theDependencies'],
                       personas=fake_prop['thePersonas'],
                       assets=fake_prop['theAssets'],
                       concs=fake_prop['theConcernAssociations'],
                       narrative=fake_prop['theNarrative'],
                       consequences=fake_prop['theConsequences'],
                       benefits=fake_prop['theBenefits'],
                       tCodes=fake_prop['theCodes']
                     )
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])
    return new_props
