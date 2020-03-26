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
from cairis.daemon.CairisHTTPError import ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, ObjectNotFoundHTTPError
from cairis.core.Role import Role
from cairis.core.RoleEnvironmentProperties import RoleEnvironmentProperties
from cairis.core.RoleParameters import RoleParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import RoleModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin, Shamal Faily'


class RoleDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'role')

  def get_objects(self, constraint_id=-1):
    try:
      roles = self.db_proxy.getRoles(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    roleKeys = sorted(roles.keys())
    roleList = []
    for key in roleKeys:
      roleList.append(self.simplify(roles[key]))
    return roleList

  def get_object_by_name(self, name, simplify=True):
    try:
      roleId = self.db_proxy.getDimensionId(name,'role')
      roles = self.db_proxy.getRoles(roleId)
      found_role = roles.get(name, None)
      if found_role is None:
        self.close()
        raise ObjectNotFoundHTTPError('The provided role name')
      if (simplify == True):
        return self.simplify(found_role)
      else:
        return found_role
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided role name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_role_props(self, name, pathValues = []):
    role = self.get_object_by_name(name, simplify=False)
    props = role.theEnvironmentProperties
    return props


  def add_object(self, role):
    role_params = RoleParameters(
      name=role.theName,
      rType=role.theType,
      sCode=role.theShortCode,
      desc=role.theDescription,
      cProperties=[]
    )
    try:
      self.db_proxy.nameCheck(role.theName, 'role')
      self.db_proxy.addRole(role_params)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, role, name):
    params = RoleParameters(
      name=role.theName,
      rType=role.theType,
      sCode=role.theShortCode,
      desc=role.theDescription,
      cProperties=[]
    )
    try:
      roleId = self.db_proxy.getDimensionId(name,'role')
      params.setId(roleId)
      self.db_proxy.updateRole(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      roleId = self.db_proxy.getDimensionId(name,'role')
      self.db_proxy.deleteRole(roleId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, RoleModel.required)
    json_dict['__python_obj__'] = Role.__module__+'.'+Role.__name__
    role = json_serialize(json_dict)
    role = json_deserialize(role)
    if not isinstance(role, Role):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return role

  def simplify(self, obj):
    del obj.theId
    del obj.costLookup
    del obj.theEnvironmentDictionary
    del obj.theEnvironmentProperties
    return obj
