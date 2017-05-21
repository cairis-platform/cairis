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

from cairis.core.ARM import *
from cairis.daemon.CairisHTTPError import CairisHTTPError, ARMHTTPError
from cairis.data.CairisDAO import CairisDAO
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy

__author__ = 'Shamal Faily'


class DimensionDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def getDimensions(self,table,id):
    try:
      if (table == 'persona_characteristic_synopsis'):
        return self.getDimensionNames(table,'')
      else: 
        return self.db_proxy.getDimensions(table,id).keys()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def getDimensionNames(self,table,environment):
    try:
      return self.db_proxy.getDimensionNames(table,environment)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
