#!/usr/bin/python
import string

if __name__ == '__main__':
  xmlHdr = '<?xml version="1.0"?>\n<!DOCTYPE usability PUBLIC "-//CAIRIS//DTD USABILITY 1.0//EN" "http://cairis.org/dtd/usability.dtd">\n\n<usability>\n\n'
  xmlBuf = ''

  cf = open('Concepts.csv',"r")
  conceptDict = {}
  for l in cf.readlines():
    l = string.strip(l)
    ce = l.split(',')
    edCode = ce[0]
    edName = ce[1] + ' GT concept'
    conceptDict[edCode] = edName
    xmlBuf += '<external_document name=\"' + edName + '\" version=\"1.0\" date=\"April 2015\" authors=\"Shamal Faily\">\n  <description>' + edName + '</description>\n</external_document>\n'
  cf.close()
  xmlBuf += '\n'
  pf = open('Propositions.csv',"r")
  propDict = {}
  for l in pf.readlines():
    l = string.strip(l)
    pe = l.split(',')
    pId = pe[0]
    edCode,pNo = pId.split('-')
    docName = conceptDict[edCode]
    pName = pe[1]
    pDesc = pe[2]
    propDict[pId] = (pName,pDesc)
    xmlBuf += '<document_reference name=\"' + pName + '\" contributor=\"Shamal Faily\" document=\"' + docName + '\">\n  <excerpt>' + pDesc + '</excerpt>\n</document_reference>\n'

  pf.close()
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
  
  pcf = open('Characteristics.csv',"r")
  for l in pcf.readlines():
    l = string.strip(l)
    pce = l.split(',')
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

  pHdr = ''
  for personaName in personaNames:
    pHdr += '<persona name=\"' + personaName + '\" type=\"Primary\" assumption_persona=\"FALSE\" image=\"\" >\n <activities>None</activities>\n  <attitudes>None</attitudes>\n  <aptitudes>None</aptitudes>\n  <motivations>None</motivations>\n  <skills>None</skills>\n  <intrinsic>None</intrinsic>\n  <contextual>None</contextual>\n</persona>\n\n'     
  
  xmlBuf = xmlHdr + '\n' + pHdr + '\n' + xmlBuf + '\n</usability>'
  xmlOut = open('delme.xml',"w")
  xmlOut.write(xmlBuf)
  xmlOut.close()
