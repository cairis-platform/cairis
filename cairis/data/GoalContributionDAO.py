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
from cairis.core.GoalContribution import GoalContribution
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import GoalContributionModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.tools.JsonConverter import json_serialize, json_deserialize
import re

__author__ = 'Shamal Faily'


class GoalContributionDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_objects(self,source = -1, target = -1, pathValues = []):
    try:
      rawObjts = self.db_proxy.getGoalContributionsTable(source,target)
      objts = []
      for objt in rawObjts:
        objts.append(objt)
      if (source != -1 and target != -1):
        return objts[0]
      else:
        return objts
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, gc):
    try:
      self.db_proxy.addReferenceContribution(gc)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self,gc,source,target, pathValues = []):
    try:
      self.db_proxy.deleteGoalContribution(source,target)
      self.db_proxy.addReferenceContribution(gc)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, source, target, pathValues = []):
    try:
      self.db_proxy.deleteGoalContribution(source,target)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, GoalContributionModel.required)
    json_dict['__python_obj__'] = GoalContribution.__module__+'.'+ GoalContribution.__name__
    gc = json_serialize(json_dict)
    gc = json_deserialize(gc)

    if isinstance(gc, GoalContribution):
      return gc
    else:
      self.close()
      raise MalformedJSONHTTPError()
