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
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.Attacker import Attacker
from cairis.core.AttackerParameters import AttackerParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import AttackerModel, AttackerEnvironmentPropertiesModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin, Shamal Faily'


class AttackerDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'attacker')

  def get_objects(self, constraint_id=-1, simplify=True):
    try:
      attackers = self.db_proxy.getAttackers(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in list(attackers.items()):
        attackers[key] = self.simplify(value)

    return attackers

  def get_objects_summary(self):
    try:
      ats = self.db_proxy.getAttackersSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return ats

  def get_object_by_name(self, name, simplify=True):
    attackers = self.get_objects(simplify=simplify)
    found_attacker = attackers.get(name, None)

    if found_attacker is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided attacker name')

    return found_attacker

  def add_object(self, attacker):
    attacker_params = AttackerParameters(
      name=attacker.theName,
      desc=attacker.theDescription,
      image=attacker.theImage,
      tags=attacker.theTags,
      properties=attacker.theEnvironmentProperties
    )

    try:
      if not self.check_existing_attacker(attacker.theName):
        self.db_proxy.addAttacker(attacker_params)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=attacker.theName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, attacker, name):
    attacker_params = AttackerParameters(
      name=attacker.theName,
      desc=attacker.theDescription,
      image=attacker.theImage,
      tags=attacker.theTags,
      properties=attacker.theEnvironmentProperties
    )

    try:
      attackerId = self.db_proxy.getDimensionId(name,'attacker')
      attacker_params.setId(attackerId)
      self.db_proxy.updateAttacker(attacker_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      attackerId = self.db_proxy.getDimensionId(name,'attacker')
      self.db_proxy.deleteAttacker(attackerId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_attacker(self, name):
    try:
      self.db_proxy.nameCheck(name, 'attacker')
      return False
    except DatabaseProxyException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
      self.close()
      raise ARMHTTPError(ex)

  # region Capabilities
  def get_attacker_capabilities(self, pathValues):
    try:
      environment_name = pathValues[0]
      attacker_capabilities = self.db_proxy.getValueTypes('capability', environment_name)
      return attacker_capabilities
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_attacker_capability_by_name(self, name, environment_name=''):
    found_capability = None
    attacker_capabilities = self.get_attacker_capabilities(environment_name=environment_name)

    if attacker_capabilities is None or len(attacker_capabilities) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Attacker capabilities')

    idx = 0
    while found_capability is None and idx < len(attacker_capabilities):
      if attacker_capabilities[idx].theName == name:
        found_capability = attacker_capabilities[idx]
      idx += 1

    if found_capability is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided attacker capability name')

    return found_capability

  def add_attacker_capability(self, attacker_capability, pathValues):
    assert isinstance(attacker_capability, ValueType)
    environment_name = pathValues[0]
    type_exists = self.check_existing_attacker_capability(attacker_capability.theName, environment_name=environment_name)

    if type_exists:
      self.close()
      raise OverwriteNotAllowedHTTPError(obj_name='The attacker capability')

    params = ValueTypeParameters(
      vtName=attacker_capability.theName,
      vtDesc=attacker_capability.theDescription,
      vType='capability',
      envName=environment_name,
      vtScore=attacker_capability.theScore,
      vtRat=attacker_capability.theRationale
    )

    try:
      return self.db_proxy.addValueType(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_attacker_capability(self, attacker_capability, name, pathValues):
    assert isinstance(attacker_capability, ValueType)
    environment_name = pathValues[0]
    found_capability = self.get_attacker_capability_by_name(name, environment_name)
    params = ValueTypeParameters(
      vtName=attacker_capability.theName,
      vtDesc=attacker_capability.theDescription,
      vType='capability',
      envName=environment_name,
      vtScore=attacker_capability.theScore,
      vtRat=attacker_capability.theRationale
    )
    params.setId(found_capability.theId)

    try:
      self.db_proxy.updateValueType(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_attacker_capability(self, name, pathValues):
    environment_name = pathValues[0]
    found_capability = self.get_attacker_capability_by_name(name, environment_name)
    try:
      self.db_proxy.deleteAssetType(found_capability.theId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_attacker_capability(self, name, environment_name):
    try:
      self.get_attacker_capability_by_name(name, environment_name)
      return True
    except ObjectNotFoundHTTPError:
      self.db_proxy.reconnect(session_id=self.session_id)
      return False
  # endregion

  # region Motivations
  def get_attacker_motivations(self, pathValues):
    try:
      environment_name = pathValues[0]
      attacker_motivations = self.db_proxy.getValueTypes('motivation', environment_name)
      return attacker_motivations
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_attacker_motivation_by_name(self, name, pathValues):
    found_motivation = None
    environment_name = pathValues[0]
    attacker_motivations = self.get_attacker_motivations(environment_name=environment_name)

    if attacker_motivations is None or len(attacker_motivations) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Attacker motivations')

    idx = 0
    while found_motivation is None and idx < len(attacker_motivations):
      if attacker_motivations[idx].theName == name:
        found_motivation = attacker_motivations[idx]
      idx += 1

    if found_motivation is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided attacker motivation name')

    return found_motivation

  def add_attacker_motivation(self, attacker_motivation, pathValues):
    assert isinstance(attacker_motivation, ValueType)
    environment_name = pathValues[0]
    type_exists = self.check_existing_attacker_motivation(attacker_motivation.theName, environment_name=environment_name)

    if type_exists:
      self.close()
      raise OverwriteNotAllowedHTTPError(obj_name='The attacker motivation')

    params = ValueTypeParameters(
      vtName=attacker_motivation.theName,
      vtDesc=attacker_motivation.theDescription,
      vType='motivation',
      envName=environment_name,
      vtScore=attacker_motivation.theScore,
      vtRat=attacker_motivation.theRationale
    )

    try:
      return self.db_proxy.addValueType(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_attacker_motivation(self, attacker_motivation, name, pathValues):
    assert isinstance(attacker_motivation, ValueType)
    environment_name = pathValues[0]
    found_motivation = self.get_attacker_motivation_by_name(name, environment_name)

    params = ValueTypeParameters(
            vtName=attacker_motivation.theName,
            vtDesc=attacker_motivation.theDescription,
            vType='motivation',
            envName=environment_name,
            vtScore=attacker_motivation.theScore,
            vtRat=attacker_motivation.theRationale
    )
    params.setId(found_motivation.theId)

    try:
      self.db_proxy.updateValueType(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_attacker_motivation(self, name):
    environment_name = pathValues[0]
    found_motivation = self.get_attacker_motivation_by_name(name, environment_name)
    try:
      self.db_proxy.deleteAssetType(found_motivation.theId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_attacker_motivation(self, name, environment_name):
    try:
      self.get_attacker_motivation_by_name(name, environment_name)
      return True
    except ObjectNotFoundHTTPError:
      self.db_proxy.reconnect(session_id=self.session_id)
      return False
    # endregion

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, AttackerModel.required)
    json_dict['__python_obj__'] = Attacker.__module__ + '.' + Attacker.__name__

    attacker_props = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    attacker = json_serialize(json_dict)
    attacker = json_deserialize(attacker)
    attacker.theEnvironmentProperties = attacker_props
    if not isinstance(attacker, Attacker):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return attacker

  def simplify(self, obj):
    assert isinstance(obj, Attacker)
    del obj.theEnvironmentDictionary
    del obj.theId
    del obj.isPersona
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, AttackerEnvironmentProperties)
          capabilities = []
          for capability in real_prop.theCapabilities:
            if len(capability) == 2:
              capabilities.append({
                'name': capability[0],
                'value': capability[1]
              })
          real_prop.theCapabilities = capabilities
          new_props.append(real_prop)
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, AttackerEnvironmentPropertiesModel.required)
          cap_list = []
          assert isinstance(cap_list, list)
          for cap in fake_prop['theCapabilities']:
            cap_list.append((cap['name'], cap['value']))
          new_prop = AttackerEnvironmentProperties(
            environmentName=fake_prop['theEnvironmentName'],
            roles=fake_prop['theRoles'],
            motives=fake_prop['theMotives'],
            capabilities=cap_list
          )
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])

    return new_props
