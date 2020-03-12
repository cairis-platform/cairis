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
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator
from importlib import import_module


__author__ = 'Shamal Faily'


class ComponentAssetModelAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ArchitecturalPatternDAO'),'ArchitecturalPatternDAO')


  def get(self, component):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = self.DAOModule(session_id)
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

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ArchitecturalPatternDAO'),'ArchitecturalPatternDAO')

  def get(self, component):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = self.DAOModule(session_id)
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

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ArchitecturalPatternDAO'),'ArchitecturalPatternDAO')

  def get(self, ap_name):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = self.DAOModule(session_id)
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

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ArchitecturalPatternDAO'),'ArchitecturalPatternDAO')

  def get(self,architectural_pattern_name,environment_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    cwm = dao.get_weakness_analysis(architectural_pattern_name,environment_name)
    dao.close()
    resp = make_response(json_serialize(cwm, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class SituateArchitecturalPatternAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.ArchitecturalPatternDAO'),'ArchitecturalPatternDAO')

  def post(self,architectural_pattern_name,environment_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    cwm = dao.situate_component_view(architectural_pattern_name,environment_name)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully situated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp
