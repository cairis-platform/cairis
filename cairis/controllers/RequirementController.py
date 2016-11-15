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

import httplib
from flask import session, request, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError
from cairis.data.RequirementDAO import RequirementDAO
from cairis.tools.MessageDefinitions import RequirementMessage
from cairis.tools.ModelDefinitions import RequirementModel
from cairis.tools.SessionValidator import get_session_id
from cairis.tools.JsonConverter import json_serialize

__author__ = 'Robin Quetin'


class RequirementsAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all requirements',
        nickname='requirements-get',
        responseClass=RequirementModel.__name__,
        responseContainer='List',
        parameters=[
            {
                "name": "ordered",
                "description": "Defines if the list has to be order",
                "default": 1,
                "required": False,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "query"
            },
            {
                "name": "constraint_id",
                "description": "The constraint used as filter to query the database",
                "default": "",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            },
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            }
        ]
    )
    # endregion
    def get(self):
        session_id = get_session_id(session, request)
        ordered = request.args.get('ordered', 0)
        constraint_id = request.args.get('constraint_id', '')

        dao = RequirementDAO(session_id)
        reqs = dao.get_requirements(constraint_id=constraint_id, ordered=(ordered=='1'))
        dao.close()

        resp = make_response(json_serialize(reqs, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new requirement',
        nickname='requirements-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new requirement to be added",
                "required": True,
                "allowMultiple": False,
                "type": RequirementMessage.__name__,
                "paramType": "body"
            },
            {
                "name": "asset",
                "description": "The name of the asset which is associated to the new requirement",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "environment",
                "description": "The name of the environment which is associated to the new requirement",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            },
            {
                'code': MalformedJSONHTTPError.status_code,
                'message': MalformedJSONHTTPError.status
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            }
        ]
    )
    # endregion
    def post(self):
        session_id = get_session_id(session, request)
        asset_name = request.args.get('asset', None)
        environment_name = request.args.get('environment', None)

        dao = RequirementDAO(session_id)
        new_req = dao.from_json(request)
        req_id = dao.add_requirement(new_req, asset_name=asset_name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Requirement successfully added', 'requirement_id': req_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates a requirement',
        nickname='requirement-update-put',
        parameters=[
            {
                'name': 'body',
                "description": "The new updated requirement",
                "required": True,
                "allowMultiple": False,
                'type': RequirementMessage.__name__,
                'paramType': 'body'
            }
        ],
        responseMessages=[
            {
                'code': ObjectNotFoundHTTPError.status_code,
                'message': ObjectNotFoundHTTPError.status
            },
            {
                'code': MalformedJSONHTTPError.status_code,
                'message': MalformedJSONHTTPError.status
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            },
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            }
        ]
    )
    # endregion
    def put(self):
        session_id = get_session_id(session, request)
        dao = RequirementDAO(session_id)
        req = dao.from_json(request)
        dao.update_requirement(req, req_id=req.theId)
        dao.close()

        resp_dict = {'message': 'Requirement successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp


class RequirementsByAssetAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get the requirements associated with an asset',
        nickname='requirements-by-asset-get',
        responseClass=RequirementModel.__name__,
        responseContainer='List',
        parameters=[
            {
                "name": "ordered",
                "description": "Defines if the list has to be order",
                "default": 1,
                "required": False,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "query"
            },
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            },
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)
        ordered = request.args.get('ordered', '1')

        dao = RequirementDAO(session_id)
        reqs = dao.get_requirements(constraint_id=name, is_asset=True, ordered=(ordered=='1'))
        dao.close()

        resp = make_response(json_serialize(reqs, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp


class RequirementsByEnvironmentAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get the requirements associated with an environment',
        nickname='requirements-by-environment-get',
        responseClass=RequirementModel.__name__,
        responseContainer='List',
        parameters=[
            {
                "name": "ordered",
                "description": "Defines if the list has to be order",
                "default": 1,
                "required": False,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "query"
            },
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            },
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)
        ordered = request.args.get('ordered', '1')

        dao = RequirementDAO(session_id)
        reqs = dao.get_requirements(constraint_id=name, is_asset=False, ordered=(ordered=='1'))
        dao.close()

        resp = make_response(json_serialize(reqs, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp


class RequirementByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a requirement by name',
        nickname='requirement-by-name-get',
        responseClass=RequirementModel.__name__,
        parameters=[
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": httplib.BAD_REQUEST,
                "message": "The database connection was not properly set up"
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            },
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            },
            {
                'code': ObjectNotFoundHTTPError.status_code,
                'message': ObjectNotFoundHTTPError.status
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)

        dao = RequirementDAO(session_id)
        req = dao.get_requirement_by_name(name)
        dao.close()

        resp = make_response(json_serialize(req, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing requirement',
        nickname='requirement-by-name-delete',
        parameters=[
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            },
            {
                'code': MalformedJSONHTTPError.status_code,
                'message': MalformedJSONHTTPError.status
            },
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            },
            {
                'code': ObjectNotFoundHTTPError.status_code,
                'message': ObjectNotFoundHTTPError.status
            }
        ]
    )
    # endregion
    def delete(self, name):
        session_id = get_session_id(session, request)

        dao = RequirementDAO(session_id)
        dao.delete_requirement(name=name)
        dao.close()

        resp_dict = {'message': 'Requirement successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

class RequirementByShortcodeAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a requirement by ID',
        nickname='requirement-by-id-get',
        responseClass=RequirementModel.__name__,
        parameters=[
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            },
            {
                'code': MissingParameterHTTPError.status_code,
                'message': MissingParameterHTTPError.status
            },
            {
                'code': ObjectNotFoundHTTPError.status_code,
                'message': ObjectNotFoundHTTPError.status
            }
        ]
    )
    # endregion
    def get(self, shortcode):
        session_id = get_session_id(session, request)

        dao = RequirementDAO(session_id)
        req = dao.get_requirement_by_shortcode(shortcode)
        dao.close()

        resp = make_response(json_serialize(req, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp
