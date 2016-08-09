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
from flask import make_response, request, session
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from cairis.core.ARM import DatabaseProxyException, ARMException
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, CairisHTTPError, ARMHTTPError, MissingParameterHTTPError
from cairis.bin.cexport import *
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import CExportMessage
from cairis.tools.ModelDefinitions import CExportParams
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class CExportTextAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Exports data from XML text',
    nickname='cexport-text-post',
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
  def post(self):
    session_id = get_session_id(session, request)

    try:
      modelBuf = file_export(session_id=session_id)
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)
    except Exception as ex:
      raise CairisHTTPError(status_code=500,message=str(ex.message),status='Unknown error')

    resp = make_response(json_serialize(modelBuf, session_id=session_id), httplib.OK)
    resp.headers['Content-Type'] = 'application/json'
    return resp
