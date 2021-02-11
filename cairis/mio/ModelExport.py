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
import os
import re
import codecs
import io
import zipfile
from cairis.core.ARM import ARMException
from base64 import b64decode
from xlsxwriter import Workbook

__author__ = 'Shamal Faily'

def listToString(l):
  s = ''
  listSize = len(l)
  if listSize == 0:
    return 'None'
  for idx,v in enumerate(l):
    s += v
    if idx < (listSize - 1):
      s += ','
  return s

def drawGraph(graph,graphName):
  import cairo
  import pangocairo
  b = Borg()
  tmpDir = b.tmpDir
  outputDir = os.environ['OUTPUT_DIR']
  tmpFile = tmpDir + '/' + graphName + '.pdf'
#Make the surface a bit bigger to account for graphviz positioning the image too far left
  s = cairo.PDFSurface(tmpFile,graph.width + 5,graph.height + 5)
  c1 = cairo.Context(s)
  c2 = pangocairo.CairoContext(c1)
  c2.set_line_cap(cairo.LINE_CAP_BUTT)
  c2.set_line_join(cairo.LINE_JOIN_MITER)
  graph.zoom_ratio = 1
#Reposition the co-ordinates to start a bit more to the right
  c2.translate(3,3)
  graph.draw(c2)
  s.finish()
  svgFile = tmpDir + '/' + graphName + '.svg'
  s = cairo.SVGSurface(svgFile,graph.width,graph.height)
  c1 = cairo.Context(s)
  c2 = pangocairo.CairoContext(c1)
  c2.set_line_cap(cairo.LINE_CAP_BUTT)
  c2.set_line_join(cairo.LINE_JOIN_MITER)
  graph.zoom_ratio = 1
  graph.draw(c2)
  s.finish()

  ppmFile = tmpDir + '/' + graphName + '.ppm'
  jpgFile = outputDir + '/' + graphName
  cmd1 = 'pdftoppm ' + tmpFile + ' > ' + ppmFile
  cmd2 = 'ppmtojpeg ' + ppmFile + ' > ' + jpgFile
  os.system(cmd1)
  os.system(cmd2)

def buildConceptMap(p,envName,graphName):
  from cairis.core.kaosxdot import KaosXDotParser
  from cairis.core.ConceptMapModel import ConceptMapModel
  model = ConceptMapModel(list(p.conceptMapModel(envName).values()),envName,'',True)
  if (model.size() == 0):
    return False
  parser = KaosXDotParser('conceptmap',model.graph())
  parser.cfSet = True
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True


def exportRedmineScenarios(outFile,session_id = None):
  b = Borg()
  rmScenarios = b.get_dbproxy(session_id).redmineScenarios()

  buf = ''
  noScenarios = 0
  for sName,sEnv,sTxt in rmScenarios:
    buf += sTxt + '\n'
    noScenarios += 1
  sFile = codecs.open(outFile,'w','utf-8')
  sFile.write(buf)
  sFile.close()
  return 'Exported ' + str(noScenarios) + ' scenarios.'

  
def exportRedmineUseCases(outFile,session_id = None):
  b = Borg()
  rmUseCases = b.get_dbproxy(session_id).redmineUseCases()

  buf = ''
  noUseCases = 0

  ucDict = {}
  envs = b.get_dbproxy(session_id).getEnvironments()
  for envName in envs:
    envShortCode = envs[envName].shortCode()
    ucDict[envShortCode] = []

  for ucName,ucShortCode,ucAuthor,ucTxt in rmUseCases:
    ucCat = re.sub('[0-9]','',ucShortCode)
    ucDict[ucCat].append( (ucName,ucShortCode,ucAuthor,ucTxt))
  fnlCats = list(ucDict.keys())
  fnlCats.sort()

  for fnlCat in fnlCats:
    for ucName,ucShortCode,ucAuthor,ucTxt in ucDict[fnlCat]: 
      buf += ucTxt + '\n'
      noUseCases += 1
  ucFile = open(outFile,'w')
  ucFile.write(buf)
  ucFile.close()
  return 'Exported ' + str(noUseCases) + ' use cases.'


def exportRedmineRequirements(outFileName,session_id = None):
  b = Borg()
  reqs = b.get_dbproxy(session_id).getRedmineRequirements()

  envNames = list(reqs.keys())
  envNames.sort()
  outputDir = os.environ['OUTPUT_DIR']

  outputBuf = ''
  for envName in envNames:
    envReqs = reqs[envName]
    envCode = envReqs[0][5]
    buf = 'h1. ' + envName + ' requirements\n\n' 

    cmFile = envCode + '_conceptMap'
    buildConceptMap(b.get_dbproxy(session_id),envName,cmFile)
    buf +='!' + cmFile + '!\n\n'
    
    buf += '|*Short Name*|*Comments*|*Scenarios*|*Use Cases*|*Backlog*|\n'

    for envReq in envReqs:
      reqName = envReq[0]
      reqOrig = envReq[1]
      reqPri = envReq[2]
      reqComments = envReq[3]
      reqDesc = envReq[4]
      reqScs = envReq[6]
      reqUcs = envReq[7]
      reqBis = envReq[8]
   
      buf += '|/2.*' + reqName + '*\n' + reqPri + ', ' + reqOrig + '|\\4.' + reqDesc + '|\n|' + reqComments + '|' + listToString(reqScs) + '|' + listToString(reqUcs) + '|' + listToString(reqBis) + '|\n'
    envFile = open(outputDir + '/' + envCode + '-requirements.txt','w,')
    envFile.write(buf)
    envFile.close()
    outputBuf += buf + '\n'

  outputFile = open(outFileName,'w')
  outputFile.write(outputBuf)
  outputFile.close()
  return 'Exported requirements'

def exportGRL(outFileName,personaNames,taskNames,envName,session_id = None):
  b = Borg()
  pStr = personaNames
  tStr = taskNames
  buf = b.get_dbproxy(session_id).pcToGrl(pStr,tStr,envName)
  rFile = open(outFileName,'w')
  rFile.write(buf)
  rFile.close()
  return 'Exported GRL for ' + str(pStr) + ' in tasks ' + str(tStr) + ' situated in environment ' + envName

def exportSecurityPatterns(outFileName,session_id = None):
  b = Borg()
  buf = b.get_dbproxy(session_id).securityPatternsToXml()
  rFile = open(outFileName,'w')
  rFile.write(buf)
  rFile.close()
  return 'Exported security patterns'

def buildComponentModel(p,apName,graphName):
  from cairis.legacy.componentxdot import ComponentXDotParser
  from cairis.legacy.ComponentModel import ComponentModel
  interfaces,connectors = p.componentView(apName)
  model = ComponentModel(interfaces,connectors)
  parser = ComponentXDotParser(model.graph())
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True

def buildComponentAssetModel(p,cName,graphName):
  from cairis.legacy.kaosxdot import KaosXDotParser
  from cairis.legacy.AssetModel import AssetModel
  assocs = p.componentAssetModel(cName)
  model = AssetModel(list(assocs.values()),'')
  parser = KaosXDotParser('class',model.graph())
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True

def buildComponentGoalModel(p,cName,graphName):
  from cairis.legacy.kaosxdot import KaosXDotParser
  from cairis.legacy.KaosModel import KaosModel
  assocs = p.componentGoalModel(cName)
  model = KaosModel(list(assocs.values()),'','template_goal')
  parser = KaosXDotParser('goal',model.graph())
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True

def buildRiskObstacleModel(p,apName,envName,graphName):
  from cairis.legacy.kaosxdot import KaosXDotParser
  from cairis.legacy.KaosModel import KaosModel
  assocs = p.riskObstacleModel(apName,envName)
  model = KaosModel(list(assocs.values()),envName,'obstacle',apName)
  parser = KaosXDotParser('obstacle',model.graph())
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True

def exportArchitecture(outFile,session_id = None):
  b = Borg()
  rmArchitecture = b.get_dbproxy(session_id).redmineArchitecture()

  buf = ''
  noAPs = 0
  for aName,aType,sTxt in rmArchitecture:
    buf += sTxt + '\n'
    noAPs += 1
    if (aType == 'component'):
      caName = aName.replace(' ','_') + 'AssetModel.jpg'
      cgName = aName.replace(' ','_') + 'GoalModel.jpg'
      buildComponentAssetModel(b.get_dbproxy(session_id),aName,caName)
      buildComponentGoalModel(b.get_dbproxy(session_id),aName,cgName)
    elif (aType == 'architectural_pattern'):
      graphName = aName.replace(' ','_') + 'ComponentModel.jpg'
      buildComponentModel(b.get_dbproxy(session_id),aName,graphName)
  
  aFile = open(outFile,'w')
  aFile.write(buf)
  aFile.close()

  outFilePrefix,outFilePostfix = outFile.split('.')
  summaryFile = outFilePrefix + '-summary.' + outFilePostfix

  archSumm = b.get_dbproxy(session_id).redmineArchitectureSummary('Complete')
  buf = ''
  for aName,sTxt in archSumm:
    buf += sTxt + '\n'

  aFile = open(summaryFile,'w')
  aFile.write(buf)
  aFile.close()
 
  return 'Exported ' + str(noAPs) + ' architectural patterns.'

def exportAttackPatterns(outFile,session_id = None):
  b = Borg()
  rmAttackPatterns = b.get_dbproxy(session_id).redmineAttackPatterns()

  buf = 'h1. Contextualised Attack Patterns\n\nThis section was automatically generated based on the contents of the webinos WP 2 git repository at http://dev.webinos.org/git/wp2.git.\n\nh2. Obstacle probability: colour codes\n\n!{width:200px}ObsColour.jpg!\n\n'
  apdxBuf = ''
  noAPs = 0
  for apName,envName,cType,apTxt in rmAttackPatterns:
    if (cType == 'body'):
      buf += apTxt + '\n'
      gmName = apName.replace(' ','_') + 'ObstacleModel.jpg'
      buildRiskObstacleModel(b.get_dbproxy(session_id),apName,envName,gmName)
    else:
      apdxBuf += apTxt + '\n' 
    noAPs += 1
  aFile = open(outFile,'w')
  aFile.write(buf)
  aFile.close()

  fileName,filePostfix = outFile.split('.')
  summaryFile = fileName + '-summary.txt'
  buf = b.get_dbproxy(session_id).redmineAttackPatternsSummary('Complete')
  aFile = open(summaryFile,'w')
  aFile.write(buf)
  aFile.close()

  return 'Exported ' + str(noAPs) + ' attack patterns.'

def extractModel(session_id = None,ignoreValidityCheck = 0,dbProxy = None):
  proxy = dbProxy
  if (proxy == None):
    b = Borg()
    proxy = b.get_dbproxy(session_id)
  if (ignoreValidityCheck == 0):
    valStr = proxy.validateForExport() 
    if (len(valStr) > 0):
      raise ARMException(valStr)
  xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE cairis_model PUBLIC "-//CAIRIS//DTD MODEL 1.0//EN" "http://cairis.org/dtd/cairis_model.dtd">\n<cairis_model>\n\n\n'
  xmlBuf+= proxy.tvTypesToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.domainValuesToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.projectToXml(0) + '\n\n'
  xmlBuf+= proxy.riskAnalysisToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.usabilityToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.goalsToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.associationsToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.synopsesToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.misusabilityToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.dataflowsToXml(0)[0] + '\n\n'
  xmlBuf+= proxy.locationsToXml()[0] + '\n\n'
  xmlBuf+= proxy.storiesToXml(0)[0] + '\n\n</cairis_model>'
  return xmlBuf

def exportModel(outFile = None,session_id = None, ignoreValidityCheck = 0,dbProxy = None):
  xmlBuf = extractModel(session_id,ignoreValidityCheck,dbProxy)
  if outFile == None:
    return xmlBuf
  else:
    f = codecs.open(outFile,'w','utf-8')
    f.write(xmlBuf)
    f.close()
    return 'Exported model'

def extractPackage(session_id = None, ignoreValidityCheck = 0, dbProxy = None):
  buf = io.BytesIO()
  zf = zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED)
  zf.writestr('model.xml',extractModel(session_id,ignoreValidityCheck,dbProxy))

  proxy = dbProxy
  if (proxy == None):
    b = Borg()
    proxy = b.get_dbproxy(session_id)
  apNames = proxy.getDimensionNames('component_view','')
  for apName in apNames:
    apBuf = proxy.architecturalPatternToXml(apName)
    zf.writestr(apName + '.xml',apBuf)

  spNames = proxy.getDimensionNames('securitypattern','')
  if (len(spNames) > 0):
    spBuf = proxy.securityPatternsToXml()
    zf.writestr('security_patterns.xml',spBuf)

  for imgName,imgContent in proxy.getImages():
    zf.writestr(imgName,b64decode(imgContent))
  zf.close()
  return buf.getvalue()

def exportPackage(outFile = None, session_id = None, ignoreValidityCheck = 0, dbProxy = None):
  buf = extractPackage(session_id,ignoreValidityCheck,dbProxy)
  if outFile == None:
    return buf
  else:
    f = codecs.open(outFile,'wb')
    f.write(buf)
    f.close()
    return 'Exported package'

def exportJSON(outFile = None, session_id = None):
  b = Borg()
  jsonBuf = '{"version" : "2",\n'
  jsonBuf += b.get_dbproxy(session_id).tvTypesToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).domainValuesToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).projectToJSON() + ',\n'
  jsonBuf += b.get_dbproxy(session_id).riskAnalysisToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).usabilityToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).goalsToJSON()[0] + ',\n\n'
  jsonBuf += b.get_dbproxy(session_id).associationsToJSON()[0] + ',\n\n'
  jsonBuf += b.get_dbproxy(session_id).misusabilityToJSON()[0] + ',\n\n'
  jsonBuf += b.get_dbproxy(session_id).dataflowsToJSON()[0] + ',\n\n'
  jsonBuf += b.get_dbproxy(session_id).locationsToJSON()[0] + '\n\n'
  jsonBuf += '}'
  if outFile == None:
    return jsonBuf
  else:
    f = codecs.open(outFile,'w','utf-8')
    f.write(jsonBuf)
    f.close()
    return 'Exported JSON'

def exportUserGoalWorkbook(outFile, session_id = None):
  b = Borg()
  dbProxy = b.get_dbproxy(session_id)
  drs = dbProxy.getDocumentReferences()
  pcs = list(map(lambda x: x[1],list(dbProxy.getPersonaCharacteristics().items())))

  drSet = set([])
  for pc in pcs:
    personaName = pc.persona()
    for e in pc.grounds() + pc.warrant() + pc.rebuttal():
      dr = drs[e[0]]
      dr.thePersonaName = personaName
      drSet.add(dr)

  wb = Workbook(outFile)
  ugSheet = wb.add_worksheet('UserGoal')
  hFormat = wb.add_format({'border':1,'bg_color' : '#C6EFCE', 'bold' : True, 'text_wrap' : True})
  unlocked = wb.add_format({'locked': False,'text_wrap' : True,'font_color' : 'green'})
  tWrap = wb.add_format({'text_wrap' : True,'italic' : True})
  ugSheet.protect()
  ugSheet.write('A1','Reference',hFormat)
  ugSheet.write('B1','Description',hFormat)
  ugSheet.write('C1','Persona',hFormat)
  ugSheet.write('D1','persona/document_reference',hFormat)
  ugSheet.write('E1','Element Type',hFormat)
  ugSheet.write('F1','User Goal',hFormat)
  ugSheet.write('G1','Initial Satisfaction',hFormat)

  cellDict = {}
  ugRow = 1
  for objt in pcs + list(drSet):
    refName = ''
    elementType = ''
    refDesc = ''
    if (objt.__class__.__name__ == 'PersonaCharacteristic'):
      refName = objt.characteristic()
      elementType = 'persona'
      refDesc = refName
    else:
      refName = objt.name()
      elementType = 'document_reference'
      refDesc = objt.excerpt()
    ugSheet.write_string(ugRow,0,refName,tWrap)
    ugSheet.write_string(ugRow,1,refDesc,tWrap)
    ugSheet.write_string(ugRow,2,objt.thePersonaName,tWrap)
    ugSheet.write_string(ugRow,3,elementType,tWrap)
    ugSheet.data_validation('E' + str(ugRow),{'validate':'list','source' : ['goal','softgoal','belief']})
    ugSheet.write_string('E' + str(ugRow + 1),'goal',unlocked)
    cellDict[refName] = 'F' + str(ugRow + 1)
    ugSheet.write_string(ugRow,5,'',unlocked)
    ugSheet.data_validation('G' + str(ugRow + 1),{'validate':'list','source' : ['Satisfied','Weakly Satisfied','None','Weakly Denied','Denied']})
    ugSheet.write_string('G' + str(ugRow + 1),'None',unlocked)
    ugRow += 1
  ugSheet.set_column('A:B',30)
  ugSheet.set_column('C:D',20)
  ugSheet.set_column('F:G',30)

  contSheet = wb.add_worksheet('Contributions')
  hFormat = wb.add_format({'border':1,'bg_color' : '#C6EFCE', 'bold' : True, 'text_wrap' : True})
  contSheet.protect()
  contSheet.write('A1','Source (GWR User Goal)',hFormat)
  contSheet.write('B1','Destination (PC User Goal)',hFormat)
  contSheet.write('C1','Means/End',hFormat)
  contSheet.write('D1','Contribution',hFormat)

  contRow = 1
  for pc in pcs:
    for e in pc.grounds() + pc.warrant() + pc.rebuttal():
      contSheet.write_formula(contRow,0,"=UserGoal!" + cellDict[e[0]],tWrap)
      contSheet.write_formula(contRow,1,"=UserGoal!" + cellDict[pc.characteristic()],tWrap)
      contSheet.data_validation('C' + str(contRow + 1),{'validate':'list','source' : ['means','end']})
      contSheet.write('C' + str(contRow + 1),'means',unlocked)
      contSheet.data_validation('D' + str(contRow + 1),{'validate':'list','source' : ['Make','SomePositive','Help','Hurt','SomeNegative','Break']})
      contSheet.write('D' + str(contRow + 1),'Help',unlocked)
      contRow +=1
  contSheet.set_column('A:B',20)
  contSheet.set_column('C:D',15)
  wb.close()

def exportPersonaCharacteristicsWorkbook(outFile, session_id = None):
  b = Borg()
  dbProxy = b.get_dbproxy(session_id)
  roles = list(map(lambda x: x[1],list(dbProxy.getRoles().items())))
  eds = list(map(lambda x: x[1],list(dbProxy.getExternalDocuments().items())))
  drs = list(map(lambda x: x[1],list(dbProxy.getDocumentReferences().items())))
  pcs = list(map(lambda x: x[1],list(dbProxy.getPersonaCharacteristics().items())))


  wb = Workbook(outFile)
  hFormat = wb.add_format({'border':1,'bg_color' : '#C6EFCE', 'bold' : True, 'text_wrap' : True})
  wrapped = wb.add_format({'text_wrap' : True,})

  edSheet = wb.add_worksheet('External Documents')
  edSheet.write('A1','Name',hFormat)
  edSheet.write('B1','Authors',hFormat)
  edSheet.write('C1','Version',hFormat)
  edSheet.write('D1','Publication Date',hFormat)
  edSheet.write('E1','Description',hFormat)

  edRow = 1
  for edoc in eds:
    edSheet.write('A' + str(edRow + 1),edoc.name(),wrapped)
    edSheet.write('B' + str(edRow + 1),edoc.authors(),wrapped)
    edSheet.write('C' + str(edRow + 1),edoc.version())
    edSheet.write('D' + str(edRow + 1),edoc.date(),wrapped)
    edSheet.write('E' + str(edRow + 1),edoc.description(),wrapped)
    edRow += 1
  edSheet.set_column('A:D',20)
  edSheet.set_column('E:E',50)

  drSheet = wb.add_worksheet('Document References')
  drSheet.write('A1','Name',hFormat)
  drSheet.write('B1','External Document',hFormat)
  drSheet.write('C1','Contributor',hFormat)
  drSheet.write('D1','Excerpt',hFormat)

  drRow = 1
  for dr in drs:
    drSheet.write('A' + str(drRow + 1),dr.name(),wrapped)
    drSheet.data_validation('B' + str(drRow + 1),{'validate':'list','source' : "='External Documents'!$A$2:$A$5000"})
    drSheet.write('B' + str(drRow + 1),dr.document(),wrapped)
    drSheet.write('C' + str(drRow + 1),dr.contributor(),wrapped)
    drSheet.write('D' + str(drRow + 1),dr.excerpt(),wrapped)
    drRow += 1

  while drRow <= 5000:
    drSheet.data_validation('B' + str(drRow + 1),{'validate':'list','source' : "='External Documents'!$A$2:$A$5000"})
    drRow += 1

  drSheet.set_column('A:C',50)
  drSheet.set_column('D:D',75)


  pcSheet = wb.add_worksheet('Persona Characteristics')
  pcSheet.write('A1','Characteristic',hFormat)
  pcSheet.write('B1','Persona',hFormat)
  pcSheet.write('C1','Variable',hFormat)
  pcSheet.write('D1','Modal Qualifier',hFormat)
  pcSheet.write('E1','Grounds',hFormat)
  pcSheet.write('F1','Warrant',hFormat)
  pcSheet.write('G1','Rebuttal',hFormat)

  pcRow = 1
  for pc in pcs:
    pcSheet.write('A' + str(pcRow + 1),pc.characteristic(),wrapped)
    pcSheet.write('B' + str(pcRow + 1),pc.persona(),wrapped)
    pcSheet.data_validation('C' + str(pcRow + 1),{'validate':'list','source' : ['Activities','Attitudes','Aptitudes','Motivations','Skills','Environment Narrative','Intrinsic','Contextual']})
    pcSheet.write('C' + str(pcRow + 1),pc.behaviouralVariable(),wrapped)
    pcSheet.write('D' + str(pcRow + 1),pc.qualifier(),wrapped)
    pcSheet.write('E' + str(pcRow + 1),','.join(list(map(lambda x: x[0],pc.grounds()))),wrapped)
    pcSheet.write('F' + str(pcRow + 1),','.join(list(map(lambda x: x[0],pc.warrant()))),wrapped)
    pcSheet.write('G' + str(pcRow + 1),','.join(list(map(lambda x: x[0],pc.rebuttal()))),wrapped)
    pcRow += 1

  while pcRow <= 5000:
    pcSheet.data_validation('C' + str(pcRow + 1),{'validate':'list','source' : ['Activities','Attitudes','Aptitudes','Motivations','Skills','Environment Narrative','Intrinsic','Contextual']})
    pcRow += 1

  pcSheet.set_column('A:A',50)
  pcSheet.set_column('B:D',20)
  pcSheet.set_column('E:G',75)
  wb.close()
