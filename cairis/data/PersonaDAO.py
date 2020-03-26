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
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.Persona import Persona
from cairis.core.PersonaParameters import PersonaParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import PersonaModel, PersonaEnvironmentPropertiesModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.misc.AssumptionPersonaModel import AssumptionPersonaModel

__author__ = 'Shamal Faily'


class PersonaDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'persona')

  def get_objects(self, constraint_id=-1, simplify=True):
    try:
      personas = self.db_proxy.getPersonas(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in list(personas.items()):
        personas[key] = self.simplify(value)

    return personas

  def get_objects_summary(self):
    try:
      ps = self.db_proxy.getPersonasSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return ps

  def get_persona_names(self,pathValues = []):
    try:
      persona_names = self.db_proxy.getDimensionNames('persona')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return persona_names


  def get_object_by_name(self, name, simplify=True):
    try:
      personaId = self.db_proxy.getDimensionId(name,'persona')
      personas = self.db_proxy.getPersonas(personaId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    found_persona = personas.get(name, None)

    if found_persona is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided persona name')

    found_persona = self.simplify(found_persona)
    return found_persona

  def add_object(self, persona):
    persona_params = PersonaParameters(
      name=persona.name(),
      activities=persona.activities(),
      attitudes=persona.attitudes(),
      aptitudes=persona.aptitudes(),
      motivations=persona.motivations(),
      skills=persona.skills(),
      intrinsic=persona.intrinsic(),
      contextual=persona.contextual(),
      image=persona.image(),
      isAssumption=persona.assumption(),
      pType=persona.type(),
      tags=persona.tags(),
      properties=persona.environmentProperties(),
      pCodes=[]
    )

    try:
      if not self.check_existing_persona(persona.name()):
        self.db_proxy.addPersona(persona_params)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=persona.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, persona, name):
    persona_params = PersonaParameters(
      name=persona.name(),
      activities=persona.activities(),
      attitudes=persona.attitudes(),
      aptitudes=persona.aptitudes(),
      motivations=persona.motivations(),
      skills=persona.skills(),
      intrinsic=persona.intrinsic(),
      contextual=persona.contextual(),
      image=persona.image(),
      isAssumption=persona.assumption(),
      pType=persona.type(),
      tags=persona.tags(),
      properties=persona.environmentProperties(),
      pCodes=[]
    )
    try:
      personaId = self.db_proxy.getDimensionId(name,'persona')
      persona_params.setId(personaId)
      self.db_proxy.updatePersona(persona_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      personaId = self.db_proxy.getDimensionId(name,'persona')
      self.db_proxy.deletePersona(personaId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_persona(self, name):
    try:
      self.db_proxy.nameCheck(name, 'persona')
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


  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, PersonaModel.required)
    json_dict['__python_obj__'] = Persona.__module__ + '.' + Persona.__name__

    persona_props = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    persona = json_serialize(json_dict)
    persona = json_deserialize(persona)
    persona.theEnvironmentProperties = persona_props
    if not isinstance(persona, Persona):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return persona

  def simplify(self, obj):
    assert isinstance(obj, Persona)
    del obj.theId
    del obj.theEnvironmentDictionary
    del obj.theCodes
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, PersonaEnvironmentProperties)
          del real_prop.theCodes
          new_props.append(real_prop)
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, PersonaEnvironmentPropertiesModel.required)
          new_prop = PersonaEnvironmentProperties(
                       environmentName=fake_prop['theEnvironmentName'],
                       direct=fake_prop['theDirectFlag'],
                       description=fake_prop['theNarrative'],
                       roles=fake_prop['theRoles'],
                       pCodes=[]
                     )
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])
    return new_props

  def get_persona_model(self, persona_name,variable_name,characteristic_name, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    if (variable_name == 'All' or variable_name == 'all'):  
      variable_name = ''
    if (characteristic_name == 'All' or characteristic_name == 'all'): 
      characteristic_name = ''

    try:
      modelAssocs = self.db_proxy.assumptionPersonaModel(persona_name,variable_name,characteristic_name)
      associations = AssumptionPersonaModel(modelAssocs,font_name=fontName,font_size=fontSize)
      dot_code = associations.graph()
      if not dot_code:
        raise ObjectNotFoundHTTPError('The persona model')
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_persona_characteristics(self, persona_name,variable_name,characteristic_name, pathValue = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    if (variable_name == 'All' or variable_name == 'all'):  
      variable_name = ''
    if (characteristic_name == 'All' or characteristic_name == 'all'): 
      characteristic_name = ''

    try:
      modelAssocs = self.db_proxy.assumptionPersonaModel(persona_name,variable_name,characteristic_name)
      associations = AssumptionPersonaModel(modelAssocs,font_name=fontName,font_size=fontSize)
      associations.graph()
      pChars = associations.characteristics()
      return pChars
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_persona_types(self, pathValues = []):
    try:
      pTypes = self.db_proxy.getDimensions('persona_type')
      return pTypes 
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
