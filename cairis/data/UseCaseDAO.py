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
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.UseCase import UseCase
from cairis.core.Steps import Steps
from cairis.core.Step import Step
from cairis.core.UseCaseParameters import UseCaseParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import UseCaseModel, UseCaseEnvironmentPropertiesModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.tools.PseudoClasses import StepAttributes, StepsAttributes 

__author__ = 'Shamal Faily'


class UseCaseDAO(CairisDAO):

  def __init__(self, session_id):
    """
    :raise CairisHTTPError:
    """
    CairisDAO.__init__(self, session_id)

  def get_usecases(self, constraint_id=-1, simplify=True):
    """
    :rtype: dict[str,UseCase]
    :return
    :raise ARMHTTPError:
    """
    try:
      usecases = self.db_proxy.getUseCases(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if simplify:
      for key, value in usecases.items():
        usecases[key] = self.simplify(value)

    return usecases

  def get_usecase_by_name(self, name, simplify=True):
    """
    :rtype: UseCase
    :raise ObjectNotFoundHTTPError:
    """
    usecases = self.get_usecases(simplify=simplify)
    found_usecase = usecases.get(name, None)

    if found_usecase is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided usecase name')

    return found_usecase

  def add_usecase(self, usecase):
    """
    :type usecase: UseCase
    :rtype: int
    :raise ARMHTTPError:
    """
    usecase_params = UseCaseParameters(
      ucName=usecase.name(),
      ucAuth=usecase.author(),
      ucCode=usecase.code(),
      ucActors=usecase.actors(),
      ucDesc=usecase.description(),
      tags=usecase.tags(),
      cProps=usecase.environmentProperties()
    )

    try:
      if not self.check_existing_usecase(usecase.name()):
        new_id = self.db_proxy.addUseCase(usecase_params)
        return new_id
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=usecase.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_usecase(self, usecase, name):
    found_usecase = self.get_usecase_by_name(name, simplify=False)
    usecase_params = UseCaseParameters(
      ucName=usecase.name(),
      ucAuth=usecase.author(),
      ucCode=usecase.code(),
      ucActors=usecase.actors(),
      ucDesc=usecase.description(),
      tags=usecase.tags(),
      cProps=usecase.environmentProperties()
    )
    usecase_params.setId(found_usecase.id())

    try:
      self.db_proxy.updateUseCase(usecase_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_usecase(self, name):
    found_usecase = self.get_usecase_by_name(name, simplify=False)
    usecase_id = found_usecase.id()

    try:
      self.db_proxy.deleteUseCase(usecase_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_usecase(self, name):
    """
    :rtype: bool
    :raise: ARMHTTPError
    """
    try:
      self.db_proxy.nameCheck(name, 'usecase')
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
    """
    :rtype : UseCase
    :raise MalformedJSONHTTPError:
    """
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, UseCaseModel.required)
    json_dict['__python_obj__'] = UseCase.__module__ + '.' + UseCase.__name__

    usecase_props = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    usecase = json_serialize(json_dict)
    usecase = json_deserialize(usecase)
    usecase.theEnvironmentProperties = usecase_props
    if not isinstance(usecase, UseCase):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return usecase

  def simplify(self, obj):
    assert isinstance(obj, UseCase)
    obj.theEnvironmentDictionary = {}

    delattr(obj, 'theEnvironmentDictionary')
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, UseCaseEnvironmentProperties)
          s = Steps()
          for step in real_prop.steps().theSteps:
            s.append((step.text(),step.synopsis(),step.actor(),step.actorType(),step.tags())) 
          real_prop.theSteps = s
          new_props.append(real_prop)
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, UseCaseEnvironmentPropertiesModel.required)
          stepList = [] 
          for s in fake_prop['theSteps']:
            ptList.append([s['theStepText'],s['theSynopsis'],s['theActor'],s['theActorType'],s['theTags']]) 
          fake_prop['theSteps'] = stepList
          
          new_prop = UseCaseEnvironmentProperties(
                       environmentName=fake_prop['theEnvironmentName'],
                       preconds=fake_prop['thePreCond'],
                       steps=fake_prop['theSteps'],
                       postconds=fake_prop['thePostConds']
                     )
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])
    return new_props
