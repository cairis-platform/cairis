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
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, ARMHTTPError, ObjectNotFoundHTTPError
from cairis.data.EnvironmentDAO import EnvironmentDAO
from cairis.tools.MessageDefinitions import EnvironmentMessage
from cairis.tools.ModelDefinitions import EnvironmentModel
from cairis.tools.PseudoClasses import EnvironmentTensionModel
from cairis.tools.SessionValidator import get_session_id
from cairis.tools.JsonConverter import json_serialize


__author__ = 'Robin Quetin, Shamal Faily'


class EnvironmentsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraintsId = request.args.get('constraints_id', -1)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environments(constraintsId)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = EnvironmentDAO(session_id)
    new_environment = dao.from_json(request)
    new_environment_id = dao.add_environment(new_environment)
    dao.close()

    resp_dict = {'message': 'Environment successfully added', 'environment_id': new_environment_id}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class EnvironmentByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    found_environment = dao.get_environment_by_name(name)
    dao.close()

    resp = make_response(json_serialize(found_environment, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    dao = EnvironmentDAO(session_id)
    new_environment = dao.from_json(request)
    dao.update_environment(new_environment, name=name)
    dao.close()

    resp_dict = {'message': 'Environment successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    dao = EnvironmentDAO(session_id)
    dao.delete_environment(name=name)
    dao.close()

    resp_dict = {'message': 'Environment successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class EnvironmentsByThreatVulnerability(Resource):

  def get(self, threat, vulnerability):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environments_by_threat_vulnerability(threat, vulnerability)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class EnvironmentNamesByThreatVulnerability(Resource):

  def get(self, threat, vulnerability):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environment_names_by_threat_vulnerability(threat, vulnerability)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class EnvironmentNamesByRisk(Resource):

  def get(self, risk):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environments = dao.get_environment_names_by_risk(risk)
    dao.close()

    resp = make_response(json_serialize(environments, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class EnvironmentNamesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)

    dao = EnvironmentDAO(session_id)
    environment_names = dao.get_environment_names()
    dao.close()

    resp = make_response(json_serialize(environment_names, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
