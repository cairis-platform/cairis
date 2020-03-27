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
from cairis.core.Trace import Trace
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, MalformedJSONHTTPError, ARMHTTPError, MissingParameterHTTPError, OverwriteNotAllowedHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.ModelDefinitions import TraceModel
from cairis.tools.SessionValidator import check_required_keys
from cairis.tools.JsonConverter import json_serialize, json_deserialize

__author__ = 'Shamal Faily'


class TraceDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_traces(self,envName, pathValues = []):
    try:
      trs = self.db_proxy.removableTraces(envName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return self.simplify(trs)

  def simplify(self,trs):
    trList = []
    for tr in trs:
      trList.append(TraceModel(tr[0],tr[1],tr[2],tr[3],tr[4]))
    return trList

  def add_object(self, tr):
    try:
      trace_table = tr.theFromObject + '_' + tr.theToObject
      self.db_proxy.checkTrace(tr.theFromObject,tr.theFromName,tr.theToObject,tr.theToName)
      fromId = self.db_proxy.getDimensionId(tr.theFromName,tr.theFromObject)
      toId = self.db_proxy.getDimensionId(tr.theToName,tr.theToObject)
      self.db_proxy.addTrace(trace_table,fromId,toId,tr.theLabel)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def delete_trace(self, fromObjt,fromName,toObjt,toName,pathValues = []):
    try:
      self.db_proxy.deleteTrace(fromObjt,fromName,toObjt,toName)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def trace_dimensions(self,dimension_name,is_from, pathValues = []):
    if is_from == '1':
      is_from = True
    else:
      is_from = False
    try:
      return self.db_proxy.getTraceDimensions(dimension_name,is_from)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
  

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, TraceModel.required)
    json_dict['__python_obj__'] = Trace.__module__+'.'+ Trace.__name__
    tr = json_serialize(json_dict)
    tr = json_deserialize(tr)

    if isinstance(tr, Trace):
      return tr
    else:
      self.close()
      raise MalformedJSONHTTPError()
