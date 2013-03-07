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
from AttackPatternContentHandler import AttackPatternContentHandler
from TVTypeContentHandler import TVTypeContentHandler
from DomainValueContentHandler import DomainValueContentHandler
from DirectoryContentHandler import DirectoryContentHandler
from RiskAnalysisContentHandler import RiskAnalysisContentHandler
from GoalsContentHandler import GoalsContentHandler
from UsabilityContentHandler import UsabilityContentHandler
from AssociationsContentHandler import AssociationsContentHandler
from CairisContentHandler import CairisContentHandler
from ArchitecturalPatternContentHandler import ArchitecturalPatternContentHandler
from SynopsesContentHandler import SynopsesContentHandler
from TemplateAssetsContentHandler import TemplateAssetsContentHandler
from ProcessesContentHandler import ProcessesContentHandler
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

def importAttackPattern(importFile):
  parser = xml.sax.make_parser()
  handler = AttackPatternContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)

  assets = handler.assets()
  attackers = handler.attackers()
  vulnerability = handler.vulnerability()
  threat = handler.threat()
  risk = handler.risk()

  raTxt = importRiskAnalysis([],assets,[vulnerability],attackers,[threat],[risk],[],[])
  obsTxt = importRequirements([],[],handler.obstacles(),[],[])
  assocTxt = importAssociations([],handler.obstacleAssociations(),[])
  return obsTxt + assocTxt + raTxt

def importTVTypeFile(importFile,isOverwrite=1):
  parser = xml.sax.make_parser()
  handler = TVTypeContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  vulTypes,threatTypes = handler.types()
  return importTVTypes(vulTypes,threatTypes,isOverwrite)
 
def importTVTypes(vulTypes,threatTypes,isOverwrite):
  b = Borg()
  noOfVts = len(vulTypes)
  noOfTts = len(threatTypes)
  if (noOfVts > 0):
    if (isOverwrite):
      b.dbProxy.deleteVulnerabilityType(-1)
    for vt in vulTypes:
      b.dbProxy.addValueType(vt)
  if (noOfTts > 0):
    if (isOverwrite):
      b.dbProxy.deleteThreatType(-1)
    for tt in threatTypes:
      b.dbProxy.addValueType(tt)
  msgStr = 'Imported ' + str(noOfVts) + ' vulnerability types and ' + str(noOfTts) + ' threat types.'
  return msgStr

def importDirectoryFile(importFile,isOverwrite=1):
  parser = xml.sax.make_parser()
  handler = DirectoryContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  vulDir,threatDir = handler.directories()
  vdSize = len(vulDir)
  tdSize = len(threatDir)
  b = Borg()
  if (vdSize > 0):
    b.dbProxy.addVulnerabilityDirectory(vulDir,isOverwrite)
  if (tdSize > 0):
    b.dbProxy.addThreatDirectory(threatDir,isOverwrite)
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
    objtId = b.dbProxy.existingObject(dpParameters.name(),'domainproperty')
    if objtId == -1:
      b.dbProxy.addDomainProperty(dpParameters)
    else:
      dpParameters.setId(objtId)
      b.dbProxy.updateDomainProperty(dpParameters)
    dpCount += 1

  goalCount = 0
  for goalParameters in goalParameterSet:
    objtId = b.dbProxy.existingObject(goalParameters.name(),'goal')
    if objtId == -1:
      b.dbProxy.addGoal(goalParameters)
    else:
      goalParameters.setId(objtId)
      b.dbProxy.updateGoal(goalParameters)
    goalCount += 1

  obsCount = 0
  for obsParameters in obsParameterSet:
    objtId = b.dbProxy.existingObject(obsParameters.name(),'obstacle')
    if objtId == -1:
      b.dbProxy.addObstacle(obsParameters)
    else:
      obsParameters.setId(objtId)
      b.dbProxy.updateObstacle(obsParameters)
    obsCount += 1

  reqCount = 0
  for req,refName,refType in reqParameterSet:
    objtId = b.dbProxy.existingObject(req.name(),'requirement')
    if objtId == -1:
      isAsset = True
      if (refType == 'environment'):
        isAsset = False
      b.dbProxy.addRequirement(req,refName,isAsset)
    else:
      b.dbProxy.updateRequirement(req)
    reqCount += 1

  cmCount = 0
  for cmParameters in cmParameterSet:
    objtId = b.dbProxy.existingObject(cmParameters.name(),'countermeasure')
    if objtId == -1:
      b.dbProxy.addCountermeasure(cmParameters)
    else:
      cmParameters.setId(objtId)
      b.dbProxy.updateCountermeasure(cmParameters)
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
    objtId = b.dbProxy.existingObject(roleParameters.name(),'role')
    if objtId == -1:
      b.dbProxy.addRole(roleParameters)
    else:
      roleParameters.setId(objtId)
      b.dbProxy.updateRole(roleParameters)
    roleCount += 1

  assetCount = 0
  for assetParameters in assetParameterSet:
    objtId = b.dbProxy.existingObject(assetParameters.name(),'asset')
    if objtId == -1:
      b.dbProxy.addAsset(assetParameters)
    else:
      assetParameters.setId(objtId)
      b.dbProxy.updateAsset(assetParameters)
    assetCount += 1

  vulCount = 0
  for vulParameters in vulParameterSet:
    objtId = b.dbProxy.existingObject(vulParameters.name(),'vulnerability')
    if objtId == -1:
      b.dbProxy.addVulnerability(vulParameters)
    else:
      vulParameters.setId(objtId)
      b.dbProxy.updateVulnerability(vulParameters)
    vulCount += 1

  attackerCount = 0
  for attackerParameters in attackerParameterSet:
    objtId = b.dbProxy.existingObject(attackerParameters.name(),'attacker')
    if objtId == -1:
      b.dbProxy.addAttacker(attackerParameters)
    else:
      attackerParameters.setId(objtId)
      b.dbProxy.updateAttacker(attackerParameters)
    attackerCount += 1

  threatCount = 0
  for threatParameters in threatParameterSet:
    objtId = b.dbProxy.existingObject(threatParameters.name(),'threat')
    if objtId == -1:
      b.dbProxy.addThreat(threatParameters)
    else:
      threatParameters.setId(objtId)
      b.dbProxy.updateThreat(threatParameters)
    threatCount += 1

  riskCount = 0
  for riskParameters in riskParameterSet:
    objtId = b.dbProxy.existingObject(riskParameters.name(),'risk')
    if objtId == -1:
      b.dbProxy.addRisk(riskParameters)
    else:
      riskParameters.setId(objtId)
      b.dbProxy.updateRisk(riskParameters)
    riskCount += 1

  responseCount = 0
  for responseParameters in responseParameterSet:
    objtId = b.dbProxy.existingObject(responseParameters.name(),'response')
    if objtId == -1:
      b.dbProxy.addResponse(responseParameters)
    else:
      responseParameters.setId(objtId)
      b.dbProxy.updateResponse(responseParameters)
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
    objtId = b.dbProxy.existingObject(personaParameters.name(),'persona')
    if objtId == -1:
      b.dbProxy.addPersona(personaParameters)
    else:
      personaParameters.setId(objtId)
      b.dbProxy.updatePersona(personaParameters)
    personaCount += 1

  edCount = 0
  for edParameters in edParameterSet:
    objtId = b.dbProxy.existingObject(edParameters.name(),'external_document')
    if objtId == -1:
      b.dbProxy.addExternalDocument(edParameters)
    else:
      edParameters.setId(objtId)
      b.dbProxy.updateExternalDocument(edParameters)
    edCount += 1

  drCount = 0
  for drParameters in drParameterSet:
    objtId = b.dbProxy.existingObject(drParameters.name(),'document_reference')
    if objtId == -1:
      b.dbProxy.addDocumentReference(drParameters)
    else:
      drParameters.setId(objtId)
      b.dbProxy.updateDocumentReference(drParameters)
    drCount += 1

  taskCount = 0
  for taskParameters in taskParameterSet:
    objtId = b.dbProxy.existingObject(taskParameters.name(),'task')
    if objtId == -1:
      b.dbProxy.addTask(taskParameters)
    else:
      taskParameters.setId(objtId)
      b.dbProxy.updateTask(taskParameters)
    taskCount += 1

  ucCount = 0
  for ucParameters in ucParameterSet:
    objtId = b.dbProxy.existingObject(ucParameters.name(),'usecase')
    if objtId == -1:
      b.dbProxy.addUseCase(ucParameters)
    else:
      ucParameters.setId(objtId)
      b.dbProxy.updateUseCase(ucParameters)
    ucCount += 1

  crCount = 0
  for crParameters in crParameterSet:
    objtId = b.dbProxy.existingObject(crParameters.name(),'concept_reference')
    if objtId == -1:
      b.dbProxy.addConceptReference(crParameters)
    else:
      crParameters.setId(objtId)
      b.dbProxy.updateConceptReference(crParameters)
    crCount += 1

  pcCount = 0
  for pcParameters in pcParameterSet:
    b.dbProxy.addPersonaCharacteristic(pcParameters)
    pcCount += 1

  tcCount = 0
  for tcParameters in tcParameterSet:
    objtId = b.dbProxy.existingObject(tcParameters.task(),'task_characteristic')
    if objtId == -1:
      b.dbProxy.addTaskCharacteristic(tcParameters)
    else:
      tcParameters.setId(objtId)
      b.dbProxy.updateTaskCharacterisric(tcParameters)
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
    objtId = b.dbProxy.existingObject(envParameters.name(),'environment')
    if objtId == -1:
      b.dbProxy.addEnvironment(envParameters)
    else:
      envParameters.setId(objtId)
      b.dbProxy.updateEnvironment(envParameters)
    envCount += 1
  msgText = 'Imported ' + str(envCount) + ' environments'
  if (pSettings != None):
    msgText += ', and project settings'
    msgText += '.'
  return msgText

def importComponentViewFile(importFile):
  parser = xml.sax.make_parser()
  handler = ArchitecturalPatternContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  view = handler.view()
  return importComponentViewData(view)

def importAssetsFile(importFile):
  parser = xml.sax.make_parser()
  handler = TemplateAssetsContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  return importAssets(handler.valueTypes(),handler.assets())

def importAssets(valueTypes,assets):
  b = Borg()
  vtCount = 0
  taCount = 0

  for vtParameters in valueTypes:
    vtId = b.dbProxy.existingObject(vtParameters.name(),vtParameters.type())
    if vtId == -1:
      b.dbProxy.addValueType(vtParameters)
      vtCount += 1
  for taParameters in assets:
    taId = b.dbProxy.existingObject(taParameters.name(),'template_asset')
    if taId == -1:
      b.dbProxy.addTemplateAsset(taParameters)
      taCount += 1
  return 'Imported ' + str(vtCount) + ' value types, and ' + str(taCount) + ' template assets.'

def importComponentViewData(view):
  b = Borg()
  b.dbProxy.addComponentView(view)
  msgStr = 'Imported architectural pattern'
  return msgStr

def importSynopsesFile(importFile):
  parser = xml.sax.make_parser()
  handler = SynopsesContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  charSyns = handler.characteristicSynopses()
  refSyns = handler.referenceSynopses()
  stepSyns = handler.stepSynopses()
  refConts = handler.referenceContributions()
  ucConts = handler.useCaseContributions()
  return importSynopses(charSyns,refSyns,stepSyns,refConts,ucConts)

def importSynopses(charSyns,refSyns,stepSyns,refConts,ucConts):
  b = Borg()
  for cs in charSyns:
    b.dbProxy.addCharacteristicSynopsis(cs)
  for rs in refSyns:
    b.dbProxy.addReferenceSynopsis(rs)
  for ucName,envName,stepNo,synName,aType,aName in stepSyns:
    b.dbProxy.addStepSynopsis(ucName,envName,stepNo,synName,aType,aName)
  b.dbProxy.conn.commit()
  for rc in refConts:
    b.dbProxy.addReferenceContribution(rc)
  for uc in ucConts:
    b.dbProxy.addUseCaseContribution(uc)

  msgStr = 'Imported ' + str(len(charSyns)) + ' characteristic synopses, ' + str(len(refSyns)) + ' reference synopses, ' + str(len(stepSyns)) + ' step synopses, ' + str(len(refConts)) + ' reference contributions, and ' + str(len(ucConts)) + ' use case contributions.'
  return msgStr

def importDomainValuesFile(importFile):
  parser = xml.sax.make_parser()
  handler = DomainValueContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  tvValues,rvValues,cvValues,svValues,lvValues,capValues,motValues = handler.values()
  return importDomainValues(tvValues,rvValues,cvValues,svValues,lvValues,capValues,motValues)

def importDomainValues(tvValues,rvValues,cvValues,svValues,lvValues,capValues,motValues):
  noOfTvs = len(tvValues)
  noOfRvs = len(rvValues)
  noOfCvs = len(cvValues)
  noOfSvs = len(svValues)
  noOfLvs = len(lvValues)
  noOfCapVs = len(capValues)
  noOfMotVs = len(motValues)
 
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
  if (noOfCapVs > 0):
    for capvp in capValues:
      b.dbProxy.addValueType(capvp)
  if (noOfMotVs > 0):
    for motvp in motValues:
      b.dbProxy.addValueType(motvp)

  msgStr = 'Imported domain values'
  return msgStr

def importProcessesFile(importFile):
  parser = xml.sax.make_parser()
  handler = ProcessesContentHandler()
  parser.setContentHandler(handler)
  parser.setEntityResolver(handler)
  parser.parse(importFile)
  docs = handler.internalDocuments()
  codes = handler.codes()
  memos = handler.memos()
  quotations = handler.quotations()
  codeNetworks = handler.codeNetworks()
  processes = handler.processes()
  ics = handler.impliedCharacteristics()
  return importProcesses(docs,codes,memos,quotations,codeNetworks,processes,ics)

def importProcesses(docs,codes,memos,quotations,codeNetworks,processes,ics):
  noOfDocs = len(docs)
  noOfCodes = len(codes)
  noOfMemos = len(memos)
  noOfQuotations = len(quotations)
  noOfCNs = len(codeNetworks)
  noOfProcs = len(processes)
  noOfICs = len(ics)

  b = Borg()

  for dp in docs:
    b.dbProxy.addInternalDocument(dp)

  for cp in codes:
    b.dbProxy.addCode(cp)

  for mp in memos:
    b.dbProxy.addMemo(mp)

  for q in quotations:
    b.dbProxy.addQuotation(q)

  # Necessary because adding document memos currently overwrites the existing memo text
  for mp in memos:
    b.dbProxy.updateMemo(mp)

  for cn in codeNetworks:
    personaName = cn[0]
    rtName = cn[1]
    fromCode = cn[2]
    toCode = cn[3]
    b.dbProxy.addCodeRelationship(personaName,fromCode,toCode,rtName)

  for p in processes:
    b.dbProxy.addImpliedProcess(p)

  for ic in ics:
    b.dbProxy.addImpliedCharacteristic(ic)

  msgStr = 'Imported ' + str(noOfDocs) + ' internal documents, ' + str(noOfCodes) + ' codes, ' + str(noOfMemos) + ' memos, ' + str(noOfQuotations) + ' quotations, ' + str(noOfCNs) + ' code relationships, and ' + str(noOfProcs) + ' implied processes.'
  return msgStr

def importModelFile(importFile,isOverwrite = 1):
  b = Borg()
  modelTxt = ''
  if isOverwrite == 1:
    b.dbProxy.clearDatabase()
    modelTxt += importTVTypeFile(importFile) + '  '
  modelTxt += importDomainValuesFile(importFile) + ' '
  modelTxt += importProjectFile(importFile) + ' '
  modelTxt += importRiskAnalysisFile(importFile) + ' '
  modelTxt += importUsabilityFile(importFile) + ' '
  modelTxt += importRequirementsFile(importFile) + ' '
  modelTxt += importAssociationsFile(importFile) + ' '
  modelTxt += importSynopsesFile(importFile)
  return modelTxt
