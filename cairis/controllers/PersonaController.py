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
from flask import request, session, make_response
from flask_restful import Resource
from cairis.daemon.CairisHTTPError import ARMHTTPError
from cairis.data.PersonaDAO import PersonaDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import PersonaMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import PersonaModel, PersonaEnvironmentPropertiesModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator
__author__ = 'Shamal Faily'


class PersonasAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = PersonaDAO(session_id)
    personas = dao.get_personas(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(personas, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    new_persona = dao.from_json(request)
    dao.add_persona(new_persona)
    dao.close()

    resp_dict = {'message': new_persona.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class PersonaByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    persona = dao.get_persona_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(persona, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    req = dao.from_json(request)
    dao.update_persona(req, name=name)
    dao.close()

    resp_dict = {'message': req.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    dao.delete_persona(name=name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class PersonaModelByNameAPI(Resource):

  def get(self, persona, variable, characteristic):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = PersonaDAO(session_id)
    if (variable == 'All' or variable == 'all'):  variable = ''
    if (characteristic == 'All' or characteristic == 'all'): characteristic = ''
    dot_code = dao.get_persona_model(persona,variable,characteristic)
    dao.close()

    resp = make_response(model_generator.generate(dot_code, model_type='persona', renderer='dot'), OK)

    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp

class PersonaCharacteristicsByNameAPI(Resource):

  def get(self, persona, variable, characteristic):
    session_id = get_session_id(session, request)
    model_generator = get_model_generator()

    dao = PersonaDAO(session_id)
    if (variable == 'All' or variable == 'all'):  variable = ''
    if (characteristic == 'All' or characteristic == 'all'): characteristic = ''
    char_names = dao.get_persona_characteristics(persona,variable,characteristic)
    dao.close()
    resp = make_response(json_serialize(char_names, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class PersonaNamesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)

    dao = PersonaDAO(session_id)
    persona_names = dao.get_persona_names()
    dao.close()

    resp = make_response(json_serialize(persona_names, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class PersonaTypesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = PersonaDAO(session_id)
    pTypes = dao.get_persona_types()
    dao.close()
    resp = make_response(json_serialize(pTypes, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class PersonasSummaryAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = PersonaDAO(session_id)
    objts = dao.get_personas_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp
