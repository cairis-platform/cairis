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
from cairis.data.ProjectDAO import ProjectDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ProjectMessage
from cairis.tools.PseudoClasses import ProjectSettings
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Robin Quetin, Shamal Faily'


class ProjectClearAPI(Resource):

  def post(self):
    session_id = get_session_id(session, request)

    dao = ProjectDAO(session_id)
    dao.clear_project()
    dao.close()
    resp_dict = {'message': 'Project cleared successfully'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class ProjectCreateDatabaseAPI(Resource):

  def post(self,db_name):
    session_id = get_session_id(session, request)
    dao = ProjectDAO(session_id)
    dao.create_new_database(db_name)
    dao.close()
    resp_dict = {'message': 'New database successfully created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ProjectOpenDatabaseAPI(Resource):

  def post(self,db_name):
    session_id = get_session_id(session, request)
    dao = ProjectDAO(session_id)
    dao.open_database(db_name)
    dao.close()
    resp_dict = {'message': 'Database successfully opened'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ProjectDeleteDatabaseAPI(Resource):

  def post(self,db_name):
    session_id = get_session_id(session, request)
    dao = ProjectDAO(session_id)
    dao.delete_database(db_name)
    dao.close()
    resp_dict = {'message': 'Database successfully deleted'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ProjectSettingsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)

    dao = ProjectDAO(session_id)
    settings = dao.get_settings()

    resp = make_response(json_serialize(settings, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self):
    session_id = get_session_id(session, request)

    dao = ProjectDAO(session_id)
    settings = dao.from_json(request)
    dao.apply_settings(settings)

    resp_dict = {'message': 'Project settings successfully updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
