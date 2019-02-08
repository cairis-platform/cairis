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


from .ARM import *
from .MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from .MisuseCase import MisuseCase
from cairis.tools.PseudoClasses import RiskRating
from .Borg import Borg

__author__ = 'Shamal Faily'

def objectiveText(vulnerableAssets,threatenedAssets):
  objectiveText = 'Exploit vulnerabilities in '
  for idx,vulAsset in enumerate(vulnerableAssets):
    objectiveText += vulAsset
    if (idx != (len(vulnerableAssets) -1)):
      objectiveText += ','
  objectiveText += ' to threaten '
  for idx,thrAsset in enumerate(threatenedAssets):
    objectiveText += thrAsset
    if (idx != (len(threatenedAssets) -1)):
      objectiveText += ','
  objectiveText += '.'
  return objectiveText



def build(threatName,vulnerabilityName,dbProxy = None):
  if (dbProxy == None):
    b = Borg()
    dbProxy = b.dbProxy


  envNames = dbProxy.riskEnvironments(threatName,vulnerabilityName)
  threatId = dbProxy.getDimensionId(threatName,'threat')
  vulId = dbProxy.getDimensionId(vulnerabilityName,'vulnerability')

  envList = []
  for envName in envNames:
    mcEnv = MisuseCaseEnvironmentProperties(envName)

    mcEnv.theRiskRating = RiskRating(threatName,vulnerabilityName,envName,dbProxy.riskRating(-1,threatName,vulnerabilityName,envName))
    envId = dbProxy.getDimensionId(envName,'environment')
    mcEnv.theLikelihood = dbProxy.threatLikelihood(threatId,envId)
    mcEnv.theSeverity = dbProxy.vulnerabilitySeverity(vulId,envId)
    mcEnv.theAttackers = dbProxy.threatAttackers(threatId,envId)

    threatenedAssets = dbProxy.threatenedAssets(threatId,envId)
    vulnerableAssets = dbProxy.vulnerableAssets(vulId,envId)
    mcEnv.theObjective = objectiveText(vulnerableAssets,threatenedAssets)
    mcEnv.theAssets = set(threatenedAssets + vulnerableAssets)
    envList.append(mcEnv) 
  mc = MisuseCase(-1,'',envList,'')
  mc.theThreatName = threatName
  mc.theVulnerabilityName = vulnerabilityName
  return mc
