import httplib

from flask import request, session, make_response
from flask.ext.restful import Resource
from flask_restful_swagger import swagger

from cairis.data.ThreatDAO import ThreatDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ThreatMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import ThreatModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id


__author__ = 'Robin Quetin'


class ThreatAPI(Resource):
    #region Swagger Doc
    @swagger.operation(
        notes='Get all threats',
        nickname='threats-get',
        responseClass=ThreatModel.__name__,
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
            }
        ]
    )
    #endregion
    def get(self):
        session_id = get_session_id(session, request)
        constraint_id = request.args.get('constraint_id', -1)

        dao = ThreatDAO(session_id)
        threats = dao.get_threats(constraint_id=constraint_id)
        dao.close()

        resp = make_response(json_serialize(threats, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new threat',
        nickname='threats-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new threat to be added",
                "required": True,
                "allowMultiple": False,
                "type": ThreatMessage.__name__,
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

        dao = ThreatDAO(session_id)
        new_threat = dao.from_json(request)
        threat_id = dao.add_threat(new_threat)
        dao.close()

        resp_dict = {'message': 'Threat successfully added', 'threat_id': threat_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class ThreatByIdAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a threat by ID',
        nickname='threat-by-id-get',
        responseClass=ThreatModel.__name__,
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
    def get(self, id):
        session_id = get_session_id(session, request)

        dao = ThreatDAO(session_id)
        threat = dao.get_threat_by_id(threat_id=id)
        dao.close()

        resp = make_response(json_serialize(threat, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

class ThreatByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a threat by name',
        nickname='threat-by-name-get',
        responseClass=ThreatModel.__name__,
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

        dao = ThreatDAO(session_id)
        threat = dao.get_threat_by_name(name=name)
        dao.close()

        resp = make_response(json_serialize(threat, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates a threat',
        nickname='threat-by-name-put',
        parameters=[
            {
                'name': 'body',
                "description": "JSON serialized version of the threat to be updated",
                "required": True,
                "allowMultiple": False,
                'type': ThreatMessage.__name__,
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
                'message': '''Some parameters are missing. Be sure 'threat' is defined.'''
            }
        ]
    )
    # endregion
    def put(self, name):
        session_id = get_session_id(session, request)

        dao = ThreatDAO(session_id)
        req = dao.from_json(request)
        dao.update_threat(req, name=name)
        dao.close()

        resp_dict = {'message': 'Threat successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing threat',
        nickname='threat-by-name-delete',
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
                'message': 'The provided threat name could not be found in the database'
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

        dao = ThreatDAO(session_id)
        dao.delete_threat(name=name)
        dao.close()

        resp_dict = {'message': 'Threat successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

class ThreatTypesAPI(Resource):
    #region Swagger Doc
    @swagger.operation(
        notes='Get all threat types',
        nickname='threats-types-get',
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

        dao = ThreatDAO(session_id)
        threats = dao.get_threat_types(environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(threats, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Creates a new threat type',
        nickname='threat-type-by-name-post',
        parameters=[
            {
                "name": "body",
                "description": "The serialized version of the new threat type to be added",
                "required": True,
                "allowMultiple": False,
                "type": ThreatMessage.__name__,
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

        dao = ThreatDAO(session_id)
        new_value_type = dao.type_from_json(request)
        threat_type_id = dao.add_threat_type(new_value_type, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Threat type successfully added', 'threat_type_id': threat_type_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class ThreatTypeByNameAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get a threat type by name',
        nickname='threat-type-by-name-get',
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

        dao = ThreatDAO(session_id)
        threat_type = dao.get_threat_type_by_name(name=name, environment_name=environment_name)
        dao.close()

        resp = make_response(json_serialize(threat_type, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Docs
    @swagger.operation(
        notes='Updates a threat type',
        nickname='threat-type-by-name-put',
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
                'message': '''Some parameters are missing. Be sure 'threat' is defined.'''
            }
        ]
    )
    # endregion
    def put(self, name):
        session_id = get_session_id(session, request)
        environment_name = request.args.get('environment', '')

        dao = ThreatDAO(session_id)
        threat_type = dao.type_from_json(request)
        dao.update_threat_type(threat_type, name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Threat type successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Deletes an existing threat type',
        nickname='threat-type-by-name-delete',
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
                'message': 'The provided threat name could not be found in the database'
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

        dao = ThreatDAO(session_id)
        dao.delete_threat_type(name=name, environment_name=environment_name)
        dao.close()

        resp_dict = {'message': 'Threat type successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp
