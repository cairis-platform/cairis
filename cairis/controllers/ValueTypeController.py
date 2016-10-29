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
from flask.ext.restful_swagger import swagger
from flask_restful import Resource
from cairis.data.ValueTypeDAO import ValueTypeDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ValueTypeMessage
from cairis.tools.ModelDefinitions import ValueTypeModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ValueTypesAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all value types.',
    responseClass=ValueTypeModel.__name__,
    nickname='value_types-get',
    parameters=[
      {
        "name": "type_name",
        "description": "The Value Type name",
        "required": True,
        "default": -1,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "environment_name",
        "description": "The Value Type environment",
        "required": False,
        "default": "all",
        "allowMultiple": False,
        "dataType": str.__name__,
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
  def get(self,type_name,environment_name):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    if environment_name == 'all':
      environment_name = ''
    vts = dao.get_value_types(type_name,environment_name)
    dao.close()

    resp = make_response(json_serialize(vts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


class ValueTypesCreateAPI(Resource):

  #region Swagger Doc
  @swagger.operation(
    notes='Creates a new value type',
    nickname='value_type-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new value type to be added",
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
  #endregion
  def post(self):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    new_vt = dao.from_json(request)
    dao.add_value_type(new_vt)
    dao.close()

    resp_dict = {'message': 'Value Type successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class ValueTypesByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a value type by name',
    responseClass=ValueTypeModel.__name__,
    nickname='value_type-by-name-get',
    parameters=[
      {
        "name": "type_name",
        "description": "The Value Type name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "environment_name",
        "description": "The Value Type environment",
        "required": False,
        "default": "all",
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "object_name",
        "description": "The Value Type object",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
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
  # endregion
  def get(self, type_name,environment_name,object_name):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    found_vt = dao.get_value_type(type_name,environment_name,object_name)
    dao.close()

    resp = make_response(json_serialize(found_vt, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


  #region Swagger Doc
  @swagger.operation(
    notes='Updates an existing value type',
    nickname='value_types-put',
    parameters=[
      {
        "name": "type_name",
        "description": "The Value Type name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "environment_name",
        "description": "The Value Type environment",
        "required": False,
        "default": "all",
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "object_name",
        "description": "The Value Type object",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "body",
        "description": "The serialized version of the value type to be updated",
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
  #endregion
  def put(self, type_name, environment_name, object_name):
    session_id = get_session_id(session, request)
    import pytest
    pytest.set_trace()
    dao = ValueTypeDAO(session_id)
    upd_vt = dao.from_json(request)
    dao.update_value_type(upd_vt, type_name, environment_name, object_name)
    dao.close()

    resp_dict = {'message': 'Value Type successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing value type',
    nickname='value_type-by-id-delete',
    parameters=[
      {
        "name": "type_name",
        "description": "The Value Type name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "environment_name",
        "description": "The Value Type environment",
        "required": False,
        "default": "all",
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "object_name",
        "description": "The Value Type object",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
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
  #endregion
  def delete(self, type_name, environment_name, object_name):
    session_id = get_session_id(session, request)

    dao = ValueTypeDAO(session_id)
    dao.delete_value_type(type_name,environment_name,object_name)
    dao.close()

    resp_dict = {'message': 'Value Type successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
