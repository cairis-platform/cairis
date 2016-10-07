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
    CairisDAO.__init__(self, session_id)

  def get_external_documents(self,constraint_id = -1):
    """
    :rtype: dict[str,ExternalDocument]
    :return
    :raise ARMHTTPError:
    """
    try:
      edocs = self.db_proxy.getExternalDocuments(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    return edocs

  def get_external_document(self, external_document_name):
    edocs = self.get_external_documents()
    if edocs is None or len(edocs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('External Documents')
    for key in edocs:
      if (key == external_document_name):
        edoc = edocs[key]
        return edoc
    self.close()
    raise ObjectNotFoundHTTPError('The provided external document parameters')

  def add_external_document(self, edoc):
    edParams = ExternalDocumentParameters(
      edName=edoc.theName,
      edVersion=edoc.theVersion,
      edDate=edoc.thePublicationDate,
      edAuths=edoc.theAuthors,
      edDesc=edoc.theDescription)
    try:
      self.db_proxy.addExternalDocument(edParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_external_document(self,edoc,name):
    found_edoc = self.get_external_document(name)
    edParams = ExternalDocumentParameters(
      edName=edoc.theName,
      edVersion=edoc.theVersion,
      edDate=edoc.thePublicationDate,
      edAuths=edoc.theAuthors,
      edDesc=edoc.theDescription)
    edParams.setId(found_edoc.theId)
    try:
      self.db_proxy.updateExternalDocument(edParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_external_document(self, name):
    edoc = self.get_external_document(name)
    try:
      self.db_proxy.deleteExternalDocument(edoc.theId)
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
