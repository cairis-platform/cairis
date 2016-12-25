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
from cairis.data.LocationsDAO import LocationsDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import LocationsMessage
from cairis.tools.ModelDefinitions import LocationsModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class LocationsAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all locations',
    responseClass=LocationsModel.__name__,
    nickname='locations-get',
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
    constraint_id = request.args.get('constraint_id', -1)

    dao = LocationsDAO(session_id)
    locs = dao.get_locations(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(locs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Creates new locations',
    nickname='locations-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of new locations to be added",
        "required": True,
        "allowMultiple": False,
        "type": LocationsMessage.__name__,
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

    dao = LocationsDAO(session_id)
    new_locs = dao.from_json(request)
    dao.add_locations(new_locs)
    dao.close()

    resp_dict = {'message': 'Locations successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class LocationsByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get locations by name',
    responseClass=LocationsModel.__name__,
    nickname='locations-by-name-get',
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

    dao = LocationsDAO(session_id)
    found_locs = dao.get_locations_name(name)
    dao.close()

    resp = make_response(json_serialize(found_locs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Updates existing locations',
    nickname='locations-put',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of locations to be updated",
        "required": True,
        "allowMultiple": False,
        "type": LocationsMessage.__name__,
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
  def put(self, name):
    session_id = get_session_id(session, request)

    dao = LocationsDAO(session_id)
    upd_locs = dao.from_json(request)
    dao.update_locations(upd_locs, name)
    dao.close()

    resp_dict = {'message': 'Locations successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Deletes existing locations',
    nickname='locations-by-id-delete',
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
  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = LocationsDAO(session_id)
    dao.delete_locations(name)
    dao.close()

    resp_dict = {'message': 'Locations successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
