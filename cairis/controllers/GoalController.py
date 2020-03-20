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
  from urllib.parse import unquote
  import http.client
  from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
else:
  from urllib import unquote
  import httplib
  from httplib import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
from flask import session, request, make_response
from flask_restful import Resource
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator
from importlib import import_module

__author__ = 'Robin Quetin, Shamal Faily'


class GoalsAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.GoalDAO'),'GoalDAO')

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)
    coloured = request.args.get('coloured', False)
    dao = self.DAOModule(session_id)
    objts = dao.get_objects(constraint_id=constraint_id, coloured=(coloured == '1'))
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.from_json(request)
    dao.add_object(objt)
    dao.close()
    resp_dict = {'message': objt.name() + ' created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class GoalByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.GoalDAO'),'GoalDAO')

  def get(self, name):
    session_id = get_session_id(session, request)
    coloured = request.args.get('coloured', False)
    dao = self.DAOModule(session_id)
    found_goal = dao.get_object_by_name(unquote(name), coloured=(coloured == '1'))
    dao.close()
    resp = make_response(json_serialize(found_goal, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.from_json(request)
    dao.update_object(objt, unquote(name))
    dao.close()
    resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.delete_object(unquote(name))
    dao.close()
    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class GoalByEnvironmentNamesAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.GoalDAO'),'GoalDAO')

  def get(self, environment):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    goals = dao.get_goal_names(environment=environment)
    dao.close()
    resp = make_response(json_serialize(goals, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class GoalAssociationByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.GoalAssociationDAO'),'GoalAssociationDAO')

  def get(self,environment_name,goal_name,subgoal_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    assoc = dao.get_goal_association(unquote(environment_name),unquote(goal_name),unquote(subgoal_name))
    dao.close()
    resp = make_response(json_serialize(assoc, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def delete(self,environment_name,goal_name,subgoal_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.delete_goal_association(unquote(environment_name),unquote(goal_name),unquote(subgoal_name))
    dao.close()
    resp_dict = {'message': 'Goal Association successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,environment_name,goal_name,subgoal_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    assoc = dao.from_json(request)
    dao.update_goal_association(assoc,unquote(environment_name),unquote(goal_name),unquote(subgoal_name))
    dao.close()
    resp_dict = {'message': 'Goal Association successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class GoalAssociationAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.GoalAssociationDAO'),'GoalAssociationDAO')

  def get(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment_name', '')
    dao = self.DAOModule(session_id)
    assocs = dao.get_goal_associations(environment_name)
    dao.close()
    resp = make_response(json_serialize(assocs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    assoc = dao.from_json(request)
    dao.add_goal_association(assoc)
    dao.close()
    resp_dict = {'message': 'Goal Association successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp
