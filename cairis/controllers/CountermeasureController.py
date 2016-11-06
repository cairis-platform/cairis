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
from flask import request, session, make_response
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.CountermeasureDAO import CountermeasureDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import CountermeasureMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import CountermeasureModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class CountermeasuresAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all countermeasures',
    nickname='countermeasures-get',
    responseClass=CountermeasureModel.__name__,
    responseContainer='List',
    parameters=[
      {
        "name": "constraint_id",
        "description": "The constraint to use when querying the database",
        "default": -1,
        "required": False,
        "allowMultiple": False,
        "dataType": int.__name__,
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
  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = CountermeasureDAO(session_id)
    countermeasures = dao.get_countermeasures(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(countermeasures, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Creates a new countermeasure',
    nickname='countermeasures-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new countermeasure to be added",
        "required": True,
        "allowMultiple": False,
        "type": CountermeasureMessage.__name__,
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

    dao = CountermeasureDAO(session_id)
    new_countermeasure = dao.from_json(request)
    countermeasure_id = dao.add_countermeasure(new_countermeasure)
    dao.close()

    resp_dict = {'message': 'Countermeasure successfully added', 'countermeasure_id': countermeasure_id}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class CountermeasureByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a countermeasure by name',
    nickname='countermeasure-by-name-get',
    responseClass=CountermeasureModel.__name__,
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
  def get(self, name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    countermeasure = dao.get_countermeasure_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(countermeasure, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Docs
  @swagger.operation(
    notes='Updates a countermeasure',
    nickname='countermeasure-by-name-put',
    parameters=[
      {
        'name': 'body',
        "description": "JSON serialized version of the countermeasure to be updated",
        "required": True,
        "allowMultiple": False,
        'type': CountermeasureMessage.__name__,
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
        'code': httplib.BAD_REQUEST,
        'message': 'The provided file is not a valid XML file'
      },
      {
        'code': httplib.BAD_REQUEST,
        'message': '''Some parameters are missing. Be sure 'Countermeasure' is defined.'''
      }
    ]
  )
  # endregion
  def put(self, name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    req = dao.from_json(request)
    dao.update_countermeasure(req, name=name)
    dao.close()

    resp_dict = {'message': 'Countermeasure successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing countermeasure',
    nickname='countermeasure-by-name-delete',
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
        'code': httplib.NOT_FOUND,
        'message': 'The provided countermeasure name could not be found in the database'
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
  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    dao.delete_countermeasure(name=name)
    dao.close()

    resp_dict = {'message': 'Countermeasure successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class TargetsAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get countermeasure targets by requirements',
    nickname='countermeasure-targets-by-requirement-get',
    responseClass=list.__name__,
    parameters=[
      {
        "name": "environment",
        "description": "Countermeasure environments",
        "required": False,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "requirements",
        "description": "Countermeasure requirements",
        "required": False,
        "allowMultiple": False,
        "dataType": list.__name__,
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
  def get(self, environment):
    session_id = get_session_id(session, request)
    reqList = request.args.getlist('requirement')
    dao = CountermeasureDAO(session_id)
    targets = dao.get_countermeasure_targets(reqList,environment)
    dao.close()

    resp = make_response(json_serialize(targets, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
    dao.close()
