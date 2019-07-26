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
from cairis.data.RoleDAO import RoleDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import RoleMessage
from cairis.tools.ModelDefinitions import RoleModel, RoleEnvironmentPropertiesModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin, Shamal Faily'


class RolesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)
    dao = RoleDAO(session_id)
    roles = dao.get_roles(constraint_id)
    dao.close()
    resp = make_response(json_serialize(roles, session_id=session_id))
    resp.contenttype = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = RoleDAO(session_id)
    new_role = dao.from_json(request)
    dao.add_role(new_role)
    dao.close()
    resp_dict = {'message': new_role.name() + ' created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class RolesByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = RoleDAO(session_id)
    found_role = dao.get_role_by_name(name)
    dao.close()
    resp = make_response(json_serialize(found_role, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    dao = RoleDAO(session_id)
    upd_role = dao.from_json(request)
    dao.update_role(upd_role, name=name)
    dao.close()
    resp_dict = {'message': upd_role.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    dao = RoleDAO(session_id)
    dao.delete_role(name=name)
    dao.close()
    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class RoleEnvironmentPropertiesAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = RoleDAO(session_id)
    props = dao.get_role_props(name)
    dao.close()
    resp = make_response(json_serialize(props, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
