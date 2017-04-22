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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError
from cairis.data.SecurityPatternDAO import SecurityPatternDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import SecurityPatternMessage
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class SecurityPatternsAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get security patterns',
    nickname='security-patterns-get',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      }
    ],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The database connection was not properly setup'
      },
    ]
  )
  # endregion
  def get(self):
    session_id = get_session_id(session, request)
    dao = SecurityPatternDAO(session_id)
    sps = dao.get_security_patterns()
    dao.close()
    resp = make_response(json_serialize(sps, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Add security pattern',
    nickname='security-pattern-add',
    responseClass=str.__name__,
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new security pattern to be added",
        "required": True,
        "allowMultiple": False,
        "type": SecurityPatternMessage.__name__,
        "paramType": "body"
      },
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      }
    ],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The database connection was not properly setup'
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
    dao = SecurityPatternDAO(session_id)
    new_sp = dao.from_json(request)
    dao.add_security_pattern(new_sp)
    dao.close()
    resp_dict = {'message': 'Security Pattern successfully added'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class SecurityPatternByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get security patterns by name',
    nickname='security-patterns-get-by-name',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Security pattern name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      }
    ],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The database connection was not properly setup'
      },
    ]
  )
  # endregion
  def get(self,name):
    session_id = get_session_id(session, request)
    dao = SecurityPatternDAO(session_id)
    sp = dao.get_security_pattern(name)
    dao.close()
    resp = make_response(json_serialize(sp, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


  # region Swagger Doc
  @swagger.operation(
    notes='Update security pattern',
    nickname='security-pattern-update',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Security pattern name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        "name": "body",
        "description": "The serialized version of the security pattern to be updated",
        "required": True,
        "allowMultiple": False,
        "type": SecurityPatternMessage.__name__,
        "paramType": "body"
      },
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      }
    ],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The database connection was not properly setup'
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
  def put(self,name):
    session_id = get_session_id(session, request)
    dao = SecurityPatternDAO(session_id)
    upd_sp = dao.from_json(request)
    dao.update_security_pattern(upd_sp,name)
    dao.close()
    resp_dict = {'message': 'Security Pattern successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


  # region Swagger Doc
  @swagger.operation(
    notes='Delete an existing security patterns',
    nickname='security-pattern-by-name-delete',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Security pattern name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      }
    ],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The database connection was not properly setup'
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
  def delete(self,name):
    session_id = get_session_id(session, request)
    dao = SecurityPatternDAO(session_id)
    dao.delete_security_pattern(name)
    dao.close()

    resp_dict = {'message': 'Security Pattern successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class SituateSecurityPatternAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Situate security pattern',
    nickname='security-patterns-situate-post',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'security_pattern_name',
        'description': 'The security pattern name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'environment_name',
        'description': 'The environment name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      }
    ],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The database connection was not properly setup'
      },
    ]
  )
  # endregion
  def post(self,security_pattern_name,environment_name):
    session_id = get_session_id(session, request)
    dao = SecurityPatternDAO(session_id)
    dao.situate_security_pattern(security_pattern_name,environment_name)
    dao.close()
    resp_dict = {'message': 'Security Pattern successfully situated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
