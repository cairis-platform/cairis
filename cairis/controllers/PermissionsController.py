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
from cairis.daemon.CairisHTTPError import MissingParameterHTTPError, CairisHTTPError
from cairis.data.PermissionsDAO import PermissionsDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'


class PermissionsAPI(Resource):

  def get(self,db_name):
    session_id = get_session_id(session, request)
    dao = PermissionsDAO(session_id)
    permissions = dao.get_permissions(db_name)
    dao.close()
    resp = make_response(json_serialize(permissions, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class ChangePermissionAPI(Resource):
  def post(self,db_name,user_id,permission):
    session_id = get_session_id(session, request)
    dao = PermissionsDAO(session_id)
    dao.set_permission(db_name, user_id, permission)
    dao.close()
    msg = 'Permission successfully '
    if (permission == 'grant'):
      msg += 'granted'
    else:
      msg += 'revoked'
    resp_dict = {'message': msg}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
