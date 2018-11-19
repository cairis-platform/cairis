#!/usr/bin/python
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
from cairis.core.Requirement import Requirement
from optparse import OptionParser
import os
import sys
from subprocess import check_output as cmd
from tempfile import mkstemp as make_tempfile
from .EnvironmentModel import EnvironmentModel
from .KaosModel import KaosModel
from .AssetModel import AssetModel
from .DataFlowDiagram import DataFlowDiagram
from .LocationModel import LocationModel
from .AssumptionPersonaModel import AssumptionPersonaModel
from cairis.core.armid import *
import requests

__author__ = 'Shamal Faily'

def dictToRows(dict):
  keys = list(dict.keys())
  keys.sort()
  rows = []
  for key in keys:
    rows.append((key,(dict[key]).description()))
  return rows

def listToString(l):
  s = ''
  noRows = len(l)
  for idx,row in enumerate(l):
    s += row
    if idx != (noRows-1):
      s += ', '
  return s

def paraText(txt):
  paraTxt = ''
  for c in txt:
    if c == '\n':
      paraTxt += '</para><para>'
    elif c == '&':
      c = '\&'
    else:
      paraTxt += c 
  return paraTxt

def listToRows(l):
  rows = []
  for row in l:
    rows.append((row.name(),paraText(row.description())))
  return rows

def listToPara(dList):
  paraTxt = ''
  for rowTxt in dList:
    paraTxt += '<para>' + rowTxt + '</para>'
  return paraTxt

def listToItems(dList):
  if len(dList) == 0:
    return 'None'
  else:
    paraTxt = '<itemizedlist>'
    for rowTxt in dList:
      paraTxt += '<listitem><para>' + rowTxt + '</para></listitem>'
    paraTxt += '</itemizedlist>'
    return paraTxt

def tupledListToItems(dList):
  if len(dList) == 0:
    return 'None'
  else:
    paraTxt = '<itemizedlist>'
    for tup in dList:
        paraTxt += '<listitem><para>' + tup[0] + ' : ' + tup[1] + '</para></listitem>'
    paraTxt += '</itemizedlist>'
    return paraTxt


def tuplesToPara(ts):
  paraTxt = ''
  for t in ts:
    paraTxt += '<para>' + t[0] + ' : ' + t[1] + '</para>' 
  return paraTxt

def buildImage(imageFile,caption):
  components = imageFile.split('.')
  if (len(components) != 2):
    format = 'SVG'
  else:
    format = components[1]
  if (format == 'jpg' or format == 'jpeg' or format == 'JPG' or format == 'JPEG'):
    imageFormat = 'JPG'
  else:
    imageFormat = 'SVG'
  b = Borg()
  txt = """
    <mediaobject>
      <imageobject>
        <imagedata align=\"left\" fileref=\"""" + imageFile + "\" format=\"" + imageFormat + "\" />" + """
      </imageobject>
      <caption><para>""" + caption + "</para></caption>" + """
    </mediaobject>"""
  return txt

def drawGraph(dotTxt,renderer,graphFile):
  fd, temp_abspath = make_tempfile(suffix='svg')
  temp_file = open(temp_abspath, 'w')
  temp_file.write(dotTxt)
  temp_file.close()
  os.close(fd)
  cmd([renderer, '-Tsvg', temp_abspath,'-o',graphFile + '.svg'])
  os.remove(temp_abspath)


def buildModel(p,envName,modelType,graphFile,locsName = ''):
  graph = None
  if (modelType == 'Risk'):
    model = EnvironmentModel(p.riskAnalysisModel(envName),envName,p,'dot')
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'Asset'):
    model = AssetModel(list(p.classModel(envName).values()),envName,db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'Goal'):
    model = KaosModel(list(p.goalModel(envName).values()),envName,'goal',db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'Obstacle'):
    model = KaosModel(list(p.obstacleModel(envName).values()),envName,'obstacle',db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'Task'):
    model = KaosModel(list(p.taskModel(envName).values()),envName,'task',db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'Responsibility'):
    model = KaosModel(list(p.responsibilityModel(envName).values()),envName,'responsibility',db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'DataFlow'):
    model = DataFlowDiagram(p.dataFlowDiagram(envName),envName,db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'PersonalDataFlow'):
    model = DataFlowDiagram(p.personalDataFlowDiagram(envName),envName,db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  elif (modelType == 'Locations'):
    riskOverlay = p.locationsRiskModel(locsName,envName)
    model = LocationModel(locsName,envName,riskOverlay,db_proxy=p)
    if (model.size() == 0):
      return False
    drawGraph(model.graph(),'dot',graphFile)
  return True

def buildAPModel(p,personaName,bvName,graphFile):
  b = Borg()
  graph = None
  proxy = p
  model = AssumptionPersonaModel(proxy.assumptionPersonaModel(personaName,bvName))
  if (model.size() == 0):
    return False
  drawGraph(model.graph(),'dot',graphFile)
  return True

def buildTable(tableId, tableTitle, colNames,colData,linkInd = 1):
  noOfCols = len(colNames)
  tgroupTxt = """
    <tgroup cols=\"""" + str(noOfCols) + "\">"
  tHeadTxt = """
      <thead>
        <row>"""
  for col in colNames:
    tgroupTxt += """
      <colspec align="left" />"""
    tHeadTxt += """
          <entry>""" + col + "</entry>"
  tHeadTxt += """
        </row>
      </thead>"""
  txt = """
  <table id=\"""" + tableId + "\"><title>" + tableTitle + "</title>"
  txt += tgroupTxt
  txt += tHeadTxt
  txt += """
      <tbody>"""
  for col in colData:
    txt += """
        <row>"""
    if (noOfCols == 1):
      if (linkInd == 1):
        txt += """
          <entry>"""
        txt += """
            <para><link linkend=\"""" + (str(col)).replace(" ","_") + "\">" + str(col) + "</link></para>"""
        txt += """
          </entry>"""
      else:
        txt += """
          <entry>""" + str(col) + "</entry>"
    else:
      for idx in range(0,noOfCols):
        if (linkInd == 1):
          txt += """
          <entry>"""
          txt += """
            <para><link linkend=\"""" + (str(col[idx])).replace(" ","_") + "\">" + str(col[idx]) + "</link></para>"""
          txt += """
          </entry>"""
        else:
          txt += """
          <entry>""" + str(col[idx]) + "</entry>"
    txt += """
        </row>
    """

  txt += """
      </tbody>
      </tgroup>
      </table>
  """
  return txt


def bookHeader(specName,contributors,revisions,logoFile = 'logo.jpg',logoFormat = 'JPG'):
  b = Borg()
  headerText = '''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook 4.1//EN" "'''+b.docBookDir+"""/docbookx.dtd" >
<book>
  <bookinfo>
    <title>""" + specName + "</title>"  + '''
    <mediaobject>
      <imageobject>
        <imagedata align=\"center\" fileref=\"''' + logoFile + "\" format=\"" + logoFormat + "\" />" + """
      </imageobject>
    </mediaobject>
  """
  if (len(contributors) > 0):
    headerText += """
    <authorgroup>"""
    for firstName,surname,affiliation,role in contributors:
      headerText += """
      <author role=\"""" + role + "\">" + """
        <firstname>""" + firstName + "</firstname>" + """
        <surname>""" + surname + "</surname>" + """
        <affiliation>
          <orgname>""" + affiliation + "</orgname>" + """
        </affiliation>
      </author>"""
    headerText += """
    </authorgroup>"""
  if (len(contributors) > 0):
    headerText += """
    <revhistory>"""
    for revNo,revDate,revDesc in revisions:
      headerText += """
      <revision>
        <revnumber>""" + str(revNo) + "</revnumber>" + """
        <date>""" + revDate + "</date>" + """
        <revremark>""" + revDesc + "</revremark>" + """
      </revision>"""
    headerText += """ 
    </revhistory>
  """ 
  headerText += """
  </bookinfo>
"""
  return headerText

def bookFooter():
  footerText = """
</book>\n
"""
  return footerText

def reqNotation():
  b = Borg()
  chapterText = ''' 
  <xi:include href="'''+b.configDir+"""/reqNotation.xml" xmlns:xi="http://www.w3.org/2003/XInclude"/> """ 
  return chapterText

def perNotation():
  b = Borg()
  chapterText = ''' 
  <xi:include href="'''+b.configDir+"""/perNotation.xml" xmlns:xi="http://www.w3.org/2003/XInclude"/> """ 
  return chapterText

def projectPurpose(pSettings):
  chapterTxt = """
  <chapter><title>Project Purpose</title>"""
  if (len(pSettings) == 0):
    return ""
  chapterTxt += """
    <section><title>Project Background</title>
      <para>""" + paraText(pSettings['Project Background']) + """</para>
    </section>
    <section><title>Project Goals</title>
      <para>""" + paraText(pSettings['Project Goals']) + """</para>
    </section>
  </chapter>
"""
  return chapterTxt

def dpiaNeed(p,pSettings):
  chapterTxt = """
  <chapter><title>Motivation for DPIA</title>"""
  if (len(pSettings) == 0):
    return ""
  chapterTxt += """
    <section><title>Background</title>
      <para>""" + paraText(pSettings['Project Background']) + """</para>
    </section>
    <section><title>Goals</title>
      <para>""" + paraText(pSettings['Project Goals']) + """</para>
    </section>
    <section><title>Scope</title>
      <para>""" + paraText(pSettings['Project Scope']) + """</para>
    </section>
  """
  rpFile = pSettings['Rich Picture']
  if (rpFile != ''):
    chapterTxt += richPictureSection(rpFile)

  environments = p.getEnvironments()
  if (environments != None):
    chapterTxt += """
    <section><title>Contexts of Use</title>
      <para>This section describes the environments within which the planned system will operate in.  Personal information, data flows, and privacy risks may vary based on these environments.</para>
"""
    for idx,environment in environments.items():
      environmentName = environment.name()
      chapterTxt +=  """
      <section id=\'""" + environmentName.replace(" ","_") + "\' ><title>" + environmentName + "</title>"
      chapterTxt += """
        <section><title>Description</title>
          <para>""" + paraText(environment.description()) + "</para>" + """
        </section>
        <section><title>Short Code</title>
          <para>""" + paraText(environment.shortCode()) + "</para>" + """
        </section>
        <section><title>Asset Values</title>"""
      avRows = []
      for avt in p.getValueTypes('asset_value',environmentName):
        avRows.append((avt.name(),avt.description()))
      chapterTxt += buildTable( (environmentName + "AssetValues").replace(" ","_") + "AssetValuesTable","",['Value','Description'],avRows,0)
      chapterTxt += """
        </section>
      </section>"""
    chapterTxt += """ 
    </section>
  </chapter>
"""
  return chapterTxt



def dpiaProcessing(p,docDir):
  chapterTxt = """
  <chapter><title>Processing</title>
    <section><title>Roles</title>
      <para>The following roles participate in processes and dataflows.  However, roles may also be fulfilled by potential attackers.</para>
"""
  roles = p.getRoles()
  if (roles == None):
    return ""
  componentRows = []
  for idx,role in roles.items():
    componentRows.append((role.name(),role.description()))
  chapterTxt += buildTable( "RolePropertiesTable"," Roles",['Name','Description'],componentRows,0) + """
    </section>
    <section><title>Nature of Processing</title>
      <section><title>Data Flow Diagram (DFDs)</title>
        <para>The DFDs in the following sub-sections illustrate the flow of personal data.</para>
  """
  envs = p.getEnvironments()
  modelType = 'PersonalDataFlow'
  for idx,env in envs.items():
    environmentName = env.name()
    modelFile = docDir + '/' + environmentName + modelType + 'Model'
    if (buildModel(p,environmentName,modelType,modelFile) == True):
      chapterTxt += """
        <section><title>""" + environmentName + "</title>" 
      chapterTxt += buildImage(modelFile,environmentName + ' ' + 'Data Flow Diagram')
      chapterTxt += """
        </section>"""
  chapterTxt += """
      </section>
      <section><title>Data Mapping Tables</title>
        <section><title>Processes</title>
  """
  chapterTxt += p.processDataMaps()
  chapterTxt += """
        </section>
        <section><title>Data Stores</title>
   """
  chapterTxt += p.datastoreDataMaps()
  chapterTxt += """
        </section>
      </section>
    </section>
    <section><title>Scope of Processing</title>
      <section><title>Overview</title>
        <para>The scope of processing is limited to the personal information described the following sub-sections.</para>
      </section>
    """
  chapterTxt = buildAssetContent(p,docDir,chapterTxt,True)
  chapterTxt += """
    </section>
    <section><title>Context of Processing</title>
      <section><title>Overview</title>
        <para>Our understanding of the data subjects is summarised by the personas below.</para>
      </section>
  """ 
  chapterTxt = buildPersonas(p,docDir,chapterTxt,True)
  chapterTxt += """
    </section>
    <section><title>Purpose of Processing</title>
      <para>Personal information is processed in the use cases specified below.</para>
   """
  chapterTxt = buildUseCases(p,docDir,chapterTxt)
  chapterTxt += """
      </section>
  </chapter>
  """
  return chapterTxt

def dpiaConsultation(p,docDir):
  chapterTxt = """
  <chapter><title>Consultation</title>
    <section><title>Overview</title>
      <para>Individual views were sought when creating the personas.  These are described in the sections that follow.</para>
    </section>
  """
  personas = p.getPersonas()
  for idx,persona in personas.items():
    personaName = persona.name()
    chapterTxt += """
     <section><title>""" + personaName + "</title>" + """
    """
    chapterTxt = buildPersonaRationale(p,personaName, docDir, chapterTxt)
    chapterTxt += """
     </section>
    """
  chapterTxt += """
  </chapter>"""
  return chapterTxt

def dpiaNecessity(p,docDir):
  chapterTxt = """
  <chapter><title>Necessity and Proportionality</title>
    <para>The table below describe the processes that handle personal data, and the goals that describe the necessity of this processing.</para>
  """
  envs = p.getEnvironments()
  for idx,env in envs.items():
    envName = env.name()
    lpTable = p.lawfulProcessingTable(envName)
    if (len(lpTable) > 0):
      chapterTxt += """
    <section><title>""" + envName + "</title>" + """
      """
      chapterTxt += buildTable( envName + "LPTable",envName + " Lawful Processing table",['Process','Personal Information','Goal','Definition','Fit Criterion','Issues'],lpTable,0) 
      chapterTxt += """
    </section>
      """
  chapterTxt += """
  </chapter>
  """
  return chapterTxt

def dpiaRisks(p,docDir):
  chapterTxt = """
  <chapter><title>Privacy Risks</title>

    <section><title>Vulnerabilities</title>
  """
  chapterTxt = buildVulnerabilities(p,chapterTxt,True)
  
  chapterTxt += """
    </section>
    <section><title>Attackers</title>
  """

  chapterTxt = buildAttackers(p,chapterTxt,True)
  chapterTxt += """
    </section>
    <section><title>Threat</title>
  """

  chapterTxt = buildThreats(p,chapterTxt,True)
  chapterTxt += """
    </section>
    <section><title>Risk</title>
  """

  chapterTxt = buildRisks(p,docDir,chapterTxt,True)
  chapterTxt += """
    </section>
  </chapter>
  """
  return chapterTxt

def dpiaMeasures(p):
  chapterTxt = """
  <chapter><title>Risk Response Measures</title>
  """

  chapterTxt = buildResponses(p,chapterTxt,True)

  chapterTxt += """
  </chapter>
  """
  return chapterTxt


def projectScope(pSettings,p,docDir):
  chapterTxt = """
  <chapter><title>Project Scope</title>"""
  if (len(pSettings) == 0):
    return ""
  chapterTxt += """
    <section><title>Overview</title>
      <para>""" + paraText(pSettings['Project Scope']) + "</para>" + """
    </section>
  """
  rpFile = pSettings['Rich Picture']
  if (rpFile != ''):
    chapterTxt += richPictureSection(rpFile)
  chapterTxt += """
  </chapter>
"""
  return chapterTxt


def mandatedConstraints(p):
  chapterTxt = """
  <chapter><title>Mandated Constraints</title>
"""
  objts = p.getDomainProperties()
  if (objts == None):
    return ""

  rows = []
  for idx,objt in objts.items():
    rows.append((objt.name(),objt.type(),objt.description()))
  chapterTxt += buildTable('DomainProperties','Constraints',['Name','Type','Description'],rows,0)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def namingConventions(p):
  chapterTxt = """
  <chapter><title>Naming Conventions</title>
"""
  entryRows = []
  objts = p.getDictionary()
  if (objts == None):
    return ""

  for name,defn in objts.items():
    entryRows.append((name,defn)) 
  chapterTxt += buildTable('projectNamingConventions','Naming Conventions',['Name','Definition'],entryRows,0)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def reqSection(typename,reqs):
  if (len(reqs) == 0): return ''
  else:
    reqSect = """
  <section><title>""" + typename + " Requirements</title>"
    reqSect += buildTable(typename + 'requirements','Requirements',['Id','Description','Priority','Rationale','Fit Criterion','Originator'],reqs,0)
  reqSect += """
  </section>"""
  return reqSect

def frReqSection(typename,reqs):
  if (len(reqs) == 0): return ''
  else:
    reqSect = """
  <section><title>""" + typename + " Requirements</title>"
    sections = list(reqs.keys())
    sections.sort()
    for section in sections:
      reqSect += """
    <section><title>""" + section + "</title>" 
      reqSect += buildTable(typename + section + 'requirements',section + ' ' + typename + ' Requirements',['Id','Description','Priority','Rationale','Fit Criterion','Originator'],reqs[section],0)
      reqSect += """
    </section>"""
  reqSect += """
  </section>"""
  return reqSect

def functionalRequirements(frDomDict,ddDomDict):
  chapterTxt = """
  <chapter><title>Functional Requirements</title>
"""
  chapterTxt += frReqSection('Functional',frDomDict)
  chapterTxt += frReqSection('Data',ddDomDict)
  chapterTxt += """
  </chapter>
"""
  return chapterTxt

def nonFunctionalRequirements(reqDict):
  chapterTxt = """
  <chapter><title>Nonfunctional Requirements</title>
"""
  chapterTxt += reqSection('Look and Feel',reqDict['Look and Feel'])
  chapterTxt += reqSection('Usability',reqDict['Usability'])
  chapterTxt += reqSection('Performance',reqDict['Performance'])
  chapterTxt += reqSection('Operational',reqDict['Operational'])
  chapterTxt += reqSection('Maintainability',reqDict['Maintainability'])
  chapterTxt += reqSection('Portability',reqDict['Portability'])
  chapterTxt += reqSection('Security',reqDict['Security'])
  chapterTxt += reqSection('Privacy',reqDict['Privacy'])
  chapterTxt += reqSection('Cultural and Political',reqDict['Cultural and Political'])
  chapterTxt += reqSection('Legal',reqDict['Legal'])
  chapterTxt += """
  </chapter>\n
"""
  return chapterTxt

def useCases(p,docDir):
  chapterTxt = """
  <chapter><title>Use Cases</title>
    <section><title>Overview</title>
      <para>This chapter describes, in more abstract terms than tasks, the interaction which takes place between roles and the system.  Use Cases operationalise goals and requirements, and each step in a use case may lead to possible exceptions.  These exceptions may be related to obstacles.</para>
    </section>
"""
  chapterTxt = buildUseCases(p,docDir,chapterTxt)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def buildUseCases(p,docDir,chapterTxt):
  ucs = p.getUseCases()
  if (ucs == None):
    return ""

  for idx,uc in ucs.items():
    ucName = uc.name()
    chapterTxt +=  """
    <section id=\"""" + ucName.replace(" ","_") + "\"><title>" + ucName + "</title>" + """ 
      <section><title>Actors</title>
        <itemizedlist>
    """
    for uca in uc.actors():
      chapterTxt += """
          <listitem><para>""" + uca + "</para></listitem>" + """
      """

    chapterTxt += """
        </itemizedlist>
      </section>
      <section><title>Description</title>
        <para>""" + paraText(uc.description()) + "</para>" + """
      </section>
      <section><title>Environments</title>"""
    for eProps in uc.environmentProperties():
      environmentName = eProps.name()
      envSteps = eProps.steps()
      stepRows = []
      for idx,step in enumerate(envSteps):
        stepNo = idx + 1
        stepRows.append((stepNo,step.text(),listToItems(step.exceptions())))  
      chapterTxt += """
        <section id=\"""" + (ucName + environmentName).replace(" ","_") + "UCEnv\"><title>" + environmentName + "</title>" + """
          <section id=\"""" + (ucName + environmentName).replace(" ","_") + "UCEnvPreCond\"><title>Pre-conditions</title>" + """
            <para>""" + eProps.preconditions() + "</para>" + """
          </section>
          <section id=\"""" + (ucName + environmentName).replace(" ","_") + "UCEnvSteps\"><title>Steps</title>" + """
             """
      chapterTxt += buildTable( (ucName + environmentName).replace(" ","_") + "UCStepsTable","Steps",['Step','Description','Exceptions'],stepRows,0) + """
          </section>
          <section id=\"""" + (ucName + environmentName).replace(" ","_") + "UCEnvPostCond\"><title>Post-conditions</title>" + """
            <para>""" + eProps.postconditions() + "</para>" + """
          </section>
        </section>"""
    chapterTxt += """
      </section>
    </section>
    """
  return chapterTxt


def tasks(p,docDir):
  chapterTxt = """
  <chapter><title>Tasks</title>
    <section><title>Overview</title>
      <para>This chapter describes the work tasks which the planned system will need to be designed for.  These tasks incorporate some level of interactivity with the planned system, and are carried out by the personas.  Tasks are also scored based on how usable these are to the personas who carry them out.</para>
    </section>
"""
  chapterTxt += modelSection(p,'Task',docDir)
  tasks = p.getTasks()
  if (tasks == None):
    return ""
  
  durationLookup = {}
  durationLookup['None'] = 'None'
  durationLookup['Low'] = 'Seconds'
  durationLookup['Medium'] = 'Minutes'
  durationLookup['High'] = 'Hours or longer' 

  frequencyLookup = {}
  frequencyLookup['High'] = 'Hourly or more'
  frequencyLookup['Medium'] = 'Daily - Weekly'
  frequencyLookup['Low'] = 'Monthly or less'
  frequencyLookup['None'] = 'None'

  for idx,task in tasks.items():
    taskName = task.name()
    chapterTxt +=  """
    <section id=\"""" + taskName.replace(" ","_") + "\"><title>" + taskName + "</title>" + """ 
      <section><title>Objective</title>
        <para>""" + paraText(task.objective()) + "</para>" + """
      </section>
      <section id=\"""" + taskName.replace(" ","_") + "Environments\"><title>Environments</title>"
 
    for eProps in task.environmentProperties():
      environmentName = eProps.name()
      chapterTxt += """
        <section id=\"""" + (taskName + environmentName).replace(" ","_") + "TaskProperties\"><title>" + environmentName + "</title>" + """
          <section id=\"""" + (taskName + environmentName).replace(" ","_") + "TaskDependencies\"><title>Dependencies</title>" + """
            <para>""" + eProps.dependencies() + "</para>" + """
          </section>
          <section id=\"""" + (taskName + environmentName).replace(" ","_") + "TaskPersonas\"><title>Personas</title>"
      tpRows = []
      for persona,duration,frequency,demands,goals in eProps.personas():
        tpRows.append((persona,durationLookup[duration],frequencyLookup[frequency],demands,goals))
      chapterTxt += buildTable( (taskName + environmentName).replace(" ","_") + "TaskPersonaTable","Personas",['Persona','Duration','Frequency','Demands','Goals'],tpRows,0) + """
          </section>
          <section id=\"""" + (taskName + environmentName).replace(" ","_") + "TaskAssets\"><title>Assets</title>"
      assetRows = []
      for asset in eProps.assets():
        assetRows.append( (asset))
      chapterTxt += buildTable( (taskName + environmentName).replace(" ","_") + "TaskAssetTable","Assets",['Asset'],assetRows,1) + """
          </section>
          <section id=\"""" + (taskName + environmentName).replace(" ","_") + "TaskNarrative\"><title>Narrative</title>" + """
            <para>""" + paraText(eProps.narrative()) + "</para>" + """
          </section>
        </section>""" 
    chapterTxt += """
      </section>
    </section>"""
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def characteristicsToRows(pcDict):
  pcList = list(pcDict.values())
  rows = []
  for pc in pcList:
    rows.append((pc.characteristic(),pc.qualifier(),tuplesToPara(pc.grounds()),tuplesToPara(pc.warrant()),listToPara(pc.backing()),tuplesToPara(pc.rebuttal())) )
  return rows

def personas(p,docDir):
  chapterTxt = """
  <chapter><title>Personas</title>
    <section><title>Overview</title>
      <para>This project needs to be situated for the personas below and the work they carry out.  Primary personas should be the main focus of analysis, but it is important not to forget the role other types of persona might play.</para>
    </section>
    <section><title>Roles</title>
      <para>Personas may fulfil one or more of the below roles.  However, roles may also be fulfilled by potential attackers.</para>
"""
  roles = p.getRoles()
  if (roles == None):
    return ""
  componentRows = []
  for idx,role in roles.items():
    componentRows.append((role.name(),role.description()))
  chapterTxt += buildTable( "RolePropertiesTable"," Roles",['Name','Description'],componentRows,0) + """
    </section>
    <section><title>Personas</title>
"""
  chapterTxt = buildPersonas(p,docDir,chapterTxt,False)
  chapterTxt += """
    </section>
  </chapter>
  """          
  return chapterTxt

def buildPersonas(p,docDir,chapterTxt,isDpia = False):

  b = Borg()
  personas = p.getPersonas()
  for idx,persona in personas.items():
    personaName = persona.name()
    chapterTxt += """
      <section id=\"""" + personaName.replace(" ","_") + "\"><title>" + personaName + "</title>"
    chapterTxt += buildImage(b.imageDir + "/" + persona.image(),persona.name())
    chapterTxt += """
        <section><title>Type</title>
          """ + "<para>" + paraText(persona.type()) + "</para>" + """
        </section>
        <section><title>Activities</title>
          """ + "<para>" + paraText(persona.activities()) + "</para>" + """
        </section>
        <section><title>Attitudes</title>
          """ + "<para>" + paraText(persona.attitudes()) + "</para>" + """
        </section>
        <section><title>Aptitudes</title>
          """ + "<para>" + paraText(persona.aptitudes()) + "</para>" + """
        </section>
        <section><title>Motivations</title>
          """ + "<para>" + paraText(persona.motivations()) + "</para>" + """
        </section>
        <section><title>Skills</title>
          """ + "<para>" + paraText(persona.skills()) + "</para>" + """
        </section>
        <section><title>Intrinsic</title>
          """ + "<para>" + paraText(persona.intrinsic()) + "</para>" + """
        </section>
        <section><title>Contextual</title>
          """ + "<para>" + paraText(persona.contextual()) + "</para>" + """
        </section>
    """

    for eProps in persona.environmentProperties():
      environmentName = eProps.name()
      chapterTxt += """
        <section><title>""" + environmentName + " Roles</title>" + """
          """
      envRows = [(listToString(eProps.roles()),eProps.directFlag())]
      chapterTxt += buildTable( personaName.replace(" ","_") + environmentName.replace(" ","_") + "PropertiesTable",personaName + " role attributes",['Roles','Direct/Indirect'],envRows,0) + """
        </section>
        <section><title>""" + environmentName + " Security Issues</title>" + """
          """ + "<para>" + paraText(eProps.narrative()) + "</para>" + """
        </section>
      """ 
    
    if (isDpia == False):
      chapterTxt = buildPersonaRationale(p,persona.name(), docDir, chapterTxt)
    chapterTxt += """   
      </section>"""
    return chapterTxt

def buildPersonaRationale(p,personaName,docDir,chapterTxt):
  chapterTxt += personaModelSection(p,personaName,docDir)

  docRefs = p.getPersonaDocumentReferences(personaName)
  if len(docRefs) > 0:
    chapterTxt += """
        <section><title>Document References</title>
    """
    chapterTxt += buildTable( personaName.replace(" ","_") + "DocumentReferencesTable",personaName + " Document References",['Reference','Document','Excerpt'],docRefs,0)
    chapterTxt += """
        </section>
    """

  edRefs = p.getPersonaExternalDocuments(personaName)
  if len(edRefs) > 0:
    chapterTxt += """
        <section><title>External Documents</title>
    """
    chapterTxt += buildTable( personaName.replace(" ","_") + "ExternalDocumentReferencesTable",personaName + " External Documents",['Document','Version','Authors','Date'],edRefs,0)
    chapterTxt += """
        </section>
    """

  conRefs = p.getPersonaConceptReferences(personaName)
  if len(conRefs) > 0:
    chapterTxt += """
      <section><title>Concept References</title>
    """
    chapterTxt += buildTable( personaName.replace(" ","_") + "ConceptReferencesTable",personaName + " Concept References",['Reference','Concept','Name','Excerpt'],conRefs,0)
    chapterTxt += """
        </section>
    """
  return chapterTxt

def attackers(p):
  chapterTxt = """
  <chapter><title>Attackers</title>
    <section><title>Overview</title>
      <para>This chapter describes the attackers the planned system needs to defend against.  These attackers will launch attacks, in the shape of threats, and take advantage of the vulnerabilities described by this specification.</para>
    </section>
  """
  chapterTxt = buildAttackers(p,chapterTxt)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def buildAttackers(p,chapterTxt,isPia = False):
  capabilityRows = listToRows(p.getValueTypes('capability'))
  motivationRows = listToRows(p.getValueTypes('motivation'))
  chapterTxt += """
    <section><title>Motivations</title>
    """ 
  chapterTxt += buildTable("AttackerMotivationTable","Attacker Motivations",['Motivation','Description'],motivationRows,0) + """
    </section>
    <section><title>Capability</title>
    """ 
  chapterTxt += buildTable("AttackerCapabilitiesTable","Attacker Capabilities",['Capability','Description'],capabilityRows,0) + """
    </section>
"""
  b = Borg()
  attackers = None
  if (isPia == True):
    attackers = p.getPersonalAttackers()
  else: 
    attackers = p.getAttackers()

  if (attackers == None):
    return ""
  for idx,attacker in attackers.items():
    attackerName = attacker.name()
    chapterTxt += """
    <section id=\"""" + attackerName.replace(" ","_") + "\"><title>" + attackerName + "</title>"
    chapterTxt += buildImage(b.imageDir + "/" + attacker.image(),attacker.name())
    chapterTxt += "<para>" + paraText(attacker.description()) + "</para>"

    aaRows = []
    for eProps in attacker.environmentProperties():
      environmentName = eProps.name()
      aaRows.append((environmentName,listToPara(eProps.roles()),listToPara(eProps.motives()),tuplesToPara(eProps.capabilities())))
    chapterTxt += buildTable( attackerName.replace(" ","_") + "PropertiesTable",attackerName + " environmental attributes",['Environment','Roles','Motives','Capabilities'],aaRows,0) + """
    </section>"""
  return chapterTxt

def objectiveText(p,environmentName,threatName,vulName):
  environmentId = p.getDimensionId(environmentName,'environment')
  threatId = p.getDimensionId(threatName,'threat')
  vulId = p.getDimensionId(vulName,'vulnerability')

  threatenedAssets = p.threatenedAssets(threatId,environmentId)
  vulnerableAssets = p.vulnerableAssets(vulId,environmentId)

  txt = 'Exploit vulnerabilities in '
  for idx,vulAsset in enumerate(vulnerableAssets):
    txt += vulAsset
    if (idx != (len(vulnerableAssets) -1)):
      txt += ','
  txt += ' to threaten '
  for idx,thrAsset in enumerate(threatenedAssets):
    txt += thrAsset
    if (idx != (len(threatenedAssets) -1)):
      txt += ','
  txt += '.'
  return txt

def misuseCases(p):
  chapterTxt = """
  <chapter><title>Misuse Cases</title>
    <section><title>Overview</title>
      <para>The Misuse Cases below describe how an attacker exploits each of the identified risks.</para>
    </section>
"""
  mcs = p.getMisuseCases()
  if mcs == None:
    return ""
 
  for idx,mc in mcs.items():
    mcName = mc.name()
    riskName = mc.risk()
    threatName,vulName = p.riskComponents(riskName) 
    summaryRows = [('Risk',riskName),('Threat',threatName),('Vulnerability',vulName)]
    chapterTxt +=  """
    <section id=\"""" + mcName.replace(" ","_") + "\"><title>" + mcName + "</title>" + """ 
      <section><title>Components</title>"""
    chapterTxt += buildTable( mcName.replace(" ","_") + "MisuseCaseComponentsTable","Components",['Component','Value'],summaryRows,0) + """
      </section>
      <section id=\"""" + mcName.replace(" ","_") + "Environments\"><title>Environments</title>"
    for eProps in mc.environmentProperties():
      environmentName = eProps.name()
      chapterTxt += """
        <section id=\"""" + (mcName + environmentName).replace(" ","_") + "MisuseCaseProperties\"><title>" + environmentName + "</title>" + """
          <section id=\"""" + (mcName + environmentName).replace(" ","_") + "MisuseCaseObjectives\"><title>Objective</title>" + """
            <para>""" + paraText(objectiveText(p,environmentName,threatName,vulName)) + "</para>" + """
          </section>
          <section id=\"""" + (mcName + environmentName).replace(" ","_") + "MisuseCaseNarrative\"><title>Narrative</title>" + """
            <para>""" + paraText(eProps.narrative()) + "</para>" + """
          </section>
        </section>""" 
    chapterTxt += """
      </section>
    </section>"""
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def assets(p,docDir):
  chapterTxt = """
  <chapter><title>Assets</title>
    <section><title>Overview</title>
      <para>This chapter describes the most important assets in, or associated with, the planned system.</para>
    </section>
  """
  chapterTxt = buildAssetContent(p,docDir,chapterTxt,False)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def buildAssetContent(p,docDir,chapterTxt,isPia = False):
  assetTypeRows = listToRows(p.getValueTypes('asset_type'))
  assetPropertyRows = listToRows(p.getValueTypes('asset_value'))
  chapterTxt += """
    <section><title>Asset Types</title>
    """ 
  chapterTxt += buildTable("AssetTypesTable","Asset Types",['Type','Description'],assetTypeRows,0) + """
    </section>
    <section><title>Asset Properties</title>
    """ 
  chapterTxt += buildTable("AssetPropertiesTable","Asset Properties",['Property','Description'],assetPropertyRows,0) + """
    </section>
"""

  if (isPia == False):
    chapterTxt += modelSection(p,'Asset',docDir)

  objts = None
  if (isPia == True):
    objts = p.getPersonalInformation()
  else:
    objts = p.getAssets()

  if (objts == None):
    return ""
  for idx,objt in objts.items():
    objtName = objt.name()
    chapterTxt += """
      <section id=\"""" + objtName.replace(" ","_") + "\"><title>" + objtName + "</title>"
    if (objt.critical() == True):
      chapterTxt += """
        <section><title>Critical Asset</title>
          <para>This asset has been designated as a critical asset.</para>
          <para>""" + objt.criticalRationale() + """</para> 
        </section>"""

    oAttributes = [('Type',objt.type()),('Description',paraText(objt.description())),('Significance',paraText(objt.significance()))]
    chapterTxt += buildTable( objtName + "AssetPropertiesTable",objtName + " attributes",['Attribute','Description'],oAttributes,0)
    oaRows = []
    for eProps in objt.environmentProperties():
      environmentName = eProps.name()
      oaRows.append((environmentName,tuplesToPara(objt.propertyList(environmentName,'',''))))
    chapterTxt += buildTable( objtName.replace(" ","_") + "PropertiesTable",objtName + " environmental attributes",['Environment','Security Properties'],oaRows,0)
    chapterTxt += """
      </section>"""
  return chapterTxt




def threats(p):
  chapterTxt = """
  <chapter><title>Threats</title>
    <section><title>Overview</title>
      <para>This chapter describes the threats which impact the planned system.</para>
    </section>
  """ 
  chapterTxt = buildThreats(p,chapterTxt)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt 

def buildThreats(p,chapterTxt,isPia = False):
  threatTypeRows = listToRows(p.getValueTypes('threat_type'))
  threatLhoodRows = listToRows(p.getValueTypes('likelihood'))
  threatPropertyRows = listToRows(p.getValueTypes('threat_value'))

  chapterTxt += """
    <section><title>Threat Types</title>
  """
  chapterTxt += buildTable("ThreatTypesTable","Threat Types",['Type','Description'],threatTypeRows,0) + """
    </section>
    <section><title>Threat Likelihoods</title>
    """
  chapterTxt += buildTable("ThreatLikelihoodsTable","Threat Likelihoods",['Type','Description'],threatLhoodRows,0) + """
    </section>
    <section><title>Threat Properties</title>
    """ 
  chapterTxt += buildTable("ThreatPropertiesTable","Threat Properties",['Property','Description'],threatPropertyRows,0) + """
    </section>
"""
  objts = None
  if (isPia == True):
    objts = p.getPersonalThreats()
  else:
    objts = p.getThreats()

  if (objts == None):
    return ""
  for idx,objt in objts.items():
    objtName = objt.name()
    chapterTxt += """
      <section id=\"""" + objtName.replace(" ","_") + "\"><title>" + objtName + "</title>"
    oAttributes = [('Type',objt.type()),('Method',paraText(objt.method()))]

    chapterTxt += buildTable( objtName + "ThreatPropertiesTable",objtName + " attributes",['Attribute','Description'],oAttributes,0)
    oaRows = []
    for eProps in objt.environmentProperties():
      environmentName = eProps.name()
      oaRows.append((environmentName,eProps.likelihood(),listToPara(eProps.attackers()),tuplesToPara(objt.propertyList(environmentName,'',''))))
    chapterTxt += buildTable( objtName.replace(" ","_") + "PropertiesTable",objtName + " environmental attributes",['Environment','Likelihood','Attackers','Security Properties'],oaRows,0) + """
      </section>"""
  return chapterTxt

def vulnerabilities(p):
  chapterTxt = """
  <chapter><title>Vulnerabilities</title>
    <section><title>Overview</title>
      <para>This chapter describes the vulnerabilities evident in this system.  These vulnerabilities may arise due to the nature of the environment, the system itself, or some aspect of the system's design.</para>
    </section>
  """
  chapterTxt = buildVulnerabilities(p,chapterTxt)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def buildVulnerabilities(p,chapterTxt,isPia = False):
  vulTypeRows = listToRows(p.getValueTypes('vulnerability_type'))
  vulSevRows = listToRows(p.getValueTypes('severity'))
  chapterTxt += """
    <section><title>Vulnerability Types</title>
    """ 
  chapterTxt += buildTable("VulnerabilityTypesTable","Vulnerability Types",['Type','Description'],vulTypeRows,0) + """
    </section>
    <section><title>Vulnerability Severities</title>
    """
  chapterTxt += buildTable("VulnerabilitySeveritiesTable","Vulnerability Severities",['Type','Description'],vulSevRows,0) + """
    </section>
"""

  objts = None
  if (isPia == True):
    objts = p.getPersonalVulnerabilities()
  else:
    objts = p.getVulnerabilities()

  if (objts == None):
    return ""
  for idx,objt in objts.items():
    objtName = objt.name()
    chapterTxt +=  """
    <section id=\"""" + objtName.replace(" ","_") + "\"><title>" + objtName + "</title>" + """ 
      <section><title>Type</title>
        <para>""" + objt.type() + "</para>" + """
      </section>
      <section><title>Description</title>
        <para>""" + objt.description() + "</para>" + """
      </section>
      <section id=\"""" + objtName.replace(" ","_") + "Environments\"><title>Environments</title>"
    for eProps in objt.environmentProperties():
      environmentName = eProps.name()
      chapterTxt += """
        <section id=\"""" + (objtName + environmentName).replace(" ","_") + "VulnerabilityProperties\"><title>" + environmentName + "</title>" + """
          <section id=\"""" + (objtName + environmentName).replace(" ","_") + "VulnerabilityPropertiesSeverity\"><title>Severity</title>" + """
            <para>""" + eProps.severity() + "</para>" + """
          </section>
          <section id=\"""" + (objtName + environmentName).replace(" ","_") + "VulnerabilityPropertiesAssets\"><title>Assets</title>" 
      chapterTxt += buildTable( (objtName + environmentName).replace(" ","_") + "VulnerabilityAssetsTable","Assets",['Asset'],eProps.assets(),1) + """
          </section>
        </section>""" 
    chapterTxt += """
      </section>
    </section>"""
  return chapterTxt

def modelSection(p,modelType,docDir):
  validModels = False
  txt = """
    <section><title>Models</title>"""
  envs = p.getEnvironments()
  for idx,env in envs.items():
    environmentName = env.name()
    modelFile = docDir + '/' + environmentName + modelType + 'Model'
    if (buildModel(p,environmentName,modelType,modelFile) == True):
      validModels = True
      txt += """
        <section><title>""" + environmentName + "</title>" 
      txt += buildImage(modelFile,environmentName + ' ' + modelType + ' Model')
      txt += """
        </section>"""
  txt += """
    </section>"""
  if (validModels == False):
    return ""
  else:
    return txt

def locationModelSection(p,locsName,docDir):
  validModels = False
  txt = """
      <section><title>""" + locsName + """</title>"""
  envs = p.getEnvironments()
  for idx,env in envs.items():
    environmentName = env.name()
    modelFile = docDir + '/' + locsName + environmentName + 'LocationsModel'
    if (buildModel(p,environmentName,'Locations',modelFile,locsName) == True):
      validModels = True
      txt += """
        <section><title>""" + environmentName + "</title>" 
      txt += buildImage(modelFile,environmentName + ' ' + 'Locations Model')
      txt += """
        </section>"""
  txt += """
      </section>"""
  if (validModels == False):
    return ""
  else:
    return txt


def personaModelSection(p,pName,docDir):
  validModels = False
  txt = """
    <section><title>""" + pName + """ Argumentation Model</title>
  """
  bvList = ['Activities','Attitudes','Aptitudes','Motivations','Skills','Environment Narrative']
  for bv in bvList:
    modelFile = docDir + '/' + pName + bv + 'Model'
    if (buildAPModel(p,pName,bv,modelFile) == True):
      validModels = True
      txt += """
        <section><title>""" + bv + "</title>"
      txt += buildImage(modelFile + ".svg",pName + ' ' + bv + ' Assumptions Model')
      txt += """
        </section>"""
  txt += """
    </section>"""
  if (validModels == False):
    return ""
  else: 
    return txt

def richPictureSection(rpFile):
  b = Borg()
  txt = """
    <section><title>Scope of work</title>
      <para>The following rich picture illustrates the scope of this document.</para>"""
  txt += buildImage(b.imageDir + "/" + rpFile,'Rich picture of the problem domain')
   
  txt += """
    </section>"""
  return txt

def goals(p,docDir):
  chapterTxt = """
  <chapter><title>Goals</title>
    <section><title>Overview</title>
      <para>This chapter describes the goals that the planned system needs to satisfy.  These are subsequently realised by requirements and tasks, but may be obstructed by obstacles.</para>
    </section>
"""
  chapterTxt += modelSection(p,'Goal',docDir)
  objts = p.getGoals()
  if (objts == None):
    return ""
  for idx,objt in objts.items():
    objtName = objt.name()
    chapterTxt +=  """
    <section id=\"""" + objtName.replace(" ","_") + "\"><title>" + objtName + "</title>"
    componentRows = []
    for eProps in objt.environmentProperties():
      environmentName = eProps.name()
      componentRows.append((environmentName,eProps.category(),eProps.priority(),eProps.definition(),eProps.fitCriterion(),eProps.issue()))
    chapterTxt += buildTable( objtName.replace(" ","_") + "PropertiesTable",objtName + " attributes",['Environment','Category','Priority','Definition','Fit','Issues'],componentRows,0) + """
    </section>"""
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def responsibilities(p,docDir):
  chapterTxt = """
  <chapter><title>Responsibilities</title>
    <section><title>Overview</title>
      <para>This chapter describes the dependencies between roles, and the various artifacts that roles are responsible for.</para>
    </section>
"""
  chapterTxt += modelSection(p,'Responsibility',docDir)
  deps = p.getDependencyTables()
  if (len(deps) == 0):
    chapterTxt += """
  </chapter>"""
    return chapterTxt 
  else:
    chapterTxt += """
    <section><title>Dependencies</title>
    """
    envs = list(deps.keys())
    envs.sort()
    for env in envs:
      chapterTxt += """
      <section><title>""" + env + """</title>
      """
      componentRows = deps[env]
      chapterTxt += buildTable( env.replace(" ","_") + "DependencyTable","Dependency",['Depender','Dependee','Type','Dependency','Rationale'],componentRows,0) + """
      </section>"""
    chapterTxt += """
    </section>"""
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def obstacles(p,docDir):
  chapterTxt = """
  <chapter><title>Obstacles</title>
    <section><title>Overview</title>
      <para>Obstacles are obstructions to goals.  These may be refined to possible threats and vulnerabilities.</para>
    </section>
"""
  chapterTxt += modelSection(p,'Obstacle',docDir)
  objts = p.getObstacles()
  if (objts == None):
    return ""
  for idx,objt in objts.items():
    objtName = objt.name()
    chapterTxt +=  """
    <section id=\"""" + objtName.replace(" ","_") + "\"><title>" + objtName + "</title>"
    componentRows = []
    for eProps in objt.environmentProperties():
      environmentName = eProps.name()
      componentRows.append((environmentName,eProps.category(),eProps.definition()))
    chapterTxt += buildTable( objtName.replace(" ","_") + "PropertiesTable",objtName + " attributes",['Environment','Category','Definition'],componentRows,0) + """
    </section>"""
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def risks(p,docDir):
  chapterTxt = """
  <chapter><title>Risks</title>
    <section><title>Overview</title>
      <para>This chapter describes the identified risks which impact the planned system. These arise when attackers launch attacks, manifested as threats, which expose a vulnerability.  A risk is only evident if both the threat and vulnerability exist in at least one environment.</para>
    </section>
  """
  chapterTxt += modelSection(p,'Risk',docDir)
  chapterTxt = buildRisks(p,docDir,chapterTxt)
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def buildRisks(p,docDir,chapterTxt,isPia = False):
  riskClassRows = listToRows(p.getValueTypes('risk_class'))
  chapterTxt += """
    <section><title>Risk categories</title>
  """
  chapterTxt += buildTable("RiskCategoriesTable","Risk Categories",['Category','Description'],riskClassRows,0) + """
    </section>
  """

  objts = None
  if (isPia == True):
    objts = p.getPersonalRisks()
  else:
    objts = p.getRisks()

  if (objts == None):
    return ""
  for idx,objt in objts.items():
    objtName = objt.name()
    chapterTxt +=  """
    <section id=\"""" + objtName.replace(" ","_") + "\"><title>" + objtName + "</title>" + """ 
      <section><title>Components</title>"""
    riskName = objt.name()
    threatName,vulName = p.riskComponents(riskName) 
    componentRows = [('Threat',threatName),('Vulnerability',vulName)]
    chapterTxt += buildTable( objtName.replace(" ","_") + "RiskComponentTable","Risks",['Property','Value'],componentRows,0) + """
      </section>
      <section id=\"""" + objtName.replace(" ","_") + "Environments\"><title>Environments</title>"
    for environmentName in p.riskEnvironments(threatName,vulName):
      chapterTxt += """
        <section id=\"""" + (objtName + environmentName).replace(" ","_") + "RiskProperties\"><title>" + environmentName + "</title>" + """
          <section id=\"""" + (objtName + environmentName).replace(" ","_") + "RiskPropertiesRating\"><title>Severity</title>" + """
            <para>""" + p.riskRating(threatName,vulName,environmentName) + "</para>" + """
          </section>
          <section id=\"""" + (objtName + environmentName).replace(" ","_") + "RiskPropertiesResponses\"><title>Mitigation Scores</title>" 
      riskScoreList = p.riskScore(threatName,vulName,environmentName,riskName)
      responseRows = []
      for idx,riskScore in enumerate(riskScoreList):
        responseRows.append( (riskScore[0],riskScore[1]) )
      chapterTxt += buildTable( (objtName + environmentName).replace(" ","_") + "RiskPropertiesResponsesTable","Responses",['Response','Score'],responseRows,0) + """
          </section>
        </section>""" 
    chapterTxt += """
      </section>
    </section>"""
  return chapterTxt

def sectionHeader(sectTitle):
  hdrTxt = """
      <section><title>""" + sectTitle + """</title>
  """ 
  return hdrTxt

def subSectionHeader(subSectTitle):
  hdrTxt = """
        <section><title>""" + subSectTitle + """</title>
  """ 
  return hdrTxt

def acceptSection(response):
  responseName = response.name()
  acceptTxt = """
        <section><title>""" + responseName + """</title>
          <section><title>Risk</title>
            <para>""" + response.risk() + """</para>
          </section>
          <section><title>Cost</title>
            <table id=\"""" + responseName.replace(" ","_") + "Costs\"" + """><title>""" + responseName + """ Costs</title>
              <tgroup cols="2">
                <colspec align="left" />
                <colspec align="left" />
              <thead>
                <row>
                  <entry>Environment</entry>
                  <entry>Cost</entry>
                </row>
              </thead>
              <tbody>
  """
  for cProps in response.environmentProperties():
    environmentName = cProps.name()
    acceptTxt += """
                 <row>
                   <entry>""" + environmentName + """</entry> 
                   <entry>""" + cProps.cost() + """</entry>
                 </row>\n"""
  acceptTxt += """ 
              </tbody>
              </tgroup>
            </table>
          </section>
          <section><title>Rationale</title>
            <table id=\"""" + responseName.replace(" ","_") + "Rationale\"" + """><title>""" + responseName + """ Rationale</title>
              <tgroup cols="2">
                <colspec align="left" />
                <colspec align="left" />
              <thead>
                <row>
                  <entry>Environment</entry>
                  <entry>Rationale</entry>
                </row>
              </thead>
              <tbody>
  """
  for cProps in response.environmentProperties():
    environmentName = cProps.name()
    acceptTxt += """
                <row>
                  <entry>""" + environmentName + """</entry> 
                  <entry>""" + cProps.description() + """</entry>
                </row>\n"""
  acceptTxt += """ 
              </tbody>
              </tgroup>
            </table>
          </section>\n
    """
  acceptTxt += """
        </section>\n
  """      
  return acceptTxt


def transferSection(response):
  responseName = response.name()
  transferTxt = """
        <section><title>""" + responseName + """</title>
          <section><title>Risk</title>
            <para>""" + response.risk() + """</para>
          </section>
          <section><title>Role</title>
            <table id=\"""" + responseName.replace(" ","_") + "Roles\"" + """><title>""" + responseName + """ Roles</title>
              <tgroup cols="2">
                <colspec align="left" />
                <colspec align="left" />
              <thead>
                <row>
                  <entry>Environment</entry>
                  <entry>Roles</entry>
                </row>
              </thead>
              <tbody>
  """
  for cProps in response.environmentProperties():
    environmentName = cProps.name()
    transferTxt += """
                 <row>
                   <entry>""" + environmentName + """</entry> 
                   <entry>""" 
    for role in cProps.roles():
      transferTxt += """
                     <para>""" + role[0] + " : " + role[1] + """</para>
                   </entry>
                 </row>\n"""
  transferTxt += """ 
              </tbody>
              </tgroup>
            </table>
          </section>
          <section><title>Rationale</title>
            <table id=\"""" + responseName.replace(" ","_") + "Rationale\"" + """><title>""" + responseName + """ Rationale</title>
              <tgroup cols="2">
                <colspec align="left" />
                <colspec align="left" />
              <thead>
                <row>
                  <entry>Environment</entry>
                  <entry>Rationale</entry>
                </row>
              </thead>
              <tbody>
  """
  for cProps in response.environmentProperties():
    environmentName = cProps.name()
    transferTxt += """
                <row>
                  <entry>""" + environmentName + """</entry> 
                  <entry>""" + cProps.description() + """</entry>
                </row>\n"""
  transferTxt += """ 
              </tbody>
              </tgroup>
            </table>
          </section>\n
    """
  transferTxt += """
        </section>\n
  """      
  return transferTxt

def mitigateSection(response):
  responseName = response.name()
  mitTxt = """
        <section><title>""" + responseName + """</title>
          <section><title>Risk</title>
            <para>""" + response.risk() + """</para>
          </section>
          <section><title>Type</title>
            <table id=\"""" + responseName.replace(" ","_") + "Type\"" + """><title>""" + responseName + """ Type</title>
              <tgroup cols="2">
                <colspec align="left" />
                <colspec align="left" />
              <thead>
                <row>
                  <entry>Environment</entry>
                  <entry>Roles</entry>
                </row>
              </thead>
              <tbody>
  """
  for cProps in response.environmentProperties():
    environmentName = cProps.name()
    mitTxt += """
                 <row>
                   <entry>""" + environmentName + """</entry> 
                   <entry>"""
    mitType = cProps.type()
    mitTxt += """
                     <para>""" + mitType
    if (mitType == 'Detect'):
      mitTxt += " : detected " + cProps.detectionPoint()
    elif (mitType == 'React'):
      mitTxt += " : detection mechanisms " + str(cProps.detectionMechanisms())
    
    mitTxt += "</para>" + """
                   
                   </entry>
                 </row>\n"""
  mitTxt += """ 
              </tbody>
              </tgroup>
            </table>
          </section>\n
    """
  mitTxt += """
        </section>\n
  """      
  return mitTxt




def responses(p):
  chapterTxt = """
  <chapter><title>Responses</title>
  """
  chapterTxt = buildResponses(p,chapterTxt)
  chapterTxt += """
  </chapter>
  """
  return chapterTxt

def buildResponses(p,chapterTxt,isPia = False):
  responses = None
  if (isPia == True):
    responses = p.getPersonalResponses()
  else:
    responses = p.getResponses()

  if (responses == None):
    return ""
  acceptTxt = ''
  transferTxt = ''
  mitigateTxt = ''
  

  for idx,response in responses.items():
    if (response.responseType() == 'Accept'):
      if (len(acceptTxt) == 0):
        acceptTxt += sectionHeader('Accept')
      acceptTxt += acceptSection(response)
    
    elif (response.responseType() == 'Transfer'):
      if (len(transferTxt) == 0):
        transferTxt += sectionHeader('Transfer')
      transferTxt += transferSection(response)
    else:
      if (len(mitigateTxt) == 0):
        mitigateTxt += sectionHeader('Mitigate')
      mitigateTxt += mitigateSection(response)

  if (len(acceptTxt) > 0):
    acceptTxt += """ 
      </section>\n"""
    chapterTxt += acceptTxt
  if (len(transferTxt) > 0):
    transferTxt += """ 
      </section>\n"""
    chapterTxt += transferTxt
  if (len(mitigateTxt) > 0):
    mitigateTxt += """ 
      </section>\n"""
    chapterTxt += mitigateTxt


  return chapterTxt

def countermeasures(p):
  chapterTxt = """
  <chapter><title>Countermeasures</title>
"""
  objts = p.getCountermeasures()
  if (objts == None):
    return ""
  for idx,objt in objts.items():
    objtName = objt.name()
    chapterTxt +=  """
    <section id=\"""" + objtName.replace(" ","_") + "\"><title>" + objtName + "</title>" + """ 
      <section><title>Type</title>
        <para>""" + objt.type() + "</para>" + """
      </section>
      <section><title>Description</title>
        <para>""" + objt.description() + "</para>" + """
      </section>
      <section id=\"""" + objtName.replace(" ","_") + "Environments\"><title>Environments</title>"
    for eProps in objt.environmentProperties():
      environmentName = eProps.name()
      chapterTxt += """
        <section id=\"""" + (objtName + environmentName).replace(" ","_") + "CountermeasureProperties\"><title>" + environmentName + "</title>" + """
          <section id=\"""" + (objtName + environmentName).replace(" ","_") + "CountermeasurePropertiesCost\"><title>Cost</title>" + """
            <para>""" + eProps.cost() + "</para>" + """
          </section>
          <section id=\"""" + (objtName + environmentName).replace(" ","_") + "CountermeasureSecurityProperties\"><title>Security Properties</title>" 
      chapterTxt += buildTable( (objtName + environmentName).replace(" ","_") + "CountermeasureRequirementsTable","Requirements",['Requirement'],eProps.requirements(),0)
      chapterTxt += buildTable( (objtName + environmentName).replace(" ","_") + "CountermeasureTargetTable","Targets",['Target','Effectiveness'],eProps.targets(),0)
      cmRows = []
      for p,v in objt.propertyList(environmentName,'',''):
        cmRows.append((p,v))
      chapterTxt += buildTable( (objtName + environmentName).replace(" ","_") + "CountermeasurePropertiesTable","Security Properties",['Property','Value'],cmRows,0) + """
          </section>
          <section id=\"""" + (objtName + environmentName).replace(" ","_") + "CountermeasureUsabilityProperties\"><title>Usability Properties</title>" 
      chapterTxt += buildTable( (objtName + environmentName).replace(" ","_") + "CountermeasureRolesTable","Roles",['Role'],eProps.roles(),1)
      chapterTxt += buildTable( (objtName + environmentName).replace(" ","_") + "CountermeasureTaskTable","",['Task','Persona','Duration','Frequency','Demands','Goals'],eProps.personas(),0) + """
          </section>
        </section>""" 
    chapterTxt += """
      </section>
    </section>"""
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def environments(p,docDir):
  environments = p.getEnvironments()
  if (environments == None):
    return ""
  chapterTxt = """
  <chapter><title>Environments</title>
    <section><title>Overview</title>
      <para>This paragraph describes the environments within which the planned system will operate in.  Properties associated with artifacts such as goals, assets, threats, and vulnerabilties may vary based on these environments, although the system needs to be designed to work in all possible environments.</para>
    </section>
"""
  for idx,environment in environments.items():
    environmentName = environment.name()
    chapterTxt +=  """
      <section id=\'""" + environmentName.replace(" ","_") + "\' ><title>" + environmentName + "</title>"
    chapterTxt += """
        <section><title>Description</title>
          <para>""" + paraText(environment.description()) + "</para>" + """
        </section>
        <section><title>Short Code</title>
          <para>""" + paraText(environment.shortCode()) + "</para>" + """
        </section>
        <section><title>Asset Values</title>"""
    avRows = []
    for avt in p.getValueTypes('asset_value',environmentName):
      avRows.append((avt.name(),avt.description()))
    chapterTxt += buildTable( (environmentName + "AssetValues").replace(" ","_") + "AssetValuesTable","",['Value','Description'],avRows,0)
    chapterTxt += """
        </section>"""
    if (len(environment.environments()) > 0):
      chapterTxt += """
      <section><title>Properties</title> 
        <table id=\"""" + environmentName.replace(" ","_") + "Properties\"" + """><title>""" + environmentName + """ Properties </title>
          <tgroup cols="2">
            <colspec align="left" />
            <colspec align="left" />
          <thead>
            <row>
              <entry>Property</entry>
              <entry>Value</entry>
            </row>
          </thead>
          <tbody>
            <row>
              <entry>Duplicate Property</entry>
              <entry><para>""" + environment.duplicateProperty()
      if (environment.overridingEnvironment() != ''):
        chapterTxt += ' : ' + environment.overridingEnvironment()
      chapterTxt += "</para></entry>"
      chapterTxt += """
            </row>
            <row>
              <entry>Environments</entry>
              <entry>"""
      for componentEnvironment in environment.environments():
        chapterTxt += """ 
                <para><link linkend=\"""" + componentEnvironment.replace(" ","_") + "\">" + componentEnvironment + "</link></para>"
      chapterTxt += """
              </entry>
            </row>
          </tbody>
          </tgroup>
        </table>
      </section>"""    
    chapterTxt += """
    </section>""" 
  chapterTxt += """
  </chapter>\n
"""
  return chapterTxt

def dependencies(p):
  chapterTxt = """
  <chapter><title>Dependencies</title>
"""
  dependencies = p.getDependencies()
  envDict = {}
  for idx,d in dependencies.items():
    if d.environment() not in envDict:
      t = (d.depender(),d.dependee(),d.dependency(),d.dependencyType(),d.rationale())
      envDict[d.environment()] = [t]
    else:
      envDict[d.environment()].append(t)
  envList = list(envDict.keys())
  envList.sort()
  for envName in envList:
    chapterTxt +=  """
      <section id=\'""" + envName.replace(" ","_") + "_Dependencies\' ><title>" + envName + "</title>" 
    chapterTxt += buildTable(envName + '_' + 'DepdendenciesTable'.replace(" ","_"),'Dependencies',['Depender','Dependee','Dependency','Type','Rationale'],envDict[envName],0)
    chapterTxt += """
      </section>""" 
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def dataflows(p,docDir):
  chapterTxt = """
  <chapter><title>Data Flows</title>
"""
  chapterTxt += modelSection(p,'DataFlow',docDir)
  dfs = p.getDataFlows()
  envDict = {}
  for idx,d in dfs.items():
    if d.environment() not in envDict:
      envDict[d.environment()] = [(d.name(),d.fromName(),d.fromType(),d.toName(),d.toType(),listToItems(d.assets()))]
    else:
      envDict[d.environment()].append((d.name(),d.fromName(),d.fromType(),d.toName(),d.toType(),listToItems(d.assets())))
  envList = list(envDict.keys())
  envList.sort()
  for envName in envList:
    chapterTxt +=  """
      <section id=\'""" + envName.replace(" ","_") + "_Dataflows\' ><title>" + envName + "</title>"
    chapterTxt += buildTable(envName + '_' + 'DataFlows'.replace(" ","_"),'Data Flows',['Name','From','Type','To','Type','Assets'],envDict[envName],0)

    chapterTxt += """
      </section>""" 
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt

def locations(p,docDir):
  chapterTxt = """
  <chapter><title>Locations</title>
    <section><title>Models</title>"""

  allLocs = p.getLocations()
  locsList = list(allLocs.keys())
  locsList.sort()
  for locs in locsList:
    chapterTxt += locationModelSection(p,locs,docDir)
  chapterTxt += """
    </section>
  """          
  for locsName in locsList:
    chapterTxt += """
      <section><title>""" + locs + """</title>
    """          
    locs = allLocs[locsName]
    locsRows = []
    for loc in locs.locations():
      locsRows.append((loc.name(),tupledListToItems(loc.assetInstances()),tupledListToItems(loc.personaInstances())))
    chapterTxt += buildTable(locsName + '_' + 'LocationTable'.replace(" ","_"),'Locations',['Location','Objects','People'],locsRows,0)
    chapterTxt += """
      </section>
    """          
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def architecture(p,docDir):
  chapterTxt = """
  <chapter><title>Architectural Patterns</title>
"""
  chapterTxt += """
  </chapter>
  """          
  return chapterTxt


def buildReqSpecBody(p,sectionFlags,docDir):
  contributors = p.getContributors()
  revisions = p.getRevisions()

  pSettings = p.getProjectSettings()
  specName = pSettings['Project Name'] + ' Requirements Specification'

  specDoc = bookHeader(specName,contributors,revisions)
  specDoc += reqNotation()
  
  if (sectionFlags[REQDOC_PROJECTPURPOSE_ID]):
    specDoc += projectPurpose(pSettings)
  if (sectionFlags[REQDOC_PROJECTSCOPE_ID]):
    specDoc += projectScope(pSettings,p,docDir)
  if (sectionFlags[REQDOC_ENVIRONMENTS_ID]):
    specDoc += environments(p,docDir)
  if (sectionFlags[REQDOC_STAKEHOLDERS_ID]):
    specDoc += personas(p,docDir)
  if (sectionFlags[REQDOC_MANDATEDCONSTRAINTS_ID]):
    specDoc += mandatedConstraints(p)
  if (sectionFlags[REQDOC_NAMINGCONVENTIONS_ID]):
    specDoc += namingConventions(p)
  if (sectionFlags[REQDOC_ASSETS_ID]):
    specDoc += assets(p,docDir)
  if (sectionFlags[REQDOC_TASKS_ID]):
    specDoc += tasks(p,docDir)
  if (sectionFlags[REQDOC_USECASES_ID]):
    specDoc += useCases(p,docDir)
  if (sectionFlags[REQDOC_DATAFLOWS_ID]):
    specDoc += dataflows(p,docDir)
  if (sectionFlags[REQDOC_GOALS_ID]):
    specDoc += goals(p,docDir)
  if (sectionFlags[REQDOC_RESPONSIBILITIES_ID]):
    specDoc += responsibilities(p,docDir)
  if (sectionFlags[REQDOC_OBSTACLES_ID]):
    specDoc += obstacles(p,docDir)
  if (sectionFlags[REQDOC_VULNERABILITIES_ID]):
    specDoc += vulnerabilities(p)
  if (sectionFlags[REQDOC_ATTACKERS_ID]):
    specDoc += attackers(p)
  if (sectionFlags[REQDOC_THREATS_ID]):
    specDoc += threats(p)
  if (sectionFlags[REQDOC_RISKS_ID]):
    specDoc += risks(p,docDir)
  if (sectionFlags[REQDOC_LOCATIONS_ID]):
    specDoc += locations(p,docDir)
  if (sectionFlags[REQDOC_MISUSECASES_ID]):
    specDoc += misuseCases(p)
  if (sectionFlags[REQDOC_RESPONSES_ID]):
    specDoc += responses(p)
  if (sectionFlags[REQDOC_COUNTERMEASURES_ID]):
    specDoc += countermeasures(p)

  if (sectionFlags[REQDOC_REQUIREMENTS_ID]):
    reqs = p.getOrderedRequirements()
    reqDict = {}
    reqDict['Functional'] = []
    reqDict['Data'] = []
    reqDict['Look and Feel'] = []
    reqDict['Usability'] = []
    reqDict['Performance'] = []
    reqDict['Operational'] = []
    reqDict['Maintainability'] = []
    reqDict['Portability'] = []
    reqDict['Security'] = []
    reqDict['Privacy'] = []
    reqDict['Cultural and Political'] = []
    reqDict['Legal'] = []
    frDomDict = {}
    ddDomDict = {}
    for val in reqs:
      colData = (val.label(),val.description(),val.priority(),val.rationale(),val.fitCriterion(),val.originator())
      reqType = val.type()
      reqDict[reqType].append(colData)
      if (reqType == 'Functional'):
        reqDomain = val.asset()
        if (reqDomain not in frDomDict):
          frDomDict[reqDomain] = []
        frDomDict[reqDomain].append(colData)
      if (reqType == 'Data'):
        reqDomain = val.asset()
        if (reqDomain not in ddDomDict):
          ddDomDict[reqDomain] = []
        ddDomDict[reqDomain].append(colData)

    specDoc += functionalRequirements(frDomDict,ddDomDict)
    specDoc += nonFunctionalRequirements(reqDict)

  if (sectionFlags[REQDOC_DEPENDENCIES_ID]):
    specDoc += dependencies(p)
  if (sectionFlags[REQDOC_ARCHITECTURALPATTERNS_ID]):
    specDoc += architecture(p,docDir)
  return specDoc

def buildPersonasBody(p,sectionFlags,docDir):
  contributors = p.getContributors()
  revisions = p.getRevisions()
  pSettings = p.getProjectSettings()
  specName = pSettings['Project Name'] + ' Personas'
  specDoc = bookHeader(specName,contributors,revisions)
  specDoc += perNotation()
  
  if (sectionFlags[PERDOC_PROJECTPURPOSE_ID]):
    specDoc += projectPurpose(pSettings)
  if (sectionFlags[PERDOC_PROJECTSCOPE_ID]):
    specDoc += projectScope(pSettings,p,docDir)
  if (sectionFlags[PERDOC_ENVIRONMENTS_ID]):
    specDoc += environments(p,docDir)
  if (sectionFlags[PERDOC_STAKEHOLDERS_ID]):
    specDoc += personas(p,docDir)
  if (sectionFlags[PERDOC_TASKS_ID]):
    specDoc += tasks(p,docDir)
  return specDoc

def buildDPIABody(p,sectionFlags,docDir):
  contributors = p.getContributors()
  revisions = p.getRevisions()
  pSettings = p.getProjectSettings()
  specName = pSettings['Project Name'] + ' Data Protection Impact Assessment'
  specDoc = bookHeader(specName,contributors,revisions)

  if (sectionFlags[DPIA_NEED_ID]):
    specDoc += dpiaNeed(p,pSettings)
  if (sectionFlags[DPIA_PROCESSING_ID]):
    specDoc += dpiaProcessing(p,docDir)
  if (sectionFlags[DPIA_CONSULTATION_ID]):
    specDoc += dpiaConsultation(p,docDir)
  if (sectionFlags[DPIA_NECESSITY_ID]):
    specDoc += dpiaNecessity(p,docDir)
  if (sectionFlags[DPIA_RISKS_ID]):
    specDoc += dpiaRisks(p,docDir)
  if (sectionFlags[DPIA_MEASURES_ID]):
    specDoc += dpiaMeasures(p)
  return specDoc


def build(dbProxy,docType,sectionFlags,typeFlags,fileName,docDir):
  p = dbProxy

  if (docType == 'Requirements'):
    specDoc = buildReqSpecBody(p,sectionFlags,docDir)
  elif (docType == 'Personas'):
    specDoc = buildPersonasBody(p,sectionFlags,docDir)
  else:
    specDoc = buildDPIABody(p,sectionFlags,docDir)

  specDoc += bookFooter()

  docFile = docDir + '/' + fileName + '.xml'
  f = open(docFile,'w')
  f.write(specDoc)
  f.close()
  
  b = Borg()
  if(b.docker == True):
    requestString = "http://cairis-latex:5000/latexApi/fileName/{}".format(fileName)
    requests.post(requestString, data={'docDir': docDir, 'docFile': docFile, 'typeFlags':typeFlags}) 
  else:
    if (typeFlags[DOCOPT_HTML_ID]):
      htmlGenCmd = 'docbook2html -o ' + docDir + ' ' + docFile
      os.system(htmlGenCmd)
    if (typeFlags[DOCOPT_RTF_ID]):
      rtfGenCmd = 'docbook2rtf -o ' + docDir + ' ' + docFile
      os.system(rtfGenCmd)
    if (typeFlags[DOCOPT_PDF_ID]):
      pdfGenCmd = 'dblatex --param=table.in.float="0" -o  ' + docDir + '/' + fileName + '.pdf '  + docFile
      os.system(pdfGenCmd)
      