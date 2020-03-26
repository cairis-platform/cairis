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
from cairis.core.TaskContribution import TaskContribution
from cairis.misc.KaosModel import KaosModel
from cairis.misc.AssumptionTaskModel import AssumptionTaskModel as GraphicalAssumptionTaskModel
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import TaskModel, TaskEnvironmentPropertiesModel, ConcernAssociationModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.tools.PseudoClasses import PersonaTaskCharacteristics, TaskGoalContribution


__author__ = 'Shamal Faily'


class TaskDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'task')

  def get_objects(self, constraint_id=-1):
    try:
      tasks = self.db_proxy.getTasks(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    taskKeys = sorted(tasks.keys())
    taskList = []
    for key in taskKeys:
      taskList.append(self.simplify(tasks[key]))
    return taskList

  def get_object_by_name(self, name, simplify=True):
    try:
      taskId = self.db_proxy.getDimensionId(name,'task')
      tasks = self.db_proxy.getTasks(taskId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    found_task = tasks.get(name, None)

    if found_task is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided task name')
    found_task = self.simplify(found_task)
    return found_task

  def add_object(self, task):
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
        self.db_proxy.addTask(task_params)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=task.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, task, name):
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
      taskId = self.db_proxy.getDimensionId(name,'task')
      task_params.setId(taskId)
      self.db_proxy.updateTask(task_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      taskId = self.db_proxy.getDimensionId(name,'task')
      self.db_proxy.deleteTask(taskId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_task(self, name):
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
    del obj.theId
    del obj.theEnvironmentDictionary
    del obj.scoreLookup
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, TaskEnvironmentProperties)
          del real_prop.theCodes
          ptList = []
          for ptc in real_prop.personas():
            ptList.append(PersonaTaskCharacteristics(ptc[0],ptc[1],ptc[2],ptc[3],ptc[4])) 
          real_prop.thePersonas = ptList
          gcaList = []
          for gca in real_prop.concernAssociations():
            gcaList.append(ConcernAssociationModel(gca[0],gca[1],gca[2],gca[3],gca[4])) 
          real_prop.theConcernAssociations = gcaList
          realContList = real_prop.theContributions
          del real_prop.theContributions
          contList = []
          for tgc in realContList:
            contList.append(TaskGoalContribution(tgc.source(),tgc.destination(),tgc.environment(),tgc.contribution()))
          real_prop.theContributions = contList
          new_props.append(real_prop)
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, TaskEnvironmentPropertiesModel.required)
          ptList = [] 
          for ptc in fake_prop['thePersonas']:
            ptList.append([ptc['thePersona'],ptc['theDuration'],ptc['theFrequency'],ptc['theDemands'],ptc['theGoalConflict']]) 
          fake_prop['thePersonas'] = ptList
          gcaList = []
          for gca in fake_prop['theConcernAssociations']:
            gcaList.append([gca['theSource'],gca['theSourceNry'],gca['theLinkVerb'],gca['theTarget'],gca['theTargetNry']]) 
          fake_prop['theConcernAssociations'] = gcaList
          contList = []
          for tgc in fake_prop['theContributions']:
            contList.append(TaskContribution(tgc['theSource'],tgc['theDestination'],tgc['theEnvironment'],tgc['theContribution']))
          new_prop = TaskEnvironmentProperties(
                       environmentName=fake_prop['theEnvironmentName'],
                       deps=fake_prop['theDependencies'],
                       personas=fake_prop['thePersonas'],
                       assets=fake_prop['theAssets'],
                       concs=fake_prop['theConcernAssociations'],
                       narrative=fake_prop['theNarrative'],
                       consequences=fake_prop['theConsequences'],
                       benefits=fake_prop['theBenefits'],
                       contribs=contList,
                       tCodes=[]
                     )
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])
    return new_props

  def get_task_model(self, environment_name,task_name,misusecase_name, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    if task_name == 'all':  
      task_name = ''
    if misusecase_name == 'all': 
       misusecase_name = ''

    try:
      mcFilter = False
      filter_name = task_name
      if misusecase_name != '': 
        mcFilter = True
        filter_name = misusecase_name
      associationDirectory = self.db_proxy.taskModel(environment_name,filter_name,mcFilter)
      associations = KaosModel(list(associationDirectory.values()), environment_name, kaosModelType = 'task',goalName = filter_name,db_proxy=self.db_proxy, font_name=fontName, font_size=fontSize)
      dot_code = associations.graph()
      if not dot_code:
        raise ObjectNotFoundHTTPError('The task model')
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def task_score_by_name_environment(self,task_name,environment_name, pathValues = []):
    try:
      return self.db_proxy.taskUsabilityScore(task_name,environment_name)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def task_load_by_name_environment(self,task_name,environment_name,pathValues = []):
    try:
      taskId = self.db_proxy.getDimensionId(task_name,'task')
      envId = self.db_proxy.getDimensionId(environment_name,'environment')
      return self.db_proxy.taskLoad(taskId,envId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def task_hindrance_by_name_environment(self,task_name,environment_name, pathValues = []):
    try:
      taskId = self.db_proxy.getDimensionId(task_name,'task')
      envId = self.db_proxy.getDimensionId(environment_name,'environment')
      return self.db_proxy.countermeasureLoad(taskId,envId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_misusability_model(self, mc_name,tc_name, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    if tc_name == 'all':
      tc_name = ''
    try:
      associations = self.db_proxy.assumptionTaskModel(mc_name,tc_name)
      model = GraphicalAssumptionTaskModel(associations,db_proxy=self.db_proxy, font_name=fontName, font_size=fontSize)
      dot_code = model.graph()
      if not dot_code:
        raise ObjectNotFoundHTTPError('The misusability model')
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
