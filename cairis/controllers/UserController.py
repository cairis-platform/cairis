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

import httplib
import logging
from flask.ext.restful_swagger import swagger
from flask import request, make_response, session
from flask.ext.restful import Resource
from jsonpickle import encode

from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MissingParameterHTTPError, MalformedJSONHTTPError
from cairis.tools.ModelDefinitions import UserConfigModel
from cairis.tools.SessionValidator import get_logger
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy


__author__ = 'Robin Quetin, Shamal Faily'


def set_dbproxy():
  b = Borg()
  db_proxy = MySQLDatabaseProxy()
  pSettings = db_proxy.getProjectSettings()

  id = b.init_settings()
  db_proxy.close()
  session['session_id'] = id
  b.settings[id]['dbProxy'] = db_proxy
  b.settings[id]['dbUser'] = b.dbUser
  b.settings[id]['dbPasswd'] = b.dbPasswd
  b.settings[id]['dbHost'] = b.dbHost
  b.settings[id]['dbPort'] = b.dbPort
  b.settings[id]['dbName'] = b.dbName
  b.settings[id]['fontSize'] = pSettings['Font Size']
  b.settings[id]['apFontSize'] = pSettings['AP Font Size']
  b.settings[id]['fontName'] = pSettings['Font Name']
  b.settings[id]['jsonPrettyPrint'] = False
  return b.settings[id]

class UserConfigAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Sets up the user session',
    nickname='user-config-post',
    responseClass=str.__name__,
    parameters=[],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The method is not callable without setting up a database connection'
      },
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The provided parameters are invalid'
      }
    ]
  )
  # endregion
  def post(self):
    s = set_dbproxy()
    resp_dict = {'session_id': s['session_id'], 'message': 'Session created'}
    resp = make_response(encode(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
