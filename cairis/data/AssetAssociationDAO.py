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
from cairis.core.ClassAssociation import ClassAssociation
from cairis.core.ClassAssociationParameters import ClassAssociationParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import AssetAssociationModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class AssetAssociationDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_asset_association(self, environment_name, head_name, tail_name, pathValues = []):
    assocs = self.db_proxy.classModel(environment_name)
    if assocs is None or len(assocs) < 1:
      self.close()
      raise ObjectNotFoundHTTPError('Asset Associations')
    for key in assocs:
      envName,headName,tailName = key.split('/')
      if (envName == environment_name) and (((headName == head_name) and (tailName == tail_name)) or ((headName == tail_name) and (tailName == head_name))):
        assoc = assocs[key]
        del assoc.theId
        return assoc 
    self.close()
    raise ObjectNotFoundHTTPError('The provided asset association parameters')

  def get_asset_associations(self, pathValues = []):
    try:
      cas = self.db_proxy.getClassAssociations()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

    assocs = []
    for key in cas:
      ca = cas[key]
      del ca.theId
      del ca.theHeadDim
      del ca.theTailDim
      assocs.append(ca)

    return assocs

  def add_asset_association(self, assoc, pathValues = []):
    assocParams = ClassAssociationParameters(
      envName=assoc.theEnvironmentName,
      headName=assoc.theHeadAsset,
      headDim='asset',
      headNav=assoc.theHeadNavigation,
      headType=assoc.theHeadType,
      headMultiplicity=assoc.theHeadMultiplicity,
      headRole=assoc.theHeadRole,
      tailRole=assoc.theTailRole,
      tailMultiplicity=assoc.theTailMultiplicity,
      tailType=assoc.theTailType,
      tailNav=assoc.theTailNavigation,
      tailDim='asset',
      tailName=assoc.theTailAsset,
      rationale=assoc.theRationale)
    try:
      self.db_proxy.addClassAssociation(assocParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_asset_association(self,assoc,oldEnvName,oldHeadAsset,oldTailAsset,pathValues = []):
    assocParams = ClassAssociationParameters(
      envName=assoc.theEnvironmentName,
      headName=assoc.theHeadAsset,
      headDim='asset',
      headNav=assoc.theHeadNavigation,
      headType=assoc.theHeadType,
      headMultiplicity=assoc.theHeadMultiplicity,
      headRole=assoc.theHeadRole,
      tailRole=assoc.theTailRole,
      tailMultiplicity=assoc.theTailMultiplicity,
      tailType=assoc.theTailType,
      tailNav=assoc.theTailNavigation,
      tailDim='asset',
      tailName=assoc.theTailAsset,
      rationale=assoc.theRationale)
    try:
      if ((assoc.theEnvironmentName != oldEnvName) or (assoc.theHeadAsset != oldHeadAsset) or (assoc.theTailAsset != oldTailAsset)):
        self.db_proxy.checkAssetAssociation(assoc.theEnvironmentName,assoc.theHeadAsset,assoc.theTailAsset)
      caId = self.db_proxy.getDimensionId(oldEnvName + '/' + oldHeadAsset + '/' + oldTailAsset,'classassociation')
      assocParams.setId(caId)
      self.db_proxy.updateClassAssociation(assocParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_asset_association(self, environment_name, head_name, tail_name, pathValues = []):
    try:
      caId = self.db_proxy.getDimensionId(environment_name + '/' + head_name + '/' + tail_name,'classassociation')
      self.db_proxy.deleteClassAssociation(caId)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, AssetAssociationModel.required)
    json_dict['__python_obj__'] = ClassAssociation.__module__+'.'+ClassAssociation.__name__
    assoc = json_serialize(json_dict)
    assoc = json_deserialize(assoc)

    if isinstance(assoc, ClassAssociation):
      return assoc
    else:
      self.close()
      raise MalformedJSONHTTPError()

