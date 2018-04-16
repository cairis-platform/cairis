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
from flask import request, session, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.DataFlowDAO import DataFlowDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import DataFlowMessage
from cairis.tools.ModelDefinitions import DataFlowModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class DataFlowsAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all dataflows',
    nickname='dataflows-get',
    responseClass=DataFlowModel.__name__,
    responseContainer='List',
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
    dao = DataFlowDAO(session_id)
    dataflows = dao.get_dataflows()
    dao.close()
    resp = make_response(json_serialize(dataflows, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Creates a new dataflow',
    nickname='dataflows-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new dataflow to be added",
        "required": True,
        "allowMultiple": False,
        "type": DataFlowMessage.__name__,
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
        'code': CONFLICT,
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

    dao = DataFlowDAO(session_id)
    new_dataflow = dao.from_json(request)
    dao.add_dataflow(new_dataflow)
    dao.close()

    resp_dict = {'message': 'DataFlow successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class DataFlowByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a dataflow by name',
    nickname='dataflow-by-name-get',
    responseClass=DataFlowModel.__name__,
    parameters=[
      {
        'name': 'dataflow_name',
        'description': 'Dataflow name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'environment_name',
        'description': 'Environment name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        "name": "session_id",
        "description": "The ID of the user's session",
        "required": False,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
    ],
    responseMessages=[
      {
        "code": BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  # endregion
  def get(self, dataflow_name,environment_name):
    session_id = get_session_id(session, request)

    dao = DataFlowDAO(session_id)
    dataflow = dao.get_dataflow_by_name(dataflow_name,environment_name)
    dao.close()
    resp = make_response(json_serialize(dataflow, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Docs
  @swagger.operation(
    notes='Updates a dataflow',
    nickname='dataflow-by-name-put',
    parameters=[
      {
        'name': 'dataflow_name',
        'description': 'Old dataflow name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'environment_name',
        'description': 'Old environment name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'body',
        "description": "JSON serialized version of the dataflow to be updated",
        "required": True,
        "allowMultiple": False,
        'type': DataFlowMessage.__name__,
        'paramType': 'body'
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
        'message': 'The provided file is not a valid XML file'
      },
      {
        'code': BAD_REQUEST,
        'message': '''Some parameters are missing. Be sure 'DataFlow' is defined.'''
      }
    ]
  )
  # endregion
  def put(self, dataflow_name,environment_name):
    session_id = get_session_id(session, request)
    dao = DataFlowDAO(session_id)
    df = dao.from_json(request)
    dao.update_dataflow(dataflow_name,environment_name,df)
    dao.close()

    resp_dict = {'message': 'DataFlow successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing dataflow',
    nickname='dataflow-by-name-delete',
    parameters=[
      {
        'name': 'dataflow_name',
        'description': 'Dataflow name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'environment_name',
        'description': 'Environment name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
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
        'code': NOT_FOUND,
        'message': 'The provided dataflow name could not be found in the database'
      },
      {
        'code': CONFLICT,
        'message': 'Some problems were found during the name check'
      },
      {
        'code': CONFLICT,
        'message': 'A database error has occurred'
      }
    ]
  )
  # endregion
  def delete(self, dataflow_name,environment_name):
    session_id = get_session_id(session, request)

    dao = DataFlowDAO(session_id)
    dao.delete_dataflow(dataflow_name, environment_name)
    dao.close()

    resp_dict = {'message': 'DataFlow successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class DataFlowDiagramAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get dataflow diagram for a specific environment',
    responseClass=str.__name__,
    nickname='dataflow-diagram-get',
    parameters=[
      {
        "name": "environment_name",
        "description": "The dataflow diagram environment",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "filter_element",
        "description": "The filter element",
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
        "code": BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  #endregion
  def get(self, environment_name,filter_element):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()
    dao = DataFlowDAO(session_id)
    if filter_element == 'None':
      filter_element = ''
    dot_code = dao.get_dataflow_diagram(environment_name,filter_element)
    dao.close()
    resp = make_response(model_generator.generate(dot_code, model_type='dataflow',renderer='dot'), OK)

    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp
