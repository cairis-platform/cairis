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
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator
from importlib import import_module


__author__ = 'Shamal Faily'


class ObstacleModelAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ObstacleDAO'),'ObstacleDAO')

  def get(self, environment, obstacle):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()
    dao = self.DAOModule(session_id)
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

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ObstacleDAO'),'ObstacleDAO')

  def get(self, environment):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    goals = dao.get_obstacle_names(environment=environment)
    dao.close()
    resp = make_response(json_serialize(goals, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class ObstaclesSummaryAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ObstacleDAO'),'ObstacleDAO')

  def get(self):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objts = dao.get_obstacles_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class GenerateVulnerabilityAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ObstacleDAO'),'ObstacleDAO')

  def post(self,name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.generate_vulnerability(name)
    dao.close()
    resp_dict = {'message': 'Vulnerability successfully generated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
