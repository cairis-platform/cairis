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
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator
from importlib import import_module


__author__ = 'Shamal Faily'

class GenerateAssetAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.CountermeasureDAO'),'CountermeasureDAO')

  def post(self, name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    dao.generate_asset(name)
    dao.close()

    resp_dict = {'message': 'Asset ' + name + ' CM created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class GenerateAssetFromTemplateAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.CountermeasureDAO'),'CountermeasureDAO')

  def post(self, name, template_asset_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    dao.generate_asset_from_template(name,template_asset_name)
    dao.close()

    resp_dict = {'message': 'Asset ' + template_asset_name  + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class SituateCountermeasurePatternAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.CountermeasureDAO'),'CountermeasureDAO')

  def post(self, name, security_pattern_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    dao.situate_countermeasure_pattern(name,security_pattern_name)
    dao.close()

    resp_dict = {'message': security_pattern_name + ' situated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class AssociateSituatedPatternAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.CountermeasureDAO'),'CountermeasureDAO')

  def post(self, name, security_pattern_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    dao.associate_situated_pattern(name,security_pattern_name)
    dao.close()

    resp_dict = {'message': security_pattern_name + ' associated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class RemoveSituatedPatternAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.CountermeasureDAO'),'CountermeasureDAO')

  def delete(self, name, security_pattern_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    dao.remove_situated_pattern(name,security_pattern_name)
    dao.close()

    resp_dict = {'message': 'Situated pattern ' + security_pattern_name + ' removed'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class CandidatePatternsAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.CountermeasureDAO'),'CountermeasureDAO')

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    spNames = dao.candidate_countermeasure_patterns(name)
    dao.close()
    resp = make_response(json_serialize(spNames, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class CountermeasurePatternsAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.CountermeasureDAO'),'CountermeasureDAO')

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    spNames = dao.countermeasure_patterns(name)
    dao.close()
    resp = make_response(json_serialize(spNames, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
