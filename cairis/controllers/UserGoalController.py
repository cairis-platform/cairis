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
import http.client
from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
from flask import session, request, make_response
from flask_restful import Resource
from cairis.data.UserGoalDAO import UserGoalDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class UserGoalsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = UserGoalDAO(session_id)
    ugs = dao.get_user_goals()
    dao.close()
    resp = make_response(json_serialize(ugs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = UserGoalDAO(session_id)
    new_ug = dao.from_json(request)
    dao.add_user_goal(new_ug)
    dao.close()
    resp_dict = {'message': new_ug.synopsis() + ' created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class UserGoalByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = UserGoalDAO(session_id)
    found_ug = dao.get_user_goals(name)
    dao.close()
    resp = make_response(json_serialize(found_ug, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    dao = UserGoalDAO(session_id)
    upd_ug = dao.from_json(request)
    dao.update_user_goal(upd_ug, name)
    dao.close()
    resp_dict = {'message': upd_ug.synopsis() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    dao = UserGoalDAO(session_id)
    dao.delete_user_goal(name)
    dao.close()
    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class UserGoalModelAPI(Resource):

  def get(self, environment_name,filter_element):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()
    dao = UserGoalDAO(session_id)

    if filter_element == 'all':
      filter_element = ''
    dot_code = dao.get_user_goal_model(environment_name,filter_element)
    dao.close()
    resp = make_response(model_generator.generate(dot_code, model_type='usergoal',renderer='dot'), OK)

    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp
