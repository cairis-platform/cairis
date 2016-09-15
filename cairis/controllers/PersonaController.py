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
from flask import request, session, make_response
from flask.ext.restful import Resource
from flask_restful_swagger import swagger
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.PersonaDAO import PersonaDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import PersonaMessage, PersonaEnvironmentPropertiesMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import PersonaModel, PersonaEnvironmentPropertiesModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator
__author__ = 'Shamal Faily'


class PersonasAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get all personas',
    nickname='personas-get',
    responseClass=PersonaModel.__name__,
    responseContainer='List',
    parameters=[
      {
        "name": "constraint_id",
        "description": "The constraint to use when querying the database",
        "default": -1,
        "required": False,
        "allowMultiple": False,
        "dataType": int.__name__,
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
  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = PersonaDAO(session_id)
    personas = dao.get_personas(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(personas, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Creates a new persona',
    nickname='personas-post',
    parameters=[
      {
        "name": "body",
        "description": "The serialized version of the new persona to be added",
        "required": True,
        "allowMultiple": False,
        "type": PersonaMessage.__name__,
        "paramType": "body"
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
        'message': 'One or more attributes are missing'
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

    dao = PersonaDAO(session_id)
    new_persona = dao.from_json(request)
    persona_id = dao.add_persona(new_persona)
    dao.close()

    resp_dict = {'message': 'Persona successfully added', 'persona_id': persona_id}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class PersonaByNameAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get a persona by name',
    nickname='persona-by-name-get',
    responseClass=PersonaModel.__name__,
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
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  # endregion
  def get(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    persona = dao.get_persona_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(persona, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Docs
  @swagger.operation(
    notes='Updates a persona',
    nickname='persona-by-name-put',
    parameters=[
      {
        'name': 'body',
        "description": "JSON serialized version of the persona to be updated",
        "required": True,
        "allowMultiple": False,
        'type': PersonaMessage.__name__,
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
        'code': httplib.BAD_REQUEST,
        'message': 'The provided file is not a valid XML file'
      },
      {
        'code': httplib.BAD_REQUEST,
        'message': '''Some parameters are missing. Be sure 'persona' is defined.'''
      }
    ]
  )
  # endregion
  def put(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    req = dao.from_json(request)
    dao.update_persona(req, name=name)
    dao.close()

    resp_dict = {'message': 'Persona successfully updated'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Deletes an existing persona',
    nickname='persona-by-name-delete',
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
        'message': 'One or more attributes are missing'
      },
      {
        'code': httplib.NOT_FOUND,
        'message': 'The provided persona name could not be found in the database'
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
  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    dao.delete_persona(name=name)
    dao.close()

    resp_dict = {'message': 'Persona successfully deleted'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class PersonaModelByNameAPI(Resource):
  #region Swagger Doc
  @swagger.operation(
    notes='Get persona model for a specific persona',
    responseClass=str.__name__,
    nickname='persona-model-by-name-get',
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
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  #endregion
  def get(self, persona, variable, characteristic):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = PersonaDAO(session_id)
    if variable == 'All':  variable = ''
    if characteristic == 'All': characteristic = ''
    dot_code = dao.get_persona_model(persona,variable,characteristic)
    dao.close()

    resp = make_response(model_generator.generate(dot_code, model_type='persona', renderer='dot'), httplib.OK)

    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp

class PersonaNamesAPI(Resource):
  #region Swagger Docs
  @swagger.operation(
    notes='Get all persona names',
    nickname='persona-names-get',
    responseClass=str.__name__,
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
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  #endregion
  def get(self):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    persona_names = dao.get_persona_names()
    dao.close()

    resp = make_response(json_serialize(persona_names, session_id=session_id), httplib.OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class PersonaTypesAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get all persona types',
    nickname='persona-types-get',
    responseClass=ValueTypeModel.__name__,
    responseContainer='List',
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
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  # endregion
  def get(self):
    session_id = get_session_id(session, request)
    dao = PersonaDAO(session_id)
    pTypes = dao.get_persona_types()
    dao.close()
    resp = make_response(json_serialize(pTypes, session_id=session_id), httplib.OK)
    resp.contenttype = 'application/json'
    return resp

class PersonaEnvironmentPropertiesAPI(Resource):
  # region Swagger Doc
  @swagger.operation(
    notes='Get the environment properties for a specific persona',
    nickname='persona-envprops-by-name-get',
    responseClass=PersonaEnvironmentPropertiesModel.__name__,
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
        "code": httplib.BAD_REQUEST,
        "message": "The database connection was not properly set up"
      }
    ]
  )
  # endregion
  def get(self, persona_name):
    session_id = get_session_id(session, request)
    dao = PersonaDAO(session_id)
    persona_props = dao.get_persona_props(name=persona_name)
    dao.close()
    resp = make_response(json_serialize(asset_props, session_id=session_id))
    resp.contenttype = 'application/json'
    return resp

  # region Swagger Doc
  @swagger.operation(
    notes='Updates the environment properties for a specific persona',
    nickname='persona-envprops-by-name-put',
    parameters=[
      {
        "name": "body",
        "required": True,
        "allowMultiple": False,
        "dataType": PersonaEnvironmentPropertiesMessage.__name__,
        "paramType": "body"
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
  def put(self, persona_name):
    session_id = get_session_id(session, request)
    dao = PersonaDAO(session_id)
    persona_prop = dao.from_json(request, to_props=True)
    dao.update_persona_properties(persona_prop, name=persona_name)
    dao.close()
    resp_dict = {'message': 'The persona properties were successfully updated.'}
    resp = make_response(json_serialize(resp_dict), httplib.OK)
    resp.contenttype = 'application/json'
    return resp
