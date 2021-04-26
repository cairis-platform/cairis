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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, handle_exception, \
    MissingParameterHTTPError
from cairis.core.Requirement import Requirement
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import RequirementModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.misc.ConceptMapModel import ConceptMapModel as GraphicalConceptMapModel

__author__ = 'Robin Quetin, Shamal Faily'

class RequirementDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'requirement')

  def get_requirements_by_asset(self, name, pathValues):
    ordered = pathValues[0]
    constraint_id = name
    assetName  = ''
    environmentName = None
    return self.get_requirements([pathValues[0],constraint_id,assetName,environmentName])

  def get_requirements_by_environment(self, name, pathValues):
    ordered = pathValues[0]
    constraint_id = name
    assetName  = None
    environmentName = ''
    return self.get_requirements([pathValues[0],constraint_id,assetName,environmentName])

  def get_requirements(self, pathValues):
    ordered = pathValues[0]
    constraint_id = pathValues[1]
    asset_name = pathValues[2]
    environment_name = pathValues[3]
    
    ordered = False
    if (ordered == 1):
      ordered = True
    
    is_asset = False
    if ((asset_name == None and environment_name == None) or (asset_name != None)):
      is_asset = True

    try:
      if (constraint_id != ''):
        if (is_asset == True):
          self.db_proxy.getDimensionId(constraint_id,'asset')
        else:
          self.db_proxy.getDimensionId(constraint_id,'environment')
        
      if ordered:
        requirements = self.simplifyList(self.db_proxy.getOrderedRequirements(constraint_id, is_asset))
      else:
        requirements = self.simplifyList((self.db_proxy.getRequirements(constraint_id, is_asset)).values())
      return requirements
    except ObjectNotFound as ex:
      self.close()
      dimName = 'environment'
      if (is_asset == True):
        dimName = 'asset'
      raise ObjectNotFoundHTTPError('The provided ' + dimName + ' name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def simplifyList(self,requirements):
    reqList = []
    for r in requirements:
      reqList.append(self.simplify(r))
    return reqList

  def get_object_by_name(self, name):
    try:
      req = self.db_proxy.getRequirement(name)
      if (req == None):
        self.close()
        raise ObjectNotFoundHTTPError('The provided requirement name ' + name)
      return self.simplify(req)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided requirement name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_requirement(self, requirement, pathValues = []):

    try:
      self.db_proxy.nameCheck(requirement.theName, 'requirement')
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    new_id = self.db_proxy.newId()
    requirement.theId = new_id
    requirement.theVersion = 1

    isAsset = False
    if requirement.domainType() == 'asset':
      isAsset = True 

    try:
      self.db_proxy.addRequirement(requirement, assetName=requirement.domain(), isAsset=isAsset)
    except ARMException as ex:
      self.close()
      handle_exception(ex)


  def delete_object(self, name=None):
    if name is not None:
      req = self.db_proxy.getRequirement(name)
      reqReference = req.domain()
      self.db_proxy.deleteRequirement(req.id())
      self.db_proxy.relabelRequirements(reqReference)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['name'])

  def update_object(self, requirement, name=None):
    old_requirement = None
    old_reference = None
    if name is not None:
      old_requirement = self.db_proxy.getRequirement(name)
      old_reference = old_requirement.domain()
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['theId'])

    if old_requirement is not None:
      try:
        requirement.theVersion = old_requirement.theVersion
        requirement.theId = old_requirement.theId
        requirement.incrementVersion()
        self.db_proxy.updateRequirement(requirement)
        reqReference = requirement.domain()
        if (reqReference != old_reference):
          self.db_proxy.reassociateRequirement(requirement.name(),reqReference)
          self.db_proxy.relabelRequirements(reqReference)
          self.db_proxy.relabelRequirements(old_reference)
      except DatabaseProxyException as ex:
        self.close()
        raise ARMHTTPError(ex)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['id'])

  def from_json(self, request,domain_name=None):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, RequirementModel.required)
    json_dict['__python_obj__'] = Requirement.__module__+'.'+Requirement.__name__
    json_dict['attrs'] = {}
    json_dict['dirtyAttrs'] = {}
    json_dict['theVersion'] = -1
    json_dict['attrs']['originator'] = json_dict['theOriginator']
    json_dict['attrs']['supportingMaterial'] = ''
    json_dict['attrs']['fitCriterion'] = json_dict['theFitCriterion']
     
    if (domain_name != None):
      json_dict['attrs']['asset'] = domain_name
    else:
      json_dict['attrs']['asset'] = json_dict['theDomain']
    json_dict['attrs']['rationale'] = json_dict['theRationale']
    json_dict['attrs']['type'] = json_dict['theType']
    requirement = json_serialize(json_dict)
    requirement = json_deserialize(requirement)
    if not isinstance(requirement, Requirement):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return requirement

  def simplify(self, obj):
    del obj.theId
    del obj.theSupportingMaterial
    del obj.attrs
    del obj.dirtyAttrs
    del obj.theVersion
    return obj

  def get_concept_map_model(self, environment_name, requirement_name, pathValues):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    isAsset = pathValues[0]
    if (isAsset == '1'):
      isAsset = True
    else:
      isAsset = False

    try:
      associationDictionary = self.db_proxy.conceptMapModel(environment_name, requirement_name)
      associations = GraphicalConceptMapModel(list(associationDictionary.values()), environment_name, requirement_name, isAsset, True, db_proxy=self.db_proxy, font_name=fontName, font_size=fontSize)
      dot_code = associations.graph()
      return dot_code
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided environment name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except Exception as ex:
      print(ex)

  def get_environment_requirement_names(self,name, pathValues = []):
    return self.get_dimension_requirement_names('environment',name)

  def get_asset_requirement_names(self,name, pathValues = []):
    return self.get_dimension_requirement_names('asset',name)

  def get_dimension_requirement_names(self, dimName, objtName):
    try:
      return self.db_proxy.dimensionRequirements(dimName,objtName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
