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
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.TrustBoundaryDAO import TrustBoundaryDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import TrustBoundaryMessage
from cairis.tools.ModelDefinitions import TrustBoundaryModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class TrustBoundariesAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all trust boundaries',
    nickname='trustboundaries-get',
    responseClass=TrustBoundaryModel.__name__,
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
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  #endregion
  def get(self):
    session_id = get_session_id(session, request)
    dao = TrustBoundaryDAO(session_id)
    tbs = dao.get_trust_boundaries()
    dao.close()
    resp = make_response(json_serialize(tbs, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Creates a new trust boundary',
    nickname='trustboundary-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new trustboundary to be added",
        "required": True,
        "allowMultiple": False,
        "type": TrustBoundaryMessage.__name__,
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

    dao = TrustBoundaryDAO(session_id)
    new_tb = dao.from_json(request)
    dao.add_trust_boundary(new_tb)
    dao.close()

    resp_dict = {'message': 'TrustBoundary successfully added'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class TrustBoundaryByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a trust boundary by name',
    nickname='trustboundary-by-name-get',
    responseClass=TrustBoundaryModel.__name__,
    parameters=[
      {
        'name': 'trust_boundary_name',
        'description': 'Trust Boundary name',
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
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  # endregion
  def get(self, trust_boundary_name):
    session_id = get_session_id(session, request)

    dao = TrustBoundaryDAO(session_id)
    tb = dao.get_trust_boundary_by_name(trust_boundary_name)
    dao.close()
    resp = make_response(json_serialize(tb, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Docs
  @swagger.operation(
    notes='Updates a trust boundary',
    nickname='trust_boundary-by-name-put',
    parameters=[
      {
        'name': 'trust_boundary_name',
        'description': 'Old trust boundary name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'body',
        "description": "JSON serialized version of the trust boundary to be updated",
        "required": True,
        "allowMultiple": False,
        'type': TrustBoundaryMessage.__name__,
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
        'message': '''Some parameters are missing. Be sure 'TrustBoundary' is defined.'''
      }
    ]
  )
  # endregion
  def put(self, trust_boundary_name):
    session_id = get_session_id(session, request)

    dao = TrustBoundaryDAO(session_id)
    tb = dao.from_json(request)
    dao.update_trust_boundary(trust_boundary_name,tb)
    dao.close()

    resp_dict = {'message': 'TrustBoundary successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing trust boundary',
    nickname='trust_boundary-by-name-delete',
    parameters=[
      {
        'name': 'trust_boundary_name',
        'description': 'Dataflow name',
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
        'code': httplib.BAD_REQUEST,
        'message': 'One or more attributes are missing'
      },
      {
        'code': httplib.NOT_FOUND,
        'message': 'The provided trustboundary name could not be found in the database'
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
  def delete(self, trust_boundary_name):
    session_id = get_session_id(session, request)

    dao = TrustBoundaryDAO(session_id)
    dao.delete_trust_boundary(trust_boundary_name)
    dao.close()

    resp_dict = {'message': 'TrustBoundary successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
