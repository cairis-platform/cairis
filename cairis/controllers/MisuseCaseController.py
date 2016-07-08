import httplib

from flask import session, request, make_response
from flask.ext.restful import Resource
from flask.ext.restful_swagger import swagger

from cairis.data.RiskDAO import RiskDAO
from cairis.tools.ModelDefinitions import MisuseCaseModel
from cairis.tools.SessionValidator import get_session_id
from cairis.tools.JsonConverter import json_serialize


__author__ = 'Robin Quetin'


class MisuseCasesAPI(Resource):
    #region Swagger Docs
    @swagger.operation(
        notes='Get all misuse cases',
        nickname='misuse-cases-get',
        responseClass=MisuseCaseModel.__name__,
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
        constraintsId = request.args.get('constraints_id', -1)

        dao = RiskDAO(session_id)
        misuse_cases = dao.get_misuse_cases(constraintsId)
        dao.close()

        resp = make_response(json_serialize(misuse_cases, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp


class MisuseCaseByNameAPI(Resource):
    #region Swagger Docs
    @swagger.operation(
        notes='Get a misuse case associated with a certain risk',
        nickname='misuse-case-by-risk-name-get',
        responseClass=MisuseCaseModel.__name__,
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
    def get(self, risk_name):
        session_id = get_session_id(session, request)

        dao = RiskDAO(session_id)
        found_misuse_case = dao.get_misuse_case_by_risk_name(risk_name)
        dao.close()

        resp = make_response(json_serialize(found_misuse_case, session_id=session_id), httplib.OK)
        resp.headers['Content-type'] = 'application/json'
        return resp
