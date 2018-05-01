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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError
from cairis.data.ArchitecturalPatternDAO import ArchitecturalPatternDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ArchitecturalPatternMessage, WeaknessAnalysisMessage
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class ArchitecturalPatternsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    aps = dao.get_architectural_patterns()
    dao.close()
    resp = make_response(json_serialize(aps, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    new_ap = dao.from_json(request)
    dao.add_architectural_pattern(new_ap)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp


class ArchitecturalPatternByNameAPI(Resource):

  def get(self,name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    ap = dao.get_architectural_pattern(name)
    dao.close()
    resp = make_response(json_serialize(ap, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    upd_ap = dao.from_json(request)
    dao.update_architectural_pattern(upd_ap,name)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self,name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    dao.delete_architectural_pattern(name)
    dao.close()

    resp_dict = {'message': 'Architectural Pattern successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ComponentAssetModelAPI(Resource):

  def get(self, component):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = ArchitecturalPatternDAO(session_id)
    dot_code = dao.get_component_asset_model(component)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,renderer='dot'), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'

    return resp

class ComponentGoalModelAPI(Resource):

  def get(self, component):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = ArchitecturalPatternDAO(session_id)
    dot_code = dao.get_component_goal_model(component)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,model_type='goal',renderer='dot'), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'

    return resp

class ComponentModelAPI(Resource):

  def get(self, ap_name):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = ArchitecturalPatternDAO(session_id)
    dot_code = dao.get_component_model(ap_name)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,renderer='dot'), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'

    return resp

class WeaknessAnalysisAPI(Resource):

  def get(self,architectural_pattern_name,environment_name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    cwm = dao.get_weakness_analysis(architectural_pattern_name,environment_name)
    dao.close()
    resp = make_response(json_serialize(cwm, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class SituateArchitecturalPatternAPI(Resource):

  def post(self,architectural_pattern_name,environment_name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    cwm = dao.situate_component_view(architectural_pattern_name,environment_name)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully situated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp
