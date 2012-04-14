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


from SecurityPatternContentHandler import SecurityPatternContentHandler
from TVTypeContentHandler import TVTypeContentHandler
from DomainValueContentHandler import DomainValueContentHandler
from DirectoryContentHandler import DirectoryContentHandler
from RiskAnalysisContentHandler import RiskAnalysisContentHandler
from GoalsContentHandler import GoalsContentHandler
from UsabilityContentHandler import UsabilityContentHandler
from AssociationsContentHandler import AssociationsContentHandler
from CairisContentHandler import CairisContentHandler
from ComponentViewContentHandler import ComponentViewContentHandler
from Borg import Borg
import xml.sax

def importSecurityPatterns(importFile):
  parser = xml.sax.make_parser()
  handler = SecurityPatternContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  taps = handler.assets()
  spps = handler.patterns()
  noOfTaps = len(taps)
  noOfSpps = len(spps)

  b = Borg()

  msgStr = 'No patterns imported'
  if (noOfTaps > 0):
    tapId = 0;
    b.dbProxy.deleteSecurityPattern(-1)
    b.dbProxy.deleteTemplateAsset(-1)
    for tap in taps:
      tap.setId(tapId)
      b.dbProxy.addTemplateAsset(tap)
      tapId += 1

    if (noOfSpps > 0):
      spId = 0;
      b.dbProxy.deleteSecurityPattern(-1)
      for sp in spps:
        sp.setId(spId)
        b.dbProxy.addSecurityPattern(sp)
        spId += 1
      msgStr =  'Imported ' + str(noOfTaps) + ' template assets and ' + str(noOfSpps) + ' security patterns'
  return msgStr

def importTVTypeFile(importFile):
  parser = xml.sax.make_parser()
  handler = TVTypeContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  vulTypes,threatTypes = handler.types()
  return importTVTypes(vulTypes,threatTypes)
 
def importTVTypes(vulTypes,threatTypes):
  b = Borg()
  noOfVts = len(vulTypes)
  noOfTts = len(threatTypes)
  tId = 0
  if (noOfVts > 0):
    b.dbProxy.deleteVulnerabilityType(-1)
    for vt in vulTypes:
      vt.setId(tId)
      b.dbProxy.addValueType(vt)
      tId += 1
  tId = 0
  if (noOfTts > 0):
    b.dbProxy.deleteThreatType(-1)
    for tt in threatTypes:
      tt.setId(tId)
      b.dbProxy.addValueType(tt)
      tId += 1
  msgStr = 'Imported ' + str(noOfVts) + ' vulnerability types and ' + str(noOfTts) + ' threat types.'
  return msgStr

def importDirectoryFile(importFile):
  parser = xml.sax.make_parser()
  handler = DirectoryContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  vulDir,threatDir = handler.directories()
  vdSize = len(vulDir)
  tdSize = len(threatDir)
  tId = 0
  b = Borg()
  if (vdSize > 0):
    b.dbProxy.addVulnerabilityDirectory(vulDir)
  if (tdSize > 0):
    b.dbProxy.addThreatDirectory(threatDir)
  msgStr = 'Imported ' + str(vdSize) + ' template vulnerabilities and ' + str(tdSize) + ' template threats.'
  return msgStr


def importRequirementsFile(importFile):
  parser = xml.sax.make_parser()
  handler = GoalsContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  return importRequirements(handler.domainProperties(),handler.goals(),handler.obstacles(),handler.requirements(),handler.countermeasures())

def importRequirements(dpParameterSet,goalParameterSet,obsParameterSet,reqParameterSet,cmParameterSet):
  b = Borg()
  dpCount = 0
  for dpParameters in dpParameterSet:
    b.dbProxy.addDomainProperty(dpParameters)
    dpCount += 1
  goalCount = 0
  for goalParameters in goalParameterSet:
    b.dbProxy.addGoal(goalParameters)
    goalCount += 1
  obsCount = 0
  for obsParameters in obsParameterSet:
    b.dbProxy.addObstacle(obsParameters)
    obsCount += 1
  reqCount = 0
  for req,refName,refType in reqParameterSet:
    isAsset = True
    if (refType == 'environment'):
      isAsset = False
    b.dbProxy.addRequirement(req,refName,isAsset)
    reqCount += 1
  cmCount = 0
  for cmParameters in cmParameterSet:
    b.dbProxy.addCountermeasure(cmParameters)
    cmCount += 1
  msgStr = 'Imported ' + str(dpCount) + ' domain properties, ' + str(goalCount) + ' goals, ' + str(obsCount) + ' obstacles, ' + str(reqCount) + ' requirements, and ' + str(cmCount) + ' countermeasures.'
  return msgStr

def importRiskAnalysisFile(importFile):
  parser = xml.sax.make_parser()
  handler = RiskAnalysisContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  return importRiskAnalysis(handler.roles(),handler.assets(),handler.vulnerabilities(),handler.attackers(),handler.threats(),handler.risks(),handler.responses(),handler.associations())

def importRiskAnalysis(roleParameterSet,assetParameterSet,vulParameterSet,attackerParameterSet,threatParameterSet,riskParameterSet,responseParameterSet,assocParameterSet):

  b = Borg()
  roleCount = 0
  for roleParameters in roleParameterSet:
    b.dbProxy.addRole(roleParameters)
    roleCount += 1

  assetCount = 0
  for assetParameters in assetParameterSet:
    b.dbProxy.addAsset(assetParameters)
    assetCount += 1

  vulCount = 0
  for vulParameters in vulParameterSet:
    b.dbProxy.addVulnerability(vulParameters)
    vulCount += 1

  attackerCount = 0
  for attackerParameters in attackerParameterSet:
    b.dbProxy.addAttacker(attackerParameters)
    attackerCount += 1

  threatCount = 0
  for threatParameters in threatParameterSet:
    b.dbProxy.addThreat(threatParameters)
    threatCount += 1

  riskCount = 0
  for riskParameters in riskParameterSet:
    b.dbProxy.addRisk(riskParameters)
    riskCount += 1

  responseCount = 0
  for responseParameters in responseParameterSet:
    b.dbProxy.addResponse(responseParameters)
    responseCount += 1

  rshipCount = 0
  for assocParameters in assocParameterSet:
    b.dbProxy.addClassAssociation(assocParameters)
    rshipCount += 1

  msgStr = 'Imported ' + str(roleCount) + ' roles, ' + str(assetCount) + ' assets, ' + str(vulCount) + ' vulnerabilities, ' + str(attackerCount) + ' attackers, ' + str(threatCount) + ' threats, ' + str(riskCount) + ' risks, ' + str(responseCount) + ' responses, and ' + str(rshipCount) + ' asset associations.'
  return msgStr

def importUsabilityFile(importFile):
  parser = xml.sax.make_parser()
  handler = UsabilityContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  return importUsability(handler.personas(),handler.externalDocuments(),handler.documentReferences(),handler.conceptReferences(),handler.personaCharacteristics(),handler.taskCharacteristics(),handler.tasks(),handler.usecases())


def importUsability(personaParameterSet,edParameterSet,drParameterSet,crParameterSet,pcParameterSet,tcParameterSet,taskParameterSet,ucParameterSet):
  b = Borg()

  personaCount = 0
  for personaParameters in personaParameterSet:
    b.dbProxy.addPersona(personaParameters)
    personaCount += 1
  edCount = 0
  for edParameters in edParameterSet:
    b.dbProxy.addExternalDocument(edParameters)
    edCount += 1
  drCount = 0
  for drParameters in drParameterSet:
    b.dbProxy.addDocumentReference(drParameters)
    drCount += 1
  taskCount = 0
  for taskParameters in taskParameterSet:
    b.dbProxy.addTask(taskParameters)
    taskCount += 1
  ucCount = 0
  for ucParameters in ucParameterSet:
    b.dbProxy.addUseCase(ucParameters)
    ucCount += 1
  crCount = 0
  for crParameters in crParameterSet:
    b.dbProxy.addConceptReference(crParameters)
    crCount += 1
  pcCount = 0
  for pcParameters in pcParameterSet:
    b.dbProxy.addPersonaCharacteristic(pcParameters)
    pcCount += 1
  tcCount = 0
  for tcParameters in tcParameterSet:
    b.dbProxy.addTaskCharacteristic(tcParameters)
    tcCount += 1
  msgStr = 'Imported ' + str(personaCount) + ' personas, ' + str(edCount) + ' external documents, ' + str(drCount) + ' document references, ' + str(crCount) + ' concept references, ' + str(pcCount) + ' persona characteristics, ' + str(tcCount) + ' task characteristics, ' + str(taskCount) + ' tasks, and ' + str(ucCount) + ' use cases.'
  return msgStr

def importAssociationsFile(importFile):
  parser = xml.sax.make_parser()
  handler = AssociationsContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  return importAssociations(handler.manualAssociations(),handler.goalAssociations(),handler.dependencyAssociations())
  
def importAssociations(maParameterSet,gaParameterSet,depParameterSet):
  b = Borg()
  maCount = 0
  for tTable,fromId,toId,refType in maParameterSet:
    b.dbProxy.addTrace(tTable,fromId,toId,refType)
    maCount += 1
  gaCount = 0
  for gaParameters in gaParameterSet:
    b.dbProxy.addGoalAssociation(gaParameters)
    gaCount += 1
  depCount = 0
  for depParameters in depParameterSet:
    b.dbProxy.addDependency(depParameters)
    depCount += 1
  msgStr = 'Imported ' + str(maCount) + ' manual associations, ' + str(gaCount) + ' goal associations, and ' + str(depCount) + ' dependency associations.'
  return msgStr

def importProjectFile(importFile):
  parser = xml.sax.make_parser()
  handler = CairisContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  pSettings = handler.settings()
  envParameterSet = handler.environments()
  return importProjectData(pSettings,envParameterSet)

def importProjectData(pSettings,envParameterSet):
  b = Borg()
  if (pSettings != None):
    b.dbProxy.updateSettings(pSettings[0],pSettings[1],pSettings[2],pSettings[3],pSettings[4],pSettings[5],pSettings[6],pSettings[7])
  envCount = 0
  for envParameters in envParameterSet:
    b.dbProxy.addEnvironment(envParameters)
    envCount += 1
  msgText = 'Imported ' + str(envCount) + ' environments'
  if (pSettings != None):
    msgText += ', and project settings'
    msgText += '.'
  return msgText

def importComponentViewFile(importFile):
  parser = xml.sax.make_parser()
  handler = ComponentViewContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  view = handler.view()
  return importComponentViewData(view)

def importComponentViewData(view):
  b = Borg()
  b.dbProxy.addComponentView(view)
  msgStr = 'Imported component view'
  return msgStr

def importDomainValuesFile(importFile):
  parser = xml.sax.make_parser()
  handler = DomainValueContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  tvValues,rvValues,cvValues,svValues,lvValues = handler.values()
  return importDomainValues(tvValues,rvValues,cvValues,svValues,lvValues)

def importDomainValues(tvValues,rvValues,cvValues,svValues,lvValues):
  noOfTvs = len(tvValues)
  noOfRvs = len(rvValues)
  noOfCvs = len(cvValues)
  noOfSvs = len(svValues)
  noOfLvs = len(lvValues)
 
  b = Borg()

  tId = 0
  if (noOfTvs > 0):
    for tvp in tvValues:
      tvp.setId(tId)
      b.dbProxy.updateValueType(tvp)
      tId += 1
  tId =1
  if (noOfRvs > 0):
    for rvp in rvValues:
      rvp.setId(tId)
      b.dbProxy.updateValueType(rvp)
      tId += 1
  tId = 0
  if (noOfCvs > 0):
    for cvp in cvValues:
      cvp.setId(tId)
      b.dbProxy.updateValueType(cvp)
      tId += 1
  tId = 0
  if (noOfSvs > 0):
    for svp in svValues:
      svp.setId(tId)
      b.dbProxy.updateValueType(svp)
      tId += 1
  tId = 0
  if (noOfLvs > 0):
    for lvp in lvValues:
      lvp.setId(tId)
      b.dbProxy.updateValueType(lvp)
      tId += 1
  msgStr = 'Imported domain values'
  return msgStr


def importModelFile(importFile):
  b = Borg()
  b.dbProxy.clearDatabase()
  modelTxt = importTVTypeFile(importFile) + '  '
  modelTxt += importDomainValuesFile(importFile) + ' '
  modelTxt += importProjectFile(importFile) + ' '
  modelTxt += importRiskAnalysisFile(importFile) + ' '
  modelTxt += importUsabilityFile(importFile) + ' '
  modelTxt += importRequirementsFile(importFile) + ' '
  modelTxt += importAssociationsFile(importFile)
  return modelTxt
