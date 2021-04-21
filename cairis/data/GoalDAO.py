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
from cairis.core.Goal import Goal
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.GoalParameters import GoalParameters
from cairis.daemon.CairisHTTPError import CairisHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
from cairis.misc.KaosModel import KaosModel
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import GoalEnvironmentPropertiesModel, GoalModel, ConcernAssociationModel, RefinementModel,PolicyStatementModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
import http

__author__ = 'Robin Quetin, Shamal Faily'

class GoalDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'goal')

  def get_objects(self, pathValues):
    constraint_id = pathValues[0]
    coloured = pathValues[1]
    if (coloured == '1'):
      coloured = True
    else:
      coloured = False
    try:
      if coloured:
        goals = self.db_proxy.getColouredGoals(constraint_id)
      else:
        goals = self.db_proxy.getGoals(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    goalKeys = sorted(goals.keys())
    goalList = []
    for key in goalKeys:
      goalList.append(self.simplify(goals[key]))
    return goalList

  def get_objects_summary(self):
    try:
      goals = self.db_proxy.getGoalsSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return goals


  def get_object_by_name(self, name, pathValues):
    coloured = pathValues[1]
    if (coloured == '1'):
      coloured = True
    else:
      coloured = False
    try:
      goalId = self.db_proxy.getDimensionId(name,'goal')
      if coloured:
        goals = self.db_proxy.getColouredGoals(goalId)
      else:
        goals = self.db_proxy.getGoals(goalId)

      found_goal = goals.get(name,None)
      if found_goal is None:
        self.close()
        raise ObjectNotFoundHTTPError('The provided goal name')
      found_goal = self.simplify(found_goal)
      return found_goal
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, goal, pathValues = []):
    goalParams = GoalParameters(goalName=goal.theName,goalOrig=goal.theOriginator,tags=goal.theTags,properties=goal.theEnvironmentProperties)
    try:
      if not self.check_existing_goal(goal.theName):
        self.db_proxy.addGoal(goalParams)
      else:
        self.close()
        raise CairisHTTPError(status_code=http.client.BAD_REQUEST,status="Object exists",message="An object with the name " + goal.theName + " already exists.")
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, goal, name, pathValues = []):
    params = GoalParameters(goalName=goal.theName,goalOrig=goal.theOriginator,tags=goal.theTags,properties=goal.theEnvironmentProperties)
    try:
      goalId = self.db_proxy.getDimensionId(name,'goal')
      params.setId(goalId)
      self.db_proxy.updateGoal(params)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name, pathValues = []):
    try:
      goalId = self.db_proxy.getDimensionId(name,'goal')
      self.db_proxy.deleteGoal(goalId)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError(ex)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_goal(self, name):
    try:
      self.db_proxy.nameCheck(name, 'goal')
      return False
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
      self.close()
      raise ARMHTTPError(ex)

  def get_goal_model(self, environment_name,goal_name,usecase_name, pathValues):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    is_top_level = pathValues[0]
    if goal_name == 'all':
      goal_name = ''
    if usecase_name == 'all':
      usecase_name = ''
    try:
      associationDictionary = {}
      goalFilter = 0
      ucFilter = 0
      if goal_name != '': 
        goalFilter = 1
      if usecase_name != '': 
        ucFilter = 1
        goal_name = usecase_name
      associationDictionary = self.db_proxy.goalModel(environment_name,goal_name,is_top_level,ucFilter)
      associations = KaosModel(list(associationDictionary.values()), environment_name, 'goal',goal_name,db_proxy=self.db_proxy, font_name=fontName,font_size=fontSize)
      dot_code = associations.graph()
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_responsibility_model(self, environment_name, role_name, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    if role_name == 'all':
      role_name = ''
    try:
      associationDictionary = self.db_proxy.responsibilityModel(environment_name, role_name)
      associations = KaosModel(list(associationDictionary.values()), environment_name, 'responsibility',goalName=role_name,db_proxy=self.db_proxy, font_name=fontName,font_size=fontSize)
      dot_code = associations.graph()
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)


  # region Goal types
  def get_goal_types(self, environment_name=''):
    try:
      goal_types = self.db_proxy.getValueTypes('goal_type', environment_name)
      return goal_types
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def get_goal_type_by_name(self, name, environment_name=''):
    found_type = None
    goal_types = self.get_goal_types(environment_name=environment_name)

    if goal_types is None or len(goal_types) < 1:
      raise ObjectNotFoundHTTPError('Goal types')

    idx = 0
    while found_type is None and idx < len(goal_types):
      if goal_types[idx].theName == name:
        found_type = goal_types[idx]
      idx += 1

    if found_type is None:
      raise ObjectNotFoundHTTPError('The provided goal type name')

    return found_type

  def add_goal_type(self, goal_type, environment_name=''):
    assert isinstance(goal_type, ValueType)
    type_exists = self.check_existing_goal_type(goal_type.theName, environment_name=environment_name)

    if type_exists:
      raise OverwriteNotAllowedHTTPError(obj_name='The goal type')

    params = ValueTypeParameters(
            vtName=goal_type.theName,
            vtDesc=goal_type.theDescription,
            vType='goal_type',
            envName=environment_name,
            vtScore=goal_type.theScore,
            vtRat=goal_type.theRationale)

    try:
      return self.db_proxy.addValueType(params)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def update_goal_type(self, goal_type, name, environment_name=''):
    assert isinstance(goal_type, ValueType)

    found_type = self.get_goal_type_by_name(name, environment_name)

    params = ValueTypeParameters(
            vtName=goal_type.theName,
            vtDesc=goal_type.theDescription,
            vType='goal_type',
            envName=environment_name,
            vtScore=goal_type.theScore,
            vtRat=goal_type.theRationale)
    params.setId(found_type.theId)

    try:
      self.db_proxy.updateValueType(params)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def delete_goal_type(self, name, environment_name=''):
    found_type = self.get_goal_type_by_name(name, environment_name)

    try:
      self.db_proxy.deleteGoalType(found_type.theId)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def check_existing_goal_type(self, name, environment_name):
    try:
      self.get_goal_type_by_name(name, environment_name)
      return True
    except ObjectNotFoundHTTPError:
      return False
  # endregion

  # region Goal values
  def get_goal_values(self, environment_name=''):
    try:
      goal_values = self.db_proxy.getValueTypes('goal_value', environment_name)
      return goal_values
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def get_goal_value_by_name(self, name, environment_name=''):
    found_value = None
    goal_values = self.get_goal_values(environment_name=environment_name)
    if goal_values is None or len(goal_values) < 1:
      raise ObjectNotFoundHTTPError('Goal values')
    idx = 0
    while found_value is None and idx < len(goal_values):
      if goal_values[idx].theName == name:
        found_value = goal_values[idx]
      idx += 1
    if found_value is None:
      raise ObjectNotFoundHTTPError('The provided goal value name')
    return found_value

  def update_goal_value(self, goal_value, name, environment_name=''):
    assert isinstance(goal_value, ValueType)
    found_value = self.get_goal_value_by_name(name, environment_name)
    params = ValueTypeParameters(
            vtName=goal_value.theName,
            vtDesc=goal_value.theDescription,
            vType='goal_value',
            envName=environment_name,
            vtScore=goal_value.theScore,
            vtRat=goal_value.theRationale
    )
    params.setId(found_value.theId)
    try:
      self.db_proxy.updateValueType(params)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)

  def check_existing_goal_value(self, name, environment_name):
    try:
      self.get_goal_value_by_name(name, environment_name)
      return True
    except ObjectNotFoundHTTPError:
      return False
  # endregion

  def convert_properties(self, goalName, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      for real_prop in real_props:
        assert isinstance(real_prop, GoalEnvironmentProperties)
        del real_prop.theLabel
        new_concern_assocs = []
        for concern_assoc in real_prop.theConcernAssociations:
          new_concern_assocs.append(ConcernAssociationModel(concern_assoc[0],concern_assoc[1],concern_assoc[2],concern_assoc[3],concern_assoc[4]))

        new_goal_refinements = []
        for gr in real_prop.theGoalRefinements:
          new_goal_refinements.append(RefinementModel(gr[0],gr[1],gr[2],gr[3],gr[4]))

        new_subgoal_refinements = []
        for sgr in real_prop.theSubGoalRefinements:
          new_subgoal_refinements.append(RefinementModel(sgr[0],sgr[1],sgr[2],sgr[3],sgr[4]))

        real_prop.theConcernAssociations = new_concern_assocs
        real_prop.theGoalRefinements = new_goal_refinements
        real_prop.theSubGoalRefinements = new_subgoal_refinements
        gp = real_prop.thePolicy
        if (gp != None):
          real_prop.thePolicy = PolicyStatementModel(goalName,gp['theEnvironmentName'],gp['theSubject'],gp['theAccessType'],gp['theResource'],gp['thePermission'])
        new_props.append(real_prop)
    elif fake_props is not None:
      for fake_prop in fake_props:
        check_required_keys(fake_prop, GoalEnvironmentPropertiesModel.required)

        new_concern_assocs = []
        for concern_assoc in fake_prop['theConcernAssociations']:
          new_concern_assocs.append([concern_assoc['theSource'],concern_assoc['theSourceNry'],concern_assoc['theLinkVerb'],concern_assoc['theTarget'],concern_assoc['theTargetNry']])

        new_goal_refinements = []
        for gr in fake_prop['theGoalRefinements']:
          new_goal_refinements.append((gr['theEndName'],gr['theEndType'],gr['theRefType'],gr['isAlternate'],gr['theRationale']))

        new_subgoal_refinements = []
        for sgr in fake_prop['theSubGoalRefinements']:
          new_subgoal_refinements.append((sgr['theEndName'],sgr['theEndType'],sgr['theRefType'],sgr['isAlternate'],sgr['theRationale']))

        fgp = fake_prop['thePolicy']
        if (fgp != None): 
          gp = {'theGoalName': goalName,'theEnvironmentName':fake_prop['theEnvironmentName'],'theSubject':fgp['theSubject'],'theAccessType':fgp['theAccessType'],'theResource':fgp['theResource'],'thePermission':fgp['thePermission']}
        else:
          gp = None

        new_prop = GoalEnvironmentProperties(
          environmentName=fake_prop['theEnvironmentName'],
          lbl='',
          definition=fake_prop['theDefinition'],
          category=fake_prop['theCategory'],
          priority=fake_prop['thePriority'],
          fitCriterion=fake_prop['theFitCriterion'],
          issue=fake_prop['theIssue'],
          goalRefinements=new_goal_refinements,
          subGoalRefinements=new_subgoal_refinements,
          concs=fake_prop['theConcerns'],
          cas=new_concern_assocs,
          gp = gp)
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
    check_required_keys(json_dict, GoalModel.required)
    json_dict['__python_obj__'] = Goal.__module__+'.'+Goal.__name__
    props_list = json_dict.pop('theEnvironmentProperties', [])
    json_dict.pop('theEnvironmentDictionary', None)
    real_props = self.convert_properties(json_dict['theName'],fake_props=props_list)

    new_json_goal = json_serialize(json_dict)
    new_json_goal = json_deserialize(new_json_goal)
    new_json_goal.theEnvironmentProperties = real_props

    if not isinstance(new_json_goal, Goal):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return new_json_goal

  def simplify(self, goal):
    goal.theEnvironmentProperties = self.convert_properties(goal.theName,real_props=goal.theEnvironmentProperties)
    assert isinstance(goal, Goal)
    del goal.theId
    del goal.theEnvironmentDictionary
    del goal.theColour
    return goal

  def get_goal_names(self, environment='', pathValues = []):
    try:
      goal_names = self.db_proxy.getDimensionNames('goal', environment)
      return goal_names
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_goal_concerns(self,goal,environment,pathValues = []):
    try:
      goalId = self.db_proxy.getDimensionId(goal,'goal')
      envId = self.db_proxy.getDimensionId(environment,'environment')
      return self.db_proxy.goalConcerns(goalId,envId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
