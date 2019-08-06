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
from cairis.core.DataFlow import DataFlow
from cairis.core.DataFlowParameters import DataFlowParameters

from cairis.misc.DataFlowDiagram import DataFlowDiagram
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import DataFlowModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts


__author__ = 'Shamal Faily'


class DataFlowDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_dataflows(self, dataflow_name = '', environment_name = ''):
    try:
      dfs = self.db_proxy.getDataFlows(dataflow_name,environment_name)
      return dfs
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)


  def get_dataflow_by_name(self, dataflow_name, environment_name):
    dfs = self.get_dataflows(dataflow_name,environment_name)
    if len(dfs) == 0:
      self.close()
      raise ObjectNotFoundHTTPError('The provided dataflow name')
    return dfs[0]

  def add_dataflow(self, dataflow):
    df_params = DataFlowParameters(
      dfName=dataflow.name(),
      envName=dataflow.environment(),
      fromName=dataflow.fromName(),
      fromType=dataflow.fromType(),
      toName=dataflow.toName(),
      toType=dataflow.toType(),
      dfAssets=dataflow.assets()
    )

    try:
      if not self.check_existing_dataflow(dataflow.name(),dataflow.fromType(), dataflow.fromName(), dataflow.toType(), dataflow.toName(), dataflow.environment()):
        self.db_proxy.addDataFlow(df_params)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=dataflow.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_dataflow(self, old_dataflow_name,old_environment_name, dataflow):

    df_params = DataFlowParameters(
      dfName=dataflow.name(),
      envName=dataflow.environment(),
      fromName=dataflow.fromName(),
      fromType=dataflow.fromType(),
      toName=dataflow.toName(),
      toType=dataflow.toType(),
      dfAssets=dataflow.assets()
    )

    try:
#      if not self.check_existing_dataflow(dataflow.name(),dataflow.fromType(), dataflow.fromName(), dataflow.toType(), dataflow.toName(), dataflow.environment()):
       self.db_proxy.updateDataFlow(old_dataflow_name,old_environment_name,df_params)
#      else:
#        self.close()
#        raise OverwriteNotAllowedHTTPError(obj_name=dataflow.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_dataflow(self, dataflow_name, environment_name):
    try:
      self.db_proxy.deleteDataFlow(dataflow_name, environment_name)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_dataflow(self, dataflow_name, from_type, from_name, to_type, to_name, environment_name):
    try:
       self.db_proxy.checkDataFlowExists(dataflow_name, from_type, from_name, to_type, to_name, environment_name)
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
    check_required_keys(json_dict, DataFlowModel.required)
    json_dict['__python_obj__'] = DataFlow.__module__ + '.' + DataFlow.__name__

    dataflow = json_serialize(json_dict)
    dataflow = json_deserialize(dataflow)
    if not isinstance(dataflow, DataFlow):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return dataflow

  def get_dataflow_diagram(self, environment_name, filter_element):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    try:
      dfdRows = self.db_proxy.dataFlowDiagram(environment_name,filter_element)
      associations = DataFlowDiagram(dfdRows,environment_name,self.db_proxy,font_name=fontName, font_size=fontSize)
      dot_code = associations.graph()
      if not dot_code:
        raise ObjectNotFoundHTTPError('The data flow diagram')
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
