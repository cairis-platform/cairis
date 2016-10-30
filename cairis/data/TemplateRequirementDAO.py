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
from cairis.core.TemplateRequirement import TemplateRequirement
from cairis.core.TemplateRequirementParameters import TemplateRequirementParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import TemplateRequirementModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class TemplateRequirementDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_template_requirements(self,constraint_id = -1):
    """
    :rtype: dict[str,TemplateRequirement]
    :return
    :raise ARMHTTPError:
    """
    try:
      trs = self.db_proxy.getTemplateRequirements(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return trs

  def get_template_requirement(self, template_requirement_name):
    trs = self.get_template_requirements()
    if trs is None or len(trs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Template Requirements')
    for key in trs:
      if (key == template_requirement_name):
        tr = trs[key]
        return tr
    self.close()
    raise ObjectNotFoundHTTPError('The provided template requirement parameters')

  def add_template_requirement(self, tr):
    trParams = TemplateRequirementParameters(
      reqName=tr.theName,
      assetName=tr.theAssetName,
      reqType=tr.theType,
      reqDesc=tr.theDescription,
      reqRat=tr.theRationale,
      reqFC=tr.theFitCriterion)
    try:
      self.db_proxy.addTemplateRequirement(trParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_template_requirement(self,tr,name):
    found_tr = self.get_template_requirement(name)
    trParams = TemplateRequirementParameters(
      reqName=tr.theName,
      assetName=tr.theAssetName,
      reqType=tr.theType,
      reqDesc=tr.theDescription,
      reqRat=tr.theRationale,
      reqFC=tr.theFitCriterion)
    trParams.setId(found_tr.theId)
    try:
      self.db_proxy.updateTemplateRequirement(trParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_template_requirement(self, name):
    tr = self.get_template_requirement(name)
    try:
      self.db_proxy.deleteTemplateRequirement(tr.theId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TemplateRequirementModel.required)
    json_dict['__python_obj__'] = TemplateRequirement.__module__+'.'+ TemplateRequirement.__name__
    tr = json_serialize(json_dict)
    tr = json_deserialize(tr)

    if isinstance(tr, TemplateRequirement):
      return tr
    else:
      self.close()
      raise MalformedJSONHTTPError()
