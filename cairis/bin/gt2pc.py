#!/usr/bin/python3
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

import string
import argparse
import csv

__author__ = 'Shamal Faily'

def remspace(my_str):
  if len(my_str) < 2: # returns ' ' unchanged
    return my_str
  if my_str[-1] == '\n':
    if my_str[-2] == ' ':
      return my_str[:-2] + '\n'
  if my_str[-1] == ' ':
    return my_str[:-1]
  return my_str



def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Grounded Theory to Persona Case converter')
  parser.add_argument('modelFile',help='model file to create')
  parser.add_argument('--context',dest='contextName',help='model context')
  parser.add_argument('--originator',dest='originatorName',help='model originator')
  parser.add_argument('--concepts',dest='conceptsFile',help='grounded theory model concepts')
  parser.add_argument('--propositions',dest='propositionsFile',help='Propositions associated with grounded theory model quotations')
  parser.add_argument('--characteristics',dest='characteristicsFile',help='Persona characteristics associated with grounded theory model associations')
  parser.add_argument('--narratives',dest='narrativesFile',help='Persona narratives')

  args = parser.parse_args()


  xmlHdr = '<?xml version="1.0"?>\n<!DOCTYPE cairis_model PUBLIC "-//CAIRIS//DTD MODEL 1.0//EN" "http://cairis.org/dtd/cairis_model.dtd">\n\n<cairis_model>\n\n'

  xmlHdr += '<cairis>\n  <project_settings name="' + args.contextName + '">\n    <contributors>\n      <contributor first_name="None" surname="None" affiliation="' + args.originatorName + '" role="Scribe" />\n    </contributors>\n  </project_settings>\n  <environment name="' + args.contextName + '" short_code="' + args.contextName + '">\n    <definition>' + args.contextName + '</definition>\n    <asset_values>\n      <none>TBC</none>\n      <low>TBC</low>\n      <medium>TBC</medium>\n      <high>TBC</high>\n    </asset_values>\n  </environment>\n</cairis>\n\n<riskanalysis>\n  <role name="Undefined" type="Stakeholder" short_code="UNDEF">\n    <description>Undefined</description>\n  </role>\n</riskanalysis>\n\n<usability>\n'
  xmlBuf = ''

  conceptDict = {}
  with open(args.conceptsFile,'r') as cFile:
    cReader = csv.reader(cFile, delimiter = ',', quotechar='"')
    for row in cReader:
      edCode = row[0]
      edName = row[1] + ' GT concept'
      conceptDict[edCode] = edName
      edVersion = row[2]
      edDate = row[3]
      edAuthors = row[4]
      xmlBuf += '<external_document name=\"' + edName + '\" version=\"' + edVersion + '\" date=\"' + edDate + '\" authors=\"' + edAuthors + '\">\n  <description>' + edName + '</description>\n</external_document>\n'
  xmlBuf += '\n'

  propDict = {}
  with open(args.propositionsFile,'r') as pFile:
    pReader = csv.reader(pFile, delimiter = ',', quotechar='"')
    for row in pReader:
      pId = row[0]
      edCode,pNo = pId.split('-')
      docName = conceptDict[edCode]
      pName = row[1]
      pDesc = row[2]
      pContrib = row[3]
      propDict[pId] = (pName,pDesc)
      xmlBuf += '<document_reference name=\"' + pName + '\" contributor=\"' + pContrib + '\" document=\"' + docName + '\">\n  <excerpt>' + pDesc + '</excerpt>\n</document_reference>\n'
  xmlBuf += '\n'

  xmlBuf += '\n'
  bvDict = {}
  bvDict['ACT'] = 'Activities'
  bvDict['ATT'] = 'Attitudes'
  bvDict['APT'] = 'Aptitudes'
  bvDict['MOT'] = 'Motivations'
  bvDict['SKI'] = 'Skills'
  bvDict['INT'] = 'Intrinsic'
  bvDict['CON'] = 'Contextual'

  personaNames = set([])
  
  pcf = open(args.characteristicsFile,"r")
  for li in pcf.readlines():
    li = string.strip(li)
    pce = li.split(',')
    gtr = pce[0]
    pcName = pce[1]
    labelName = pce[2]
    pName = pce[3]
    if pName == 'NONE':
      continue 

    personaNames.add(pName)
    bvName = bvDict[pce[4]]
    gcList = pce[5].split(' ')
    gList = []
    for gc in gcList:
      if gc != '':
        gVal = propDict[gc] 
        gList.append((gVal[0],gVal[1],'document'))
    
    wcList = pce[6].split(' ')
    wList = []
    for wc in wcList:
      if wc != '':
        wVal = propDict[wc] 
        wList.append((wVal[0],wVal[1],'document'))

    modQual = pce[7]
    rcList = pce[8].split(' ')
    rList = []
    for rc in rcList:
      if rc != '':
        rVal = propDict[rc] 
        rList.append((rVal[0],rVal[1],'document'))
    xmlBuf += '<persona_characteristic persona=\"' + pName + '\" behavioural_variable=\"' + bvName + '\" modal_qualifier=\"' + modQual + '\" >\n  <definition>' + pcName + '</definition>\n'
    for g in gList:
      xmlBuf += '  <grounds type=\"document\" reference=\"' + g[0] + '\" />\n'
    for w in wList:
      xmlBuf += '  <warrant type=\"document\" reference=\"' + w[0] + '\" />\n'
    for r in rList:
      xmlBuf += '  <rebuttal type=\"document\" reference=\"' + r[0] + '\" />\n'
    xmlBuf += '</persona_characteristic>\n'          
  pcf.close()

  pnDict = {}
  with open(args.narrativesFile,'r') as nFile:
    nReader = csv.reader(nFile, delimiter = ',', quotechar='"')
    for row in nReader:
      pnDict[(row[0],row[1])] = row[2]

  pHdr = ''
  for personaName in personaNames:
    pHdr += '<persona name=\"' + personaName + '\" type=\"Primary\" assumption_persona=\"FALSE\" image=\"\" >\n <activities>' + pnDict[(personaName,'ACT')] + '</activities>\n  <attitudes>' + pnDict[(personaName,'ATT')] + '</attitudes>\n  <aptitudes>' + pnDict[(personaName,'APT')] + '</aptitudes>\n  <motivations>' + pnDict[(personaName,'MOT')] + '</motivations>\n  <skills>' + pnDict[(personaName,'SKI')] + '</skills>\n  <intrinsic>' + pnDict[(personaName,'INT')] + '</intrinsic>\n  <contextual>' + pnDict[(personaName,'CON')] + '</contextual>\n<persona_environment name=\"' + args.contextName + '\" is_direct="TRUE">\n  <persona_role name="Undefined" />\n  <narrative>Nothing stipulated</narrative>\n</persona_environment>\n</persona>\n\n'
  
  xmlBuf = xmlHdr + '\n' + pHdr + '\n' + xmlBuf + '\n</usability>\n</cairis_model>'
  xmlOut = open(args.modelFile,"w")
  xmlOut.write(xmlBuf)
  xmlOut.close()

if __name__ == '__main__':
  main()
