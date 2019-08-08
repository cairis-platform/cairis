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
from cairis.data.CountermeasureDAO import CountermeasureDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import CountermeasureMessage, ValueTypeMessage,CountermeasureTaskMessage
from cairis.tools.ModelDefinitions import CountermeasureModel, ValueTypeModel,CountermeasureTask
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class CountermeasuresAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = CountermeasureDAO(session_id)
    countermeasures = dao.get_countermeasures(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(countermeasures, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    new_countermeasure = dao.from_json(request)
    dao.add_countermeasure(new_countermeasure)
    dao.close()

    resp_dict = {'message': new_countermeasure.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class CountermeasureByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    countermeasure = dao.get_countermeasure_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(countermeasure, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    cm = dao.from_json(request)
    dao.update_countermeasure(cm, name=name)
    dao.close()

    resp_dict = {'message': cm.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    dao.delete_countermeasure(name=name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class TargetsAPI(Resource):

  def get(self, environment):
    session_id = get_session_id(session, request)
    reqList = request.args.getlist('requirement')
    dao = CountermeasureDAO(session_id)
    targets = dao.get_countermeasure_targets(reqList,environment)
    dao.close()
    resp = make_response(json_serialize(targets, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class CountermeasureTasksAPI(Resource):

  def get(self, environment):
    session_id = get_session_id(session, request)
    roleList = request.args.getlist('role')
    dao = CountermeasureDAO(session_id)
    tasks = dao.get_countermeasure_tasks(roleList,environment)
    dao.close()

    resp = make_response(json_serialize(tasks, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
    dao.close()


class GenerateAssetAPI(Resource):

  def post(self, name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    dao.generate_asset(name)
    dao.close()

    resp_dict = {'message': 'Asset ' + name + ' CM created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class GenerateAssetFromTemplateAPI(Resource):

  def post(self, name, template_asset_name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    dao.generate_asset_from_template(name,template_asset_name)
    dao.close()

    resp_dict = {'message': 'Asset ' + template_asset_name  + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class SituateCountermeasurePatternAPI(Resource):

  def post(self, name, security_pattern_name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    dao.situate_countermeasure_pattern(name,security_pattern_name)
    dao.close()

    resp_dict = {'message': security_pattern_name + ' situated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class AssociateSituatedPatternAPI(Resource):

  def post(self, name, security_pattern_name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    dao.associate_situated_pattern(name,security_pattern_name)
    dao.close()

    resp_dict = {'message': security_pattern_name + ' associated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class RemoveSituatedPatternAPI(Resource):

  def delete(self, name, security_pattern_name):
    session_id = get_session_id(session, request)

    dao = CountermeasureDAO(session_id)
    dao.remove_situated_pattern(name,security_pattern_name)
    dao.close()

    resp_dict = {'message': 'Situated pattern ' + security_pattern_name + ' removed'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class CandidatePatternsAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = CountermeasureDAO(session_id)
    spNames = dao.candidate_countermeasure_patterns(name)
    dao.close()
    resp = make_response(json_serialize(spNames, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class CountermeasurePatternsAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = CountermeasureDAO(session_id)
    spNames = dao.countermeasure_patterns(name)
    dao.close()
    resp = make_response(json_serialize(spNames, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
