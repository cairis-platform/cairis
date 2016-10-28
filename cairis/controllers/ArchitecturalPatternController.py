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
from flask.ext.restful import Resource
from flask.ext.restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.ArchitecturalPatternDAO import ArchitecturalPatternDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ArchitecturalPatternMessage
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ArchitecturalPatternsAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get architectural patterns',
    nickname='architectural-patterns-get',
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
    dao = ArchitecturalPatternDAO(session_id)
    aps = dao.get_architectural_patterns()
    dao.close()
    resp = make_response(json_serialize(aps, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Add architectural pattern',
    nickname='architectural-pattern-add',
    responseClass=str.__name__,
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new architectural pattern to be added",
        "required": True,
        "allowMultiple": False,
        "type": ArchitecturalPatternMessage.__name__,
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
    dao = ArchitecturalPatternDAO(session_id)
    new_ap = dao.from_json(request)
    dao.add_architectural_pattern(new_ap)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully added'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class ArchitecturalPatternByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get architectural patterns',
    nickname='architectural-patterns-get',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Architectural pattern name',
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
    dao = ArchitecturalPatternDAO(session_id)
    ap = dao.get_architectural_pattern(name)
    dao.close()
    resp = make_response(json_serialize(ap, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


  # region Swagger Doc
  @swagger.operation(
    notes='Update architectural pattern',
    nickname='architectural-pattern-update',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Architectural pattern name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        "name": "body",
        "description": "The serialized version of the architectural pattern to be updated",
        "required": True,
        "allowMultiple": False,
        "type": ArchitecturalPatternMessage.__name__,
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
    dao = ArchitecturalPatternDAO(session_id)
    upd_ap = dao.from_json(request)
    dao.update_architectural_pattern(upd_ap,name)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


  # region Swagger Doc
  @swagger.operation(
    notes='Delete an existing architectural patterns',
    nickname='architectural-pattern-by-name-delete',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Architectural pattern name',
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
    dao = ArchitecturalPatternDAO(session_id)
    dao.delete_architectural_pattern(name)
    dao.close()

    resp_dict = {'message': 'Architectural Pattern successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
