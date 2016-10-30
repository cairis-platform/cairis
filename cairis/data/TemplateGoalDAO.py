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
    CairisDAO.__init__(self, session_id)

  def get_template_goals(self,constraint_id = -1):
    """
    :rtype: dict[str,TemplateGoal]
    :return
    :raise ARMHTTPError:
    """
    try:
      tgs = self.db_proxy.getTemplateGoals(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return tgs

  def get_template_goal(self, template_goal_name):
    tgs = self.get_template_goals()
    if tgs is None or len(tgs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Template Goals')
    for key in tgs:
      if (key == template_goal_name):
        tg = tgs[key]
        return tg
    self.close()
    raise ObjectNotFoundHTTPError('The provided template goal parameters')

  def add_template_goal(self, tg):
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

  def update_template_goal(self,tg,name):
    found_tg = self.get_template_goal(name)
    tgParams = TemplateGoalParameters(
      goalName=tg.theName,
      goalDef=tg.theDefinition,
      goalRat=tg.theRationale,
      goalConcerns=tg.theConcerns,
      goalResp=tg.theResponsibilities)
    tgParams.setId(found_tg.theId)
    try:
      self.db_proxy.updateTemplateGoal(tgParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_template_goal(self, name):
    tg = self.get_template_goal(name)
    try:
      self.db_proxy.deleteTemplateGoal(tg.theId)
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
