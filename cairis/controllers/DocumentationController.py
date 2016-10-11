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
import os.path
from flask import make_response, request, session, send_file
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from cairis.core.ARM import DatabaseProxyException, ARMException
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, CairisHTTPError, ARMHTTPError, MissingParameterHTTPError
from cairis.data.DocumentationDAO import DocumentationDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import DocumentationMessage
from cairis.tools.ModelDefinitions import DocumentationParams
from cairis.tools.SessionValidator import get_session_id
from StringIO import StringIO

__author__ = 'Shamal Faily'


class DocumentationAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Generate documentation',
    nickname='generate-documentation',
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
        'name': 'doc_type',
        "description": "Document type",
        "required": True,
        "allowMultiple": False,
        'type': DocumentationMessage.__name__,
        'paramType': 'body'
      },
      {
        'name': 'doc_format',
        "description": "Document format",
        "required": True,
        "allowMultiple": False,
        'type': DocumentationMessage.__name__,
        'paramType': 'body'
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
  def get(self,doc_type,doc_format):
    session_id = get_session_id(session, request)
    dao = DocumentationDAO(session_id)
    sectionFlags = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    if (doc_format == 'PDF'):
      filePostfix = 'pdf'
      doc_format = [0,0,1]
    else:
      filePostfix = 'rtf'
      doc_format = [0,1,0]
    b = Borg()
    reportName = b.tmpDir + '/report.' + filePostfix

    dao.generate_documentation(doc_type,sectionFlags,doc_format)
    dao.close()

    if os.path.isfile(reportName):
      binary_pdf = open(reportName).read()
      resp = make_response(binary_pdf)
      resp.headers['Content-Type'] = 'application/' + filePostfix
      resp.headers['Content-Disposition'] = 'inline; filename=report.' + filePostfix
      return resp
    else:
      raise CairisHTTPError(status_code=500,message='report file not found',status='Unknown error')
