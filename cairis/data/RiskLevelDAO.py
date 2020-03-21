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
from cairis.daemon.CairisHTTPError import ARMHTTPError
import cairis.core.armid
from cairis.data.CairisDAO import CairisDAO

__author__ = 'Shamal Faily'


class RiskLevelDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_risk_level(self,assetName, pathValues = []):
    return self.get_risk_level_by_environment(assetName,'',pathValues)

  def get_risk_level_by_environment(self,assetName,envName = '', pathValues = []):
    try:
      riskLevel = self.db_proxy.assetRiskLevel(assetName,envName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return riskLevel

  def get_risk_threat_level(self,assetName,threatName,pathValues = []):
    return self.get_risk_threat_level_by_environment(assetName,threatName,'',pathValues)

  def get_risk_threat_level_by_environment(self,assetName,threatName,envName = '', pathValues = []):
    try:
      riskLevel = self.db_proxy.assetThreatRiskLevel(assetName,threatName,envName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return riskLevel
