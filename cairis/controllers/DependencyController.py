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
from flask import session, make_response
from flask import request
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError
from cairis.data.DependencyDAO import DependencyDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import DependencyMessage
from cairis.tools.ModelDefinitions import DependencyModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin'


class DependenciesAPI(Resource):
    #region Swagger Docs
    @swagger.operation(
        notes='Get all dependencies',
        nickname='dependencies-get',
        responseClass=DependencyModel.__name__,
        parameters=[
            {
                "name": "constraint_id",
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
            }
        ]
    )
    #endregion
    def get(self):
        session_id = get_session_id(session, request)
        constraintsId = request.args.get('constraint_id', '')

        dao = DependencyDAO(session_id)
        dependencies = dao.get_dependencies(constraintsId)
        dao.close()

        resp = make_response(json_serialize(dependencies, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    #region Swagger Docs
    @swagger.operation(
        notes='Add a new dependency',
        nickname='dependencies-post',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the asset to be updated",
                "required": True,
                "allowMultiple": False,
                "type": DependencyMessage.__name__,
                "paramType": "body"
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
                "code": MalformedJSONHTTPError.status_code,
                "message": MalformedJSONHTTPError.status
            },
            {
                "code": ARMHTTPError.status_code,
                "message": ARMHTTPError.status
            }
        ]
    )
    #endregion
    def post(self):
        session_id = get_session_id(session, request)

        dao = DependencyDAO(session_id)
        new_dependency = dao.from_json(request)
        new_dependency_id = dao.add_dependency(new_dependency)
        dao.close()

        resp_dict = {'message': 'Dependency successfully added', 'dependency_id': new_dependency_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

class DependencyByNameAPI(Resource):
    #region Swagger Docs
    @swagger.operation(
        notes='Get a dependency/dependencies by their environment, depender, dependee or dependency. Use \'all\' as joker.',
        nickname='dependency-by-name-get',
        responseClass=DependencyModel.__name__,
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
            }
        ]
    )
    #endregion
    def get(self, environment, depender, dependee, dependency):
        session_id = get_session_id(session, request)

        dao = DependencyDAO(session_id)
        found_dependency = dao.get_dependency(
            environment=environment,
            depender=depender,
            dependee=dependee,
            dependency=dependency
        )
        dao.close()

        resp = make_response(json_serialize(found_dependency, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Updates an existing dependency',
        nickname='dependency-name-put',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the asset to be updated",
                "required": True,
                "allowMultiple": False,
                "type": DependencyMessage.__name__,
                "paramType": "body"
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
                'code': httplib.BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': ObjectNotFoundHTTPError.status_code,
                'message': ObjectNotFoundHTTPError.status
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            }
        ]
    )
    # endregion
    def put(self, environment, depender, dependee, dependency):
        session_id = get_session_id(session, request)
        dep_name = '/'.join([environment, depender, dependee, dependency])

        dao = DependencyDAO(session_id)
        new_dependency = dao.from_json(request)
        dao.update_dependency(dep_name, new_dependency)
        dao.close()

        resp_dict = {'message': 'Dependency successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp


    #region Swagger Docs
    @swagger.operation(
        notes='Add a new dependency',
        nickname='dependencies-post',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the asset to be updated",
                "required": True,
                "allowMultiple": False,
                "type": DependencyMessage.__name__,
                "paramType": "body"
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
                "code": MalformedJSONHTTPError.status_code,
                "message": MalformedJSONHTTPError.status
            },
            {
                "code": ARMHTTPError.status_code,
                "message": ARMHTTPError.status
            }
        ]
    )
    #endregion
    def post(self, environment, depender, dependee, dependency):
        session_id = get_session_id(session, request)

        dao = DependencyDAO(session_id)
        new_dependency = dao.from_json(request)
        new_dependency_id = dao.add_dependency(new_dependency)
        dao.close()

        resp_dict = {'message': 'Dependency successfully added', 'dependency_id': new_dependency_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Updates an existing dependency',
        nickname='dependency-name-put',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the asset to be updated",
                "required": True,
                "allowMultiple": False,
                "type": DependencyMessage.__name__,
                "paramType": "body"
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
                'code': httplib.BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': ObjectNotFoundHTTPError.status_code,
                'message': ObjectNotFoundHTTPError.status
            },
            {
                'code': ARMHTTPError.status_code,
                'message': ARMHTTPError.status
            }
        ]
    )
    # endregion
    def delete(self, environment, depender, dependee, dependency):
        session_id = get_session_id(session, request)

        dao = DependencyDAO(session_id)
        count = dao.delete_dependencies(
            environment=environment,
            depender=depender,
            dependee=dependee,
            dependency=dependency
        )
        dao.close()

        if count > 1:
            resp_dict = {'message': count+' dependencies successfully deleted'}
        else:
            resp_dict = {'message': 'Dependency successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp
