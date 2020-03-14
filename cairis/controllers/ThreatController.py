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
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id
from importlib import import_module

__author__ = 'Robin Quetin, Shamal Faily'

class ThreatTypesAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ThreatDAO'),'ThreatDAO')

  def get(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')
    dao = self.DAOModule(session_id)
    threats = dao.get_threat_types(environment_name=environment_name)
    dao.close()
    resp = make_response(json_serialize(threats, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')
    dao = self.DAOModule(session_id)
    new_value_type = dao.type_from_json(request)
    dao.add_threat_type(new_value_type, environment_name=environment_name)
    dao.close()
    resp_dict = {'message': 'Threat type successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class ThreatTypeByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ThreatDAO'),'ThreatDAO')

  def get(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')
    dao = self.DAOModule(session_id)
    threat_type = dao.get_threat_type_by_name(name=name, environment_name=environment_name)
    dao.close()
    resp = make_response(json_serialize(threat_type, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')
    dao = self.DAOModule(session_id)
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
    dao = self.DAOModule(session_id)
    dao.delete_threat_type(name=name, environment_name=environment_name)
    dao.close()
    resp_dict = {'message': 'Threat type successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ThreatModelAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ThreatDAO'),'ThreatDAO')

  def get(self,environment_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    model = dao.get_threat_model(environment_name)
    dao.close()
    resp = make_response(json_serialize(model, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
