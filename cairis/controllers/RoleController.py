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

import sys
if (sys.version_info > (3,)):
  import http.client
  from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
else:
  import httplib
  from httplib import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
from flask import request, session, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.data.RoleDAO import RoleDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import RoleMessage
from cairis.tools.ModelDefinitions import RoleModel, RoleEnvironmentPropertiesModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin, Shamal Faily'


class RolesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all roles',
        responseClass=RoleModel.__name__,
        nickname='roles-get',
        parameters=[
            {
                "name": "session_id",
                "description": "The ID of the user's session",
                "required": False,
                "allowMultiple": False,
                "dataType": str.__name__,
                "paramType": "query"
            },
            {
                "name": "constraint_id",
                "description": "An ID used to filter the roles",
                "required": False,
                "default": -1,
                "allowMultiple": False,
                "dataType": int.__name__,
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": BAD_REQUEST,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    # endregion
    def get(self):
        session_id = get_session_id(session, request)
        constraint_id = request.args.get('constraint_id', -1)

        dao = RoleDAO(session_id)
        roles = dao.get_roles(constraint_id)
        dao.close()

        resp = make_response(json_serialize(roles, session_id=session_id))
        resp.contenttype = "application/json"
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new role',
        nickname='role-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new role to be added",
                "required": True,
                "allowMultiple": False,
                "type": RoleMessage.__name__,
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
                'code': BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def post(self):
        session_id = get_session_id(session, request)

        dao = RoleDAO(session_id)
        new_role = dao.from_json(request)
        role_id = dao.add_role(new_role)
        dao.close()

        resp_dict = {'role_id': role_id}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
        resp.contenttype = 'application/json'
        return resp

class RolesByIdAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get an role by name',
        responseClass=RoleModel.__name__,
        nickname='role-by-name-get',
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
                "code": BAD_REQUEST,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    # endregion
    def get(self, id):
        session_id = get_session_id(session, request)

        dao = RoleDAO(session_id)
        found_role = dao.get_role_by_id(id)
        dao.close()

        resp = make_response(json_serialize(found_role, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Updates an existing role',
        nickname='role-put',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the role to be updated",
                "required": True,
                "allowMultiple": False,
                "type": RoleMessage.__name__,
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
                'code': BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': NOT_FOUND,
                'message': 'The provided role name could not be found in the database'
            },
            {
                'code': CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def put(self, id):
        session_id = get_session_id(session, request)

        dao = RoleDAO(session_id)
        upd_role = dao.from_json(request)
        dao.update_role(upd_role, role_id=id)
        dao.close()

        resp_dict = {'message': 'Update successful'}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing role',
        nickname='role-delete',
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
                'code': BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': NOT_FOUND,
                'message': 'The provided role name could not be found in the database'
            },
            {
                'code': CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def delete(self, id):
        session_id = get_session_id(session, request)

        dao = RoleDAO(session_id)
        dao.delete_role(role_id=id)
        dao.close()

        resp_dict = {'message': 'Role successfully deleted'}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
        resp.contenttype = 'application/json'
        return resp

class RolesByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get an role by name',
        responseClass=RoleModel.__name__,
        nickname='role-by-name-get',
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
                "code": BAD_REQUEST,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)

        dao = RoleDAO(session_id)
        found_role = dao.get_role_by_name(name)
        dao.close()

        resp = make_response(json_serialize(found_role, session_id=session_id))
        resp.headers['Content-Type'] = "application/json"
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Updates an existing role',
        nickname='role-put',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the role to be updated",
                "required": True,
                "allowMultiple": False,
                "type": RoleMessage.__name__,
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
                'code': BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': NOT_FOUND,
                'message': 'The provided role name could not be found in the database'
            },
            {
                'code': CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def put(self, name):
        session_id = get_session_id(session, request)
        dao = RoleDAO(session_id)

        upd_role = dao.from_json(request)
        dao.update_role(upd_role, name=name)
        dao.close()

        resp_dict = {'message': 'Update successful'}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing role',
        nickname='role-delete',
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
                'code': BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': NOT_FOUND,
                'message': 'The provided role name could not be found in the database'
            },
            {
                'code': CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def delete(self, name):
        session_id = get_session_id(session, request)

        dao = RoleDAO(session_id)
        dao.delete_role(name=name)
        dao.close()

        resp_dict = {'message': 'Role successfully deleted'}
        resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
        resp.contenttype = 'application/json'
        return resp

class RoleEnvironmentPropertiesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get the environment properties for a specific role',
        nickname='role-envprops-by-name-get',
        responseClass=RoleEnvironmentPropertiesModel.__name__,
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
                "code": BAD_REQUEST,
                "message": "The database connection was not properly set up"
            }
        ]
    )
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)

        dao = RoleDAO(session_id)
        props = dao.get_role_props(name)
        dao.close()

        resp = make_response(json_serialize(props, session_id=session_id), OK)
        resp.contenttype = 'application/json'
        return resp
