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
    CairisDAO.__init__(self, session_id, 'trust_boundary')

  def get_objects(self, constraint_id = -1):
    try:
      tbs = self.db_proxy.getTrustBoundaries(constraint_id)
      values = []
      for value in tbs:
        values.append(self.simplify(value))
      return values
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def get_object_by_name(self, trust_boundary_name):
    tbId = self.db_proxy.getDimensionId(trust_boundary_name,'trust_boundary')
    tbs = self.get_objects(tbId)
    if len(tbs) == 0:
      self.close()
      raise ObjectNotFoundHTTPError('The provided trust boundary name')
    return tbs[0]

  def add_object(self, tb):
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

  def update_object(self, tb, old_trust_boundary_name):
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

  def delete_object(self, trust_boundary_name):
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
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TrustBoundaryModel.required)
    json_dict['__python_obj__'] = TrustBoundary.__module__ + '.' + TrustBoundary.__name__
    comps,pls = self.convert_props(fake_props=json_dict['theEnvironmentProperties'])
    json_dict['theEnvironmentProperties'] = []

    tb = json_serialize(json_dict)
    tb = json_deserialize(tb)
    tb.theComponents = comps
    tb.thePrivilegeLevels = pls
    if not isinstance(tb, TrustBoundary):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return tb

  def simplify(self, tb):
    assert isinstance(tb, TrustBoundary)
    del tb.theId
    tb.theEnvironmentProperties = self.convert_props(real_props=(tb.theComponents,tb.thePrivilegeLevels))
    del tb.theComponents
    del tb.thePrivilegeLevels
    return tb


  def convert_props(self, real_props=None, fake_props=None):
    if real_props is not None:
      real_comps = real_props[0]
      real_pls = real_props[1]
      new_props = []
      for envName in real_comps:
        compList = []
        for tbCompType,tbComp in real_comps[envName]:
          compList.append(TrustBoundaryComponent(tbComp,tbCompType))
        pLevel = real_pls[envName]
        new_props.append(TrustBoundaryEnvironmentModel(envName,compList,pLevel))
      return new_props
    elif fake_props is not None:
      new_props = {}
      new_pls = {}
     
      for fake_prop in fake_props:
        envName = fake_prop['theEnvironmentName']
        pLevel = fake_prop['thePrivilege']
        compList = []
        for comp in fake_prop['theComponents']:
          compList.append((comp['theType'],comp['theName']))
        new_props[envName] = compList
        new_pls[envName] = pLevel
      return (new_props,new_pls)
