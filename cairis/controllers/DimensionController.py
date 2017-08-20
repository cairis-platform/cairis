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
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError
from cairis.data.DimensionDAO import DimensionDAO
from cairis.tools.JsonConverter import json_serialize

__author__ = 'Robin Quetin, Shamal Faily'


class DimensionsAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get all dimensions of a specific table',
    nickname='dimensions-table-get',
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
        "description": "The ID of the constraint used when obtaining the data",
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
        "code": CONFLICT,
        "message": "Database conflict"
      }
    ]
  )
  # endregion
  def get(self, table):
    session_id = request.args.get('session_id', None)
    id = request.args.get('constraint_id', -1)
    dao = DimensionDAO(session_id)
    dimension_names = dao.getDimensions(table,id)
    dao.close()

    resp = make_response(json_serialize(dimension_names, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class DimensionNamesAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get all dimensions of a specific table in a specific environment',
    nickname='dimensions-table-environment-get',
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
  # endregion
  def get(self, table, environment):
    session_id = request.args.get('session_id', None)

    dao = DimensionDAO(session_id)
    dimension_names = dao.getDimensionNames(table,environment)
    dao.close()

    resp = make_response(json_serialize(dimension_names, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
