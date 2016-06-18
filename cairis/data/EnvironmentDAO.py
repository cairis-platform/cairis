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
from cairis.daemon.CairisHTTPError import ARMHTTPError, MalformedJSONHTTPError, ObjectNotFoundHTTPError, MissingParameterHTTPError
from cairis.core.Environment import Environment
from cairis.core.EnvironmentParameters import EnvironmentParameters
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import EnvironmentModel
from cairis.tools.PseudoClasses import EnvironmentTensionModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin'


class EnvironmentDAO(CairisDAO):
    def __init__(self, session_id):
        CairisDAO.__init__(self, session_id)

    def get_environments(self, constraint_id=-1, simplify=True):
        """
        Get all the environments in dictionary form with the key being the environment name.
        :param simplify: Defines if the environment should be changed to be compatible with JSON
        :rtype list
        :raise ARMHTTPError:
        """
        try:
            environments = self.db_proxy.getEnvironments(constraint_id)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

        if simplify:
            for key, value in environments.items():
                environments[key] = self.simplify(value)
        return environments

    def get_environment_names(self):
        """
        Get the available environment names.
        :rtype list[str]
        :raise ARMHTTPError:
        """
        try:
            environment_names = self.db_proxy.getEnvironmentNames()
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)
        return environment_names
    
    def get_environment_by_name(self, name, simplify=True):
        """
        :rtype: Environment
        :raise ObjectNotFoundHTTPError:
        """
        found_environment = None
        try:
            environments = self.db_proxy.getEnvironments()
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

        if environments is not None:
            found_environment = environments.get(name)

        if found_environment is None:
            self.close()
            raise ObjectNotFoundHTTPError('The provided environment name')

        if simplify:
            found_environment = self.simplify(found_environment)

        return found_environment

    def get_environment_by_id(self, env_id, simplify=True):
        """
        :rtype: Environment
        :raise ObjectNotFoundHTTPError:
        """
        found_environment = None
        try:
            environments = self.db_proxy.getEnvironments()
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

        if environments is not None:
            found_environment = None
            idx = 0
            while found_environment is None and idx < len(environments):
                if environments.values()[idx].theId == env_id:
                    found_environment = environments.values()[idx]
                idx += 1

        if found_environment is None:
            self.close()
            raise ObjectNotFoundHTTPError('The provided environment name')

        if simplify:
            found_environment = self.simplify(found_environment)

        return found_environment

    def get_environments_by_threat_vulnerability(self, threat_name, vulnerability_name):
        """
        :rtype : dict[str, Environment]
        """
        env_names = self.get_environment_names_by_threat_vulnerability(threat_name, vulnerability_name)
        environments = {}
        for env_name in env_names:
            try:
                environment = self.get_environment_by_name(env_name)
                environments[env_name] = environment
            except:
                pass

        return environments

    def get_environment_names_by_threat_vulnerability(self, threat_name, vulnerability_name):
        """
        :rtype : list[str]
        """
        try:
            environments = self.db_proxy.riskEnvironments(threat_name, vulnerability_name)
            return environments
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def add_environment(self, environment):
        """
        :return: Returns the ID of the new environment
        :raise ARMHTTPError:
        """
        env_params = self.to_environment_parameters(environment)
        try:
            if not self.check_existing_environment(environment.theName):
                self.db_proxy.addEnvironment(env_params)
            else:
                self.close()
                raise DatabaseProxyException('Environment name already exists within the database.')
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

        try:
            new_environment = self.get_environment_by_name(environment.theName, simplify=False)
            if new_environment is not None:
                return new_environment.theId
        except ObjectNotFoundHTTPError:
            self.logger.warning('The new environment was not found in the database')
            self.logger.warning('Environment name: %s', environment.theName)
            return -1

    def update_environment(self, environment, name=None, env_id=None):
        if name is not None:
            environment_to_update = self.get_environment_by_name(name)
        elif env_id is not None:
            environment_to_update = self.get_environment_by_id(env_id)

        env_params = self.to_environment_parameters(environment)
        env_params.setId(environment_to_update.theId)
        if env_id is not None:
            name = environment.theName

        try:
            if self.check_existing_environment(name):
                self.db_proxy.updateEnvironment(env_params)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def delete_environment(self, name=None, env_id=None):
        if name is not None:
            found_environment = self.get_environment_by_name(name, simplify=False)
            if found_environment is None:
                raise ObjectNotFoundHTTPError('The provided environment name')
            env_id = found_environment.theId

        if env_id is not None and env_id > -1:
            try:
                self.db_proxy.deleteEnvironment(env_id)
            except DatabaseProxyException as ex:
                self.close()
                raise ARMHTTPError(ex)
            except ARMException as ex:
                self.close()
                raise ARMHTTPError(ex)
        else:
            self.close()
            raise MissingParameterHTTPError(param_names=['id'])

    def check_existing_environment(self, environment_name):
        """
        :raise ARMHTTPError:
        """
        try:
            self.db_proxy.nameCheck(environment_name, 'environment')
            return False
        except DatabaseProxyException as ex:
            if str(ex.value).find(' already exists') > -1:
                return True
            else:
                self.close()
                raise ARMHTTPError(ex)
        except ARMException as ex:
            if str(ex.value).find(' already exists') > -1:
                return True
            else:
                self.close()
                raise ARMHTTPError(ex)

    def to_environment_parameters(self, environment):
        assert isinstance(environment, Environment)
        env_params = EnvironmentParameters(
            conName=environment.theName,
            conSc=environment.theShortCode,
            conDesc=environment.theDescription,
            environments=environment.theEnvironments,
            duplProperty=environment.theDuplicateProperty,
            overridingEnvironment=environment.theOverridingEnvironment,
            envTensions=environment.theTensions
        )
        return env_params

    def from_json(self, request):
        json = request.get_json(silent=True)
        if json is False or json is None:
            self.close()
            raise MalformedJSONHTTPError(data=request.get_data())

        json_dict = json['object']
        assert isinstance(json_dict, dict)
        check_required_keys(json_dict, EnvironmentModel.required)
        json_dict['__python_obj__'] = Environment.__module__+'.'+Environment.__name__

        if json_dict.has_key('theTensions'):
            assert isinstance(json_dict['theTensions'], list)
            tensions = json_dict['theTensions']
            json_dict['theTensions'] = {}
            for tension in tensions:
                check_required_keys(tension, EnvironmentTensionModel.required)
                key = tuple([tension['base_attr_id'], tension['attr_id']])
                value = tuple([tension['value'], tension['rationale']])
                json_dict['theTensions'][key] = value

        new_json_environment = json_serialize(json_dict)
        environment = json_deserialize(new_json_environment)
        if not isinstance(environment, Environment):
            self.close()
            raise MalformedJSONHTTPError(data=request.get_data())
        else:
            return environment

    def simplify(self, obj):
        assert isinstance(obj, Environment)
        the_tensions = obj.theTensions
        assert isinstance(the_tensions, dict)
        obj.theTensions = []
        for key, value in the_tensions.items():
            obj.theTensions.append(EnvironmentTensionModel(key=key, value=value))

        return obj
