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
from cairis.daemon.CairisHTTPError import CairisHTTPError, ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.UseCase import UseCase
from cairis.core.Steps import Steps
from cairis.core.Step import Step
from cairis.core.UseCaseParameters import UseCaseParameters
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.ReferenceContribution import ReferenceContribution
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import UseCaseModel, UseCaseEnvironmentPropertiesModel, UseCaseContributionModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.tools.PseudoClasses import StepAttributes, StepsAttributes, ExceptionAttributes, CharacteristicReferenceContribution
import http.client

__author__ = 'Shamal Faily'


class UseCaseDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'usecase')

  def get_objects(self, constraint_id=-1, simplify=True):
    try:
      usecases = self.db_proxy.getUseCases(constraint_id)
      if simplify:
        for key, value in list(usecases.items()):
          uc = self.simplify(value)
          uc.theReferenceContributions = []
          contribs = self.db_proxy.getUseCaseContributions(uc.name())
          for rsName in contribs: 
            rrc,rsType = contribs[rsName]
            frc = CharacteristicReferenceContribution(rrc.meansEnd(),rrc.contribution())
            uc.theReferenceContributions.append(UseCaseContributionModel(rsName,frc))
          usecases[key] = uc
      return usecases
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_objects_summary(self):
    try:
      ucs = self.db_proxy.getUseCasesSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return ucs

  def get_object_by_name(self, name, simplify=True):
    try:
      ucId = self.db_proxy.getDimensionId(name,'usecase')
      ucs = self.db_proxy.getUseCases(ucId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if ucs is not None:
      found_uc = ucs.get(name)

    if found_uc is None:
      self.close()
      raise ObjectNotFoundHTTPError(obj='The provided usecase name')

    found_uc = self.simplify(found_uc)
    found_uc.theReferenceContributions = []
    contribs = self.db_proxy.getUseCaseContributions(found_uc.name())
    for rsName in contribs: 
      rrc,rsType = contribs[rsName]
      frc = CharacteristicReferenceContribution(rrc.meansEnd(),rrc.contribution())
      found_uc.theReferenceContributions.append(UseCaseContributionModel(rsName,frc))
    return found_uc


  def add_object(self, usecase):
    usecase_params = UseCaseParameters(
      ucName=usecase.name(),
      ucAuth=usecase.author(),
      ucCode=usecase.code(),
      ucActors=usecase.actors(),
      ucDesc=usecase.description(),
      tags=usecase.tags(),
      cProps=usecase.environmentProperties()
    )

    for envProp in usecase.environmentProperties():
      for step in envProp.steps():
        for exc in step.exceptions():
          self.db_proxy.nameCheck(exc[0],'obstacle')

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

  def update_object(self, usecase, name):
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
      ucId = self.db_proxy.getDimensionId(name,'usecase')
      if (self.db_proxy.exceptionRootObstacles(ucId) > 0):
        raise CairisHTTPError(status_code=http.client.BAD_REQUEST,status="Exception has root obstacles",message="Cannot update use case while use case exception obstacles are connected to other obstacles, goals, requirements, or domain properties.")
      usecase_params.setId(ucId)
      self.db_proxy.updateUseCase(usecase_params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      ucId = self.db_proxy.getDimensionId(name,'usecase')
      self.db_proxy.deleteUseCase(ucId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_usecase_requirements(self, name, pathValues = []):
    try:
      return self.db_proxy.getUseCaseRequirements(name)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_usecase_goals(self, goal_name,environment_name, pathValues = []):
    try:
      return self.db_proxy.getUseCaseGoals(goal_name,environment_name)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    
  def check_existing_usecase(self, name):
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
      frcs = json_dict['theReferenceContributions']
      refContribs = []
      for frc in frcs:
        refContribs.append(ReferenceContribution(usecase.theName,frc['theContributionTo'],frc['theReferenceContribution']['theMeansEnd'],frc['theReferenceContribution']['theContribution']))
      return usecase,refContribs

  def simplify(self, obj):
    assert isinstance(obj, UseCase)
    del obj.theId
    del obj.theEnvironmentDictionary
    obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties)
    return obj

  def convert_props(self, real_props=None, fake_props=None):
    new_props = []
    if real_props is not None:
      if len(real_props) > 0:
        for real_prop in real_props:
          assert isinstance(real_prop, UseCaseEnvironmentProperties)
          s = []
          for step in real_prop.steps().theSteps:
            excs = []
            for excKey in step.exceptions():
              exc = step.exception(excKey)
              excs.append(ExceptionAttributes(exc[0],exc[1],exc[2],exc[3],exc[4]))
            s.append(StepAttributes(step.text(),step.synopsis(),step.actor(),step.actorType(),excs)) 
          real_prop.theSteps = s
          new_props.append(real_prop)
    elif fake_props is not None:
      if len(fake_props) > 0:
        for fake_prop in fake_props:
          check_required_keys(fake_prop, UseCaseEnvironmentPropertiesModel.required)
          steps = Steps()
          for fs in fake_prop['theSteps']:
            aStep = Step(fs['theStepText'],fs['theSynopsis'],fs['theActor'],fs['theActorType'],[])
            for exc in fs['theExceptions']:
              aStep.addException((exc['theName'],exc['theDimensionType'],exc['theDimensionValue'],exc['theCategoryName'],exc['theDescription']))
            steps.append(aStep)
          fake_prop['theSteps'] = steps
          
          new_prop = UseCaseEnvironmentProperties(
                       environmentName=fake_prop['theEnvironmentName'],
                       preCond=fake_prop['thePreCond'],
                       steps=fake_prop['theSteps'],
                       postCond=fake_prop['thePostCond']
                     )
          new_props.append(new_prop)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['real_props', 'fake_props'])
    return new_props

  def assign_usecase_contribution(self,rc):
    if (self.db_proxy.hasContribution('usecase',rc.source(),rc.destination())):
      self.db_proxy.updateUseCaseContribution(rc)
    else:
      self.db_proxy.addUseCaseContribution(rc)

  def remove_usecase_contributions(self,uc):
    try:
      ucId = self.db_proxy.getDimensionId(uc.theName,'usecase')
      self.db_proxy.removeUseCaseContributions(ucId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
