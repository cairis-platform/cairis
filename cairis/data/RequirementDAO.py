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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, handle_exception, \
    MissingParameterHTTPError
from cairis.core.Requirement import Requirement
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import RequirementModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin'


class RequirementDAO(CairisDAO):
    def __init__(self, session_id):
        CairisDAO.__init__(self, session_id)

    def get_requirements(self, constraint_id='', is_asset=True, ordered=False):
        try:
            if ordered:
                requirements = self.db_proxy.getOrderedRequirements(constraint_id, is_asset)
            else:
                requirements = self.db_proxy.getRequirements(constraint_id, is_asset)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

        return requirements

    def get_requirement_by_id(self, req_id):
        found_requirement = None
        try:
            requirements = self.db_proxy.getRequirements()
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

        idx = 0
        while found_requirement is None and idx < len(requirements):
            if requirements.values()[idx].theId == int(req_id):
                found_requirement = requirements.values()[idx]
            idx += 1

        if found_requirement is None:
            self.close()
            raise ObjectNotFoundHTTPError('The provided requirement ID')

        return found_requirement

    def get_requirement_by_name(self, name):
        found_requirement = None
        try:
            requirements = self.db_proxy.getRequirements()
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)

        if requirements is not None:
            idx = 0
            while found_requirement is None and idx < len(requirements):
                if requirements.values()[idx].theName == name:
                    found_requirement = requirements.values()[idx]

                idx += 1

        if found_requirement is None:
            self.close()
            raise ObjectNotFoundHTTPError('The provided requirement name')

        return found_requirement

    def get_requirement_by_shortcode(self, shortcode):
        found_requirement = None
        requirements = self.get_requirements().values()
        idx = 0

        while found_requirement is None and idx < len(requirements):
            requirement = requirements[idx]
            if requirement.theLabel == shortcode:
                found_requirement = requirement
            idx +=1

        if found_requirement is None:
            self.close()
            raise ObjectNotFoundHTTPError(obj='The provided requirement shortcode')

        return found_requirement

    def add_requirement(self, requirement, asset_name=None, environment_name=None):
        try:
            self.db_proxy.nameCheck(requirement.theName, 'requirement')
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

        new_id = self.db_proxy.newId()
        requirement.theId = new_id

        if asset_name is not None:
            try:
                self.db_proxy.addRequirement(requirement, assetName=asset_name, isAsset=True)
            except Exception as ex:
                self.close()
                handle_exception(ex)
        elif environment_name is not None:
            try:
                self.db_proxy.addRequirement(requirement, assetName=environment_name, isAsset=False)
            except Exception as ex:
                self.close()
                handle_exception(ex)
        else:
            self.close()
            raise MissingParameterHTTPError(param_names=['requirement', 'environment'])

        return new_id

    def delete_requirement(self, name=None, req_id=None):
        if name is not None:
            req = self.get_requirement_by_name(name)
        elif req_id is not None:
            req = self.get_requirement_by_id(req_id)
        else:
            self.close()
            raise MissingParameterHTTPError(param_names=['id'])

        if req is None:
            self.close()
            raise ObjectNotFoundHTTPError('The provided requirement')

        self.db_proxy.deleteRequirement(req.theId)

    def update_requirement(self, requirement, name=None, req_id=-1):
        old_requirement = None
        if name is not None:
            old_requirement = self.get_requirement_by_name(name)
        elif req_id > -1:
            old_requirement = self.get_requirement_by_id(req_id=req_id)
        else:
            self.close()
            raise MissingParameterHTTPError(param_names=['theId'])

        if old_requirement is not None:
            try:
                requirement.theVersion = old_requirement.theVersion
                requirement.incrementVersion()
                self.db_proxy.updateRequirement(requirement)
            except DatabaseProxyException as ex:
                self.close()
                raise ARMHTTPError(ex)
        else:
            self.close()
            raise MissingParameterHTTPError(param_names=['id'])

    def from_json(self, request):
        """
        :rtype Requirement
        """
        json = request.get_json(silent=True)
        if json is False or json is None:
            self.close()
            raise MalformedJSONHTTPError(data=request.get_data())

        json_dict = json['object']
        check_required_keys(json_dict, RequirementModel.required)
        json_dict['__python_obj__'] = Requirement.__module__+'.'+Requirement.__name__
        requirement = json_serialize(json_dict)
        requirement = json_deserialize(requirement)
        if not isinstance(requirement, Requirement):
            self.close()
            raise MalformedJSONHTTPError(data=request.get_data())
        else:
            return requirement

    def simplify(self, obj):
        # Requirements do not need simplification
        return obj
