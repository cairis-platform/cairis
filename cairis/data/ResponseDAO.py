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
from cairis.core.AcceptEnvironmentProperties import AcceptEnvironmentProperties
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, OverwriteNotAllowedHTTPError
from cairis.core.MitigateEnvironmentProperties import MitigateEnvironmentProperties
from cairis.core.ResponseParameters import ResponseParameters
from cairis.core.TransferEnvironmentProperties import TransferEnvironmentProperties
from cairis.data.CairisDAO import CairisDAO
from cairis.core.Response import Response
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import ResponseModel, ResponseEnvironmentPropertiesModel, AcceptEnvironmentPropertiesModel, \
    MitigateEnvironmentPropertiesModel, TransferEnvironmentPropertiesModel
from cairis.tools.PseudoClasses import ValuedRole
from cairis.tools.SessionValidator import check_required_keys
import cairis.core.GoalFactory

__author__ = 'Robin Quetin, Shamal Faily'


class ResponseDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'response')

  def get_objects(self, constraint_id=-1):
    try:
      responses = self.db_proxy.getResponses(constraintId=constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    respKeys = sorted(responses.keys())
    respList = []
    for key in respKeys:
      respList.append(self.simplify(responses[key]))
    return respList

  def get_object_by_name(self, response_name):
    respId = self.db_proxy.getDimensionId(response_name,'response')
    responses = self.db_proxy.getResponses(respId)
    found_response = responses.get(response_name, None)

    if not found_response:
      self.close()
      raise ObjectNotFoundHTTPError(obj='The provided response name')
    return self.simplify(found_response)

  def delete_object(self, response_name):
    try:
      respId = self.db_proxy.getDimensionId(response_name,'response')
      self.db_proxy.deleteResponse(respId)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided response name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, response):
    if self.check_existing_response(response.theName):
      self.close()
      raise OverwriteNotAllowedHTTPError('The provided response name')

    params = ResponseParameters(
            respName=response.theName,
            respRisk=response.theRisk,
            tags=response.theTags,
            cProps=response.theEnvironmentProperties,
            rType=response.theResponseType
    )

    try:
      self.db_proxy.addResponse(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, response, resp_name):
    params = ResponseParameters(
            respName=response.theName,
            respRisk=response.theRisk,
            tags=response.theTags,
            cProps=response.theEnvironmentProperties,
            rType=response.theResponseType
    )
    try:
      respId = self.db_proxy.getDimensionId(resp_name,'response')
      params.setId(respId)
      self.db_proxy.updateResponse(params)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided response name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_response(self, risk_name):
    try:
      self.get_object_by_name(risk_name)
      return True
    except ObjectNotFound as ex:
      return False
    except ObjectNotFoundHTTPError:
      self.db_proxy.reconnect(session_id=self.session_id)
      return False

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ResponseModel.required)
    json_dict['__python_obj__'] = Response.__module__+'.'+Response.__name__

    property_dict = json_dict['theEnvironmentProperties']
    try:
      real_props = self.convert_props(fake_props=property_dict, response_type=json_dict['theResponseType'])
      json_dict['theEnvironmentProperties'] = real_props

      json_resp = json_serialize(json_dict)
      response = json_deserialize(json_resp)

      if isinstance(response, Response):
        return response
      else:
        raise MalformedJSONHTTPError()
    except MalformedJSONHTTPError as ex:
      self.close()
      raise ex

  def convert_props(self, real_props=None, fake_props=None, response_type=None):
    response_type = response_type.lower()

    if real_props:
      if response_type in ('prevent','detect','deter','react'):
        response_type = 'mitigate'
      new_props_list = []
      for idx in range(0, len(real_props)):
        real_prop = real_props[idx]
        
        if isinstance(real_prop, AcceptEnvironmentProperties) and response_type == 'accept':
          new_props_list.append(real_prop)
        elif isinstance(real_prop, MitigateEnvironmentProperties) and response_type == 'mitigate':
          new_props_list.append(real_prop)
        elif isinstance(real_prop, TransferEnvironmentProperties) and response_type == 'transfer':
          roles = real_prop.theRoles
          for idx in range(0, len(roles)):
            roles[idx] = ValuedRole(roles[idx][0], roles[idx][1])
          real_prop.theRoles = roles
          new_props_list.append(real_prop)
      new_props = { response_type: new_props_list }
    elif fake_props:
      new_props = []
      if (response_type in ['Prevent','Deter','Detect','React']):
        response_type = 'mitigate'
      if not (response_type in ResponseEnvironmentPropertiesModel.field_names):
        raise MalformedJSONHTTPError()

      if response_type == 'accept':
        model_class = AcceptEnvironmentPropertiesModel
        target_class = AcceptEnvironmentProperties
      elif response_type == 'mitigate':
        model_class = MitigateEnvironmentPropertiesModel
        target_class = MitigateEnvironmentProperties
      elif response_type == 'transfer':
        model_class = TransferEnvironmentPropertiesModel
        target_class = TransferEnvironmentProperties
      else:
        raise MalformedJSONHTTPError()

      for fake_prop_key in fake_props:
        fake_prop_list = fake_props[fake_prop_key]
        if (len(fake_prop_list) > 0):
          for fake_prop in fake_prop_list:
            check_required_keys(fake_prop, model_class.required)
            fake_prop['__python_obj__'] = target_class.__module__+'.'+target_class.__name__
            if target_class is TransferEnvironmentProperties:
              roles = []
              if isinstance(fake_prop['theRoles'], list):
                for role in fake_prop['theRoles']:
                  check_required_keys(role, ValuedRole.required)
                  roles.append((role['roleName'], role['cost']))
              fake_prop['theRoles'] = roles
            new_props.append(fake_prop)
    else:
      self.close()
      raise MalformedJSONHTTPError()

    return new_props

  def simplify(self, obj):
    del obj.theId
    del obj.theEnvironmentDictionary
    del obj.costLookup
    try:
      obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties, response_type=obj.theResponseType)
    except MalformedJSONHTTPError as ex:
      self.close()
      raise ex

    return obj

  def generate_goal(self,responseName, pathValues = []):
    try:
      respId = self.db_proxy.getDimensionId(responseName,'response')
      responses = self.db_proxy.getResponses(respId)
      goalParameters = cairis.core.GoalFactory.build(responses[responseName],self.db_proxy)
      if (goalParameters == None):
        raise ARMException('Error generating a goal. Cannot generate goals from Accept responses')
      riskParameters = goalParameters[0]
      self.db_proxy.nameCheck(riskParameters.name(), 'goal')
      riskGoalId = self.db_proxy.addGoal(riskParameters)
      self.db_proxy.addTrace('response_goal',respId,riskGoalId)
      if (len(goalParameters) > 1):
        threatParameters = goalParameters[1]
        vulnerabilityParameters = goalParameters[2]
        self.db_proxy.addGoal(vulnerabilityParameters)
        self.db_proxy.addGoal(threatParameters)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided object name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
