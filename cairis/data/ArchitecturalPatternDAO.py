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
from cairis.daemon.CairisHTTPError import ARMHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, SilentHTTPError
from cairis.data.CairisDAO import CairisDAO
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.ModelDefinitions import ArchitecturalPatternModel,ComponentModel,ConnectorModel,ComponentInterfaceModel,ComponentGoalAssociationModel,ComponentStructureModel
from cairis.tools.SessionValidator import check_required_keys

__author__ = 'Shamal Faily'


class ArchitecturalPatternDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)

  def get_architectural_patterns(self):
    try:
      cvs = self.db_proxy.getComponentViews()
      return self.realToFakeAPs(cvs)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_architectural_pattern(self,name):
    try:
      cvId = self.db_proxy.getDimensionId(name,'component_view')
      cv = self.db_proxy.getComponentViews(cvId)
      return self.realToFakeAP(cv[name])
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def realToFakeAPs(self,cvs):
    fakeAPs = []
    for cvKey in cvs:
      fakeAPs.append(self.realToFakeAP(cvs[cvKey]))
    return fakeAPs

  def realToFakeAP(self,cv):
    ap = {}
    ap['theName'] = cv.name()
    ap['theSynopsis'] = cv.synopsis()
    ap['theComponents'] = []
    for co in cv.components():
      fComp = {}
      fComp['theName'] = co.name()
      fComp['theDescription'] = co.description()
      fComp['theInterfaces'] = []
      for ci in co.interfaces():
        fci = {}
        fci['theName'] = ci[0]
        fci['theType'] = ci[1]
        fci['theAccessRight'] = ci[2]
        fci['thePrivilege'] = ci[3]
        fComp['theInterfaces'].append(fci)
      fComp['theStructure'] = []
      for cs in co.structure():
        fcs = {}
        fcs['theHeadAsset'] = cs[0]
        fcs['theHeadAdornment'] = cs[1]
        fcs['theHeadNav'] = cs[2]
        fcs['theHeadNry'] = cs[3]
        fcs['theHeadRole'] = cs[4]
        fcs['theTailRole'] = cs[5]
        fcs['theTailNry'] = cs[6]
        fcs['theTailNav'] = cs[7]
        fcs['theTailAdornment'] = cs[8]
        fcs['theTailAsset'] = cs[9]
        fComp['theStructure'].append(fcs)
      fComp['theRequirements'] = co.requirements()
      fComp['theGoals'] = co.goals()
      fComp['theGoalAssociations'] = []
      for cga in co.associations():
        fcga = {}
        fcga['theGoalName'] = cga[0] 
        fcga['theRefType'] = cga[1] 
        fcga['theSubGoalName'] = cga[2] 
        fcga['theRationale'] = cga[3] 
        fComp['theGoalAssociations'].append(fcga) 
      ap['theComponents'].append(fComp)
    ap['theConnectors'] = []
    for cn in cv.connectors():
      fConn = {} 
      fConn['theConnectorName'] = cn[0]
      fConn['theFromComponent'] = cn[1]
      fConn['theFromRole'] = cn[2]
      fConn['theFromInterface'] = cn[3]
      fConn['theToComponent'] = cn[4]
      fConn['theToInterface'] = cn[5]
      fConn['theToRole'] = cn[6]
      fConn['theAssetName'] = cn[7]
      fConn['theProtocol'] = cn[8]
      fConn['theAccessRight'] = cn[9]
      ap['theConnectors'].append(fConn)
    ap['theAttackSurfaceMetric'] = list(cv.attackSurfaceMetric())
    return ap
