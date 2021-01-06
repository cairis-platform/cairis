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
from cairis.daemon.CairisHTTPError import ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, SilentHTTPError
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.PseudoClasses import ObjectDependency
from cairis.tools.ModelDefinitions import ObjectDependencyModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Shamal Faily'


class ObjectDependencyDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def report_dependencies(self,dimension_name,object_name, pathValues = []):
    try:
      if (dimension_name == 'architectural_pattern'):
        dimension_name = 'component_view'
      elif (dimension_name == 'user_goal'):
        dimension_name = 'synopsis'
      objtId = self.db_proxy.getDimensionId(object_name,dimension_name)
      realDeps = self.db_proxy.reportDependencies(dimension_name,objtId)
      fakeDeps = ObjectDependencyModel()
      for dep in realDeps:
        fakeDeps.theDependencies.append(ObjectDependency(dep[0],dep[2]))
      return fakeDeps
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_dependencies(self,dimension_name,object_name, pathValues = []):
    try:
      if (dimension_name == 'architectural_pattern'):
        dimension_name = 'component_view'
      elif (dimension_name == 'user_goal'):
        dimension_name = 'synopsis'
      objtId = self.db_proxy.getDimensionId(object_name,dimension_name)
      realDeps = self.db_proxy.reportDependencies(dimension_name,objtId)
      self.db_proxy.deleteDependencies(realDeps)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
