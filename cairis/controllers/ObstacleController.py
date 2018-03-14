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
from flask import session, request, make_response
from flask_restful_swagger import swagger
from flask_restful import Resource
from cairis.data.ObstacleDAO import ObstacleDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ObstacleMessage
from cairis.tools.ModelDefinitions import ObstacleModel as SwaggerObstacleModel
from cairis.tools.ModelDefinitions import ObjectSummaryModel as SwaggerObjectSummaryModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class ObstaclesAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all obstacles.',
    responseClass=SwaggerObstacleModel.__name__,
    nickname='obstacles-get',
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
    constraint_id = request.args.get('constraint_id', -1)

    dao = ObstacleDAO(session_id)
    obstacles = dao.get_obstacles(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(obstacles, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Creates a new obstacle',
    nickname='obstacle-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new obstacle to be added",
        "required": True,
        "allowMultiple": False,
        "type": ObstacleMessage.__name__,
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
      }
    ]
  )
  #endregion
  def post(self):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    new_obstacle = dao.from_json(request)
    new_obstacle_id = dao.add_obstacle(new_obstacle)
    dao.close()

    resp_dict = {'message': 'Obstacle successfully added', 'obstacle_id': new_obstacle_id}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ObstacleByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get an obstacle by name',
    responseClass=SwaggerObstacleModel.__name__,
    nickname='obstacle-by-name-get',
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
  def get(self, name):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    found_obstacle = dao.get_obstacle_by_name(name)
    dao.close()

    resp = make_response(json_serialize(found_obstacle, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Updates an existing obstacle',
    nickname='obstacle-put',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the obstacle to be updated",
        "required": True,
        "allowMultiple": False,
        "type": ObstacleMessage.__name__,
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
      }
    ]
  )
  #endregion
  def put(self, name):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    upd_obs = dao.from_json(request)
    dao.update_obstacle(upd_obs, name)
    dao.close()

    resp_dict = {'message': 'Obstacle successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  #region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing obstacle',
    nickname='obstacle-by-id-delete',
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
      }
    ]
  )
  #endregion
  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    dao.delete_obstacle(name)
    dao.close()

    resp_dict = {'message': 'Obstacle successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp


class ObstacleModelAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get the obstacle model for a specific environment',
    responseClass=SwaggerObstacleModel.__name__,
    nickname='obstacle-by-name-get',
    parameters=[
      {
        "name": "environment",
        "description": "The obstacle model environment",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "goal",
        "description": "The obstacle model filtering goal",
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
      },
      {
        "code": NOT_FOUND,
        "message": "Environment not found"
      },
      {
        "code": BAD_REQUEST,
        "message": "Environment not defined"
      }
    ]
  )
  # endregion
  def get(self, environment, obstacle):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = ObstacleDAO(session_id)
    if obstacle == 'all':  obstacle = ''
    dot_code = dao.get_obstacle_model(environment,obstacle)
    dao.close()

    resp = make_response(model_generator.generate(dot_code, model_type='obstacle',renderer='dot'), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp

class ObstacleByEnvironmentNamesAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get all the obstacle names associated with a specific environment',
    responseClass=SwaggerObstacleModel.__name__,
    nickname='obstacles-by-environment-names-get',
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
  def get(self, environment):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    goals = dao.get_obstacle_names(environment=environment)
    dao.close()

    resp = make_response(json_serialize(goals, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class ObstaclesSummaryAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get summary of obstacles',
    responseClass=SwaggerObjectSummaryModel.__name__,
    nickname='obstacles-summary-get',
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
  def get(self):
    session_id = get_session_id(session, request)
    dao = ObstacleDAO(session_id)
    objts = dao.get_obstacles_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class GenerateVulnerabilityAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Generates a vulnerability based on an obstacle',
    nickname='generate-vulnerability',
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
        'code': CONFLICT,
        'message': 'A database error has occurred'
      }
    ]
  )
  #endregion
  def post(self,name):
    session_id = get_session_id(session, request)
    dao = ObstacleDAO(session_id)
    dao.generate_vulnerability(name)
    dao.close()
    resp_dict = {'message': 'Vulnerability successfully generated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
