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
from cairis.core.ValueType import ValueType
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import ValueTypeModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class ValueTypeDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'value_type')

  def get_objects_by_2parameters(self,dimName,envName):
    if envName == 'all':
      envName = ''
    return self.get_value_types(dimName,envName,True)

  def get_object_by_3parameters(self,dimName,envName,objtName):
    if envName == 'all':
      envName = ''
    return self.get_value_type(dimName,envName,objtName,True)

  def get_value_types(self,dimName,envName = '',deleteId=True):
    try:
      vts = self.db_proxy.getValueTypes(dimName,envName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    vtso = []
    for vt in vts:
      if (deleteId == True):
        del vt.theId
      vtso.append(vt)
    return vtso

  def get_value_type(self, dimName,envName,objtName,deleteId=True):
    vts = self.get_value_types(dimName,envName,False)
    if vts is None or len(vts) < 1:
      self.close()
      raise ObjectNotFoundHTTPError(dimName)
    for vt in vts:
      if (vt.name() == objtName):
        if (deleteId == True):
          del vt.theId
        return vt
    self.close()
    raise ObjectNotFoundHTTPError('The provided ' + dimName + ' value types')

  def add_object(self, vt):
    vtParams = ValueTypeParameters(vtName=vt.theName,vtDesc=vt.theDescription,vType=vt.theType,envName=vt.theEnvironmentName,vtScore=vt.theScore,vtRat=vt.theRationale)
    try:
      self.db_proxy.addValueType(vtParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def update_object_by_3parameters(self,type_name,environment_name,object_name,vt):
    found_vt = self.get_value_type(type_name,environment_name,object_name,False)
    vtParams = ValueTypeParameters(vtName=vt.theName,vtDesc=vt.theDescription,vType=vt.theType,envName=vt.theEnvironmentName,vtScore=vt.theScore,vtRat=vt.theRationale)
    vtParams.setId(found_vt.theId)
    try:
      self.db_proxy.updateValueType(vtParams)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object_by_3parameters(self, type_name,environment_name,object_name):
    vt = self.get_value_type(type_name,environment_name,object_name,False)
    try:
      self.db_proxy.deleteValueType(vt.theId,type_name)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request, to_props=False):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ValueTypeModel.required)
    json_dict['__python_obj__'] = ValueType.__module__+'.'+ ValueType.__name__
    vt = json_serialize(json_dict)
    vt = json_deserialize(vt)

    if isinstance(vt, ValueType):
      return vt 
    else:
      self.close()
      raise MalformedJSONHTTPError()
