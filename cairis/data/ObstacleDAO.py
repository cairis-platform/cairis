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
from cairis.core.Obstacle import Obstacle
from cairis.core.Vulnerability import Vulnerability
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from cairis.core.ObstacleParameters import ObstacleParameters
from cairis.core.VulnerabilityParameters import VulnerabilityParameters
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
from cairis.misc.KaosModel import KaosModel
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import ObstacleEnvironmentPropertiesModel, ObstacleModel, RefinementModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts

__author__ = 'Shamal Faily'

class ObstacleDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'obstacle')

  def get_objects(self, constraint_id=-1, simplify=True):
    try:
      obstacles = self.db_proxy.getObstacles(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in list(obstacles.items()):
        obstacles[key] = self.simplify(value)

    return obstacles

  def get_objects_summary(self):
    try:
      obs = self.db_proxy.getObstaclesSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return obs

  def get_object_by_name(self, name, simplify=True):
    obsId = self.db_proxy.getDimensionId(name,'obstacle')
    found_obstacle = None
    obstacles = self.get_objects(obsId,simplify=False)

    if obstacles is not None:
      found_obstacle = obstacles.get(name)

    if found_obstacle is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided obstacle name')

    if simplify:
      found_obstacle = self.simplify(found_obstacle)

    return found_obstacle

  def add_object(self, obstacle):
    obsParams = ObstacleParameters(obsName=obstacle.theName,obsOrig=obstacle.theOriginator,tags=obstacle.theTags,properties=obstacle.theEnvironmentProperties)
    if not self.check_existing_obstacle(obstacle.theName):
      self.db_proxy.addObstacle(obsParams)
    else:
      self.close()
      raise OverwriteNotAllowedHTTPError('The provided obstacle name')

  def update_object(self, obstacle, name):
    old_obstacle = self.get_object_by_name(name, simplify=False)
    id = old_obstacle.theId
    params = ObstacleParameters(obsName=obstacle.theName,obsOrig=obstacle.theOriginator,tags=obstacle.theTags,properties=obstacle.theEnvironmentProperties)
    params.setId(id)

    try:
      self.db_proxy.updateObstacle(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      obsId = self.db_proxy.getDimensionId(name,'obstacle')
      self.db_proxy.deleteObstacle(obsId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_obstacle(self, name):
    try:
      self.db_proxy.nameCheck(name, 'obstacle')
      return False
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
      self.close()
      raise ARMHTTPError(ex)

  def get_obstacle_model(self, environment_name, obstacle_name, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    if obstacle_name == 'all':  
      obstacle_name = ''

    try:
      obstacle_filter = 0
      associationDictionary = self.db_proxy.obstacleModel(environment_name, obstacle_name, obstacle_filter)
      associations = KaosModel(list(associationDictionary.values()), environment_name, 'obstacle',obstacle_name,db_proxy=self.db_proxy, font_name=fontName,font_size=fontSize)
      dot_code = associations.graph()
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  # region Obstacle types
  def get_obstacle_types(self, environment_name=''):
    try:
      obstacle_types = self.db_proxy.getValueTypes('obstacle_type', environment_name)
      return obstacle_types
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def get_obstacle_type_by_name(self, name, environment_name=''):
    found_type = None
    obstacle_types = self.get_obstacle_types(environment_name=environment_name)

    if obstacle_types is None or len(obstacle_types) < 1:
      raise ObjectNotFoundHTTPError('Obstacle types')

    idx = 0
    while found_type is None and idx < len(obstacle_types):
      if obstacle_types[idx].theName == name:
        found_type = obstacle_types[idx]
      idx += 1

    if found_type is None:
      raise ObjectNotFoundHTTPError('The provided obstacle type name')
    return found_type

  def add_obstacle_type(self, obstacle_type, environment_name=''):
    assert isinstance(obstacle_type, ValueType)
    type_exists = self.check_existing_obstacle_type(obstacle_type.theName, environment_name=environment_name)

    if type_exists:
      raise OverwriteNotAllowedHTTPError(obj_name='The obstacle type')

    params = ValueTypeParameters(vtName=obstacle_type.theName,vtDesc=obstacle_type.theDescription,vType='obstacle_type',envName=environment_name,vtScore=obstacle_type.theScore,vtRat=obstacle_type.theRationale)

    try:
      return self.db_proxy.addValueType(params)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def update_obstacle_type(self, obstacle_type, name, environment_name=''):
    assert isinstance(obstacle_type, ValueType)
    found_type = self.get_obstacle_type_by_name(name, environment_name)
    params = ValueTypeParameters(vtName=obstacle_type.theName,vtDesc=obstacle_type.theDescription,vType='obstacle_type',envName=environment_name,vtScore=obstacle_type.theScore,vtRat=obstacle_type.theRationale)
    params.setId(found_type.theId)

    try:
      self.db_proxy.updateValueType(params)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def delete_obstacle_type(self, name, environment_name=''):
    found_type = self.get_obstacle_type_by_name(name, environment_name)

    try:
      self.db_proxy.deleteObstacleType(found_type.theId)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def check_existing_obstacle_type(self, name, environment_name):
    try:
      self.get_obstacle_type_by_name(name, environment_name)
      return True
    except ObjectNotFoundHTTPError:
      return False
  # endregion

  # region Goal values
  def get_obstacle_values(self, environment_name=''):
    try:
      obstacle_values = self.db_proxy.getValueTypes('obstacle_value', environment_name)
      return obstacle_values
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def get_obstacle_value_by_name(self, name, environment_name=''):
    found_value = None
    obstacle_values = self.get_obstacle_values(environment_name=environment_name)
    if obstacle_values is None or len(obstacle_values) < 1:
      raise ObjectNotFoundHTTPError('Obstacle values')
    idx = 0
    while found_value is None and idx < len(obstacle_values):
      if obstacle_values[idx].theName == name:
        found_value = obstacle_values[idx]
      idx += 1
    if found_value is None:
      raise ObjectNotFoundHTTPError('The provided obstacle value name')
    return found_value

  def update_obstacle_value(self, obstacle_value, name, environment_name=''):
    assert isinstance(obstacle_value, ValueType)
    found_value = self.get_obstacle_value_by_name(name, environment_name)
    params = ValueTypeParameters(vtName=obstacle_type.theName,vtDesc=obstacle_type.theDescription,vType='obstacle_type',envName=environment_name,vtScore=obstacle_type.theScore,vtRat=obstacle_type.theRationale)
    params.setId(found_value.theId)
    try:
      self.db_proxy.updateValueType(params)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def check_existing_obstacle_value(self, name, environment_name):
    try:
      self.get_obstacle_value_by_name(name, environment_name)
      return True
    except ObjectNotFoundHTTPError:
      return False
  # endregion

  def convert_properties(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      for real_prop in real_props:
        assert isinstance(real_prop, ObstacleEnvironmentProperties)
        del real_prop.theLabel

        new_goal_refinements = []
        for gr in real_prop.theGoalRefinements:
          new_goal_refinements.append(RefinementModel(gr[0],gr[1],gr[2],gr[3],gr[4]))

        new_subgoal_refinements = []
        for sgr in real_prop.theSubGoalRefinements:
          new_subgoal_refinements.append(RefinementModel(sgr[0],sgr[1],sgr[2],sgr[3],sgr[4]))

        real_prop.theGoalRefinements = new_goal_refinements
        real_prop.theSubGoalRefinements = new_subgoal_refinements
        new_props.append(real_prop)
    elif fake_props is not None:
      for fake_prop in fake_props:
        if fake_prop is not None:
          check_required_keys(fake_prop, ObstacleEnvironmentPropertiesModel.required)
          new_goal_refinements = []
          for gr in fake_prop['theGoalRefinements']:
            new_goal_refinements.append((gr['theEndName'],gr['theEndType'],gr['theRefType'],gr['isAlternate'],gr['theRationale']))
          new_subgoal_refinements = []
          for sgr in fake_prop['theSubGoalRefinements']:
            new_subgoal_refinements.append((sgr['theEndName'],sgr['theEndType'],sgr['theRefType'],sgr['isAlternate'],sgr['theRationale']))
          new_prop = ObstacleEnvironmentProperties(environmentName=fake_prop['theEnvironmentName'],lbl='',definition=fake_prop['theDefinition'],category=fake_prop['theCategory'],gRefs=new_goal_refinements,sgRefs=new_subgoal_refinements,concs=fake_prop['theConcerns'])
          new_prop.theProbability = fake_prop['theProbability']
          new_prop.theProbabilityRationale = fake_prop['theProbabilityRationale']
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])

    return new_props

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ObstacleModel.required)
    json_dict['__python_obj__'] = Obstacle.__module__+'.'+Obstacle.__name__
    props_list = json_dict.pop('theEnvironmentProperties', [])
    json_dict.pop('theEnvironmentDictionary', None)
    real_props = self.convert_properties(fake_props=props_list)

    new_json_obstacle = json_serialize(json_dict)
    new_json_obstacle = json_deserialize(new_json_obstacle)
    new_json_obstacle.theEnvironmentProperties = real_props

    if not isinstance(new_json_obstacle, Obstacle):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return new_json_obstacle

  def simplify(self, obstacle):
    obstacle.theEnvironmentProperties = self.convert_properties(real_props=obstacle.theEnvironmentProperties)
    assert isinstance(obstacle, Obstacle)
    del obstacle.theId
    del obstacle.theEnvironmentDictionary
    return obstacle

  def generate_vulnerability(self, name, pathValues = []):
    obs = self.db_proxy.dimensionObject(name,'obstacle')
    vps = []
    gaps = []
    for op in obs.environmentProperties():
      vps.append(VulnerabilityEnvironmentProperties(op.name(),'Negligible',op.concerns()))
      gaps.append(GoalAssociationParameters(op.name(),obs.name(),'obstacle','and',obs.name() + '(V)','vulnerability'))
    v = VulnerabilityParameters(obs.name() + '(V)',obs.name(),self.db_proxy.defaultValue('vulnerability_type'),[],vps)
    self.db_proxy.addVulnerability(v)
    for gap in gaps:
      self.db_proxy.addGoalAssociation(gap)
