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
from cairis.tools.JsonConverter import json_serialize
from cairis.tools.SessionValidator import get_session_id, get_model_generator
from cairis.core.ARM import ARMException, DatabaseProxyException
from cairis.daemon.CairisHTTPError import CairisHTTPError, ARMHTTPError, MissingParameterHTTPError,ObjectNotFoundHTTPError
from importlib import import_module
from tempfile import mkstemp
import codecs
import os

__author__ = 'Robin Quetin, Shamal Faily'


class ObjectsAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get('constraint_id', -1)
    dao = self.DAOModule(session_id)
    objts = dao.get_objects(constraint_id)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)

    dao = self.DAOModule(session_id)

    new_objt = None
    if (dao.dimension() == 'usecase'):
      new_objt, ucContribs = dao.from_json(request)
    elif (dao.dimension() == 'persona_characteristic'):
      new_objt,ps,rss,rcs = dao.from_json(request)
    else:
      new_objt = dao.from_json(request)
 
    if (dao.dimension() != ''):
      objtName = ''
      if (isinstance(new_objt,dict)):
        objtName = new_objt['theName']
      else:
        objtName = new_objt.name()
      dao.nameCheck(objtName)

    postMsg = dao.add_object(new_objt)

    if (dao.dimension() == 'usecase'):
      for rc in ucContribs:
        dao.assign_usecase_contribution(rc)
    elif(dao.dimension() == 'persona_characteristic'):
      if (ps != None):
        dao.assignIntentionalElements(ps,rss,rcs)

    dao.close()
    resp_dict = {}
    if (postMsg != None):
      resp_dict = {'message': postMsg}
    elif (isinstance(new_objt,dict)):
      resp_dict = {'message': new_objt['theName'] + ' created'}
    else:
      resp_dict = {'message': new_objt.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.contenttype = 'application/json'
    return resp

class ObjectsByMethodAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'put_method' in kwargs:
      self.thePutMethod = kwargs['put_method']
    if 'post_method' in kwargs:
      self.thePostMethod = kwargs['post_method']
    if 'path_parameters' in kwargs:
      self.thePathParameters = kwargs['path_parameters']
    self.isType = False
    if 'isType' in kwargs:
      self.isType = kwargs['isType']

  def get(self):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objts = getattr(dao, self.theGetMethod)(pathValues)
    dao.close()

    resp = None
    if (self.DAOModule.__name__ == 'ExportDAO'):
      resp = make_response(objts)
      if (self.theGetMethod == 'file_export' and pathValues[1] == 'cairis'):
        resp.headers["Content-Type"] = 'application/octet-stream' 
      elif (self.theGetMethod == 'user_goals_export'):
        resp.headers["Content-Type"] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      else:
        resp.headers["Content-Type"] = 'application/xml'

      if (self.theGetMethod == 'file_export'): 
        resp.headers["Content-Disposition"] = 'Attachment; filename=' + pathValues[0] + '.'  + pathValues[1]
      elif (self.theGetMethod == 'user_goals_export' or self.theGetMethod == 'persona_characteristics_export'):
        resp.headers["Content-Disposition"] = 'Attachment; filename=' + pathValues[0] + '.xlsx'
      else:
        resp.headers["Content-Disposition"] = 'Attachment; filename=' + pathValues[0]
    else:
      resp = make_response(json_serialize(objts, session_id=session_id), OK)
      resp.contenttype = 'application/json'
    return resp

  def put(self):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objt = dao.from_json(request)
    getattr(dao, self.thePutMethod)(objt,pathValues)
    resp_dict = {'message': 'Object updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objt = None
    if (dao.dimension() == 'project'):
      objt = None
    elif (dao.dimension() == 'requirement'):
     domain_name = pathValues[2]
     envName = pathValues[3]
     if (envName != None):
       domain_name = envName
     objt = dao.from_json(request,domain_name)
    elif self.isType:
      objt = dao.type_from_json(request)
    else:
      objt = dao.from_json(request)
    postMsg = getattr(dao, self.thePostMethod)(objt,pathValues)
    resp_dict = {}
    if (postMsg != None):
      resp_dict = {'message': postMsg}
    else:
      resp_dict = {'message': objt.name() + ' created'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class ObjectsByMethodAndFourParametersAPI(Resource):
  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'del_method' in kwargs:
      self.theDelMethod = kwargs['del_method']

  def get(self,p1,p2,p3,p4):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objts = getattr(dao, self.theGetMethod)(p1,p2,p3,p4,pathValues)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self,p1,p2,p3,p4):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    getattr(dao, self.theDelMethod)(p1,p2,p3,p4,pathValues)
    resp_dict = {'message': p2 + ' / ' + p4 + ' deleted'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp



class ObjectsByMethodAndThreeParametersAPI(Resource):
  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    self.thePostMessage = ''
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'post_method' in kwargs:
      self.thePostMethod = kwargs['post_method']
    if 'put_method' in kwargs:
      self.thePutMethod = kwargs['put_method']
    if 'del_method' in kwargs:
      self.theDelMethod = kwargs['del_method']
    if 'path_parameters' in kwargs:
      self.thePathParameters = kwargs['path_parameters']
    self.isType = False
    if 'isType' in kwargs:
      self.isType = kwargs['isType']

  def get(self,p1,p2,p3):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objts = getattr(dao, self.theGetMethod)(p1,p2,p3,pathValues)
    dao.close()
    resp = None
    if (self.DAOModule.__name__ == 'ExportDAO'):
      fileName = pathValues[0]
      if (fileName == ''):
        fileName = p1
      resp = make_response(objts)
      resp.headers["Content-Type"] = 'application/grl'
      resp.headers["Content-Disposition"] = 'Attachment; filename=' + fileName + '.grl'
    else:
      resp = make_response(json_serialize(objts, session_id=session_id), OK)
      resp.contenttype = 'application/json'
    return resp

  def post(self,p1,p2,p3):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    postMsg = getattr(dao, self.thePostMethod)(p1,p2,p3,pathValues)
    resp_dict = {'message': self.thePostMessage}
    if (postMsg != None):
      resp_dict = {'message': postMsg}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,p1,p2,p3):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objt = None
    if self.isType:
      objt = dao.type_from_json(request)
    else:
      objt = dao.from_json(request)
    getattr(dao, self.thePutMethod)(objt,p1,p2,p3,pathValues)
    resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self,p1,p2,p3):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    getattr(dao, self.theDelMethod)(p1,p2,p3,pathValues)
    resp_dict = {'message': p1 + ' / ' + p2 + ' / ' + p3 + ' deleted'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ObjectsByMethodAndTwoParametersAPI(Resource):
  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'post_method' in kwargs:
      self.thePostMethod = kwargs['post_method']
    if 'put_method' in kwargs:
      self.thePutMethod = kwargs['put_method']
    if 'del_method' in kwargs:
      self.theDelMethod = kwargs['del_method']
    if 'path_parameters' in kwargs:
      self.thePathParameters = kwargs['path_parameters']
    self.thePostMessage = ''
    if 'post_message' in kwargs:
      self.thePostMessage = kwargs['post_message']
    self.theDelMessage = ''
    if 'del_message' in kwargs:
      self.theDelMessage = kwargs['del_message']

  def get(self,p1,p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objts = getattr(dao, self.theGetMethod)(p1,p2,pathValues)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def post(self,p1,p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    postMsg = getattr(dao, self.thePostMethod)(p1,p2,pathValues)
    resp_dict = {'message': self.thePostMessage}
    if (postMsg != None):
      resp_dict = {'message': postMsg}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,p1,p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objt = dao.from_json(request)
    getattr(dao, self.thePutMethod)(objt,p1,p2,pathValues)
    resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self,p1,p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    delMsg = getattr(dao, self.theDelMethod)(p1,p2,pathValues)
    resp_dict = None
    if (delMsg != None):
      resp_dict = {'message': delMsg}
    elif (self.theDelMessage != ''):
      resp_dict = {'message': self.theDelMessage}
    else:
      resp_dict = {'message': p1 + ' / ' + p2 + ' deleted'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class ObjectsByMethodAndParameterAPI(Resource):
  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'put_method' in kwargs:
      self.thePutMethod = kwargs['put_method']
    if 'post_method' in kwargs:
      self.thePostMethod = kwargs['post_method']
    if 'del_method' in kwargs:
      self.theDelMethod = kwargs['del_method']
    if 'path_parameters' in kwargs:
      self.thePathParameters = kwargs['path_parameters']
    self.isType = False
    if 'isType' in kwargs:
      self.isType = kwargs['isType']
    self.thePostMessage = ''
    if 'post_message' in kwargs:
      self.thePostMessage = kwargs['post_message']


  def get(self,parameter_string):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      if (self.DAOModule.__name__ == 'CountermeasureDAO' and parameterName in ['requirement','role']):
        pathValues.append(request.args.getlist(parameterName))
      else:
        pathValues.append(request.args.get(parameterName,defaultValue))
    objts = getattr(dao, self.theGetMethod)(parameter_string,pathValues)
    dao.close()
    resp = None
    if (self.DAOModule.__name__ == 'ExportDAO'):
      resp = make_response(objts)
      fileName = pathValues[0]
      if (fileName == ''):
        fileName = parameter_string
      resp.headers["Content-Type"] = 'application/xml'
      resp.headers["Content-Disposition"] = 'Attachment; filename=' + pathValues[0] + '.xml'


    else:
      resp = make_response(json_serialize(objts, session_id=session_id), OK)
      resp.contenttype = 'application/json'
    return resp

  def post(self,parameter_string):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    postMsg = getattr(dao, self.thePostMethod)(parameter_string,pathValues)
    resp_dict = {'message': self.thePostMessage}
    if postMsg != None:
      resp_dict = {'message': postMsg}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,parameter_string):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objt = None
    if self.isType:
      objt = dao.type_from_json(request)
    else:
      objt = dao.from_json(request)
    getattr(dao, self.thePutMethod)(objt,parameter_string,pathValues)
    resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self,parameter_string):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    delMsg = getattr(dao, self.theDelMethod)(parameter_string,pathValues)
    resp_dict = {'message': parameter_string + ' deleted'}
    if (delMsg != None):
      resp_dict = {'message': delMsg}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp


class ObjectsByNameAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self,parameter_string):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objts = dao.get_objects(parameter_string)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class ConstrainedObjectsByNameAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.theConstraintParameter = kwargs['constraint_parameter']

  def get(self,parameter_string):
    session_id = get_session_id(session, request)
    constraint_id = request.args.get(self.theConstraintParameter, -1)
    dao = self.DAOModule(session_id)
    objts = dao.get_objects_by_names(parameter_string,constraint_id)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp



class ObjectByNameAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self, name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.get_object_by_name(name)
    dao.close()
    resp = make_response(json_serialize(objt, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)

    objt = None
    if (dao.dimension() == 'usecase'):
      objt, ucContribs = dao.from_json(request)
    elif (dao.dimension() == 'persona_characteristic'):
      objt,ps,rss,rcs = dao.from_json(request)
    else:
      objt = dao.from_json(request)

    if (dao.dimension() != ''):
      objtName = ''
      if (isinstance(objt,dict)):
        objtName = objt['theName']
      else:
        objtName = objt.name()
      if ((name != objtName) and (name.lower() != objtName.lower())):
        dao.nameCheck(objtName)
    dao.update_object(objt, name)

    if (dao.dimension() == 'usecase'):
      dao.remove_usecase_contributions(objt)
      for rc in ucContribs:
        dao.assign_usecase_contribution(rc)
    elif(dao.dimension() == 'persona_characteristic'):
      if (ps != None):
        dao.assignIntentionalElements(ps,rss,rcs)

    dao.close()
    resp_dict = {}
    if (isinstance(objt,dict)):
      resp_dict = {'message': objt['theName'] + ' updated'}
    else:
      resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, name):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.delete_object(name)
    dao.close()
    resp_dict = {'message': name + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ObjectByTwoParametersAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self, p1, p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.get_object_by_name(p1, p2)
    dao.close()
    resp = make_response(json_serialize(objt, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, p1, p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.from_json(request)
    dao.update_object(objt, p1, p2)
    dao.close()
    resp_dict = {}
    if (isinstance(objt,dict)):
      resp_dict = {'message': objt['theName'] + ' updated'}
    else:
      resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, p1, p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.delete_object(p1, p2)
    dao.close()
    resp_dict = {'message': p1 + ' / ' + p2 + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ObjectsSummaryAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objts = dao.get_objects_summary()
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id))
    resp.headers['Content-Type'] = "application/json"
    return resp

class ObjectsByTwoParametersAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self, p1, p2):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objts = dao.get_objects_by_2parameters(p1,p2)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ObjectByThreeParametersAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self, p1, p2, p3):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.get_object_by_3parameters(p1,p2,p3)
    dao.close()
    resp = make_response(json_serialize(objt, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, p1, p2, p3):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.from_json(request)
    if (dao.dimension() != ''):
      objtName = ''
      if (isinstance(objt,dict)):
        objtName = objt['theName']
      else:
        objtName = objt.name()
      if ((p3 != objtName) and (p3.lower() != objtName.lower())):
        dao.nameCheck(objtName)
    dao.update_object_by_3parameters(p1,p2,p3,objt)
    dao.close()
    resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, p1, p2, p3):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.delete_object_by_3parameters(p1,p2,p3)
    dao.close()
    resp_dict = {'message': p3 + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp


class ObjectByFourParametersAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])

  def get(self, p1, p2, p3, p4):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.get_object_by_4parameters(p1,p2,p3,p4)
    dao.close()
    resp = make_response(json_serialize(objt, session_id=session_id), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def put(self, p1, p2, p3, p4):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.from_json(request)
    dao.update_object_by_4parameters(p1,p2,p3,p4,objt)
    dao.close()
    resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def post(self, p1, p2, p3, p4):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    objt = dao.from_json(request)
    dao.add_object(objt)
    dao.close()
    resp_dict = {'message': objt.name() + ' created'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

  def delete(self, p1, p2, p3, p4):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    dao.delete_object_by_4parameters(p1,p2,p3,p4)
    dao.close()
    resp_dict = {'message': p1 + ' / ' + p2 + ' / ' + p3 + ' / ' + p4 + ' deleted'}
    resp = make_response(json_serialize(resp_dict), OK)
    resp.headers['Content-type'] = 'application/json'
    return resp

class ModelByParameterAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'path_parameters' in kwargs:
      self.thePathParameters = kwargs['path_parameters']
    self.theModelType = ''
    if 'model_type' in kwargs:
      self.theModelType = kwargs['model_type']
    self.theRenderer = 'dot'
    if 'renderer' in kwargs:
      self.theRenderer = kwargs['renderer']

  def get(self, parameter_string):
    session_id = get_session_id(session, request)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    model_generator = get_model_generator()
    dao = self.DAOModule(session_id)
    dot_code = getattr(dao, self.theGetMethod)(parameter_string,pathValues)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    if (self.theModelType == 'risk'):
      if pathValues[4] == 'Hierarchical':
        self.theRenderer = 'dot'
      elif pathValues[4] == 'Spring':
        self.theRenderer = 'fdp'
      elif pathValues[4] == 'Radial':
        self.theRenderer = 'twopi'
      else:
        self.theRenderer = 'circo'

    resp = make_response(model_generator.generate(dot_code, model_type = self.theModelType, renderer = self.theRenderer), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp


class ModelByTwoParametersAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'path_parameters' in kwargs:
      self.thePathParameters = kwargs['path_parameters']
    self.theModelType = ''
    if 'model_type' in kwargs:
      self.theModelType = kwargs['model_type']
    self.theRenderer = 'dot'
    if 'renderer' in kwargs:
      self.theRenderer = kwargs['renderer']

  def get(self, p1, p2):
    session_id = get_session_id(session, request)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    model_generator = get_model_generator()
    dao = self.DAOModule(session_id)
    dot_code = getattr(dao, self.theGetMethod)(p1,p2,pathValues)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,model_type = self.theModelType, renderer = self.theRenderer), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp

class ModelByThreeParametersAPI(Resource):

  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'path_parameters' in kwargs:
      self.thePathParameters = kwargs['path_parameters']
    self.theModelType = ''
    if 'model_type' in kwargs:
      self.theModelType = kwargs['model_type']
    self.theRenderer = 'dot'
    if 'renderer' in kwargs:
      self.theRenderer = kwargs['renderer']

  def get(self, p1, p2, p3):
    session_id = get_session_id(session, request)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    model_generator = get_model_generator()
    dao = self.DAOModule(session_id)
    dot_code = getattr(dao, self.theGetMethod)(p1,p2,p3,pathValues)
    dao.close()

    if not isinstance(dot_code, str):
      raise ObjectNotFoundHTTPError('The model')

    resp = make_response(model_generator.generate(dot_code,model_type = self.theModelType, renderer = self.theRenderer), OK)
    accept_header = request.headers.get('Accept', 'image/svg+xml')
    if accept_header.find('text/plain') > -1:
      resp.headers['Content-type'] = 'text/plain'
    else:
      resp.headers['Content-type'] = 'image/svg+xml'
    return resp

class WorkbookUploadAPI(Resource):
  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'post_method' in kwargs:
      self.thePostMethod = kwargs['post_method']

  def post(self):
    session_id = get_session_id(session, request)

    content_length = request.content_length
    max_length = 30*1024*1024
    if content_length > max_length:
      raise MissingParameterHTTPError(exception=RuntimeError('File exceeded maximum size (30MB)'))

    try:
      wb = request.files['file']
      fd, abs_path = mkstemp(suffix='.xlsx')
      fs_temp = open(abs_path, 'wb')
      fs_temp.write(wb.stream.read())
      fs_temp.close()
      os.close(fd)
      dao = self.DAOModule(session_id)
      postMsg = getattr(dao, self.thePostMethod)(abs_path)
      dao.close()
      os.remove(abs_path)
      resp_dict = {'message': postMsg}
      resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
      resp.contenttype = 'application/json'
      return resp
    except DatabaseProxyException as ex:
      raise ARMHTTPError(ex)
    except ARMException as ex:
      raise ARMHTTPError(ex)
    except LookupError as ex:
      raise MissingParameterHTTPError(param_names=['file'])
    except Exception as ex:
      raise CairisHTTPError(status_code=CONFLICT, message=str(ex), status='Unknown error')

class ObjectsByMethodAndSixParametersAPI(Resource):
  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'put_method' in kwargs:
      self.thePutMethod = kwargs['put_method']
    if 'del_method' in kwargs:
      self.theDelMethod = kwargs['del_method']

  def get(self,p1,p2,p3,p4,p5,p6):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objts = getattr(dao, self.theGetMethod)(p1,p2,p3,p4,p5,p6,pathValues)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,p1,p2,p3,p4,p5,p6):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objt = dao.from_json(request)
    getattr(dao, self.thePutMethod)(objt,p1,p2,p3,p4,p5,p6,pathValues)
    resp_dict = {'message': objt.name() + ' updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self,p1,p2,p3,p4,p5,p6):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    getattr(dao, self.theDelMethod)(p1,p2,p3,p4,p5,p6,pathValues)
    resp_dict = {'message': p1 + ' / ' + p2 + ' / ' + p4 + ' / ' +  p6 + ' deleted'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

class ObjectsByMethodAndFiveParametersAPI(Resource):
  def __init__(self,**kwargs):
    self.DAOModule = getattr(import_module('cairis.data.' + kwargs['dao']),kwargs['dao'])
    self.thePathParameters = []
    if 'get_method' in kwargs:
      self.theGetMethod = kwargs['get_method']
    if 'put_method' in kwargs:
      self.thePutMethod = kwargs['put_method']
    if 'del_method' in kwargs:
      self.theDelMethod = kwargs['del_method']

  def get(self,p1,p2,p3,p4,p5):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objts = getattr(dao, self.theGetMethod)(p1,p2,p3,p4,p5,pathValues)
    dao.close()
    resp = make_response(json_serialize(objts, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def put(self,p1,p2,p3,p4,p5):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    objt = dao.from_json(request)
    getattr(dao, self.thePutMethod)(objt,p1,p2,p3,p4,p5,pathValues)
    resp_dict = {'message': p1 + '/' + p2 + '/' + p3 + '/' + p4 + '/' +  p5 + ' updated'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp

  def delete(self,p1,p2,p3,p4,p5):
    session_id = get_session_id(session, request)
    dao = self.DAOModule(session_id)
    pathValues = []
    for parameterName,defaultValue in self.thePathParameters:
      pathValues.append(request.args.get(parameterName,defaultValue))
    getattr(dao, self.theDelMethod)(p1,p2,p3,p4,p5,pathValues)
    resp_dict = {'message': p1 + '/' + p2 + '/' + p3 + '/' + p4 + '/' +  p5 + ' deleted'}
    resp = make_response(json_serialize(resp_dict, session_id=session_id), OK)
    resp.contenttype = 'application/json'
    return resp
