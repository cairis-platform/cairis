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

def exportModel(outFile = None,session_id = None):
  b = Borg()
  xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE cairis_model PUBLIC "-//CAIRIS//DTD MODEL 1.0//EN" "http://cairis.org/dtd/cairis_model.dtd">\n<cairis_model>\n\n\n'
  xmlBuf+= b.get_dbproxy(session_id).tvTypesToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).domainValuesToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).projectToXml(0) + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).riskAnalysisToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).usabilityToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).goalsToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).associationsToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).misusabilityToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).dataflowsToXml(0)[0] + '\n\n'
  xmlBuf+= b.get_dbproxy(session_id).locationsToXml()[0] + '\n\n</cairis_model>'
  if outFile == None:
    return xmlBuf
  else:
    f = codecs.open(outFile,'w','utf-8')
    f.write(xmlBuf)
    f.close()
    return 'Exported model'

def exportJSON(outFile = None, session_id = None):
  b = Borg()
  jsonBuf = '{"version" : "2",\n'
  jsonBuf += b.get_dbproxy(session_id).tvTypesToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).domainValuesToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).projectToJSON() + ',\n'
  jsonBuf += b.get_dbproxy(session_id).riskAnalysisToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).usabilityToJSON()[0] + ',\n'
  jsonBuf += b.get_dbproxy(session_id).goalsToJSON()[0] + '\n\n'
  jsonBuf += '}'
  if outFile == None:
    return jsonBuf
  else:
    f = codecs.open(outFile,'w','utf-8')
    f.write(jsonBuf)
    f.close()
    return 'Exported JSON'
