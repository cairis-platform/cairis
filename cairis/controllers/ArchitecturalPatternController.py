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
from flask import session, request, make_response
from flask.ext.restful import Resource
from flask.ext.restful_swagger import swagger
from cairis.data.ArchitecturalPatternDAO import ArchitecturalPatternDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ProjectMessage
from cairis.tools.PseudoClasses import ProjectSettings
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ArchitecturalPatternsAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get architectural patterns',
    nickname='architectural-patterns-get',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      }
    ],
    responseMessages=[
      {
        'code': httplib.BAD_REQUEST,
        'message': 'The database connection was not properly setup'
      },
    ]
  )
  # endregion
  def get(self):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    aps = dao.get_architectural_patterns()
    dao.close()
    resp = make_response(json_serialize(aps, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
