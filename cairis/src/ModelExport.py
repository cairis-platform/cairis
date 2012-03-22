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
import cairo
import pangocairo
from ConceptMapModel import ConceptMapModel
import os

def listToString(l):
  s = ''
  noRows = len(l)
  for idx,row in enumerate(l):
    s += '** ' + row + '\n'
  return s

def drawGraph(graph,graphName):
  tmpDir = '/tmp'
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
  for ucName,ucShortCode,ucAuthor,ucTxt in rmUseCases:
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

    cmFile = envCode + '_conceptMap.jpg'
    buildConceptMap(b.dbProxy,envName,cmFile)
    buf +='!' + cmFile + '!\n\n'
    
    for envReq in envReqs:
      reqName = envReq[0]
      reqOrig = envReq[1]
      reqPri = envReq[2]
      reqComments = envReq[3]
      reqDesc = envReq[4]
      reqScs = envReq[6]
      reqUcs = envReq[7]
      reqBis = envReq[8]

      buf += 'h2. ' + reqName + '\n\n* Priority: ' + reqPri + '\n\n* Originator: ' + reqOrig + '\n\n* Comments: ' + reqComments + '\n\n* Related scenarios:\n' + listToString(reqScs) + '\n\n* Related use cases:\n' + listToString(reqUcs) + '\n\n* Related product backlog:\n' + listToString(reqBis) + '\n\n' + reqDesc + '\n\n\n'
    envFile = open(outputDir + '/' + envCode + '-requirements.txt','w,')
    envFile.write(buf)
    envFile.close()
    outputBuf += buf

  outputFile = open(outFileName,'w')
  outputFile.write(outputBuf)
  outputFile.close()
  return 'Exported requirements'
