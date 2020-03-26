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
from cairis.core.TemplateGoal import TemplateGoal
from cairis.core.TemplateGoalParameters import TemplateGoalParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import TemplateGoalModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class TemplateGoalDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'template_goal')

  def get_objects(self,constraint_id = -1):
    try:
      tgs = self.db_proxy.getTemplateGoals(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    tgList = []

    for key in tgs:
      tg = tgs[key]
      del tg.theId
      tgList.append(tg)
    return tgList

  def get_object_by_name(self, template_goal_name):
    try:
      found_tg = None
      tgId = self.db_proxy.getDimensionId(template_goal_name,'template_goal')
      tgs = self.db_proxy.getTemplateGoals(tgId)
      if tgs is not None:
        found_tg = tgs.get(template_goal_name)
      if found_tg is None:
        self.close()
        raise ObjectNotFoundHTTPError('The provided template goal')
      del found_tg.theId
      return found_tg
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided template goal')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, tg):
    tgParams = TemplateGoalParameters(
      goalName=tg.theName,
      goalDef=tg.theDefinition,
      goalRat=tg.theRationale,
      goalConcerns=tg.theConcerns,
      goalResp=tg.theResponsibilities)
    try:
      self.db_proxy.addTemplateGoal(tgParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self,tg,name):
    tgParams = TemplateGoalParameters(
      goalName=tg.theName,
      goalDef=tg.theDefinition,
      goalRat=tg.theRationale,
      goalConcerns=tg.theConcerns,
      goalResp=tg.theResponsibilities)

    try:
      tgId = self.db_proxy.getDimensionId(name,'template_goal')
      tgParams.setId(tgId)
      self.db_proxy.updateTemplateGoal(tgParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      tgId = self.db_proxy.getDimensionId(name,'template_goal')
      self.db_proxy.deleteTemplateGoal(tgId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TemplateGoalModel.required)
    json_dict['__python_obj__'] = TemplateGoal.__module__+'.'+ TemplateGoal.__name__
    tg = json_serialize(json_dict)
    tg = json_deserialize(tg)

    if isinstance(tg, TemplateGoal):
      return tg
    else:
      self.close()
      raise MalformedJSONHTTPError()
