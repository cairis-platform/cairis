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
from cairis.data.RiskDAO import RiskDAO
from cairis.tools.ModelDefinitions import MisuseCaseModel
from cairis.tools.SessionValidator import get_session_id
from cairis.tools.JsonConverter import json_serialize

__author__ = 'Robin Quetin, Shamal Faily'


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


class MisuseCaseByRiskNameAPI(Resource):
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

class MisuseCaseByNameAPI(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get a misuse case by name',
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
  def get(self, misuse_case_name):
    session_id = get_session_id(session, request)

    dao = RiskDAO(session_id)
    found_misuse_case = dao.get_misuse_case_by_name(misuse_case_name)
    dao.close()

    resp = make_response(json_serialize(found_misuse_case, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class MisuseCaseByTVAPI(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get a misuse case by threat and vulnerability',
    nickname='misuse-case-by-threat-vulnerability-get',
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
  def get(self, threat,vulnerability):
    session_id = get_session_id(session, request)

    dao = RiskDAO(session_id)
    template_misuse_case = dao.get_misuse_case_by_threat_vulnerability(threat,vulnerability)
    dao.close()

    resp = make_response(json_serialize(template_misuse_case, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
