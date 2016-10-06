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
from cairis.core.PersonaCharacteristic import PersonaCharacteristic
from cairis.core.PersonaCharacteristicParameters import PersonaCharacteristicParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import PersonaCharacteristicModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.PseudoClasses import PersonaCharacteristicReference

__author__ = 'Shamal Faily'


class PersonaCharacteristicDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_persona_characteristics(self,constraint_id = -1,simplify=True):
    """
    :rtype: dict[str,PersonaCharacteristic]
    :return
    :raise ARMHTTPError:
    """
    try:
      pcs = self.db_proxy.getPersonaCharacteristics(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in pcs.items():
        pcs[key] = self.convert_pcrs(real_pc=value) 

    return pcs

  def get_persona_characteristic(self, persona_characteristic_name):
    pcs = self.get_persona_characteristics()
    if pcs is None or len(pcs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('External Documents')
    for key in pcs:
      pName,bvName,pcDesc = key.split('/')
      if (pcDesc == persona_characteristic_name):
        pc = pcs[key]
        return pc
    self.close()
    raise ObjectNotFoundHTTPError('Persona characteristic:\"' + persona_characteristic_name + '\"')

  def add_persona_characteristic(self, pc):
    pcParams = PersonaCharacteristicParameters(
      pName=pc.thePersonaName,
      modQual=pc.theModQual,
      vName=pc.theVariable,
      cDesc=pc.theCharacteristic,
      pcGrounds=pc.theGrounds,
      pcWarrant=pc.theWarrant,
      pcBacking=pc.theBacking,
      pcRebuttal=pc.theRebuttal)
    try:
      self.db_proxy.addPersonaCharacteristic(pcParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_persona_characteristic(self,pc,name):
    found_pc = self.get_persona_characteristic(name)
    pcParams = PersonaCharacteristicParameters(
      pName=pc.thePersonaName,
      modQual=pc.theModQual,
      vName=pc.theVariable,
      cDesc=pc.theCharacteristic,
      pcGrounds=pc.theGrounds,
      pcWarrant=pc.theWarrant,
      pcBacking=pc.theBacking,
      pcRebuttal=pc.theRebuttal)
    pcParams.setId(found_pc.theId)
    try:
      self.db_proxy.updatePersonaCharacteristic(pcParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_persona_characteristic(self, name):
    pc = self.get_persona_characteristic(name)
    try:
      self.db_proxy.deletePersonaCharacteristic(pc.theId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, PersonaCharacteristicModel.required)
    json_dict['__python_obj__'] = PersonaCharacteristic.__module__+'.'+ PersonaCharacteristic.__name__
    pc = json_serialize(json_dict)
    pc = json_deserialize(pc)
    pc = self.convert_pcrs(fake_pc=pc)

    if isinstance(pc, PersonaCharacteristic):
      return pc
    else:
      self.close()
      raise MalformedJSONHTTPError()

  def convert_pcrs(self,real_pc=None,fake_pc=None):
    if real_pc is not None:
      assert isinstance(real_pc,PersonaCharacteristic)
      pcr_list = []
      if len(real_pc.theGrounds) > 0:
        for real_pcr in real_pc.theGrounds:
          pcr_list.append(PersonaCharacteristicReference(real_pcr[0],'grounds',real_pcr[1],real_pcr[2]))
        real_pc.theGrounds = pcr_list
        pcr_list = []
        for real_pcr in real_pc.theWarrant:
          pcr_list.append(PersonaCharacteristicReference(real_pcr[0],'warrant',real_pcr[1],real_pcr[2]))
        real_pc.theWarrant = pcr_list
        pcr_list = []
        for real_pcr in real_pc.theRebuttal:
          pcr_list.append(PersonaCharacteristicReference(real_pcr[0],'rebuttal',real_pcr[1],real_pcr[2]))
        real_pc.theRebuttal = pcr_list
      return real_pc 
    elif fake_pc is not None:
      pcr_list = []
      if len(fake_pc.theGrounds) > 0:
        for pcr in fake_pc.theGrounds:
          check_required_keys(pcr,PersonaCharacteristicReference.required)
          pcr_list.append((pcr['theReferenceName'],pcr['theReferenceDescription'],pcr['theDimensionName']))
        fake_pc.theGrounds = pcr_list
      if len(fake_pc.theWarrant) > 0:
        pcr_list = []
        for pcr in fake_pc.theWarrant:
          check_required_keys(pcr,PersonaCharacteristicReference.required)
          pcr_list.append((pcr['theReferenceName'],pcr['theReferenceDescription'],pcr['theDimensionName']))
        fake_pc.theWarrant = pcr_list
      if len(fake_pc.theRebuttal) > 0:
        pcr_list = []
        for pcr in fake_pc.theRebuttal:
          check_required_keys(pcr,PersonaCharacteristicReference.required)
          pcr_list.append((pcr['theReferenceName'],pcr['theReferenceDescription'],pcr['theDimensionName']))
        fake_pc.theRebuttal = pcr_list
      return fake_pc
