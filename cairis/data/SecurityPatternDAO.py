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
from cairis.daemon.CairisHTTPError import ObjectNotFoundHTTPError, ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, SilentHTTPError
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.ModelDefinitions import SecurityPatternStructureModel, PatternRequirementModel, SecurityPatternModel
from cairis.tools.SessionValidator import check_required_keys, get_fonts
from cairis.core.SecurityPatternParameters import SecurityPatternParameters
from cairis.core.TemplateRequirementParameters import TemplateRequirementParameters
import cairis.core.AssetParametersFactory

__author__ = 'Shamal Faily'


class SecurityPatternDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'securitypattern')

  def get_objects(self,constraint_id=-1):
    try:
      sps = self.db_proxy.getSecurityPatterns()
      return self.realToFakeSPs(sps)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_object_by_name(self,name):
    try:
      spId = self.db_proxy.getDimensionId(name,'securitypattern')
      sps = self.db_proxy.getSecurityPatterns(spId)
      return self.realToFakeSP(sps[name])
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def delete_object(self,name):
    try:
      spId = self.db_proxy.getDimensionId(name,'securitypattern')
      self.db_proxy.deleteSecurityPattern(spId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def realToFakeSPs(self,sps):
    fakeSPs = []
    for spKey in sps:
      fakeSPs.append(self.realToFakeSP(sps[spKey]))
    return fakeSPs

  def realToFakeSP(self,rsp):
    sp = {}
    sp['theName'] = rsp.name()
    sp['theContext'] = rsp.context()
    sp['theProblem'] = rsp.problem()
    sp['theSolution'] = rsp.solution()
    sp['theRequirements'] = []
    for req in rsp.requirements():
      freq = {}
      freq["theName"] = req[1]
      freq["theDescription"] = req[2]
      freq["theType"] = req[0]
      freq["theRationale"] = req[3]
      freq["theFitCriterion"] = req[4]
      freq["theAsset"] = req[5]
      sp['theRequirements'].append(freq)
    sp['theConcernAssociations'] = []
    for cs in rsp.associations():
      fcs = {}
      fcs['theHeadAsset'] = cs[0]
      fcs['theHeadAdornment'] = cs[1]
      fcs['theHeadNry'] = cs[2]
      fcs['theHeadRole'] = cs[3]
      fcs['theTailRole'] = cs[4]
      fcs['theTailNry'] = cs[5]
      fcs['theTailAdornment'] = cs[6]
      fcs['theTailAsset'] = cs[7]
      sp['theConcernAssociations'].append(fcs)
    return sp

  def add_object(self,sp):
    spParams = self.fakeToRealSP(sp)
    try:
      if not self.check_existing_security_pattern(spParams.name()):
        self.db_proxy.addSecurityPattern(spParams)
      else:
        self.close()
        raise OverwriteNotAllowedHTTPError(obj_name=spParams.name())
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self,sp,name):
    try:
      spId = self.db_proxy.getDimensionId(name,'securitypattern')
      spParams = self.fakeToRealSP(sp)
      spParams.setId(spId)
      self.db_proxy.updateSecurityPattern(spParams)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_security_pattern(self,spName):
    try:
      self.db_proxy.nameCheck(spName, 'securitypattern')
      return False
    except DatabaseProxyException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
        self.close()
        raise ARMHTTPError(ex)
    except ARMException as ex:
      if str(ex.value).find('already exists') > -1:
        return True
        self.close()
        raise ARMHTTPError(ex)

  def fakeToRealSP(self,sp):
    spName = sp["theName"]
    spContext = sp["theContext"]
    spProb = sp["theProblem"]
    spSol = sp["theSolution"]
    spReqs = []
    for freq in sp["theRequirements"]:
      spReqs.append(TemplateRequirementParameters(freq["theName"],freq["theAsset"],freq["theType"],freq["theDescription"],freq["theRationale"],freq["theFitCriterion"]))
    spAssocs = []
    for cs in sp["theConcernAssociations"]:
      spAssocs.append((cs["theHeadAsset"],cs["theHeadAdornment"],cs["theHeadNry"],cs["theHeadRole"],cs["theTailRole"],cs["theTailNry"],cs["theTailAdornment"],cs["theTailAsset"]))
    spParams = SecurityPatternParameters(spName,spContext,spProb,spSol,spReqs,spAssocs)
    return spParams

  def situate_security_pattern(self,spName,envName,pathValues = []):
    spId = self.db_proxy.getDimensionId(spName,'securitypattern')
    patternStructure = self.db_proxy.patternStructure(spId)
    assetSet = set([])
    for assoc in patternStructure:
      assetSet.add(assoc[0])
      assetSet.add(assoc[7])
    assetParametersList = []
    for assetName in assetSet:
      assetParametersList.append(cairis.core.AssetParametersFactory.buildFromTemplate(assetName,[envName],self.db_proxy))
    self.db_proxy.addSituatedAssets(spId,assetParametersList)
    self.db_proxy.conn.commit()
