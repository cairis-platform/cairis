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
  from urllib.parse import unquote
  import http.client
  from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
else:
  from urllib import unquote
  import httplib
  from httplib import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
from os import close as fd_close
from os import remove as remove_file
from tempfile import mkstemp
from flask import make_response, request, session
from flask_restful import Resource
from flask_restful_swagger import swagger
from werkzeug.datastructures import FileStorage
from cairis.core.ARM import DatabaseProxyException, ARMException
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import MalformedJSONHTTPError, CairisHTTPError, ARMHTTPError, MissingParameterHTTPError
from cairis.data.ImportDAO import ImportDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import CImportMessage
from cairis.tools.ModelDefinitions import CImportParams
from cairis.tools.SessionValidator import validate_proxy, check_required_keys, get_session_id
import codecs

__author__ = 'Robin Quetin, Shamal Faily'


class CImportTextAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Imports data from XML text',
    nickname='cimport-text-post',
    parameters=[
      {
        'name':'body',
        "description": "Options to be passed to the import tool",
        "required": True,
        "allowMultiple": False,
        'type': CImportMessage.__name__,
        'paramType': 'body'
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
        'code': BAD_REQUEST,
        'message': 'The provided file is not a valid XML file'
      },
      {
        'code': BAD_REQUEST,
        'message': '''Some parameters are missing. Be sure 'file_contents' and 'type' are defined.'''
      }
    ]
  )
  # endregion
  def post(self):
    session_id = get_session_id(session, request)
    json_dict = request.get_json(silent=True)
    if json_dict is False or json_dict is None:
      raise MalformedJSONHTTPError(data=request.get_data())

    cimport_params = json_dict.get('object', None)
    check_required_keys(cimport_params or {}, CImportParams.required)
    file_contents = cimport_params['urlenc_file_contents']
    file_contents = unquote(file_contents)
    file_contents = file_contents.replace("\u2018", "'").replace("\u2019", "'")
    overwrite = cimport_params['overwrite']
    type = cimport_params['type']

    if file_contents.startswith('<?xml'):
      fd, abs_path = mkstemp(suffix='.xml')
      fs_temp = codecs.open(abs_path, 'w','utf-8')
      fs_temp.write(file_contents)
      fs_temp.close()
      fd_close(fd)

      try:
        dao = ImportDAO(session_id)
        result = dao.file_import(abs_path, type, overwrite)
        dao.close()
      except DatabaseProxyException as ex:
        raise ARMHTTPError(ex)
      except ARMException as ex:
        raise ARMHTTPError(ex)
      except Exception as ex:
        raise CairisHTTPError(status_code=500,message=str(ex.message),status='Unknown error')

      remove_file(abs_path)

      resp_dict = {'message': str(result)}
      resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
      resp.headers['Content-Type'] = 'application/json'
      return resp
    elif type == 'Attack Tree (Dot)':
      try:
        environment_name = cimport_params['environment']
        contributor_name = cimport_params['contributor']
        dao = ImportDAO(session_id)
        result = dao.import_attack_tree(file_contents,environment_name,contributor_name)
        dao.close()
      except DatabaseProxyException as ex:
        raise ARMHTTPError(ex)
      except ARMException as ex:
        raise ARMHTTPError(ex)
      except Exception as ex:
        raise CairisHTTPError(status_code=500,message=str(ex.message),status='Unknown error')
    else:
      raise CairisHTTPError(status_code=BAD_REQUEST,message='The provided file is not a valid XML file',status='Invalid XML input')


class CImportFileAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Imports data from an XML file',
    nickname='cimport-file-post',
    parameters=[
      {
        'name':'file',
        "description": "The XML file to import",
        "required": True,
        "allowMultiple": False,
        'type': 'file',
        'paramType': 'form'
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
        'code': BAD_REQUEST,
        'message': 'The provided file is not a valid XML file'
      },
      {
        'code': BAD_REQUEST,
        'message': '''Some parameters are missing. Be sure 'file_contents' and 'type' are defined.'''
      }
    ]
  )
  # endregion
  def post(self, type):
    session_id = get_session_id(session, request)
    try:
      if not request.files:
        raise LookupError()
      file = request.files['file']
    except LookupError:
      raise MissingParameterHTTPError(param_names=['file'])

    try:
      fd, abs_path = mkstemp(suffix='.xml')
      fs_temp = open(abs_path, 'wb')
      xml_text = file.stream.read()
      fs_temp.write(xml_text)
      fs_temp.close()
      fd_close(fd)
    except IOError:
      raise CairisHTTPError(status_code=CONFLICT,status='Unable to load XML file',message='The XML file could not be loaded on the server.' + 'Please check if the application has permission to write temporary files.')

    try:
      dao = ImportDAO(session_id)
      result = dao.file_import(abs_path, type, 1)
      dao.close()
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)
    except Exception as ex:
      raise CairisHTTPError(status_code=500,message=str(ex.message),status='Unknown error')

    remove_file(abs_path)

    resp_dict = { 'message': str(result) }
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.headers['Content-Type'] = 'application/json'
    return resp
