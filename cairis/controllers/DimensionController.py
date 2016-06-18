import httplib
from flask import request, session, make_response
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from cairis.core.ARM import DatabaseProxyException
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import validate_proxy

__author__ = 'Robin Quetin'


class DimensionsAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all dimensions of a specific table',
        nickname='dimensions-table-get',
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
                "description": "The ID of the constraint used when obtaining the data",
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
                "code": httplib.CONFLICT,
                "message": "Database conflict"
            }
        ]
    )
    # endregion
    def get(self, table):
        session_id = request.args.get('session_id', None)
        id = request.args.get('constraint_id', -1)
        db_proxy = validate_proxy(session, session_id)

        try:
            dimensions = db_proxy.getDimensions(table, id)
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        finally:
            db_proxy.close()

        resp = make_response(json_serialize(dimensions, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp

class DimensionNamesAPI(Resource):
    # region Swagger Doc
    @swagger.operation(
        notes='Get all dimensions of a specific table in a specific environment',
        nickname='dimensions-table-environment-get',
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
    def get(self, table, environment):
        session_id = request.args.get('session_id', None)

        db_proxy = validate_proxy(session, session_id)
        try:
            dimension_names = db_proxy.getDimensionNames(table, environment)
        except DatabaseProxyException as ex:
            raise ARMHTTPError(ex)
        finally:
            db_proxy.close()

        resp = make_response(json_serialize(dimension_names, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp
