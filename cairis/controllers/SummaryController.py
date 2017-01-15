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
from flask_restful_swagger import swagger
from flask_restful import Resource
from cairis.data.SummaryDAO import SummaryDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import SummaryMessage
from cairis.tools.ModelDefinitions import SummaryModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class SummaryAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get summary table',
    responseClass=SummaryModel.__name__,
    nickname='summary-get',
    parameters=[
      {
        "name": "dimension_name",
        "description": "The relevant dimension name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "environment_name",
        "description": "The relevant environment name",
        "required": True,
        "allowMultiple": False,
        "dataType": str.__name__,
        "paramType": "query"
      },
      {
        "name": "session_id",
        "description": "The ID of the user's session",
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
  def get(self,dimension_name,environment_name):
    session_id = get_session_id(session, request)

    dao = SummaryDAO(session_id)
    sumRows = dao.get_summary(dimension_name,environment_name)
    dao.close()

    resp = make_response(json_serialize(sumRows, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp
