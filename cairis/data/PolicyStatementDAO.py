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
from cairis.core.PolicyStatement import PolicyStatement
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import PolicyStatementModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class PolicyStatementDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'policy_statement')

  def get_objects(self,constraint_id = -1):
    try:
      objts = self.db_proxy.getPolicyStatements(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    sObjts = []
    for objt in objts:
      del objt.theId
      sObjts.append(objt)
    return sObjts

  def get_object_by_name(self, goal_name, env_name,subject,access_type,resource,pathValues = []):
    psId = self.db_proxy.getDimensionId(goal_name + '/' + env_name + '/' + subject + '/' + access_type + '/' + resource,'policy_statement')
    objts = self.get_objects(psId)
    if len(objts) == 0:
      self.close()
      raise ObjectNotFoundHTTPError('The provided policy statement')
    return objts[0]

  def check_existing_policy_statement(self, ps):
    try:
      self.db_proxy.nameCheck(ps.goal() + '/' + ps.environment() + '/' + ps.subject() + '/' + ps.accessType() + '/' + ps.resource(),'policy_statement')
      return False
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, ps):
    try:
      self.db_proxy.addPolicyStatement(ps)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self, ps, goal_name, env_name,subject,access_type,resource, pathValues=[]):
    psParams = PolicyStatement(-1,ps.theGoalName,ps.theEnvironmentName,ps.theSubject,ps.theAccessType,ps.theResource,ps.thePermission)
    if (env_name == ps.theEnvironmentName) and (ps.theSubject != subject or ps.theAccessType != access_type or ps.theResource != resource):
      if(self.db_proxy.nameExists(ps.name(),'policy_statement')):
        raise ARMException('Policy statement for ' + ps.name() + ' already exists.')
    try:
      psId = self.db_proxy.getDimensionId(goal_name + '/' + env_name + '/' + subject + '/' + access_type + '/' + resource,'policy_statement')
      psParams.theId = psId
      self.db_proxy.updatePolicyStatement(psParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, goal_name, env_name,subject,access_type,resource, pathValues = []):
    try:
      psId = self.db_proxy.getDimensionId(goal_name + '/' + env_name + '/' + subject + '/' + access_type + '/' + resource,'policy_statement')
      self.db_proxy.deletePolicyStatement(psId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, PolicyStatementModel.required)
    json_dict['__python_obj__'] = PolicyStatement.__module__+'.'+ PolicyStatement.__name__
    ps = json_serialize(json_dict)
    ps = json_deserialize(ps)

    if isinstance(ps, PolicyStatement):
      return ps
    else:
      self.close()
      raise MalformedJSONHTTPError()
