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


from cairis.core.Borg import Borg
from cairis.core.ARM import *
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from cairis.core.TaskEnvironmentProperties import TaskEnvironmentProperties
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.GoalParameters import GoalParameters
import cairis.core.ObjectFactory

__author__ = 'Shamal Faily'

class GUIDatabaseProxy(MySQLDatabaseProxy):
  def __init__(self, host=None, port=None, user=None, passwd=None, db=None):
    MySQLDatabaseProxy.__init__(self,host,port,user,passwd,db)

  def associateGrid(self,gridObjt): self.theGrid = gridObjt

  def riskEnvironmentNames(self,riskName):
    return self.responseList('call riskEnvironmentNames(:risk)',{'risk':riskName},'MySQL error getting environments associated with risk ' + riskName)

  def threatVulnerabilityEnvironmentNames(self,threatName,vulName):
    return self.responseList('call threatVulnerabilityEnvironmentNames(:threat,:vuln)',{'threat':threatName,'vuln':vulName},'MySQL error getting environments associated with threat ' + threatName + ' and vulnerability ' + vulName);

  def threatTypes(self,envName = ''):
    rows = self.responseList('call threatTypes(:env)',{'env':envName},'MySQL error getting threat types')
    stats = {}
    for key,value in rows:
      stats[row[0]] = row[1]
    return stats

  def inheritedAssetProperties(self,assetId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    syProperties,pRationale = self.relatedProperties('asset',assetId,environmentId)
    assetAssociations = self.assetAssociations(assetId,environmentId)
    return AssetEnvironmentProperties(environmentName,syProperties,pRationale,assetAssociations)

  def inheritedAttackerProperties(self,attackerId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    roles = self.dimensionRoles(attackerId,environmentId,'attacker')
    capabilities = self.attackerCapabilities(attackerId,environmentId)
    motives = self.attackerMotives(attackerId,environmentId)
    return AttackerEnvironmentProperties(environmentName,roles,motives,capabilities)

  def inheritedThreatProperties(self,threatId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    likelihood = self.threatLikelihood(threatId,environmentId)
    assets = self.threatenedAssets(threatId,environmentId) 
    attackers = self.threatAttackers(threatId,environmentId)
    syProperties,pRationale = self.relatedProperties('threat',threatId,environmentId)
    return ThreatEnvironmentProperties(environmentName,likelihood,assets,attackers,syProperties,pRationale)

  def inheritedVulnerabilityProperties(self,vulId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    severity = self.vulnerabilitySeverity(vulId,environmentId)
    assets = self.vulnerableAssets(vulId,environmentId)
    return VulnerabilityEnvironmentProperties(environmentName,severity,assets)

  def inheritedTaskProperties(self,taskId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    dependencies = self.taskDependencies(taskId,environmentId)
    personas = self.taskPersonas(taskId,environmentId)
    assets = self.taskAssets(taskId,environmentId)
    concs = self.taskConcernAssociations(taskId,environmentId)
    narrative = self.taskNarrative(taskId,environmentId)
    return TaskEnvironmentProperties(environmentName,dependencies,personas,assets,concs,narrative)

  def inheritedUseCaseProperties(self,ucId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    preConds,postConds = self.useCaseConditions(ucId,environmentId)
    ucSteps = self.useCaseSteps(ucId,environmentId)
    return UseCaseEnvironmentProperties(environmentName,preConds,ucSteps,postConds)

  def inheritedGoalProperties(self,goalId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    goalDef = self.goalDefinition(goalId,environmentId)
    goalType = self.goalCategory(goalId,environmentId)
    goalPriority = self.goalPriority(goalId,environmentId)
    goalFitCriterion = self.goalFitCriterion(goalId,environmentId)
    goalIssue = self.goalIssue(goalId,environmentId) 
    concs = self.goalConcerns(goalId,environmentId)
    cas = self.goalConcernAssociations(goalId,environmentId)
    goalRefinements,subGoalRefinements = self.goalRefinements(goalId,environmentId)
    return GoalEnvironmentProperties(environmentName,'',goalDef,goalType,goalPriority,goalFitCriterion,goalIssue,goalRefinements,subGoalRefinements,concs,cas)

  def inheritedObstacleProperties(self,obsId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    obsDef = self.obstacleDefinition(obsId,environmentId)
    obsType = self.obstacleCategory(obsId,environmentId)
    goalRefinements,subGoalRefinements = self.goalRefinements(obsId,environmentId)
    return ObstacleEnvironmentProperties(environmentName,'',obsDef,obsType,goalRefinements,subGoalRefinements)

  def reassociateAsset(self,assetName,envName,reqId):
    self.updateDatabase('call reassociateAsset(:ass,:env,:req)',{'ass':assetName,'env':envName,'req':reqId},'MySQL error reassociating asset')

  def getEnvironmentGoals(self,goalName,envName):
    goalRows = self.responseList('call getEnvironmentGoals(:goal,:env)',{'goal':goalName,'env':envName},'MySQL error getting goals')
    oals = []
    for goalId,goalName,goalOrig in goalRows:
      environmentProperties = self.goalEnvironmentProperties(goalId)
      parameters = GoalParameters(goalName,goalOrig,[],self.goalEnvironmentProperties(goalId))
      goal = cairis.core.ObjectFactory.build(goalId,parameters)
      goals.append(goal)
    return goals

  def updateEnvironmentGoal(self,g,envName):
    envProps = g.environmentProperty(envName)
    goalDef = envProps.definition()
    goalCat = envProps.category()
    goalPri = envProps.priority()
    goalFc = envProps.fitCriterion()
    goalIssue = envProps.issue()
    
    self.updateDatabase('call updateEnvironmentGoal(:id,:env,:name,:orig,:def,:cat,:pri,:fc,:issue)',{'id':g.id(),'env':envName,'name':g.name(),'orig':g.originator(),'def':goalDef,'cat':goalCat,'pri':goalPri,'fc':goalFc,'issue':goalIssue},'MySQL error updating environment goal')

  def getTaskSpecificCharacteristics(self,tName):
    rows = self.responseList('call taskSpecificCharacteristics(:task)',{'task':tName},'MySQL error getting task specific characteristics')
    tChars = {}
    tcSumm = []
    for tcId,qualName,tcDesc in rows:
      tcSumm.append((tcId,tName,qualName,tcDesc))
    for tcId,tName,qualName,tcDesc in tcSumm:
      grounds,warrant,backing,rebuttal = self.characteristicReferences(tcId,'taskCharacteristicReferences')
      parameters = TaskCharacteristicParameters(tName,qualName,tcDesc,grounds,warrant,backing,rebuttal)
      tChar = cairis.core.ObjectFactory.build(tcId,parameters)
      tChars[tName + '/' + tcDesc] = tChar
    return tChars

  def getImpliedProcesses(self,constraintId = -1):
    ipRows = self.responseList('call getImpliedProcesses(:const)',{'const':constraintId},'MySQL error getting implied processes')
    ips = {}
    for ipId,ipName,ipDesc,pName,ipSpec in ipRows:
      ipNet = self.impliedProcessNetwork(ipName)
      chs = self.impliedProcessChannels(ipName)
      parameters = ImpliedProcessParameters(ipName,ipDesc,pName,ipNet,ipSpec,chs)
      ip = ObjectFactory.build(ipId,parameters)
      ips[ipName] = ip
    return ips

  def updateImpliedProcess(self,parameters):
    ipId = parameters.id()
    ipName = parameters.name()
    ipDesc = parameters.description()
    pName = parameters.persona()
    cNet = parameters.network()
    ipSpec = parameters.specification()
    chs = parameters.channels()
    session = self.updateDatabase('call deleteImpliedProcessComponents(:id)',{'id':ipId},'MySQL error deleting implied process components',None,False)
    self.updateDatabase('call updateImpliedProcess(:id,:name,:desc,:proc,:spec)',{'id':ipId,'name':ipName,'desc':ipDesc.encode('utf-8'),'proc':pName,'spec':ipSpec.encode('utf-8')},'MySQL error updating implied process',session)
    self.addImpliedProcessNetwork(ipId,pName,cNet)
    self.addImpliedProcessChannels(ipId,chs)

  def getSubGoalNames(self,goalName,envName):
    rows = ['']
    rows += self.responseList('call subGoalNames(:goal,:env)',{'goal':goalName,'env':envName},'MySQL error getting sub goal names')
    return rows

  def getSubObstacleNames(self,obsName,envName):
    rows = ['']
    rows += self.responseList('call subObstacleNames(:obs,:env)',{'obs':obsName,'env':envName},'MySQL error getting sub obstacle names')
    return rows

  def goalEnvironments(self,goalName):
    rows = ['']
    rows += self.responseList('call goalEnvironments(:goal)',{'goal':goalName},'MySQL error getting goal environments')
    return rows

  def obstacleEnvironments(self,obsName):
    rows = ['']
    rows += self.responseList('call obstacleEnvironments(:obs)',{'obs':obsName},'MySQL error getting obstacle environments')
    return rows

  def getEnvironmentObstacles(self,obsName,envName):
    obsRows = self.responseList('call getEnvironmentObstacles(:obs,:env)',{'obs':obsName,'env':envName},'MySQL error getting obstacles')
    obs = []
    for obsId,obsName,obsOrig in obsRows:
      environmentProperties = self.obstacleEnvironmentProperties(obsId)
      parameters = ObstacleParameters(obsName,obsOrig,self.obstacleEnvironmentProperties(obsId))
      obstacle = ObjectFactory.build(obsId,parameters)
      obs.append(obstacle)
    return obs

  def updateEnvironmentObstacle(self,o,envName):
    envProps = o.environmentProperty(envName)
    obsDef = envProps.definition()
    obsCat = envProps.category()
    self.updateDatabase('call updateEnvironmentObstacle(:id,:env,:name,:orig,:def,:cat)',{'id':o.id(),'env':envName,'name':o.name(),'orig':o.originator(),'def':obsDef,'cat':obsCat},'MySQL error updating environment obstacle')

  def impliedProcessChannels(self,procName):
    return self.responseList('call impliedProcessChannels(:proc)',{'proc':procName},'MySQL error getting implied process channels')

  def artifactText(self,artType,artName):
    if artType == 'internal_document':
      return self.responseList('call artifactText(:type,:name)',{'type':artType,'name':artName},'MySQL error getting artifact text')[0]
    else: 
      return ''

  def impliedCharacteristicElements(self,pName,fromCode,toCode,rtName,isLhs):
    return self.responseList('call impliedCharacteristicElements(:pName,:fCode,:tCode,:rt,:lhs)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName,'lhs':isLhs},'MySQL error getting implied characteristic elements')

  def initialiseImpliedCharacteristic(self,pName,fromCode,toCode,rtName):
    self.updateDatabase('call initialiseImpliedCharacteristic(pName,fCode,tCode,rt)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName},'MySQL error initialising implied characteristic')

  def exposedCountermeasures(self,parameters):
    objtId = parameters.id()
    expCMs = []
    for cProperties in parameters.environmentProperties():
      envName = cProperties.name()
      expAssets = cProperties.assets()
      for expAsset in expAssets:
        expCMs += self.exposedCountermeasure(envName,expAsset)
    return expCMs

  def exposedCountermeasure(self,envName,assetName):
    rows = self.responseList('call exposedCountermeasure(:env,:ass)',{'env':envName,'ass':assetName},'MySQL error checking countermeasures exposed by ' + assetName)
    expCMs = []
    for r1, r2 in rows:
      expCMs.append((envName,r1,assetName,r2))
    return expCMs

  def getExternalDocumentReferences(self,docName = ''):
    drRows = self.responseList('call getDocumentReferencesByExternalDocument(:doc)',{'doc':docName},'MySQL error getting document references for external document ' + docName)
    dRefs = {}
    for refId,refName,docName,cName,excerpt in drRows:
      parameters = DocumentReferenceParameters(refName,docName,cName,excerpt)
      dRef = ObjectFactory.build(refId,parameters)
      dRefs[refName] = dRef
    return dRefs

  def getPersonaBehaviouralCharacteristics(self,pName,bvName):
    rows = self.responseList('call personaBehaviouralCharacteristics(:pName,:bvName)',{'pName':pName,'bvName':bvName},'MySQL error getting persona behavioural characteristics')
    pChars = {}
    pcSumm = []
    for pcId, qualName, pcDesc in rows:
      pcSumm.append((pcId,pName,bvName,qualName,pcDesc))
    for pcId,pName,bvName,qualName,pcDesc in pcSumm:
      grounds,warrant,backing,rebuttal = self.characteristicReferences(pcId,'characteristicReferences')
      parameters = PersonaCharacteristicParameters(pName,qualName,bvName,pcDesc,grounds,warrant,backing,rebuttal)
      pChar = ObjectFactory.build(pcId,parameters)
      pChars[pName + '/' + bvName + '/' + pcDesc] = pChar
    return pChars

  def personaImpactRationale(self,cvName,personaName,envName):
    rows = self.responseList('call personaImpactRationale(:cv,:pers,:env)',{'cv':cvName,'pers':personaName,'env':envName},'MySQL error getting persona impact rationale')
    piRationale = {}
    for taskName, durLabel, freqLabel, pdLabel, gcLabel in rows:
      piRationale[taskName] = [durLabel,freqLabel,pdLabel,gcLabel]
    for taskName in piRationale:
      ucDict = {}
      taskUseCases = self.taskUseCases(taskName)
      for ucName in taskUseCases:
        ucComs = self.usecaseComponents(ucName) 
        ucDict[ucName] = []
        for componentName in ucComs:
          ucDict[ucName].append(componentName)
      piRationale[taskName].append(ucDict) 
    return piRationale
