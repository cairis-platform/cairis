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
from cairis.data.ConceptReferenceDAO import ConceptReferenceDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import ConceptReferenceMessage
from cairis.tools.ModelDefinitions import ConceptReferenceModel
from cairis.tools.SessionValidator import get_session_id

__author__ = 'Shamal Faily'


class ConceptReferencesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = ConceptReferenceDAO(session_id)
    crs = dao.get_concept_references(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(crs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = ConceptReferenceDAO(session_id)
    new_cr = dao.from_json(request)
    dao.add_concept_reference(new_cr)
    dao.close()

    resp_dict = {'message': new_cr.name() + ' created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ConceptReferenceByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = ConceptReferenceDAO(session_id)
    found_cr = dao.get_concept_reference(name)
    dao.close()

    resp = make_response(json_serialize(found_cr, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = ConceptReferenceDAO(session_id)
    upd_cr = dao.from_json(request)
    dao.update_concept_reference(upd_cr, name)
    dao.close()

    resp_dict = {'message': upd_cr.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = ConceptReferenceDAO(session_id)
    dao.delete_concept_reference(name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp
