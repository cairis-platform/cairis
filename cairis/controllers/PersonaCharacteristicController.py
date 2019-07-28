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
from flask import session, request, make_response
from flask_restful import Resource
from cairis.data.PersonaCharacteristicDAO import PersonaCharacteristicDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import PersonaCharacteristicMessage
from cairis.tools.ModelDefinitions import PersonaCharacteristicModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class PersonaCharacteristicsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = PersonaCharacteristicDAO(session_id)
    pcs = dao.get_persona_characteristics(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(pcs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = PersonaCharacteristicDAO(session_id)
    new_pc,ps,rss,rcs = dao.from_json(request)
    dao.add_persona_characteristic(new_pc)
    if (ps != None):
      dao.assignIntentionalElements(ps,rss,rcs)
    dao.close()

    resp_dict = {'message': new_pc.characteristic() + ' created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class PersonaCharacteristicByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = PersonaCharacteristicDAO(session_id)
    found_pc = dao.get_persona_characteristic(name)
    dao.close()

    resp = make_response(json_serialize(found_pc, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaCharacteristicDAO(session_id)
    upd_pc,ps,rss,rcs = dao.from_json(request)
    dao.update_persona_characteristic(upd_pc, name)
    if (ps != None):
      dao.assignIntentionalElements(ps,rss,rcs)
    dao.close()

    resp_dict = {'message': upd_pc.characteristic() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = PersonaCharacteristicDAO(session_id)
    dao.delete_persona_characteristic(name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class PersonaCharacteristicsSummaryAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = PersonaCharacteristicDAO(session_id)
    objts = dao.get_persona_characteristics_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp
