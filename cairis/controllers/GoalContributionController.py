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
import http.client
from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, OK
from flask import session, request, make_response
from flask_restful import Resource
from cairis.data.GoalContributionDAO import GoalContributionDAO
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator

__author__ = 'Shamal Faily'


class GoalContributionsAPI(Resource):

  def get(self):
    session_id = get_session_id(session, request)
    dao = GoalContributionDAO(session_id)
    gcs = dao.get_goal_contributions()
    dao.close()
    resp = make_response(json_serialize(gcs, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = GoalContributionDAO(session_id)
    new_gc = dao.from_json(request)
    dao.add_goal_contribution(new_gc)
    dao.close()
    resp_dict = {'message': new_gc.source() + ' / ' + new_gc.destination() + ' goal contribution created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class GoalContributionByNameAPI(Resource):

  def get(self, sourceName, targetName):
    session_id = get_session_id(session, request)
    dao = GoalContributionDAO(session_id)
    found_gc = dao.get_goal_contributions(sourceName,targetName)
    dao.close()
    resp = make_response(json_serialize(found_gc, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

  def put(self, sourceName, targetName):
    session_id = get_session_id(session, request)
    dao = GoalContributionDAO(session_id)
    upd_gc = dao.from_json(request)
    dao.update_goal_contribution(upd_gc, sourceName, targetName)
    dao.close()
    resp_dict = {'message': upd_gc.source() + ' / ' + upd_gc.destination() + ' goal contribution updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self, sourceName, targetName):
    session_id = get_session_id(session, request)
    dao = GoalContributionDAO(session_id)
    dao.delete_goal_contribution(sourceName,targetName)
    dao.close()
    resp_dict = {'message': sourceName + ' / ' + targetName + ' goal contribution deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp
