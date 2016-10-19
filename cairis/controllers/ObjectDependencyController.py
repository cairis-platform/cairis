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
from cairis.data.ObjectDependencyDAO import ObjectDependencyDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ProjectMessage
from cairis.tools.PseudoClasses import ProjectSettings
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ObjectDependencyAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get object dependencies',
    nickname='object-dependency-get',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'dimension_name',
        'description': 'The dimension name, e.g. asset',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'object_name',
        'description': 'The object name, e.g. Clinical data',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
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
        'message': 'One or more attributes are missing'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'Some problems were found during the name check'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'A database error has occurred'
      }
    ]
  )
  # endregion
  def get(self,dimension_name,object_name):
    session_id = get_session_id(session, request)

    dao = ObjectDependencyDAO(session_id)
    deps = dao.report_dependencies(dimension_name,object_name)
    dao.close()

    resp = make_response(json_serialize(deps, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Delete object dependencies',
    nickname='object-dependency-delete',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'dimension_name',
        'description': 'The dimension name, e.g. asset',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'object_name',
        'description': 'The object name, e.g. Clinical data',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
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
        'message': 'One or more attributes are missing'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'Some problems were found during the name check'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'A database error has occurred'
      }
    ]
  )
  # endregion
  def delete(self,dimension_name,object_name):
    session_id = get_session_id(session, request)

    dao = ObjectDependencyDAO(session_id)
    deps = dao.delete_dependencies(dimension_name,object_name)
    dao.close()

    resp_dict = {'message': 'Object dependencies successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
