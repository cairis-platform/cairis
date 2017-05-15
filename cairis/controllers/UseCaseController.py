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
from cairis.data.UseCaseDAO import UseCaseDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import UseCaseMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import UseCaseModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class UseCasesAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all usecases',
    nickname='usecases-get',
    responseClass=UseCaseModel.__name__,
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

    dao = UseCaseDAO(session_id)
    usecases = dao.get_usecases(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(usecases, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Creates a new usecase',
    nickname='usecases-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new usecase to be added",
        "required": True,
        "allowMultiple": False,
        "type": UseCaseMessage.__name__,
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

    dao = UseCaseDAO(session_id)
    new_usecase,ucContribs = dao.from_json(request)
    usecase_id = dao.add_usecase(new_usecase)
    for rc in ucContribs:
      dao.assign_usecase_contribution(rc)
    dao.close()

    resp_dict = {'message': 'UseCase successfully added', 'usecase_id': usecase_id}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class UseCaseByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a usecase by name',
    nickname='usecase-by-name-get',
    responseClass=UseCaseModel.__name__,
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

    dao = UseCaseDAO(session_id)
    usecase = dao.get_usecase_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(usecase, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Docs
  @swagger.operation(
    notes='Updates a usecase',
    nickname='usecase-by-name-put',
    parameters=[
      {
        'name': 'body',
        "description": "JSON serialized version of the usecase to be updated",
        "required": True,
        "allowMultiple": False,
        'type': UseCaseMessage.__name__,
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
        'message': '''Some parameters are missing. Be sure 'UseCase' is defined.'''
      }
    ]
  )
  # endregion
  def put(self, name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    uc,ucContribs = dao.from_json(request)
    dao.update_usecase(uc, name=name)
    if (len(ucContribs) > 0):
      for rc in ucContribs:
        dao.assign_usecase_contribution(rc)
    else:
      dao.remove_usecase_contributions(uc)
    dao.close()


    resp_dict = {'message': 'UseCase successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing usecase',
    nickname='usecase-by-name-delete',
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
        'message': 'The provided usecase name could not be found in the database'
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

    dao = UseCaseDAO(session_id)
    dao.delete_usecase(name=name)
    dao.close()

    resp_dict = {'message': 'UseCase successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class UseCaseRequirementsByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get requirements associated with usecase ',
    nickname='usecase-requirements-by-name-get',
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
        "name": "usecase_name",
        "description": "The use case name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      }
    ],
    responseMessages=[
      {
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      },
      {
        "code": httplib.CONFLICT,
        "message": "Database conflict"
      }

    ]
  )
  # endregion
  def get(self, usecase_name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    reqs = dao.get_usecase_requirements(usecase_name)
    dao.close()

    resp = make_response(json_serialize(reqs, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class UseCaseGoalsByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get goals associated with usecase ',
    nickname='usecase-requirements-by-name-get',
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
        "name": "usecase_name",
        "description": "The use case name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "environment_name",
        "description": "The environment name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      }
    ],
    responseMessages=[
      {
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      },
      {
        "code": httplib.CONFLICT,
        "message": "Database conflict"
      }

    ]
  )
  # endregion
  def get(self, usecase_name,environment_name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    goals = dao.get_usecase_goals(usecase_name,environment_name)
    dao.close()

    resp = make_response(json_serialize(goals, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class UseCaseExceptionAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Creates a new obstacle from use case exception',
    nickname='usecase-exception-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the exception",
        "required": True,
        "allowMultiple": False,
        "type": UseCaseMessage.__name__,
        "paramType": "body"
      },
      {
        "name": "environment_name",
        "description": "The environment name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "step_name",
        "description": "The step name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "exception_name",
        "description": "The exception name",
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
  def post(self,environment_name,step_name,exception_name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    uc,ucContribs = dao.from_json(request)
    dao.generate_obstacle_from_usecase(uc,environment_name,step_name,exception_name)
    dao.close()

    resp_dict = {'message': 'Obstacle generated from exception'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
