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


from xml.sax.handler import ContentHandler,EntityResolver
from cairis.core.AssetParameters import AssetParameters
import cairis.core.AssetParametersFactory
from cairis.core.AttackerParameters import AttackerParameters
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.core.VulnerabilityParameters import VulnerabilityParameters
from cairis.core.VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from cairis.core.ThreatParameters import ThreatParameters
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.MisuseCase import MisuseCase
from cairis.core.RiskParameters import RiskParameters
from cairis.core.TemplateObstacleParameters import TemplateObstacleParameters
from cairis.core.ObstacleParameters import ObstacleParameters
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.GoalAssociationParameters import GoalAssociationParameters
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

def a2i(spLabel):
  if spLabel == 'Low':
    return 1
  elif spLabel == 'Medium':
    return 2
  elif spLabel == 'High':
    return 3
  else:
    return 0

def it2Id(itLabel):
  if itLabel == 'required':
    return 1
  else:
    return 0

class AttackPatternContentHandler(ContentHandler,EntityResolver):
  def __init__(self,session_id = None):
    self.thePatternName = ''
    self.theLikelihood = ''
    self.theSeverity = ''
    self.theObstacles = []
    self.theObstacleAssociations = []
    self.inIntent = 0
    self.theIntent = ''
    self.theMotivations = []
    self.theEnvironment = ''
    self.theAttack = ''
    self.theExploit = ''
    self.theAttackObstacle = ''
    self.theExploitObstacle = ''
    self.theParticipants = []
    self.theTargets = []
    self.theExploits = []
    self.inConsequences = 0
    self.theConsequences = ''
    self.inImplementation = 0
    self.theImplementation = ''
    self.inKnownUses = 0
    self.theKnownUses = ''
    self.inRelatedPatterns = 0
    self.theRelatedPatterns = ''
    b = Borg()
    self.configDir = b.configDir
    self.dbProxy = b.get_dbproxy(session_id)

    self.theObstacleParameters = []
    self.theObstacleAssociationParameters = []
    self.theAssetParameters = []
    self.theAttackerParameters = []
    self.theVulnerabilityParameters = None
    self.theThreatParameters = None
    self.theRiskParameters = None

    self.resetObstacleElements()
    self.resetObstacleAssociationElements()
    self.resetMotivationElements()
    self.resetParticipantElements()

  def obstacles(self): return self.theObstacleParameters
  def obstacleAssociations(self): return self.theObstacleAssociationParameters
  def assets(self): return self.theAssetParameters
  def attackers(self): return self.theAttackerParameters
  def vulnerability(self): return self.theVulnerabilityParameters
  def threat(self): return self.theThreatParameters
  def risk(self): return self.theRiskParameters

  def resetObstacleElements(self):
    self.theObstacleName = ''
    self.theObstacleCategory = ''
    self.inDefinition = 0
    self.theDefinition = ''
    self.theConcerns = []
    self.theResponsibilities = []
    self.resetProbabilityElements()

  def resetProbabilityElements(self):
    self.theProbability = 0.0
    self.inRationale = 0
    self.theRationale = ''

  def resetObstacleAssociationElements(self):
    self.theObstacleName = ''
    self.theRefType = ''
    self.theSubObstacleName = ''
    self.inRationale = 0
    self.theRationale = ''

  def resetMotivationElements(self):
    self.theGoal = ''
    self.theValue = 'None'
    self.inDescription = 0
    self.theDescription = ''

  def resetParticipantElements(self):
    self.theParticipant = ''
    self.theMotives = []
    self.theResponsibilities = []
     
  def resolveEntity(self,publicId,systemId):
    return systemId

  def startElement(self,name,attrs):
    if (name == 'attack_pattern'):
      self.thePatternName = attrs['name']
      self.theLikelihood = attrs['likelihood']
      self.theSeverity = attrs['severity']
    elif (name == 'obstacle'):
      self.theObstacleName = attrs['name']
      self.theObstacleCategory = attrs['category'].replace('_',' ')
    elif (name == 'probability'):
      self.theProbability = attrs['value']
    elif (name == 'obstacle_association'):
      self.theObstacleName = attrs['obstacle_name']
      self.theSubObstacleName = attrs['subobstacle_name']
      self.theRefType = attrs['ref_type']
    elif (name == 'definition'):
      self.inDefinition = 1
      self.theDefinition = ''
    elif (name == 'rationale'):
      self.inRationale = 1
      self.theRationale = ''
    elif (name == 'intent'):
      self.inIntent = 1
      self.theIntent = ''
    elif (name == 'motivation'):
      self.theGoal = attrs['goal']
      self.theValue = attrs['value']
    elif (name == 'description'):
      self.inDescription = 1
      self.theDescription = ''
      if self.inImplementation:
        self.theImplementation = ''
    elif (name == 'applicability'):
      self.theEnvironment = attrs['environment']
    elif (name == 'structure'):
      self.theAttack = attrs['attack']
      self.theExploit = attrs['exploit']
      try:
        self.theAttackObstacle = attrs['attack_obstacle']
      except KeyError:
        self.theAttackObstacle = '' 

      try:
        self.theExploitObstacle = attrs['exploit_obstacle']
      except KeyError:
        self.theExploitObstacle = '' 

    elif (name == 'participant'):
      self.theParticipant = attrs['name']
    elif (name == 'motive'):
      self.theMotives.append(attrs['name'])
    elif (name == 'capability'):
      self.theResponsibilities.append((attrs['name'],attrs['value']))
    elif (name == 'target'):
      self.theTargets.append(attrs['name'])
    elif (name == 'exploit'):
      self.theExploits.append(attrs['name'])
    elif (name == 'consequences'):
      self.inConsequences = 1
      self.theConsequences = ''
    elif name == 'implementation':
      self.inImplementation = 1
      self.theImplementation = ''
    elif name == 'known_uses':
      self.inKnownUses = 1
      self.theKnownUses = ''
    elif name == 'related_patterns':
      self.inRelatedPatterns = 1
      self.theRelatedPatterns = ''
    elif name == 'concern':
      self.theConcerns.append(attrs['name'])
    elif name == 'responsibility':
      self.theResponsibilities.append(attrs['name'])

  def characters(self,data):
    if self.inDefinition:
      self.theDefinition += data
    elif self.inRationale:
      self.theRationale += data
    elif self.inIntent:
      self.theIntent += data
    elif self.inDescription and self.inImplementation:
      self.theImplementation += data
    elif self.inDescription:
      self.theDescription += data
    elif self.inConsequences:
      self.theConsequences += data
    elif self.inImplementation:
      self.theImplementation += data
    elif self.inKnownUses:
      self.theKnownUses += data
    elif self.inRelatedPatterns:
      self.theRelatedPatterns += data


  def endElement(self,name):
    if name == 'intent':
      self.inIntent = 0
    elif name == 'definition':
      self.inDefinition = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'motivation':
      self.theMotivations.append((self.theGoal,self.theValue,self.theDescription))
      self.resetMotivationElements()
    elif name == 'participant':
      self.theParticipants.append((self.theParticipant,self.theMotives,self.theResponsibilities))
      self.resetParticipantElements()
    elif name == 'description':
      self.inDescription = 0
      if self.inImplementation:
        self.inImplementation = 0
    elif name == 'consequences':
      self.inConsequences = 0
    elif name == 'implementation':
      self.inImplementation = 0
    elif name == 'known_uses':
      self.inKnownUses = 0
    elif name == 'related_patterns':
      self.inRelatedPatterns = 0
    elif name == 'obstacle':

      self.theObstacles.append( TemplateObstacleParameters(self.theObstacleName,self.theObstacleCategory,self.theDefinition,self.theConcerns,self.theResponsibilities,self.theProbability,self.theRationale))
      self.resetObstacleElements()
    elif name == 'obstacle_association':
      self.theObstacleAssociations.append((self.theObstacleName,self.theRefType,self.theSubObstacleName,self.theRationale))
      self.resetObstacleAssociationElements()
    elif name == 'attack_pattern':
      assetList = self.theTargets + self.theExploits
      for assetName in assetList:
        assetId = self.dbProxy.existingObject(assetName,'asset')
        if assetId == -1:
          taId = self.dbProxy.existingObject(assetName,'template_asset')
          if taId == -1:
           raise ARMException('Cannot import attack pattern: no asset or template asset for ' + assetName)
          else:
            self.theAssetParameters.append(cairis.core.AssetParametersFactory.buildFromTemplate(assetName,[self.theEnvironment]))

      attackerNames = []
      for attackerName,attackerMotives,attackerCapabilities in self.theParticipants:
        if (self.dbProxy.existingObject(attackerName,'attacker') == -1):
          attackerRoles = self.dbProxy.dimensionRoles(self.dbProxy.getDimensionId(attackerName,'persona'),self.dbProxy.getDimensionId(self.theEnvironment,'environment'),'persona')
          ep = AttackerEnvironmentProperties(self.theEnvironment,attackerRoles,attackerMotives,attackerCapabilities)
          p = AttackerParameters(attackerName,'','',[],[ep])
          p.isPersona = True
          self.theAttackerParameters.append(p) 
        attackerNames.append(attackerName)
  
      for tObs in self.theObstacles:
        sgRefs = []
        for resp in tObs.responsibilities():
          sgRefs.append((resp,'role','responsible',0,'None')) 
        ep = ObstacleEnvironmentProperties(self.theEnvironment,'',tObs.definition(),tObs.category(),[],sgRefs,tObs.concerns())
        ep.theProbability = tObs.probability()
        ep.theProbabilityRationale = tObs.probabilityRationale()
        self.theObstacleParameters.append(ObstacleParameters(tObs.name(),self.thePatternName,[],[ep]))

      for obsAssoc in self.theObstacleAssociations:
        obsName = obsAssoc[0]
        refType = obsAssoc[1]
        subObsName = obsAssoc[2]
        assocRationale = obsAssoc[3]  
        self.theObstacleAssociationParameters.append(GoalAssociationParameters(self.theEnvironment,obsName,'obstacle',refType,subObsName,'obstacle',0,assocRationale))
 
      vp = VulnerabilityEnvironmentProperties(self.theEnvironment,self.theSeverity,self.theExploits)
      vulRows = self.dbProxy.getVulnerabilityDirectory(self.theExploit)
      if (len(vulRows) == 0):
        vulData = ['','',self.theExploit,self.dbProxy.defaultValue('vulnerability_type')]
      else:
        vulData = vulRows[0]
      self.theVulnerabilityParameters = VulnerabilityParameters(self.theExploit,vulData[2],vulData[3],[],[vp])

      spDict = {}
      spDict['confidentiality'] = (0,'None')
      spDict['integrity'] = (0,'None')
      spDict['availability'] = (0,'None')
      spDict['accountability'] = (0,'None')
      spDict['anonymity'] = (0,'None')
      spDict['pseudonymity'] = (0,'None')
      spDict['unlinkability'] = (0,'None')
      spDict['unobservability'] = (0,'None')

      for thrMotivation in self.theMotivations:
        spName = thrMotivation[0]
        spValue = thrMotivation[1]
        spRationale = thrMotivation[2]
        spDict[spName] = (a2i(spValue),spRationale)
      
      cProperty,cRationale = spDict['confidentiality']
      iProperty,iRationale = spDict['integrity']
      avProperty,avRationale = spDict['availability']
      acProperty,acRationale = spDict['accountability']
      anProperty,anRationale = spDict['anonymity']
      panProperty,panRationale = spDict['pseudonymity']
      unlProperty,unlRationale = spDict['unlinkability']
      unoProperty,unoRationale = spDict['unobservability']

      tp = ThreatEnvironmentProperties(self.theEnvironment,self.theLikelihood,self.theTargets,attackerNames,[cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty],[cRationale,iRationale,avRationale,acRationale,anRationale,panRationale,unlRationale,unoRationale])
      thrRows = self.dbProxy.getThreatDirectory(self.theAttack)

      if (len(thrRows) == 0):
        thrData = ['','',self.theExploit,self.dbProxy.defaultValue('threat_type')]
      else:
        thrData = thrRows[0]
      self.theThreatParameters = ThreatParameters(self.theAttack,thrData[3],thrData[2],[],[tp])

      if (self.theAttackObstacle != ''):
        self.theObstacleAssociationParameters.append(GoalAssociationParameters(self.theEnvironment,self.theAttackObstacle,'obstacle','or',self.theAttack,'threat',0,'None'))
      if (self.theExploitObstacle != ''):
        self.theObstacleAssociationParameters.append(GoalAssociationParameters(self.theEnvironment,self.theExploitObstacle,'obstacle','or',self.theExploit,'vulnerability',0,'None'))
      rep = MisuseCaseEnvironmentProperties(self.theEnvironment,self.theImplementation )
      mc = MisuseCase(-1,'Exploit ' + self.thePatternName,[rep],self.thePatternName)
      self.theRiskParameters = RiskParameters(self.thePatternName,self.theAttack,self.theExploit,mc,[],self.theIntent)
