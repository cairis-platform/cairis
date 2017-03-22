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
from flask_restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError
from cairis.data.ArchitecturalPatternDAO import ArchitecturalPatternDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ArchitecturalPatternMessage, WeaknessAnalysisMessage
from cairis.tools.SessionValidator import get_session_id, get_model_generator

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

  # region Swagger Doc
  @swagger.operation(
    notes='Add architectural pattern',
    nickname='architectural-pattern-add',
    responseClass=str.__name__,
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new architectural pattern to be added",
        "required": True,
        "allowMultiple": False,
        "type": ArchitecturalPatternMessage.__name__,
        "paramType": "body"
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
        'message': 'The database connection was not properly setup'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'Some problems were found during the name check'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'A database error has occurred'
      },
      {
        'code': ARMHTTPError.status_code,
        'message': ARMHTTPError.status
      }
    ]
  )
  # endregion
  def post(self):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    new_ap = dao.from_json(request)
    dao.add_architectural_pattern(new_ap)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully added'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


class ArchitecturalPatternByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get architectural patterns by name',
    nickname='architectural-patterns-get-by-name',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Architectural pattern name',
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
        'message': 'The database connection was not properly setup'
      },
    ]
  )
  # endregion
  def get(self,name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    ap = dao.get_architectural_pattern(name)
    dao.close()
    resp = make_response(json_serialize(ap, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


  # region Swagger Doc
  @swagger.operation(
    notes='Update architectural pattern',
    nickname='architectural-pattern-update',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Architectural pattern name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        "name": "body",
        "description": "The serialized version of the architectural pattern to be updated",
        "required": True,
        "allowMultiple": False,
        "type": ArchitecturalPatternMessage.__name__,
        "paramType": "body"
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
        'message': 'The database connection was not properly setup'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'Some problems were found during the name check'
      },
      {
        'code': httplib.CONFLICT,
        'message': 'A database error has occurred'
      },
      {
        'code': ARMHTTPError.status_code,
        'message': ARMHTTPError.status
      }
    ]
  )
  # endregion
  def put(self,name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    upd_ap = dao.from_json(request)
    dao.update_architectural_pattern(upd_ap,name)
    dao.close()
    resp_dict = {'message': 'Architectural Pattern successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp


  # region Swagger Doc
  @swagger.operation(
    notes='Delete an existing architectural patterns',
    nickname='architectural-pattern-by-name-delete',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'name',
        'description': 'Architectural pattern name',
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
        'message': 'The database connection was not properly setup'
      },
      {
        'code': httplib.NOT_FOUND,
        'message': 'The provided threat name could not be found in the database'
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
  def delete(self,name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    dao.delete_architectural_pattern(name)
    dao.close()

    resp_dict = {'message': 'Architectural Pattern successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ComponentAssetModelAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get the asset model for a specific component',
    nickname='component-asset-model-get',
    parameters=[
      {
        "name": "component",
        "description": "The component",
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
  # endregion
  def get(self, component):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = ArchitecturalPatternDAO(session_id)
    dot_code = dao.get_component_asset_model(component)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,renderer='dot'), httplib.OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'

    return resp

class ComponentGoalModelAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get the goal model for a specific component',
    nickname='component-goal-model-get',
    parameters=[
      {
        "name": "component",
        "description": "The component",
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
  # endregion
  def get(self, component):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = ArchitecturalPatternDAO(session_id)
    dot_code = dao.get_component_goal_model(component)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,model_type='goal',renderer='dot'), httplib.OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'

    return resp

class ComponentModelAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get the component model for a specific architectural pattern',
    nickname='component-asset-model-get',
    parameters=[
      {
        "name": "ap_name",
        "description": "The architectural pattern",
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
  # endregion
  def get(self, ap_name):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = ArchitecturalPatternDAO(session_id)
    dot_code = dao.get_component_model(ap_name)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,renderer='dot'), httplib.OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'

    return resp

class WeaknessAnalysisAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get weakness analysis',
    nickname='architectural-patterns-weakness-analysis-get',
    responseClass=str.__name__,
    parameters=[
      {
        'name': 'session_id',
        'description': 'The ID of the session to use',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'architectural_pattern_name',
        'description': 'The architectural pattern name',
        'required': True,
        'allowMultiple': False,
        'type': 'string',
        'paramType': 'query'
      },
      {
        'name': 'environment_name',
        'description': 'The environment name',
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
  def get(self,architectural_pattern_name,environment_name):
    session_id = get_session_id(session, request)
    dao = ArchitecturalPatternDAO(session_id)
    cwm = dao.get_weakness_analysis(architectural_pattern_name,environment_name)
    dao.close()
    resp = make_response(json_serialize(cwm, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
