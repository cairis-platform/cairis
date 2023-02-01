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


from .Borg import Borg
import MySQLdb
from sqlalchemy.exc import OperationalError, ProgrammingError, DataError, IntegrityError
from . import RequirementFactory
from .Environment import Environment
from .ARM import *
from MySQLdb._exceptions import DatabaseError, IntegrityError
from . import Attacker
from . import Asset
from . import Threat
from . import Vulnerability
from . import Persona
from . import MisuseCase
from . import Task
from . import Risk
from . import Response
from . import ClassAssociation
from .ObjectSummary import ObjectSummary
from .AttackerParameters import AttackerParameters
from .PersonaParameters import PersonaParameters
from .GoalParameters import GoalParameters
from .ObstacleParameters import ObstacleParameters
from .AssetParameters import AssetParameters
from .TemplateAssetParameters import TemplateAssetParameters
from .TemplateGoalParameters import TemplateGoalParameters
from .TemplateRequirementParameters import TemplateRequirementParameters
from .SecurityPatternParameters import SecurityPatternParameters
from .ThreatParameters import ThreatParameters
from .VulnerabilityParameters import VulnerabilityParameters
from .RiskParameters import RiskParameters
from .ResponseParameters import ResponseParameters
from .RoleParameters import RoleParameters
from . import ObjectFactory
from .TaskParameters import TaskParameters
from .MisuseCaseParameters import MisuseCaseParameters
from .DomainPropertyParameters import DomainPropertyParameters
from . import Trace
from cairis.core.armid import *
from .DotTraceParameters import DotTraceParameters
from .EnvironmentParameters import EnvironmentParameters
from .Target import Target
from .AttackerEnvironmentProperties import AttackerEnvironmentProperties
from .AssetEnvironmentProperties import AssetEnvironmentProperties
from .ThreatEnvironmentProperties import ThreatEnvironmentProperties
from .VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from .AcceptEnvironmentProperties import AcceptEnvironmentProperties
from .TransferEnvironmentProperties import TransferEnvironmentProperties
from .MitigateEnvironmentProperties import MitigateEnvironmentProperties
from .CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties
from .CountermeasureParameters import CountermeasureParameters
from .PersonaEnvironmentProperties import PersonaEnvironmentProperties
from .TaskEnvironmentProperties import TaskEnvironmentProperties
from .MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from .RoleEnvironmentProperties import RoleEnvironmentProperties
from .ClassAssociationParameters import ClassAssociationParameters
from .GoalAssociationParameters import GoalAssociationParameters
from .DependencyParameters import DependencyParameters
from .GoalEnvironmentProperties import GoalEnvironmentProperties
from .ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from .ValueTypeParameters import ValueTypeParameters
from .ExternalDocumentParameters import ExternalDocumentParameters
from .InternalDocumentParameters import InternalDocumentParameters
from .CodeParameters import CodeParameters
from .MemoParameters import MemoParameters
from .DocumentReferenceParameters import DocumentReferenceParameters
from .ConceptReferenceParameters import ConceptReferenceParameters
from .PersonaCharacteristicParameters import PersonaCharacteristicParameters
from .TaskCharacteristicParameters import TaskCharacteristicParameters
from .UseCaseParameters import UseCaseParameters
from .UseCase import UseCase
from .UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from .UseCaseParameters import UseCaseParameters
from .Step import Step
from .Steps import Steps
from .ReferenceSynopsis import ReferenceSynopsis
from .ReferenceContribution import ReferenceContribution
from .ConceptMapAssociationParameters import ConceptMapAssociationParameters
from .ComponentViewParameters import ComponentViewParameters;
from .ComponentParameters import ComponentParameters;
from .ConnectorParameters import ConnectorParameters;
from .WeaknessTarget import WeaknessTarget
from .ImpliedProcess import ImpliedProcess
from .ImpliedProcessParameters import ImpliedProcessParameters
from .Location import Location
from .Locations import Locations
from .LocationsParameters import LocationsParameters
from .DataFlow import DataFlow
from .DataFlowParameters import DataFlowParameters
from .TrustBoundary import TrustBoundary
from .ValidationResult import ValidationResult
from .GoalContribution import GoalContribution
from .TaskContribution import TaskContribution
from .UserStory import UserStory
from .PolicyStatement import PolicyStatement
from cairis.tools.PseudoClasses import RiskRating
import string
import os
from numpy import *
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
import sys
from base64 import b64encode
from .dba import canonicalDbUser, canonicalDbName, createDatabaseSchema, createDefaults, createDatabaseAndPrivileges, databases

__author__ = 'Shamal Faily, Robin Quetin, Nathan Jenkins'

class MySQLDatabaseProxy:
  def __init__(self, host=None, port=None, user=None, passwd=None, db=None):
    b = Borg()
    if (user is None or passwd is None or db is None):
      user = b.dbUser
      passwd = b.dbPasswd
      db = b.dbName
    host = b.dbHost
    port = b.dbPort

    try:
      dbEngine = create_engine('mysql+mysqldb://' + user + ':' + passwd + '@' + host + ':' + str(port) + '/' + db + '?charset=utf8mb4')
      self.conn = scoped_session(sessionmaker(bind=dbEngine))
      self.conn.execute(text("set session max_sp_recursion_depth = 255"))
    except OperationalError as e:
      exceptionText = 'MySQL error connecting to the CAIRIS database ' + db + ' on host ' + host + ' at port ' + str(port) + ' with user ' + user + ' (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      id,msg = e
      exceptionText = 'MySQL error connecting to the CAIRIS database ' + db + ' on host ' + host + ' at port ' + str(port) + ' with user ' + user + ' (id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 
    self.theDimIdLookup, self.theDimNameLookup = self.buildDimensionLookup()

  def reconnect(self,closeConn = True,session_id = None):
    b = Borg()
    try:
      if (closeConn) and self.conn.connection().connection.open:
        self.conn.close()

      if b.runmode == 'web':
        ses_settings = b.get_settings(session_id)
        dbUser = ses_settings['dbUser']
        dbPasswd = ses_settings['dbPasswd']
        dbHost = ses_settings['dbHost']
        dbPort = ses_settings['dbPort']
        dbName = ses_settings['dbName']
        dbEngine = create_engine('mysql+mysqldb://' + dbUser+':' + dbPasswd+'@' + dbHost+':' + str(dbPort)+'/' + dbName + '?charset=utf8mb4')
        self.conn = scoped_session(sessionmaker(bind=dbEngine))
      elif b.runmode == 'desktop':
        dbEngine = create_engine('mysql+mysqldb://' + b.dbUser+':' + b.dbPasswd+'@' + b.dbHost+':' + str(b.dbPort)+'/' + b.dbName + '?charset=utf8mb4')
        self.conn = scoped_session(sessionmaker(bind=dbEngine))
      else:
        raise RuntimeError('Run mode not recognized')
      self.conn.execute(text("set session max_sp_recursion_depth = 255"))

    except OperationalError as e:
      exceptionText = 'MySQL error re-connecting to the CAIRIS database: ' + format(e)
      raise DatabaseProxyException(exceptionText) 
    except ProgrammingError as e:
      exceptionText = 'MySQL error re-connecting to the CAIRIS database: ' + format(e)
      raise DatabaseProxyException(exceptionText) 
    except IntegrityError as e:
      exceptionText = 'MySQL error re-connecting to the CAIRIS database: ' + format(e)
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      exceptionText = 'MySQL error re-connecting to the CAIRIS database: ' + format(e)
      raise DatabaseProxyException(exceptionText) 
    self.theDimIdLookup, self.theDimNameLookup = self.buildDimensionLookup()


  def buildDimensionLookup(self):
    dimRows = self.responseList('call traceDimensions()',{},'MySQL error building trace dimension lookup tables')
    idLookup  = {}
    nameLookup = {}
    for dimId,dimName in dimRows:
      idLookup[dimId] = dimName
      nameLookup[dimName] = dimId
    return (idLookup, nameLookup)
    
  def close(self):
    try:
      self.conn.remove()
    except ProgrammingError:
      pass

  def getRequirements(self,constraintId = '',isAsset = 1):
    reqRows = self.responseList('call getRequirements(:id,:isAs)',{'id':constraintId,'isAs':isAsset},'MySQL error getting requirements')
    reqDict = {}
    for reqLabel, reqId, reqName, reqDesc, priority, rationale, fitCriterion, originator, reqVersion, reqType, reqDomain,domainType in reqRows:
      r = RequirementFactory.build(reqId,reqLabel,reqName,reqDesc,priority,rationale,fitCriterion,originator,reqType,reqDomain,domainType,reqVersion)
      reqDict[reqName] = r
    return reqDict

  def getRequirement(self,reqId):
    reqRows = self.responseList('call getRequirement(:id)',{'id':reqId},'MySQL error getting requirement')
    reqDict = {}
    for reqLabel, reqId, reqName, reqDesc, priority, rationale, fitCriterion, originator, reqVersion, reqType, reqDomain, domainType in reqRows:
      return RequirementFactory.build(reqId,reqLabel,reqName,reqDesc,priority,rationale,fitCriterion,originator,reqType,reqDomain,domainType,reqVersion)

  def getOrderedRequirements(self,constraintId = '',isAsset = True):
    reqRows = self.responseList('call getRequirements(:id,:isAs)',{'id':constraintId,'isAs':isAsset},'MySQL error getting requirements')
    reqList = []
    for reqLabel, reqId, reqName, reqDesc, priority, rationale, fitCriterion, originator, reqVersion, reqType, reqDomain, domainType in reqRows:
      r = RequirementFactory.build(reqId,reqLabel,reqName,reqDesc,priority,rationale,fitCriterion,originator,reqType,reqDomain,domainType,reqVersion)
      reqList.append(r)
    return reqList

    
  def newId(self):
    return self.responseList('call newId()',{},'MySQL error getting new identifier')[0]

  def commitDatabase(self,session):
    try:
      session.commit()
      session.close()
    except OperationalError as e:
      exceptionText = 'Commit error (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      id,msg = e
      exceptionText = 'Commit error (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateDatabase(self,callTxt,argDict,errorTxt,session = None,doCommit = True):
    try:
      if (session == None):
        session = self.conn()
      session.execute(text(callTxt),argDict)
      if (doCommit):
        session.commit()
        session.close()
        return None
      else:
        return session
    except OperationalError as e:
      exceptionText = 'Update error (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except IntegrityError as e:
      exceptionText = 'Update error (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      id,msg = e
      exceptionText = 'Update error (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addRequirement(self,req,assetName,isAsset = True):
    req.validate()
    self.updateDatabase('call addRequirement(:lbl,:id,:vers,:name,:desc,:rationale,:origin,:fCrit,:priority,:type,:asName,:isAs)',{'lbl':req.label(),'id':req.id(),'vers':req.version(),'name':req.name(),'desc':req.description(),'rationale':req.rationale(),'origin':req.originator(),'fCrit':req.fitCriterion(),'priority':req.priority(),'type':req.type(),'asName':assetName,'isAs':isAsset},'MySQL error adding new requirement ' + str(req.id()))

  def updateRequirement(self,req):
    req.validate()
    self.updateDatabase('call updateRequirement(:lbl,:id,:vers,:name,:desc,:rationale,:origin,:fCrit,:priority,:type)',{'lbl':req.label(),'id':req.id(),'vers':req.version(),'name':req.name(),'desc':req.description(),'rationale':req.rationale(),'origin':req.originator(),'fCrit':req.fitCriterion(),'priority':req.priority(),'type':req.type()},'MySQL error updating requirement ' + str(req.id()))

  def addValueTensions(self,envId,tensions):
    for vtKey in tensions:
      spValue = vtKey[0]
      prValue = vtKey[1]
      vt = tensions[vtKey]
      vtValue = vt[0]
      vtRationale = vt[1]
      self.addValueTension(envId,spValue,prValue,vtValue,vtRationale)

  def addValueTension(self,envId,spId,prId,tId,tRationale):
    self.updateDatabase('call addValueTension(:env,:sp,:pr,:tId,:rationale)',{'env':envId,'sp':spId,'pr':prId,'tId':tId,'rationale':tRationale},'MySQL error adding value tension for environment id ' + str(envId))

  def addEnvironment(self,parameters):
    parameters.validate()
    environmentId = self.newId()
    environmentName = parameters.name()
    environmentShortCode = parameters.shortCode()
    environmentDescription = parameters.description()
    session = self.updateDatabase('call addEnvironment(:id,:name,:sc,:desc)',{'id':environmentId,'name':environmentName,'sc':environmentShortCode,'desc':environmentDescription},'MySQL error adding environment',None,False)
    if (len(parameters.environments()) > 0):
      for c in parameters.environments():
        self.updateDatabase('call addCompositeEnvironment(:id,:c)',{'id':environmentId,'c':c},'MySQL error adding composite environment',session,False)
      self.addCompositeEnvironmentProperties(environmentId,parameters.duplicateProperty(),parameters.overridingEnvironment(),session)
      self.commitDatabase(session)
    assetValues = parameters.assetValues()
    if (assetValues != None):
      for v in assetValues: self.updateValueType(v)
    self.addValueTensions(environmentId,parameters.tensions())
    self.commitDatabase(session)

  def addCompositeEnvironmentProperties(self,environmentId,duplicateProperty,overridingEnvironment,session = None):
    self.updateDatabase('call addCompositeEnvironmentProperties(:id,:dp,:oe)',{'id':environmentId,'dp':duplicateProperty,'oe':overridingEnvironment},'MySQL error adding duplicate properties for environment id ' + str(environmentId),session,False)

  def riskEnvironments(self,threatName,vulName):
    return self.responseList('call riskEnvironments(:thr,:vul)',{'thr':threatName,'vul':vulName},'MySQL error getting environments associated with threat ' + threatName + ' and vulnerability ' + vulName)

  def riskEnvironmentsByRisk(self,riskName):
    return self.responseList('call riskEnvironmentsByRisk(:risk)',{'risk':riskName},'MySQL error getting environments associated with risk ' + riskName)

  def updateEnvironment(self,parameters):
    parameters.validate()
    environmentId = parameters.id()
    environmentName = parameters.name()
    environmentShortCode = parameters.shortCode()
    environmentDescription = parameters.description()

    session = self.updateDatabase('call deleteEnvironmentComponents(:id)',{'id':parameters.id()},'MySQL error deleting environment components',None,False)
    self.updateDatabase('call updateEnvironment(:id,:name,:shortCode,:desc)',{'id':environmentId,'name':environmentName,'shortCode':environmentShortCode,'desc':environmentDescription},'MySQL error updating environment',session,False)
    if (len(parameters.environments()) > 0):
      for c in parameters.environments():  self.updateDatabase('call addCompositeEnvironment(:id,:c)',{'id':environmentId,'c':c},'MySQL error adding composite environment',session,False)
      if (len(parameters.duplicateProperty()) > 0):
        self.addCompositeEnvironmentProperties(environmentId,parameters.duplicateProperty(),parameters.overridingEnvironment())
    self.commitDatabase(session)
    self.addValueTensions(environmentId,parameters.tensions())
    self.commitDatabase(session)

  def deleteRequirement(self,r):
    self.deleteObject(r,'requirement')
    
  def responseList(self,callTxt,argDict,errorTxt,session = None):
    try:
      persistSession = True
      if (session == None):
        session = self.conn()
        persistSession = False
      rs = session.execute(text(callTxt),argDict)
      responseList = []
      if (rs.rowcount > 0):
        for row in rs.fetchall():
          if (len(row) > 1):
            responseList.append(tuple(list(row)))
          else:
            responseList.append(list(row)[0])
      rs.close()
      if (persistSession == False):
        session.close()
      return responseList
    except OperationalError as e:
      exceptionText = 'MySQL error calling ' + callTxt + ' (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DataError as e:
      exceptionText = 'MySQL error calling ' + callTxt + ' (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      id,msg = e
      exceptionText = errorTxt + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 
    except ProgrammingError as e:
      raise DatabaseProxyException(format(e)) 

  def getEnvironments(self,constraintId = -1):
    envRows = self.responseList('call getEnvironments(:id)',{'id':constraintId},'MySQL error getting environments')
    environments = {}
    for environmentId,environmentName,environmentShortCode,environmentDesc in envRows:
      cc = self.compositeEnvironments(environmentId)
      duplicateProperty = 'None'
      overridingEnvironment = ''
      if (len(cc) > 0):
        duplicateProperty,overridingEnvironment = self.duplicateProperties(environmentId)
      tensions = self.environmentTensions(environmentName)
      p = EnvironmentParameters(environmentName,environmentShortCode,environmentDesc,cc,duplicateProperty,overridingEnvironment,tensions)
      cn = ObjectFactory.build(environmentId,p)
      environments[environmentName] = cn 
    return environments

  def compositeEnvironments(self,environmentId):
    return self.responseList('call compositeEnvironments(:id)',{'id':environmentId},'MySQL error getting environments associated with composite environment id ' + str(environmentId))


  def duplicateProperties(self,environmentId):
    return self.responseList('call duplicateProperties(:id)',{'id':environmentId},'MySQL error getting duplicate properties associated with composite environment id ' + str(environmentId))[0]

  def getAttackers(self,constraintId = -1):
    return self.populateAttackers(self.responseList('call getAttackers(:id)',{'id':constraintId},'MySQL error getting attackers' + str(constraintId)))

  def getPersonalAttackers(self):
    return self.populateAttackers(self.responseList('call getPersonalAttackers()',{},'MySQL error getting personal attackers'))

  def populateAttackers(self,attackerRows):
    attackers = {}
    for attackerId,attackerName,attackerDesc,attackerImage in attackerRows:
      tags = self.getTags(attackerName,'attacker')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(attackerId,'attacker'):
        roles = self.dimensionRoles(attackerId,environmentId,'attacker')
        capabilities = self.attackerCapabilities(attackerId,environmentId)
        motives = self.attackerMotives(attackerId,environmentId)
        properties = AttackerEnvironmentProperties(environmentName,roles,motives,capabilities)
        environmentProperties.append(properties) 
      p = AttackerParameters(attackerName,attackerDesc,attackerImage,tags,environmentProperties)
      attacker = ObjectFactory.build(attackerId,p)
      attackers[attackerName] = attacker
    return attackers
  
  def dimensionEnvironments(self,dimId,dimTable):
    return self.responseList('call ' + dimTable + '_environments(:id)',{'id':dimId},'MySQL error getting environments for ' + dimTable + ' id ' + str(dimId))
   
  def attackerMotives(self,attackerId,environmentId):
    return self.responseList('call attacker_motivation(:aId,:eId)',{'aId':attackerId,'eId':environmentId},'MySQL error getting motives for attacker id ' + str(attackerId) + ' in environment id ' + str(environmentId))

  def threatLikelihood(self,threatId,environmentId):
    return self.responseList('select threat_likelihood(:tId,:eId)',{'tId':threatId,'eId':environmentId},'MySQL error getting likelihood for threat id ' + str(threatId) + ' in environment id ' + str(environmentId))[0]

  def vulnerabilitySeverity(self,vulId,environmentId):
    return self.responseList('select vulnerability_severity(:vId,:eId)',{'vId':vulId,'eId':environmentId},'MySQL error getting severity for vulnerability id ' + str(vulId) + ' in environment id ' + str(environmentId))[0]

  def attackerCapabilities(self,attackerId,environmentId):
    return self.responseList('call attacker_capability(:aId,:eId)',{'aId':attackerId,'eId':environmentId},'MySQL error getting capabilities for attacker id ' + str(attackerId) + ' in environment id ' + str(environmentId))

  def addAttacker(self,parameters):
    parameters.validate()
    attackerId = self.newId()
    attackerName = parameters.name()
    attackerDesc = parameters.description()
    attackerImage = parameters.image()
    tags = parameters.tags()
    self.updateDatabase("call addAttacker(:id,:name,:desc,:image)",{'id':attackerId,'name':attackerName,'desc':attackerDesc,'image':attackerImage},'MySQL error adding attacker ' + str(attackerId))
    self.addTags(attackerName,'attacker',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(attackerId,'attacker',environmentName)
      self.addAttackerMotives(attackerId,environmentName,environmentProperties.motives())
      self.addAttackerCapabilities(attackerId,environmentName,environmentProperties.capabilities())
      self.addDimensionRoles(attackerId,'attacker',environmentName,environmentProperties.roles())
    return attackerId

  def addDimensionEnvironment(self,dimId,table,environmentName,session = None):
    if (session != None):
      self.updateDatabase('call add_' + table + '_environment(:id,:name)',{'id':dimId,'name':environmentName},'MySQL error associating ' + table + ' id ' + str(dimId) + ' with environment ' + environmentName,session)
    else:
      self.updateDatabase('call add_' + table + '_environment(:id,:name)',{'id':dimId,'name':environmentName},'MySQL error associating ' + table + ' id ' + str(dimId) + ' with environment ' + environmentName)

  def addAttackerMotives(self,attackerId,environmentName,motives):
    for motive in motives:
      self.updateDatabase('call addAttackerMotive(:aId,:envName,:motive)',{'aId':attackerId,'envName':environmentName,'motive':motive},'MySQL error updating motivates for attacker id ' + str(attackerId))

  def addAttackerCapabilities(self,attackerId,environmentName,capabilities):
    for name,value in capabilities:
      self.updateDatabase('call addAttackerCapability(:aId,:envName,:name,:value)',{'aId':attackerId,'envName':environmentName,'name':name,'value':value},'MySQL error updating attacker capabilities for attacker id ' + str(attackerId))
  
  def updateAttacker(self,parameters):
    parameters.validate()
    session = self.updateDatabase('call deleteAttackerComponents(:id)',{'id':parameters.id()},'MySQL error deleting attacker components',None,False)
    attackerId = parameters.id()
    attackerName = parameters.name()
    attackerDesc = parameters.description()
    attackerImage = parameters.image()
    tags = parameters.tags()
    self.updateDatabase("call updateAttacker(:id,:name,:desc,:image)",{'id':attackerId,'name':attackerName,'desc':attackerDesc,'image':attackerImage},'MySQL error updating attacker',session)
    self.addTags(attackerName,'attacker',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(attackerId,'attacker',environmentName)
      self.addAttackerMotives(attackerId,environmentName,environmentProperties.motives())
      self.addAttackerCapabilities(attackerId,environmentName,environmentProperties.capabilities())
      self.addDimensionRoles(attackerId,'attacker',environmentName,environmentProperties.roles())

  def deleteAttacker(self,attackerId):
    self.deleteObject(attackerId,'attacker')
    
  def deleteObject(self,objtId,tableName):
    sqlTxt = 'call delete_' + tableName + '(:obj)'
    self.updateDatabase(sqlTxt,{'obj':objtId},'MySQL error deleting ' + tableName + 's')

  def addAsset(self,parameters):
    parameters.validate()
    assetId = self.newId()
    assetName = parameters.name()
    shortCode = parameters.shortCode()
    assetDesc = parameters.description()
    assetSig = parameters.significance()
    assetType = parameters.type()
    assetCriticality = parameters.critical()
    assetCriticalRationale = parameters.criticalRationale()
    tags = parameters.tags()
    ifs = parameters.interfaces()
    self.updateDatabase('call addAsset(:id,:name,:sc,:desc,:sig,:type,:c,:cr)',{'id':assetId,'name':assetName,'sc':shortCode,'desc':assetDesc,'sig':assetSig,'type':assetType,'c':assetCriticality,'cr':assetCriticalRationale},'MySQL error adding asset')
    self.addTags(assetName,'asset',tags)
    self.addInterfaces(assetName,'asset',ifs)
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(assetId,'asset',environmentName)
      self.addAssetAssociations(assetId,assetName,environmentName,cProperties.associations())
      self.addSecurityProperties('asset',assetId,environmentName,cProperties.properties(),cProperties.rationale())
    return assetId

  def updateAsset(self,parameters):
    parameters.validate()
    assetId = parameters.id()
    assetName = parameters.name()
    shortCode = parameters.shortCode()
    assetDesc = parameters.description()
    assetSig = parameters.significance()
    assetType = parameters.type()
    assetCriticality = parameters.critical()
    assetCriticalRationale = parameters.criticalRationale()
    tags = parameters.tags()
    ifs = parameters.interfaces()
    session = self.updateDatabase('call deleteAssetComponents(:id)',{'id':assetId},'MySQL error deleting asset components',None,False)
    self.updateDatabase('call updateAsset(:id,:name,:shortCode,:desc,:sig,:type,:crit,:rationale)',{'id':assetId,'name':assetName,'shortCode':shortCode,'desc':assetDesc,'sig':assetSig,'type':assetType,'crit':assetCriticality,'rationale':assetCriticalRationale},'MySQL error updating asset',session)
    self.addTags(assetName,'asset',tags)
    self.addInterfaces(assetName,'asset',ifs)
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(assetId,'asset',environmentName)
      self.addAssetAssociations(assetId,assetName,environmentName,cProperties.associations())
      self.addSecurityProperties('asset',assetId,environmentName,cProperties.properties(),cProperties.rationale())
    self.updateDatabase('call deleteWidowedConcerns(:name)',{'name':assetName},'MySQL error delete widowed concerns')
    


  def addTemplateAssetProperties(self,taId,cProp,iProp,avProp,acProp,anProp,panProp,unlProp,unoProp,cRat,iRat,avRat,acRat,anRat,panRat,unlRat,unoRat):
    callTxt = 'call add_template_asset_properties(:ta,:cPr,:iPr,:avPr,:acPr,:anPr,:panPr,:unlPr,:unoPr,:cRa,:iRa,:avRa,:acRa,:anRa,:panRa,:unlRa,:unoRa)'
    self.updateDatabase(callTxt, {'ta':taId,'cPr':cProp,'iPr':iProp,'avPr':avProp,'acPr':acProp,'anPr':anProp,'panPr':panProp,'unlPr':unlProp,'unoPr':unoProp,'cRa':cRat,'iRa':iRat,'avRa':avRat,'acRa':acRat,'anRa':anRat,'panRa':panRat,'unlRa':unlRat,'unoRa':unoRat},'MySQL error adding security properties to template asset')

  def updateTemplateAssetProperties(self,taId,cProp,iProp,avProp,acProp,anProp,panProp,unlProp,unoProp,cRat,iRat,avRat,acRat,anRat,panRat,unlRat,unoRat):
    callTxt = 'update template_asset_property set property_value_id=:v, property_rationale=":r" where template_asset_id = :a and property_id = :p' 
    argDict = {'v':cProp,'r':cRat,'a':taId,'p':C_PROPERTY}
    session = self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',None,False)
    argDict = {'v':iProp,'r':iRat,'a':taId,'p':I_PROPERTY}
    self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',session,False)
    argDict = {'v':avProp,'r':avRat,'a':taId,'p':AV_PROPERTY}
    self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',session,False)
    argDict = {'v':acProp,'r':acRat,'a':taId,'p':AC_PROPERTY}
    self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',session,False)
    argDict = {'v':anProp,'r':anRat,'a':taId,'p':AN_PROPERTY}
    self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',session,False)
    argDict = {'v':panProp,'r':panRat,'a':taId,'p':PAN_PROPERTY}
    self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',session,False)
    argDict = {'v':unlProp,'r':unlRat,'a':taId,'p':UNL_PROPERTY}
    self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',session,False)
    argDict = {'v':unoProp,'r':unoRat,'a':taId,'p':UNO_PROPERTY}
    self.updateDatabase(callTxt,argDict,'MySQL error updating template asset property',session,False)
    self.commitDatabase(session)

  def addSecurityProperties(self,dimTable,objtId,environmentName,securityProperties,pRationale):
    sqlTxt = 'call add_' + dimTable + '_properties(:obj,:env,:cPr,:iPr,:avPr,:acPr,:anPr,:panPr,:unlPr,:unoPr,:cRa,:iRa,:avRa,:acRa,:anRa,:panRa,:unlRa,:unoRa)'
    self.updateDatabase(sqlTxt,{'obj':objtId,'env':environmentName,'cPr':securityProperties[C_PROPERTY],'iPr':securityProperties[I_PROPERTY],'avPr':securityProperties[AV_PROPERTY],'acPr':securityProperties[AC_PROPERTY],'anPr':securityProperties[AN_PROPERTY],'panPr':securityProperties[PAN_PROPERTY],'unlPr':securityProperties[UNL_PROPERTY],'unoPr':securityProperties[UNO_PROPERTY],'cRa':pRationale[C_PROPERTY],'iRa':pRationale[I_PROPERTY],'avRa':pRationale[AV_PROPERTY],'acRa':pRationale[AC_PROPERTY],'anRa':pRationale[AN_PROPERTY],'panRa':pRationale[PAN_PROPERTY],'unlRa':pRationale[UNL_PROPERTY],'unoRa':pRationale[UNO_PROPERTY]},'MySQL error adding security properties for ' + dimTable)

  def deleteAsset(self,assetId):
    self.deleteObject(assetId,'asset')
    

  def dimensionObject(self,constraintName,dimensionTable):
    if (dimensionTable != 'requirement'): constraintId = self.getDimensionId(constraintName,dimensionTable)
    objts = {}
    if (dimensionTable == 'provided_interface' or dimensionTable == 'required_interface'): objts = self.getInterfaces(constraintId)
    if (dimensionTable == 'goalassociation'): objts = self.getGoalAssociations(constraintId)
    if (dimensionTable == 'asset'): objts = self.getAssets(constraintId)
    if (dimensionTable == 'template_asset'): objts = self.getTemplateAssets(constraintId)
    if (dimensionTable == 'template_requirement'): objts = self.getTemplateRequirements(constraintId)
    if (dimensionTable == 'template_goal'): objts = self.getTemplateGoals(constraintId)
    if (dimensionTable == 'securitypattern'): objts = self.getSecurityPatterns(constraintId)
    if (dimensionTable == 'component_view'): objts = self.getComponentViews(constraintId)
    if (dimensionTable == 'component'): objts = self.getComponents(constraintId)
    if (dimensionTable == 'classassociation'): objts = self.getClassAssociations(constraintId)
    if (dimensionTable == 'goal'): objts = self.getGoals(constraintId)
    if (dimensionTable == 'obstacle'): objts = self.getObstacles(constraintId)
    elif (dimensionTable == 'attacker'): objts = self.getAttackers(constraintId)
    elif (dimensionTable == 'threat'): objts = self.getThreats(constraintId)
    elif (dimensionTable == 'vulnerability'): objts = self.getVulnerabilities(constraintId)
    elif (dimensionTable == 'risk'): objts = self.getRisks(constraintId)
    elif (dimensionTable == 'response'): objts = self.getResponses(constraintId)
    elif (dimensionTable == 'countermeasure'): objts = self.getCountermeasures(constraintId)
    elif (dimensionTable == 'persona'): objts = self.getPersonas(constraintId)
    elif (dimensionTable == 'task'): objts = self.getTasks(constraintId)
    elif (dimensionTable == 'usecase'): objts = self.getUseCases(constraintId)
    elif (dimensionTable == 'userstory'): objts = self.getUserStories(constraintId)
    elif (dimensionTable == 'misusecase'): objts = self.getMisuseCases(constraintId)
    elif (dimensionTable == 'requirement'): return self.getRequirement(constraintName)
    elif (dimensionTable == 'environment'): objts = self.getEnvironments(constraintId)
    elif (dimensionTable == 'role'): objts = self.getRoles(constraintId)
    elif (dimensionTable == 'domainproperty'): objts = self.getDomainProperties(constraintId)
    elif (dimensionTable == 'document_reference'): objts = self.getDocumentReferences(constraintId)
    elif (dimensionTable == 'concept_reference'): objts = self.getConceptReferences(constraintId)
    elif (dimensionTable == 'persona_characteristic'): objts = self.getPersonaCharacteristics(constraintId)
    elif (dimensionTable == 'task_characteristic'): objts = self.getTaskCharacteristics(constraintId)
    elif (dimensionTable == 'external_document'): objts = self.getExternalDocuments(constraintId)
    elif (dimensionTable == 'internal_document'): objts = self.getInternalDocuments(constraintId)
    elif (dimensionTable == 'code'): objts = self.getCodes(constraintId)
    elif (dimensionTable == 'memo'): objts = self.getMemos(constraintId)
    elif (dimensionTable == 'reference_synopsis'): objts = self.getReferenceSynopsis(constraintId)
    elif (dimensionTable == 'reference_contribution'): objts = self.getReferenceContributions(constraintId)
    elif (dimensionTable == 'persona_implied_process'): objts = self.getImpliedProcesses(constraintId)
    elif (dimensionTable == 'trust_boundary'): objts = self.getTrustBoundaries(constraintId)
    elif (dimensionTable == 'policy_statement'): objts = self.getPolicyStatements(constraintId)
    return (list(objts.values()))[0]


  def getAssets(self,constraintId = -1):
    return self.populateAssets(self.responseList('call getAssets(:id)',{'id':constraintId},'MySQL error getting assets'))

  def getPersonalInformation(self):
    return self.populateAssets(self.responseList('call getPersonalInformation()',{},'MySQL error getting personal information'))

  def populateAssets(self,assetRows):
    assets = {}
    for assetId,assetName,shortCode,assetDesc,assetSig,assetType,assetCriticality,assetCriticalRationale in assetRows:
      tags = self.getTags(assetName,'asset')
      ifs = self.getInterfaces(assetName,'asset')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(assetId,'asset'):
        syProperties,pRationale = self.relatedProperties('asset',assetId,environmentId)
        assetAssociations = self.assetAssociations(assetId,environmentId)
        properties = AssetEnvironmentProperties(environmentName,syProperties,pRationale,assetAssociations)
        environmentProperties.append(properties) 
      parameters = AssetParameters(assetName,shortCode,assetDesc,assetSig,assetType,assetCriticality,assetCriticalRationale,tags,ifs,environmentProperties)
      asset = ObjectFactory.build(assetId,parameters)
      assets[assetName] = asset
    return assets

  def getAssetsSummary(self):
    objtRows = self.responseList('call getAssetsSummary()',{},'MySQL error getting asset summary')
    rows = []
    for objtName, objtType in objtRows:
      rows.append(ObjectSummary(objtName,type=objtType))
    return rows

  def getGoalsSummary(self):
    objtRows = self.responseList('call getGoalsSummary()',{},'MySQL error getting goal summary')
    rows = []
    for objtName, objtOrig, objtStatus in objtRows:
      rows.append(ObjectSummary(objtName,originator=objtOrig,status=objtStatus))
    return rows

  def getObstaclesSummary(self):
    objtRows = self.responseList('call getObstaclesSummary()',{},'MySQL error getting obstacle summary')
    rows = []
    for objtName, objtOrig in objtRows:
      rows.append(ObjectSummary(objtName,originator=objtOrig))
    return rows

  def getUseCasesSummary(self):
    objtRows = self.responseList('call getUseCasesSummary()',{},'MySQL error getting use case summary')
    rows = []
    for objtName, objtDesc in objtRows:
      rows.append(ObjectSummary(objtName,description=objtDesc))
    return rows

  def getAttackersSummary(self):
    objtRows = self.responseList('call getAttackersSummary()',{},'MySQL error getting attacker summary')
    rows = []
    for objtName, objtDesc in objtRows:
      rows.append(ObjectSummary(objtName,description=objtDesc))
    return rows

  def getPersonasSummary(self):
    objtRows = self.responseList('call getPersonasSummary()',{},'MySQL error getting persona summary')
    rows = []
    for objtName, objtType in objtRows:
      rows.append(ObjectSummary(objtName,type=objtType))
    return rows

  def getThreatsSummary(self):
    objtRows = self.responseList('call getThreatsSummary()',{},'MySQL error getting threat summary')
    rows = []
    for objtName, objtType in objtRows:
      rows.append(ObjectSummary(objtName,type=objtType))
    return rows

  def getPersonaCharacteristicsSummary(self):
    objtRows = self.responseList('call getPersonaCharacteristicsSummary()',{},'MySQL error getting persona characteristics summary')
    rows = []
    for objtName, objtVar, objtChar in objtRows:
      rows.append(ObjectSummary(objtChar,variable=objtVar,characteristic=objtName))
    return rows


  def getThreats(self,constraintId = -1):
    return self.populateThreats(self.responseList('call getThreats(:id)',{'id':constraintId},'MySQL error getting threats'))

  def getPersonalThreats(self):
    return self.populateThreats(self.responseList('call getPersonalThreats()',{},'MySQL error getting personal threats'))
   
  def populateThreats(self,threatRows):
    threats = {}
    for threatId,threatName,threatType,thrMethod in threatRows: 
      tags = self.getTags(threatName,'threat')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(threatId,'threat'):
        likelihood = self.threatLikelihood(threatId,environmentId)
        assets = self.threatenedAssets(threatId,environmentId) 
        attackers = self.threatAttackers(threatId,environmentId)
        syProperties,pRationale = self.relatedProperties('threat',threatId,environmentId)
        properties = ThreatEnvironmentProperties(environmentName,likelihood,assets,attackers,syProperties,pRationale)
        environmentProperties.append(properties)
      parameters = ThreatParameters(threatName,threatType,thrMethod,tags,environmentProperties)
      threat = ObjectFactory.build(threatId,parameters)
      threats[threatName] = threat
    return threats

  def getDimensionId(self,dimensionName,dimensionTable):
    if (dimensionTable == 'trace_dimension'):
      return self.theDimNameLookup[dimensionName]
    if dimensionTable == 'linkand':
      dimensionTable = 'goalassociation'
    if dimensionTable == 'security_pattern':
      dimensionTable = 'securitypattern'
    try:
      session = self.conn()
      sqlText = ''
      if ((dimensionTable == 'classassociation') or (dimensionTable == 'goalassociation')):
        associationComponents = dimensionName.split('/')
        if (dimensionTable == 'goalassociation'):
          rs = session.execute(text('select goalAssociationId(:ac0,:ac1,:ac2,:ac3,ac:4)'),{'ac0':associationComponents[0],'ac1':associationComponents[1],'ac2':associationComponents[2],'ac3':associationComponents[3],'ac4':associationComponents[4]})
        elif (dimensionTable == 'classassociation'):
          rs = session.execute(text('select classAssociationId(:ac0,:ac1,:ac2)'),{'ac0':associationComponents[0],'ac1':associationComponents[1],'ac2':associationComponents[2]})
      elif ((dimensionTable == 'provided_interface') or (dimensionTable == 'required_interface')):
        cName,ifName = dimensionName.split('_')
        rs = session.execute(text('select interfaceId(:name)'),{'name':ifName})
      elif (dimensionTable == 'policy_statement'):
        psComponents = dimensionName.split('/')
        rs = session.execute(text('select policyStatementId(:goal,:env,:subj,:at,:res)'),{'goal':psComponents[0],'env':psComponents[1],'subj':psComponents[2],'at':psComponents[3],'res':psComponents[4]})
      else:
        callTxt = text('call dimensionId(:name,:table)')
        argDict = {'name':dimensionName,'table':dimensionTable}
        rs = session.execute(callTxt,argDict)

      if (rs.rowcount == 0):
        exceptionText = 'No identifier associated with '
        exceptionText += dimensionTable + ' object ' + str(dimensionName)
        raise ObjectNotFound(exceptionText)

      row = rs.fetchone() 
      dimId = row[0]
      if (dimId == None and dimensionTable == 'requirement'):
        rs = session.execute('select requirementNameId(:name)',{'name':dimensionName})
        row = rs.fetchone()
        dimId = row[0]
      rs.close()
      session.close()
      return dimId
    except ValueError as e:
      exceptionText = 'Error splitting ' + dimensionName + ': ' + format(e)
      raise DatabaseProxyException(exceptionText) 
    except OperationalError as e:
      exceptionText = 'MySQL error getting '
      exceptionText += dimensionTable + ' (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      id,msg = e
      exceptionText = 'MySQL error getting '
      exceptionText += dimensionTable + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getDimensions(self,dimensionTable,idConstraint=-1):
    dimRows = self.responseList('call getDimensions(:dimensionTable, :idConstraint)',{'dimensionTable':dimensionTable,'idConstraint':idConstraint},'MySQL error getting ' + dimensionTable)
    dimensions = {}
    for dimensionId,dimensionName in dimRows:
      dimensions[dimensionName] = dimensionId
    return dimensions

  def getDimensionNames(self,dimensionTable,currentEnvironment = ''):
    if (dimensionTable != 'template_asset' and dimensionTable != 'template_requirement' and dimensionTable != 'template_goal' and dimensionTable != 'locations' and dimensionTable != 'persona_characteristic_synopsis' and dimensionTable != 'document_reference_synopsis'):
      callTxt = 'call ' + dimensionTable + 'Names(:env)' 
      argDict = {'env':currentEnvironment}
      return self.responseList(callTxt,argDict,'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'template_asset'): return self.responseList('call template_assetNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'template_requirement'): return self.responseList('call template_requirementNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'template_goal'): return self.responseList('call template_goalNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'locations'): return self.responseList('call locationsNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'persona_characteristic_synopsis'): return self.responseList('call persona_characteristic_synopsisNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'document_reference_synopsis'): return self.responseList('call document_reference_synopsisNames()',{},'MySQL error getting ' + dimensionTable + 's')

  def getEnvironmentNames(self):
    return self.responseList('call nonCompositeEnvironmentNames()',{},'MySQL error getting environments')

  def addThreat(self,parameters,update = False):
    parameters.validate()
    threatId = self.newId()
    threatName = parameters.name()
    threatType = parameters.type()
    threatMethod = parameters.method()
    tags = parameters.tags()
    session = self.updateDatabase("call addThreat(:id,:name,:type,:method)",{'id':threatId,'name':threatName,'type':threatType,'method':threatMethod},'MySQL error adding threat',None,False)
    self.addTags(threatName,'threat',tags)
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(threatId,'threat',environmentName)
      self.updateDatabase("call addThreatLikelihood(:tId,:env,:likely)",{'tId':threatId,'env':environmentName,'likely':cProperties.likelihood()},'MySQL error adding threat likelihood',session,False)
      self.addSecurityProperties('threat',threatId,environmentName,cProperties.properties(),cProperties.rationale())

      for assetName in cProperties.assets():
        self.updateDatabase("call addAssetThreat(:tId,:env,:assName)",{'tId':threatId,'env':environmentName,'assName':assetName},'MySQL error adding asset threat',session,False)
      for attacker in cProperties.attackers():
        self.updateDatabase("call addThreatAttacker(:tId,:env,:attacker)",{'tId':threatId,'env':environmentName,'attacker':attacker},'MySQL error adding threat attacker',session,False)
    self.commitDatabase(session)
    return threatId

  def updateThreat(self,parameters):
    parameters.validate()
    threatId = parameters.id()
    threatName = parameters.name()
    threatType = parameters.type()
    threatMethod = parameters.method()
    tags = parameters.tags()

    session = self.updateDatabase('call deleteThreatComponents(:id)',{'id':threatId},'MySQL error deleting threat components',None,False)
    self.updateDatabase('call updateThreat(:id,:name,:type,:method)',{'id':threatId,'name':threatName,'type':threatType,'method':threatMethod},'MySQL error updating threat',session,False)
    self.addTags(threatName,'threat',tags)

    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(threatId,'threat',environmentName)
      self.updateDatabase("call addThreatLikelihood(:tId,:env,:likely)",{'tId':threatId,'env':environmentName,'likely':cProperties.likelihood()},'MySQL error adding threat likelihood',session,False)
      self.addSecurityProperties('threat',threatId,environmentName,cProperties.properties(),cProperties.rationale())

      for assetName in cProperties.assets():
        self.updateDatabase("call addAssetThreat(:tId,:env,:assName)",{'tId':threatId,'env':environmentName,'assName':assetName},'MySQL error adding asset threat',session,False)
      for attacker in cProperties.attackers():
        self.updateDatabase("call addThreatAttacker(:tId,:env,:attacker)",{'tId':threatId,'env':environmentName,'attacker':attacker},'MySQL error adding threat attacker',session,False)
    self.commitDatabase(session)

  def getVulnerabilities(self,constraintId = -1):
    return self.populateVulnerabilities(self.responseList('call getVulnerabilities(:id)',{'id':constraintId},'MySQL error getting vulnerabilities'))

  def getPersonalVulnerabilities(self):
    return self.populateVulnerabilities(self.responseList('call getPersonalVulnerabilities()',{},'MySQL error getting personal vulnerabilities'))

  def populateVulnerabilities(self,vulRows):
    vulnerabilities = {}
    for vulnerabilityId,vulnerabilityName,vulnerabilityDescription,vulnerabilityType in vulRows:
      tags = self.getTags(vulnerabilityName,'vulnerability')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(vulnerabilityId,'vulnerability'):
        severity = self.vulnerabilitySeverity(vulnerabilityId,environmentId)
        assets = self.vulnerableAssets(vulnerabilityId,environmentId)
        properties = VulnerabilityEnvironmentProperties(environmentName,severity,assets)
        environmentProperties.append(properties)
      parameters = VulnerabilityParameters(vulnerabilityName,vulnerabilityDescription,vulnerabilityType,tags,environmentProperties)
      vulnerability = ObjectFactory.build(vulnerabilityId,parameters)
      vulnerabilities[vulnerabilityName] = vulnerability
    return vulnerabilities

  def deleteVulnerability(self,vulId):
    self.deleteObject(vulId,'vulnerability')
    

  def addVulnerability(self,parameters):
    parameters.validate()
    vulName = parameters.name()
    vulDesc = parameters.description()
    vulType = parameters.type()
    tags = parameters.tags()
    vulId = self.newId()
    session = self.updateDatabase('call addVulnerability(:id,:name,:desc,:type)',{'id':vulId,'name':vulName,'desc':vulDesc,'type':vulType},'MySQL error adding vulnerabilitity',None,False)
    self.addTags(vulName,'vulnerability',tags)
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(vulId,'vulnerability',environmentName)
      self.updateDatabase("call addVulnerabilitySeverity(:vId,:env,:severity)",{'vId':vulId,'env':environmentName,'severity':cProperties.severity()},'MySQL error adding vulnerability severity',session,False)
      for assetName in cProperties.assets():
        self.updateDatabase("call addAssetVulnerability(:vId,:env,:assName)",{'vId':vulId,'env':environmentName,'assName':assetName},'MySQL error adding asset vulnerability',session,False)
    self.commitDatabase(session)
    return vulId

  def updateVulnerability(self,parameters):
    parameters.validate()
    vulId = parameters.id()
    vulName = parameters.name()
    vulDesc = parameters.description()
    vulType = parameters.type()
    tags = parameters.tags()

    session = self.updateDatabase('call deleteVulnerabilityComponents(:id)',{'id':vulId},'MySQL error deleting vulnerability components',None,False)
    self.updateDatabase('call updateVulnerability(:id,:name,:desc,:type)',{'id':vulId,'name':vulName,'desc':vulDesc,'type':vulType},'MySQL error updating vulnerability',session,False)
    self.addTags(vulName,'vulnerability',tags)
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(vulId,'vulnerability',environmentName)
      self.updateDatabase("call addVulnerabilitySeverity(:vId,:env,:severity)",{'vId':vulId,'env':environmentName,'severity':cProperties.severity()},'MySQL error adding vulnerability severity',session,False)
      for assetName in cProperties.assets():
        self.updateDatabase("call addAssetVulnerability(:vId,:env,:assName)",{'vId':vulId,'env':environmentName,'assName':assetName},'MySQL error adding asset vulnerability',session,False)
    self.commitDatabase(session)

  def relatedProperties(self,dimTable,objtId,environmentId):
    callTxt = 'call ' + dimTable + 'Properties (:objtId,:envId)'
    argDict = {'objtId':objtId,'envId':environmentId}
    row = self.responseList(callTxt,argDict,'MySQL error getting related properties')[0]
    properties = []
    properties =  array((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])).astype(int32) 
    pRationale =  [row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15]]
    return (properties,pRationale)

  def templateAssetProperties(self,taId):
    row = self.responseList('call template_assetProperties(:id)',{'id':taId},'MySQL error getting template asset properties')[0]
    properties = []
    rationale = []
    properties.append(row[0])
    properties.append(row[1])
    properties.append(row[2])
    properties.append(row[3])
    properties.append(row[4])
    properties.append(row[5])
    properties.append(row[6])
    properties.append(row[7])
    rationale.append(row[8])
    rationale.append(row[9])
    rationale.append(row[10])
    rationale.append(row[11])
    rationale.append(row[12])
    rationale.append(row[13])
    rationale.append(row[14])
    rationale.append(row[15])
    return (properties,rationale)

  def getPersonas(self,constraintId = -1):
    personaRows = self.responseList('call getPersonas(:id)',{'id':constraintId},'MySQL error getting personas')
    personas = {}
    for personaId,personaName,activities,attitudes,aptitudes,motivations,skills,intrinsic,contextual,image,isAssumption,pType in personaRows:
      tags = self.getTags(personaName,'persona')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(personaId,'persona'):
        personaDesc = self.personaNarrative(personaId,environmentId)
        directFlag = self.personaDirect(personaId,environmentId)
        roles = self.dimensionRoles(personaId,environmentId,'persona')
        envCodes = self.personaEnvironmentCodes(personaName,environmentName)
        properties = PersonaEnvironmentProperties(environmentName,directFlag,personaDesc,roles,envCodes)
        environmentProperties.append(properties)
      codes = self.personaCodes(personaName)
      parameters = PersonaParameters(personaName,activities,attitudes,aptitudes,motivations,skills,intrinsic,contextual,image,isAssumption,pType,tags,environmentProperties,codes)
      persona = ObjectFactory.build(personaId,parameters)
      personas[personaName] = persona
    return personas

  def dimensionRoles(self,dimId,environmentId,table):
    return self.responseList('call ' + table + '_roles(:dimId,:envId)',{'dimId':dimId,'envId':environmentId},'MySQL error getting roles for ' + table + ' associated with environment id ' + str(environmentId))

  def threatAttackers(self,threatId,environmentId):
    return self.responseList('call threat_attacker(:tId,:eId)',{'tId':threatId,'eId':environmentId},'MySQL error getting attackers for threat id ' + str(threatId) + ' in environment ' + str(environmentId))

  def addPersona(self,parameters):
    personaId = self.newId()
    personaName = parameters.name()
    activities = parameters.activities()
    attitudes = parameters.attitudes()
    aptitudes = parameters.aptitudes()
    motivations = parameters.motivations()
    skills = parameters.skills()
    intrinsic = parameters.intrinsic()
    contextual = parameters.contextual()
    image = parameters.image()
    isAssumption = parameters.assumption()
    pType = parameters.type()
    codes = parameters.codes()
    tags = parameters.tags()
    self.updateDatabase('call addPersona(:id,:name,:act,:att,:apt,:mot,:skills,:intr,:cont,:img,:ass,:type)',{'id':personaId,'name':personaName,'act':activities,'att':attitudes,'apt':aptitudes,'mot':motivations,'skills':skills,'intr':intrinsic,'cont':contextual,'img':image,'ass':isAssumption,'type':pType},'MySQL error adding persona')
    self.addPersonaCodes(personaName,codes)
    self.addTags(personaName,'persona',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(personaId,'persona',environmentName)
      self.addPersonaNarrative(personaId,environmentName,environmentProperties.narrative())
      self.addPersonaDirect(personaId,environmentName,environmentProperties.directFlag())
      self.addDimensionRoles(personaId,'persona',environmentName,environmentProperties.roles())
      self.addPersonaEnvironmentCodes(personaName,environmentName,environmentProperties.codes())
    return personaId

  def addDimensionRoles(self,personaId,table,environmentName,roles):
    session = self.conn()
    for role in roles:
      self.updateDatabase('call add_' + table + '_role (:id,:envName,:role)',{'id':personaId,'envName':environmentName,'role':role},'MySQL error adding dimension role',session,False)
    self.commitDatabase(session) 

  def updatePersona(self,parameters):
    personaId = parameters.id()
    personaName = parameters.name()
    activities = parameters.activities()
    attitudes = parameters.attitudes()
    aptitudes = parameters.aptitudes()
    motivations = parameters.motivations()
    skills = parameters.skills()
    intrinsic = parameters.intrinsic()
    contextual = parameters.contextual()
    image = parameters.image()
    isAssumption = parameters.assumption()
    pType = parameters.type()
    codes = parameters.codes()
    tags = parameters.tags()

    session = self.updateDatabase('call deletePersonaComponents(:id)',{'id':personaId},'MySQL error deleting persona components',None,False)
    self.updateDatabase('call updatePersona(:id,:name,:act,:att,:apt,:mot,:skills,:intr,:cont,:img,:ass,:type)',{'id':personaId,'name':personaName,'act':activities,'att':attitudes,'apt':aptitudes,'mot':motivations,'skills':skills,'intr':intrinsic,'cont':contextual,'img':image,'ass':isAssumption,'type':pType},'MySQL error updating database',session)
    self.addPersonaCodes(personaName,codes)
    self.addTags(personaName,'persona',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(personaId,'persona',environmentName)
      self.addPersonaNarrative(personaId,environmentName,environmentProperties.narrative())
      self.addPersonaDirect(personaId,environmentName,environmentProperties.directFlag())
      self.addDimensionRoles(personaId,'persona',environmentName,environmentProperties.roles())
      self.addPersonaEnvironmentCodes(personaName,environmentName,environmentProperties.codes())

  def deletePersona(self,personaId):
    self.deleteObject(personaId,'persona')

  def getTasks(self,constraintId = -1):
    taskRows = self.responseList('call getTasks(:id)',{'id':constraintId},'MySQL error getting tasks')
    tasks = {}
    for taskId,taskName,taskShortCode,taskObjective,isAssumption,taskAuthor in taskRows:
      tags = self.getTags(taskName,'task')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(taskId,'task'):
        dependencies = self.taskDependencies(taskId,environmentId)
        personas = self.taskPersonas(taskId,environmentId)
        assets = self.taskAssets(taskId,environmentId)
        narrative = self.taskNarrative(taskId,environmentId)
        consequences = self.taskConsequences(taskId,environmentId)
        benefits = self.taskBenefits(taskId,environmentId)
        concernAssociations = self.taskConcernAssociations(taskId,environmentId)
        contributions = self.taskContributions(taskName,environmentName)
        envCodes = self.taskEnvironmentCodes(taskName,environmentName)
        properties = TaskEnvironmentProperties(environmentName,dependencies,personas,assets,concernAssociations,narrative,consequences,benefits,contributions,envCodes)
        environmentProperties.append(properties)
      parameters = TaskParameters(taskName,taskShortCode,taskObjective,isAssumption,taskAuthor,tags,environmentProperties)
      task = ObjectFactory.build(taskId,parameters)
      tasks[taskName] = task
    return tasks

  def getMisuseCases(self,constraintId = -1):
    mcRows = self.responseList('call getMisuseCases(:id)',{'id':constraintId},'MySQL error getting misuse cases')
    mcs = {}
    for mcId,mcName in mcRows:
      risk = self.misuseCaseRisk(mcId)
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(mcId,'misusecase'):
        riskId = self.getDimensionId(risk,'risk')
        mcEnv = self.misuseCaseEnvironment(environmentName,mcId,riskId,environmentId)
        environmentProperties.append(mcEnv)
      parameters = MisuseCaseParameters(mcName,environmentProperties,risk)
      mc = ObjectFactory.build(mcId,parameters)
      mcs[mcName] = mc
    return mcs

  def misuseCaseEnvironment(self,envName,mcId,riskId,envId,thrName = '',vulName = ''):
    narrative = self.misuseCaseNarrative(mcId,envId)
    mcEnv = MisuseCaseEnvironmentProperties(envName,narrative)
    if (thrName != '' and vulName != ''):
      mcEnv.theRiskRating = RiskRating(thrName,vulName,envName,self.riskRating(riskId,thrName,vulName,envName))
      threatId = self.getDimensionId(thrName,'threat')
      vulId = self.getDimensionId(vulName,'vulnerability')
      mcEnv.theLikelihood = self.threatLikelihood(threatId,envId)
      mcEnv.theSeverity = self.vulnerabilitySeverity(vulId,envId)
      mcEnv.theAttackers = self.threatAttackers(threatId,envId)
      threatenedAssets = self.threatenedAssets(threatId,envId)
      vulnerableAssets = self.vulnerableAssets(vulId,envId)

      mcEnv.theObjective = 'Exploit vulnerabilities in '
      for idx,vulAsset in enumerate(vulnerableAssets):
        mcEnv.theObjective += vulAsset
        if (idx != (len(vulnerableAssets) -1)):
          mcEnv.theObjective += ','
      mcEnv.theObjective += ' to threaten '
      for idx,thrAsset in enumerate(threatenedAssets):
        mcEnv.theObjective += thrAsset
        if (idx != (len(threatenedAssets) -1)):
          mcEnv.theObjective += ','
      mcEnv.theObjective += '.'
      mcEnv.theAssets = set(threatenedAssets + vulnerableAssets)
    return mcEnv


  def riskMisuseCase(self,riskId,thrName = '',vulName = ''):
    rows = []
    if (thrName != '' and vulName != ''):
      rows = self.responseList('call riskMisuseCaseByTV(:threat,:vulnerability)',{'threat':thrName,'vulnerability':vulName},'MySQL error getting risk misuse case')
    else:
      rows = self.responseList('call riskMisuseCase(:id)',{'id':riskId},'MySQL error getting risk misuse case')
    if (len(rows) == 0): return None
    else:
      row = rows[0]
      mcId = row[0]
      mcName = row[1]
      risk = self.misuseCaseRisk(mcId)
      if (riskId == -1):
        riskId = self.getDimensionId(risk,'risk')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(riskId,'risk'):
        mcEnv = self.misuseCaseEnvironment(environmentName,mcId,riskId,environmentId,thrName,vulName)
        environmentProperties.append(mcEnv)
      parameters = MisuseCaseParameters(mcName,environmentProperties,risk)
      mc = ObjectFactory.build(mcId,parameters)
      return mc

  def misuseCaseRisk(self,mcId):
    return self.responseList('select misuseCaseRisk(:id)',{'id':mcId},'MySQL error getting risk for misuse case id ' + str(mcId))[0]

  def taskPersonas(self,taskId,environmentId):
    return self.responseList('call taskPersonas(:tId,:eId)',{'tId':taskId,'eId':environmentId},'MySQL error getting task personas for environment id ' + str(environmentId))

  def taskAssets(self,taskId,environmentId):
    return self.responseList('call taskAssets(:tId,:eId)',{'tId':taskId,'eId':environmentId},'MySQL error getting task assets for environment id ' + str(environmentId))

  def addTask(self,parameters):
    taskName = parameters.name()
    taskShortCode = parameters.shortCode()
    taskObjective = parameters.objective()
    isAssumption = parameters.assumption()
    taskAuthor = parameters.author()
    tags = parameters.tags()
    taskId = self.newId()
    self.updateDatabase('call addTask(:id,:name,:shortCode,:obj,:ass,:auth)',{'id':taskId,'name':taskName,'shortCode':taskShortCode,'obj':taskObjective,'ass':isAssumption,'auth':taskAuthor},'MySQL error adding task')
    self.addTags(taskName,'task',tags)
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(taskId,'task',environmentName)
      self.addTaskDependencies(taskId,cProperties.dependencies(),environmentName)
      taskAssets = cProperties.assets()
      if (len(taskAssets) > 0):
        self.addTaskAssets(taskId,taskAssets,environmentName)
      self.addTaskPersonas(taskId,cProperties.personas(),environmentName)
      self.addTaskConcernAssociations(taskId,environmentName,cProperties.concernAssociations())
      self.addTaskNarrative(taskId,cProperties.narrative(),cProperties.consequences(),cProperties.benefits(),environmentName)
      self.addTaskContributions(cProperties.contributions())
      self.addTaskEnvironmentCodes(taskName,environmentName,cProperties.codes())
    return taskId

  def addMisuseCase(self,parameters,session):
    parameters.validate()
    mcName = parameters.name()
    mcId = self.newId()
    self.updateDatabase('call addMisuseCase(:id,:name)',{'id':mcId,'name':mcName},'MySQL error adding misuse case ' + mcName,session)
    self.addMisuseCaseRisk(mcId,parameters.risk(),session)
    for cProperties in parameters.environmentProperties():
      cProperties.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(mcId,'misusecase',environmentName,session)
      self.addMisuseCaseNarrative(mcId,cProperties.narrative(),environmentName,session)
    return mcId


  def updateTask(self,parameters):
    taskId = parameters.id()
    taskName = parameters.name()
    taskShortCode = parameters.shortCode()
    taskObjective = parameters.objective()
    isAssumption = parameters.assumption()
    taskAuthor = parameters.author()
    tags = parameters.tags()
    session = self.updateDatabase('call deleteTaskComponents(:id)',{'id':taskId},'MySQL error deleting task components',None,False)
    self.updateDatabase('call updateTask(:id,:name,:shortCode,:obj,:ass,:auth)',{'id':taskId,'name':taskName,'shortCode':taskShortCode,'obj':taskObjective,'ass':isAssumption,'auth':taskAuthor},session)
    self.addTags(taskName,'task',tags)
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(taskId,'task',environmentName)
      self.addTaskDependencies(taskId,cProperties.dependencies(),environmentName)
      self.addTaskConcernAssociations(taskId,environmentName,cProperties.concernAssociations())
      self.addTaskPersonas(taskId,cProperties.personas(),environmentName)
      taskAssets = cProperties.assets()
      if (len(taskAssets) > 0):
        self.addTaskAssets(taskId,taskAssets,environmentName)
      self.addTaskNarrative(taskId,cProperties.narrative(),cProperties.consequences(),cProperties.benefits(),environmentName)
      self.addTaskContributions(cProperties.contributions())
      self.addTaskEnvironmentCodes(taskName,environmentName,cProperties.codes())

  def updateMisuseCase(self,parameters,session):
    parameters.validate()
    mcId = parameters.id()
    mcName = parameters.name()
    self.updateDatabase('call deleteMisuseCaseComponents(:id)',{'id':mcId},'MySQL error dleting misuse case components',session,False)
    self.updateDatabase('call updateMisuseCase(:id,:name)',{'id':mcId,'name':mcName},'MySQL error updating misuse case',session,False)
    self.addMisuseCaseRisk(mcId,parameters.risk(),session)
    for cProperties in parameters.environmentProperties():
      cProperties.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(mcId,'misusecase',environmentName,session)
      self.addMisuseCaseNarrative(mcId,cProperties.narrative(),environmentName,session)


  def addTaskPersonas(self,taskId,personas,environmentName):
    session = self.conn()
    for persona,duration,frequency,demands,goalsupport in personas:
      self.updateDatabase('call addTaskPersona(:tId,:pers,:dur,:freq,:dem,:goal,:env)',{'tId':taskId,'pers':persona,'dur':duration,'freq':frequency,'dem':demands,'goal':goalsupport,'env':environmentName},'MySQL error adding task persona',session,False)
    self.commitDatabase(session)

  def addTaskAssets(self,taskId,assets,environmentName):
    session = self.conn()
    for asset in assets:
      self.updateDatabase('call addTaskAsset(:tId,:ass,:env)',{'tId':taskId,'ass':asset,'env':environmentName},'MySQL error adding task asset',session,False)
    self.commitDatabase(session)

  def addMisuseCaseRisk(self,mcId,riskName,session):
    self.updateDatabase('call addMisuseCaseRisk(:id,:risk)',{'id':mcId,'risk':riskName},'MySQL error associating risk with misuse case',session,False)

  def deleteTask(self,taskId):
    self.deleteObject(taskId,'task')
    

  def deleteThreat(self,objtId):
    self.deleteObject(objtId,'threat')
    

  def deleteResponse(self,responseId):
    self.deleteObject(responseId,'response')
    

  def getTraceDimensions(self,dimName,isFrom):
    return self.traceDimensionList(self.getDimensionId(dimName,'trace_dimension'),isFrom)

  def traceDimensionList(self,dimId,isFrom):
    return self.responseList('call traceDimensionList(:id,:from)',{'id':dimId,'from':isFrom},'MySQL error getting trace dimensions')

  def getRisks(self,constraintId = -1):
    return self.populateRisks(self.responseList('call getRisks(:id)',{'id':constraintId},'MySQL error getting risks'))

  def getPersonalRisks(self):
    return self.populateRisks(self.responseList('call getPersonalRisks()',{},'MySQL error getting personal risks'))

  def populateRisks(self,parameterList):
    risks = {}
    for parameters in parameterList:
      riskId = parameters[0]
      mc = self.riskMisuseCase(riskId)
      tags = self.getTags(parameters[1],'risk')
      parameters = RiskParameters(parameters[1],parameters[2],parameters[3],mc,tags)
      risk = ObjectFactory.build(riskId,parameters)
      risks[risk.name()] = risk
    return risks

  def getRisksSummary(self):
    objtRows = self.responseList('call getRisksSummary()',{},'MySQL error getting risk summary')
    rows = []
    for objtName, thrName, vulName in objtRows:
      rows.append(ObjectSummary(objtName,vulnerability=vulName,threat=thrName))
    return rows


  def addRisk(self,parameters):
    threatName = parameters.threat()
    vulName = parameters.vulnerability()
    tags = parameters.tags()
    riskId = self.newId()
    riskName = parameters.name()
    inTxt = parameters.intent()
    session = self.updateDatabase('call addRisk(:threat,:vuln,:rId,:risk,:txt)',{'threat':threatName,'vuln':vulName,'rId':riskId,'risk':riskName,'txt':inTxt},'MySQL error adding risk',None,False)
    mc = parameters.misuseCase()
    mcParameters = MisuseCaseParameters(mc.name(),mc.environmentProperties(),mc.risk())
    self.addMisuseCase(mcParameters,session)
    self.addTags(riskName,'risk',tags)
    self.commitDatabase(session)
    return riskId

  def updateRisk(self,parameters):
    riskId = parameters.id()
    threatName = parameters.threat()
    vulName = parameters.vulnerability()
    tags = parameters.tags()
    riskName = parameters.name()
    inTxt = parameters.intent()
    session = self.updateDatabase('call updateRisk(:threat,:vuln,:rId,:risk,:txt)',{'threat':threatName,'vuln':vulName,'rId':riskId,'risk':riskName,'txt':inTxt},'MySQL error updating risk',None,False)
    self.commitDatabase(session)

    mc = parameters.misuseCase()
    mcName = 'Exploit ' + riskName
    mcId,oldMcName = self.responseList('call riskMisuseCase(:id)',{'id':riskId},'MySQL error getting risk misuse case')[0]
    mcParameters = MisuseCaseParameters(mcName,mc.environmentProperties(),riskName)
    mcParameters.setId(mcId)
    self.updateMisuseCase(mcParameters,session)
    self.addTags(riskName,'risk',tags)
    self.commitDatabase(session)

  def deleteRisk(self,riskId):
    self.deleteObject(riskId,'risk')
    

  def deleteMisuseCase(self,mcId): self.deleteObject(mcId,'misusecase')
    
  def getResponses(self,constraintId = -1):
    return self.populateResponses(self.responseList('call getResponses(:id)',{'id':constraintId},'MySQL error getting responses'))

  def getPersonalResponses(self):
    return self.populateResponses(self.responseList('call getPersonalResponses()',{},'MySQL error getting personal responses'))

  def populateResponses(self,responseRows):
    responses = {}
    for respId,respName,respType,respRisk in responseRows:
      tags = self.getTags(respName,'response')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(respId,'response'):
        if (respType == 'Accept'):
          respCost = self.responseCost(respId,environmentId)
          respDescription = self.responseDescription(respId,environmentId)
          properties = AcceptEnvironmentProperties(environmentName,respCost,respDescription)
          environmentProperties.append(properties) 
        elif (respType == 'Transfer'):
          respDescription = self.responseDescription(respId,environmentId)
          respRoles = self.responseRoles(respId,environmentId)
          properties = TransferEnvironmentProperties(environmentName,respDescription,respRoles)
          environmentProperties.append(properties) 
        else:
          mitType = self.mitigationType(respId,environmentId)
          detPoint = ''
          detMechs = []
          if (mitType == 'Detect'):
            detPoint = self.detectionPoint(respId,environmentId)
          elif (mitType == 'React'):
            detMechs = self.detectionMechanisms(respId,environmentId)
          properties = MitigateEnvironmentProperties(environmentName,mitType,detPoint,detMechs)
          environmentProperties.append(properties) 
       
      parameters = ResponseParameters(respName,respRisk,tags,environmentProperties,respType)
      response = ObjectFactory.build(respId,parameters)
      responses[respName] = response
    return responses

  def responseCost(self,responseId,environmentId):
    return self.responseList('select responseCost(:rId,:eId)',{'rId':responseId,'eId':environmentId},'MySQL error getting cost associated with response id ' + str(responseId) + ' in environment ' + str(environmentId))[0]

  def responseDescription(self,responseId,environmentId):
    return self.responseList('select responseDescription(:rId,:eId)',{'rId':responseId,'eId':environmentId},'MySQL error getting description associated with response id ' + str(responseId) + ' in environment ' + str(environmentId))[0]

  def responseRoles(self,responseId,environmentId):
    return self.responseList('call responseRoles(:rId,:eId)',{'rId':responseId,'eId':environmentId},'MySQL error getting roles associated with response id ' + str(responseId) + ' in environment ' + str(environmentId))

  def mitigationType(self,responseId,environmentId):
    return self.responseList('select mitigationType(:rId,:eId)',{'rId':responseId,'eId':environmentId},'MySQL error getting mitigation type associated with response id ' + str(responseId) + ' in environment ' + str(environmentId))[0]


  def riskComponents(self,riskName):
    row = self.responseList('call riskComponents(:rId)',{'rId':riskName},'MySQL error getting risk components')[0]
    threatName = row[0]
    vulName = row[1]
    return [threatName,vulName]

  def addResponse(self,parameters):
    parameters.validate()
    respName = parameters.name()
    respRisk = parameters.risk()
    respType = parameters.responseType()
    tags = parameters.tags()
    respId = self.newId()
    self.updateDatabase('call addResponse(:id,:name,:type,:risk)',{'id':respId,'name':respName,'type':respType,'risk':respRisk},'MySQL error adding response')
    self.addTags(respName,'response',tags)
    for cProperties in parameters.environmentProperties():
      cProperties.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(respId,'response',environmentName)
      if (respType == 'Accept'):
        self.addResponseCost(respId,cProperties.cost(),environmentName)
        self.addResponseDescription(respId,cProperties.description(),environmentName)
      elif (respType == 'Transfer'):
        self.addResponseDescription(respId,cProperties.description(),environmentName)
        self.addResponseRoles(respId,cProperties.roles(),environmentName,cProperties.description())
      else:
        mitType = cProperties.type()
        self.addMitigationType(respId,mitType,environmentName)
        if (mitType == 'Detect'):    
          self.addDetectionPoint(respId,cProperties.detectionPoint(),environmentName)
        elif (mitType == 'React'):
         for detMech in cProperties.detectionMechanisms():
           self.addReactionDetectionMechanism(respId,detMech,environmentName)
    return respId

  def addMitigationType(self,responseId,mitType,environmentName):
    self.updateDatabase('call add_response_mitigate(:rId,:env,:type)',{'rId':responseId,'env':environmentName,'type':mitType},'MySQL error adding mitigation type')

  def addResponseCost(self,responseId,costName,environmentName):
    self.updateDatabase('call addResponseCost(:rId,:name,:env)',{'rId':responseId,'name':costName,'env':environmentName},'MySQL error adding response cost')
  def addResponseDescription(self,responseId,descriptionText,environmentName):
    self.updateDatabase('call addResponseDescription(:id,:desc,:env)',{'id':responseId,'desc':descriptionText,'env':environmentName},'MySQL error adding response description')

  def addResponseRoles(self,responseId,roles,environmentName,respDesc):
    session = self.conn()
    for role,cost in roles:
      self.updateDatabase('call addResponseRole(:id,:role,:cost,:env,:desc)',{'id':responseId,'role':role,'cost':cost,'env':environmentName,'desc':respDesc},'MySQL error adding response role',session,False)
    self.commitDatabase(session)

  def updateResponse(self,parameters):
    parameters.validate()
    respName = parameters.name()
    respRisk = parameters.risk()
    respType = parameters.responseType()
    tags = parameters.tags()
    respId = parameters.id()
    session = self.updateDatabase('call deleteResponseComponents(:id)',{'id':respId},'MySQL error deleting response components',None,False)
    self.updateDatabase('call updateResponse(:id,:name,:type,:risk)',{'id':respId,'name':respName,'type':respType,'risk':respRisk},'MySQL error updating response',session)
    self.addTags(respName,'response',tags)
    for cProperties in parameters.environmentProperties():
      cProperties.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(respId,'response',environmentName)
      if (respType == 'Accept'):
        self.addResponseCost(respId,cProperties.cost(),environmentName)
        self.addResponseDescription(respId,cProperties.description(),environmentName)
      elif (respType == 'Transfer'):
        self.addResponseDescription(respId,cProperties.description(),environmentName)
        self.addResponseRoles(respId,cProperties.roles(),environmentName,cProperties.description())
      else:
        mitType = cProperties.type()
        self.addMitigationType(respId,mitType,environmentName)
        if (mitType == 'Detect'):    
          self.addDetectionPoint(respId,cProperties.detectionPoint(),environmentName)
        elif (mitType == 'React'):
         for detMech in cProperties.detectionMechanisms():
           self.addReactionDetectionMechanism(respId,detMech,environmentName)

  def detectionPoint(self,responseId,environmentId):
    return self.responseList('select mitigatePoint(:rId,:eId)',{'rId':responseId,'eId':environmentId},'MySQL error getting detection point for detection response id ' + str(responseId))[0]

  def addDetectionPoint(self,mitId,detPoint,environmentName):
    self.updateDatabase('call add_mitigate_point(:id,:env,:point)',{'id':mitId,'env':environmentName,'point':detPoint},'MySQL error adding detection point')
  def addReactionDetectionMechanism(self,mitId,detMech,environmentName):
    self.updateDatabase('call add_reaction_detection_mechanism(:id,:methc,:env)',{'id':mitId,'metch':detMech,'env':environmentName},'MySQL error adding reaction detection mechanism')

  def detectionMechanisms(self,responseId,environmentId):
    return self.responseList('call detectionMechanisms(:rId,:eId)',{'rId':responseId,'eId':environmentId},'MySQL error getting detection mechanisms for detection response id ' + str(responseId))

  def riskAnalysisModel(self,environmentName,dimensionName='',objectName=''):
    if (dimensionName == 'risk' and objectName !='') or (objectName != '' and self.isRisk(objectName)):
      return self.riskModel(environmentName,objectName)

    traceRows = self.responseList('call riskAnalysisModel(:env)',{'env':environmentName},'MySQL error getting risk analysis model')
    traces = []
    for fromObjt,fromName,toObjt,toName in traceRows:
      if (dimensionName != ''):
        if (fromObjt != dimensionName) and (toObjt != dimensionName): continue
      if (objectName != ''):
        if (fromName != objectName) and (toName != objectName): continue
      parameters = DotTraceParameters(fromObjt,fromName,toObjt,toName)
      traces.append(ObjectFactory.build(-1,parameters))
    return traces

  def removableTraces(self,environmentName):
    traceRows = self.responseList('call viewRemovableTraces(:env)',{'env':environmentName},'MySQL error getting removable trace relations')
    traces = []
    for fromObjt,fromName,toObjt,toName,lbl in traceRows:
      if (fromObjt == 'task' and toObjt == 'asset'):
        continue
      traces.append((fromObjt,fromName,toObjt,toName,lbl))
    return traces

  def allowableTraceDimension(self,fromId,toId):
    return self.responseList('call allowableTraceDimension(:frm,:to)',{'frm':fromId,'to':toId},'MySQL error getting allowable trace dimensions for from_id ' + str(fromId) + ' and to_id ' + str(toId))[0]

  def reportDependencies(self,dimName,objtId):
    return self.responseList('call reportDependents(:id,:name)',{'id':objtId,'name':dimName},'MySQL error getting dependencies for ' + dimName + ' id ' + str(objtId))

  def deleteDependencies(self,deps):
    for dep in deps:
      dimName = dep[0]
      if (dimName == 'architectural_pattern'):
        dimName = 'component_view'
      objtId = dep[1]
      self.deleteObject(objtId,dimName)
    

  def threatenedAssets(self,threatId,environmentId):
    return self.responseList('call threat_asset(:tId,:eId)',{'tId':threatId,'eId':environmentId},'MySQL error getting assets associated with threat id ' + str(threatId) + ' in environment id ' + str(environmentId))

  def vulnerableAssets(self,vulId,environmentId):
    return self.responseList('call vulnerability_asset(:vId,:eId)',{'vId':vulId,'eId':environmentId},'MySQL error getting assets associated with vulnerability id ' + str(vulId) + ' in environment id ' + str(environmentId))

  def addTrace(self,traceTable,fromId,toId,label = 'supports'):
    if (traceTable != 'requirement_task' and traceTable != 'requirement_usecase' and traceTable != 'requirement_requirement'):
      self.updateDatabase('insert into ' + traceTable + ' values(:fromId,:toId)',{'fromId':fromId,'toId':toId},'MySQL error adding trace')
    elif (traceTable == 'requirement_requirement'):
      self.updateDatabase('insert into ' + traceTable + ' values(:fromId,:toId,":label")',{'fromId':fromId,'toId':toId,'label':label},'MySQL error adding trace')
    else:
      refTypeId = self.getDimensionId(label,'reference_type')
      self.updateDatabase('insert into ' + traceTable + ' values(:fromId,:toId,:refTypeId)',{'fromId':fromId,'toId':toId,'refTypeId':refTypeId},'MySQL error adding trace')

  def deleteEnvironment(self,environmentId):
    try: 
      curs = self.conn.connection().connection.cursor()
      sqlTxt = 'call delete_environment(%s)'
      curs.execute(sqlTxt,[environmentId])
      session = self.conn()
      session.commit()
      curs.close()
    except IntegrityError as e:
      exceptionText = 'Cannot remove environment due to dependent data (' + str(e) + ').'
      raise IntegrityException(exceptionText) 
    except OperationalError as e:
      exceptionText = 'MySQL error deleting environments (' + format(e) + ')'
      raise DatabaseProxyException(exceptionText)  
    except DatabaseError as e:
      exceptionText = 'MySQL error deleting environments (' + str(e) + ')'
      raise DatabaseProxyException(exceptionText)  

  def riskRating(self,riskId,thrName,vulName,environmentName):
    return self.responseList('call riskRating(:riskId,:thr,:vuln,:env)',{'riskId':riskId,'thr':thrName,'vuln':vulName,'env':environmentName},'MySQL error rating risk associated with threat/vulnerability/environment ' + thrName + '/' + vulName + '/' + environmentName)[0]


  def riskScore(self,threatName,vulName,environmentName,riskName = ''):
    return self.responseList('call riskScore(:threat,:vuln,:env,:risk)',{'threat':threatName,'vuln':vulName,'env':environmentName,'risk':riskName},'MySQL error rating risk associated with risk ' + riskName)

  def targetNames(self,reqList,envName):
    targetDict = {}
    for reqLabel in reqList:
      reqTargets = self.reqTargetNames(reqLabel,envName)
      for target in reqTargets:
        if target in targetDict:
          for x in reqTargets:
            targetDict[target].add(x)
        else:
          targetDict[target] = reqTargets[target]
    return targetDict

  def reqTargetNames(self,reqLabel,envName):
    rows = self.responseList('call targetNames(:req,:env)',{'req':reqLabel,'env':envName},'MySQL error getting target names')
    targets = {}
    for targetName,responseName in rows:
      if (targetName in targets): targets[targetName].add(responseName)
      else:
        targets[targetName] = set([responseName])
    return targets

  def getRoles(self,constraintId = -1):
    roleRows = self.responseList('call getRoles(:id)',{'id':constraintId},'MySQL error getting roles')
    roles = {}
    for roleId,roleName,roleType,shortCode,roleDescription in roleRows:
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(roleId,'role'):
        roleResponses = self.roleResponsibilities(roleId,environmentId)
        roleCountermeasures = self.roleCountermeasures(roleId,environmentId)
        roleGoals = self.roleGoals(roleId,environmentId)
        roleRequirements = self.roleRequirements(roleId,environmentId)
        properties = RoleEnvironmentProperties(environmentName,roleResponses,roleCountermeasures,roleGoals,roleRequirements)
        environmentProperties.append(properties)
      parameters = RoleParameters(roleName,roleType,shortCode,roleDescription,environmentProperties)
      role = ObjectFactory.build(roleId,parameters)
      roles[roleName] = role
    return roles

  def addRole(self,parameters):
    parameters.validate()
    roleId = self.newId()
    roleName = parameters.name()
    roleType = parameters.type()
    shortCode = parameters.shortCode()
    roleDesc = parameters.description()
    self.updateDatabase('call addRole(:id,:name,:type,:shortCode,:desc)',{'id':roleId,'name':roleName,'type':roleType,'shortCode':shortCode,'desc':roleDesc},'MySQL error adding role')
    return roleId

  def updateRole(self,parameters):
    parameters.validate()
    roleId = parameters.id()
    roleName = parameters.name()
    roleType = parameters.type()
    shortCode = parameters.shortCode()
    roleDesc = parameters.description()
    self.updateDatabase('call updateRole(:id,:name,:type,:shortCode,:desc)',{'id':roleId,'name':roleName,'type':roleType,'shortCode':shortCode,'desc':roleDesc},'MySQL error updating role')
    return roleId

  def deleteRole(self,roleId):
    self.deleteObject(roleId,'role')
    

  def roleResponsibilities(self,roleId,environmentId):
    return self.responseList('call roleResponses(:rId,:eId)',{'rId':roleId,'eId':environmentId},'MySQL error getting responses for role id ' + str(roleId) + ' in environment ' + str(environmentId))

  def roleCountermeasures(self,roleId,environmentId):
    return self.responseList('call roleCountermeasures(:rId,:eId)',{'rId':roleId,'eId':environmentId},'MySQL error getting countermeasures for role id ' + str(roleId) + ' in environment ' + str(environmentId))

  def roleGoals(self,roleId,environmentId):
    return self.responseList('call roleGoalResponsibilities(:rId,:eId)',{'rId':roleId,'eId':environmentId},'MySQL error getting goals for role id ' + str(roleId) + ' in environment ' + str(environmentId))

  def roleRequirements(self,roleId,environmentId):
    return self.responseList('call roleRequirementResponsibilities(:rId,:eId)',{'rId':roleId,'eId':environmentId},'MySQL error getting requirements for role id ' + str(roleId) + ' in environment ' + str(environmentId))


  def getCountermeasures(self,constraintId = -1):
    cmRows = self.responseList('call getCountermeasures(:id)',{'id':constraintId},'MySQL error getting countermeasures')
    countermeasures = {}
    for cmId,cmName,cmDesc,cmType in cmRows:
      tags = self.getTags(cmName,'countermeasure')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(cmId,'countermeasure'):
        reqs,targets = self.countermeasureTargets(cmId,environmentId)
        properties,pRationale = self.relatedProperties('countermeasure',cmId,environmentId)
        cost = self.countermeasureCost(cmId,environmentId)
        roles = self.countermeasureRoles(cmId,environmentId)
        personas = self.countermeasurePersonas(cmId,environmentId)
        properties = CountermeasureEnvironmentProperties(environmentName,reqs,targets,properties,pRationale,cost,roles,personas)
        environmentProperties.append(properties) 
      parameters = CountermeasureParameters(cmName,cmDesc,cmType,tags,environmentProperties)
      countermeasure = ObjectFactory.build(cmId,parameters)
      countermeasures[cmName] = countermeasure
    return countermeasures

  def countermeasureCost(self,cmId,environmentId):
    return self.responseList('select countermeasureCost(:cmId,:envId)',{'cmId':cmId,'envId':environmentId},'MySQL error getting cost associated with countermeasure id ' + str(cmId))[0]

  def countermeasureTargets(self,cmId,environmentId):
    reqs = self.responseList('call countermeasureRequirements(:cmId,:envId)',{'cmId':cmId,'envId':environmentId},'MySQL error getting requirements with countermeasure id ' + str(cmId))
    targets = self.responseList('call countermeasureTargets(:cmId,:envId)',{'cmId':cmId,'envId':environmentId},'MySQL error getting targets with countermeasure id ' + str(cmId))
    return (reqs,targets)

  def countermeasureRoles(self,cmId,environmentId):
    return self.responseList('call countermeasureRoles(:cmId,:envId)',{'cmId':cmId,'envId':environmentId},'MySQL error getting roles associated with countermeasure id ' + str(cmId))

  def countermeasurePersonas(self,cmId,environmentId):
    return self.responseList('call countermeasurePersonas(:cmId,:envId)',{'cmId':cmId,'envId':environmentId},'MySQL error getting personas associated with countermeasure id ' + str(cmId))

  def addCountermeasure(self,parameters):
    parameters.validate()
    cmName = parameters.name()
    cmDesc = parameters.description()
    cmType = parameters.type()
    tags = parameters.tags()
    cmId = self.newId()
    self.updateDatabase('call addCountermeasure(:id,:name,:desc,:type)',{'id':cmId,'name':cmName,'desc':cmDesc,'type':cmType},'MySQL error adding countermeasure')
    self.addTags(cmName,'countermeasure',tags)
    for cProperties in parameters.environmentProperties():
      cProperties.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(cmId,'countermeasure',environmentName)
      self.addCountermeasureTargets(cmId,cProperties.requirements(),cProperties.targets(),environmentName)
      self.addSecurityProperties('countermeasure',cmId,environmentName,cProperties.properties(),cProperties.rationale())
      self.addCountermeasureCost(cmId,cProperties.cost(),environmentName)
      self.addCountermeasureRoles(cmId,cProperties.roles(),environmentName)
      self.addCountermeasurePersonas(cmId,cProperties.personas(),environmentName)
      self.addRequirementRoles(cmName,cProperties.roles(),cProperties.requirements(),environmentName)
    return cmId

  def updateCountermeasure(self,parameters):
    parameters.validate()
    cmName = parameters.name()
    cmDesc = parameters.description()
    cmType = parameters.type()
    tags = parameters.tags()
    cmId = parameters.id()
    environmentProperties = parameters.environmentProperties()
    session = self.updateDatabase('call deleteCountermeasureComponents(:id)',{'id':cmId},'MySQL error deleting countermeasure components')
    self.updateDatabase('call updateCountermeasure(:id,:name,:desc,:type)',{'id':cmId,'name':cmName,'desc':cmDesc,'type':cmType},'MySQL error updating countermeasures',session)
    self.addTags(cmName,'countermeasure',tags)
    for cProperties in environmentProperties:
      cProperties.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(cmId,'countermeasure',environmentName)
      self.updateCountermeasureTargets(cmId,cProperties.requirements(),cProperties.targets(),environmentName)
      self.addSecurityProperties('countermeasure',cmId,environmentName,cProperties.properties(),cProperties.rationale())
      self.addCountermeasureCost(cmId,cProperties.cost(),environmentName)
      self.addCountermeasureRoles(cmId,cProperties.roles(),environmentName)
      self.addCountermeasurePersonas(cmId,cProperties.personas(),environmentName)
      self.updateRequirementRoles(cmName,cProperties.roles(),cProperties.requirements(),environmentName)
    return cmId

  def addCountermeasureTargets(self,cmId,reqs,targets,environmentName):
    session = self.conn()
    for reqLabel in reqs:
      self.updateDatabase('call addCountermeasureRequirement(:cmId,:lbl,:env)',{'cmId':cmId,'lbl':reqLabel,'env':environmentName},'MySQL error adding countermeasure requirement',session,False)
    for target in targets:
      self.updateDatabase('call addCountermeasureTarget(:cmId,:name,:effectiveness,:rationale,:env)',{'cmId':cmId,'name':target.name(),'effectiveness':target.effectiveness(),'rationale':target.rationale(),'env':environmentName},'MySQL error adding countermeasure target',session,False)
    self.commitDatabase(session)

  def updateCountermeasureTargets(self,cmId,reqs,targets,environmentName):
    session = self.conn()
    for reqLabel in reqs:
      self.updateDatabase('call updateCountermeasureRequirement(:cmId,:lbl,:env)',{'cmId':cmId,'lbl':reqLabel,'env':environmentName},'MySQL error updating countermeasure requirement',session,False)
    for target in targets:
      self.updateDatabase('call addCountermeasureTarget(:cmId,:name,:effectiveness,:rationale,:env)',{'cmId':cmId,'name':target.name(),'effectiveness':target.effectiveness(),'rationale':target.rationale(),'env':environmentName},'MySQL error adding countermeasure target',session,False)
    self.commitDatabase(session)

  def addRequirementRoles(self, cmName,roles, requirements, environmentName):
    for role in roles:
      for requirement in requirements:
        self.addRequirementRole(cmName,role,requirement,environmentName)

  def updateRequirementRoles(self, cmName,roles, requirements, environmentName):
    for role in roles:
      for requirement in requirements:
        self.updateRequirementRole(cmName,role,requirement,environmentName)
          
  def deleteRequirementRoles(self, roles, requirements, environmentName):
    for role in roles:
      for requirement in requirements:
        self.deleteRequirementRole(role,requirement,environmentName)

  def addRequirementRole(self,cmName,roleName,reqName,envName):
    associationId = self.newId()
    self.updateDatabase('call addRequirementRole(:aId,:cm,:role,:req,:env)',{'aId':associationId,'cm':cmName,'role':roleName,'req':reqName,'env':envName},'MySQL error adding requirement role')

  def updateRequirementRole(self,cmName,roleName,reqName,envName):
    associationId = self.newId()
    self.updateDatabase('call updateRequirementRole(:aId,:cm,:role,:req,:env)',{'aId':associationId,'cm':cmName,'role':roleName,'req':reqName,'env':envName},'MySQL error updating requirement role')

  def deleteRequirementRole(self,roleName,reqName,envName):
    self.updateDatabase('call deleteRequirementRole(:role,:req,:env)',{'role':roleName,'req':reqName,'env':envName},'MySQL error deleting requirement role')

  def addCountermeasureCost(self,cmId,costName,environmentName):
    self.updateDatabase('call addCountermeasureCost(:cmId,:cost,:env)',{'cmId':cmId,'cost':costName,'env':environmentName},'MySQL error adding countermeasure cost')

  def addCountermeasureRoles(self,cmId,roles,environmentName):
    session = self.conn()
    for role in roles:
      self.updateDatabase('call addCountermeasureRole(:cmId,:role,:env)',{'cmId':cmId,'role':role,'env':environmentName},'MySQL error adding countermeasure role',session,False)
    self.commitDatabase(session)

  def addCountermeasurePersonas(self,cmId,personas,environmentName):
    session = self.conn()
    for task,persona,duration,frequency,demands,goalSupport in personas:
      self.updateDatabase('call addCountermeasurePersona(:id,:persona,:task,:dur,:freq,:dem,:goal,:env)',{'id':cmId,'persona':persona,'task':task,'dur':duration,'freq':frequency,'dem':demands,'goal':goalSupport,'env':environmentName},'MySQL error adding countermeasure persona',session,False)
    self.commitDatabase(session)

  def personaNarrative(self,scId,environmentId):
    return self.responseList('select personaNarrative(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting narrative for persona id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def personaDirect(self,scId,environmentId):
    directFlag = self.responseList('select personaDirect(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting directFlag for persona id ' + str(scId) + ' in environment ' + str(environmentId))[0]
    directValue = 'False'
    if (directFlag == 1): directValue = 'True'
    return directValue
   

  def addPersonaNarrative(self,stId,environmentName,descriptionText):
    self.updateDatabase('call addPersonaNarrative(:stId,:desc,:env)',{'stId':stId,'desc':descriptionText,'env':environmentName},'MySQL error adding persona narrative')

  def addPersonaDirect(self,stId,environmentName,directText):
    self.updateDatabase('call addPersonaDirect(:stId,:txt,:env)',{'stId':stId,'txt':directText,'env':environmentName},'MySQL error adding persona direct flag')

  def taskNarrative(self,scId,environmentId):
    return self.responseList('select taskNarrative(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting narrative for task id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def taskConsequences(self,scId,environmentId):
    return self.responseList('select taskConsequences(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting consequences for task id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def taskBenefits(self,scId,environmentId):
    return self.responseList('select taskBenefits(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting benefits for task id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def addTaskNarrative(self,scId,narrativeText,cText,bText,environmentName):
    self.updateDatabase('call addTaskNarrative(:scId,:nTxt,:cTxt,:bTxt,:env)',{'scId':scId,'nTxt':narrativeText,'cTxt':cText,'bTxt':bText,'env':environmentName},'MySQL error adding task narrative')

  def misuseCaseNarrative(self,mcId,environmentId):
    return self.responseList('select misuseCaseNarrative(:mcId,:env)',{'mcId':mcId,'env':environmentId},'MySQL error getting narrative for misusecase id ' + str(mcId) + ' in environment ' + str(environmentId))[0]

  def addMisuseCaseNarrative(self,mcId,narrativeText,environmentName,session):
    self.updateDatabase('call addMisuseCaseNarrative(:mcId,:nTxt,:env)',{'mcId':mcId,'nTxt':narrativeText,'env':environmentName},'MySQL error adding misuse case narrative',session)

  def taskDependencies(self,tId,environmentId):
    return self.responseList('select taskDependencies(:tId,:eId)',{'tId':tId,'eId':environmentId},'MySQL error getting dependencies for task id ' + str(tId) + ' in environment ' + str(environmentId))[0]

  def addTaskDependencies(self,tId,depsText,environmentName):
    self.updateDatabase('call addTaskDependencies(:tId,:txt,:env)',{'tId':tId,'txt':depsText,'env':environmentName},'MySQL error adding task dependencies')

  def mitigatedRisks(self,cmId):
    return self.responseList('call mitigatedRisks(:id)',{'id':cmId},'MySQL error getting risks mitigated by countermeasure id ' + str(cmId))

  def deleteTrace(self,fromObjt,fromName,toObjt,toName):
    self.updateDatabase('call delete_trace(:fObj,:fName,:tObj,:tName)',{'fObj':fromObjt,'fName':fromName,'tObj':toObjt,'tName':toName},'MySQL error deleting trace')

  def deleteCountermeasure(self,cmId):
    self.deleteObject(cmId,'countermeasure')
    

  def addGoal(self,parameters):
    parameters.validate()
    goalId = self.newId()
    goalName = parameters.name()
    goalOrig = parameters.originator()
    tags = parameters.tags()
    self.updateDatabase('call addGoal(:id,:name,:orig)',{'id':goalId,'name':goalName,'orig':goalOrig},'MySQL error adding goal')
    self.addTags(goalName,'goal',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentProperties.validate()
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(goalId,'goal',environmentName)
      self.addGoalDefinition(goalId,environmentName,environmentProperties.definition())
      self.addGoalCategory(goalId,environmentName,environmentProperties.category())
      self.addGoalPriority(goalId,environmentName,environmentProperties.priority())
      self.addGoalFitCriterion(goalId,environmentName,environmentProperties.fitCriterion())
      self.addGoalIssue(goalId,environmentName,environmentProperties.issue())
      self.addGoalRefinements(goalId,goalName,environmentName,environmentProperties.goalRefinements(),environmentProperties.subGoalRefinements())
      self.addGoalConcerns(goalId,environmentName,environmentProperties.concerns())
      self.addGoalConcernAssociations(goalId,environmentName,environmentProperties.concernAssociations())
      gp = environmentProperties.policy()
      if (gp != None):
        self.addGoalPolicy(goalId,environmentName,gp['theSubject'],gp['theAccessType'],gp['theResource'],gp['thePermission'])
    return goalId

  def updateGoal(self,parameters):
    parameters.validate()
    goalId = parameters.id()
    goalName = parameters.name()
    goalOrig = parameters.originator()
    tags = parameters.tags()
    session = self.updateDatabase('call deleteGoalComponents(:id)',{'id':goalId},'MySQL error deleting goal components',None,False)
    self.updateDatabase('call updateGoal(:id,:name,:orig)',{'id':goalId,'name':goalName,'orig':goalOrig},'MySQL error updating goal',session)
    self.addTags(goalName,'goal',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentProperties.validate()
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(goalId,'goal',environmentName)
      self.addGoalDefinition(goalId,environmentName,environmentProperties.definition())
      self.addGoalCategory(goalId,environmentName,environmentProperties.category())
      self.addGoalPriority(goalId,environmentName,environmentProperties.priority())
      self.addGoalFitCriterion(goalId,environmentName,environmentProperties.fitCriterion())
      self.addGoalIssue(goalId,environmentName,environmentProperties.issue())
      self.addGoalRefinements(goalId,goalName,environmentName,environmentProperties.goalRefinements(),environmentProperties.subGoalRefinements())
      self.addGoalConcerns(goalId,environmentName,environmentProperties.concerns())
      self.addGoalConcernAssociations(goalId,environmentName,environmentProperties.concernAssociations())
      gp = environmentProperties.policy()
      if (gp != None):
        self.addGoalPolicy(goalId,environmentName,gp['theSubject'],gp['theAccessType'],gp['theResource'],gp['thePermission'])

  def getGoals(self,constraintId = -1):
    goalRows = self.responseList('call getGoals(:id)',{'id':constraintId},'MySQL error getting goals')
    goals = {}
    for goalId,goalName,goalOrig in goalRows:
      tags = self.getTags(goalName,'goal')
      environmentProperties = self.goalEnvironmentProperties(goalId)
      parameters = GoalParameters(goalName,goalOrig,tags,self.goalEnvironmentProperties(goalId))
      goal = ObjectFactory.build(goalId,parameters)
      goals[goalName] = goal
    return goals

  def getColouredGoals(self,constraintId = -1):
    goalRows = self.responseList('call getColouredGoals(:id)',{'id':constraintId},'MySQL error getting coloured goals')
    goals = {}
    for goalId,goalName,goalOrig,goalColour in goalRows:
      tags = self.getTags(goalName,'goal')
      environmentProperties = self.goalEnvironmentProperties(goalId)
      parameters = GoalParameters(goalName,goalOrig,tags,self.goalEnvironmentProperties(goalId))
      goal = ObjectFactory.build(goalId,parameters)
      goal.setColour(goalColour)
      goals[goalName] = goal
    return goals


  def goalEnvironmentProperties(self,goalId):
    environmentProperties = []
    for environmentId,environmentName in self.dimensionEnvironments(goalId,'goal'):
      goalLabel = self.goalLabel(goalId,environmentId)
      goalDef = self.goalDefinition(goalId,environmentId)
      goalType = self.goalCategory(goalId,environmentId)
      goalPriority = self.goalPriority(goalId,environmentId)
      goalFitCriterion = self.goalFitCriterion(goalId,environmentId)
      goalIssue = self.goalIssue(goalId,environmentId) 
      goalRefinements,subGoalRefinements = self.goalRefinements(goalId,environmentId)
      concerns = self.goalConcerns(goalId,environmentId)
      concernAssociations = self.goalConcernAssociations(goalId,environmentId)
      gp = self.goalPolicy(goalId,environmentId)
      properties = GoalEnvironmentProperties(environmentName,goalLabel,goalDef,goalType,goalPriority,goalFitCriterion,goalIssue,goalRefinements,subGoalRefinements,concerns,concernAssociations,gp)
      environmentProperties.append(properties) 
    return environmentProperties

  def deleteGoal(self,goalId):
    self.deleteObject(goalId,'goal')
    

  def roleTasks(self,environmentName,roles):
    tpSet = set([])
    for role in roles:
      rows = self.responseList('call countermeasureTaskPersonas(:role,:env)',{'role':role,'env':environmentName},'MySQL error getting role tasks')
      for taskName,personaName in rows:
        tpSet.add((taskName,personaName))
    tpDict = {}
    for taskName,personaName in tpSet:
      tpDict[(taskName,personaName)] = ['None','None','None','None']
    return tpDict

  def taskUsabilityScore(self,taskName,environmentName):
    return int(self.responseList('select task_usability(:task,:env)',{'task':taskName,'env':environmentName},'MySQL error getting task usability')[0])

  def taskLoad(self,taskId,environmentId):
    return self.responseList('select usability_score(:tId,:eId)',{'tId':taskId,'eId':environmentId},'MySQL error getting task load')[0]

  def countermeasureLoad(self,taskId,environmentId):
    return self.responseList('select hindrance_score(:tId,:eId)',{'tId':taskId,'eId':environmentId},'MySQL error getting task countermeasure load')[0]

  def environmentDimensions(self,dimension,envName): return self.responseList('call ' + dimension + 'Names(:env)',{'env':envName},'MySQL error getting ' + dimension + 's associated with environment ' + envName)

  def environmentAssets(self,envName): return self.environmentDimensions('asset',envName)

  def environmentGoals(self,envName): return self.environmentDimensions('goal',envName)

  def environmentObstacles(self,envName): return self.environmentDimensions('obstacle',envName)

  def environmentDomainProperties(self,envName): return self.environmentDimensions('domainProperty',envName)

  def environmentCountermeasures(self,envName): return self.environmentDimensions('countermeasure',envName)

  def environmentTasks(self,envName): return self.environmentDimensions('task',envName)

  def environmentThreats(self,envName): return self.environmentDimensions('threat',envName)

  def environmentVulnerabilities(self,envName): return self.environmentDimensions('vulnerability',envName)

  def environmentUseCases(self,envName): return self.environmentDimensions('usecase',envName)

  def environmentMisuseCases(self,envName): return self.environmentDimensions('misusecase',envName)

  def goalModelElements(self,envName): 
    return self.responseList('call goalModelElements(:env)',{'env':envName},'MySQL error getting goal model elements')

  def obstacleModelElements(self,envName):
    return self.responseList('call obstacleModelElements(:env)',{'env':envName},'MySQL error getting obstacle model elements')

  def responsibilityModelElements(self,envName):
    return self.responseList('call responsibilityModelElements(:env)',{'env':envName},'MySQL error getting responsibility model elements')

  def taskModelElements(self,envName):
    return self.responseList('call taskModelElements(:env)',{'env':envName},'MySQL error getting task model elements')

  def classModelElements(self,envName,hideConcerns = False):
    callTxt = ''
    argDict = {'env':envName}
    if (hideConcerns == True):
      callTxt = 'call concernlessClassModelElements(:env)'
    else:
      callTxt = 'call classModelElements(:env)'
    return self.responseList(callTxt,argDict,'MySQL error getting class model elements')

  def classModel(self,envName,asName = '',hideConcerns = False):
    if (hideConcerns == True):
      if (asName == ''):
        return self.classAssociations('call concernlessClassModel(:id)',envName)
      else:
        return self.classTreeAssociations('call concernlessClassTree(:id1,:id2)',asName,envName)
    else:
      if (asName == ''):
        return self.classAssociations('call classModel(:id)',envName)
      else:
        return self.classTreeAssociations('call classTree(:id1,:id2)',asName,envName)


  def getClassAssociations(self,constraintId = ''):
    return self.classAssociations('call classAssociationNames(:id)',constraintId)


  def classAssociations(self,procName,constraintId = ''):
    rows = self.responseList(procName,{'id':constraintId},'MySQL error getting class associations')
    associations = {}
    for associationId,envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName,rationale in rows:
      parameters = ClassAssociationParameters(envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = envName + '/' + headName + '/' + tailName
      associations[asLabel] = association
    return associations

  def classTreeAssociations(self,procName,assetName,envName):
    rows = self.responseList(procName,{'id1':assetName,'id2':envName},'MySQL error getting class associations')
    associations = {}
    for associationId,envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName,rationale in rows:
      parameters = ClassAssociationParameters(envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = envName + '/' + headName + '/' + tailName
      associations[asLabel] = association
    return associations

  def addClassAssociation(self,parameters):
    parameters.validate()
    associationId = self.newId()
    envName = parameters.environment()
    headAsset = parameters.headAsset()
    headType = parameters.headType()
    headNav = parameters.headNavigation()
    headMult = parameters.headMultiplicity()
    headRole = parameters.headRole()
    tailRole = parameters.tailRole()
    tailMult = parameters.tailMultiplicity()
    tailNav = parameters.tailNavigation()
    tailType = parameters.tailType()
    tailAsset = parameters.tailAsset()
    assocRationale = parameters.rationale()
    self.checkAssetAssociation(envName,headAsset,tailAsset)
    self.updateDatabase('call addClassAssociation(:ass,:env,:hAss,:hType,:hNav,:hMult,:hRole,:tRole,:tMult,:tNav,:tType,:tAss,:rationale)',{'ass':associationId,'env':envName,'hAss':headAsset,'hType':headType,'hNav':headNav,'hMult':headMult,'hRole':headRole,'tRole':tailRole,'tMult':tailMult,'tNav':tailNav,'tType':tailType,'tAss':tailAsset,'rationale':assocRationale},'MySQL error adding class association')
    return associationId

  def updateClassAssociation(self,parameters):
    parameters.validate()
    associationId = parameters.id()
    envName = parameters.environment()
    headAsset = parameters.headAsset()
    headType = parameters.headType()
    headNav = parameters.headNavigation()
    headMult = parameters.headMultiplicity()
    headRole = parameters.headRole()
    tailRole = parameters.tailRole()
    tailMult = parameters.tailMultiplicity()
    tailNav = parameters.tailNavigation()
    tailType = parameters.tailType()
    tailAsset = parameters.tailAsset()
    assocRationale = parameters.rationale()
    self.updateDatabase('call updateClassAssociation(:ass,:env,:hAss,:hType,:hNav,:hMult,:hRole,:tRole,:tMult,:tNav,:tType,:tAss,:rationale)',{'ass':associationId,'env':envName,'hAss':headAsset,'hType':headType,'hNav':headNav,'hMult':headMult,'hRole':headRole,'tRole':tailRole,'tMult':tailMult,'tNav':tailNav,'tType':tailType,'tAss':tailAsset,'rationale':assocRationale},'MySQL error updating class association')

  def deleteClassAssociation(self,associationId):
    self.deleteObject(associationId,'classassociation')
    

  def goalModel(self,envName,goalName = '',topLevelGoals = 0,caseFilter = 0):
    if (goalName == ''):
      return self.goalAssociations('call goalModel(:id)',envName)
    else:
      return self.goalTreeAssociations('call goalTree(:id1,:id2,:id3,:id4)',goalName,envName,topLevelGoals,caseFilter)
   

  def responsibilityModel(self,envName,roleName = ''):
    if (roleName == ''):
      return self.goalAssociations('call responsibilityModel(:id)',envName)
    else:
      return self.goalTreeAssociations('call subResponsibilityModel(:id1,:id2)',envName,roleName)
 
  def obstacleModel(self,envName,goalName = '',topLevelGoals = 0):
    if (goalName == ''):
      return self.goalAssociations('call obstacleModel(:id)',envName)
    else:
      return self.goalTreeAssociations('call obstacleTree(:id1,:id2,:id3,:id4)',goalName,envName,topLevelGoals)
 


  def taskModel(self,envName,taskName = '',mcFilter=False):
    if (taskName == ''):
      return self.goalAssociations('call taskModel(:id)',envName)
    else:
      if (mcFilter == True):
        return self.goalTreeAssociations('call subMisuseCaseModel(:id1,:id2)',taskName,envName)
      else:
        return self.goalTreeAssociations('call subTaskModel(:id1,:id2)',taskName,envName)

  def getGoalAssociations(self,constraintId = ''):
    return self.goalAssociations('call goalAssociationNames(:id)',constraintId)

  def getGoalAssociation(self,envName,goalName,subGoalName):
    rows = self.responseList('call getGoalAssociation(:environment,:goal,:subgoal)',{'environment':envName,'goal':goalName,'subgoal':subGoalName},'MySQL error getting goal association')
    if (len(rows) == 0):
      raise DatabaseProxyException('Goal association ' + envName + '/' + goalName + '/' + subGoalName + ' not found')
    associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale = rows[0]
    parameters = GoalAssociationParameters(envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale)
    association = ObjectFactory.build(associationId,parameters)
    return association
    

  def goalAssociations(self,procName,constraintId = ''):
    rows = self.responseList(procName,{'id':constraintId},'MySQL error getting goal associations')
    associations = {}
    for associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale in rows:
      parameters = GoalAssociationParameters(envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = envName + '/' + goalName + '/' + subGoalName + '/' + aType
      associations[asLabel] = association
    return associations

  def riskObstacleModel(self,riskName,envName):
    rows = self.responseList('call riskObstacleTree(:risk,:env,0)',{'risk':riskName,'env':envName},'MySQL error getting risk obstacle model')
    associations = {}
    for associationId,envName,goalDim,goalName,aType,subGoalName,subGoalDim,alternativeId,rationale in rows:
      parameters = GoalAssociationParameters(envName,goalName,goalDim,aType,subGoalName,subGoalDim,alternativeId,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = envName + '/' + goalName + '/' + subGoalName + '/' + aType
      associations[asLabel] = association
    return associations


  def goalTreeAssociations(self,procName,goalName,envName,topLevelGoals = 0,caseFilter = 0):
    rows = []
    if (procName == 'call goalTree(:id1,:id2,:id3,:id4)') or (procName == 'call obstacleTree(:id1,:id2,:id3,:id4)'):
      rows = self.responseList(procName,{'id1':goalName,'id2':envName,'id3':topLevelGoals,'id4':caseFilter},'MySQL error getting goal tree associations')
    else:
      rows = self.responseList(procName,{'id1':goalName,'id2':envName},'MySQL error getting goal tree associations')
    associations = {}
    for associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale in rows:
      parameters = GoalAssociationParameters(envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = envName + '/' + goalName + '/' + subGoalName + '/' + aType
      associations[asLabel] = association
    return associations

  def addGoalAssociation(self,parameters):
    associationId = self.newId()
    envName = parameters.environment()
    goalName = parameters.goal()
    if (goalName == ''): return
    goalDimName = parameters.goalDimension()
    aType = parameters.type()
    subGoalName = parameters.subGoal()
    subGoalDimName = parameters.subGoalDimension()
    alternativeId = parameters.alternative()
    rationale = parameters.rationale()
    self.updateDatabase('call addGoalAssociation(:assId,:env,:goal,:dim,:type,:sGName,:sGDName,:altId,:rationale)',{'assId':associationId,'env':envName,'goal':goalName,'dim':goalDimName,'type':aType,'sGName':subGoalName,'sGDName':subGoalDimName,'altId':alternativeId,'rationale':rationale},'MySQL error adding goal association')
    return associationId

  def updateGoalAssociation(self,parameters):
    associationId = parameters.id()
    envName = parameters.environment()
    goalName = parameters.goal()
    goalDimName = parameters.goalDimension()
    aType = parameters.type()
    subGoalName = parameters.subGoal()
    subGoalDimName = parameters.subGoalDimension()
    alternativeId = parameters.alternative()
    rationale = parameters.rationale()
    self.updateDatabase('call updateGoalAssociation(:assId,:env,:goal,:dim,:type,:sGName,:sGDName,:altId,:rationale)',{'assId':associationId,'env':envName,'goal':goalName,'dim':goalDimName,'type':aType,'sGName':subGoalName,'sGDName':subGoalDimName,'altId':alternativeId,'rationale':rationale},'MySQL error updating goal association')

  def deleteGoalAssociation(self,associationId,goalDimName,subGoalDimName):
    self.updateDatabase('call delete_goalassociation(:ass,:gDName,:sGDName)',{'ass':associationId,'gDName':goalDimName,'sGDName':subGoalDimName},'MySQL error deleting goal association')

  def addGoalDefinition(self,goalId,environmentName,goalDef):
    self.updateDatabase('call addGoalDefinition(:gId,:env,:gDef)',{'gId':goalId,'env':environmentName,'gDef':goalDef},'MySQL error adding goal definition')

  def addGoalCategory(self,goalId,environmentName,goalCat):
    self.updateDatabase('call addGoalCategory(:gId,:env,:gCat)',{'gId':goalId,'env':environmentName,'gCat':goalCat},'MySQL error adding goal category')

  def addGoalPriority(self,goalId,environmentName,goalPri):
    self.updateDatabase('call addGoalPriority(:gId,:env,:gPri)',{'gId':goalId,'env':environmentName,'gPri':goalPri},'MySQL error adding goal priority')

  def addGoalFitCriterion(self,goalId,environmentName,goalFC):
    self.updateDatabase('call addGoalFitCriterion(:gId,:env,:gFC)',{'gId':goalId,'env':environmentName,'gFC':goalFC},'MySQL error adding goal fit criterion')

  def addGoalIssue(self,goalId,environmentName,goalIssue):
    self.updateDatabase('call addGoalIssue(:gID,:env,:gIssue)',{'gID':goalId,'env':environmentName,'gIssue':goalIssue},'MySQL error adding goal issue')

  def addGoalRefinements(self,goalId,goalName,environmentName,goalAssociations,subGoalAssociations):
    for goal,goalDim,refinement,altName,rationale in subGoalAssociations:
      alternativeId = 0
      if (altName == 'Yes'): alternativeId = 1
      parameters = GoalAssociationParameters(environmentName,goalName,'goal',refinement,goal,goalDim,alternativeId,rationale)
      self.addGoalAssociation(parameters) 
    for goal,goalDim,refinement,altName,rationale in goalAssociations:
      alternativeId = 0
      if (altName == 'Yes'): alternativeId = 1
      parameters = GoalAssociationParameters(environmentName,goal,goalDim,refinement,goalName,'goal',alternativeId,rationale)
      self.addGoalAssociation(parameters) 

  def addGoalConcernAssociations(self,goalId,environmentName,associations):
    for source,sourceMultiplicity,link,target,targetMultiplicity in associations:
      self.addGoalConcernAssociation(goalId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity) 

  def addGoalConcernAssociation(self,goalId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity):
    self.updateDatabase('call addGoalConcernAssociation(:gId,:env,:src,:sMulti,:link,:trgt,:tMulti)',{'gId':goalId,'env':environmentName,'src':source,'sMulti':sourceMultiplicity,'link':link,'trgt':target,'tMulti':targetMultiplicity},'MySQL error adding goal concern association')

  def addTaskConcernAssociations(self,taskId,environmentName,associations):
    for source,sourceMultiplicity,link,target,targetMultiplicity in associations:
      self.addTaskConcernAssociation(taskId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity) 

  def addTaskConcernAssociation(self,taskId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity):
    self.updateDatabase('call addTaskConcernAssociation(:tId,:env,:src,:sMulti,:link,:trgt,:tMulti)',{'tId':taskId,'env':environmentName,'src':source,'sMulti':sourceMultiplicity,'link':link,'trgt':target,'tMulti':targetMultiplicity},'MySQL error adding task concern association')

  def addObstacleRefinements(self,goalId,goalName,environmentName,goalAssociations,subGoalAssociations):
    for goal,goalDim,refinement,altName,rationale in subGoalAssociations:
      alternativeId = 0
      if (altName == 'Yes'): alternativeId = 1
      parameters = GoalAssociationParameters(environmentName,goalName,'obstacle',refinement,goal,goalDim,alternativeId,rationale)
      self.addGoalAssociation(parameters) 
    for goal,goalDim,refinement,altName,rationale in goalAssociations:
      alternativeId = 0
      if (altName == 'Yes'): alternativeId = 1
      parameters = GoalAssociationParameters(environmentName,goal,goalDim,refinement,goalName,'obstacle',alternativeId,rationale)
      self.addGoalAssociation(parameters) 

  def addObstacleConcerns(self,obsId,environmentName,concerns):
    for concern in concerns:
      assetId = self.existingObject(concern,'asset')
      if assetId == -1:
        assetId = self.existingObject(concern,'template_asset')
        if assetId != -1:
          self.importTemplateAsset(concern,environmentName)
        else:
          exceptionText = 'Cannot add obstacle concern: asset or template asset ' + concern + ' does not exist.'
          raise DatabaseProxyException(exceptionText)
      self.addObstacleConcern(obsId,environmentName,concern)

  def addObstacleConcern(self,obsId,environmentName,concern):
    self.updateDatabase('call add_obstacle_concern(:oId,:env,:conc)',{'oId':obsId,'env':environmentName,'conc':concern},'MySQL error adding obstacle concern')

  def addGoalConcerns(self,obsId,environmentName,concerns):
    for concern in concerns:
      assetId = self.existingObject(concern,'asset')
      if assetId == -1:
        assetId = self.existingObject(concern,'template_asset')
        if assetId != -1:
          self.importTemplateAsset(concern,environmentName)
        else:
          exceptionText = 'Cannot add goal concern: asset or template asset ' + concern + ' does not exist.'
          raise DatabaseProxyException(exceptionText)
      self.addGoalConcern(obsId,environmentName,concern)


  def addGoalConcern(self,goalId,environmentName,concern):
    self.updateDatabase('call add_goal_concern(:goal,:env,:conc)',{'goal':goalId,'env':environmentName,'conc':concern},'MySQL error adding goal concern')

  def addAssetAssociations(self,assetId,assetName,environmentName,assetAssociations):
    for headNav,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailNav,tailAsset in assetAssociations:
      parameters = ClassAssociationParameters(environmentName,assetName,'asset',headNav,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailNav,'asset',tailAsset)
      self.addClassAssociation(parameters) 

  def goalLabel(self,goalId,environmentId):
    return self.responseList('select goal_label(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal label')[0]

  def goalDefinition(self,goalId,environmentId):
    return self.responseList('select goal_definition(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal definition')[0]

  def goalCategory(self,goalId,environmentId):
    return self.responseList('select goal_category(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal category')[0]

  def goalPriority(self,goalId,environmentId):
    return self.responseList('select goal_priority(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal priority')[0]

  def goalFitCriterion(self,goalId,environmentId):
    return self.responseList('select goal_fitcriterion(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal fit criterion')[0]

  def goalIssue(self,goalId,environmentId):
    return self.responseList('select goal_issue(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal issue')[0]

  def goalRefinements(self,goalId,environmentId):
    rows = self.responseList('call goalRefinements(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal refinements')
    goalRefinements = []
    for associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale in rows:
      altName = 'No'
      if (alternativeId == 1):
        altName = 'Yes'
      goalRefinements.append((goalName,goalDimName,aType,altName,rationale))
    rows = self.responseList('call subGoalRefinements(:gId,:eId)',{'gId':goalId,'eId':environmentId},'MySQL error getting goal refinements')
    subGoalRefinements = []
    for associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale in rows:
      altName = 'No'
      if (alternativeId == 1):
        altName = 'Yes'
      subGoalRefinements.append((subGoalName,subGoalDimName,aType,altName,rationale))
    return goalRefinements,subGoalRefinements 

  def assetAssociations(self,assetId,environmentId):
    rows = self.responseList('call assetAssociations(:aId,:eId)',{'aId':assetId,'eId':environmentId},'MySQL error getting asset associations')
    associations = []
    for associationId,envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName in rows:
      associations.append((headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailName))
    return associations

  def getDomainProperties(self,constraintId = -1):
    dpRows = self.responseList('call getDomainProperties(:id)',{'id':constraintId},'MySQL error getting domain properties')
    dps = {}
    for dpId,dpName,dpDesc,dpType,dpOrig in dpRows:
      tags = self.getTags(dpName,'domainproperty')
      parameters = DomainPropertyParameters(dpName,dpDesc,dpType,dpOrig,tags)
      dp = ObjectFactory.build(dpId,parameters)
      dps[dpName] = dp
    return dps

  def addDomainProperty(self,parameters):
    parameters.validate()
    dpId = self.newId()
    dpName = parameters.name()
    dpDesc = parameters.description()
    dpType = parameters.type()
    dpOrig = parameters.originator()
    tags = parameters.tags()
    self.updateDatabase('call addDomainProperty(:id,:name,:desc,:type,:orig)',{'id':dpId,'name':dpName,'desc':dpDesc,'type':dpType,'orig':dpOrig},'MySQL error adding domain property')
    self.addTags(dpName,'domainproperty',tags)
    session = self.conn()
    session.commit()
    return dpId

  def updateDomainProperty(self,parameters):
    parameters.validate()
    dpId = parameters.id()
    dpName = parameters.name()
    dpDesc = parameters.description()
    dpType = parameters.type()
    dpOrig = parameters.originator()
    tags = parameters.tags()
    self.updateDatabase('call updateDomainProperty(:id,:name,:desc,:type,:orig)',{'id':dpId,'name':dpName,'desc':dpDesc,'type':dpType,'orig':dpOrig},'MySQL error updating domain property')
    self.addTags(dpName,'domainproperty',tags)
    session = self.conn()
    session.commit()
    return dpId

  def deleteDomainProperty(self,dpId):
    self.deleteObject(dpId,'domainproperty')
    

  def getObstacles(self,constraintId = -1):
    obstacleRows = self.responseList('call getObstacles(:id)',{'id':constraintId},'MySQL error getting obstacles')
    obstacles = {}
    for obsId,obsName,obsOrig in obstacleRows:
      tags = self.getTags(obsName,'obstacle')
      environmentProperties = self.obstacleEnvironmentProperties(obsId)
      parameters = ObstacleParameters(obsName,obsOrig,tags,environmentProperties)
      obstacle = ObjectFactory.build(obsId,parameters)
      obstacles[obsName] = obstacle
    return obstacles

  def obstacleEnvironmentProperties(self,obsId):
    environmentProperties = []
    for environmentId,environmentName in self.dimensionEnvironments(obsId,'obstacle'):
      obsLabel = self.obstacleLabel(obsId,environmentId)
      obsDef,obsProb,obsProbRat = self.obstacleDefinition(obsId,environmentId)
      obsType = self.obstacleCategory(obsId,environmentId)
      goalRefinements,subGoalRefinements = self.goalRefinements(obsId,environmentId)
      concerns = self.obstacleConcerns(obsId,environmentId)
      properties = ObstacleEnvironmentProperties(environmentName,obsLabel,obsDef,obsType,goalRefinements,subGoalRefinements,concerns)
      properties.theProbability = obsProb
      properties.theProbabilityRationale = obsProbRat
      environmentProperties.append(properties) 
    return environmentProperties

  def obstacleDefinition(self,obsId,environmentId):
    obsDef = self.responseList('select obstacle_definition(:oId,:eId)',{'oId':obsId,'eId':environmentId},'MySQL error getting obstacle definition')[0]
    obsProb,obsProbRat = self.obstacleProbability(obsId,environmentId)
    return (obsDef,obsProb,obsProbRat)

  def obstacleProbability(self,obsId,environmentId):
    row = self.responseList('call obstacle_probability(:oId,:eId)',{'oId':obsId,'eId':environmentId},'MySQL error getting obstacle probability')[0]
    obsAttr = row[0]
    obsRationale = row[1]
    return obsAttr,obsRationale

  def obstacleCategory(self,obsId,environmentId):
    return self.responseList('select obstacle_category(:oId,:eId)',{'oId':obsId,'eId':environmentId},'MySQL error getting obstacle category')[0]

  def addObstacle(self,parameters):
    parameters.validate()
    obsId = self.newId()
    obsName = parameters.name()
    obsOrig = parameters.originator()
    tags = parameters.tags()
    self.updateDatabase('call addObstacle(:id,:name,:orig)',{'id':obsId,'name':obsName,'orig':obsOrig},'MySQL error adding obstacle')
    self.addTags(obsName,'obstacle',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentProperties.validate()
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(obsId,'obstacle',environmentName)
      self.addObstacleDefinition(obsId,environmentName,environmentProperties.definition(),environmentProperties.probability(),environmentProperties.probabilityRationale())
      self.addObstacleCategory(obsId,environmentName,environmentProperties.category())
      self.addObstacleRefinements(obsId,obsName,environmentName,environmentProperties.goalRefinements(),environmentProperties.subGoalRefinements())
      self.addObstacleConcerns(obsId,environmentName,environmentProperties.concerns())
    return obsId

  def updateObstacle(self,parameters):
    parameters.validate()
    obsId = parameters.id()
    obsName = parameters.name()
    obsOrig = parameters.originator()
    tags = parameters.tags()
    session = self.updateDatabase('call deleteObstacleComponents(:id)',{'id':obsId},'MySQL error deleting obstacle components',None,False)
    self.updateDatabase('call updateObstacle(:id,:name,:orig)',{'id':obsId,'name':obsName,'orig':obsOrig},'MySQL error updating obstacle',session)
    self.addTags(obsName,'obstacle',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentProperties.validate()
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(obsId,'obstacle',environmentName)
      self.addObstacleDefinition(obsId,environmentName,environmentProperties.definition(),environmentProperties.probability(),environmentProperties.probabilityRationale())
      self.addObstacleCategory(obsId,environmentName,environmentProperties.category())
      self.addObstacleRefinements(obsId,obsName,environmentName,environmentProperties.goalRefinements(),environmentProperties.subGoalRefinements())
      self.addObstacleConcerns(obsId,environmentName,environmentProperties.concerns())

  def addObstacleDefinition(self,obsId,environmentName,obsDef,obsProb,obsProbRat):
    self.updateDatabase('call addObstacleDefinition(:id,:env,:def,:prob,:probRat)',{'id':obsId,'env':environmentName,'def':obsDef,'prob':obsProb,'probRat':obsProbRat},'MySQL error adding obstacle definition')

  def addObstacleCategory(self,obsId,environmentName,obsCat):
    self.updateDatabase('call addObstacleCategory(:obs,:env,:cat)',{'obs':obsId,'env':environmentName,'cat':obsCat},'MySQL error adding obstacle category')

  def deleteObstacle(self,obsId):
    self.deleteObject(obsId,'obstacle')

  def updateSettings(self, projName, background, goals, scope, definitions, contributors,revisions,richPicture,fontSize = '7.5',fontName = 'Times New Roman'):
    session = self.updateDatabase('call updateProjectSettings(:proj,:bg,:goals,:scope,:picture,:fontSize,:font)',{'proj':projName,'bg':background,'goals':goals,'scope':scope,'picture':richPicture,'fontSize':fontSize,'font':fontName},'MySQL error updating project settings',None,False)
    self.updateDatabase('call deleteDictionary()',{},'MySQL error deleting directory',session,False)
    for entry in definitions:
      self.updateDatabase('call addDictionaryEntry(:e0,:e1)',{'e0':entry['name'],'e1':entry['value']},'MySQL error adding dictionary entry',session,False)
    self.updateDatabase('call deleteContributors()',{},'MySQL error deleting contributions',session,False)
    for entry in contributors:
      self.updateDatabase('call addContributorEntry(:e0,:e1,:e2,:e3)',{'e0':entry[0],'e1':entry[1],'e2':entry[2],'e3':entry[3]},'MySQL error adding contribution entry',session,False)
    self.updateDatabase('call deleteRevisions()',{},'MySQL error deleting revisions',session,False)
    for entry in revisions:
      self.updateDatabase('call addRevision(:e0,:e1,:e2)',{'e0':entry[0],'e1':entry[1],'e2':entry[2]},'MySQL error adding revision',session,False)
    self.commitDatabase(session)

  def getProjectSettings(self):
    rows = self.responseList('call getProjectSettings()',{},'MySQL error getting project settings')
    pSettings = {}
    for key,value in rows:
      pSettings[key] = value
    return pSettings
  
  def getDictionary(self):
    rows = self.responseList('call getDictionary()',{},'MySQL error getting dictionary')
    pDict = []
    for key,value in rows:
      pDict.append({'name' : key, 'value' : value})
    return pDict

  def getContributors(self):
    return self.responseList('call getContributors()',{},'MySQL error getting contributors')

  def getRevisions(self):
    return self.responseList('call getRevisions()',{},'MySQL error getting revisions')

  def getRequirementVersions(self,reqId):
    return self.responseList('call getRequirementVersions(:id)',{'id':reqId},'MySQL error getting requirement versions')

  def existingResponseGoal(self,responseId): return int(self.responseList('select existingResponseGoal(:id)',{'id':responseId},'MySQL error getting existing response goal')[0])

  def getValueTypes(self,dimName,envName = ''):
    customisableValues = set(['asset_value','threat_value','risk_class','countermeasure_value','capability','motivation','asset_type','threat_type','vulnerability_type','severity','likelihood','access_right','protocol','privilege','surface_type'])
    if (dimName not in customisableValues):
      exceptionText = 'Values for ' + dimName + ' are not customisable.'
      raise DatabaseProxyException(exceptionText) 
    values = []
    rows = self.responseList('call getCustomisableValues(:dim,:env)',{'dim':dimName,'env':envName},'MySQL error getting customisable values')
    for typeId,typeName,typeDesc,typeValue,typeRat in rows:
      parameters = ValueTypeParameters(typeName,typeDesc,dimName,envName,typeValue,typeRat)
      objt = ObjectFactory.build(typeId,parameters)
      values.append(objt)
    return values

  def deleteCapability(self,objtId): self.deleteValueType(objtId,'capability')

  def deleteMotivation(self,objtId): self.deleteValueType(objtId,'motivation')

  def deleteAssetType(self,objtId):
    self.deleteValueType(objtId,'asset_type')

  def deleteThreatType(self,objtId):
    self.deleteValueType(objtId,'threat_type')

  def deleteVulnerabilityType(self,objtId):
    self.deleteValueType(objtId,'vulnerability_type')

  def deleteValueType(self,objtId,value_type):
    self.deleteObject(objtId,value_type)
    
  def addValueType(self,parameters):
    if (parameters.id() != -1): valueTypeId = parameters.id()
    else:
      valueTypeId = self.newId()
    vtName = parameters.name()
    vtDesc = parameters.description()
    vtType = parameters.type()
    vtScore = parameters.score()
    if vtType == 'access_right' and vtScore == '':
      vtScore = 1
    elif vtScore == '': 
      vtScore = 0
    else:
      vtScore = int(vtScore)
      if (vtType == 'access_right' and vtScore == 0):
        raise DatabaseProxyException('Access right value cannot be set to 0')
    vtRat = parameters.rationale()
    if ((vtType == 'asset_value') or (vtType == 'threat_value') or (vtType == 'risk_class') or (vtType == 'countermeasure_value')):
      exceptionText = 'Cannot add ' + vtType + 's'
      raise DatabaseProxyException(exceptionText) 
    self.updateDatabase('call addValueType(:id,:name,:desc,:type,:score,:rat)',{'id':valueTypeId,'name':vtName,'desc':vtDesc,'type':vtType,'score':vtScore,'rat':vtRat},'MySQL error adding value type')

  def updateValueType(self,parameters):
    valueTypeId = parameters.id()
    vtName = parameters.name()
    vtDesc = parameters.description()
    vtType = parameters.type()
    envName = parameters.environment()
    vtScore = parameters.score()
    vtRat = parameters.rationale()
    if (vtType == 'access_right' and vtScore == 0):
      raise DatabaseProxyException('Access right value cannot be set to 0')
    self.updateDatabase('call updateValueType(:id,:name,:desc,:type,:env,:score,:rat)',{'id':valueTypeId,'name':vtName,'desc':vtDesc,'type':vtType,'env':envName,'score':vtScore,'rat':vtRat},'MySQL error updating value type')

  def getVulnerabilityDirectory(self,vulName = ''):
    return self.responseList('call getVulnerabilityDirectory(:vuln)',{'vuln':vulName},'MySQL error getting vulnerability directory')

  def getThreatDirectory(self,thrName = ''):
    return self.responseList('call getThreatDirectory(:threat)',{'threat':thrName},'MySQL error getting threat directory')

  def obstacleConcerns(self,obsId,envId):
    return self.responseList('call obstacleConcerns(:obs,:env)',{'obs':obsId,'env':envId},'MySQL error getting obstacle concerns')

  def goalConcerns(self,goalId,envId):
    return self.responseList('call goalConcerns(:goal,:env)',{'goal':goalId,'env':envId},'MySQL error getting goal concerns')

  def goalConcernAssociations(self,goalId,envId):
    return self.responseList('call goalConcernAssociations(:goal,:env)',{'goal':goalId,'env':envId},'MySQL error getting goal concern associations')

  def taskConcernAssociations(self,taskId,envId):
    return self.responseList('call taskConcernAssociations(:task,:env)',{'task':taskId,'env':envId},'MySQL error getting task concern associations')

  def getDependencies(self,constraintId = ''):
    depRows = self.responseList('call getDependencies(:id)',{'id':constraintId},'MySQL error getting dependencies')
    dependencies = {}
    for depId,envName,depender,dependee,dType,dependencyName,rationale in depRows:
      parameters = DependencyParameters(envName,depender,dependee,dType,dependencyName,rationale)
      dependency = ObjectFactory.build(depId,parameters)
      dLabel = envName + '/' + depender + '/' + dependee + '/' + dependencyName
      dependencies[dLabel] = dependency
    return dependencies

  def addDependency(self,parameters):
    depId = self.newId()
    envName = parameters.environment()
    depender = parameters.depender()
    dependee = parameters.dependee()
    dType = parameters.dependencyType()
    dependencyName = parameters.dependency()
    rationale = parameters.rationale()
    self.updateDatabase('call addDependency(:id,:env,:depender,:dependee,:type,:name,:rationale)',{'id':depId,'env':envName,'depender':depender,'dependee':dependee,'type':dType,'name':dependencyName,'rationale':rationale},'MySQL error adding dependency')
    return depId

  def updateDependency(self,parameters):
    depId = parameters.id()
    envName = parameters.environment()
    depender = parameters.depender()
    dependee = parameters.dependee()
    dType = parameters.dependencyType()
    dependencyName = parameters.dependency()
    rationale = parameters.rationale()
    self.updateDatabase('call updateDependency(:id,:env,:depender,:dependee,:type,:name,:rationale)',{'id':depId,'env':envName,'depender':depender,'dependee':dependee,'type':dType,'name':dependencyName,'rationale':rationale},'MySQL error updating dependency')

  def deleteDependency(self,depId,depType):
    self.updateDatabase('call delete_dependency(:id,:type)',{'id':depId,'type':depType},'MySQL error deleting dependency')

  def getDependencyTable(self,envName):
    return self.responseList('call dependencyTable(:env)',{'env':envName},'MySQL error getting dependency table')

  def getDependencyTables(self):
    envs = self.getEnvironmentNames()
    deps = {}
    session = self.conn()
    for env in envs:
      depRows = self.getDependencyTable(env)
      if (len(depRows) > 0):
        deps[env] = self.getDependencyTable(env)
    return deps

  def reportAssociationDependencies(self,fromAsset,toAsset,envName): return self.responseList('call associationDependencyCheck(:from,:to,:env)',{'from':fromAsset,'to':toAsset,'env':envName},'MySQL error reporting association dependencies')

  def reportAssociationTargetDependencies(self,assetProperties,toAsset,envName): return self.responseList('call associationTargetDependencyCheck(:a0,:a1,:a2,:a3,:a4,:a5,:a6,:a7,:to,:env)',{'a0':assetProperties[0],'a1':assetProperties[1],'a2':assetProperties[2],'a3':assetProperties[3],'a4':assetProperties[4],'a5':assetProperties[5],'a6':assetProperties[6],'a7':assetProperties[7],'to':toAsset,'env':envName},'MySQL error reporting association target dependencies')

  def addTemplateAsset(self,parameters):
    assetId = self.newId()
    assetName = parameters.name()
    shortCode = parameters.shortCode()
    assetDesc = parameters.description()
    assetSig = parameters.significance()
    assetType = parameters.type()
    surfaceType = parameters.surfaceType()
    accessRight = parameters.accessRight()
    cProp = parameters.confidentialityProperty()
    cRat = parameters.confidentialityRationale()
    iProp = parameters.integrityProperty()
    iRat = parameters.integrityRationale()
    avProp = parameters.availabilityProperty()
    avRat = parameters.availabilityRationale()
    acProp = parameters.accountabilityProperty()
    acRat = parameters.accountabilityRationale()
    anProp = parameters.anonymityProperty()
    anRat = parameters.anonymityRationale()
    panProp = parameters.pseudonymityProperty()
    panRat = parameters.pseudonymityRationale()
    unlProp = parameters.unlinkabilityProperty()
    unlRat = parameters.unlinkabilityRationale()
    unoProp = parameters.unobservabilityProperty()
    unoRat = parameters.unobservabilityRationale()
    tags = parameters.tags()
    ifs = parameters.interfaces()
    self.updateDatabase('call addTemplateAsset(:id,:name,:shortCode,:desc,:sig,:type,:surfType,:rights)',{'id':assetId,'name':assetName,'shortCode':shortCode,'desc':assetDesc,'sig':assetSig,'type':assetType,'surfType':surfaceType,'rights':accessRight},'MySQL error adding template asset')
    self.addTags(assetName,'template_asset',tags)
    self.addInterfaces(assetName,'template_asset',ifs)
    self.addTemplateAssetProperties(assetId,cProp,iProp,avProp,acProp,anProp,panProp,unlProp,unoProp,cRat,iRat,avRat,acRat,anRat,panRat,unlRat,unoRat)
    return assetId

  def updateTemplateAsset(self,parameters):
    assetId = parameters.id()
    assetName = parameters.name()
    shortCode = parameters.shortCode()
    assetDesc = parameters.description()
    assetSig = parameters.significance()
    assetType = parameters.type()
    surfaceType = parameters.surfaceType()
    accessRight = parameters.accessRight()
    cProp = parameters.confidentialityProperty()
    cRat = parameters.confidentialityRationale()
    iProp = parameters.integrityProperty()
    iRat = parameters.integrityRationale()
    avProp = parameters.availabilityProperty()
    avRat = parameters.availabilityRationale()
    acProp = parameters.accountabilityProperty()
    acRat = parameters.accountabilityRationale()
    anProp = parameters.anonymityProperty()
    anRat = parameters.anonymityRationale()
    panProp = parameters.pseudonymityProperty()
    panRat = parameters.pseudonymityRationale()
    unlProp = parameters.unlinkabilityProperty()
    unlRat = parameters.unlinkabilityRationale()
    unoProp = parameters.unobservabilityProperty()
    unoRat = parameters.unobservabilityRationale()
    ifs = parameters.interfaces()
    tags = parameters.tags()

    self.updateDatabase('call updateTemplateAsset(:id,:name,:shortCode,:desc,:sig,:type,:surfType,:rights)',{'id':assetId,'name':assetName,'shortCode':shortCode,'desc':assetDesc,'sig':assetSig,'type':assetType,'surfType':surfaceType,'rights':accessRight},'MySQL error updating template asset')
    self.addTags(assetName,'template_asset',tags)
    self.addInterfaces(assetName,'template_asset',ifs)
    self.updateTemplateAssetProperties(assetId,cProp,iProp,avProp,acProp,anProp,panProp,unlProp,unoProp,cRat,iRat,avRat,acRat,anRat,panRat,unlRat,unoRat)
    return assetId

  def getTemplateAssets(self,constraintId = -1):
    vals = self.responseList('call getTemplateAssets(:id)',{'id':constraintId},'MySQL error getting template assets')
    templateAssets = {}
    for assetId,assetName,shortCode,assetDesc,assetSig,assetType,surfaceType,accessRight in vals:
      ifs = self.getInterfaces(assetName,'template_asset')
      tags = self.getTags(assetName,'template_asset')
      taProps,taRat = self.templateAssetProperties(assetId)
      parameters = TemplateAssetParameters(assetName,shortCode,assetDesc,assetSig,assetType,surfaceType,accessRight,taProps,taRat,tags,ifs)
      templateAsset = ObjectFactory.build(assetId,parameters)
      templateAssets[assetName] = templateAsset
    return templateAssets

  def deleteTemplateAsset(self,assetId):
    self.deleteObject(assetId,'template_asset')
    

  def deleteSecurityPattern(self,patternId):
    self.deleteObject(patternId,'securitypattern')
    

  def getSecurityPatterns(self,constraintId = -1):
    patternRows = self.responseList('call getSecurityPatterns(:id)',{'id':constraintId},'MySQL error getting security patterns')
    patterns = {}
    for patternId,patternName,patternContext,patternProblem,patternSolution in patternRows:
      patternStructure = self.patternStructure(patternId)
      patternReqs = self.patternRequirements(patternId)
      parameters = SecurityPatternParameters(patternName,patternContext,patternProblem,patternSolution,patternReqs,patternStructure)
      pattern = ObjectFactory.build(patternId,parameters)
      patterns[patternName] = pattern
    return patterns

  def patternStructure(self,patternId):
    return self.responseList('call getSecurityPatternStructure(:pat)',{'pat':patternId},'MySQL error getting pattern structure')

  def patternRequirements(self,patternId):
    return self.responseList('call getSecurityPatternRequirements(:pat)',{'pat':patternId},'MySQL error getting pattern requirements')

  def addSecurityPattern(self,parameters):
    patternId = parameters.id()
    if (patternId == -1):
      patternId = self.newId()
    patternName = parameters.name()
    patternContext = parameters.context()
    patternProblem = parameters.problem()
    patternSolution = parameters.solution()
    patternStructure = parameters.associations()
    patternRequirements = parameters.requirements()
    self.updateDatabase('call addSecurityPattern(:id,:name,:cont,:prob,:sol)',{'id':patternId,'name':patternName,'cont':patternContext,'prob':patternProblem,'sol':patternSolution},'MySQL error adding security pattern')
    self.addPatternStructure(patternId,patternStructure)
    self.addPatternRequirements(patternId,patternRequirements)
    return patternId

  def updateSecurityPattern(self,parameters):
    patternId = parameters.id()
    patternName = parameters.name()
    patternContext = parameters.context()
    patternProblem = parameters.problem()
    patternSolution = parameters.solution()
    patternStructure = parameters.associations()
    patternRequirements = parameters.requirements()
    session = self.updateDatabase('call deleteSecurityPatternComponents(:pat)',{'pat':patternId},'MySQL error deleting security pattern components',None,False)
    self.updateDatabase('call updateSecurityPattern(:id,:name,:cont,:prob,:sol)',{'id':patternId,'name':patternName,'cont':patternContext,'prob':patternProblem,'sol':patternSolution},'MySQL error updating security pattern',session)
    self.addPatternStructure(patternId,patternStructure)
    self.addPatternRequirements(patternId,patternRequirements)
    return patternId

  def addPatternStructure(self,patternId,patternStructure):
    for headAsset,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailAsset in patternStructure:
      self.addPatternAssetAssociation(patternId,headAsset,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailAsset)

  def addPatternRequirements(self,patternId,patternRequirements):
    for idx,reqData in enumerate(patternRequirements):
      if (self.nameExists(reqData.name(),'template_requirement')):
        self.updateTemplateRequirement(reqData)
      else:
        self.addTemplateRequirement(reqData)
      self.addPatternRequirement(idx+1,patternId,reqData.name())

  def addPatternRequirement(self,reqLabel,patternId,reqName):
    self.updateDatabase('call addSecurityPatternRequirement(:reqLbl,:pat,:req)',{'reqLbl':reqLabel,'pat':patternId,'req':reqName},'MySQL error adding pattern requirement')

  def addPatternAssetAssociation(self,patternId,headAsset,headAdornment,headNry,headRole,tailRole,tailNry,tailAdornment,tailAsset):
    assocId = self.newId()
    self.updateDatabase('call addSecurityPatternStructure(:ass,:pat,:hAss,:hAd,:hNry,:hRole,:tRole,:tNry,:tAd,:tAss)',{'ass':assocId,'pat':patternId,'hAss':headAsset,'hAd':headAdornment,'hNry':headNry,'hRole':headRole,'tRole':tailRole,'tNry':tailNry,'tAd':tailAdornment,'tAss':tailAsset},'MySQL adding pattern asset association')

  def patternAssets(self,patternId):
    return self.responseList('call securityPatternAssets(:pat)',{'pat':patternId},'MySQL error getting pattern assets')

  def addSituatedAssets(self,patternId,assetParametersList):
    for assetParameters in assetParametersList:
      assetId = -1
      if (self.nameExists(assetParameters.name(),'asset')):
        assetId = self.getDimensionId(assetParameters.name(),'asset')
      else:
        assetId = self.addAsset(assetParameters)
      self.situatePatternAsset(patternId,assetId)

  def situatePatternAsset(self,patternId,assetId):
    self.updateDatabase('call situatePatternAsset(:ass,:pat)',{'ass':assetId,'pat':patternId},'MySQL error situating pattern asset')

  def isCountermeasureAssetGenerated(self,cmId): return self.responseList('select isCountermeasureAssetGenerated(:cm)',{'cm':cmId},'MySQL error checking assets associated with countermeasure')[0]

  def isCountermeasurePatternGenerated(self,cmId): return self.responseList('select isCountermeasurePatternGenerated(:cm)',{'cm':cmId},'MySQL error checking patterns associated with countermeasure')[0]

  
  def updateCountermeasuresEffectiveness(self,objtId,dimName,expCMs):
    for envName,cmName,assetName,cmEffectiveness in expCMs:
      self.updateCountermeasureEffectiveness(objtId,dimName,cmName,assetName,envName,cmEffectiveness) 

  def updateCountermeasureEffectiveness(self,objtId,dimName,cmName,assetName,envName,cmEffectiveness): self.updateDatabase('call updateCountermeasureEffectiveness(:obj,:dim,:cm,:ass,:env,:cmEff)',{'obj':objtId,'dim':dimName,'cm':cmName,'ass':assetName,'env':envName,'cmEff':cmEffectiveness},'MySQL error updating effectiveness of countermeasure ' + cmName)

  def countermeasurePatterns(self,cmId): return self.responseList('call countermeasurePatterns(:cm)',{'cm':cmId},'MySQL error getting patterns associated with countermeasure')

  def deleteSituatedPattern(self,cmId,patternName): self.updateDatabase('call deleteSituatedPattern(:cm,:pat)',{'cm':cmId,'pat':patternName},'MySQL deleting situated pattern')

  def candidateCountermeasurePatterns(self,cmId): return self.responseList('call candidateCountermeasurePatterns(:cm)',{'cm':cmId},'MySQL error getting candidate countermeasure patterns')

  def associateCountermeasureToPattern(self,cmId,patternName): self.updateDatabase('call associateCountermeasureToPattern(:cm,:pat)',{'cm':cmId,'pat':patternName},'MySQL error associating countermeasure to pattern')

  def nameCheck(self,objtName,dimName):
    objtCount = 0
    if (dimName == 'policy_statement'):
      goalName,envName,subjName,atName,resName = objtName.split('/')
      objtCount = self.responseList('call policyStatementExists(:env,:subj,:at,:res)',{'env':envName,'subj':subjName,'at':atName,'res':resName},'MySQL error checking existence of ' + dimName + ' ' + objtName)[0]
    else:
      objtCount = self.responseList('call nameExists(:obj,:dim)',{'obj':objtName,'dim':dimName},'MySQL error checking existence of ' + dimName + ' ' + objtName)[0]
    if (objtCount > 0): raise ARMException('Object with name ' + objtName + ' already exists.')
  

  def nameCheckEnvironment(self,objtName,envName,dimName):
    objtCount = self.responseList('call nameEnvironmentExists(:obj,:env,:dim)',{'obj':objtName,'env':envName,'dim':dimName},'MySQL error naming checking in environment')[0]
    if (objtCount > 0): raise ARMException(dimName + ' ' + objtName + ' in environment ' + envName + ' already exists.')

  def nameExists(self,objtName,dimName):
    objtCount = 0
    if (dimName == 'policy_statement'):
      goalName,envName,subjName,atName,resName = objtName.split('/')
      objtCount = self.responseList('call policyStatementExists(:env,:subj,:at,:res)',{'env':envName,'subj':subjName,'at':atName,'res':resName},'MySQL error checking existence of ' + dimName + ' ' + objtName)[0]
    else:
      objtCount = self.responseList('call nameExists(:obj,:dim)',{'obj':objtName,'dim':dimName},'MySQL error checking name exists')[0]
    if (objtCount > 0):
      return True
    else:
      return False

  def getExternalDocuments(self,constraintId = -1):
    edRows = self.responseList('call getExternalDocuments(:id)',{'id':constraintId},'MySQL error getting external documents')
    eDocs = {}

    for docId,docName,docVersion,docPubDate,docAuthors,docDesc in edRows:
      parameters = ExternalDocumentParameters(docName,docVersion,docPubDate,docAuthors,docDesc)
      eDoc = ObjectFactory.build(docId,parameters)
      eDocs[docName] = eDoc
    return eDocs

  def getDocumentReferences(self,constraintId = -1):
    drRows = self.responseList('call getDocumentReferences(:id)',{'id':constraintId},'MySQL error getting document references')
    dRefs = {}
    for refId,refName,docName,cName,excerpt in drRows:
      parameters = DocumentReferenceParameters(refName,docName,cName,excerpt)
      dRef = ObjectFactory.build(refId,parameters)
      dRefs[refName] = dRef
    return dRefs

  def getPersonaDocumentReferences(self,personaName):
    return self.responseList('call getPersonaDocumentReferences(:pers)',{'pers':personaName},'MySQL error getting document references for persona ' + personaName)

  def getPersonaConceptReferences(self,personaName):
    return self.responseList('call getPersonaConceptReferences(:pers)',{'pers':personaName},'MySQL error getting concept references for persona ' + personaName)

  def getPersonaExternalDocuments(self,personaName):
    return self.responseList('call getPersonaExternalDocuments(:pers)',{'pers':personaName},'MySQL error getting external documents for persona ' + personaName)

  def getPersonaCharacteristics(self,constraintId = -1):
    pcSumm = self.responseList('call getPersonaCharacteristics(:id)',{'id':constraintId},'MySQL error getting persona characteristics')
    pChars = {}
    for pcId,pName,bvName,qualName,pcDesc in pcSumm:
      grounds,warrant,backing,rebuttal = self.characteristicReferences(pcId,'characteristicReferences')
      parameters = PersonaCharacteristicParameters(pName,qualName,bvName,pcDesc,grounds,warrant,backing,rebuttal)
      pChar = ObjectFactory.build(pcId,parameters)
      pChars[pName + '/' + bvName + '/' + pcDesc] = pChar
    return pChars

  def characteristicReferences(self,pcId,spName):
    rows = self.responseList('call ' + spName + '(:pc)',{'pc':pcId},'MySQL error getting characteristic references')
    refDict = {}
    refDict['grounds'] = []
    refDict['warrant'] = []
    refDict['rebuttal'] = []
    for refName,typeName,refDesc,dimName in rows:
      refDict[typeName].append((refName,refDesc,dimName))
    refDict['grounds'].sort()
    refDict['warrant'].sort()
    refDict['rebuttal'].sort()
    pcBacking = self.characteristicBacking(pcId,spName)
    backingList = []
    for backing,concept in pcBacking:
      backingList.append(backing)
    backingList.sort()
    return (refDict['grounds'],refDict['warrant'],backingList,refDict['rebuttal'])

  def deleteExternalDocument(self,docId = -1):
    self.deleteObject(docId,'external_document')
    

  def deleteDocumentReference(self,refId = -1):
    self.deleteObject(refId,'document_reference')
    

  def deletePersonaCharacteristic(self,pcId = -1):
    self.deleteObject(pcId,'persona_characteristic')
    

  def addExternalDocument(self,parameters):
    docId = self.newId()
    if (sys.version_info > (3,)):
      docName = parameters.name() 
    else:
      docName = parameters.name().encode('ascii','ignore')
      docName = self.conn.connection().connection.escape_string(docName.replace("\\u2018", "'").replace("\\u2019", "'").replace("\\u2013", "-").replace("\\u2022","*"))
    docVersion = parameters.version()
    docDate = self.conn.connection().connection.escape_string(parameters.date())
    docAuthors = self.conn.connection().connection.escape_string(parameters.authors())
    docDesc = self.conn.connection().connection.escape_string(parameters.description())
    if (sys.version_info > (3,)):
      self.updateDatabase('call addExternalDocument(:id,:name,:vers,:date,:auth,:desc)',{'id':docId,'name':docName,'vers':docVersion,'date':docDate,'auth':docAuthors,'desc':docDesc},'MySQL error adding external document')
    else:
      self.updateDatabase('call addExternalDocument(:id,:name,:vers,:date,:auth,:desc)',{'id':docId,'name':docName,'vers':docVersion,'date':docDate,'auth':docAuthors,'desc':docDesc},'MySQL error adding external document')
    return docId


  def updateExternalDocument(self,parameters):
    docId = parameters.id()
    docName = self.conn.connection().connection.escape_string(parameters.name())
    docVersion = parameters.version()
    docDate = self.conn.connection().connection.escape_string(parameters.date())
    docAuthors = self.conn.connection().connection.escape_string(parameters.authors())
    docDesc = self.conn.connection().connection.escape_string(parameters.description())
    if (sys.version_info > (3,)):
      self.updateDatabase('call updateExternalDocument(:id,:name,:vers,:date,:auth,:desc)',{'id':docId,'name':docName,'vers':docVersion,'date':docDate,'auth':docAuthors,'desc':docDesc},'MySQL error updating external document')
    else:
      self.updateDatabase('call updateExternalDocument(:id,:name,:vers,:date,:auth,:desc)',{'id':docId,'name':docName,'vers':docVersion,'date':docDate,'auth':docAuthors,'desc':docDesc},'MySQL error updating external document')

  def addDocumentReference(self,parameters):
    refId = self.newId()
    refName = parameters.name()
    docName = parameters.document()
    cName = parameters.contributor()
    refExc = parameters.description()
    if (sys.version_info < (3,)):
      refName = parameters.name().encode('ascii','ignore')
      refName = self.conn.connection().connection.escape_string(refName.replace("\\u2018", "'").replace("\\u2019", "'").replace("\\u2013", "-").replace("\\u2022","*"))
      refName = self.conn.connection().connection.escape_string(refName.replace("\\u2018", "'").replace("\\u2019", "'").replace("\\u2013", "-"))
      docName = parameters.document().encode('ascii','ignore')
      docName = self.conn.connection().connection.escape_string(docName.replace("\\u2018", "'").replace("\\u2019", "'").replace("\\u2013", "-").replace("\\u2022","*").replace("\xb7","."))
      self.updateDatabase('call addDocumentReference(:rId,:rName,:dName,:cName,:rExec)',{'rId':refId,'rName':refName,'dName':docName,'cName':cName,'rExec':refExc},'MySQL error adding document reference')
    else:
      self.updateDatabase('call addDocumentReference(:rId,:rName,:dName,:cName,:rExec)',{'rId':refId,'rName':refName,'dName':docName,'cName':cName,'rExec':refExc},'MySQL error adding document reference')
    return refId

  def updateDocumentReference(self,parameters):
    refId = parameters.id()
    refName = parameters.name()
    docName = parameters.document()
    cName = parameters.contributor()
    refExc = parameters.description()
    if (sys.version_info > (3,)):
      self.updateDatabase('call updateDocumentReference(:rId,:rName,:dName,:cName,:rExec)',{'rId':refId,'rName':refName,'dName':docName,'cName':cName,'rExec':refExc},'MySQL error updating document reference')
    else:
      self.updateDatabase('call updateDocumentReference(:rId,:rName,:dName,:cName,:rExec)',{'rId':refId,'rName':refName,'dName':docName,'cName':cName,'rExec':refExc},'MySQL error updating document reference')

  def addPersonaCharacteristic(self,parameters):
    pcId = self.newId()
    personaName = parameters.persona()
    qualName = parameters.qualifier()
    bVar = parameters.behaviouralVariable()
    cDesc = parameters.characteristic()
    grounds = parameters.grounds()
    warrant = parameters.warrant() 
    rebuttal = parameters.rebuttal()
    if (sys.version_info > (3,)):
      self.updateDatabase('call addPersonaCharacteristic(:pc,:pers,:qual,:bVar,:cDesc)',{'pc':pcId,'pers':personaName,'qual':qualName,'bVar':bVar,'cDesc':cDesc},'MySQL error adding persona characteristic')
    else:
      self.updateDatabase('call addPersonaCharacteristic(:pc,:pers,:qual,:bVar,:cDesc)',{'pc':pcId,'pers':personaName,'qual':qualName,'bVar':bVar,'cDesc':cDesc},'MySQL error adding persona characteristic')
    self.addPersonaCharacteristicReferences(pcId,grounds,warrant,rebuttal)
    return pcId

  def updatePersonaCharacteristic(self,parameters):
    pcId = parameters.id()
    personaName = parameters.persona()
    qualName = parameters.qualifier()
    bVar = parameters.behaviouralVariable()
    cDesc = parameters.characteristic()
    grounds = parameters.grounds()
    warrant = parameters.warrant() 
    rebuttal = parameters.rebuttal()
    session = self.updateDatabase('call deletePersonaCharacteristicComponents(:pers)',{'pers':pcId},'MySQL error deleting persona characteristic components',None,False)
    if (sys.version_info > (3,)):
      self.updateDatabase('call updatePersonaCharacteristic(:pc,:pers,:qual,:bVar,:cDesc)',{'pc':pcId,'pers':personaName,'qual':qualName,'bVar':bVar,'cDesc':cDesc},'MySQL error updating persona characteristic',session)
    else:
      self.updateDatabase('call updatePersonaCharacteristic(:pc,:pers,:qual,:bVar,:cDesc)',{'pc':pcId,'pers':personaName,'qual':qualName,'bVar':bVar,'cDesc':cDesc},'MySQL error updating persona characteristic',session)
    self.addPersonaCharacteristicReferences(pcId,grounds,warrant,rebuttal)

  def getConceptReferences(self,constraintId = -1):
    crRows = self.responseList('call getConceptReferences(:id)',{'id':constraintId},'MySQL error getting concept references')
    cRefs = {}
    for refId,refName,dimName,objtName,cDesc in crRows:
      parameters = ConceptReferenceParameters(refName,dimName,objtName,cDesc)
      cRef = ObjectFactory.build(refId,parameters)
      cRefs[refName] = cRef
    return cRefs

  def addConceptReference(self,parameters):
    refId = self.newId()
    refName = parameters.name()
    dimName = parameters.dimension()
    objtName = parameters.objectName()
    cDesc = parameters.description()
    self.updateDatabase('call addConceptReference(:rId,:rName,:dName,:obj,:cDesc)',{'rId':refId,'rName':refName,'dName':dimName,'obj':objtName,'cDesc':cDesc},'MySQL error adding concept reference')
    return refId

  def updateConceptReference(self,parameters):
    refId = parameters.id()
    refName = parameters.name()
    dimName = parameters.dimension()
    objtName = parameters.objectName()
    cDesc = parameters.description()
    self.updateDatabase('call updateConceptReference(:rId,:rName,:dName,:obj,:cDesc)',{'rId':refId,'rName':refName,'dName':dimName,'obj':objtName,'cDesc':cDesc},'MySQL error updating concept reference')
    return refId

  def deleteConceptReference(self,refId,dimName):
    self.updateDatabase('call delete_concept_reference(:ref,:dim)',{'ref':refId,'dim':dimName},'MySQL error deleting concept reference')

  def addPersonaCharacteristicReferences(self,pcId,grounds,warrant,rebuttal):
    for g,desc,dim in grounds:
      self.addPersonaCharacteristicReference(pcId,g,'grounds',desc,dim)

    for w,desc,dim in warrant:
      self.addPersonaCharacteristicReference(pcId,w,'warrant',desc,dim)

    for r,desc,dim in rebuttal:
      self.addPersonaCharacteristicReference(pcId,r,'rebuttal',desc,dim)


  def addPersonaCharacteristicReference(self,pcId,refName,crTypeName,refDesc,dimName):
    self.updateDatabase('call addPersonaCharacteristicReference(:pc,:ref,:cr,:refD,:dim)',{'pc':pcId,'ref':refName,'cr':crTypeName,'refD':refDesc,'dim':dimName},'MySQL error adding persona characteristic reference')

  def referenceDescription(self,dimName,refName): return self.responseList('call referenceDescription(:dim,:ref)',{'dim':dimName,'ref':refName},'MySQL error getting reference description')[0]
  
  def documentReferenceNames(self,docName): return self.responseList('call documentReferenceNames(:doc)',{'doc':docName},'MySQL error getting document reference names')

  def referenceUse(self,refName,dimName): return self.responseList('call referenceUse(:ref,:dim)',{'ref':refName,'dim':dimName},'MySQL error getting reference use')

  def characteristicBacking(self,pcId,spName):
    argDict = {'pc':pcId}
    if (spName == 'characteristicReferences'):
      callTxt = 'call characteristicBacking(:pc)'
    else:
      callTxt = 'call taskCharacteristicBacking(:pc)'
    return self.responseList(callTxt,argDict,'MySQL error getting characteristic backing')

  def assumptionPersonaModel(self,personaName = '',bvName = '',pcName = ''):
    return self.responseList('call assumptionPersonaModel(:pers,:bv,:pc)',{'pers':personaName,'bv':bvName,'pc':pcName},'MySQL error getting assumption persona model')

  def getGrounds(self,constraintName):
    return self.getArgReference('Grounds',constraintName)

  def getWarrant(self,constraintName):
    return self.getArgReference('Warrant',constraintName)

  def getRebuttal(self,constraintName):
    return self.getArgReference('Rebuttal',constraintName)

  def getTaskGrounds(self,constraintName): return self.getArgReference('TaskGrounds',constraintName)

  def getTaskWarrant(self,constraintName): return self.getArgReference('TaskWarrant',constraintName)

  def getTaskRebuttal(self,constraintName): return self.getArgReference('TaskRebuttal',constraintName)


  def getArgReference(self,atName,constraintName):
    row = self.responseList('call get' + atName + '(:const)',{'const':constraintName},'MySQL error getting ' + atName + ':' + constraintName)[0]
    groundsName = row[0] 
    dimName = row[1]
    objtName = row[2]
    refDesc = row[3]
    return (dimName,objtName,refDesc) 

  def addThreatDirectory(self,tDir,isOverwrite = 1):
    self.addDirectory(tDir,'threat',isOverwrite)

  def addVulnerabilityDirectory(self,vDir,isOverwrite = 1):
    self.addDirectory(vDir,'vulnerability',isOverwrite)

  def addDirectory(self,gDir,dimName,isOverwrite):
    if (isOverwrite): self.deleteObject(-1,dimName + '_directory')
    for dLabel,dName,dDesc,dType,dRef in gDir:
      dTypeId = self.getDimensionId(dType,dimName + '_type')
      self.addDirectoryEntry(dLabel,dName,dDesc,dTypeId,dRef,dimName)
      

  def addDirectoryEntry(self,dLabel,dName,dDesc,dTypeId,dRef,dimName):
    dimName = dimName[0].upper() + dimName[1:]
    self.updateDatabase('call add' + dimName + 'DirectoryEntry(:lbl,:name,:desc,:type,:ref)',{'lbl':dLabel,'name':dName,'desc':dDesc,'type':dTypeId,'ref':dRef},'MySQL error adding directory entry')

  def lastRequirementLabel(self,assetName): return self.responseList('select lastRequirementLabel(:ass)',{'ass':assetName},'MySQL error getting last requirement label')[0]

  def getUseCases(self,constraintId = -1):
    ucRows = self.responseList('call getUseCases(:id)',{'id':constraintId},'MySQL error getting use cases')
    ucs = {} 
    for ucId,ucName,ucAuth,ucCode,ucDesc in ucRows:
      ucRoles = self.useCaseRoles(ucId)
      tags = self.getTags(ucName,'usecase')
      environmentProperties = []
      for environmentId,environmentName in self.dimensionEnvironments(ucId,'usecase'):
        preConds,postConds = self.useCaseConditions(ucId,environmentId)
        ucSteps = self.useCaseSteps(ucId,environmentId)
        properties = UseCaseEnvironmentProperties(environmentName,preConds,ucSteps,postConds)
        environmentProperties.append(properties)
        parameters = UseCaseParameters(ucName,ucAuth,ucCode,ucRoles,ucDesc,tags,environmentProperties)
        uc = ObjectFactory.build(ucId,parameters)
        ucs[ucName] = uc
    return ucs

  def useCaseRoles(self,ucId):
    return self.responseList('call useCaseRoles(:id)',{'id':ucId},'MySQL error getting actors associated with use case id ' + str(ucId))

  def useCaseConditions(self,ucId,envId):
    return self.responseList('call useCaseConditions(:uc,:env)',{'uc':ucId,'env':envId},'MySQL error getting conditions associated with use case id ' + str(ucId))[0]

  def useCaseSteps(self,ucId,envId):
    stepRows = self.responseList('call useCaseSteps(:uc,:env)',{'uc':ucId,'env':envId},'MySQL error getting steps associated with use case id ' + str(ucId))
    steps = Steps()
    for pos,stepDetails in enumerate(stepRows):
      stepTxt = stepDetails[1]
      stepSyn = stepDetails[2]
      stepActor = stepDetails[3]
      stepActorType = stepDetails[4]
      stepNo = pos + 1  
      excs = self.useCaseStepExceptions(ucId,envId,stepNo) 
      tags = self.useCaseStepTags(ucId,envId,stepNo) 
      step = Step(stepTxt,stepSyn,stepActor,stepActorType,tags)
      for exc in excs:
        step.addException(exc)
      steps.append(step)
    return steps

  def useCaseStepExceptions(self,ucId,envId,stepNo):
    return self.responseList('call useCaseStepExceptions(:uc,:env,:step)',{'uc':ucId,'env':envId,'step':stepNo},'MySQL error getting exceptions associated with use case id ' + str(ucId))


  def useCaseStepTags(self,ucId,envId,stepNo):
    return self.responseList('call useCaseStepTags(:uc,:env,:step)',{'uc':ucId,'env':envId,'step':stepNo},'MySQL error getting tags associated with use case id ' + str(ucId))

  def addUseCase(self,parameters):
    parameters.validate()
    ucName = parameters.name()
    ucAuth = parameters.author()
    ucCode = parameters.code()
    ucActors = parameters.actors()
    ucDesc = parameters.description()
    tags = parameters.tags()
    ucId = self.newId()
    self.updateDatabase('call addUseCase(:id,:name,:auth,:code,:desc)',{'id':ucId,'name':ucName,'auth':ucAuth,'code':ucCode,'desc':ucDesc},'MySQL error adding use case')
    for actor in ucActors:
      self.addUseCaseRole(ucId,actor)
    self.addTags(ucName,'usecase',tags)

    for cProperties in parameters.environmentProperties():
      parameters.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(ucId,'usecase',environmentName)
      self.addUseCaseConditions(ucId,environmentName,cProperties.preconditions(),cProperties.postconditions())
      self.addUseCaseSteps(ucId,environmentName,cProperties.steps())
    return ucId

  def addUseCaseRole(self,ucId,actor):
    self.updateDatabase('call addUseCaseRole(:id,:act)',{'id':ucId,'act':actor},'MySQL error adding use case role') 

  def addUseCaseConditions(self,ucId,envName,preCond,postCond):
    self.updateDatabase('call addUseCaseConditions(:id,:env,:pre,:post)',{'id':ucId,'env':envName,'pre':preCond,'post':postCond},'MySQL error adding use case conditions') 

  def addUseCaseSteps(self,ucId,envName,steps):
    for pos,step in enumerate(steps.theSteps):
      stepNo = pos + 1
      self.addUseCaseStep(ucId,envName,stepNo,step)

  def addUseCaseStep(self,ucId,envName,stepNo,step):
    step.validate()
    self.updateDatabase('call addUseCaseStep(:id,:env,:step,:text,:synopsis,:actor,:type)',{'id':ucId,'env':envName,'step':stepNo,'text':step.text(),'synopsis':step.synopsis(),'actor':step.actor(),'type':step.actorType()},'MySQL error adding use case step') 
    for tag in set(step.tags()): self.addUseCaseStepTag(ucId,envName,stepNo,tag)
    for idx,exc in list((step.theExceptions).items()):
      self.addUseCaseStepException(ucId,envName,stepNo,exc[0],exc[1],exc[2],exc[3],exc[4])

  def addUseCaseStepTag(self,ucId,envName,stepNo,tag): self.updateDatabase('call addUseCaseStepTag(:id,:env,:step,:tag)',{'id':ucId,'env':envName,'step':stepNo,'tag':tag},'MySQL error adding use case step tag')

  def addUseCaseStepException(self,ucId,envName,stepNo,exName,dimType,dimName,catName,exDesc):
    self.updateDatabase('call addUseCaseStepException(:uc,:env,:step,:ex,:dType,:dName,:cName,:desc)',{'uc':ucId,'env':envName,'step':stepNo,'ex':exName,'dType':dimType,'dName':dimName,'cName':catName,'desc':exDesc},'MySQL error adding use case step exception')

  def updateUseCase(self,parameters):
    parameters.validate()
    ucId = parameters.id()
    ucName = parameters.name()
    ucAuth = parameters.author()
    ucCode = parameters.code()
    ucActors = parameters.actors()
    ucDesc = parameters.description()
    tags = parameters.tags()
    session = self.updateDatabase('call deleteUseCaseComponents(:uc)',{'uc':ucId},'MySQL error deleting use case components',None,False)
    self.updateDatabase('call updateUseCase(:id,:name,:auth,:code,:desc)',{'id':ucId,'name':ucName,'auth':ucAuth,'code':ucCode,'desc':ucDesc},'MySQL error updating use case',session)
    for actor in ucActors:
      self.addUseCaseRole(ucId,actor)
    self.addTags(ucName,'usecase',tags)
    for cProperties in parameters.environmentProperties():
      cProperties.validate()
      environmentName = cProperties.name()
      self.addDimensionEnvironment(ucId,'usecase',environmentName)
      self.addUseCaseConditions(ucId,environmentName,cProperties.preconditions(),cProperties.postconditions())
      self.addUseCaseSteps(ucId,environmentName,cProperties.steps())

  def deleteUseCase(self,ucId):
    self.deleteObject(ucId,'usecase')
    

  def riskModel(self,environmentName,riskName):
    rows = self.responseList('call riskModel(:risk,:env)',{'risk':riskName,'env':environmentName},'MySQL error getting risk model')
    traces = []
    for fromObjt,fromName,toObjt,toName in rows:
      parameters = DotTraceParameters(fromObjt,fromName,toObjt,toName)
      traces.append(ObjectFactory.build(-1,parameters))
    return traces

  def isRisk(self,candidateRiskName): return self.responseList('select is_risk(:cand)',{'cand':candidateRiskName},'MySQL error checking candidate risk')[0]

  def textualArgumentationModel(self,personaName,bvType):
    return self.responseList('call assumptionPersonaModel_textual(:pers,:type)',{'pers':personaName,'type':bvType},'MySQL error getting textual argumentation model')

  def riskAnalysisToXml(self,includeHeader=True):
    return self.responseList('call riskAnalysisToXml(:head)',{'head':includeHeader},'MySQL error exporting risk analysis artifacts to XML')[0]

  def riskAnalysisToJSON(self):
    return self.responseList('call riskAnalysisToJSON()',{},'MySQL error exporting risk analysis artifacts to JSON')[0]

  def goalsToXml(self,includeHeader=True):
    return self.responseList('call goalsToXml(:head)',{'head':includeHeader},'MySQL error exporting goals to XML')[0]

  def goalsToJSON(self):
    return self.responseList('call goalsToJSON()',{},'MySQL error exporting goals to JSON')[0]

  def usabilityToXml(self,includeHeader=True):
    return self.responseList('call usabilityToXml(:head)',{'head':includeHeader},'MySQL error exporting usability data to XML')[0]

  def usabilityToJSON(self):
    return self.responseList('call usabilityToJSON()',{},'MySQL error exporting usability data to JSON')[0]

  def misusabilityToXml(self,includeHeader=True):
    return self.responseList('call misusabilityToXml(:head)',{'head':includeHeader},'MySQL error exporting misusability data to XML')[0]

  def misusabilityToJSON(self):
    return self.responseList('call misusabilityToJSON()',{},'MySQL error exporting misusability data to JSON')[0]

  def synopsesToXml(self,includeHeader=True):
    return self.responseList('call synopsesToXml(:head)',{'head':includeHeader},'MySQL error exporting synopses data to XML')[0]

  def associationsToXml(self,includeHeader=True):
    return self.responseList('call associationsToXml(:head)',{'head':includeHeader},'MySQL error exporting association data to XML')[0]

  def dataflowsToXml(self,includeHeader=True):
    return self.responseList('call dataflowsToXml(:head)',{'head':includeHeader},'MySQL error exporting dataflow data to XML')[0]

  def dataflowsToJSON(self):
    return self.responseList('call dataflowsToJSON()',{},'MySQL error exporting dataflow data to JSON')[0]

  def projectToXml(self,includeHeader=True):
    return self.responseList('call projectToXml(:head)',{'head':includeHeader},'MySQL error exporting project data to XML')[0]

  def projectToJSON(self):
    return self.responseList('call projectToJSON()',{},'MySQL error exporting project data to JSON')[0]

  def architecturalPatternToXml(self,apName):
    return self.responseList('call architecturalPatternToXml(:name)',{'name':apName},'MySQL error exporting architectural pattern to XML')[0]

  def getTaskCharacteristics(self,constraintId = -1):
    tcSumm = self.responseList('call getTaskCharacteristics(:id)',{'id':constraintId},'MySQL error getting task characteristics')
    tChars = {}
    for tcId,tName,qualName,tcDesc in tcSumm:
      grounds,warrant,backing,rebuttal = self.characteristicReferences(tcId,'taskCharacteristicReferences')
      parameters = TaskCharacteristicParameters(tName,qualName,tcDesc,grounds,warrant,backing,rebuttal)
      tChar = ObjectFactory.build(tcId,parameters)
      tChars[tName + '/' + tcDesc] = tChar
    return tChars

  def addTaskCharacteristic(self,parameters):
    tcId = self.newId()
    taskName = self.conn.connection().connection.escape_string(parameters.task())
    qualName = self.conn.connection().connection.escape_string(parameters.qualifier())
    cDesc = self.conn.connection().connection.escape_string(parameters.characteristic())
    grounds = parameters.grounds()
    warrant = parameters.warrant()
    rebuttal = parameters.rebuttal()
    self.updateDatabase('call addTaskCharacteristic(:id,:task,:qual,:desc)',{'id':tcId,'task':taskName,'qual':qualName,'desc':cDesc},'MySQL error adding task characteristic')
    self.addTaskCharacteristicReferences(tcId,grounds,warrant,rebuttal)
    return tcId

  def addTaskCharacteristicReferences(self,tcId,grounds,warrant,rebuttal):
    for g,desc,dim in grounds:
      self.addTaskCharacteristicReference(tcId,g,'grounds',desc,dim)

    for w,desc,dim in warrant:  self.addTaskCharacteristicReference(tcId,w,'warrant',desc,dim)

    for r, desc, dim in rebuttal:  self.addTaskCharacteristicReference(tcId,r,'rebuttal',desc,dim)


  def addTaskCharacteristicReference(self,tcId,refName,crTypeName,refDesc,dimName):
    self.updateDatabase('call addTaskCharacteristicReference(:id,:ref,:type,:desc,:dim)',{'id':tcId,'ref':refName,'type':crTypeName,'desc':refDesc,'dim':dimName},'MySQL error adding task characteristic reference')

  def updateTaskCharacteristic(self,parameters):
    tcId = parameters.id()
    taskName = parameters.task()
    qualName = parameters.qualifier()
    cDesc = parameters.characteristic()
    grounds = parameters.grounds()
    warrant = parameters.warrant() 
    rebuttal = parameters.rebuttal()
    session = self.updateDatabase('call deleteTaskCharacteristicComponents(:task)',{'task':tcId},'MySQL error deleting task characteristic components',None,False)
    self.updateDatabase('call updateTaskCharacteristic(:id,:task,:qual,:desc)',{'id':tcId,'task':taskName,'qual':qualName,'desc':cDesc},'MySQL error updating task characteristic',session)
    self.addTaskCharacteristicReferences(tcId,grounds,warrant,rebuttal)

  def deleteTaskCharacteristic(self,pcId = -1):
    self.deleteObject(pcId,'task_characteristic')
    

  def assumptionTaskModel(self,taskName = '',tcName = ''):
    return self.responseList('call assumptionTaskModel(:task,:tc)',{'task':taskName,'tc':tcName},'MySQL error getting assumption task model')

  def searchModel(self,inTxt,opts):
    argDict = {
    'in': inTxt,
    'ps': opts[0],
    'env': opts[1],
    'role': opts[2],
    'pc': opts[3],
    'tc': opts[4],
    'ref': opts[5],
    'p': opts[6],
    'task': opts[7],
    'uc': opts[8],
    'dp': opts[9],
    'goal': opts[10],
    'obs': opts[11],
    'req': opts[12],
    'asset': opts[13],
    'vul': opts[14],
    'attacker': opts[15],
    'thr': opts[16],
    'risk': opts[17],
    'resp': opts[18],
    'cm': opts[19],
    'dir':opts[20],
    'code': opts[21],
    'memo': opts[22],
    'id': opts[23],
    'tag': opts[24]}
    return self.responseList('call grepModel(:in,:ps,:env,:role,:pc,:tc,:ref,:p,:task,:uc,:dp,:goal,:obs,:req,:asset,:vul,:attacker,:thr,:risk,:resp,:cm,:dir,:code,:memo,:id,:tag)',argDict,'MySQL error searching model')

  def getExternalDocumentReferencesByExternalDocument(self,edName): return self.responseList('call getExternalDocumentReferences(:name)',{'name':edName},'MySQL error external document references')

  def dimensionNameByShortCode(self,scName): return self.responseList('call dimensionNameByShortCode(:shortCode)',{'shortCode':scName},'MySQL error calling dimension name by short code')

  def misuseCaseRiskComponents(self,mcName):
    return self.responseList('call misuseCaseRiskComponents(:misuse)',{'misuse':mcName},'MySQL error getting risk components associated with misuse case ' + mcName)[0]

  def personaToXml(self,pName):
    return self.responseList('call personaToXml(:persona)',{'persona':pName},'MySQL error exporting persona to XML')[0]

  def defaultEnvironment(self): return self.responseList('select defaultEnvironment()',{},'MySQL error obtaining default environment')[0]

  def environmentTensions(self,envName):
    rows = self.responseList('call environmentTensions(:env)',{'env':envName},'MySQL error getting environment tensions')
    vts = {}
    rowIdx = 0
    for anTR, panTR, unlTR, unoTR in rows:
      anValue,anRationale = anTR.split('#')
      vts[(rowIdx,4)] = (int(anValue),anRationale)
      panValue,panRationale = panTR.split('#')
      vts[(rowIdx,5)] = (int(panValue),panRationale)
      unlValue,unlRationale = unlTR.split('#')
      vts[(rowIdx,6)] = (int(unlValue),unlRationale)
      unoValue,unoRationale = unoTR.split('#')
      vts[(rowIdx,7)] = (int(unoValue),unoRationale)
      rowIdx += 1
    return vts


  def getReferenceSynopsis(self,refName):
    row = self.responseList('call getReferenceSynopsis(:ref)',{'ref':refName},'MySQL error getting response synopsis')[0]
    rsId = row[0]
    synName = row[1]
    dimName = row[2]
    aType = row[3]
    aName = row[4]
    synDim = row[5]
    gsName = row[6]
    goals = self.userGoalSystemGoals(rsId)
    rs = ReferenceSynopsis(rsId,refName,synName,dimName,aType,aName,synDim,gsName,goals)
    return rs 

  def getReferenceContribution(self,charName,refName):
    row = self.responseList('call getReferenceContribution(:ref,:char)',{'ref':refName,'char':charName},'MySQL error getting reference contribution')[0]
    rsName = row[0]
    csName = row[1]
    me = row[2]
    cont = row[3]
    rc = ReferenceContribution(rsName,csName,me,cont)
    return rc

  def addReferenceContribution(self,rc):
    rsName = rc.source()
    csName = rc.destination()
    meName = rc.meansEnd()
    contName = rc.contribution()
    self.updateDatabase('call addReferenceContribution(:rs,:cs,:me,:cont)',{'rs':rsName,'cs':csName,'me':meName,'cont':contName},'MySQL error adding reference contribution')

  def updateReferenceContribution(self,rc):
    rsName = rc.source()
    csName = rc.destination()
    meName = rc.meansEnd()
    contName = rc.contribution()
    self.updateDatabase('call updateReferenceContribution(:rs,:cs,:me,:cont)',{'rs':rsName,'cs':csName,'me':meName,'cont':contName},'MySQL error updating reference contribution')

  def addReferenceSynopsis(self,rs):
    rsId = self.newId()
    refName = rs.reference()
    rsName = rs.synopsis()
    rsDim = rs.dimension()
    atName = rs.actorType()
    actorName = rs.actor()
    gSat = rs.satisfaction()
    self.updateDatabase('call addReferenceSynopsis(:rsId,:ref,:rs,:dim,:atName,:actName,:gSat)',{'rsId':rsId,'ref':refName,'rs':rsName,'dim':rsDim,'atName':atName,'actName':actorName,'gSat':gSat},'MySQL error adding reference synopsis')
    for sysGoal in rs.goals():
      self.addUserSystemGoalLink(rsName,sysGoal)
    return rsId

  def updateReferenceSynopsis(self,rs):
    rsId = rs.id()
    refName = rs.reference()
    rsName = rs.synopsis()
    rsDim = rs.dimension()
    atName = rs.actorType()
    actorName = rs.actor()
    gSat = rs.satisfaction()
    session = self.updateDatabase('call deleteUserGoalComponents(:id)',{'id':rsId},'MySQL error deleting user goal components',None,False)
    self.updateDatabase('call updateReferenceSynopsis(:rsId,:ref,:rs,:dim,:atName,:actName,:gSat)',{'rsId':rsId,'ref':refName,'rs':rsName,'dim':rsDim,'atName':atName,'actName':actorName,'gSat':gSat},'MySQL error updating reference synopsis',session)
    for sysGoal in rs.goals():
      self.addUserSystemGoalLink(rsName,sysGoal)

  def addCharacteristicSynopsis(self,cs):
    cName = cs.reference()
    csName = cs.synopsis()
    csDim = cs.dimension()
    atName = cs.actorType()
    actorName = cs.actor()
    gSat = cs.satisfaction()
    self.updateDatabase('call addCharacteristicSynopsis(:cName,:csName,:csDim,:atName,:actName,:gSat)',{'cName':cName,'csName':csName,'csDim':csDim,'atName':atName,'actName':actorName,'gSat':gSat},'MySQL error adding characteristic synopsis')
    for sysGoal in cs.goals():
      self.addUserSystemGoalLink(csName,sysGoal)

  def updateCharacteristicSynopsis(self,cs):
    cName = cs.reference()
    csName = cs.synopsis()
    csDim = cs.dimension()
    atName = cs.actorType()
    actorName = cs.actor()
    gSat = cs.satisfaction()
    session = self.updateDatabase('call deleteUserGoalComponents(:id)',{'id':cs.id()},'MySQL error deleting user goal components',None,False)
    self.updateDatabase('call updateCharacteristicSynopsis(:cName,:csName,:csDim,:atName,:actName,:gSat)',{'cName':cName,'csName':csName,'csDim':csDim,'atName':atName,'actName':actorName,'gSat':gSat},'MySQL error updating characteristic synopsis',session)
    for sysGoal in cs.goals():
      self.addUserSystemGoalLink(csName,sysGoal)

  def referenceCharacteristic(self,refName): return self.responseList('call referenceCharacteristic(:ref)',{'ref':refName},'MySQL error getting characteristics associated with reference ' + refName)

  def getCharacteristicSynopsis(self,cName):
    row = self.responseList('call getCharacteristicSynopsis(:characteristic)',{'characteristic':cName},'MySQL error getting characteristic synopsis')[0]
    synName = row[0]
    dimName = row[1]
    aType = row[2]
    aName = row[3]
    if synName == '':
      synId = -1
    else:
      synId = 0
    rs = ReferenceSynopsis(synId,cName,synName,dimName,aType,aName)
    return rs 

  def hasCharacteristicSynopsis(self,charName): return self.responseList('select hasCharacteristicSynopsis(:characteristic)',{'characteristic':charName},'MySQL error finding characteristic synopsis')[0]

  def hasReferenceSynopsis(self,refName): return self.responseList('select hasReferenceSynopsis(:ref)',{'ref':refName},'MySQL error finding reference synopsis')[0]

  def addUseCaseSynopsis(self,cs): self.updateDatabase('call addUseCaseSynopsis(:cName,:csName,:csDim,:atName,:actName)',{'cName':cs.reference(),'csName':cs.synopsis(),'csDim':cs.dimension(),'atName':cs.actorType(),'actName':cs.actor()},'MySQL error adding use case synopsis')

  def getUseCaseContributions(self,ucName):
    rows = self.responseList('call getUseCaseContributions(:useCase)',{'useCase':ucName},'MySQL error getting use case contributions')
    ucs = {}
    for rsName,me,cont,rType in rows:
      rc = ReferenceContribution(ucName,rsName,me,cont)
      ucs[rsName] = (rc,rType) 
    return ucs

  def addUseCaseContribution(self,rc):
    ucName = rc.source()
    csName = rc.destination()
    meName = rc.meansEnd()
    contName = rc.contribution()
    self.updateDatabase('call addUseCaseContribution(:useCase,:csName,:meName,:cont)',{'useCase':ucName,'csName':csName,'meName':meName,'cont':contName},'MySQL error adding use case contribution')

  def updateUseCaseContribution(self,rc):
    ucName = rc.source()
    csName = rc.destination()
    meName = rc.meansEnd()
    contName = rc.contribution()
    self.updateDatabase('call updateUseCaseContribution(:useCase,:csName,:meName,:cont)',{'useCase':ucName,'csName':csName,'meName':meName,'cont':contName},'MySQL error updating use case contribution')

  def addTaskContributions(self,tcs):
    for tc in tcs:
      self.addTaskContribution(tc)

  def addTaskContribution(self,tc):
    src = tc.source()
    dest = tc.destination()
    env = tc.environment()
    cont = tc.contribution()
    self.updateDatabase('call addTaskContribution(:src,:dest,:env,:cont)',{'src':src,'dest':dest,'env':env,'cont':cont},'MySQL error adding task contribution')

  def updateTaskContribution(self,tc):
    src = tc.source()
    dest = tc.destination()
    env = tc.environment()
    cont = tc.contribution()
    self.updateDatabase('call updateTaskContribution(:src,:dest,:env,:cont)',{'src':src,'dest':dest,'env':env,'cont':cont},'MySQL error updating task contribution')

  def pcToGrl(self,pNames,tNames,envName):
    return self.responseList('call pcToGrl(":pNames", ":tNames", :env)',{'pNames':pNames,'tNames':tNames,'env':envName},'MySQL error exporting to GRL')[0]

  def dependentLabels(self,goalName,envName): return self.responseList('call dependentLabels(:goal,:env)',{'goal':goalName,'env':envName},'MySQL error getting dependent labels')

  def relabelGoals(self,envName):
    self.updateDatabase('call relabelGoals(:env)',{'env':envName},'MySQL error relabelling goals')

  def relabelObstacles(self,envName):
    self.updateDatabase('call relabelObstacles(:env)',{'env':envName},'MySQL error relabelling obstacles')

  def obstacleLabel(self,goalId,environmentId):
    return self.responseList('select obstacle_label(:goal,:env)',{'goal':goalId,'env':environmentId},'MySQL error getting obstacle label')[0]

  def redmineGoals(self,envName):
    goalRows = self.responseList('call redmineGoals(:env)',{'env':envName},'MySQL error getting redmine goals')
    goals = {}
    for goalId,envId,goalLabel,goalName,goalOrig,goalDef,goalCat,goalPri,goalFC,goalIssue in goalRows:
      goalRefinements,subGoalRefinements = self.goalRefinements(goalId,envId)
      concerns = self.goalConcerns(goalId,envId)
      concernAssociations = self.goalConcernAssociations(goalId,envId)
      ep = GoalEnvironmentProperties(envName,goalLabel,goalDef,'Maintain',goalPri,goalFC,goalIssue,goalRefinements,subGoalRefinements,concerns,concernAssociations)
      parameters = GoalParameters(goalName,goalOrig,[],[ep])
      g = ObjectFactory.build(goalId,parameters)
      lbl = g.label(envName)
      goals[lbl] = g
    lbls = list(goals.keys())
    if (len(lbls) > 0):
      shortCode = lbls[0].split('-')[0]
      lblNos = []
      for lbl in lbls:
        lblNos.append(lbl.split('-')[1])
      lblNos.sort(key=lambda x: [int(y) for y in x.split('.')])
      lbls = []
      for ln in lblNos:
        lbls.append(shortCode + '-' + ln) 
    return lbls,goals

  def redmineUseCases(self):
    return self.responseList('call usecasesToRedmine()',{},'MySQL exporting usecases to Redmine')

  def redmineScenarios(self):
    return self.responseList('call redmineScenarios()',{},'MySQL exporting scenarios to Redmine')


  def redmineArchitecture(self):
    return self.responseList('call redmineArchitecture()',{},'MySQL exporting architecture to Redmine')

  def redmineAttackPatterns(self):
    return self.responseList('call redmineAttackPatterns()',{},'MySQL exporting attack patterns to Redmine')

  def tvTypesToXml(self,includeHeader=True):
    return self.responseList('call tvTypesToXml(:head)',{'head':includeHeader},'MySQL error exporting threat and vulnerability types to XML')[0]

  def tvTypesToJSON(self):
    return self.responseList('call tvTypesToJSON()',{},'MySQL error exporting threat and vulnerability types to JSON')[0]

  def domainValuesToXml(self,includeHeader=True):
    return self.responseList('call domainValuesToXml(:head)',{'head':includeHeader},'MySQL error exporting domain values to XML')[0]

  def domainValuesToJSON(self,includeHeader=True):
    return self.responseList('call domainValuesToJSON()',{},'MySQL error exporting domain values to JSON')[0]

  def locationsToXml(self):
    return self.responseList('call locationsToXml()',{},'MySQL error exporting locations to XML')[0]

  def locationsToJSON(self):
    return self.responseList('call locationsToJSON()',{},'MySQL error exporting locations to JSON')[0]

  def associationsToJSON(self):
    return self.responseList('call associationsToJSON()',{},'MySQL error exporting associations to JSON')[0]

  def clearDatabase(self,session_id = None,dbUser=None,dbPasswd=None,dbName=None):
    b = Borg()
    if b.runmode == 'desktop':
      db_proxy = b.dbProxy
      dbHost = b.dbHost
      dbPort = b.dbPort
      dbUser = b.dbUser
      dbPasswd = b.dbPasswd
      dbName = b.dbName
    elif b.runmode == 'web':
      ses_settings = b.get_settings(session_id)
      db_proxy = ses_settings['dbProxy']
      dbHost = ses_settings['dbHost']
      dbPort = ses_settings['dbPort']

      if (dbUser == None or dbPasswd == None or dbName == None):
        dbUser = ses_settings['dbUser']
        dbPasswd = ses_settings['dbPasswd']
        dbName = ses_settings['dbName']
    else:
      raise RuntimeError('Run mode not recognized')
    db_proxy.close()
    createDatabaseSchema(b.cairisRoot,dbHost,dbPort,dbUser,dbPasswd,dbName)
    if (session_id != None):
      db_proxy.reconnect(False, session_id)

  def conceptMapModel(self,envName,reqName = 'all'):
    callTxt = 'call conceptMapModel_all(:env,:req)'
    argDict = {'env':envName,'req':reqName}
    rows = self.responseList(callTxt,argDict,'MySQL error getting concept map model')
    associations = {}

    for fromName,toName,lbl,fromEnv,toEnv in rows:
      cmLabel = fromName + '#' + toName + '#' + lbl
      assoc = ConceptMapAssociationParameters(fromName,toName,lbl,fromEnv,toEnv)
      associations[cmLabel] = assoc
    return associations

  def traceabilityScore(self,reqName):
    return self.responseList('select traceabilityScore(:req)',{'req':reqName},'MySQL error getting traceability score')[0]


  def getRedmineRequirements(self):
    reqRows = self.responseList('select name,originator,priority,comments,description,environment_code,environment from redmine_requirement order by 1',{},'MySQL error getting redmine requirements');
    reqs = {}
    priorityLookup = {1:'High',2:'Medium',3:'Low'}
    for reqName,reqOriginator,reqPriority,reqComments,reqDesc,reqEnvCode,reqEnv in reqRows:
      reqScs = self.getRequirementScenarios(reqName)
      reqUcs = self.getRequirementUseCases(reqName)
      reqBis = self.getRequirementBacklog(reqName)
      if reqEnv not in reqs:
        reqs[reqEnv] = []
      reqs[reqEnv].append((reqName,reqOriginator,priorityLookup[reqPriority],reqComments,reqDesc,reqEnvCode,reqScs,reqUcs,reqBis))
    return reqs

  def getRequirementScenarios(self,reqName):
    scs = self.responseList('call requirementScenarios(:req)',{'req':reqName},'MySQL error getting redmine scenarios');
    if len(scs) == 0:
      scs.append('None')
    return scs

  def getRequirementUseCases(self,reqName):
    ucs = self.responseList('call requirementUseCases(:req)',{'req':reqName},'MySQL error getting redmine use cases');
    if len(ucs) == 0:
      ucs.append('None')
    return ucs

  def getRequirementBacklog(self,reqName):
    bis = self.responseList('call requirementBacklog(:req)',{'req':reqName},'MySQL error getting backlog items');
    if len(bis) == 0:
      bis.append('None')
    return bis

  def environmentRequirements(self,envName): 
    return self.responseList('call requirementNames(:env)',{'env':envName},'MySQL error getting requirements associated with environment ' + envName)

  def deleteTags(self,tagObjt,tagDim): 
    self.updateDatabase('call deleteTags(:obj,:dim)',{'obj':tagObjt,'dim':tagDim},'MySQL error deleting tags')

  def deleteDataFlowTags(self,dfName,fromType,fromName,toType,toName,envName): 
    self.updateDatabase('call deleteDataFlowTags(:dfName, :fromType, :fromName, :toType, :toName, :envName)',{'dfName' : dfName, 'fromType' : fromType, 'fromName' : fromName, 'toType' : toType, 'toName' : toName, 'envName' : envName},'MySQL error deleting data flow tags')

  def addTags(self,dimObjt,dimName,tags):
    self.deleteTags(dimObjt,dimName)
    curs = self.conn.connection().connection.cursor()
    for tag in set(tags):
      try:
        curs.execute('call addTag(%s,%s,%s)',[dimObjt,tag,dimName])
      except OperationalError as e:
        raise DatabaseProxyException('MySQL error adding tag (message: ' + format(e))
      except DatabaseError as e:
        raise DatabaseProxyException('MySQL error adding ' + dimName + ' ' + dimObjt + ' tag ' + tag + ': ' + format(e))
    curs.close()

  def addDataFlowTags(self,dfName,fromType,fromName,toType,toName,envName,tags):
    self.deleteDataFlowTags(dfName,fromType,fromName,toType,toName,envName)
    curs = self.conn.connection().connection.cursor()
    for tag in set(tags):
      try:
        curs.execute('call addDataFlowTag(%s,%s,%s,%s,%s,%s,%s)',[dfName,fromType,fromName,toType,toName,envName,tag])
      except OperationalError as e:
        raise DatabaseProxyException('MySQL error adding dataflow tag (message: ' + format(e))
      except DatabaseError as e:
        raise DatabaseProxyException('MySQL error adding dataflow tag ' + tag + ': ' + format(e))
    curs.close()

  def getTags(self,dimObjt,dimName):
    return self.responseList('call getTags(:obj,:name)',{'obj':dimObjt,'name':dimName},'MySQL error getting tags')

  def getDataFlowTags(self,dfName,fromType,fromName,toType,toName,envName):
    return self.responseList('call getDataFlowTags(:dfName,:fromType,:fromName,:toType,:toName,:envName)',{'dfName':dfName,'fromType':fromType,'fromName':fromName,'toType':toType,'toName':toName,'envName':envName},'MySQL error getting data flow tags')

  def deleteTag(self,tagId): self.deleteObject(tagId,'tag')
    

  def componentView(self,cvName):
    interfaces = self.responseList('call componentViewInterfaces(:cv)',{'cv':cvName},'MySQL error getting component view interfaces')
    connectors = self.componentViewConnectors(cvName)
    return (interfaces,connectors)


  def componentViewConnectors(self,cvName):
    return self.responseList('call componentViewConnectors(:cv)',{'cv':cvName},'MySQL error getting component view connectors')

  def addComponentToView(self,cId,cvId): self.updateDatabase('call addComponentToView(:cId,:cvId)',{'cId':cId,'cvId':cvId},'MySQL error adding component to view')

  def addComponent(self,parameters,cvId = -1):
    componentId = self.newId()
    componentName = parameters.name()
    componentDesc = parameters.description()
    structure = parameters.structure()
    requirements = parameters.requirements()
    goals = parameters.goals()
    assocs = parameters.associations()

    session = self.updateDatabase('call addComponent(:id,:name,:desc)',{'id':componentId,'name':componentName,'desc':componentDesc},'MySQL error adding component',None,False)
    if cvId != -1:
      self.updateDatabase('call addComponentToView(:compId,:cvId)',{'compId':componentId,'cvId':cvId},'MySQL error adding component to view',session,False)
    self.commitDatabase(session)
    for ifName,ifType,arName,pName in parameters.interfaces():
      self.addComponentInterface(componentId,ifName,ifType,arName,pName)
    self.addComponentStructure(componentId,structure)
    self.addComponentRequirements(componentId,requirements)
    self.addComponentGoals(componentId,goals)
    self.addComponentAssociations(componentId,assocs)

  def updateComponent(self,parameters,cvId = -1):
    componentId = parameters.id()
    componentName = parameters.name()
    componentDesc = parameters.description()
    structure = parameters.structure()
    requirements = parameters.requirements()
    goals = parameters.goals()
    assocs = parameters.associations()

    session = self.updateDatabase('call deleteComponentComponents(:comp)',{'comp':componentId},'MySQL error deleting component components',None,False)
    if (componentId != -1):
      self.updateDatabase('call updateComponent(:id,:name,:desc)',{'id':componentId,'name':componentName,'desc':componentDesc},'MySQL error updating component',session)
    else:
      componentId = self.newId()
      self.updateDatabase('call addComponent(:id,:name,:desc)',{'id':componentId,'name':componentName,'desc':componentDesc},'MySQL error adding component',session,False)

    if cvId != -1:
      self.updateDatabase('call addComponentToView(:compId,:cvId)',{'compId':componentId,'cvId':cvId},'MySQL error adding component to view',session,False)
    self.commitDatabase(session)
    for ifName,ifType,arName,pName in parameters.interfaces():
      self.addComponentInterface(componentId,ifName,ifType,arName,pName)
    self.addComponentStructure(componentId,structure)
    self.addComponentRequirements(componentId,requirements)
    self.addComponentGoals(componentId,goals)
    self.addComponentAssociations(componentId,assocs)

  def addComponentInterface(self,componentId,ifName,ifType,arName,pName):
    self.updateDatabase('call addComponentInterface(:compId,:ifName,:ifType,:arName,:pName)',{'compId':componentId,'ifName':ifName,'ifType':ifType,'arName':arName,'pName':pName},'MySQL error adding component interface')

  def addConnector(self,parameters):
    connId = self.newId()
    cName = parameters.name()
    cvName = parameters.view()
    fromName = parameters.fromName()
    fromRole = parameters.fromRole()
    fromIf = parameters.fromInterface()
    toName = parameters.toName()
    toIf = parameters.toInterface()
    toRole = parameters.toRole()
    conAsset = parameters.asset()
    pName = parameters.protocol()
    arName = parameters.accessRight()
    self.updateDatabase('call addConnector(:connId,:cvName,:cName,:fName,:fRole,:fIf,:tName,:tIf,:tRole,:conAsset,:pName,:arName)',{'connId':connId,'cvName':cvName,'cName':cName,'fName':fromName,'fRole':fromRole,'fIf':fromIf,'tName':toName,'tIf':toIf,'tRole':toRole,'conAsset':conAsset,'pName':pName,'arName':arName},'MySQL error adding connector')

  def getInterfaces(self,dimObjt,dimName):
    rows = self.responseList('call getInterfaces(:obj,:name)',{'obj':dimObjt,'name':dimName},'MySQL error getting interfaces')
    ifs = []
    for ifName,ifTypeId,arName,prName in rows:
      ifType = 'provided'
      if (ifTypeId == 1): ifType = 'required'
      ifs.append((ifName,ifType,arName,prName))
    return ifs

  def addInterfaces(self,dimObjt,dimName,ifs):
    try:
      self.deleteInterfaces(dimObjt,dimName)
      for ifName,ifType,arName,pName in ifs:
        self.addInterface(dimObjt,ifName,ifType,arName,pName,dimName)
    except OperationalError as e:
      exceptionText = 'MySQL error adding interfaces to ' + dimName + ' ' + dimObjt +  ' (message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      id,msg = e
      exceptionText = 'MySQL error adding interfaces to ' + dimName + ' ' + dimObjt +  ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteInterfaces(self,ifName,ifDim):
    self.updateDatabase('call deleteInterfaces(:name,:dim)',{'name':ifName,'dim':ifDim},'MySQL error deleting interfaces')

  def addInterface(self,ifObjt,ifName,ifType,arName,pName,ifDim):
    self.updateDatabase('call addInterface(:ifObj,:ifName,:ifType,:arName,:pName,:ifDim)',{'ifObj':ifObjt,'ifName':ifName,'ifType':ifType,'arName':arName,'pName':pName,'ifDim':ifDim},'MySQL error adding interface')

  def addComponentStructure(self,componentId,componentStructure):
    for headAsset,headAdornment,headNav,headNry,headRole,tailRole,tailNry,tailNav,tailAdornment,tailAsset in componentStructure:
      self.addComponentAssetAssociation(componentId,headAsset,headAdornment,headNav,headNry,headRole,tailRole,tailNry,tailNav,tailAdornment,tailAsset)

  def addComponentAssetAssociation(self,componentId,headAsset,headAdornment,headNav,headNry,headRole,tailRole,tailNry,tailNav,tailAdornment,tailAsset):
    assocId = self.newId()
    self.updateDatabase('call addComponentStructure(:aId,:cId,:hAss,:hAd,:hNav,:hNry,:hRole,:tRole,:tNry,:tNav,:tAd,:tAss)',{'aId':assocId,'cId':componentId,'hAss':headAsset,'hAd':headAdornment,'hNav':headNav,'hNry':headNry,'hRole':headRole,'tRole':tailRole,'tNry':tailNry,'tNav':tailNav,'tAd':tailAdornment,'tAss':tailAsset},'MySQL error adding component asset association')

  def componentStructure(self,componentId):
    return self.responseList('call getComponentStructure(:comp)',{'comp':componentId},'MySQL error getting structure for component')

  def addComponentRequirements(self,componentId,componentRequirements):
    for idx,reqName in enumerate(componentRequirements):
      self.addComponentRequirement(idx+1,componentId,reqName)

  def addComponentRequirement(self,reqLabel,componentId,reqName): self.updateDatabase('call addComponentRequirement(:reqLbl,:comp,:req)',{'reqLbl':reqLabel,'comp':componentId,'req':reqName},'MySQL error adding component requirement')

  def getComponentViews(self,constraintId = -1):
    cvRows = self.responseList('call getComponentView(:cons)',{'cons':constraintId},'MySQL error getting component view')
    cvs = {}
    for cvId,cvName,cvSyn in cvRows:
      viewComponents = self.componentViewComponents(cvId)
      components = []
      for componentId,componentName,componentDesc in viewComponents:
        componentInterfaces = self.componentInterfaces(componentId)
        componentStructure = self.componentStructure(componentId)
        componentReqs = self.componentRequirements(componentId)
        componentGoals = self.componentGoals(componentId)
        goalAssocs = self.componentGoalAssociations(componentId)
        comParameters = ComponentParameters(componentName,componentDesc,componentInterfaces,componentStructure,componentReqs,componentGoals,goalAssocs)
        comParameters.setId(componentId)
        components.append(comParameters)
      connectors = self.componentViewConnectors(cvName)
      asm = self.attackSurfaceMetric(cvName)
      parameters = ComponentViewParameters(cvName,cvSyn,[],[],[],[],[],components,connectors,asm)
      cv = ObjectFactory.build(cvId,parameters)
      cvs[cvName] = cv
    return cvs

  def componentRequirements(self,componentId):
    return self.responseList('call getComponentRequirements(:comp)',{'comp':componentId},'MySQL error getting component requirements')

  def componentInterfaces(self,componentId):
    rows = self.responseList('call componentInterfaces(:comp)',{'comp':componentId},'MySQL error getting component interfaces')
    ifs = []
    for compName,ifName,ifTypeId,arName,prName in rows:
      ifType = 'provided'
      if (ifTypeId == 1):
        ifType = 'required'
      ifs.append((ifName,ifType,arName,prName))
    return ifs

  def addComponentView(self,parameters):
    parameters.validate();
    cvId = self.newId()
    cvName = parameters.name()
    cvSyn = parameters.synopsis()
    cvValueTypes = parameters.metricTypes()
    cvRoles = parameters.roles()
    cvAssets = parameters.assets()
    cvReqs = parameters.requirements()
    cvGoals = parameters.goals()
    cvComs = parameters.components()
    cvCons = parameters.connectors()

    self.updateDatabase('call addComponentView(:id,:name,:syn)',{'id':cvId,'name':cvName,'syn':cvSyn},'MySQL error adding component view')
    for vtParameters in cvValueTypes:
      vtId = self.existingObject(vtParameters.name(),vtParameters.type())
      if vtId == -1:
        self.addValueType(vtParameters)
    for rParameters in cvRoles:
      rId = self.existingObject(rParameters.name(),'role')
      if rId == -1:
        self.addRole(rParameters)
    for taParameters in cvAssets:
      taId = self.existingObject(taParameters.name(),'template_asset')
      if taId == -1:
        self.addTemplateAsset(taParameters)
    for trParameters in cvReqs:
      trId = self.existingObject(trParameters.name(),'template_requirement')
      if trId == -1:
        self.addTemplateRequirement(trParameters)
    for tgParameters in cvGoals:
      tgId = self.existingObject(tgParameters.name(),'template_goal')
      if tgId == -1:
        self.addTemplateGoal(tgParameters)
    for comParameters in cvComs:
      cId = self.existingObject(comParameters.name(),'component')
      if cId == -1:
        self.addComponent(comParameters,cvId)
      else:
        comParameters.setId(cId)
        self.addComponentToView(cId,cvId)
        self.mergeComponent(comParameters)

    for conParameters in cvCons:
      self.addConnector(conParameters)
    return cvId

  def updateComponentView(self,parameters):
    parameters.validate();
    cvId = parameters.id()
    cvName = parameters.name()
    cvSyn = parameters.synopsis()
    cvAssets = parameters.assets()
    cvReqs = parameters.requirements()
    cvComs = parameters.components()
    cvCons = parameters.connectors()

    session = self.updateDatabase('call deleteComponentViewComponents(:id)',{'id':cvId},'MySQL error deleting component view components',None,False)
    self.updateDatabase('call updateComponentView(:id,:name,:syn)',{'id':cvId,'name':cvName,'syn':cvSyn},'MySQL error updating component view',session)
    for taParameters in cvAssets:
      self.updateTemplateAsset(taParameters)
    for trParameters in cvReqs: self.updateTemplateRequirement(trParameters)
    for comParameters in cvComs:
      self.addComponent(comParameters,cvId)
    for conParameters in cvCons:
      self.addConnector(conParameters)
    return cvId

  def deleteComponentView(self,cvId):
    self.deleteObject(cvId,'component_view')
    
  def componentViewComponents(self,cvId):
    return self.responseList('call getComponents(:id)',{'id':cvId},'MySQL error getting components')

  def componentViewWeaknesses(self,cvName,envName):
    rows = self.responseList('call componentViewWeaknesses(:cv,:env)',{'cv':cvName,'env':envName},'MySQL error getting component view weaknesses')
    thrDict = {}
    vulDict = {}
    for cName,taName,aName,targetName,targetType in rows:
      t = None
      if targetType == 'threat':
        if targetName not in thrDict: t = WeaknessTarget(targetName)
        else: t = thrDict[targetName]
        t.addTemplateAsset(taName)
        t.addAsset(aName)
        t.addComponent(cName)
        thrDict[targetName] = t
      else:
        if targetName not in vulDict:
          t = WeaknessTarget(targetName)
        else:
          t = vulDict[targetName]
        t.addTemplateAsset(taName)
        t.addAsset(aName)
        t.addComponent(cName)
        vulDict[targetName] = t
    return (thrDict,vulDict)

  def componentAssets(self,cvName,reqName = ''):
    return self.responseList('call componentAssets(:cv,:req)',{'cv':cvName,'req':reqName},'MySQL error getting component assets')

  def componentGoalAssets(self,cvName,goalName = ''): return self.responseList('call componentGoalAssets(:cv,:goal)',{'cv':cvName,'goal':goalName},'MySQL error getting component goal assets')

  def existingObject(self,objtName,dimName):
    argDict = {'objt':objtName,'dim':dimName}
    callTxt = 'call existing_object(:objt,:dim)'
    if (dimName == 'persona_characteristic' or dimName == 'task_characteristic'):
      callTxt = 'call existing_characteristic(:objt,:dim)'
    return self.responseList(callTxt,argDict,'MySQL error checking existence of object')[0]


  def situateComponentView(self,cvName,envName,acDict,assetParametersList,targets,obstructParameters):
    for assetParameters in assetParametersList:
      assetName = assetParameters.name()
      assetId = self.existingObject(assetName,'asset')
      if assetId == -1:
        assetId = self.addAsset(assetParameters)
      for cName in acDict[assetName]:
        self.situateComponentAsset(cName,assetId)
    self.situateComponentViewRequirements(cvName)
    self.situateComponentViewGoals(cvName,envName)
    self.situateComponentViewGoalAssociations(cvName,envName)
    for target in targets: self.addComponentViewTargets(target,envName)
    for op in obstructParameters: self.addGoalAssociation(op)
 
  def situateComponentAsset(self,componentName,assetId):
    self.updateDatabase('call situateComponentAsset(:ass,:comp)',{'ass':assetId,'comp':componentName},'MySQL error situating component asset')

  def addComponentViewTargets(self,target,envName):
    session = self.conn()
    for componentName in target.components():
      self.updateDatabase('call addComponentTarget(:comp,:asset,:name,:effectiveness,:rationale,:env)',{'comp':componentName,'asset':target.asset(),'name':target.name(),'effectiveness':target.effectiveness(),'rationale':target.rationale(),'env':envName},'MySQL error adding component target',session,False)
    self.commitDatabase(session)

  def assetComponents(self,assetName,envName):
    return self.responseList('call assetComponents(:ass,:env)',{'ass':assetName,'env':envName},'MySQL error getting asset components')

  def addTemplateRequirement(self,parameters):
    reqId = self.newId()
    reqName = parameters.name()
    reqAsset = parameters.asset()
    reqType = parameters.type()
    reqDesc = parameters.description()
    reqRat = parameters.rationale()
    reqFC = parameters.fitCriterion()
    self.updateDatabase('call addTemplateRequirement(:id,:name,:asset,:type,:desc,:rat,:fc)',{'id':reqId,'name':reqName,'asset':reqAsset,'type':reqType,'desc':reqDesc,'rat':reqRat,'fc':reqFC},'MySQL error adding template requirement')
    return reqId

  def updateTemplateRequirement(self,parameters):
    reqId = parameters.id()
    reqName = parameters.name()
    reqAsset = parameters.asset()
    reqType = parameters.type()
    reqDesc = parameters.description()
    reqRat = parameters.rationale()
    reqFC = parameters.fitCriterion()
    self.updateDatabase('call updateTemplateRequirement(:id,:name,:asset,:type,:desc,:rat,:fc)',{'id':reqId,'name':reqName,'asset':reqAsset,'type':reqType,'desc':reqDesc,'rat':reqRat,'fc':reqFC},'MySQL error updating template requirement')

  def getTemplateRequirements(self,constraintId = -1):
    rows = self.responseList('call getTemplateRequirements(:const)',{'const':constraintId},'MySQL error getting template requirements')
    templateReqs = {}
    for reqId,reqName,assetName,reqType,reqDesc,reqRat,reqFC in rows:
      parameters = TemplateRequirementParameters(reqName,assetName,reqType,reqDesc,reqRat,reqFC)
      templateReq = ObjectFactory.build(reqId,parameters)
      templateReqs[reqName] = templateReq
    return templateReqs

  def deleteTemplateRequirement(self,reqId):
    self.deleteObject(reqId,'template_requirement')
    

  def componentViewRequirements(self,cvName): return self.responseList('call componentViewRequirements(:cv)',{'cv':cvName},'MySQL error getting component view requirements')

  def componentViewGoals(self,cvName): return self.responseList('call componentViewGoals(:cv)',{'cv':cvName},'MySQL error getting component view goals')

  def situateComponentViewRequirements(self,cvName):
    self.updateDatabase('call situateComponentViewRequirements(:cv)',{'cv':cvName},'MySQL error situating component view requirements')

  def getComponents(self,constraintId = -1):
    componentRows = self.responseList('call getAllComponents(:const)',{'const':constraintId},'MySQL error getting components')
    components = {}
    for componentId,componentName,componentDesc in componentRows:
      componentInterfaces = self.componentInterfaces(componentId)
      componentStructure = self.componentStructure(componentId)
      componentReqs = self.componentRequirements(componentId)
      componentGoals = self.componentGoals(componentId)
      assocs = self.componentGoalAssociations(componentId)
      comParameters = ComponentParameters(componentName,componentDesc,componentInterfaces,componentStructure,componentReqs,componentGoals,assocs)
      comParameters.setId(componentId)
      component = ObjectFactory.build(componentId,comParameters)
      components[componentName] = component
    return components

  def personasImpact(self,cvName,envName):
    rows = self.responseList('call personasImpact(:cv,:env)',{'cv':cvName,'env':envName},'MySQL error getting personas impact')
    pImpact = []
    for c1,c2 in rows: pImpact.append((c1,str(c2)))
    return pImpact

  def taskUseCases(self,taskName): return self.responseList('call taskUseCases(:task)',{'task':taskName},'MySQL error getting task use cases')

  def usecaseComponents(self,ucName): return self.responseList('call usecaseComponents(:useCase)',{'useCase':ucName},'MySQL error getting use case components')

  def attackSurfaceMetric(self,cvName):
    return self.responseList('call attackSurfaceMetric(:cv)',{'cv':cvName},'MySQL error getting attack surface metrics')[0]

  def componentAssetModel(self,componentName):
    rows = self.responseList('call componentClassModel(:comp)',{'comp':componentName},'MySQL error getting component asset model')
    associations = {}
    for headName,headType,headNav,headMult,headRole,tailRole,tailMult,tailNav,tailType,tailName in rows:
      associationId = -1
      envName = ''
      headDim  = 'template_asset'
      tailDim  = 'template_asset'
      rationale = ''
      parameters = ClassAssociationParameters(envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = envName + '/' + headName + '/' + tailName
      associations[asLabel] = association
    return associations

  def getInternalDocuments(self,constraintId = -1):
    rows = self.responseList('call getInternalDocuments(:id)',{'id':constraintId},'MySQL error getting internal documents')
    idObjts = {}
    for docId,docName,docDesc,docContent in rows:
      docCodes = self.documentCodes(docName)
      docMemos = self.documentMemos(docName)
      parameters = InternalDocumentParameters(docName,docDesc,docContent,docCodes,docMemos)
      idObjt = ObjectFactory.build(docId,parameters)
      idObjts[docName] = idObjt
    return idObjts

  def deleteInternalDocument(self,docId = -1):
    self.deleteObject(docId,'internal_document')
    

  def addInternalDocument(self,parameters):
    docId = self.newId()
    docName = parameters.name()
    docDesc = parameters.description()
    docContent = parameters.content()
    docCodes = parameters.codes()
    docMemos = parameters.memos()
    self.updateDatabase('call addInternalDocument(:id,:name,:desc,:cont)',{'id':docId,'name':docName,'desc':docDesc,'cont':docContent},'MySQL error adding internal document')
    self.addDocumentCodes(docName,docCodes)
    self.addDocumentMemos(docName,docMemos)
    return docId

  def updateInternalDocument(self,parameters):
    docId = parameters.id()
    docName = parameters.name()
    docDesc = parameters.description()
    docContent = parameters.content()
    docCodes = parameters.codes()
    docMemos = parameters.memos()
    session = self.updateDatabase('call deleteInternalDocumentComponents(:id)',{'id':docId},'MySQL error deleting internal document components',None,False)
    self.updateDatabase('call updateInternalDocument(:id,:name,:desc,:cont)',{'id':docId,'name':docName,'desc':docDesc,'cont':docContent},'MySQL error updating internal document',session)
    self.addDocumentCodes(docName,docCodes)
    self.addDocumentMemos(docName,docMemos)

  def getCodes(self,constraintId = -1):
    rows = self.responseList('call getCodes(:const)',{'const':constraintId},'MySQL error getting code')
    cObjts = {}
    for codeId,codeName,codeType,codeDesc,incCriteria,codeEg in rows:
      parameters = CodeParameters(codeName,codeType,codeDesc,incCriteria,codeEg)
      cObjt = ObjectFactory.build(codeId,parameters)
      cObjts[codeName] = cObjt
    return cObjts

  def deleteCode(self,codeId = -1):
    self.deleteObject(codeId,'code')
    

  def addCode(self,parameters):
    codeId = self.newId()
    codeName = parameters.name()
    codeType = parameters.type()
    codeDesc = parameters.description()
    incCriteria = parameters.inclusionCriteria()
    codeEg  = parameters.example()
    self.updateDatabase('call addCode(:id,:name,:type,:desc,:crit,:eg)',{'id':codeId,'name':codeName,'type':codeType,'desc':codeDesc,'crit':incCriteria,'eg':codeEg},'MySQL error adding code')
    return codeId


  def updateCode(self,parameters):
    codeId = parameters.id()
    codeName = parameters.name()
    codeType = parameters.type()
    codeDesc = parameters.description()
    incCriteria = parameters.inclusionCriteria()
    codeEg  = parameters.example()
    self.updateDatabase('call updateCode(:id,:name,:type,:desc,:crit,:eg)',{'id':codeId,'name':codeName,'type':codeType,'desc':codeDesc,'crit':incCriteria,'eg':codeEg},'MySQL error updating code')

  def documentCodes(self,docName):
    rows = self.responseList('call documentCodes(:name)',{'name':docName},'MySQL error getting document code')
    codes = {}
    for codeName,startIdx,endIdx in rows:
      startIdx = int(startIdx)
      endIdx = int(endIdx)
      codes[(startIdx,endIdx)] = codeName
    return codes
  
  def addDocumentCodes(self,docName,docCodes):
    for (startIdx,endIdx) in docCodes:
      docCode = docCodes[(startIdx,endIdx)]
      self.addDocumentCode(docName,docCode,startIdx,endIdx)

  def addDocumentCode(self,docName,docCode,startIdx,endIdx,codeLabel='',codeSynopsis=''):
    self.updateDatabase('call addDocumentCode(:name,:code,:sIdx,:eIdx,:lbl,:syn)',{'name':docName,'code':docCode,'sIdx':startIdx,'eIdx':endIdx,'lbl':codeLabel,'syn':codeSynopsis},'MySQL error adding document code')

  def artifactCodes(self,artName,artType,sectName):
    rows = self.responseList('call artifactCodes(:art,:type,:sect)',{'art':artName,'type':artType,'sect':sectName},'MySQL error getting artifact codes')
    codes = {}
    for codeName,startIdx,endIdx in rows:
      startIdx = int(startIdx)
      endIdx = int(endIdx)
      codes[(startIdx,endIdx)] = codeName
    return codes

  def addPersonaCodes(self,pName,codes):
    if len(codes) > 0:
      for sectName in ['activities','attitudes','aptitudes','motivations','skills']:
        self.addArtifactCodes(pName,'persona',sectName,codes[sectName])

  def addPersonaEnvironmentCodes(self,pName,envName,codes):
    if len(codes) > 0:
      for sectName in ['narrative']:
        self.addArtifactEnvironmentCodes(pName,envName,'persona',sectName,codes[sectName])


  def addTaskEnvironmentCodes(self,tName,envName,codes):
    if len(codes) > 0:
      for sectName in ['narrative','benefits','consequences']:
        self.addArtifactEnvironmentCodes(tName,envName,'task',sectName,codes[sectName])

  def addArtifactCodes(self,artName,artType,sectName,docCodes):
    for (startIdx,endIdx) in docCodes:
      docCode = docCodes[(startIdx,endIdx)]
      self.addArtifactCode(artName,artType,sectName,docCode,startIdx,endIdx)

  def addArtifactCode(self,artName,artType,sectName,docCode,startIdx,endIdx):
    self.updateDatabase('call addArtifactCode(:art,:type,:sect,:code,:sIdx,:eIdx)',{'art':artName,'type':artType,'sect':sectName,'code':docCode,'sIdx':startIdx,'eIdx':endIdx},'MySQL error adding artifact code')

  def personaCodes(self,pName):
    codeBook = {}
    for sectName in ['activities','attitudes','aptitudes','motivations','skills','intrinsic','contextual']:
      codeBook[sectName] = self.artifactCodes(pName,'persona',sectName)
    return codeBook

  def personaEnvironmentCodes(self,pName,envName):
    codeBook = {}
    for sectName in ['narrative']:
      codeBook[sectName] = self.artifactEnvironmentCodes(pName,envName,'persona',sectName)
    return codeBook

  def taskEnvironmentCodes(self,tName,envName):
    codeBook = {}
    for sectName in ['narrative','benefits','consequences']:
      codeBook[sectName] = self.artifactEnvironmentCodes(tName,envName,'task',sectName)
    return codeBook

  def artifactEnvironmentCodes(self,artName,envName,artType,sectName):
    rows = self.responseList('call artifactEnvironmentCodes(:art,:env,:type,:sect)',{'art':artName,'env':envName,'type':artType,'sect':sectName},'MySQL error getting artifact environment codes')
    codes = {}
    for codeName,startIdx,endIdx in rows:
      startIdx = int(startIdx)
      endIdx = int(envIdx)
      codes[(startIdx,endIdx)] = codeName
    return codes

  def addArtifactEnvironmentCodes(self,artName,envName,artType,sectName,docCodes):
    for (startIdx,endIdx) in docCodes:
      docCode = docCodes[(startIdx,endIdx)]
      self.addArtifactEnvironmentCode(artName,envName,artType,sectName,docCode,startIdx,endIdx)

  def addArtifactEnvironmentCode(self,artName,envName,artType,sectName,docCode,startIdx,endIdx):
    self.updateDatabase('call addArtifactEnvironmentCode(:art,:env,:type,:sect,:code,:sIdx,:eIdx)',{'art':artName,'env':envName,'type':artType,'sect':sectName,'code':docCode,'sIdx':startIdx,'eIdx':endIdx},'MySQL error adding artifact environment code')

  def personaCodeNetwork(self,personaName,fromCode='',toCode=''):
    return self.responseList('call artifactCodeNetwork(:pers,:a,:fCode,:tCode)',{'pers':personaName,'a':'persona','fCode':fromCode,'tCode':toCode},'MySQL error getting persona code network')

  def addCodeRelationship(self,personaName,fromName,toName,rshipType):
    self.updateDatabase('call addArtifactCodeNetwork(:pers,:a,:fName,:tName,:type)',{'pers':personaName,'a':'persona','fName':fromName,'tName':toName,'type':rshipType},'MySQL error adding code relationship')

  def updateCodeNetwork(self,personaName,rships):
    self.updateDatabase('call deleteArtifactCodeNetwork(:pers,:a)',{'pers':personaName,'a':'persona'},'MySQL error deleting artifact code network')
    for fromName,toName,rshipType in rships:
      self.addCodeRelationship(personaName,fromName,toName,rshipType)



  def impliedProcessNetwork(self,ipName): return self.responseList('call impliedProcessNetwork(:name)',{'name':ipName},'MySQL error getting implied process network')

  def addImpliedProcess(self,parameters):
    ipId = self.newId()
    ipName = parameters.name()
    ipDesc = parameters.description()
    pName = parameters.persona()
    cNet = parameters.network()
    ipSpec = parameters.specification()
    chs = parameters.channels()
    self.updateDatabase('call addImpliedProcess(:id,:name,:desc,:proc,:spec)',{'id':ipId,'name':ipName,'desc':ipDesc,'proc':pName,'spec':ipSpec},'MySQL error adding implied process')
    self.addImpliedProcessNetwork(ipId,pName,cNet)
    self.addImpliedProcessChannels(ipId,chs)
    return ipId

  def addImpliedProcessNetwork(self,ipId,personaName,cNet):
    for fromName,fromType,toName,toType,rType in cNet:
      self.addImpliedProcessNetworkRelationship(ipId,personaName,fromName,toName,rType)

  def addImpliedProcessNetworkRelationship(self,ipId,personaName,fromName,toName,rType):
    self.updateDatabase('call addImpliedProcessNetworkRelationship(:id,:pers,:fName,:tName,:type)',{'id':ipId,'pers':personaName,'fName':fromName,'tName':toName,'type':rType},'MySQL error adding implied process network relationship')

  def deleteImpliedProcess(self,ipId): self.deleteObject(ipId,'persona_implied_process')
    
  def addStepSynopsis(self,ucName,envName,stepNo,synName,aType,aName): self.updateDatabase('call addStepSynopsis(:uc,:env,:step,:syn,:aName,:aType)',{'uc':ucName,'env':envName,'step':stepNo,'syn':synName,'aName':aName,'aType':aType},'MySQL error adding step synopsis')

  def directoryEntry(self,objtName,dType): return self.responseList('call directoryEntry(:obj,:dir)',{'obj':objtName,'dir':dType},'MySQL error getting directory entry')[0]

  def getTemplateGoals(self,constraintId = -1):
    tgRows = self.responseList('call getTemplateGoals(:const)',{'const':constraintId},'MySQL error getting template goals')
    templateGoals = {}
    for tgId,tgName,tgDef,tgRat in tgRows:
      tgConcerns = self.templateGoalConcerns(tgId)
      tgResps = self.templateGoalResponsibilities(tgId)
      parameters = TemplateGoalParameters(tgName,tgDef,tgRat,tgConcerns,tgResps)
      templateGoal = ObjectFactory.build(tgId,parameters)
      templateGoals[tgName] = templateGoal
    return templateGoals

  def deleteTemplateGoal(self,tgId):
    self.deleteObject(tgId,'template_goal')
    
  def componentViewGoals(self,cvName): return self.responseList('call componentViewGoals(:cv)',{'cv':cvName},'MySQL error getting component view goals')

  def situateComponentViewGoals(self,cvName,envName):
    self.updateDatabase('call situateComponentViewGoals(:cv,:env)',{'cv':cvName,'env':envName},'MySQL error situating component view goals')

  def situateComponentViewGoalAssociations(self,cvName,envName):
    self.updateDatabase('call situateComponentViewGoalAssociations(:cv,:env)',{'cv':cvName,'env':envName},'MySQL error situating component view goal associations')

  def templateGoalConcerns(self,tgId):
    return self.responseList('call templateGoalConcerns(:tg)',{'tg':tgId},'MySQL error getting template goal concerns')

  def addTemplateGoal(self,parameters):
    goalId = self.newId()
    goalName = parameters.name()
    goalDef = parameters.definition()
    goalRat = parameters.rationale()
    goalConcerns = parameters.concerns()
    goalResponsibilities = parameters.responsibilities()
    self.updateDatabase('call addTemplateGoal(:id,:name,:def,:rat)',{'id':goalId,'name':goalName,'def':goalDef,'rat':goalRat},'MySQL error adding template goal')
    self.addTemplateGoalConcerns(goalId,goalConcerns)
    self.addTemplateGoalResponsibilities(goalId,goalResponsibilities)
    return goalId

  def updateTemplateGoal(self,parameters):
    goalId = parameters.id()
    goalName = parameters.name()
    goalDef = parameters.definition()
    goalRat = parameters.rationale()
    goalConcerns = parameters.concerns()
    goalResponsibilities = parameters.responsibilities()
    session = self.updateDatabase('call deleteTemplateGoalComponents(:id)',{'id':goalId},'MySQL error deleting template goal components',None,False)
    self.updateDatabase('call updateTemplateGoal(:id,:name,:def,:rat)',{'id':goalId,'name':goalName,'def':goalDef,'rat':goalRat},'MySQL error updating template goals',session)
    self.addTemplateGoalConcerns(goalId,goalConcerns)
    self.addTemplateGoalResponsibilities(goalId,goalResponsibilities)


  def addTemplateGoalConcerns(self,goalId,concerns):
    for concern in concerns:
      if concern != '':
        self.addTemplateGoalConcern(goalId,concern)

  def addTemplateGoalConcern(self,goalId,concern):
    self.updateDatabase('call add_template_goal_concern(:id,:con)',{'id':goalId,'con':concern},'MySQL error adding template goal concern')

  def componentGoals(self,componentId):
    return self.responseList('call getComponentGoals(:comp)',{'comp':componentId},'MySQL error getting component goals')

  def addComponentGoals(self,componentId,componentGoals):
    for idx,goalName in enumerate(componentGoals):
      self.addComponentGoal(componentId,goalName)

  def addComponentGoal(self,componentId,goalName):
    self.updateDatabase('call addComponentGoal(:comp,:goal)',{'comp':componentId,'goal':goalName},'MySQL error adding component goal')

  def addComponentAssociations(self,componentId,assocs):
    for idx,assoc in enumerate(assocs):
      self.addComponentGoalAssociation(componentId,assoc[0],assoc[1],assoc[2],assoc[3])

  def addComponentGoalAssociation(self,componentId,goalName,subGoalName,refType,rationale):
    self.updateDatabase('call addComponentGoalAssociation(:comp,:goal,:sGoal,:ref,:rationale)',{'comp':componentId,'goal':goalName,'sGoal':subGoalName,'ref':refType,'rationale':rationale},'MySQL error adding component goal association')

  def componentGoalAssociations(self,componentId):
    return self.responseList('call componentGoalAssociations(:comp)',{'comp':componentId},'MySQL error getting component goal associations')

  def componentAttackSurface(self,cName):
    return self.responseList('call componentAttackSurfaceMetric(:comp)',{'comp':cName},'MySQL error getting component attack surface metric')[0]

  def componentGoalModel(self,componentName):
    rows = self.responseList('call componentGoalModel(:comp)',{'comp':componentName},'MySQL error getting component goal model')
    associations = {}
    for associationId,envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale in rows:
      parameters = GoalAssociationParameters(envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = envName + '/' + goalName + '/' + subGoalName + '/' + aType
      associations[asLabel] = association
    return associations

  def mergeComponent(self,parameters):
    componentId = parameters.id()
    componentName = parameters.name()
    componentDesc = parameters.description()
    structure = parameters.structure()
    requirements = parameters.requirements()
    goals = parameters.goals()
    assocs = parameters.associations()
    for ifName,ifType,arName,pName in parameters.interfaces():
      self.addComponentInterface(componentId,ifName,ifType,arName,pName)
    self.addComponentStructure(componentId,structure)
    self.addComponentRequirements(componentId,requirements)
    self.addComponentGoals(componentId,goals)
    self.addComponentAssociations(componentId,assocs)

  def addTemplateGoalResponsibilities(self,goalId,resps):
    for resp in resps:
      if resp != '':
        self.addTemplateGoalResponsibility(goalId,resp)

  def addTemplateGoalResponsibility(self,goalId,resp):
    self.updateDatabase('call add_template_goal_responsibility(:goal,:resp)',{'goal':goalId,'resp':resp},'MySQL error adding template goal responsibility')

  def templateGoalResponsibilities(self,tgId):
    return self.responseList('call templateGoalResponsibilities(:tg)',{'tg':tgId},'MySQL error getting template goal responsibilities')

  def importTemplateAsset(self,taName,environmentName): self.updateDatabase('call importTemplateAssetIntoEnvironment(:ta,:env)',{'ta':taName,'env':environmentName},'MySQL error importing template asset')

  def candidateGoalObstacles(self,cvName,envName):
    return self.responseList('call candidateGoalObstacles(:cv,:env)',{'cv':cvName,'env':envName},'MySQL error getting candidate goal obstacles')

  def templateGoalDefinition(self,tgId): return self.responseList('select definition from template_goal where id =:tg',{'tg':tgId},'MySQL error getting template goal definition')[0]

  def redmineArchitectureSummary(self,envName):
    return self.responseList('call redmineArchitectureSummary(:env)',{'env':envName},'MySQL error getting redmine architecture summary')

  def redmineAttackPatternsSummary(self,envName):
    return self.responseList('call redmineAttackPatternsSummary(:env)',{'env':envName},'MySQL error getting redmine attack patterns summary')[0]

  def processesToXml(self,includeHeader=True): return self.responseList('call processesToXml(:head)',{'head':includeHeader},'MySQL error exporting processes to XML')[0]

  def addQuotation(self,quotation):
    qType = quotation[0]
    cmName = quotation[1]
    artType = quotation[2]
    artName = quotation[3]
    envName = quotation[4]
    sectName = quotation[5]
    startIdx = quotation[6]
    endIdx = quotation[7]
    codeLabel = quotation[8]
    codeSynopsis = quotation[9]

    if artType == 'internal_document':
      if qType == 'memo':
        self.addDocumentMemo(artName,cmName,'',startIdx,endIdx)
      else:
        self.addDocumentCode(artName,cmName,startIdx,endIdx,codeLabel,codeSynopsis)
    else:
      if envName == 'None':
        self.addArtifactCode(artName,artType,sectName,cmName,startIdx,endIdx)
      else:
        self.addArtifactEnvironmentCode(artName,envName,artType,sectName,cmName,startIdx,endIdx)

  def getMemos(self,constraintId = -1):
    rows = self.responseList('call getMemos(:const)',{'const':constraintId},'MySQL error getting memos')
    mObjts = {}
    for memoId,memoName,memoDesc in rows:
      parameters = MemoParameters(memoName,memoDesc)
      mObjt = ObjectFactory.build(memoId,parameters)
      mObjts[memoName] = mObjt
    return mObjts

  def deleteMemo(self,memoId = -1):
    self.deleteObject(memoId,'memo')
    

  def addMemo(self,parameters):
    memoId = self.newId()
    memoName = parameters.name()
    memoDesc = parameters.description()
    self.updateDatabase('call addMemo(:id,:name,:desc)',{'id':memoId,'name':memoName,'desc':memoDesc},'MySQL error adding memo')
    return memoId

  def updateMemo(self,parameters):
    memoId = parameters.id()
    memoName = parameters.name()
    memoDesc = parameters.description()
    self.updateDatabase('call updateMemo(:id,:name,:desc)',{'id':memoId,'name':memoName,'desc':memoDesc},'MySQL error updating memo')

  def documentMemos(self,docName):
    rows = self.responseList('call documentMemos(:doc)',{'doc':docName},'MySQL error getting document memo')
    memos = {}
    for memoName,memoTxt,startIdx,endIdx in rows:
      startIdx = int(startIdx)
      endIdx = int(endIdx)
      memos[(startIdx,endIdx)] = (memoName,memoTxt)
    return memos

  def addDocumentMemos(self,docName,docMemos):
    for (startIdx,endIdx) in docMemos:
      memoName,memoTxt = docMemos[(startIdx,endIdx)]
      self.addDocumentMemo(docName,memoName,memoTxt,startIdx,endIdx)

  def addDocumentMemo(self,docName,memoName,memoTxt,startIdx,endIdx):
    self.updateDatabase('call addDocumentMemo(:doc,:mem,:txt,:sIdx,:eIdx)',{'doc':docName,'mem':memoName,'txt':memoTxt,'sIdx':startIdx,'eIdx':endIdx},'MySQL error adding document memo')

  def impliedProcess(self,procName): return self.responseList('call impliedProcess(:proc)',{'proc':procName},'MySQL error getting implied process')[0]

  def addImpliedProcessChannels(self,ipId,channels):
    for channelName,dataType in channels:
      self.addImpliedProcessChannel(ipId,channelName,dataType)

  def addImpliedProcessChannel(self,ipId,channelName,dataType):
    self.updateDatabase('call addImpliedProcessChannel(:id,:chan,:type)',{'id':ipId,'chan':channelName,'type':dataType},'MySQL error adding implied process channel')

  def getQuotations(self):
    return self.responseList('call getQuotations()',{},'MySQL error getting quotations')

  def updateQuotation(self,codeName,atName,aName,oldStartIdx,oldEndIdx,startIdx,endIdx,synopsis,label):
    if atName == 'internal_document':
      self.updateDatabase('call updateDocumentCode(:aName,:code,:oSIdx,:oEIdx,:sIdx,:eIdx,:syn,:lbl)',{'aName':aName,'code':codeName,'oSIdx':oldStartIdx,'oEIdx':oldEndIdx,'sIdx':startIdx,'eIdx':endIdx,'syn':synopsis,'lbl':label},'MySQL error updating quotation')

  def deleteQuotation(self,codeName,atName,aName,startIdx,endIdx):
    if atName == 'internal_document':
      self.updateDatabase('call deleteDocumentCode(:aName,:code,:sIdx,:eIdx)',{'aName':aName,'code':codeName,'sIdx':startIdx,'eIdx':endIdx},'MySQL error deleting quotation')

  def impliedCharacteristic(self,pName,fromCode,toCode,rtName):
    row = self.responseList('call impliedCharacteristic(:pName,:fCode,:tCode,:rt)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName},'MySQL error getting implied characteristic')[0]
    if (len(row) == 0): raise NoImpliedCharacteristic(pName,fromCode,toCode,rtName)
    return row

  def addImpliedCharacteristic(self,parameters):
    pName = parameters.persona()
    fromCode = parameters.fromCode()
    toCode = parameters.toCode()
    rtName = parameters.relationshipType()
    charName = parameters.characteristic()
    qualName = parameters.qualifier()
    lhsCodes = parameters.lhsCodes()
    rhsCodes = parameters.rhsCodes()
    charType = parameters.characteristicType()
   
    self.updateDatabase('call addImpliedCharacteristic(:pName,:fCode,:tCode,:rt,:pChar,:qual,:cType)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName,'pChar':charName,'qual':qualName,'cType':charType},'MySQL error adding implied characteristic')
    for lblName,rtName in lhsCodes:
      self.addImpliedCharacteristicElement(charName,lblName,rtName)
    for lblName,rtName in rhsCodes:
      self.addImpliedCharacteristicElement(charName,lblName,rtName)


  def updateImpliedCharacteristic(self,parameters):
    pName = parameters.persona()
    fromCode = parameters.fromCode()
    toCode = parameters.toCode()
    rtName = parameters.relationshipType()
    charName = parameters.characteristic()
    qualName = parameters.qualifier()
    lhsCodes = parameters.lhsCodes()
    rhsCodes = parameters.rhsCodes()
    charType = parameters.characteristicType()
    intName = parameters.intention()
    intType = parameters.intentionType()
   
    self.updateDatabase('call updateImpliedCharacteristic(:pName,:fCode,:tCode,:rt,:char,:qual,:cType)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName,'char':charName,'qual':qualName,'cType':charType},'MySQL error updating implied characteristic')
    for lblName,rtName in lhsCodes:
      self.updateImpliedCharacteristicElement(charName,lblName,rtName)
    for lblName,rtName in rhsCodes:
      self.updateImpliedCharacteristicElement(charName,lblName,rtName)
    self.updateImpliedCharacteristicIntention(charName,intName,intType)

  def updateImpliedCharacteristicIntention(self,charName,intName,intType): self.updateDatabase('call updateImpliedCharacteristicIntention(:char,:int,:type)',{'char':charName,'int':intName,'type':intType},'MySQL error updating implied characteristic intention')

  def addImpliedCharacteristicElement(self,charName,lblName,rtName):
    self.updateDatabase('call addImpliedCharacteristicElement(:char,:lbl,:rt)',{'char':charName,'lbl':lblName,'rt':rtName},'MySQL error adding implied characteristic element')

  def updateImpliedCharacteristicElement(self,charName,lblName,rtName): self.updateDatabase('call updateImpliedCharacteristicElement(:char,:lbl,:rt)',{'char':charName,'lbl':lblName,'rt':rtName},'MySQL error updating implied characteristic element')

  def codeCount(self,codeName): return self.responseList('select codeCount(:code)',{'code':codeName},'MySQL error getting code count')[0]

  def addIntention(self,intention):
    refName = intention[0]
    refType = intention[1]
    intentionName = intention[2]
    intentionType = intention[3]
    self.updateDatabase('call addIntention(:ref,:rType,:int,:iType)',{'ref':refName,'rType':refType,'int':intentionName,'iType':intentionType},'MySQL error adding intention')

  def addContribution(self,contribution):
    srcName = contribution[0]
    destName = contribution[1]
    meansEnd = contribution[2]
    valName = contribution[3]
    self.updateDatabase('call addContribution(:src,:dest,:means,:val)',{'src':srcName,'dest':destName,'means':meansEnd,'val':valName},'MySQL error adding contribution')

  def impliedCharacteristicIntention(self,synName,pName,fromCode,toCode,rtName): return self.responseLis('select impliedCharacteristicIntention(:syn,:pName,:fCode,:tCode,:rt)',{'syn':synName,'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName},'MySQL error getting implied characteristic intention')[0].split('#')

  def impliedCharacteristicElementIntention(self,ciName,elName): return self.responseList('select impliedCharacteristicElementIntention(:ci,:el)',{'ci':ciName,'el':elName},'MySQL error getting implied characteristic element intention')[0].split('#')

  def updateImpliedCharacteristicElementIntention(self,ciName,elName,intName,intDim,meName,contName): self.updateDatabase('call updateImpliedCharacteristicElementIntention(:ci,:el,:int,:dim,:me,:cont)',{'ci':ciName,'el':elName,'int':intName,'dim':intDim,'me':meName,'cont':contName},'MySQL error updating intention for element ' + elName + ' for implied characteristic ' + ciName)

  def deniedGoals(self,codeName): return self.responseList('call deniedGoals(:code)',{'code':codeName},'MySQL error getting denied goals')

  def addLocations(self,parameters):
    locsId = self.newId()
    locsName = parameters.name()
    locDiagram = parameters.diagram()
    locations = parameters.locations()
    links = parameters.links()
    self.updateDatabase('call addLocations(:id,:name,:diag)',{'id':locsId,'name':locsName,'diag':locDiagram},'MySQL error adding locations')
    for location in locations:
      self.addLocation(locsId,location)
    for link in links:
      self.addLocationLink(locsId,link)
    return locsId

  def updateLocations(self,parameters):
    locsId = parameters.id()
    self.deleteLocations(locsId)
    self.addLocations(parameters)

 
  def addLocation(self,locsId,location):
    locId = self.newId()
    locName = location.name()
    assetInstances = location.assetInstances()
    personaInstances = location.personaInstances()
    self.updateDatabase('call addLocation(:locsId,:locId,:locName)',{'locsId':locsId,'locId':locId,'locName':locName},'MySQL error adding location')
    for assetInstance in assetInstances:
      self.addAssetInstance(locId,assetInstance)
    for personaInstance in personaInstances:
      self.addPersonaInstance(locId,personaInstance)

  def addAssetInstance(self,locId,assetInstance):
    instanceId = self.newId()
    instanceName = assetInstance[0]
    assetName = assetInstance[1]
    self.updateDatabase('call addAssetInstance(:lId,:iId,:iName,:assName)',{'lId':locId,'iId':instanceId,'iName':instanceName,'assName':assetName},'MySQL error adding asset instance')

  def addPersonaInstance(self,locId,personaInstance):
    instanceId = self.newId()
    instanceName = personaInstance[0]
    personaName = personaInstance[1]
    self.updateDatabase('call addPersonaInstance(:lId,:iId,:iName,:pName)',{'lId':locId,'iId':instanceId,'iName':instanceName,'pName':personaName},'MySQL error adding persona instance')

  def addLocationLink(self,locsId,link):
    tailLoc = link[0]
    headLoc = link[1]
    self.updateDatabase('call addLocationLink(:lId,:tLoc,:hLoc)',{'lId':locsId,'tLoc':tailLoc,'hLoc':headLoc},'MySQL error adding location link')

  def getLocations(self,constraintId = -1):
    locsRows = self.responseList('call getLocations(:const)',{'const':constraintId},'MySQL error getting locations')
    locationsDict = {}
    for locsId,locsName,locsDia in locsRows:
      locNames = self.getLocationNames(locsName)
      linkDict = self.getLocationLinks(locsName)
      locs = []
      for locName in locNames:
        assetInstances = self.getAssetInstances(locName)
        personaInstances = self.getPersonaInstances(locName)
        locLinks = []
        if locName in linkDict:
          locLinks = linkDict[locName]
        loc = Location(-1,locName,assetInstances,personaInstances,locLinks)
        locs.append(loc)
      p = LocationsParameters(locsName,locsDia,locs)
      locations = ObjectFactory.build(locsId,p)
      locationsDict[locsName] = locations
    return locationsDict

  def getLocationNames(self,locsName):
    return self.responseList('call getLocationNames(:locs)',{'locs':locsName},'MySQL error getting location names')

  def getLocationLinks(self,locsName):
    rows = self.responseList('call getLocationLinks(:locs)',{'locs':locsName},'MySQL error getting location links')
    linkDict = {}
    for tailLoc,headLoc in rows:
      if tailLoc in linkDict: linkDict[tailLoc].append(headLoc)
      else:
        linkDict[tailLoc] = [headLoc]

      if headLoc in linkDict: 
        linkDict[headLoc].append(tailLoc)
      else:
        linkDict[headLoc] = [tailLoc]
    return linkDict

  def getAssetInstances(self,locName):
    return self.responseList('call getAssetInstances(:locs)',{'locs':locName},'MySQL error getting asset instances')

  def getPersonaInstances(self,locName):
    return self.responseList('call getPersonaInstances(:locs)',{'locs':locName},'MySQL error getting persona instances')

  def deleteLocations(self,locsId):
    self.deleteObject(locsId,'locations')
    

  def locationsRiskModel(self,locationsName,environmentName):
    traceRows = self.responseList('call locationsRiskModel(:locs,:env)',{'locs':locationsName,'env':environmentName},'MySQL error getting location risk model')
    traces = []
    for fromObjt,fromName,toObjt,toName in traceRows:
      parameters = DotTraceParameters(fromObjt,fromName,toObjt,toName)
      traces.append(ObjectFactory.build(-1,parameters))
    return traces

  def templateAssetMetrics(self,taName): return self.responseList('call templateAssetMetrics(:ta)',{'ta':taName},'MySQL error getting template asset metrics')[0]

  def riskModelElements(self,envName):
    rows = self.responseList('call riskAnalysisModelElements(:env)',{'env':envName},'MySQL error getting risk analysis model elements')
    elNames = []
    for c0,c1 in rows:
      elNames.append(c1)
    return elNames

  def assetThreatRiskLevel(self,assetName,threatName,envName):
    return self.responseList('call assetThreatRiskLevel(:ass,:thr,:env)',{'ass':assetName,'thr':threatName,'env':envName},'MySQL error getting asset threat risk level')[0]

  def assetRiskLevel(self,assetName,envName):
    return self.responseList('call assetRiskLevel(:ass,:env)',{'ass':assetName,'env':envName},'MySQL error getting asset risk level')[0]

  def dimensionSummary(self,dimName,envName):
    return self.responseList('call ' + dimName + 'Summary(:name)',{'name':envName},'MySQL error getting ' + dimName + ' summary for environment ' + envName)

  def createDatabase(self,dbName,session_id):
    if self.conn is not None:
      self.conn.close()
    b = Borg()
    ses_settings = b.get_settings(session_id)
    dbHost = ses_settings['dbHost']
    dbPort = ses_settings['dbPort']
    rPasswd = ses_settings['rPasswd']
    dbUser = ses_settings['dbUser']
    userName = ses_settings['userName']
    dbPasswd = ses_settings['dbPasswd']
    dbName = dbUser + '_' + dbName
    createDatabaseAndPrivileges(rPasswd,dbHost,dbPort,userName,dbPasswd,dbName)
    b.settings[session_id]['dbName'] = dbName
    self.clearDatabase(session_id)
    self.reconnect(True,session_id)
    rootDir = b.cairisRoot
    createDefaults(rootDir,dbHost,dbPort,dbUser,dbPasswd,dbName)

  def openDatabase(self,dbName,session_id):
    b = Borg()
    b.settings[session_id]['dbName'] = dbName
    self.reconnect(True,session_id)


  def showDatabases(self,session_id):
    b = Borg()
    ses_settings = b.get_settings(session_id)
    dbUser = ses_settings['dbUser']
    dbName = ses_settings['dbName']
    rows = databases(dbUser)
    dbs = []
    for dbn,owner in rows:
      if (dbn != dbName):
        dbs.append((dbn.split(owner + '_')[1],owner))
    return dbs

  def checkPermissions(self,reqDbName,session_id):
    b = Borg()
    ses_settings = b.get_settings(session_id)
    dbUser = ses_settings['dbUser']
    currentDbName = ses_settings['dbName']
    defaultDbName = dbUser + '_default'
    reqDbName = dbUser + '_' + reqDbName
    restrictedDbs = [currentDbName,defaultDbName]
    rows = databases(dbUser)
    dbs = []
    for dbName, owner in rows:
      if (dbName not in restrictedDbs):
        if (reqDbName == dbName):
          return True
    return False


  def deleteDatabase(self,dbName,session_id):
    b = Borg()
    ses_settings = b.get_settings(session_id)
    dbHost = ses_settings['dbHost']
    dbPort = ses_settings['dbPort']
    rPasswd = ses_settings['rPasswd']

    if (self.checkPermissions(dbName,session_id) == False):
      exceptionText = 'You cannot remove this database.'
      raise DatabaseProxyException(exceptionText) 

    dbUser = canonicalDbUser(ses_settings['dbUser'])
    dbName = canonicalDbName(dbUser + '_' + dbName)
    try:
      dbEngine = create_engine('mysql+mysqldb://root'+':'+rPasswd+'@'+dbHost+':'+str(dbPort))
      tmpConn = scoped_session(sessionmaker(bind=dbEngine))
      stmts = ['drop database if exists `' + dbName + '`',
              'delete from cairis_owner.db_owner where db = "' + dbName + '" and owner = "' + dbUser + '"',
              'delete from mysql.db where Db = "' + dbName + '"']
      session = tmpConn()
      for stmt in stmts:
        session.execute(text(stmt))
      session.close()
      tmpConn.remove()
    except OperationalError as e:
      exceptionText = 'MySQL error creating CAIRIS database ' + dbName + '(message:' + format(e) + ')'
      raise DatabaseProxyException(exceptionText) 
    except DatabaseError as e:
      id,msg = e
      exceptionText = 'MySQL error creating CAIRIS database ' + dbName + '(id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getUseCaseRequirements(self,ucName):
    return self.responseList('call useCaseRequirements(:uc)',{'uc':ucName},'MySQL error getting requirements associated with use case ' + ucName)

  def getUseCaseGoals(self,ucName,envName): return self.responseList('call useCaseGoals(:uc,:env)',{'uc':ucName,'env':envName},'MySQL error getting goals associated with use case ' + ucName)

  def synopsisId(self,synTxt):
    return self.responseList('select synopsisId(:syn)',{'syn':synTxt},'MySQL error finding synopsis id for text ' + synTxt)[0]

  def hasContribution(self,contType,rsName,csName):
    sqlTxt = 'hasReferenceContribution'
    if contType == 'usecase':
      sqlTxt = 'hasUseCaseContribution'
    hasRC = self.responseList('select ' + sqlTxt + '(:rName,:cName)',{'rName':rsName,'cName':csName},'MySQL error checking contribution')[0]
    if (hasRC == 1): 
      return True
    else:
      return False

  def removeUseCaseContributions(self,ucId): self.updateDatabase('call removeUseCaseContributions(:id)',{'id':ucId},'MySQL error removing use case contribution')

  def getDataFlows(self,dfName='',fromName='',fromType='',toName='',toType='',envName=''):
    dfRows = self.responseList('call getDataFlows(:df,:fromName,:fromType,:toName,:toType,:env)',{'df':dfName,'fromName':fromName,'fromType':fromType,'toName':toName,'toType':toType,'env':envName},'MySQL error getting data flows')
    dataFlows = []
    for dfName,dfType,envName,fromName,fromType,toName,toType in dfRows:
      tags = self.getDataFlowTags(dfName,fromType,fromName,toType,toName,envName)
      dfAssets = self.getDataFlowAssets(dfName,fromName,fromType,toName,toType,envName)
      dfObs = self.getDataFlowObstacles(dfName,fromName,fromType,toName,toType,envName)
      parameters = DataFlowParameters(dfName,dfType,envName,fromName,fromType,toName,toType,dfAssets,dfObs,tags)
      df = ObjectFactory.build(-1,parameters)
      dataFlows.append(df)
    return dataFlows

  def getDataFlowAssets(self,dfName,fromName,fromType,toName,toType,envName):
    return self.responseList('call getDataFlowAssets(:df,:fromName,:fromType,:toName,:toType,:env)',{'df':dfName,'fromName':fromName,'fromType':fromType,'toName':toName,'toType':toType,'env':envName},'MySQL error getting assets for data flow ' + dfName)

  def getDataFlowObstacles(self,dfName,fromName,fromType,toName,toType,envName):
    return self.responseList('call getDataFlowObstacles(:df,:fromName,:fromType,:toName,:toType,:env)',{'df':dfName,'fromName':fromName,'fromType':fromType,'toName':toName,'toType':toType,'env':envName},'MySQL error getting obstacles for data flow ' + dfName)


  def addDataFlow(self,parameters):
    dfName = parameters.name()
    dfType = parameters.type()
    envName = parameters.environment()
    fromName = parameters.fromName()
    fromType = parameters.fromType()
    toName = parameters.toName()
    toType = parameters.toType()
    dfAssets = parameters.assets()
    dfObs = parameters.obstacles()
    tags = parameters.tags()
    self.updateDatabase('call addDataFlow(:df,:dfType,:env,:fName,:fType,:tName,:tType)',{'df':dfName,'dfType':dfType,'env':envName,'fName':fromName,'fType':fromType,'tName':toName,'tType':toType},'MySQL error adding data flow')
    self.addDataFlowTags(dfName,fromType,fromName,toType,toName,envName,tags)
    for dfAsset in dfAssets:
      self.addDataFlowAsset(dfName,envName,fromType,fromName,toType,toName,dfAsset)
    for dfOb in dfObs:
      self.addDataFlowObstacle(dfName,envName,fromType,fromName,toType,toName,dfOb)

  def addDataFlowAsset(self,dfName,envName,fromType,fromName,toType,toName,dfAsset):
    self.updateDatabase('call addDataFlowAsset(:df,:env,:fromType,:fromName,:toType,:toName,:ass)',{'df':dfName,'env':envName,'fromType':fromType,'fromName':fromName,'toType':toType,'toName':toName,'ass':dfAsset},'MySQL error adding data flow asset')

  def addDataFlowObstacle(self,dfName,envName,fromType,fromName,toType,toName,dfOb):
    obsName,kwd,dfoContext = dfOb
    self.updateDatabase('call addDataFlowObstacle(:df,:env,:fromType,:fromName,:toType,:toName,:ob,:kwd,:dfoContext)',{'df':dfName,'env':envName,'fromType':fromType,'fromName':fromName,'toType':toType,'toName':toName,'ob':obsName,'kwd':kwd,'dfoContext':dfoContext},'MySQL error adding data flow obstacle')

  def updateDataFlow(self,oldDfName,oldFromName,oldFromType,oldToName,oldToType,oldEnvName,parameters):
    dfName = parameters.name()
    dfType = parameters.type()
    envName = parameters.environment()
    fromName = parameters.fromName()
    fromType = parameters.fromType()
    toName = parameters.toName()
    toType = parameters.toType()
    dfAssets = parameters.assets()
    dfObs = parameters.obstacles()
    tags = parameters.tags()
    session = self.updateDatabase('call deleteDataFlowAssets(:df,:fromName,:fromType,:toName,:toType,:env)',{'df':oldDfName,'fromName':fromName,'fromType':fromType,'toName':toName,'toType':toType,'env':oldEnvName},'MySQL error deleting data flow assets',None,False)
    self.updateDatabase('call deleteDataFlowObstacles(:df,:fromName,:fromType,:toName,:toType,:env)',{'df':oldDfName,'fromName':fromName,'fromType':fromType,'toName':toName,'toType':toType,'env':oldEnvName},'MySQL error deleting data flow obstacles',session,False)
    self.updateDatabase('call updateDataFlow(:oldDfName,:oldFromName,:oldFromType,:oldToName,:oldToType,:oldEnvName,:dfName,:fromName,:fromType,:toName,:toType,:envName,:dfType)',{'oldDfName':oldDfName,'oldFromName':oldFromName,'oldFromType':oldFromType,'oldToName':oldToName,'oldToType':oldToType,'oldEnvName':oldEnvName,'dfName':dfName,'fromName':fromName,'fromType':fromType,'toName':toName,'toType':toType,'envName':envName,'dfType':dfType},'MySQL error updating data flow',session)
    self.addDataFlowTags(dfName,fromType,fromName,toType,toName,envName,tags)
    for dfAsset in dfAssets:
      self.addDataFlowAsset(dfName,envName,fromType,fromName,toType,toName,dfAsset)
    for dfOb in dfObs:
      self.addDataFlowObstacle(dfName,envName,fromType,fromName,toType,toName,dfOb)

  def deleteDataFlow(self,dfName,fromName,fromType,toName,toType,envName):
    self.updateDatabase('call deleteDataFlow(:df,:fromName,:fromType,:toName,:toType,:env)',{'df':dfName,'fromName':fromName,'fromType':fromType,'toName':toName,'toType':toType,'env':envName},'MySQL Error deleting data flow')

  def dataFlowDiagram(self,envName,filterType = 'None',filterElement = ''):
    return self.responseList('call dataFlowDiagram(:env,:ft,:fe)',{'env':envName,'ft':filterType,'fe':filterElement},'MySQL error getting data flow diagram')

  def personalDataFlowDiagram(self,envName,filterElement = ''):
    return self.responseList('call personalDataFlowDiagram(:env,:fe)',{'env':envName,'fe':filterElement},'MySQL error getting personal data flow diagram')

  def relabelRequirements(self,reqReference): self.updateDatabase('call relabelRequirements(:reqReference)',{'reqReference':reqReference},'MySQL error relabelling requirements')

  def getTrustBoundaries(self,constraintId = -1):
    tbRows = self.responseList('call getTrustBoundaries(:id)',{'id':constraintId},'MySQL error getting trust boundaries')
    tbs = [] 
    for tbId,tbName,tbType,tbDesc in tbRows:
      tags = self.getTags(tbName,'trust_boundary')
      components = {}
      privileges = {}
      for environmentId,environmentName in self.dimensionEnvironments(tbId,'trust_boundary'):
        components[environmentName] = self.trustBoundaryComponents(tbId,environmentId)
        privileges[environmentName] = self.trustBoundaryPrivilege(tbId,environmentId)
      tbs.append(TrustBoundary(tbId,tbName,tbType,tbDesc,components,privileges,tags))
    return tbs

  def trustBoundaryComponents(self,tbId, envId):
    return self.responseList('call trustBoundaryComponents(:tbId,:envId)',{'tbId':tbId,'envId':envId},'MySQL error getting trust boundary components for trust boundary id ' + str(tbId))

  def trustBoundaryPrivilege(self,tbId, envId):
    return self.responseList('select trustBoundaryPrivilege(:tbId,:envId)',{'tbId':tbId,'envId':envId},'MySQL error getting the trust boundary privilege level for trust boundary id ' + str(tbId))[0]

  def addTrustBoundary(self,tb):
    tbId = self.newId()
    self.updateDatabase("call addTrustBoundary(:id,:name,:type,:desc)",{'id':tbId,'name':tb.name(),'type':tb.type(),'desc':tb.description()},'MySQL error adding trust boundary ' + str(tbId))
    self.addTags(tb.name(),'trust_boundary',tb.tags())
    defaultPrivilegeLevels = {}
    for environmentName in list(tb.components().keys()):
      defaultPrivilegeLevels[environmentName] = 'None'
      for tbComponentType,tbComponent in tb.components()[environmentName]:
        self.addTrustBoundaryComponent(tbId,environmentName,tbComponent)
    tbPrivilegeLevels = tb.privilegeLevels()
    if (len(tbPrivilegeLevels) == 0):
      tbPrivilegeLevels = defaultPrivilegeLevels
    for environmentName in list(tbPrivilegeLevels.keys()):
      self.addTrustBoundaryPrivilege(tbId,environmentName,self.privilegeValue(tbPrivilegeLevels[environmentName]))

  def privilegeValue(self,pName): return self.responseList('select privilegeValue(:pName)',{'pName':pName},'MySQL error getting privilege value')[0]

  def addTrustBoundaryComponent(self,tbId,envName,tbComponent):
    self.updateDatabase('call addTrustBoundaryComponent(:id,:environment,:component)',{'id':tbId,'environment':envName,'component':tbComponent},'MySQL error adding trust boundary component ' + tbComponent + ' to trust boundary id ' + str(tbId))

  def addTrustBoundaryPrivilege(self,tbId,envName,pValue):
    self.updateDatabase('call addTrustBoundaryPrivilege(:id,:environment,:pValue)',{'id':tbId,'environment':envName,'pValue':pValue},'MySQL error adding trust boundary privilege ' + str(pValue) + ' to trust boundary id ' + str(tbId))

  def updateTrustBoundary(self,tb):
    self.updateDatabase('call deleteTrustBoundaryComponents(:id)',{'id':tb.id()},'MySQL error deleting trust boundary components for ' + tb.name())
    self.updateDatabase("call updateTrustBoundary(:id,:name,:type,:desc)",{'id':tb.id(),'name':tb.name(),'type':tb.type(),'desc':tb.description()},'MySQL error adding trust boundary ' + tb.name())
    self.addTags(tb.name(),'trust_boundary',tb.tags())
    defaultPrivilegeLevels = {}
    for environmentName in list(tb.components().keys()):
      defaultPrivilegeLevels[environmentName] = 'None'
      for tbComponentType,tbComponent in tb.components()[environmentName]:
        self.addTrustBoundaryComponent(tb.id(),environmentName,tbComponent)
    tbPrivilegeLevels = tb.privilegeLevels()
    if (len(tbPrivilegeLevels) == 0):
      tbPrivilegeLevels = defaultPrivilegeLevels
    for environmentName in list(tbPrivilegeLevels.keys()):
      self.addTrustBoundaryPrivilege(tb.id(),environmentName,self.privilegeValue(tbPrivilegeLevels[environmentName]))

  def deleteTrustBoundary(self,tbId):
    self.deleteObject(tbId,'trust_boundary')

  def threatenedEntities(self,envName):
    return self.responseList('call threatenedEntities(:envName)',{'envName':envName},'MySQL error getting threatened entities')

  def threatenedProcesses(self,envName):
    return self.responseList('call threatenedProcesses(:envName)',{'envName':envName},'MySQL error getting threatened processes')

  def threatenedDatastores(self,envName):
    return self.responseList('call threatenedDatastores(:envName)',{'envName':envName},'MySQL error getting threatened datastores')

  def threatenedDataflows(self,envName):
    return self.responseList('call threatenedDataflows(:envName)',{'envName':envName},'MySQL error getting threatened dataflows')

  def defaultValue(self,valueType):
    return self.responseList('call defaultValue(:valueType)',{'valueType':valueType},'MySQL error getting default value for ' + valueType)[0]

  def cairisVersion(self):
    return self.responseList('select cairisVersion()',{},'MySQL error getting CAIRIS version')[0]

  def modelValidation(self,envName):
    objtRows = self.responseList('call modelValidation(:envName)',{'envName':envName},'MySQL error validating model')
    objtRows += self.responseList('call taintFlowAnalysis(:envName)',{'envName':envName},'MySQL error validating model')
    rows = []
    for lbl,msg in objtRows:
      rows.append(ValidationResult(lbl,msg))
    return rows

  def processDataMaps(self):
    return self.responseList('call processDataMaps()',{},'MySQL error getting process data maps')[0]
  
  def datastoreDataMaps(self):
    return self.responseList('call datastoreDataMaps()',{},'MySQL error getting datastore data maps')[0]

  def lawfulProcessingTable(self,envName):
    return self.responseList('call lawfulProcessingTable(:envName)',{'envName':envName},'MySQL error getting lawful processing table')

  def reassociateRequirement(self,reqName,domName):
    self.updateDatabase('call reassociateRequirement(:reqName,:domName)',{'reqName':reqName,'domName':domName},'MySQL error associating requirement ' + reqName + ' with domain ' + domName)

  def getDependency(self,envName,dependerName,dependeeName,dependencyName):
    deps = self.responseList('call getDependency(:env,:dep,:dee,:dpy)',{'env':envName,'dep':dependerName,'dee':dependeeName,'dpy':dependencyName},'MySQL error getting dependency')
    if (len(deps) == 0):
      raise ObjectNotFound(envName + ' / ' + dependerName + ' / ' + dependeeName + ' / ' + dependencyName)
    parameters = DependencyParameters(deps[0][1],deps[0][2],deps[0][3],deps[0][4],deps[0][5],deps[0][6])
    return ObjectFactory.build(deps[0][0],parameters)

  def assetAttackSurface(self,assetName,envName):
    return self.responseList('select assetAttackSurface(:asset,:environment)',{'asset':assetName,'environment':envName},'MySQL error getting asset attack surface')[0]

  def setImage(self,imageName,imageContent,mimeType):
    self.updateDatabase('call setImage(:name,:content,:type)',{'name':imageName,'content': b64encode(imageContent),'type':mimeType},'MySQL error setting image')

  def getImage(self,imageName):
    imgResponse = self.responseList('call getImage(:name)',{'name': imageName},'MySQL error getting image')
    if (len(imgResponse) == 0):
      return None
    else:
      return imgResponse[0]

  def getImages(self):
    return self.responseList('call getImages()',{},'MySQL error getting images')

  def checkDataFlowExists(self,dfName,fromType,fromName,toType,toName,envName):
    objtCount = self.responseList('call checkDataFlowExists(:dfName,:fromType,:fromName,:toType,:toName,:env)',{'dfName':dfName,'fromType':fromType,'fromName':fromName,'toType':toType,'toName':toName,'env':envName},'MySQL error checking dataflow in environment')[0]
    if (objtCount > 0): raise ARMException(dfName + ' between ' + fromType + ' ' + fromName + ' and ' + toType + ' ' + toName + ' in environment ' + envName + ' already exists.')

  def riskModelTags(self, envName):
    rows = self.responseList('call riskModelTags(:env)',{'env':envName},'MySQL error getting risk model tags')
    tagDict = {}
    for row in rows:
      tag = row[0]
      objt = row[1]
      dimName = row[2]
      if (tag not in tagDict):
        tagDict[tag] = [(objt,dimName)]
      else:
        tagDict[tag].append((objt,dimName))
    return tagDict

  def securityPatternAssetModel(self,spName):
    rows = self.responseList('call securityPatternClassModel(:sp)',{'sp':spName},'MySQL error getting security pattern asset model')
    associations = {}
    for headName,headType,headMult,headRole,tailRole,tailMult,tailType,tailName in rows:
      associationId = -1
      envName = ''
      headNav = 0
      tailNav = 0
      rationale = ''
      headDim  = 'template_asset'
      tailDim  = 'template_asset'
      parameters = ClassAssociationParameters(envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName,rationale)
      association = ObjectFactory.build(associationId,parameters)
      asLabel = spName + '/' + headName + '/' + tailName
      associations[asLabel] = association
    return associations

  def dimensionRequirements(self,dimName,objtName): return self.responseList('call ' + dimName + 'RequirementNames(:objt)',{'objt':objtName},'MySQL error getting requirements associated with ' + dimName + ' ' + objtName)

  def exceptionRootObstacles(self,ucId): return self.responseList('call hasRootObstacles(:id)',{'id':ucId},'MySQL error getting root obstacles resulting from exceptions for use case ')[0]

  def addSecurityPatterns(self,vts,taps,spps):
    self.deleteSecurityPattern(-1)
    for vt in vts:
      self.addValueType(vt)
    for tap in taps:
      if (self.nameExists(tap.name(),'template_asset')):
        tap.setId(self.getDimensionId(tap.name(),'template_asset'))
        self.updateTemplateAsset(tap)
      else: 
        self.addTemplateAsset(tap)
    for sp in spps:
      self.addSecurityPattern(sp)

  def securityPatternsToXml(self):
    return self.responseList('call patternsToXml()',{},'MySQL error exporting security patterns to XML')[0]

  def checkAssetAssociation(self,envName,headName,tailName):
    if (self.responseList('select isClassAssociationPresent(:env,:head,:tail)',{'env':envName,'head':headName,'tail':tailName},'MySQL error checking asset association')[0]):
      raise DatabaseProxyException('Association between head asset ' + headName + ' and tail asset ' + tailName + ' already exists in environment ' + envName)
    
  def checkTrace(self,fromObjt,fromName,toObjt,toName):
    if (self.responseList('call isTracePresent(:fromObjt,:fromName,:toObjt,:toName)',{'fromObjt':fromObjt,'fromName':fromName,'toObjt':toObjt,'toName':toName},'MySQL error checking trace')[0]):
      raise DatabaseProxyException('Trace from ' + fromObjt + ' ' + fromName + ' to ' + toObjt + ' ' + toName + ' already exists')
    
  def getUserGoals(self,constraintId = -1):
    rows = self.responseList('call getUserGoals(:id)',{'id':constraintId},'MySQL error getting user goals')
    objts = []
    for row in rows:  
      rsId = row[0]
      refName = row[1]
      synName = row[2]
      dimName = row[3]
      personaName = row[4]
      synDim = row[5]
      gsName = row[6]
      sysGoals = self.userGoalSystemGoals(rsId)
      objts.append(ReferenceSynopsis(rsId,refName,synName,dimName,'persona',personaName,synDim,gsName,sysGoals))
    return objts

  def addUserGoal(self,objt):
    ugId = self.newId()
    refName = objt.reference()
    synName = objt.synopsis()
    dimName = objt.dimension()
    personaName = objt.actor()
    gSat = objt.satisfaction()
    self.updateDatabase('call addUserGoal(:ugId,:refName,:synName,:dimName,:personaName,:gSat)',{'ugId':ugId,'refName':refName,'synName':synName,'dimName':dimName,'personaName':personaName,'gSat':gSat},'MySQL error adding user goal')
    for sysGoal in objt.goals():
      self.addUserSystemGoalLink(synName,sysGoal)

  def updateUserGoal(self,objt):
    ugId = objt.id()
    refName = objt.reference()
    synName = objt.synopsis()
    dimName = objt.dimension()
    personaName = objt.actor()
    gSat = objt.satisfaction()
    session = self.updateDatabase('call deleteUserGoalComponents(:id)',{'id':ugId},'MySQL error deleting user goal components',None,False)
    self.updateDatabase('call updateUserGoal(:ugId,:refName,:synName,:dimName,:personaName,:gSat)',{'ugId':ugId,'refName':refName,'synName':synName,'dimName':dimName,'personaName':personaName,'gSat':gSat},'MySQL error updating user goal',session)
    for sysGoal in objt.goals():
      self.addUserSystemGoalLink(synName,sysGoal)

  def deleteUserGoal(self,ugId = -1):
    self.deleteObject(ugId,'user_goal')

  def getGoalContributions(self,envName,personaName = '',filterElement = ''):
    rows = self.responseList('call getGoalContributions(:envName,:persona,:filter)',{'envName':envName,'persona':personaName,'filter':filterElement},'MySQL error getting goal contributions')
    return rows

  def goalSatisfactionScore(self,goalName,envName):
    return self.responseList('call calculateGoalScore(:goalName,:envName)',{'goalName':goalName,'envName':envName},'MySQL error getting goal contribution')[0]

  def getGoalContributionsTable(self,sourceId = -1, targetId = -1):
    rows = self.responseList('call getGoalContributionsTable(:source_id,:target_id)',{'source_id':sourceId,'target_id':targetId},'MySQL error getting goal contribution table')
    objts = []
    for row in rows:
      objts.append(GoalContribution(row[0],row[1],row[2],row[3],row[4],row[5]))
    return objts

  def deleteGoalContribution(self,src,tgt):
    self.updateDatabase('call deleteGoalContribution(:src,:tgt)',{'src':src,'tgt':tgt},'MySQL error deleting goal contribution')

  def taskContributions(self,taskName,envName):
    rows = self.responseList('call getTaskContributions(:taskName,:envName)',{'taskName':taskName,'envName':envName},'MySQL error getting task contributions')
    objts = []
    for row in rows:
      objts.append(TaskContribution(taskName,row[0],envName,row[1]))
    return objts

  def conflictingPersonaCharacteristics(self,pName,ugName):
    objts = self.responseList('call conflictingPersonaCharacteristics(:pName,:ugName)',{'pName':pName,'ugName':ugName},'MySQL error getting persona characteristic user goals')
    if (len(objts) == 1 and objts[0] == ''):
      objts = []
    return objts

  def addUserSystemGoalLink(self,ugName,sgName):
    self.updateDatabase('call addUserSystemGoalLink(:ugName,:sgName)',{'ugName':ugName,'sgName':sgName},'MySQL error adding user/system goal link')

  def userGoalSystemGoals(self,ugId):
    return self.responseList('call userGoalSystemGoals(:ugId)',{'ugId':ugId},'MySQL error getting user goal system goals')

  def controlStructure(self,envName,filterElement = ''):
    return self.responseList('call controlStructure(:env,:fe)',{'env':envName,'fe':filterElement},'MySQL error getting control structure')

  def validateForExport(self):
    return self.responseList('call invalidObjectNames()',{},'MySQL error getting invalid object names')[0]

  def addUserStory(self,parameters):
    parameters.validate()
    usName = parameters.name()
    usAuth = parameters.author()
    roleName = parameters.role()
    usDesc = parameters.description()
    ugName = parameters.userGoal()
    tags = parameters.tags()
    usId = self.newId()
    self.updateDatabase('call addUserStory(:id,:name,:auth,:role,:desc,:ug)',{'id':usId,'name':usName,'auth':usAuth,'role':roleName,'desc':usDesc,'ug':ugName},'MySQL error adding user story')
    self.addTags(usName,'userstory',tags)

    for ac in parameters.acceptanceCriteria():
      self.addUserStoryAcceptanceCriteria(usId,ac)
    return usId

  def addUserStoryAcceptanceCriteria(self,usId,usAc):
    self.updateDatabase('call addUserStoryAcceptanceCriteria(:usId,:usAc)',{'usId':usId,'usAc':usAc,},'MySQL error adding acceptance criteria to user story')

  
  def updateUserStory(self,parameters):
    parameters.validate()
    usId = parameters.id()
    usName = parameters.name()
    usAuth = parameters.author()
    roleName = parameters.role()
    usDesc = parameters.description()
    ugName = parameters.userGoal()
    tags = parameters.tags()
    session = self.updateDatabase('call deleteUserStoryComponents(:us)',{'us':usId},'MySQL error deleting user story components',None,False)
    self.updateDatabase('call updateUserStory(:id,:name,:auth,:role,:desc,:ug)',{'id':usId,'name':usName,'auth':usAuth,'role':roleName,'desc':usDesc,'ug':ugName},'MySQL error adding user story',session)
    self.addTags(usName,'userstory',tags)

    for ac in parameters.acceptanceCriteria():
      self.addUserStoryAcceptanceCriteria(usId,ac)

  def deleteUserStory(self,usId):
    self.deleteObject(usId,'userstory')
  
  def getUserStories(self,constraintId = -1):
    usRows = self.responseList('call getUserStories(:id)',{'id':constraintId},'MySQL error getting user stories')
    uss = []
    for usId,usName,usAuth,roleName,usDesc,ugName in usRows:
      tags = self.getTags(usName,'userstory')
      ac = self.userStoryAcceptanceCriteria(usName)
      uss.append(UserStory(usId,usName,usAuth,roleName,usDesc,ugName,ac,tags))
    return uss

  def userStoryAcceptanceCriteria(self,usName):
    return self.responseList('call userStoryAcceptanceCriteria(:usName)',{'usName':usName},'MySQL error getting user story acceptance criteria')

  def storiesToXml(self,includeHeader=True):
    return self.responseList('call storiesToXml(:head)',{'head' : includeHeader},'MySQL error exporting stories to XML')[0]

  def roleUserGoals(self,roleName):
    return self.responseList('call roleUserGoals(:name)',{'name':roleName},'MySQL error getting user goals for role ' + roleName)

  def goalPolicy(self,goalId,environmentId):
    pData = self.responseList('call goalPolicy(:gId,:eId)',{'gId':goalId, 'eId':environmentId},'MySQL error getting goal policy')
    if (len(pData) == 1):
      ps = pData[0]
      return {'theGoalName':ps[0],'theEnvironmentName':ps[1],'theSubject':ps[2],'theAccessType':ps[3],'theResource':ps[4],'thePermission':ps[5]}
    else:
      return None

  def addGoalPolicy(self,goalId,environmentName,subjName,acName,resName,pName):
    self.updateDatabase('call addGoalPolicy(:gId,:eName,:subj,:acc,:res,:perm)',{'gId':goalId,'eName':environmentName,'subj':subjName,'acc':acName,'res':resName,'perm':pName},'MySQL error adding goal policy')

  def addPolicyStatement(self,parameters):
    psId = self.newId()
    goalName = parameters.goal()
    envName = parameters.environment()
    subjName = parameters.subject() 
    atName = parameters.accessType() 
    resName = parameters.resource() 
    pName = parameters.permission() 
    self.updateDatabase('call addPolicyStatement(:id,:goal,:env,:subj,:at,:res,:perm)',{'id':psId,'goal':goalName,'env':envName,'subj':subjName,'at':atName,'res':resName,'perm':pName},'MySQL error adding policy statement')
    return psId

  def updatePolicyStatement(self,parameters):
    psId = parameters.id()
    goalName = parameters.goal()
    envName = parameters.environment()
    subjName = parameters.subject() 
    atName = parameters.accessType() 
    resName = parameters.resource() 
    pName = parameters.permission() 
    self.updateDatabase('call updatePolicyStatement(:id,:goal,:env,:subj,:at,:res,:perm)',{'id':psId,'goal':goalName,'env':envName,'subj':subjName,'at':atName,'res':resName,'perm':pName},'MySQL error updating policy statement')
    

  def deletePolicyStatement(self,psId = -1):
    self.deleteObject(psId,'policy_statement')

  def getPolicyStatements(self,constraintId = -1):
    psRows = self.responseList('call getPolicyStatements(:id)',{'id':constraintId},'MySQL error getting policy statements')
    objts = []
    for psId,goalName,envName,subjName,atName,resName,pName in psRows:
      objts.append(PolicyStatement(psId,goalName,envName,subjName,atName,resName,pName))
    return objts

  def userGoalFilters(self,envName,personaName):
    return self.responseList('call ugm_filterNames(:environment,:persona)',{'environment':envName,'persona':personaName},'MySQL error getting user goal filters for persona ' + personaName + ' in environment ' + envName)
