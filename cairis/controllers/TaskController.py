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
from cairis.data.TaskDAO import TaskDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import TaskMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import TaskModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class TasksAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all tasks',
    nickname='tasks-get',
    responseClass=TaskModel.__name__,
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

    dao = TaskDAO(session_id)
    tasks = dao.get_tasks(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(tasks, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Creates a new task',
    nickname='tasks-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new task to be added",
        "required": True,
        "allowMultiple": False,
        "type": TaskMessage.__name__,
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

    dao = TaskDAO(session_id)
    new_task = dao.from_json(request)
    task_id = dao.add_task(new_task)
    dao.close()

    resp_dict = {'message': 'Task successfully added', 'task_id': task_id}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class TaskByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a task by name',
    nickname='task-by-name-get',
    responseClass=TaskModel.__name__,
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

    dao = TaskDAO(session_id)
    task = dao.get_task_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(task, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Docs
  @swagger.operation(
    notes='Updates a task',
    nickname='task-by-name-put',
    parameters=[
      {
        'name': 'body',
        "description": "JSON serialized version of the task to be updated",
        "required": True,
        "allowMultiple": False,
        'type': TaskMessage.__name__,
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
        'message': '''Some parameters are missing. Be sure 'Task' is defined.'''
      }
    ]
  )
  # endregion
  def put(self, name):
    session_id = get_session_id(session, request)

    dao = TaskDAO(session_id)
    req = dao.from_json(request)
    dao.update_task(req, name=name)
    dao.close()

    resp_dict = {'message': 'Task successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing task',
    nickname='task-by-name-delete',
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
        'message': 'The provided task name could not be found in the database'
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

    dao = TaskDAO(session_id)
    dao.delete_task(name=name)
    dao.close()

    resp_dict = {'message': 'Task successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
