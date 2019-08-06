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
from cairis.data.UseCaseDAO import UseCaseDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import UseCaseMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import UseCaseModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class UseCasesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = UseCaseDAO(session_id)
    usecases = dao.get_usecases(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(usecases, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    new_usecase,ucContribs = dao.from_json(request)
    dao.add_usecase(new_usecase)
    for rc in ucContribs:
      dao.assign_usecase_contribution(rc)
    dao.close()

    resp_dict = {'message': new_usecase.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class UseCaseByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    usecase = dao.get_usecase_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(usecase, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    uc,ucContribs = dao.from_json(request)
    dao.update_usecase(uc, name=name)
    dao.remove_usecase_contributions(uc)
    if (len(ucContribs) > 0):
      for rc in ucContribs:
        dao.assign_usecase_contribution(rc)
    dao.close()


    resp_dict = {'message': uc.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    dao.delete_usecase(name=name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class UseCaseRequirementsByNameAPI(Resource):

  def get(self, usecase_name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    reqs = dao.get_usecase_requirements(usecase_name)
    dao.close()

    resp = make_response(json_serialize(reqs, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class UseCaseGoalsByNameAPI(Resource):

  def get(self, usecase_name,environment_name):
    session_id = get_session_id(session, request)

    dao = UseCaseDAO(session_id)
    goals = dao.get_usecase_goals(usecase_name,environment_name)
    dao.close()

    resp = make_response(json_serialize(goals, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class UseCasesSummaryAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = UseCaseDAO(session_id)
    objts = dao.get_usecases_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp
