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
from flask import session, request, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, ARMHTTPError, ObjectNotFoundHTTPError
from cairis.data.EnvironmentDAO import EnvironmentDAO
from cairis.tools.MessageDefinitions import EnvironmentMessage
from cairis.tools.ModelDefinitions import EnvironmentModel
from cairis.tools.PseudoClasses import EnvironmentTensionModel
from cairis.tools.SessionValidator import get_session_id
from cairis.tools.JsonConverter import json_serialize


__author__ = 'Robin Quetin, Shamal Faily'


class EnvironmentsAPI(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get all environments',
    nickname='environments-get',
    responseClass=EnvironmentModel.__name__,
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
  #endregion
  def get(self):
    session_id = get_session_id(session, request)
    constraintsId = request.args.get('constraints_id', -1)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environments(constraintsId)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  #region Swagger Docs
  const_str = ''
  for key, value in list(EnvironmentTensionModel.attr_dictionary.items()):
    formatted_str = '<br/>- %s: %d' % (key, value)
    const_str += formatted_str
  @swagger.operation(
    notes='Add a new environment.<br/>Constant values for tensions:<br/>'+const_str,
    nickname='environments-post',
    parameters=[
      {
        "name": "body",
        "description": "The session ID and the serialized version of the asset to be updated",
        "required": True,
        "allowMultiple": False,
        "type": EnvironmentMessage.__name__,
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
        "code": BAD_REQUEST,
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
    dao = EnvironmentDAO(session_id)
    new_environment = dao.from_json(request)
    new_environment_id = dao.add_environment(new_environment)
    dao.close()

    resp_dict = {'message': 'Environment successfully added', 'environment_id': new_environment_id}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class EnvironmentByNameAPI(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get an environment by name',
    nickname='environment-by-name-get',
    responseClass=EnvironmentModel.__name__,
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
  #endregion
  def get(self, name):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    found_environment = dao.get_environment_by_name(name)
    dao.close()

    resp = make_response(json_serialize(found_environment, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Updates an existing environment',
    nickname='environment-name-put',
    parameters=[
      {
        "name": "body",
        "description": "The session ID and the serialized version of the asset to be updated",
        "required": True,
        "allowMultiple": False,
        "type": EnvironmentMessage.__name__,
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
    dao = EnvironmentDAO(session_id)
    new_environment = dao.from_json(request)
    dao.update_environment(new_environment, name=name)
    dao.close()

    resp_dict = {'message': 'Environment successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Delete an existing environment',
    nickname='environment-name-delete',
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
    dao = EnvironmentDAO(session_id)
    dao.delete_environment(name=name)
    dao.close()

    resp_dict = {'message': 'Environment successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class EnvironmentsByThreatVulnerability(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get environments in which both the threat as the vulnerability reside in',
    nickname='environment-by-threat-vulnerability-get',
    responseClass=EnvironmentModel.__name__,
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
  #endregion
  def get(self, threat, vulnerability):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environments_by_threat_vulnerability(threat, vulnerability)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class EnvironmentNamesByThreatVulnerability(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get environment names in which both the threat as the vulnerability reside in',
    nickname='environment-names-by-threat-vulnerability-get',
    responseClass=list.__name__,
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
  #endregion
  def get(self, threat, vulnerability):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environment_names_by_threat_vulnerability(threat, vulnerability)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class EnvironmentNamesByRisk(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get environment names a risk reside in',
    nickname='environment-names-by-risk-get',
    responseClass=list.__name__,
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
  #endregion
  def get(self, risk):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environment_names_by_risk(risk)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class EnvironmentNamesAPI(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get all environment names',
    nickname='environment-names-get',
    responseClass=str.__name__,
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
  #endregion
  def get(self):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environment_names = dao.get_environment_names()
    dao.close()

    resp = make_response(json_serialize(environment_names, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
