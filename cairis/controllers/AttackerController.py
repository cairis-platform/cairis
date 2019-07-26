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
from cairis.data.AttackerDAO import AttackerDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import AttackerMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import AttackerModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin, Shamal Faily'


class AttackersAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = AttackerDAO(session_id)
    attackers = dao.get_attackers(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(attackers, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = AttackerDAO(session_id)
    new_attacker = dao.from_json(request)
    dao.add_attacker(new_attacker)
    dao.close()
    resp_dict = {'message': new_attacker.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class AttackerByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = AttackerDAO(session_id)
    attacker = dao.get_attacker_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(attacker, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = AttackerDAO(session_id)
    req = dao.from_json(request)
    dao.update_attacker(req, name=name)
    dao.close()

    resp_dict = {'message': req.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = AttackerDAO(session_id)
    dao.delete_attacker(name=name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class AttackerCapabilitiesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    assets = dao.get_attacker_capabilities(environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(assets, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    new_value_type = dao.type_from_json(request)
    attacker_capability_id = dao.add_attacker_capability(new_value_type, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Attacker capability successfully added', 'attacker_capability_id': attacker_capability_id}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class AttackerCapabilityByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    attacker_capability = dao.get_attacker_capability_by_name(name=name, environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(attacker_capability, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    attacker_capability = dao.type_from_json(request)
    dao.update_attacker_capability(attacker_capability, name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Attacker capability successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    dao.delete_attacker_capability(name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Attacker capability successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class AttackerMotivationsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    assets = dao.get_attacker_motivations(environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(assets, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    new_value_type = dao.type_from_json(request)
    attacker_motivation_id = dao.add_attacker_motivation(new_value_type, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Attacker motivation successfully added', 'attacker_motivation_id': attacker_motivation_id}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class AttackerMotivationByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    attacker_motivation = dao.get_attacker_motivation_by_name(name=name, environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(attacker_motivation, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    attacker_motivation = dao.type_from_json(request)
    dao.update_attacker_motivation(attacker_motivation, name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Attacker motivation successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = AttackerDAO(session_id)
    dao.delete_attacker_motivation(name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Attacker motivation successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class AttackersSummaryAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = AttackerDAO(session_id)
    objts = dao.get_attackers_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp
