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
from cairis.data.DomainPropertyDAO import DomainPropertyDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.MessageDefinitions import DomainPropertyMessage, ValueTypeMessage
from cairis.tools.ModelDefinitions import DomainPropertyModel, ValueTypeModel
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class DomainPropertiesAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)

    dao = DomainPropertyDAO(session_id)
    domain_properties = dao.get_domain_properties(constraint_id=constraint_id)
    dao.close()

    resp = make_response(json_serialize(domain_properties, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = DomainPropertyDAO(session_id)
    new_domain_property = dao.from_json(request)
    dao.add_domain_property(new_domain_property)
    dao.close()

    resp_dict = {'message': new_domain_property.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class DomainPropertiesByNameAPI(Resource):

  def get(self, name):
    session_id = get_session_id(session, request)

    dao = DomainPropertyDAO(session_id)
    domain_property = dao.get_domain_property_by_name(name=name)
    dao.close()

    resp = make_response(json_serialize(domain_property, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)

    dao = DomainPropertyDAO(session_id)
    req = dao.from_json(request)
    dao.update_domain_property(req, name=name)
    dao.close()

    resp_dict = {'message': req.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)

    dao = DomainPropertyDAO(session_id)
    dao.delete_domain_property(name=name)
    dao.close()

    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp
