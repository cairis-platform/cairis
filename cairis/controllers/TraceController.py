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
from flask_restful_swagger import swagger
from flask_restful import Resource
from cairis.data.TraceDAO import TraceDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import TraceMessage
from cairis.tools.ModelDefinitions import TraceModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class TraceByEnvironmentAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all traces',
    responseClass=TraceModel.__name__,
    nickname='traces-get',
    parameters=[
      {
        "name": "environment_name",
        "description": "The relevant environment name",
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
  #endregion
  def get(self,environment_name):
    session_id = get_session_id(session, request)

    dao = TraceDAO(session_id)
    trs = dao.get_traces(environment_name)
    dao.close()

    resp = make_response(json_serialize(trs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


class TracesAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Creates a new trace',
    nickname='trace-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new trace to be added",
        "required": True,
        "allowMultiple": False,
        "type": TraceMessage.__name__,
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

    dao = TraceDAO(session_id)
    new_tr = dao.from_json(request)
    dao.add_trace(new_tr)
    dao.close()

    resp_dict = {'message': 'Trace successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class TraceByNameAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing trace',
    nickname='trace-by-id-delete',
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
        'code': httplib.CONFLICT,
        'message': 'A database error has occurred'
      }
    ]
  )
  #endregion
  def delete(self, from_object,from_name,to_object,to_name):
    session_id = get_session_id(session, request)

    dao = TraceDAO(session_id)
    dao.delete_trace(from_object,from_name,to_object,to_name)
    dao.close()

    resp_dict = {'message': 'Trace successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class TraceDimensionsAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get trace dimensions',
    nickname='trace-dimensions',
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
        'code': httplib.CONFLICT,
        'message': 'A database error has occurred'
      }
    ]
  )
  #endregion
  def get(self, dimension_name,is_from):
    session_id = get_session_id(session, request)

    dao = TraceDAO(session_id)
    if is_from == '1':
      is_from = True
    else:
      is_from = False

    dims = dao.trace_dimensions(dimension_name,is_from)
    dao.close()

    resp = make_response(json_serialize(dims, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
