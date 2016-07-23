import httplib

from flask import session, request, make_response
from flask.ext.restful import Resource
from flask.ext.restful_swagger import swagger

from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, ARMHTTPError, ObjectNotFoundHTTPError
from cairis.data.ResponseDAO import ResponseDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ResponseMessage
from cairis.tools.ModelDefinitions import ResponseModel as SwaggerResponseModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin'


class ResponsesAPI(Resource):
    #region Swagger Doc
    @swagger.operation(
        notes='Get all responses',
        responseClass=SwaggerResponseModel.__name__,
        nickname='responses-get',
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
                "description": "An ID used to filter the responses",
                "required": False,
                "default": -1,
                "allowMultiple": False,
                "dataType": int.__name__,
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

        dao = ResponseDAO(session_id)
        responses = dao.get_responses(constraint_id)

        resp = make_response(json_serialize(responses, session_id=session_id), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

    #region Swagger Docs
    @swagger.operation(
        notes='Add a new response',
        nickname='responses-post',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the asset to be updated",
                "required": True,
                "allowMultiple": False,
                "type": ResponseMessage.__name__,
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
        dao = ResponseDAO(session_id)
        response = dao.from_json(request)
        response_id = dao.add_response(response)

        resp_dict = {'message': 'Response successfully added', 'response_id': response_id}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.contenttype = 'application/json'
        return resp

class ResponseByNameAPI(Resource):
    #region Swagger Docs
    @swagger.operation(
        notes='Get a response by name',
        nickname='response-by-name-get',
        responseClass=SwaggerResponseModel.__name__,
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
    def get(self, name):
        session_id = get_session_id(session, request)

        dao = ResponseDAO(session_id)
        found_response = dao.get_response_by_name(name)
        dao.close()

        resp = make_response(json_serialize(found_response, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Updates an existing response',
        nickname='response-by-name-put',
        parameters=[
            {
                "name": "body",
                "description": "The session ID and the serialized version of the asset to be updated",
                "required": True,
                "allowMultiple": False,
                "type": SwaggerResponseModel.__name__,
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
    def put(self, name):
        session_id = get_session_id(session, request)

        dao = ResponseDAO(session_id)
        new_response = dao.from_json(request)
        dao.update_response(name, new_response)
        dao.close()

        resp_dict = {'message': 'Response successfully updated'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

    # region Swagger Doc
    @swagger.operation(
        notes='Delete an existing response',
        nickname='response-name-delete',
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
    def delete(self, name):
        session_id = get_session_id(session, request)

        dao = ResponseDAO(session_id)
        dao.delete_response(name)
        dao.close()

        resp_dict = {'message': 'Response successfully deleted'}
        resp = make_response(json_serialize(resp_dict), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp
