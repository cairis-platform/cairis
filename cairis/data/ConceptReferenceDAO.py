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
from cairis.core.ConceptReference import ConceptReference
from cairis.core.ConceptReferenceParameters import ConceptReferenceParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import ConceptReferenceModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class ConceptReferenceDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'concept_reference')

  def get_objects(self,constraint_id = -1):
    try:
      crs = self.db_proxy.getConceptReferences(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    crsKeys = sorted(crs.keys())
    crsList = []
    for key in crsKeys:
      cr = crs[key]
      del cr.theId
      crsList.append(cr)
    return crsList

  def get_object_by_name(self, concept_reference_name):
    try:
      crId = self.db_proxy.getDimensionId(concept_reference_name,'concept_reference')
      crs = self.db_proxy.getConceptReferences(crId)
      found_cr = crs.get(concept_reference_name, None)
      if found_cr is None:
        self.close()
        raise ObjectNotFoundHTTPError('The provided concept reference name')
      del found_cr.theId
      return found_cr
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided concept reference name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, cr):
    crParams = ConceptReferenceParameters(
      refName=cr.theName,
      dimName=cr.theDimName,
      objtName=cr.theObjtName,
      cDesc=cr.theDescription)
    try:
      self.db_proxy.addConceptReference(crParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,cr,name):
    crParams = ConceptReferenceParameters(
      refName=cr.theName,
      dimName=cr.theDimName,
      objtName=cr.theObjtName,
      cDesc=cr.theDescription)
    try:
      crId = self.db_proxy.getDimensionId(name,'concept_reference')
      crParams.setId(crId)
      self.db_proxy.updateConceptReference(crParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    cr = self.get_object_by_name(name)
    try:
      crId = self.db_proxy.getDimensionId(name,'concept_reference')
      self.db_proxy.deleteConceptReference(crId,cr.dimension())
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ConceptReferenceModel.required)
    json_dict['__python_obj__'] = ConceptReference.__module__+'.'+ ConceptReference.__name__
    cr = json_serialize(json_dict)
    cr = json_deserialize(cr)

    if isinstance(cr, ConceptReference):
      return cr
    else:
      self.close()
      raise MalformedJSONHTTPError()
