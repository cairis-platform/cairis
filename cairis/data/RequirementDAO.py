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
    CairisDAO.__init__(self, session_id)

  def get_requirements(self, constraint_id='', is_asset=True, ordered=False):
    try:
      if ordered:
        requirements = self.db_proxy.getOrderedRequirements(constraint_id, is_asset)
      else:
        requirements = self.db_proxy.getRequirements(constraint_id, is_asset)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    return requirements

  def get_requirement_by_name(self, name):
    found_requirement = None
    try:
      requirements = self.db_proxy.getRequirements()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if requirements is not None:
      idx = 0
      while found_requirement is None and idx < len(requirements):
        if (list(requirements.values())[idx].theName == name) or (list(requirements.values())[idx].theLabel == name):
          found_requirement = list(requirements.values())[idx]
        idx += 1

    if found_requirement is None:
      self.close()
      raise ObjectNotFoundHTTPError('The provided requirement name ' + '"' + name + '"')

    return found_requirement

  def get_requirement_by_shortcode(self, shortcode):
    found_requirement = None
    requirements = list(self.get_requirements().values())
    idx = 0

    while found_requirement is None and idx < len(requirements):
      requirement = requirements[idx]
      if requirement.theLabel == shortcode:
        found_requirement = requirement
      idx +=1

    if found_requirement is None:
      self.close()
      raise ObjectNotFoundHTTPError(obj='The provided requirement shortcode')

    return found_requirement

  def add_requirement(self, requirement, asset_name=None, environment_name=None):
    try:
      self.db_proxy.nameCheck(requirement.theName, 'requirement')
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    new_id = self.db_proxy.newId()
    requirement.theId = new_id
    requirement.theVersion = 1

    if asset_name is not None:
      try:
        self.db_proxy.addRequirement(requirement, assetName=asset_name, isAsset=True)
      except ARMException as ex:
        self.close()
        handle_exception(ex)
    elif environment_name is not None:
      try:
        self.db_proxy.addRequirement(requirement, assetName=environment_name, isAsset=False)
      except ARMException as ex:
        self.close()
        handle_exception(ex)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['requirement', 'environment'])

    return new_id

  def delete_requirement(self, name=None):
    if name is not None:
      req = self.db_proxy.getRequirement(name)
      reqReference = req.asset()
      self.db_proxy.deleteRequirement(req.id())
      self.db_proxy.relabelRequirements(reqReference)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['name'])

  def update_requirement(self, requirement, name=None):
    old_requirement = None
    if name is not None:
      old_requirement = self.db_proxy.getRequirement(name)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['theId'])

    if old_requirement is not None:
      try:
        requirement.theVersion = old_requirement.theVersion
        requirement.theId = old_requirement.theId
        requirement.incrementVersion()
        self.db_proxy.updateRequirement(requirement)
      except DatabaseProxyException as ex:
        self.close()
        raise ARMHTTPError(ex)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['id'])

  def from_json(self, request):
    """
    :rtype Requirement
    """
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, RequirementModel.required)
    json_dict['__python_obj__'] = Requirement.__module__+'.'+Requirement.__name__
    requirement = json_serialize(json_dict)
    requirement = json_deserialize(requirement)
    if not isinstance(requirement, Requirement):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return requirement

  def simplify(self, obj):
    return obj

  def get_concept_map_model(self, environment_name, requirement_name):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    try:
      associationDictionary = self.db_proxy.conceptMapModel(environment_name, requirement_name)
      associations = GraphicalConceptMapModel(list(associationDictionary.values()), environment_name, requirement_name, True, db_proxy=self.db_proxy, font_name=fontName, font_size=fontSize)
      dot_code = associations.graph()
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except Exception as ex:
      print(ex)

