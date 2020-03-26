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
from cairis.core.DocumentReference import DocumentReference
from cairis.core.DocumentReferenceParameters import DocumentReferenceParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import DocumentReferenceModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize
import re

__author__ = 'Shamal Faily'


class DocumentReferenceDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'document_reference')

  def get_objects(self,constraint_id = -1):
    try:
      drs = self.db_proxy.getDocumentReferences(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    drsKeys = sorted(drs.keys())
    drsList = []
    for key in drsKeys:
      dr = drs[key]
      del dr.theId
      drsList.append(dr)
    return drsList

  def get_object_by_name(self, document_reference_name):
    drs = self.get_objects()
    if drs is None or len(drs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('External Documents')
    for dr in drs:
      if (dr.name() == document_reference_name):
        return dr 
    self.close()
    raise ObjectNotFoundHTTPError('The provided document reference parameters')

  def add_object(self, dr):
    drParams = DocumentReferenceParameters(
      refName=dr.theName,
      docName=dr.theDocName,
      cName=dr.theContributor,
      docExc=dr.theExcerpt)
    try:
      self.db_proxy.addDocumentReference(drParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,dr,name):
    drParams = DocumentReferenceParameters(
      refName=dr.theName,
      docName=dr.theDocName,
      cName=dr.theContributor,
      docExc=dr.theExcerpt)
    try:
      drId = self.db_proxy.getDimensionId(name,'document_reference')
      drParams.setId(drId)
      self.db_proxy.updateDocumentReference(drParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      drId = self.db_proxy.getDimensionId(name,'document_reference')
      self.db_proxy.deleteDocumentReference(drId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, DocumentReferenceModel.required)
    json_dict['__python_obj__'] = DocumentReference.__module__+'.'+ DocumentReference.__name__
    dr = json_serialize(json_dict)
    dr = json_deserialize(dr)

    if isinstance(dr, DocumentReference):
      return dr
    else:
      self.close()
      raise MalformedJSONHTTPError()
