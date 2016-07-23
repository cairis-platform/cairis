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
from cairis.core.AcceptEnvironmentProperties import AcceptEnvironmentProperties
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, OverwriteNotAllowedHTTPError
from cairis.core.MitigateEnvironmentProperties import MitigateEnvironmentProperties
from cairis.core.ResponseParameters import ResponseParameters
from cairis.core.TransferEnvironmentProperties import TransferEnvironmentProperties
from cairis.data.CairisDAO import CairisDAO
from cairis.core.Response import Response
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import ResponseModel, ResponseEnvironmentPropertiesModel, AcceptEnvironmentPropertiesModel, \
    MitigateEnvironmentPropertiesModel, TransferEnvironmentPropertiesModel
from cairis.tools.PseudoClasses import ValuedRole
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin'


class ResponseDAO(CairisDAO):
    def __init__(self, session_id):
        CairisDAO.__init__(self, session_id)

    def get_responses(self, constraint_id=-1, simplify=True):
        """
        :rtype : dict[str, Response]
        """
        try:
            responses = self.db_proxy.getResponses(constraintId=constraint_id)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

        if simplify:
            for key in responses:
                responses[key] = self.simplify(responses[key])

        return responses

    def get_response_by_name(self, response_name, simplify=True):
        """
        :rtype : Response
        :raises:
            ObjectNotFoundHTTPError:
            ARMHTTPError:
        """
        responses = self.get_responses(simplify=simplify)
        found_response = responses.get(response_name, None)

        if not found_response:
            self.close()
            raise ObjectNotFoundHTTPError(obj='The provided response name')

        return found_response

    def delete_response(self, response_name):
        """
        :raise: ARMHTTPError:
        """
        found_response = self.get_response_by_name(response_name)

        try:
            self.db_proxy.deleteResponse(found_response.theId)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def add_response(self, response):
        """
        :raises:
            ARMHTTPError:
            OverwriteNotAllowedHTTPError:
        """
        if self.check_existing_response(response.theName):
            self.close()
            raise OverwriteNotAllowedHTTPError('The provided response name')

        params = ResponseParameters(
            respName=response.theName,
            respRisk=response.theRisk,
            tags=response.theTags,
            cProps=response.theEnvironmentProperties,
            rType=response.theResponseType
        )

        try:
            resp_id = self.db_proxy.addResponse(params)
            return resp_id
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def update_response(self, resp_name, response):
        found_response = self.get_response_by_name(resp_name)
        params = ResponseParameters(
            respName=response.theName,
            respRisk=response.theRisk,
            tags=response.theTags,
            cProps=response.theEnvironmentProperties,
            rType=response.theResponseType
        )
        params.setId(found_response.theId)

        try:
            self.db_proxy.updateResponse(params)
        except DatabaseProxyException as ex:
            self.close()
            raise ARMHTTPError(ex)
        except ARMException as ex:
            self.close()
            raise ARMHTTPError(ex)

    def check_existing_response(self, risk_name):
        """
        :rtype : bool
        :raise: ARMHTTPError:
        """
        try:
            self.get_response_by_name(risk_name)
            return True
        except ObjectNotFoundHTTPError:
            self.db_proxy.reconnect(session_id=self.session_id)
            return False

    def from_json(self, request):
        """
        :rtype : Response
        :raise: MalformedJSONHTTPError:
        """
        json = request.get_json(silent=True)
        if json is False or json is None:
            self.close()
            raise MalformedJSONHTTPError(data=request.get_data())

        json_dict = json['object']
        check_required_keys(json_dict, ResponseModel.required)
        json_dict['__python_obj__'] = Response.__module__+'.'+Response.__name__

        property_dict = json_dict['theEnvironmentProperties']
        try:
            real_props = self.convert_props(fake_props=property_dict, response_type=json_dict['theResponseType'])
            json_dict['theEnvironmentProperties'] = real_props

            json_resp = json_serialize(json_dict)
            response = json_deserialize(json_resp)

            if isinstance(response, Response):
                return response
            else:
                raise MalformedJSONHTTPError()
        except MalformedJSONHTTPError as ex:
            self.close()
            raise ex

    def convert_props(self, real_props=None, fake_props=None, response_type=None):
        """
        :type real_props: list
        :type fake_props: dict[str,list[dict]]
        :type response_type: str
        """
        response_type = response_type.lower()

        if real_props:
            new_props_list = []
            for idx in range(0, len(real_props)):
                real_prop = real_props[idx]
                if isinstance(real_prop, AcceptEnvironmentProperties) and response_type == 'accept':
                    new_props_list.append(real_prop)
                elif isinstance(real_prop, MitigateEnvironmentProperties) and response_type == 'mitigate':
                    new_props_list.append(real_prop)
                elif isinstance(real_prop, TransferEnvironmentProperties) and response_type == 'transfer':
                    roles = real_prop.theRoles
                    for idx in range(0, len(roles)):
                        roles[idx] = ValuedRole(roles[idx][0], roles[idx][1])
                    real_prop.theRoles = roles
                    new_props_list.append(real_prop)
            new_props = { response_type: new_props_list }
        elif fake_props:
            new_props = []
            if not (response_type in ResponseEnvironmentPropertiesModel.field_names):
#            if not (response_type in ResponseEnvironmentPropertiesModel.field_names and fake_props.has_key(response_type)):
                raise MalformedJSONHTTPError()

#            fake_props = fake_props[response_type]
            if response_type == 'accept':
                model_class = AcceptEnvironmentPropertiesModel
                target_class = AcceptEnvironmentProperties
            elif response_type == 'mitigate':
                model_class = MitigateEnvironmentPropertiesModel
                target_class = MitigateEnvironmentProperties
            elif response_type == 'transfer':
                model_class = TransferEnvironmentPropertiesModel
                target_class = TransferEnvironmentProperties
            else:
                raise MalformedJSONHTTPError()

            for fake_prop in fake_props:
                check_required_keys(fake_prop, model_class.required)
                fake_prop['__python_obj__'] = target_class.__module__+'.'+target_class.__name__
                if target_class is TransferEnvironmentProperties:
                    roles = []
                    if isinstance(fake_prop['theRoles'], list):
                        for role in fake_prop['theRoles']:
                            check_required_keys(role, ValuedRole.required)
                            roles.append((role['roleName'], role['cost']))
                    fake_prop['theRoles'] = roles
                new_props.append(fake_prop)
        else:
            self.close()
            raise MalformedJSONHTTPError()

        return new_props

    def simplify(self, obj):
        """
        :type obj: Response
        :rtype: Response
        """
        obj.theEnvironmentDictionary = {}
        obj.costLookup = {}
        delattr(obj, 'costLookup')
        delattr(obj, 'theEnvironmentDictionary')

        try:
            obj.theEnvironmentProperties = self.convert_props(real_props=obj.theEnvironmentProperties, response_type=obj.theResponseType)
        except MalformedJSONHTTPError as ex:
            self.close()
            raise ex

        return obj
