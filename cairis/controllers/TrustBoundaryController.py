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
from cairis.data.TrustBoundaryDAO import TrustBoundaryDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import TrustBoundaryMessage
from cairis.tools.ModelDefinitions import TrustBoundaryModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class TrustBoundariesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = TrustBoundaryDAO(session_id)
    tbs = dao.get_trust_boundaries()
    dao.close()
    resp = make_response(json_serialize(tbs, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = TrustBoundaryDAO(session_id)
    new_tb = dao.from_json(request)
    dao.add_trust_boundary(new_tb)
    dao.close()

    resp_dict = {'message': new_tb.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class TrustBoundaryByNameAPI(Resource):

  def get(self, trust_boundary_name):
    session_id = get_session_id(session, request)

    dao = TrustBoundaryDAO(session_id)
    tb = dao.get_trust_boundary_by_name(trust_boundary_name)
    dao.close()
    resp = make_response(json_serialize(tb, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, trust_boundary_name):
    session_id = get_session_id(session, request)

    dao = TrustBoundaryDAO(session_id)
    tb = dao.from_json(request)
    dao.update_trust_boundary(trust_boundary_name,tb)
    dao.close()

    resp_dict = {'message': tb.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, trust_boundary_name):
    session_id = get_session_id(session, request)

    dao = TrustBoundaryDAO(session_id)
    dao.delete_trust_boundary(trust_boundary_name)
    dao.close()

    resp_dict = {'message': trust_boundary_name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
