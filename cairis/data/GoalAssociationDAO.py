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
from cairis.core.GoalAssociation import GoalAssociation
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.daemon.CairisHTTPError import CairisHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import GoalAssociationModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize
import http.client 

__author__ = 'Shamal Faily'


class GoalAssociationDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_goal_associations(self, pathValues):
    environment_name = pathValues[0]
    assocs = self.db_proxy.getGoalAssociations(environment_name)
    assocKeys = assocs.keys()
    assocList = []
    for key in assocKeys:
      assoc = assocs[key]
      del assoc.theId
      assocList.append(assoc)
    return assocList

  def get_goal_association(self, environment_name, goal_name, subgoal_name, pathValues = [],deleteId=True):
    try:
      assoc = self.db_proxy.getGoalAssociation(environment_name,goal_name,subgoal_name)
      if (deleteId == True):
        del assoc.theId
      return assoc 
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ValueError as ex:
      self.close()
      raise CairisHTTPError(status_code=http.client.BAD_REQUEST,status="Server error",message='Error unpacking ' + key + ': ' + format(ex))
    except Exception as ex:
      self.close()
      raise CairisHTTPError(status_code=http.client.BAD_REQUEST,status="Server error",message=format(ex))

  def add_goal_association(self, assoc, pathValues = []):
    if (assoc.theGoal == assoc.theSubGoal):
      raise CairisHTTPError(status_code=http.client.BAD_REQUEST,status="Self-refinement error",message='Cannot self-refine ' + assoc.theGoal)

    assocParams = GoalAssociationParameters(
      envName=assoc.theEnvironmentName,
      goalName=assoc.theGoal,
      goalDimName=assoc.theGoalDimension,
      aType=assoc.theAssociationType,
      subGoalName=assoc.theSubGoal,
      subGoalDimName=assoc.theSubGoalDimension,
      alternativeId=assoc.theAlternativeId,
      rationale=assoc.theRationale)

    try:
      self.db_proxy.addGoalAssociation(assocParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_goal_association(self,assoc,environment_name,goal_name,subgoal_name, pathValues = []):
    if (assoc.theGoal == assoc.theSubGoal):
      raise CairisHTTPError(status_code=http.client.BAD_REQUEST,status="Self-refinement error",message='Cannot self-refine ' + assoc.theGoal)

    old_assoc = self.get_goal_association(environment_name,goal_name,subgoal_name,[],False)
    assocId = old_assoc.theId

    assocParams = GoalAssociationParameters(
      envName=assoc.theEnvironmentName,
      goalName=assoc.theGoal,
      goalDimName=assoc.theGoalDimension,
      aType=assoc.theAssociationType,
      subGoalName=assoc.theSubGoal,
      subGoalDimName=assoc.theSubGoalDimension,
      alternativeId=assoc.theAlternativeId,
      rationale=assoc.theRationale)
    assocParams.setId(assocId)
    try:
      self.db_proxy.updateGoalAssociation(assocParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_goal_association(self, environment_name, goal_name, subgoal_name, pathValues = []):
    assoc = self.get_goal_association(environment_name,goal_name,subgoal_name,[],False)
    try:
      self.db_proxy.deleteGoalAssociation(assoc.theId,assoc.theGoalDimension,assoc.theSubGoalDimension)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, GoalAssociationModel.required)
    json_dict['__python_obj__'] = GoalAssociation.__module__+'.'+ GoalAssociation.__name__
    assoc = json_serialize(json_dict)
    assoc = json_deserialize(assoc)

    if isinstance(assoc, GoalAssociation):
      return assoc
    else:
      self.close()
      raise MalformedJSONHTTPError()

