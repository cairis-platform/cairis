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
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, ARMHTTPError, ObjectNotFoundHTTPError
from cairis.data.RiskDAO import RiskDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import RiskMessage
from cairis.tools.ModelDefinitions import RiskModel as SwaggerRiskModel
from cairis.tools.PseudoClasses import RiskScore
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Robin Quetin, Shamal Faily'


class RisksAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all risks',
    responseClass=SwaggerRiskModel.__name__,
    nickname='risks-get',
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
        "description": "An ID used to filter the risks",
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

    dao = RiskDAO(session_id)
    risks = dao.get_risks(constraint_id)
    resp = make_response(json_serialize(risks, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  #region Swagger Docs
  @swagger.operation(
    notes='Add a new risk',
    nickname='risks-post',
    parameters=[
      {
        "name": "body",
        "description": "The session ID and the serialized version of the asset to be updated",
        "required": True,
        "allowMultiple": False,
        "type": RiskMessage.__name__,
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

    dao = RiskDAO(session_id)
    risk = dao.from_json(request)
    risk_id = dao.add_risk(risk)

    resp_dict = {'message': 'Risk successfully added', 'risk_id': risk_id}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class RiskByNameAPI(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get a risk by name',
    nickname='risk-by-name-get',
    responseClass=SwaggerRiskModel.__name__,
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

    dao = RiskDAO(session_id)
    found_risk = dao.get_risk_by_name(name)
    dao.close()

    resp = make_response(json_serialize(found_risk, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Updates an existing risk',
    nickname='risk-by-name-put',
    parameters=[
      {
        "name": "body",
        "description": "The session ID and the serialized version of the asset to be updated",
        "required": True,
        "allowMultiple": False,
        "type": SwaggerRiskModel.__name__,
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
    dao = RiskDAO(session_id)
    new_risk = dao.from_json(request)
    dao.update_risk(name, new_risk)
    dao.close()

    resp_dict = {'message': 'Risk successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Delete an existing risk',
    nickname='risk-name-delete',
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
    dao = RiskDAO(session_id)
    dao.delete_risk(name)
    dao.close()

    resp_dict = {'message': 'Risk successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class RiskAnalysisModelAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get risk model',
    responseClass=str.__name__,
    nickname='risk-analysis-model-get',
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
  def get(self, environment):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()
    dim_name = request.args.get('dimension_name', '')
    obj_name = request.args.get('object_name', '')
    model_layout = request.args.get('layout','Hierarchical')

    if dim_name == 'all': dim_name = ''
    if obj_name == 'all': obj_name = ''

    if model_layout == 'Hierarchical':
      renderer = 'dot'
    elif model_layout == 'Spring':
      renderer = 'fdp'
    elif model_layout == 'Radial':
      renderer = 'twopi'
    else:
      renderer = 'circo'

    dao = RiskDAO(session_id)
    dot_code = dao.get_risk_analysis_model(environment, dim_name, obj_name, renderer)
    dao.close()

    resp = make_response(model_generator.generate(dot_code, model_type='risk', renderer=renderer), httplib.OK)

    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp


class RisksScoreByNameAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get risk scores for a risk in a specific situation',
    responseClass=RiskScore.__name__,
    nickname='risks-scores-by-rtve-get',
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
  def get(self, name, threat, vulnerability, environment):
    session_id = get_session_id(session, request)

    dao = RiskDAO(session_id)
    risk_scores = dao.get_scores_by_rtve(name, threat, vulnerability, environment)

    resp = make_response(json_serialize(risk_scores, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class RisksRatingByNameAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get risk rating for a risk in a specific situation',
    responseClass=str.__name__,
    nickname='risks-rating-by-tve-get',
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
  def get(self, threat, vulnerability, environment):
    session_id = get_session_id(session, request)

    dao = RiskDAO(session_id)
    risk_rating = dao.get_risk_rating_by_tve(threat, vulnerability, environment)

    resp = make_response(json_serialize(risk_rating, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class RiskAnalysisModelNamesAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get risk model object names',
    responseClass=str.__name__,
    nickname='risk-analysis-model-get-names',
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
  def get(self, environment):
    session_id = get_session_id(session, request)
    dao = RiskDAO(session_id)
    element_names = dao.risk_model_elements(environment)
    resp = make_response(json_serialize(element_names, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
