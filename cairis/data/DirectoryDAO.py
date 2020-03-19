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
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError
from cairis.core.Directory import Directory
from cairis.data.CairisDAO import CairisDAO


__author__ = 'Shamal Faily'


class DirectoryDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_threat_directory(self, directory_entry, pathValues = []):
    if directory_entry == 'all':
      directory_entry = '' 
    try:
      tds = self.db_proxy.getThreatDirectory(directory_entry)
      tdObjts = []
      for td in tds:
        tdObjts.append(Directory(td[0],td[1],td[2],td[3],td[4]))
      return tdObjts
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_vulnerability_directory(self, directory_entry, pathValues = []):
    if directory_entry == 'all':
      directory_entry = '' 
    try:
      vds = self.db_proxy.getVulnerabilityDirectory(directory_entry)
      vdObjts = []
      for vd in vds:
        vdObjts.append(Directory(vd[0],vd[1],vd[2],vd[3],vd[4]))
      return vdObjts
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
