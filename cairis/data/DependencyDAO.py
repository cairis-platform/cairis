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

__author__ = 'Robin Quetin'


class DependencyDAO(CairisDAO):
    def __init__(self, session_id):
        CairisDAO.__init__(self, session_id)

    def get_dependencies(self, constraint_id=''):
        """
        :rtype : dict[str, Dependency]
        """
        try:
            dependencies = self.db_proxy.getDependencies(constraint_id)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError

        return dependencies

    def get_dependency(self, environment, depender, dependee, dependency):
        """
        :type environment: str
        :type depender: str
        :type dependee: str
        :type dependency: str
        :rtype : list[Dependency]
        """
        args = [environment, depender, dependee, dependency]
        if not 'all' in args:
            return [self.get_dependency_by_name('/'.join(args))]
        else:
            dependencies = self.get_dependencies()
            found_dependencies = []

            for key in dependencies:
                parts = key.split('/')
                if environment != 'all' and parts[0] != environment:
                    continue
                if depender != 'all' and parts[1] != depender:
                    continue
                if dependee != 'all' and parts[2] != dependee:
                    continue
                if dependency != 'all' and parts[3] != dependency:
                    continue

                found_dependencies.append(dependencies[key])

            return found_dependencies


    def get_dependency_by_name(self, dep_name):
        """
        :rtype : Dependency
        """
        dependencies = self.get_dependencies()

        found_dependency = dependencies.get(dep_name, None)

        if not found_dependency:
            raise ObjectNotFoundHTTPError('The provided dependency name')

        return found_dependency

    def add_dependency(self, dependency):
        """
        :rtype : int
        """
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

        return dep_id

    def delete_dependencies(self, environment, depender, dependee, dependency):
        found_dependencies = self.get_dependency(environment, depender, dependee, dependency)

        try:
            for found_dependency in found_dependencies:
                self.db_proxy.deleteDependency(
                    found_dependency.theId,
                    found_dependency.theDependencyType
                )
            return len(found_dependencies)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def update_dependency(self, dep_name, dependency):
        found_dependency = self.get_dependency_by_name(dep_name)
        params = DependencyParameters(
            envName=dependency.theEnvironmentName,
            depender=dependency.theDepender,
            dependee=dependency.theDependee,
            dependencyType=dependency.theDependencyType,
            dependency=dependency.theDependency,
            rationale=dependency.theRationale
        )
        params.setId(found_dependency.theId)

        try:
            self.db_proxy.updateDependency(params)
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
