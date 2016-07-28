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
from flask import request, session, make_response
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.AttackerDAO import AttackerDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import AttackerMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import AttackerModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin'


class AttackersAPI(Resource):
    #region Swagger Doc
    @swagger.operation(
        notes='Get all attackers',
        nickname='attackers-get',
        responseClass=AttackerModel.__name__,
        responseContainer='List',
        parameters=[
            {
                "name": "constraint_id",
                "description": "The constraint to use when querying the database",
                "default": -1,
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
            }
        ]
    )
    #endregion
    def get(self):
        session_id = get_session_id(session, request)
        constraint_id = request.args.get('constraint_id', -1)

        dao = AttackerDAO(session_id)
        attackers = dao.get_attackers(constraint_id=constraint_id)
        dao.close()

        resp = make_response(json_serialize(attackers, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new attacker',
        nickname='attackers-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new attacker to be added",
                "required": True,
                "allowMultiple": False,
                "type": AttackerMessage.__name__,
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
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
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

        dao = AttackerDAO(session_id)
        new_attacker = dao.from_json(request)
        attacker_id = dao.add_attacker(new_attacker)
        dao.close()

        resp_dict = {'message': 'Attacker successfully added', 'attacker_id': attacker_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class AttackerByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get an attacker by name',
        nickname='attacker-by-name-get',
        responseClass=AttackerModel.__name__,
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
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)

        dao = AttackerDAO(session_id)
        attacker = dao.get_attacker_by_name(name=name)
        dao.close()

        resp = make_response(json_serialize(attacker, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates an attacker',
        nickname='attacker-by-name-put',
        parameters=[
            {
                'name': 'body',
                "description": "JSON serialized version of the attacker to be updated",
                "required": True,
                "allowMultiple": False,
                'type': AttackerMessage.__name__,
                'paramType': 'body'
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
                'message': 'The provided file is not a valid XML file'
            },
            {
                'code': httplib.BAD_REQUEST,
                'message': '''Some parameters are missing. Be sure 'attacker' is defined.'''
            }
        ]
    )
    # endregion
    def put(self, name):
        session_id = get_session_id(session, request)

        dao = AttackerDAO(session_id)
        req = dao.from_json(request)
        dao.update_attacker(req, name=name)
        dao.close()

        resp_dict = {'message': 'Attacker successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing attacker',
        nickname='attacker-by-name-delete',
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
                'code': httplib.BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.NOT_FOUND,
                'message': 'The provided attacker name could not be found in the database'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def delete(self, name):
        session_id = get_session_id(session, request)

        dao = AttackerDAO(session_id)
        dao.delete_attacker(name=name)
        dao.close()

        resp_dict = {'message': 'Attacker successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

class AttackerCapabilitiesAPI(Resource):
    #region Swagger Doc
    @swagger.operation(
        notes='Get all attacker capabilities',
        nickname='attacker-capabilities-get',
        responseClass=ValueTypeModel.__name__,
        responseContainer='List',
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
    def get(self):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        assets = dao.get_attacker_capabilities(environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(assets, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new attacker capability',
        nickname='attacker-capability-by-name-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new attacker capability to be added",
                "required": True,
                "allowMultiple": False,
                "type": ValueTypeMessage.__name__,
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
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def post(self):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        new_value_type = dao.type_from_json(request)
        attacker_capability_id = dao.add_attacker_capability(new_value_type, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Attacker capability successfully added', 'attacker_capability_id': attacker_capability_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class AttackerCapabilityByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get an attacker capability by name',
        nickname='attacker-capability-by-name-get',
        responseClass=ValueTypeModel.__name__,
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
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        attacker_capability = dao.get_attacker_capability_by_name(name=name, environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(attacker_capability, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates an attacker capability',
        nickname='attacker-capability-by-name-put',
        parameters=[
            {
                'name': 'body',
                "description": "",
                "required": True,
                "allowMultiple": False,
                'type': ValueTypeMessage.__name__,
                'paramType': 'body'
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
                'message': 'The provided file is not a valid XML file'
            },
            {
                'code': httplib.BAD_REQUEST,
                'message': '''Some parameters are missing. Be sure 'asset' is defined.'''
            }
        ]
    )
    # endregion
    def put(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        attacker_capability = dao.type_from_json(request)
        dao.update_attacker_capability(attacker_capability, name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Attacker capability successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing attacker capability',
        nickname='attacker-capability-by-name-delete',
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
                'code': httplib.BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.NOT_FOUND,
                'message': 'The provided asset name could not be found in the database'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def delete(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        dao.delete_attacker_capability(name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Attacker capability successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

class AttackerMotivationsAPI(Resource):
    #region Swagger Doc
    @swagger.operation(
        notes='Get all attacker motivations',
        nickname='attackers-motivations-get',
        responseClass=ValueTypeModel.__name__,
        responseContainer='List',
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
    def get(self):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        assets = dao.get_attacker_motivations(environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(assets, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new attacker motivation',
        nickname='attacker-motivation-by-name-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new attacker motivation to be added",
                "required": True,
                "allowMultiple": False,
                "type": ValueTypeMessage.__name__,
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
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def post(self):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        new_value_type = dao.type_from_json(request)
        attacker_motivation_id = dao.add_attacker_motivation(new_value_type, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Attacker motivation successfully added', 'attacker_motivation_id': attacker_motivation_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class AttackerMotivationByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get an attacker motivation by name',
        nickname='attacker-motivation-by-name-get',
        responseClass=ValueTypeModel.__name__,
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
    # endregion
    def get(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        attacker_motivation = dao.get_attacker_motivation_by_name(name=name, environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(attacker_motivation, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates an attacker motivation',
        nickname='attacker-motivation-by-name-put',
        parameters=[
            {
                'name': 'body',
                "description": "",
                "required": True,
                "allowMultiple": False,
                'type': ValueTypeMessage.__name__,
                'paramType': 'body'
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
                'message': 'The provided file is not a valid XML file'
            },
            {
                'code': httplib.BAD_REQUEST,
                'message': '''Some parameters are missing. Be sure 'asset' is defined.'''
            }
        ]
    )
    # endregion
    def put(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        attacker_motivation = dao.type_from_json(request)
        dao.update_attacker_motivation(attacker_motivation, name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Attacker motivation successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing attacker motivation',
        nickname='attacker-motivation-by-name-delete',
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
                'code': httplib.BAD_REQUEST,
                'message': 'One or more attributes are missing'
            },
            {
                'code': httplib.NOT_FOUND,
                'message': 'The provided asset name could not be found in the database'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'Some problems were found during the name check'
            },
            {
                'code': httplib.CONFLICT,
                'message': 'A database error has occurred'
            }
        ]
    )
    # endregion
    def delete(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = AttackerDAO(session_id)
        dao.delete_attacker_motivation(name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Attacker motivation successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp
