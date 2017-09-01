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

import unittest
import os
import json
from subprocess import call
import cairis.core.BorgFactory
from cairis.core.Borg import Borg
from cairis.core.RoleParameters import RoleParameters
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.core.TemplateGoalParameters import TemplateGoalParameters
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.ComponentParameters import ComponentParameters
from cairis.core.ConnectorParameters import ConnectorParameters
from cairis.core.ComponentViewParameters import ComponentViewParameters

__author__ = 'Shamal Faily'


class ComponentViewTest(unittest.TestCase):

  def setUp(self):
    call([os.environ['CAIRIS_CFG_DIR'] + "/initdb.sh"])
    cairis.core.BorgFactory.initialise()
    f = open(os.environ['CAIRIS_SRC'] + '/test/componentviews.json')
    d = json.load(f)
    f.close()

    self.theRequirements = []
    self.theRoles = []
    self.iRoles = d['roles']
    for i in self.iRoles:
      self.theRoles.append(RoleParameters(i["theName"], i["theType"], i["theShortCode"], i["theDescription"],[]))

    self.theMetricTypes = []
    self.iAccessRights = d['access_rights']
    for i in self.iAccessRights:
      self.theMetricTypes.append(ValueTypeParameters(i["theName"], i["theDescription"], 'access_right','',i["theValue"],i["theRationale"]))

    self.iSurfaceTypes = d['surface_types']
    for i in self.iSurfaceTypes:
      self.theMetricTypes.append(ValueTypeParameters(i["theName"], i["theDescription"], 'surface_type','',i["theValue"],i["theRationale"]))

    self.iProtocols = d['protocols']
    for i in self.iProtocols:
      self.theMetricTypes.append(ValueTypeParameters(i["theName"], i["theDescription"], 'protocol','',i["theValue"],i["theRationale"]))

    self.iPrivileges = d['privileges']
    for i in self.iPrivileges:
      self.theMetricTypes.append(ValueTypeParameters(i["theName"], i["theDescription"], 'privilege','',i["theValue"],i["theRationale"]))

    self.theAssets = []
    spValues = [0,0,0,0,0,0,0,0,]
    srValues = ['None','None','None','None','None','None','None','None']
    self.iTemplateAssets = d['template_assets']
    for i in self.iTemplateAssets:
      self.theAssets.append(TemplateAssetParameters(i["theName"], i["theShortCode"], i["theDescription"], i["theSignificance"],i["theType"],i["theSurfaceType"],i["theAccessRight"],spValues,srValues,[],[]))

    self.theGoals = []
    self.iTemplateGoals = d['template_goals']
    for i in self.iTemplateGoals:
      self.theGoals.append(TemplateGoalParameters(i["theName"],i["theDefinition"],i["theRationale"],i["theConcerns"],i["theResponsibilities"]))

    self.iComponentViews = d['architectural_patterns']
    

  def testComponentView(self):

    cvName = self.iComponentViews[0]["theName"]
    cvSyn = self.iComponentViews[0]["theSynopsis"]
    theComponents = []
    for c in self.iComponentViews[0]["theComponents"]:
      cName = c["theName"]
      cDesc = c["theDescription"]
      cInts = []
      for i in c["theInterfaces"]:
        cInts.append((i["theName"],i["theType"],i["theAccessRight"],i["thePrivilege"]))
      cStructs = []
      for cs in c["theStructure"]:
        cStructs.append((cs["theHeadAsset"],cs["theHeadAdornment"],cs["theHeadNav"],cs["theHeadNry"],cs["theHeadRole"],cs["theTailRole"],cs["theTailNry"],cs["theTailNav"],cs["theTailAdornment"],cs["theTailAsset"]))
      cReqs = []
      cGoals = []
      for i in c["theGoals"]:
        cGoals.append(i)

      cGoalAssocs = []
      for cga in c["theGoalAssociations"]:
        cGoalAssocs.append((cga["theGoalName"],cga["theSubGoalName"],cga["theRefType"],'None'))
      theComponents.append(ComponentParameters(cName,cDesc,cInts,cStructs,cReqs,cGoals,cGoalAssocs))

    theConnectors = []
    for conn in self.iComponentViews[0]["theConnectors"]:
      theConnectors.append(ConnectorParameters(conn["theConnectorName"],cvName,conn["theFromComponent"],conn["theFromRole"],conn["theFromInterface"],conn["theToComponent"],conn["theToInterface"],conn["theToRole"],conn["theAssetName"],conn["theProtocol"],conn["theAccessRight"]))
 
    icvp = ComponentViewParameters(cvName,cvSyn,self.theMetricTypes,self.theRoles,self.theAssets,self.theRequirements,self.theGoals,theComponents,theConnectors)
    b = Borg()
    b.dbProxy.addComponentView(icvp)

    ocvps = b.dbProxy.getComponentViews()
    ocvp = ocvps[cvName]

    self.assertEqual(icvp.name(), ocvp.name())
    self.assertEqual(icvp.synopsis(), ocvp.synopsis())

    self.assertEqual(b.dbProxy.componentAttackSurface('Policy Manager'),3.0)
    cg = b.dbProxy.componentGoalModel('Policy Manager')

    icvp.setId(ocvp.id())
    icvp.theSynopsis = 'revised synopsis'
    b.dbProxy.updateComponentView(icvp)
    ocvps = b.dbProxy.getComponentViews()
    ocvp = ocvps[cvName]

    self.assertEqual(icvp.name(), ocvp.name())
    self.assertEqual(ocvp.synopsis(), 'revised synopsis')


    b.dbProxy.deleteComponentView(ocvp.id())
  
  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
