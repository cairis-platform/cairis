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
from cairis.data.TemplateGoalDAO import TemplateGoalDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import TemplateGoalMessage
from cairis.tools.ModelDefinitions import TemplateGoalModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class TemplateGoalsAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all template goals',
    responseClass=TemplateGoalModel.__name__,
    nickname='template_goals-get',
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

    dao = TemplateGoalDAO(session_id)
    tgs = dao.get_template_goals(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(tgs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Creates a new template goal',
    nickname='template_goal-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new template goal to be added",
        "required": True,
        "allowMultiple": False,
        "type": TemplateGoalMessage.__name__,
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

    dao = TemplateGoalDAO(session_id)
    new_tg = dao.from_json(request)
    dao.add_template_goal(new_tg)
    dao.close()

    resp_dict = {'message': 'Template Goal successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class TemplateGoalByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a template goal by name',
    responseClass=TemplateGoalModel.__name__,
    nickname='template_goal-by-name-get',
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

    dao = TemplateGoalDAO(session_id)
    found_tg = dao.get_template_goal(name)
    dao.close()

    resp = make_response(json_serialize(found_tg, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Updates an existing template goal',
    nickname='template_goal-put',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the template goal to be updated",
        "required": True,
        "allowMultiple": False,
        "type": TemplateGoalMessage.__name__,
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

    dao = TemplateGoalDAO(session_id)
    upd_tg = dao.from_json(request)
    dao.update_template_goal(upd_tg, name)
    dao.close()

    resp_dict = {'message': 'Template Goal successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing template goal',
    nickname='template_goal-by-id-delete',
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

    dao = TemplateGoalDAO(session_id)
    dao.delete_template_goal(name)
    dao.close()

    resp_dict = {'message': 'Template Goal successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
