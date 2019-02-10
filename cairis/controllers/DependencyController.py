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
from flask import session, make_response
from flask import request
from flask_restful import Resource
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError
from cairis.data.DependencyDAO import DependencyDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import DependencyMessage
from cairis.tools.ModelDefinitions import DependencyModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin, Shamal Faily'


class DependenciesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraintsId = request.args.get('constraint_id', '')
    dao = DependencyDAO(session_id)
    dependencies = dao.get_dependencies(constraintsId)
    dao.close()
    resp = make_response(json_serialize(dependencies, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = DependencyDAO(session_id)
    new_dependency = dao.from_json(request)
    dao.add_dependency(new_dependency)
    dao.close()
    resp_dict = {'message': 'Dependency successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class DependencyByNameAPI(Resource):

  def get(self, environment, depender, dependee, dependency):
    session_id = get_session_id(session, request)
    dao = DependencyDAO(session_id)
    found_dependency = dao.get_dependency_by_name(
      environment=environment,
      depender=depender,
      dependee=dependee,
      dependency=dependency
    )
    dao.close()
    resp = make_response(json_serialize(found_dependency, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, environment, depender, dependee, dependency):
    session_id = get_session_id(session, request)
    dao = DependencyDAO(session_id)
    new_dependency = dao.from_json(request)
    dao.update_dependency(environment,depender,dependee,dependency, new_dependency)
    dao.close()
    resp_dict = {'message': 'Dependency successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


  def post(self, environment, depender, dependee, dependency):
    session_id = get_session_id(session, request)
    dao = DependencyDAO(session_id)
    new_dependency = dao.from_json(request)
    new_dependency_id = dao.add_dependency(new_dependency)
    dao.close()
    resp_dict = {'message': 'Dependency successfully added', 'dependency_id': new_dependency_id}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, environment, depender, dependee, dependency):
    session_id = get_session_id(session, request)
    dao = DependencyDAO(session_id)
    count = dao.delete_dependencies(
      environment=environment,
      depender=depender,
      dependee=dependee,
      dependency=dependency
    )
    dao.close()
    if count > 1:
      resp_dict = {'message': count+' dependencies successfully deleted'}
    else:
      resp_dict = {'message': 'Dependency successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
