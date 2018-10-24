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
__author__ = 'Shamal Faily'


class ExportDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def file_export(self):
    try:
      xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE cairis_model PUBLIC "-//CAIRIS//DTD MODEL 1.0//EN" "http://cairis.org/dtd/cairis_model.dtd">\n<cairis_model>\n\n\n'
      xmlBuf+= self.db_proxy.tvTypesToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.domainValuesToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.projectToXml(0) + '\n\n'
      xmlBuf+= self.db_proxy.riskAnalysisToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.usabilityToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.goalsToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.associationsToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.synopsesToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.misusabilityToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.dataflowsToXml(0)[0] + '\n\n'
      xmlBuf+= self.db_proxy.locationsToXml()[0] + '\n\n</cairis_model>'
      return xmlBuf
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def architectural_pattern_export(self,apName):
    try:
      return self.db_proxy.architecturalPatternToXml(apName);
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def grl_export(self,taskName,personaName,envName):
    try:
      return self.db_proxy.pcToGrl(personaName,taskName,envName);
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
