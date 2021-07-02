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
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from http.client import BAD_REQUEST
from cairis.daemon.CairisHTTPError import CairisHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import ReferenceSynopsisModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.misc.UserGoalModel import UserGoalModel
import re

__author__ = 'Shamal Faily'


class UserGoalDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_object_by_name(self,name):
    return self.get_objects(name)

  def get_objects(self,constraint_id = -1):
    try:
      if (constraint_id != -1):
        constraint_id = self.db_proxy.getDimensionId(constraint_id,'synopsis')
      rawObjts = self.db_proxy.getUserGoals(constraint_id)
      objts = []
      for objt in rawObjts:
        del objt.theId
        objts.append(objt)
      if (constraint_id != -1):
        return objts[0]
      else:
        return objts
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, ug):
    try:
      self.db_proxy.addUserGoal(ug)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,ug,name):
    try:
      ugPCs = self.db_proxy.conflictingPersonaCharacteristics(ug.theActor,name)
      if (len(ugPCs) == 0):
        ugId = self.db_proxy.getDimensionId(name,'synopsis')
        ug.setId(ugId)
        self.db_proxy.updateUserGoal(ug)
      else:
        excTxt = "Can't associate '" + name + "' with " + ug.theActor + " because it is associated with persona characteristic"
        if (len(ugPCs) > 1): 
          excTxt += "s " + ', '.join(ugPCs)
        else:
          excTxt += " " + ugPCs[0]
        raise CairisHTTPError(BAD_REQUEST,excTxt)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      ugId = self.db_proxy.getDimensionId(name,'synopsis')
      self.db_proxy.deleteUserGoal(ugId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ReferenceSynopsisModel.required)
    json_dict['__python_obj__'] = ReferenceSynopsis.__module__+'.'+ ReferenceSynopsis.__name__
    ug = json_serialize(json_dict)
    ug = json_deserialize(ug)

    if isinstance(ug, ReferenceSynopsis):
      return ug
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def get_user_goal_model(self, environment_name, persona_name,filter_element, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    if persona_name == 'all':
      persona_name = ''
    if filter_element == 'all':
      filter_element = ''
    try:
      gcs = self.db_proxy.getGoalContributions(environment_name,persona_name,filter_element)
      ugm = UserGoalModel(gcs,environment_name,self.db_proxy,font_name=fontName, font_size=fontSize)
      dot_code = ugm.graph()
      if not dot_code:
        raise ObjectNotFoundHTTPError('The user goal model')
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def role_user_goals(self,role_name, pathValues = []):
    try:
      return self.db_proxy.roleUserGoals(role_name)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def user_goal_filters(self,environment_name,persona_name, pathValues = []):
    try:
      if persona_name == 'all':
        persona_name = '' 
      return self.db_proxy.userGoalFilters(environment_name,persona_name)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
