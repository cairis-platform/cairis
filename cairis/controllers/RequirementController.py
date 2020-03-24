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
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError
from cairis.data.RequirementDAO import RequirementDAO
from cairis.tools.SessionValidator import get_session_id
from cairis.tools.JsonConverter import json_serialize

__author__ = 'Robin Quetin, Shamal Faily'


class RequirementsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    ordered = request.args.get('ordered', 0)
    constraint_id = request.args.get('constraint_id', '')

    dao = RequirementDAO(session_id)
    reqs = dao.get_requirements(constraint_id=constraint_id, ordered=(ordered=='1'))
    dao.close()

    resp = make_response(json_serialize(reqs, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    asset_name = request.args.get('asset', None)
    environment_name = request.args.get('environment', None)
    dao = RequirementDAO(session_id)

    domain_name = asset_name
    if (environment_name != None):
      domain_name = environment_name

    new_req = dao.from_json(request,domain_name)
    dao.add_requirement(new_req, asset_name=asset_name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': new_req.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class RequirementsByAssetAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    ordered = request.args.get('ordered', '1')

    dao = RequirementDAO(session_id)
    reqs = dao.get_requirements(constraint_id=name, is_asset=True, ordered=(ordered=='1'))
    dao.close()

    resp = make_response(json_serialize(reqs, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class RequirementNamesByAssetAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = RequirementDAO(session_id)
    reqs = dao.get_dimension_requirement_names('asset',name)
    dao.close()
    resp = make_response(json_serialize(reqs, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class RequirementsByEnvironmentAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    ordered = request.args.get('ordered', '1')

    dao = RequirementDAO(session_id)
    reqs = dao.get_requirements(constraint_id=name, is_asset=False, ordered=(ordered=='1'))
    dao.close()

    resp = make_response(json_serialize(reqs, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class RequirementNamesByEnvironmentAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = RequirementDAO(session_id)
    reqs = dao.get_dimension_requirement_names('environment',name)
    dao.close()
    resp = make_response(json_serialize(reqs, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
