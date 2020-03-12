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
from cairis.core.DependencyParameters import DependencyParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.core.Dependency import Dependency
from cairis.tools.JsonConverter import json_deserialize, json_serialize
from cairis.tools.ModelDefinitions import DependencyModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin, Shamal Faily'


class DependencyDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_objects(self, constraint_id='',simplify=True):
    try:
      if (constraint_id == -1): constraint_id = ''
      dependencies = self.db_proxy.getDependencies(constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError

    if (simplify):
      depKeys = sorted(dependencies.keys())
      depList = []
      for key in depKeys:
        value = dependencies[key]
        del value.theId
        depList.append(value)
      return depList
    else:
      for key, value in list(dependencies.items()):
        del value.theId
        dependencies[key] = value
      return dependencies
      
  def get_object_by_4parameters(self, environment, depender, dependee, dependency):
    try:
      dep = self.db_proxy.getDependency(environment, depender, dependee, dependency)
      del dep.theId
      return dep
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided dependency name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError
    
  def add_object(self, dependency):
    params = DependencyParameters(
      envName=dependency.theEnvironmentName,
      depender=dependency.theDepender,
      dependee=dependency.theDependee,
      dependencyType=dependency.theDependencyType,
      dependency=dependency.theDependency,
      rationale=dependency.theRationale
    )

    try:
      dep_id = self.db_proxy.addDependency(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object_by_4parameters(self, environment, depender, dependee, dependency):
    try:
      dep = self.db_proxy.getDependency(environment, depender, dependee, dependency)
      self.db_proxy.deleteDependency(dep.theId,dep.theDependencyType)
      return 1
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided dependency name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object_by_4parameters(self, environment, depender, dependee, dependency, new_dependency):
    try:
      found_dependency = self.db_proxy.getDependency(environment, depender, dependee, dependency)
      params = DependencyParameters(
        envName=new_dependency.theEnvironmentName,
        depender=new_dependency.theDepender,
        dependee=new_dependency.theDependee,
        dependencyType=new_dependency.theDependencyType,
        dependency=new_dependency.theDependency,
        rationale=new_dependency.theRationale
      )
      params.setId(found_dependency.theId)
      self.db_proxy.updateDependency(params)
    except ObjectNotFound as ex:
      self.close()
      raise ObjectNotFoundHTTPError('The provided dependency name')
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def from_json(self, request):
    json_dict = super(DependencyDAO, self).from_json(request)
    check_required_keys(json_dict, DependencyModel.required)
    json_dict['__python_obj__'] = Dependency.__module__+'.'+Dependency.__name__
    dependency = json_deserialize(json_dict)
    if isinstance(dependency, Dependency):
      return dependency
    else:
      self.close()
      raise MalformedJSONHTTPError(json_serialize(json_dict))
