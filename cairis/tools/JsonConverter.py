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

from json import dumps, loads

from flask import session, request
from jsonpickle import encode as serialize, set_preferred_backend
from jsonpickle import decode as deserialize

from cairis.core.Asset import Asset
from cairis.core.Borg import Borg
from cairis.core.Environment import Environment
from cairis.core.Goal import Goal
from cairis.core.MisuseCase import MisuseCase
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.Requirement import Requirement
from cairis.core.RiskParameters import RiskParameters
from .ModelDefinitions import AssetEnvironmentPropertiesModel, SecurityAttribute
from six import string_types


__author__ = 'Robin Quetin, Shamal Faily'

conv_terms = {
  'py/object': '__python_obj__',
  'py/id': '__python_id__',
  'py/tuple': '__python_tuple__',
}

def json_serialize(obj, pretty_printing=False, session_id=None):
  """
  Serializes the Python object to a JSON serialized string.
  :param obj: The object to be serialized
  :type obj: object
  :param pretty_printing: Defines if the string needs to be pretty printed
  :type pretty_printing: bool
  :param session_id: The user's session ID
  :type session_id: int
  :return: Returns a JSON serialized string of the object
  """
  b = Borg()
  if session_id is None:
    session_id = session.get('session_id', None)

  s = b.get_settings(session_id)
  if s is not None:
    pretty_printing = s.get('jsonPrettyPrint', False)

  if pretty_printing:
    json_string = dumps(loads(serialize(obj,unpicklable=False)), indent=4)
  else:
    json_string = serialize(obj,unpicklable=False)

  for key in conv_terms:
    json_string = json_string.replace(key, conv_terms[key])

  return json_string

def json_deserialize(string, class_name=None):
  """
  Deserializes the JSON object to the appropriate class instance.
  :param string: The JSON string
  :type string: str
  :param class_name: The name of the target class
  :type class_name: str
  :return: Returns a dictionary or a class instance depending on the target class chosen
  :rtype: list|dict|Asset|Goal|Requirement|Risk
  """
  if isinstance(string, dict) or isinstance(string, list):
    string = json_serialize(string)

  if isinstance(string, list):
    list_result = []
    for item_string in string:
      item_string = json_serialize(item_string)
      for key in conv_terms:
        item_string = item_string.replace(conv_terms[key], key)
      list_result.append(json_deserialize(item_string))

  if isinstance(string, string_types):
    for key in conv_terms:
      string = string.replace(conv_terms[key], key)

  try:
    obj = deserialize(string)
    if isinstance(obj, Environment):
      tensions = {}
      for key, value in list(obj.theTensions.items()):
        key = str(key)
        attrs = key.strip('(').strip(')').split(',')
        if len(attrs) == 2:
          idx1 = int(attrs[0].strip(' '))
          idx2 = int(attrs[1].strip(' '))
          tuple_key = (idx1, idx2)
          tensions[tuple_key] = value

      obj = Environment(
              id=obj.theId,
              name=obj.theName,
              sc=obj.theShortCode,
              description=obj.theDescription,
              environments=obj.theEnvironments,
              duplProperty=obj.theDuplicateProperty,
              overridingEnvironment=obj.theOverridingEnvironment,
              envTensions=tensions
            )

    if isinstance(obj, dict):
      if class_name == 'asset':
        from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError
        raise MalformedJSONHTTPError()
      elif class_name == 'goal':
        obj = deserialize_goal(dict)
      elif class_name == 'requirement':
        obj = deserialize_requirement(dict)

    return obj
  except Exception as ex:
    from cairis.daemon.CairisHTTPError import handle_exception
    handle_exception(ex)

def deserialize_goal(dict):
  goal = Goal(dict['theId'], dict['theName'], dict['theOriginator'], dict['theTags'], dict['theEnvironmentProperties'])
  return goal

def deserialize_requirement(dict):
  req = Requirement(id=-1, label=dict['theLabel'], name=dict['theName'], description=dict['theDescription'], priority=dict['thePriority'], rationale=dict['attrs']['rationale'], fitCriterion=dict['attrs']['fitCriterion'],originator=dict['attrs']['originator'],type=dict['attrs']['type'],asset=dict['attrs']['asset'],version=-1)
  return req

def deserialize_misuse(dict):
  mc_props = []
  for mc_prop in dict['theEnvironmentProperties']:
    new_mc_prop = MisuseCaseEnvironmentProperties().__dict__.update(mc_prop)
    mc_props.append(new_mc_prop)

  return MisuseCaseParameters(scName=dict['theName'], cProps=mc_props, risk=dict['theRisk'])

def deserialize_risk(dict):
  mc_obj = deserialize_misuse(dict['theMisuseCase'])
  return RiskParameters(riskName=dict['theRiskName'], threatName=dict['theThreatName'], vulName=dict['theVulnerabilityName'], rTags=dict['theTags'], mc=mc_obj)
