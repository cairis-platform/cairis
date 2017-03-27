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
import os
from flask import make_response, request, session, send_file
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.core.ARM import DatabaseProxyException, ARMException
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, CairisHTTPError, ARMHTTPError, MissingParameterHTTPError
from cairis.data.ExportDAO import ExportDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import CExportMessage
from cairis.tools.ModelDefinitions import CExportParams
from cairis.tools.SessionValidator import get_session_id
from StringIO import StringIO

__author__ = 'Shamal Faily'


class CExportFileAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Exports data to XML file',
    nickname='cexport-file-get',
    parameters=[
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
        'code': httplib.BAD_REQUEST,
        'message': 'The provided file is not a valid XML file'
      },
      {
        'code': httplib.BAD_REQUEST,
        'message': '''Some parameters are missing. Be sure 'file_contents' and 'type' are defined.'''
      }
    ]
  )
  # endregion
  def get(self):
    session_id = get_session_id(session, request)
    dao = ExportDAO(session_id)
    modelBuf = dao.file_export()
    dao.close()
    resp = make_response(modelBuf)
    resp.headers["Content-Type"] = 'application/xml'
    resp.headers["Content-Disposition"] = 'Attachment; filename=model.xml'
    return resp

class CExportArchitecturalPatternAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Exports architectural pattern to XML file',
    nickname='cexport-file-get',
    parameters=[
      {
        "name": "architectural_pattern_name",
        "description": "The architectural pattern name",
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
        'code': httplib.BAD_REQUEST,
        'message': 'The provided file is not a valid XML file'
      },
      {
        'code': httplib.BAD_REQUEST,
        'message': '''Some parameters are missing. Be sure 'file_contents' and 'type' are defined.'''
      }
    ]
  )
  # endregion
  def get(self,architectural_pattern_name):
    session_id = get_session_id(session, request)
    dao = ExportDAO(session_id)
    modelBuf = dao.architectural_pattern_export(architectural_pattern_name)
    dao.close()
    resp = make_response(modelBuf)
    resp.headers["Content-Type"] = 'application/xml'
    resp.headers["Content-Disposition"] = 'Attachment; filename=' + architectural_pattern_name + '.xml'
    return resp
