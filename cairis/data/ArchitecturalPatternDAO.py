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
      fakeAPs = []
      for cvKey in cvs:
        ap = {}
        ap['theName'] = cvs[cvKey].name()
        ap['theSynopsis'] = cvs[cvKey].synopsis()
        ap['theComponents'] = []
        for c in cvs[cvKey].components():
          fComp = {}
          fComp['theName'] = c.name()
          fComp['theDescription'] = c.description()
          fComp['theInterfaces'] = []
          for ci in c.interfaces():
            fci = {}
            fci['theInterfaceName'] = ci[0]
            fci['theInterfaceType'] = ci[1]
            fci['theAccessRight'] = ci[2]
            fci['theProtocol'] = ci[3]
            fComp['theInterfaces'].append(fci)
          fComp['theStructure'] = []
          for cs in c.structure():
            fcs = {}
            fcs['theHeadAsset'] = cs[0]
            fcs['theHeadAssetType'] = cs[1]
            fcs['theHeadNav'] = cs[2]
            fcs['theHeadNry'] = cs[3]
            fcs['theHeadRole'] = cs[4]
            fcs['theTailRole'] = cs[5]
            fcs['theTailNry'] = cs[6]
            fcs['theTailNav'] = cs[7]
            fcs['theTailAssetType'] = cs[8]
            fcs['theTailAsset'] = cs[9]
            fComp['theStructure'].append(fcs)
          fComp['theRequirements'] = c.requirements()
          fComp['theGoals'] = c.goals()
          fComp['theGoalAssociations'] = []
          for cga in c.associations():
            fcga = {}
            fcga['theHeadGoal'] = cga[0] 
            fcga['theRefType'] = cga[1] 
            fcga['theTailGoal'] = cga[2] 
            fcga['theRationale'] = cga[3] 
            fComp['theGoalAssociations'].append(fcga) 
          ap['theComponents'].append(fComp)
        ap['theConnectors'] = []
        for c in cvs[cvKey].connectors():
          fConn = {} 
          fConn['theConnectorName'] = c[0]
          fConn['theFromComponent'] = c[1]
          fConn['theFromRole'] = c[2]
          fConn['theFromInterface'] = c[3]
          fConn['theToComponent'] = c[4]
          fConn['theToInterface'] = c[5]
          fConn['theToRole'] = c[6]
          fConn['theAssetName'] = c[7]
          fConn['theProtocolName'] = c[8]
          fConn['theAccessRightName'] = c[9]
          ap['theConnectors'].append(fComp)
        ap['theAttackSurfaceMetric'] = cvs[cvKey].attackSurfaceMetric()
        fakeAPs.append(ap)
      return fakeAPs
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
