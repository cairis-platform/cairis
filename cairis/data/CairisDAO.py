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
  from http.client import CONFLICT
else:
  import httplib
  from httplib import CONFLICT
import logging
from cairis.core.Borg import Borg
from cairis.core.ARM import SessionNotFound
from cairis.daemon.CairisHTTPError import CairisHTTPError, NoSessionError, ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from cairis.core.ValueType import ValueType
from cairis.tools.JsonConverter import json_serialize, json_deserialize
from cairis.tools.ModelDefinitions import ValueTypeModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Robin Quetin, Shamal Faily'

class CairisDAO(object):
  def __init__(self, session_id, dimension = ''):
    b = Borg()
    self.db_proxy = self.get_dbproxy(session_id)
    self.session_id = session_id
    self.theDimension = dimension
    self.logger = logging.getLogger('cairisd')
    self.logger.setLevel(b.logLevel)

  def dimension(self): return self.theDimension

  def nameCheck(self,newObjtName):
    self.db_proxy.nameCheck(newObjtName,self.theDimension)

  def close(self):
    if self.db_proxy.conn is not None:
      self.db_proxy.close()

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    return json['object']

  def type_from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, ValueTypeModel.required)
    json_dict['__python_obj__'] = ValueType.__module__+'.'+ValueType.__name__

    value_type = json_serialize(json_dict)
    value_type = json_deserialize(value_type)
    if not isinstance(value_type, ValueType):
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())
    else:
      return value_type

  def simplify(self, obj):
    raise NotImplementedError('from_json is not yet implemented by subclass')

  def get_dbproxy(self, session_id):
    """
    Searches the MySQLDatabaseProxy instance associated with the session ID.
    :param
      session_id: The session ID
    :type
      session_id: str
    :rtype
      MySQLDatabaseProxy
    :return
      The MySQLDatabaseProxy instance associated with the session ID
    :raise
      CairisHTTPError
    """
    if session_id:
      b = Borg()
      try:
        db_proxy = b.get_dbproxy(session_id)
      except SessionNotFound as ex:
        raise NoSessionError(ex)

      if isinstance(db_proxy, MySQLDatabaseProxy):
        if db_proxy.conn is None:
          db_proxy.reconnect(session_id=session_id)
        return db_proxy
      else:
        raise CairisHTTPError(
          status_code=CONFLICT,
          message='The database connection was not properly set up. Please try to reset the connection.'
        )
    else:
      raise MissingParameterHTTPError(
        param_names=['session_id']
      )
