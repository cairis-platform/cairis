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
import zipfile
from cairis.core.Borg import Borg
import io
from base64 import b64decode
__author__ = 'Shamal Faily'


class ExportDAO(CairisDAO):

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def file_export(self,fileName='',fileType='xml'):
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
     
      if (fileType == 'xml'):
        return xmlBuf
      else:
        return self.modelPackage(fileName,xmlBuf)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def modelPackage(self,fileName,xmlBuf):
    buf = io.BytesIO()
    zf = zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED)
    zf.writestr('model.xml',xmlBuf)

    apNames = self.db_proxy.getDimensionNames('component_view','')
    for apName in apNames:
      apBuf = self.architectural_pattern_export(apName)
      zf.writestr(apName + '.xml',apBuf)

    spNames = self.db_proxy.getDimensionNames('securitypattern','')
    if (len(spNames) > 0):
      spBuf = self.security_patterns_export()
      zf.writestr('security_patterns.xml',spBuf)

    for imgName,imgContent in self.db_proxy.getImages():
      zf.writestr(imgName,b64decode(imgContent))
    zf.close()
    return buf.getvalue()


  def architectural_pattern_export(self,apName):
    try:
      return self.db_proxy.architecturalPatternToXml(apName);
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def security_patterns_export(self):
    try:
      return self.db_proxy.securityPatternsToXml();
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def grl_export(self,taskName,personaName,envName):
    try:
      return self.db_proxy.pcToGrl(personaName,taskName,envName);
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
