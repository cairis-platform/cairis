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


from Borg import Borg
from kaosxdot import KaosXDotParser
from componentxdot import ComponentXDotParser
import cairo
import pangocairo
from ConceptMapModel import ConceptMapModel
from ComponentModel import ComponentModel
from AssetModel import AssetModel
from KaosModel import KaosModel
import os
import re

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
  b = Borg()
  tmpDir = b.tmpDir
  outputDir = os.environ['OUTPUT_DIR']
  tmpFile = tmpDir + '/' + graphName + '.pdf'
  s = cairo.PDFSurface(tmpFile,graph.width,graph.height)
  c1 = cairo.Context(s)
  c2 = pangocairo.CairoContext(c1)
  c2.set_line_cap(cairo.LINE_CAP_BUTT)
  c2.set_line_join(cairo.LINE_JOIN_MITER)
  graph.zoom_ratio = 1
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
  model = ConceptMapModel(p.conceptMapModel(envName).values(),envName,'',True)
  if (model.size() == 0):
    return False
  parser = KaosXDotParser('conceptmap',model.graph())
  parser.cfSet = True
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True


def exportRedmineScenarios(outFile):
  b = Borg()
  rmScenarios = b.dbProxy.redmineScenarios()

  buf = ''
  noScenarios = 0
  for sName,sEnv,sTxt in rmScenarios:
    buf += sTxt + '\n'
    noScenarios += 1
  sFile = open(outFile,'w')
  sFile.write(buf)
  sFile.close()
  return 'Exported ' + str(noScenarios) + ' scenarios.'

  
def exportRedmineUseCases(outFile):
  b = Borg()
  rmUseCases = b.dbProxy.redmineUseCases()

  buf = ''
  noUseCases = 0
  ucDict = {'ID':[],'DA':[],'NM':[],'PS':[],'NC':[],'LC':[],'CAP':[],'TMS':[]}

  for ucName,ucShortCode,ucAuthor,ucTxt in rmUseCases:
    ucCat = re.sub('[0-9]','',ucShortCode)
    ucDict[ucCat].append( (ucName,ucShortCode,ucAuthor,ucTxt))
  fnlCats = ucDict.keys()
  fnlCats.sort()

  for fnlCat in fnlCats:
    for ucName,ucShortCode,ucAuthor,ucTxt in ucDict[fnlCat]: 
      buf += ucTxt + '\n'
      noUseCases += 1
  ucFile = open(outFile,'w')
  ucFile.write(buf)
  ucFile.close()
  return 'Exported ' + str(noUseCases) + ' use cases.'


def exportRedmineRequirements(outFileName):
  b = Borg()
  reqs = b.dbProxy.getRedmineRequirements()

  envNames = reqs.keys()
  envNames.sort()
  outputDir = os.environ['OUTPUT_DIR']

  outputBuf = ''
  for envName in envNames:
    envReqs = reqs[envName]
    envCode = envReqs[0][5]
    buf = 'h1. ' + envName + ' requirements\n\n' 

    cmFile = envCode + '_conceptMap'
    buildConceptMap(b.dbProxy,envName,cmFile)
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

def exportGRL(outFileName,personaName,taskName,envName):
  b = Borg()
  buf = b.dbProxy.pcToGrl(personaName,taskName,envName)
  rFile = open(outFileName,'w')
  rFile.write(buf)
  rFile.close()
  return 'Exported GRL for ' + personaName + ' in ' + taskName + ' situated in environment ' + envName

def buildComponentModel(p,apName,graphName):
  interfaces,connectors = p.componentView(apName)
  model = ComponentModel(interfaces,connectors)
  parser = ComponentXDotParser(model.graph())
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True

def buildComponentAssetModel(p,cName,graphName):
  assocs = p.componentAssetModel(cName)
  model = AssetModel(assocs.values(),'')
  parser = KaosXDotParser('class',model.graph())
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True

def buildComponentGoalModel(p,cName,graphName):
  assocs = p.componentGoalModel(cName)
  model = KaosModel(assocs.values(),'','template_goal')
  parser = KaosXDotParser('goal',model.graph())
  graph = parser.parse()
  drawGraph(graph,graphName)
  return True


def exportArchitecture(outFile):
  b = Borg()
  rmArchitecture = b.dbProxy.redmineArchitecture()

  buf = ''
  noAPs = 0
  for aName,aType,sTxt in rmArchitecture:
    buf += sTxt + '\n'
    noAPs += 1
    if (aType == 'component'):
      caName = aName.replace(' ','_') + 'AssetModel'
      cgName = aName.replace(' ','_') + 'GoalModel'
      buildComponentAssetModel(b.dbProxy,aName,caName)
      buildComponentGoalModel(b.dbProxy,aName,cgName)
    else:
      graphName = aName.replace(' ','_') + 'ComponentModel'
      buildComponentModel(b.dbProxy,aName,graphName)
  
  aFile = open(outFile,'w')
  aFile.write(buf)
  aFile.close()
  return 'Exported ' + str(noAPs) + ' architectural patterns.'
