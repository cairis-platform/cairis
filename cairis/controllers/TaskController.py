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
from flask import request, session, make_response
from flask_restful import Resource
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.TaskDAO import TaskDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import TaskMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import TaskModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class TasksAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = TaskDAO(session_id)
    tasks = dao.get_tasks(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(tasks, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = TaskDAO(session_id)
    new_task = dao.from_json(request)
    task_id = dao.add_task(new_task)
    dao.close()

    resp_dict = {'message': new_task.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class TaskByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = TaskDAO(session_id)
    task = dao.get_task_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(task, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = TaskDAO(session_id)
    req = dao.from_json(request)
    dao.update_task(req, name=name)
    dao.close()

    resp_dict = {'message': req.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = TaskDAO(session_id)
    dao.delete_task(name=name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class TaskModelByNameAPI(Resource):

  def get(self, environment,task,misusecase):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = TaskDAO(session_id)
    if task == 'all':  task = ''
    if misusecase == 'all': misusecase = ''

    dot_code = dao.get_task_model(environment,task,misusecase)
    dao.close()

    resp = make_response(model_generator.generate(dot_code, model_type='task',renderer='dot'), OK)

    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp

class TaskLoadByNameAPI(Resource):

  def get(self, task,environment):
    session_id = get_session_id(session, request)
    dao = TaskDAO(session_id)
    taskLoad = dao.task_load_by_name_environment(task,environment)
    dao.close()
    resp = make_response(json_serialize(taskLoad, session_id=session_id), OK)
    return resp

class TaskHindranceByNameAPI(Resource):

  def get(self, task,environment):
    session_id = get_session_id(session, request)
    dao = TaskDAO(session_id)
    cmLoad = dao.task_hindrance_by_name_environment(task,environment)
    dao.close()
    resp = make_response(json_serialize(cmLoad, session_id=session_id), OK)
    return resp

class TaskScoreByNameAPI(Resource):

  def get(self, task,environment):
    session_id = get_session_id(session, request)
    dao = TaskDAO(session_id)
    taskScore = dao.task_score_by_name_environment(task,environment)
    dao.close()
    resp = make_response(json_serialize(taskScore, session_id=session_id), OK)
    return resp

class MisusabilityModelAPI(Resource):

  def get(self, mc_name,tc_name):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = TaskDAO(session_id)
    if tc_name == 'all':  tc_name = ''

    dot_code = dao.get_misusability_model(mc_name,tc_name)
    dao.close()

    resp = make_response(model_generator.generate(dot_code, model_type='misusability',renderer='dot'), OK)

    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp
