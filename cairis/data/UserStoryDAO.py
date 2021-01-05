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
from cairis.core.UserStory import UserStory
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import UserStoryModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class UserStoryDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'userstory')

  def get_objects(self,constraint_id = -1):
    try:
      uss = self.db_proxy.getUserStories(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    simplifiedList = []  
    for us in uss:
      del us.theId
      simplifiedList.append(us)
    return simplifiedList

  def get_object_by_name(self, name):
    usId = self.db_proxy.getDimensionId(name,'userstory')
    uss = self.db_proxy.getUserStories(usId)

    if (len(uss) < 1):
      self.close()
      raise ObjectNotFoundHTTPError('User story')

    found_us = uss[0]
    del found_us.theId
    return found_us

  def add_object(self, objt):
    try:
      self.db_proxy.addUserStory(objt)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,objt,name):
    try:
      usId = self.db_proxy.getDimensionId(name,'userstory')
      objt.theId = usId
      self.db_proxy.updateUserStory(objt)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      usId = self.db_proxy.getDimensionId(name,'userstory')
      self.db_proxy.deleteUserStory(usId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, UserStoryModel.required)
    json_dict['__python_obj__'] = UserStory.__module__+'.'+ UserStory.__name__
    us = json_serialize(json_dict)
    us = json_deserialize(us)

    if isinstance(us, UserStory):
      return us
    else:
      self.close()
      raise MalformedJSONHTTPError()
