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
from cairis.data.TemplateAssetDAO import TemplateAssetDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import TemplateAssetMessage
from cairis.tools.ModelDefinitions import TemplateAssetModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class TemplateAssetsAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all template assets',
    responseClass=TemplateAssetModel.__name__,
    nickname='template_assets-get',
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

    dao = TemplateAssetDAO(session_id)
    tas = dao.get_template_assets(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(tas, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Creates a new template asset',
    nickname='template_asset-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new template asset to be added",
        "required": True,
        "allowMultiple": False,
        "type": TemplateAssetMessage.__name__,
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
    dao = TemplateAssetDAO(session_id)
    new_ta = dao.from_json(request)
    dao.add_template_asset(new_ta)
    dao.close()

    resp_dict = {'message': 'Template Asset successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class TemplateAssetByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a template asset by name',
    responseClass=TemplateAssetModel.__name__,
    nickname='template_asset-by-name-get',
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

    dao = TemplateAssetDAO(session_id)
    found_ta = dao.get_template_asset(name)
    dao.close()

    resp = make_response(json_serialize(found_ta, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Updates an existing template asset',
    nickname='template_asset-put',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the template asset to be updated",
        "required": True,
        "allowMultiple": False,
        "type": TemplateAssetMessage.__name__,
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
    dao = TemplateAssetDAO(session_id)
    upd_ta = dao.from_json(request)
    dao.update_template_asset(upd_ta, name)
    dao.close()

    resp_dict = {'message': 'Template Asset successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing template asset',
    nickname='template_asset-by-id-delete',
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

    dao = TemplateAssetDAO(session_id)
    dao.delete_template_asset(name)
    dao.close()

    resp_dict = {'message': 'Template Asset successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
