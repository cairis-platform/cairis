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
import os
from flask import make_response, request, session, send_file
from flask_restful import Resource
from cairis.core.ARM import DatabaseProxyException, ARMException
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, CairisHTTPError, ARMHTTPError, MissingParameterHTTPError
from cairis.data.ExportDAO import ExportDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import CExportMessage
from cairis.tools.ModelDefinitions import CExportParams
from cairis.tools.SessionValidator import get_session_id
from io import StringIO

__author__ = 'Shamal Faily'


class CExportFileAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    fileName = request.args.get('filename', 'model')
    fileType = request.args.get('fileType','xml')

    dao = ExportDAO(session_id)
    modelBuf = dao.file_export(fileName,fileType)
    dao.close()
    resp = make_response(modelBuf)
    if (fileType == 'cairis'):
      resp.headers["Content-Type"] = 'application/octet-stream'
    else:
      resp.headers["Content-Type"] = 'application/xml'
    resp.headers["Content-Disposition"] = 'Attachment; filename=' + fileName + '.' + fileType
    return resp

class CExportArchitecturalPatternAPI(Resource):

  def get(self,architectural_pattern_name):
    session_id = get_session_id(session, request)
    fileName = request.args.get('filename', architectural_pattern_name + '.xml')
    dao = ExportDAO(session_id)
    modelBuf = dao.architectural_pattern_export(architectural_pattern_name)
    dao.close()
    resp = make_response(modelBuf)
    resp.headers["Content-Type"] = 'application/xml'
    resp.headers["Content-Disposition"] = 'Attachment; filename=' + fileName
    return resp


class CExportGRLAPI(Resource):

  def get(self,task_name,persona_name,environment_name):
    session_id = get_session_id(session, request)
    fileName = request.args.get('filename', task_name + '.grl')
    dao = ExportDAO(session_id)
    modelBuf = dao.grl_export(task_name,persona_name,environment_name)
    dao.close()
    resp = make_response(modelBuf)
    resp.headers["Content-Type"] = 'application/grl'
    resp.headers["Content-Disposition"] = 'Attachment; filename=' + fileName
    return resp

class CExportSecurityPatternsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    fileName = request.args.get('filename', 'security_patterns.xml')
    dao = ExportDAO(session_id)
    modelBuf = dao.security_patterns_export()
    dao.close()
    resp = make_response(modelBuf)
    resp.headers["Content-Type"] = 'application/xml'
    resp.headers["Content-Disposition"] = 'Attachment; filename=' + fileName
    return resp
