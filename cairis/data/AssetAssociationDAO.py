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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError
from cairis.core.ClassAssociationParameters import ClassAssociationParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.core.ClassAssociation import ClassAssociation
from cairis.tools.JsonConverter import json_deserialize, json_serialize
from cairis.tools.ModelDefinitions import ClassAssociationModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Shamal Faily'


class AssetAssociationDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_asset_associations(self, constraint_id=''):
    """
    :rtype : dict[str, ClassAssociation]
    """
    try:
      dependencies = self.db_proxy.getClassAssociations(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError

    return dependencies

  def get_class_association(self, environment, head_name, tail_name):
    """
    :type environment: str
    :type head_name: str
    :type tail_name: str
    :rtype : [ClassAssociation]
    """
    args = [environment, head_name, tail_name]
    if not 'all' in args:
      return [self.get_class_association_by_name('/'.join(args))]
    else:
      assocs = self.get_class_associations()
      found_assocs = []

      for key in assocs:
        parts = key.split('/')
        if environment != 'all' and parts[0] != environment:
          continue
        if head_name != 'all' and parts[1] != head_name:
          continue
        if tail_name != 'all' and parts[2] != tail_name:
          continue

        found_assocs.append(assocs[key])

      return found_assocs


  def get_class_association_by_name(self, assoc_name):
    """
    :rtype : ClassAssociation
    """
    assocs = self.get_class_associations()

    found_assoc = assocs.get(assoc_name, None)

    if not found_assoc:
      raise ObjectNotFoundHTTPError('The provided asset association name')
    return found_assoc

  def add_class_association(self, assoc):

    params = ClassAssociationParameters(
      envName=assoc.theEnvironmentName,
      headName=assoc.theHeadAsset,
      headDim=assoc.theHeadDim,
      headNav=assoc.theHeadNavigation,
      headType=assoc.theHeadType,
      headMultiplicity=assoc.theHeadMultiplicity,
      headRole=assoc.theHeadRole,
      tailRole=assoc.theTailRole,
      tailMultiplicity=assoc.theTailMultiplicity,
      tailType=assoc.theTailType,
      tailNav=assoc.theTailNavigation,
      tailDim=assoc.theTailDim,
      tailName=assoc.theTailName,
      rationale=.assoc.theRationale
    )

    try:
      self.db_proxy.addClassAssociation(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_class_associations(self, environment, head_name,tail_name):
    found_dependencies = self.get_dependency(environment, head_name, tail_name)

    try:
      for found_dependency in found_dependencies:
        self.db_proxy.deleteClassAssociation(
          found_dependency.theId
        )
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_class_association(self, environment, head_name, tail_name):
    assoc_name = '/'.join([environment, head_name, tail_name])
    found_assoc = self.get_class_association_by_name(assoc_name)

    params = ClassAssociationParameters(
      envName=assoc.theEnvironmentName,
      headName=assoc.theHeadAsset,
      headDim=assoc.theHeadDim,
      headNav=assoc.theHeadNavigation,
      headType=assoc.theHeadType,
      headMultiplicity=assoc.theHeadMultiplicity,
      headRole=assoc.theHeadRole,
      tailRole=assoc.theTailRole,
      tailMultiplicity=assoc.theTailMultiplicity,
      tailType=assoc.theTailType,
      tailNav=assoc.theTailNavigation,
      tailDim=assoc.theTailDim,
      tailName=assoc.theTailName,
      rationale=.assoc.theRationale
    )
    params.setId(found_assoc.theId)

    try:
      self.db_proxy.updateClassAssociation(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request):
    json_dict = super(ClassAssociationDAO, self).from_json(request)
    check_required_keys(json_dict, ClassAssociationModel.required)
    json_dict['__python_obj__'] = ClassAssociation.__module__+'.'+ClassAssociation.__name__
    dependency = json_deserialize(json_dict)
    if isinstance(dependency, ClassAssociation):
      return dependency
    else:
      self.close()
      raise MalformedJSONHTTPError(json_serialize(json_dict))
