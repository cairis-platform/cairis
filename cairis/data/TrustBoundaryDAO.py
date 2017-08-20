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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.TrustBoundary import TrustBoundary
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import TrustBoundaryModel, TrustBoundaryEnvironmentModel, TrustBoundaryComponent
from cairis.tools.SessionValidator import check_required_keys


__author__ = 'Shamal Faily'


class TrustBoundaryDAO(CairisDAO):

  def __init__(self, session_id):
    """
    :raise CairisHTTPError:
    """
    CairisDAO.__init__(self, session_id)

  def get_trust_boundaries(self, constraint_id = -1):
    """
    :rtype: dict[str,TrustBoundary]
    :return
    :raise ARMHTTPError:
    """
    try:
      tbs = self.db_proxy.getTrustBoundaries(constraint_id)
      for key, value in list(tbs.items()):
        tbs[key] = self.simplify(value)
      return tbs
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def get_trust_boundary_by_name(self, trust_boundary_name):
    """
    :rtype: TrustBoundary
    :raise ObjectNotFoundHTTPError:
    """

    tbId = self.db_proxy.getDimensionId(trust_boundary_name,'trust_boundary')
    tbs = self.get_trust_boundaries(tbId)
    if len(tbs) == 0:
      self.close()
      raise ObjectNotFoundHTTPError('The provided trust boundary name')
    return tbs[trust_boundary_name]

  def add_trust_boundary(self, tb):
    try:
      if not self.check_existing_trust_boundary(tb.name()):
        self.db_proxy.addTrustBoundary(tb)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=tb.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_trust_boundary(self, old_trust_boundary_name, tb):
    try:
      tbId = self.db_proxy.getDimensionId(old_trust_boundary_name,'trust_boundary')
      tb.theId = tbId
      self.db_proxy.updateTrustBoundary(tb)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_trust_boundary(self, trust_boundary_name):
    try:
      tbId = self.db_proxy.getDimensionId(trust_boundary_name,'trust_boundary')
      self.db_proxy.deleteTrustBoundary(tbId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_trust_boundary(self, trust_boundary_name):
    """
    :rtype: bool
    :raise: ARMHTTPError
    """
    try:
      self.db_proxy.nameCheck(trust_boundary_name, 'trust_boundary')
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
    """
    :rtype : TrustBoundary
    :raise MalformedJSONHTTPError:
    """
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TrustBoundaryModel.required)
    json_dict['__python_obj__'] = TrustBoundary.__module__ + '.' + TrustBoundary.__name__
    env_props = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    tb = json_serialize(json_dict)
    tb = json_deserialize(tb)
    tb.theEnvironmentProperties = env_props
    if not isinstance(tb, TrustBoundary):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return tb

  def simplify(self, tb):
    assert isinstance(tb, TrustBoundary)
    tb.theEnvironmentProperties = self.convert_props(real_props=tb.theEnvironmentProperties)
    return tb


  def convert_props(self, real_props=None, fake_props=None):
    if real_props is not None:
      new_props = []
      for envName in real_props:
        compList = []
        for tbCompType,tbComp in real_props[envName]:
          compList.append(TrustBoundaryComponent(tbComp,tbCompType))
        new_props.append(TrustBoundaryEnvironmentModel(envName,compList))
      return new_props
    elif fake_props is not None:
      new_props = {}
      for fake_prop in fake_props:
        envName = fake_prop['theName']
        compList = []
        for comp in fake_prop['theComponents']:
          compList.append((comp['theType'],comp['theName']))
        new_props[envName] = compList
      return new_props
