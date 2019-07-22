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
import os.path
from flask import make_response, request, session, send_file
from flask_restful import Resource
from cairis.core.ARM import DatabaseProxyException, ARMException
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, CairisHTTPError, ARMHTTPError, MissingParameterHTTPError
from cairis.data.DocumentationDAO import DocumentationDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import DocumentationMessage
from cairis.tools.ModelDefinitions import DocumentationParams
from cairis.tools.SessionValidator import get_session_id
from io import StringIO

__author__ = 'Shamal Faily'


class DocumentationAPI(Resource):

  def get(self,doc_type,doc_format):
    session_id = get_session_id(session, request)
    fileName = request.args.get('filename', 'report')
    dao = DocumentationDAO(session_id)
    sectionFlags = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    if (doc_format == 'PDF'):
      filePostfix = 'pdf'
      doc_format = [0,0,1,0,0]
    elif (doc_format == 'RTF'):
      filePostfix = 'rtf'
      doc_format = [0,1,0,0,0]
    elif (doc_format == 'ODT'):
      filePostfix = 'odt'
      doc_format = [0,0,0,1,0]
    else:
      filePostfix = 'docx'
      doc_format = [0,0,0,0,1]

    b = Borg()
    reportName = b.tmpDir + '/' + fileName + '.' + filePostfix

    dao.generate_documentation(fileName,doc_type,sectionFlags,doc_format)
    dao.close()

    if os.path.isfile(reportName):
      binary_pdf = open(reportName,'rb').read()
      resp = make_response(binary_pdf)
      resp.headers['Content-Type'] = 'application/' + filePostfix
      resp.headers['Content-Disposition'] = 'Attachment; filename=' + fileName + '.' + filePostfix
      return resp
    else:
      raise CairisHTTPError(status_code=500,message='report file not found',status='Unknown error')
