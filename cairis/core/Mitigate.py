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


from .Response import Response
from numpy import *
from .AssetParameters import AssetParameters
from .PropertyHolder import PropertyHolder
from . import armid

__author__ = 'Shamal Faily'

class Mitigate(Response,PropertyHolder):
  def __init__(self,respId,respName,respType,mitDesc,mitCost,mitRoles,mitProps,detPt,detMech,mitRisks,mitTargets):
    Response.__init__(self,respId,respName,mitRisks,mitCost,mitRoles)
    PropertyHolder.__init__(self,mitProps)
    self.theDescription = mitDesc
    self.theDetectionPoint = detPt
    self.theDetectionMechanism = detMech
    self.theTargets = mitTargets
    self.theMitigationType = respType

  def description(self): return self.theDescription
  def detectionPoint(self): return self.theDetectionPoint
  def detectionMechanism(self): return self.theDetectionMechanism
  def targets(self): return self.theTargets
  def type(self): return self.theMitigationType
  def effectiveness(self):
    if (self.theSecurityProperties == array((0,0,0,0,0,0,0,0))): return 'None'
    elif (self.theSecurityProperties == array((1,1,1,1,1,1,1,1))): return 'Low'
    elif (self.theSecurityProperties == array((2,2,2,2,2,2,2,2))): return 'Medium'
    elif (self.theSecurityProperties == array((3,3,3,3,3,3,3,3))): return 'High'

  def assetParameters(self,assetId = -1):
    cMitigated = self.theSecurityProperties[armid.C_PROPERTY]
    iMitigated = self.theSecurityProperties[armid.I_PROPERTY]
    avMitigated = self.theSecurityProperties[armid.AV_PROPERTY]
    acMitigated = self.theSecurityProperties[armid.AC_PROPERTY]
    assetProperties = array((cMitigated,iMitigated,avMitigated,acMitigated))
    mitName = self.theName + ' response'
    parameters = AssetParameters(mitName,self.theDescription,'Mitigation',assetProperties)
    parameters.setId(assetId)
    return parameters
