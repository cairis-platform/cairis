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
from flask_restful import Resource
from cairis.data.ObstacleDAO import ObstacleDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ObstacleMessage
from cairis.tools.ModelDefinitions import ObjectSummaryModel as SwaggerObjectSummaryModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class ObstaclesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = ObstacleDAO(session_id)
    obstacles = dao.get_obstacles(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(obstacles, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    new_obstacle = dao.from_json(request)
    new_obstacle_id = dao.add_obstacle(new_obstacle)
    dao.close()

    resp_dict = {'message': new_obstacle.name() + ' created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ObstacleByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    found_obstacle = dao.get_obstacle_by_name(name)
    dao.close()

    resp = make_response(json_serialize(found_obstacle, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    upd_obs = dao.from_json(request)
    dao.update_obstacle(upd_obs, name)
    dao.close()

    resp_dict = {'message': upd_obs.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    dao.delete_obstacle(name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp


class ObstacleModelAPI(Resource):

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

  def get(self, environment):
    session_id = get_session_id(session, request)

    dao = ObstacleDAO(session_id)
    goals = dao.get_obstacle_names(environment=environment)
    dao.close()

    resp = make_response(json_serialize(goals, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class ObstaclesSummaryAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = ObstacleDAO(session_id)
    objts = dao.get_obstacles_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class GenerateVulnerabilityAPI(Resource):

  def post(self,name):
    session_id = get_session_id(session, request)
    dao = ObstacleDAO(session_id)
    dao.generate_vulnerability(name)
    dao.close()
    resp_dict = {'message': 'Vulnerability successfully generated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
