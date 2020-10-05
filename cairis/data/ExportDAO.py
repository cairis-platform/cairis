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
from cairis.core.Borg import Borg
from cairis.mio.ModelExport import extractModel,extractPackage,exportUserGoalWorkbook,exportPersonaCharacteristicsWorkbook
from os import read
from tempfile import mkstemp

__author__ = 'Shamal Faily'


class ExportDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'export')

  def file_export(self,pathValues):
    fileType = pathValues[1]
    if (fileType == 'xml'):
      return extractModel(self.session_id)
    else:
      return extractPackage(self.session_id)

  def architectural_pattern_export(self,apName, pathValues = []):
    try:
      return self.db_proxy.architecturalPatternToXml(apName);
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def user_goals_export(self,pathValues):
    wbName = pathValues[0]
    try:
      b = Borg()
      wbName = b.tmpDir + '/' + wbName
      exportUserGoalWorkbook(wbName,self.session_id)
      with open(wbName,'r+b') as f:
        buf = f.read()
      return buf
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def persona_characteristics_export(self,pathValues = []):
    try:
      b = Borg()
      fd, abs_path = mkstemp(suffix='.xlsx')
      exportPersonaCharacteristicsWorkbook(abs_path,self.session_id)
      with open(abs_path,'r+b') as f:
        buf = f.read()
      return buf
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def security_patterns_export(self,pathValues = []):
    try:
      return self.db_proxy.securityPatternsToXml();
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def grl_export(self,taskName,personaName,envName, pathValues = []):
    try:
      return self.db_proxy.pcToGrl(personaName,taskName,envName);
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
