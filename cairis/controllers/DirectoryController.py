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
from flask import request, session, make_response
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.DirectoryDAO import DirectoryDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import DirectoryMessage
from cairis.tools.ModelDefinitions import DirectoryModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ThreatDirectoryAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get threat directory',
    nickname='directory-threat-get',
    responseClass=DirectoryModel.__name__,
    responseContainer='List',
    parameters=[
      {
        "name": "session_id",
        "description": "The ID of the user's session",
        "required": False,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "entry_name",
        "description": "Directory filter",
        "required": False,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      }
    ],
    responseMessages=[
      {
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  #endregion
  def get(self,entry_name):
    session_id = get_session_id(session, request)
    dao = DirectoryDAO(session_id)
    if entry_name == 'all':
      entry_name = ''
    tds = dao.get_threat_directory(entry_name)
    dao.close()
    resp = make_response(json_serialize(tds, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class VulnerabilityDirectoryAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get vulnerability directory',
    nickname='directory-vulnerability-get',
    responseClass=DirectoryModel.__name__,
    responseContainer='List',
    parameters=[
      {
        "name": "session_id",
        "description": "The ID of the user's session",
        "required": False,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "entry_name",
        "description": "Directory filter",
        "required": False,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      }
    ],
    responseMessages=[
      {
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  #endregion
  def get(self,entry_name):
    session_id = get_session_id(session, request)
    dao = DirectoryDAO(session_id)
    if entry_name == 'all':
      entry_name = ''
    vds = dao.get_vulnerability_directory(entry_name)
    dao.close()
    resp = make_response(json_serialize(vds, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
