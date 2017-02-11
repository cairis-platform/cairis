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
from cairis.data.ConceptReferenceDAO import ConceptReferenceDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ConceptReferenceMessage
from cairis.tools.ModelDefinitions import ConceptReferenceModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ConceptReferencesAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all concept references',
    responseClass=ConceptReferenceModel.__name__,
    nickname='concept_references-get',
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

    dao = ConceptReferenceDAO(session_id)
    crs = dao.get_concept_references(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(crs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Creates a new concept reference',
    nickname='concept_reference-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new concept reference to be added",
        "required": True,
        "allowMultiple": False,
        "type": ConceptReferenceMessage.__name__,
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

    dao = ConceptReferenceDAO(session_id)
    new_cr = dao.from_json(request)
    dao.add_concept_reference(new_cr)
    dao.close()

    resp_dict = {'message': 'Concept Reference successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class ConceptReferenceByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a concept reference by name',
    responseClass=ConceptReferenceModel.__name__,
    nickname='concept_reference-by-name-get',
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

    dao = ConceptReferenceDAO(session_id)
    found_cr = dao.get_concept_reference(name)
    dao.close()

    resp = make_response(json_serialize(found_cr, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Updates an existing concept reference',
    nickname='concept_reference-put',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the concept reference to be updated",
        "required": True,
        "allowMultiple": False,
        "type": ConceptReferenceMessage.__name__,
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

    dao = ConceptReferenceDAO(session_id)
    upd_cr = dao.from_json(request)
    dao.update_concept_reference(upd_cr, name)
    dao.close()

    resp_dict = {'message': 'Concept Reference successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing concept reference',
    nickname='concept_reference-by-id-delete',
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

    dao = ConceptReferenceDAO(session_id)
    dao.delete_concept_reference(name)
    dao.close()

    resp_dict = {'message': 'Concept Reference successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
