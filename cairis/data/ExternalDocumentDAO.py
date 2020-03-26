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
from cairis.core.ExternalDocument import ExternalDocument
from cairis.core.ExternalDocumentParameters import ExternalDocumentParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import ExternalDocumentModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class ExternalDocumentDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'external_document')

  def get_objects(self,constraint_id = -1):
    try:
      edocs = self.db_proxy.getExternalDocuments(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    edocsKeys = sorted(edocs.keys())
    edocsList = []  
    for key in edocsKeys:
      edoc = edocs[key]
      del edoc.theId
      edocsList.append(edoc)
    return edocsList

  def get_object_by_name(self, external_document_name):
    edName = external_document_name.replace("\\'","'")
    edocs = self.get_objects()
    if edocs is None or len(edocs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('External Documents')
    for edoc in edocs:
      if (edoc.name() == edName):
        return edoc
    self.close()
    raise ObjectNotFoundHTTPError('The provided external document parameters')

  def add_object(self, edoc):
    edParams = ExternalDocumentParameters(
      edName = edoc.theName.replace("\\'","'"),
      edVersion=edoc.theVersion,
      edDate=edoc.thePublicationDate,
      edAuths=edoc.theAuthors,
      edDesc=edoc.theDescription)
    try:
      self.db_proxy.addExternalDocument(edParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object(self,edoc,name):
    edParams = ExternalDocumentParameters(
      edName=edoc.theName,
      edVersion=edoc.theVersion,
      edDate=edoc.thePublicationDate,
      edAuths=edoc.theAuthors,
      edDesc=edoc.theDescription)
    try:
      edId = self.db_proxy.getDimensionId(name,'external_document')
      edParams.setId(edId)
      self.db_proxy.updateExternalDocument(edParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self, name):
    try:
      edId = self.db_proxy.getDimensionId(name,'external_document')
      self.db_proxy.deleteExternalDocument(edId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ExternalDocumentModel.required)
    json_dict['__python_obj__'] = ExternalDocument.__module__+'.'+ ExternalDocument.__name__
    edoc = json_serialize(json_dict)
    edoc = json_deserialize(edoc)

    if isinstance(edoc, ExternalDocument):
      return edoc
    else:
      self.close()
      raise MalformedJSONHTTPError()
