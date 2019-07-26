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

from cairis.data.ThreatDAO import ThreatDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ThreatMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import ThreatModel, ValueTypeModel, ThreatModelModel
from cairis.tools.SessionValidator import get_session_id


__author__ = 'Robin Quetin, Shamal Faily'


class ThreatAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = ThreatDAO(session_id)
    threats = dao.get_threats(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(threats, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = ThreatDAO(session_id)
    new_threat = dao.from_json(request)
    dao.add_threat(new_threat)
    dao.close()

    resp_dict = {'message': new_threat.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class ThreatByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = ThreatDAO(session_id)
    threat = dao.get_threat_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(threat, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = ThreatDAO(session_id)
    req = dao.from_json(request)
    dao.update_threat(req, name=name)
    dao.close()

    resp_dict = {'message': req.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = ThreatDAO(session_id)
    dao.delete_threat(name=name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ThreatTypesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = ThreatDAO(session_id)
    threats = dao.get_threat_types(environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(threats, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = ThreatDAO(session_id)
    new_value_type = dao.type_from_json(request)
    dao.add_threat_type(new_value_type, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Threat type successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class ThreatTypeByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = ThreatDAO(session_id)
    threat_type = dao.get_threat_type_by_name(name=name, environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(threat_type, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = ThreatDAO(session_id)
    threat_type = dao.type_from_json(request)
    dao.update_threat_type(threat_type, name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Threat type successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = ThreatDAO(session_id)
    dao.delete_threat_type(name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Threat type successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ThreatModelAPI(Resource):

  def get(self,environment_name):
    session_id = get_session_id(session, request)
    dao = ThreatDAO(session_id)
    model = dao.get_threat_model(environment_name)
    dao.close()
    resp = make_response(json_serialize(model, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class ThreatsSummaryAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = ThreatDAO(session_id)
    objts = dao.get_threats_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp
