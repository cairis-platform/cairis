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
from cairis.daemon.CairisHTTPError import ARMHTTPError, MalformedJSONHTTPError, ObjectNotFoundHTTPError, MissingParameterHTTPError
from cairis.core.Environment import Environment
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import EnvironmentModel
from cairis.tools.PseudoClasses import EnvironmentTensionModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin, Shamal Faily'


class EnvironmentDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'environment')

  def get_objects(self, constraint_id=-1):
    try:
      environments = self.db_proxy.getEnvironments(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    envKeys = sorted(environments.keys())
    envList = []
    for key in envKeys:
      value = environments[key]
      envList.append(self.simplify(value))
    return envList

  def get_object_by_name(self, name, simplify=True):
    found_environment = None
    try:
      environments = self.db_proxy.getEnvironments()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if environments is not None:
      found_environment = environments.get(name)

    if found_environment is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided environment name')

    if simplify:
      found_environment = self.simplify(found_environment)

    return found_environment

  def get_environment_names(self,pathValues = []):
    try:
      environment_names = self.db_proxy.getEnvironmentNames()
      return environment_names
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_environment_names_by_vulnerability_threat(self, vulnerability_name, threat_name, pathValues = []):
    return self.get_environment_names_by_threat_vulnerability(threat_name, vulnerability_name, pathValues)

  def get_environment_names_by_threat_vulnerability(self, threat_name, vulnerability_name,  pathValues = []):
    try:
      environments = self.db_proxy.riskEnvironments(threat_name, vulnerability_name)
      return environments
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_environment_names_by_risk(self, risk_name, pathValues = []):
    try:
      environments = self.db_proxy.riskEnvironmentsByRisk(risk_name)
      return environments
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, environment):
    env_params = self.to_environment_parameters(environment)
    try:
      if not self.check_existing_environment(environment.theName):
        self.db_proxy.addEnvironment(env_params)
      else:
        self.close()
        raise DatabaseProxyException('Environment name already exists within the database.')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, environment, name):
    env_params = self.to_environment_parameters(environment)
    try:
      envId = self.db_proxy.getDimensionId(name,'environment')
      env_params.setId(envId)
      self.db_proxy.updateEnvironment(env_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      envId = self.db_proxy.getDimensionId(name,'environment')
      self.db_proxy.deleteEnvironment(envId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_environment(self, environment_name):
    try:
      self.db_proxy.nameCheck(environment_name, 'environment')
      return False
    except DatabaseProxyException as ex:
      if str(ex.value).find(' already exists') > -1:
        return True
      else:
        self.close()
        raise ARMHTTPError(ex)
    except ARMException as ex:
      if str(ex.value).find(' already exists') > -1:
        return True
      else:
        self.close()
        raise ARMHTTPError(ex)

  def to_environment_parameters(self, environment):
    assert isinstance(environment, Environment)
    env_params = EnvironmentParameters(
            conName=environment.theName,
            conSc=environment.theShortCode,
            conDesc=environment.theDescription,
            environments=environment.theEnvironments,
            duplProperty=environment.theDuplicateProperty,
            overridingEnvironment=environment.theOverridingEnvironment,
            envTensions=environment.theTensions
    )
    return env_params

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    assert isinstance(json_dict, dict)
    check_required_keys(json_dict, EnvironmentModel.required)
    json_dict['__python_obj__'] = Environment.__module__+'.'+Environment.__name__

    if 'theTensions' in json_dict:
      assert isinstance(json_dict['theTensions'], list)
      tensions = json_dict['theTensions']
      json_dict['theTensions'] = {}
      for tension in tensions:
        check_required_keys(tension, EnvironmentTensionModel.required)
        key = tuple([tension['base_attr_id'], tension['attr_id']])
        value = tuple([tension['value'], tension['rationale']])
        json_dict['theTensions'][key] = value

    json_dict['theId'] = -1
    new_json_environment = json_serialize(json_dict)
    environment = json_deserialize(new_json_environment)
    if not isinstance(environment, Environment):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return environment

  def simplify(self, obj):
    assert isinstance(obj, Environment)
    del obj.theId
    the_tensions = obj.theTensions
    assert isinstance(the_tensions, dict)
    obj.theTensions = []
    for key, value in list(the_tensions.items()):
      obj.theTensions.append(EnvironmentTensionModel(key=key, value=value))
    return obj
