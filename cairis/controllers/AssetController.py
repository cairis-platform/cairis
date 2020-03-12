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
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator
from importlib import import_module


__author__ = 'Robin Quetin, Shamal Faily'


class AssetByEnvironmentNamesAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetDAO'),'AssetDAO')


  def get(self, environment):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    assets = dao.get_asset_names(environment=environment)
    dao.close()

    resp = make_response(json_serialize(assets, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


class AssetNamesAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetDAO'),'AssetDAO')

  def get(self):
    session_id = request.args.get('session_id', None)

    dao = self.DAOModule(session_id)
    assets_names = dao.get_asset_names()
    dao.close()

    resp = make_response(json_serialize(assets_names, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


class AssetModelAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetDAO'),'AssetDAO')

  def get(self, environment,asset):
    session_id = get_session_id(session, request)
    hide_concerns = request.args.get('hide_concerns', '1')
    if hide_concerns == '0' or hide_concerns == 0:
      hide_concerns = False
    else:
      hide_concerns = True
    if asset == 'all':
      asset = ''
    model_generator = get_model_generator()

    dao = self.DAOModule(session_id)
    dot_code = dao.get_asset_model(environment, asset, hide_concerns=hide_concerns)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,renderer='dot'), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'

    return resp


class AssetTypesAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetDAO'),'AssetDAO')

  def get(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = self.DAOModule(session_id)
    assets = dao.get_asset_types(environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(assets, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = self.DAOModule(session_id)
    new_value_type = dao.type_from_json(request)
    dao.add_asset_type(new_value_type, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Asset type successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp


class AssetTypeByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetDAO'),'AssetDAO')

  def get(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = self.DAOModule(session_id)
    asset_type = dao.get_asset_type_by_name(name=name, environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(asset_type, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = self.DAOModule(session_id)
    asset_type = dao.type_from_json(request)
    dao.update_asset_type(asset_type, name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Asset type successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    environment_name = request.args.get('environment', '')

    dao = self.DAOModule(session_id)
    dao.delete_asset_type(name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Asset type successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class AssetValuesAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetDAO'),'AssetDAO')

  def get(self, environment_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    assets = dao.get_asset_values(environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(assets, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class AssetValueByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetDAO'),'AssetDAO')

  def get(self, name, environment_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    asset_value = dao.get_asset_value_by_name(name=name, environment_name=environment_name)
    dao.close()

    resp = make_response(json_serialize(asset_value, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name, environment_name):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    asset_value = dao.type_from_json(request)
    dao.update_asset_value(asset_value, name=name, environment_name=environment_name)
    dao.close()

    resp_dict = {'message': 'Asset type successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class AssetAssociationByNameAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetAssociationDAO'),'AssetAssociationDAO')

  def get(self,environment_name,head_name,tail_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    assoc = dao.get_asset_association(environment_name,head_name,tail_name)
    dao.close()
    resp = make_response(json_serialize(assoc, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def delete(self,environment_name,head_name,tail_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.delete_asset_association(environment_name,head_name,tail_name)
    dao.close()

    resp_dict = {'message': 'Asset Association successfully deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,environment_name,head_name,tail_name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    assoc = dao.from_json(request)
    dao.update_asset_association(environment_name,head_name,tail_name,assoc)
    dao.close()
    resp_dict = {'message': 'Asset Association successfully updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp



class AssetAssociationAPI(Resource):

  def __init__(self):
    self.DAOModule = getattr(import_module('cairis.data.AssetAssociationDAO'),'AssetAssociationDAO')

  def get(self):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    assocs = dao.get_asset_associations()
    dao.close()
    resp = make_response(json_serialize(assocs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp


  def post(self):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)
    assoc = dao.from_json(request)
    dao.add_asset_association(assoc)
    dao.close()

    resp_dict = {'message': 'Asset Association successfully added'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp
