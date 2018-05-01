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
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError
from cairis.data.LocationsDAO import LocationsDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import LocationsMessage
from cairis.tools.ModelDefinitions import LocationsModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class LocationsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = LocationsDAO(session_id)
    locs = dao.get_locations(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(locs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = LocationsDAO(session_id)
    new_locs = dao.from_json(request)
    dao.add_locations(new_locs)
    dao.close()

    resp_dict = {'message': 'Locations successfully added'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class LocationsByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = LocationsDAO(session_id)
    found_locs = dao.get_locations_name(name)
    dao.close()

    resp = make_response(json_serialize(found_locs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = LocationsDAO(session_id)
    upd_locs = dao.from_json(request)
    dao.update_locations(upd_locs, name)
    dao.close()

    resp_dict = {'message': 'Locations successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = LocationsDAO(session_id)
    dao.delete_locations(name)
    dao.close()

    resp_dict = {'message': 'Locations successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class LocationsModelAPI(Resource):

  def get(self, locations, environment):
    session_id = get_session_id(session, request)
    hide_concerns = request.args.get('hide_concerns', '1')
    model_generator = get_model_generator()

    dao = LocationsDAO(session_id)
    dot_code = dao.get_locations_model(locations,environment)
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
