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
import MySQLdb
import RequirementFactory
from Environment import Environment
from ARM import *
import _mysql_exceptions 
import Attacker
import Asset
import Threat
import Vulnerability
import Persona
import MisuseCase
import Task
import Risk
import Response
import ClassAssociation
import DatabaseProxy
from AttackerParameters import AttackerParameters
from PersonaParameters import PersonaParameters
from GoalParameters import GoalParameters
from ObstacleParameters import ObstacleParameters
from AssetParameters import AssetParameters
from TemplateAssetParameters import TemplateAssetParameters
from TemplateGoalParameters import TemplateGoalParameters
from TemplateRequirementParameters import TemplateRequirementParameters
from SecurityPatternParameters import SecurityPatternParameters
from ThreatParameters import ThreatParameters
from VulnerabilityParameters import VulnerabilityParameters
from RiskParameters import RiskParameters
from ResponseParameters import ResponseParameters
from RoleParameters import RoleParameters
from ResponsibilityParameters import ResponsibilityParameters
import ObjectFactory
from TaskParameters import TaskParameters
from MisuseCaseParameters import MisuseCaseParameters
from DomainPropertyParameters import DomainPropertyParameters
import Trace
from cairis.core.armid import *
from DotTraceParameters import DotTraceParameters
from EnvironmentParameters import EnvironmentParameters
from Target import Target
from AttackerEnvironmentProperties import AttackerEnvironmentProperties
from AssetEnvironmentProperties import AssetEnvironmentProperties
from ThreatEnvironmentProperties import ThreatEnvironmentProperties
from VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from AcceptEnvironmentProperties import AcceptEnvironmentProperties
from TransferEnvironmentProperties import TransferEnvironmentProperties
from MitigateEnvironmentProperties import MitigateEnvironmentProperties
from CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties
from CountermeasureParameters import CountermeasureParameters
from PersonaEnvironmentProperties import PersonaEnvironmentProperties
from TaskEnvironmentProperties import TaskEnvironmentProperties
from MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from RoleEnvironmentProperties import RoleEnvironmentProperties
from ClassAssociationParameters import ClassAssociationParameters
from GoalAssociationParameters import GoalAssociationParameters
from DependencyParameters import DependencyParameters
from GoalEnvironmentProperties import GoalEnvironmentProperties
from ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from ValueTypeParameters import ValueTypeParameters
from ExternalDocumentParameters import ExternalDocumentParameters
from InternalDocumentParameters import InternalDocumentParameters
from CodeParameters import CodeParameters
from MemoParameters import MemoParameters
from DocumentReferenceParameters import DocumentReferenceParameters
from ConceptReferenceParameters import ConceptReferenceParameters
from PersonaCharacteristicParameters import PersonaCharacteristicParameters
from TaskCharacteristicParameters import TaskCharacteristicParameters
from UseCaseParameters import UseCaseParameters
from UseCase import UseCase
from UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from UseCaseParameters import UseCaseParameters
from Step import Step
from Steps import Steps
from ReferenceSynopsis import ReferenceSynopsis
from ReferenceContribution import ReferenceContribution
from ConceptMapAssociationParameters import ConceptMapAssociationParameters
from ComponentViewParameters import ComponentViewParameters;
from ComponentParameters import ComponentParameters;
from ConnectorParameters import ConnectorParameters;
from WeaknessTarget import WeaknessTarget
from ImpliedProcess import ImpliedProcess
from ImpliedProcessParameters import ImpliedProcessParameters
from Location import Location
from Locations import Locations
from LocationsParameters import LocationsParameters
from DataFlow import DataFlow
from DataFlowParameters import DataFlowParameters
from TrustBoundary import TrustBoundary
import string
import os
from numpy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

__author__ = 'Shamal Faily, Robin Quetin, Nathan Jenkins'

class MySQLDatabaseProxy(DatabaseProxy.DatabaseProxy):
  def __init__(self, host=None, port=None, user=None, passwd=None, db=None):
    DatabaseProxy.DatabaseProxy.__init__(self)
    self.theGrid = 0
    b = Borg()
    if (host is None or port is None or user is None or passwd is None or db is None):
      host = b.dbHost
      port = b.dbPort
      user = b.dbUser
      passwd = b.dbPasswd
      db = b.dbName

    try:
      dbEngine = create_engine('mysql+mysqldb://'+user+':'+passwd+'@'+host+':'+str(port)+'/'+db)
      self.conn = scoped_session(sessionmaker(bind=dbEngine))
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error connecting to the CAIRIS database ' + b.dbName + ' on host ' + b.dbHost + ' at port ' + str(b.dbPort) + ' with user ' + b.dbUser + ' (id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 
    self.theDimIdLookup, self.theDimNameLookup = self.buildDimensionLookup()

  def reconnect(self,closeConn = True,session_id = None):
    b = Borg()
    try:
      if (closeConn) and self.conn.connection().connection.open:
        self.conn.close()
      if b.runmode == 'desktop':
        dbEngine = create_engine('mysql+mysqldb://'+b.dbUser+':'+b.dbPasswd+'@'+b.dbHost+':'+str(b.dbPort)+'/'+b.dbName)
        self.conn = scoped_session(sessionmaker(bind=dbEngine))
      elif b.runmode == 'web':
        ses_settings = b.get_settings(session_id)
        dbEngine = create_engine('mysql+mysqldb://'+ses_settings['dbUser']+':'+ses_settings['dbPasswd']+'@'+ses_settings['dbHost']+':'+str(ses_settings['dbPort'])+'/'+ses_settings['dbName'])
        self.conn = scoped_session(sessionmaker(bind=dbEngine))
      else:
        raise RuntimeError('Run mode not recognized')
    except _mysql_exceptions.DatabaseError, e:
      exceptionText = 'MySQL error re-connecting to the CAIRIS database ' + b.dbName + ' on host ' + b.dbHost + ' at port ' + str(b.dbPort) + ' with user ' + b.dbUser + ' (id:' + str(id) + ',message:' + format(e)
      raise DatabaseProxyException(exceptionText) 
    self.theDimIdLookup, self.theDimNameLookup = self.buildDimensionLookup()


  def associateGrid(self,gridObjt): self.theGrid = gridObjt

    
  def buildDimensionLookup(self):
    dimRows = self.responseList('call traceDimensions()',{},'MySQL error building trace dimension lookup tables')
    idLookup  = {}
    nameLookup = {}
    for dimId,dimName in dimRows:
      idLookup[dimId] = dimName
      nameLookup[dimName] = dimId
    return (idLookup, nameLookup)
    
  def close(self):
    self.conn.remove()

  def getRequirements(self,constraintId = '',isAsset = 1):
    reqRows = self.responseList('call getRequirements(:id,:isAs)',{'id':constraintId,'isAs':isAsset},'MySQL error getting requirements')
    reqDict = {}
    for reqLabel, reqId, reqName, reqDesc, priority, rationale, fitCriterion, originator, reqVersion, reqType, reqDomain in reqRows:
      r = RequirementFactory.build(reqId,reqLabel,reqName,reqDesc,priority,rationale,fitCriterion,originator,reqType,reqDomain,reqVersion)
      reqDict[reqDesc] = r
    return reqDict

  def getRequirement(self,reqId):
    reqRows = self.responseList('call getRequirement(:id)',{'id':reqId},'MySQL error getting requirement')
    reqDict = {}
    for reqLabel, reqId, reqName, reqDesc, priority, rationale, fitCriterion, originator, reqVersion, reqType, reqDomain in reqRows:
      r = RequirementFactory.build(reqId,reqLabel,reqName,reqDesc,priority,rationale,fitCriterion,originator,reqType,reqDomain,reqVersion)
      reqDict[reqDesc] = r
    return reqDict

  def getOrderedRequirements(self,constraintId = '',isAsset = True):
    reqRows = self.responseList('call getRequirements(:id,:isAs)',{'id':constraintId,'isAs':isAsset},'MySQL error getting requirements')
    reqList = []
    for reqLabel, reqId, reqName, reqDesc, priority, rationale, fitCriterion, originator, reqVersion, reqType, reqDomain in reqRows:
      r = RequirementFactory.build(reqId,reqLabel,reqName,reqDesc,priority,rationale,fitCriterion,originator,reqType,reqDomain,reqVersion)
      reqList.append(r)
    return reqList

    
  def newId(self):
    return self.responseList('call newId()',{},'MySQL error getting new identifier')[0]

  def updateDatabase(self,callTxt,argDict,errorTxt):
    try:
      session = self.conn()
      session.execute(callTxt,argDict)
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = errorTxt + ' (id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 

  def addRequirement(self,r,assetName,isAsset = True):
    self.updateDatabase('call addRequirement(:lbl,:id,:vers,:name,:desc,:rationale,:origin,:fCrit,:priority,:type,:asName,:isAs)',{'lbl':r.label(),'id':r.id(),'vers':r.version(),'name':r.name(),'desc':r.description(),'rationale':r.rationale(),'origin':r.originator(),'fCrit':r.fitCriterion(),'priority':r.priority(),'type':r.type(),'asName':assetName,'isAs':isAsset},'MySQL error adding new requirement ' + str(r.id()))

  def updateRequirement(self,r):
    self.updateDatabase('call updateRequirement(:lbl,:id,:vers,:name,:desc,:rationale,:origin,:fCrit,:priority,:type)',{'lbl':r.label(),'id':r.id(),'vers':r.version(),'name':r.name(),'desc':r.description(),'rationale':r.rationale(),'origin':r.originator(),'fCrit':r.fitCriterion(),'priority':r.priority(),'type':r.type()},'MySQL error updating requirement ' + str(r.id()))

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
    environmentId = self.newId()
    environmentName = parameters.name()
    environmentShortCode = parameters.shortCode()
    environmentDescription = parameters.description()
    try:
      session = self.conn()
      sql = 'call addEnvironment(%s,"%s","%s","%s")'%(environmentId,environmentName,environmentShortCode,environmentDescription)
      session.execute(sql)
      if (len(parameters.environments()) > 0):
        for c in parameters.environments():
          session.execute('call addCompositeEnvironment(:id,:c)',{'id':environmentId,'c':c})
        session.commit()
        session.close()        
        self.addCompositeEnvironmentProperties(environmentId,parameters.duplicateProperty(),parameters.overridingEnvironment())
      session.commit()
      session.close()        

      assetValues = parameters.assetValues()
      if (assetValues != None):
        for v in assetValues:
          self.updateValueType(v)

      self.addValueTensions(environmentId,parameters.tensions())
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addCompositeEnvironmentProperties(self,environmentId,duplicateProperty,overridingEnvironment):
    self.updateDatabase('call addCompositeEnvironmentProperties(:id,:dp,:oe)',{'id':environmentId,'dp':duplicateProperty,'oe':overridingEnvironment},'MySQL error adding duplicate properties for environment id ' + str(environmentId))

  def riskEnvironments(self,threatName,vulName):
    return self.responseList('call riskEnvironments(:threat,:vul)',{'threat':threatName,'vul':vulName},'MySQL error getting environments associated with threat ' + threatName + ' and vulnerability ' + vulName)

  def riskEnvironmentsByRisk(self,riskName):
    return self.responseList('call riskEnvironmentsByRisk(:risk)',{'risk':riskName},'MySQL error getting environments associated with risk ' + riskName)

  def updateEnvironment(self,parameters):
    environmentId = parameters.id()
    environmentName = parameters.name()
    environmentShortCode = parameters.shortCode()
    environmentDescription = parameters.description()

    try:
      session = self.conn()
      session.execute('call deleteEnvironmentComponents(:id)',{'id':parameters.id()})
      session.execute('call updateEnvironment(:id,:name,:shortCode,:desc)',{'id':environmentId,'name':environmentName,'shortCode':environmentShortCode,'desc':environmentDescription})
      if (len(parameters.environments()) > 0):
        for c in parameters.environments():
          session.execute('call addCompositeEnvironment(:id,:c)',{'id':environmentId,'c':c})
      session.commit()
      session.close()
      if (len(parameters.duplicateProperty()) > 0):
        self.addCompositeEnvironmentProperties(environmentId,parameters.duplicateProperty(),parameters.overridingEnvironment())
      self.addValueTensions(environmentId,parameters.tensions())
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteRequirement(self,r):
    self.deleteObject(r,'requirement')
    
  def responseList(self,callTxt,argDict,errorTxt):
    try:
      session = self.conn()
      rs = session.execute(callTxt,argDict)
      responseList = []
      if (rs.rowcount > 0):
        for row in rs.fetchall():
          if (len(row) > 1):
            responseList.append(tuple(list(row)))
          else:
            responseList.append(list(row)[0])
      rs.close()
      session.close()
      return responseList
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = errorTxt + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    attackerRows = self.responseList('call getAttackers(:id)',{'id':constraintId},'MySQL error getting attackers' + str(constraintId))
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

  def addDimensionEnvironment(self,dimId,table,environmentName):
    self.updateDatabase('call add_' + table + '_environment(:id,:name)',{'id':dimId,'name':environmentName},'MySQL error associating ' + table + ' id ' + str(dimId) + ' with environment ' + environmentName)

  def addAttackerMotives(self,attackerId,environmentName,motives):
    for motive in motives:
      self.updateDatabase('call addAttackerMotive(:aId,:envName,:motive)',{'aId':attackerId,'envName':environmentName,'motive':motive},'MySQL error updating motivates for attacker id ' + str(attackerId))

  def addAttackerCapabilities(self,attackerId,environmentName,capabilities):
    for name,value in capabilities:
      self.updateDatabase('call addAttackerCapability(:aId,:envName,:name,:value)',{'aId':attackerId,'envName':environmentName,'name':name,'value':value},'MySQL error updating attacker capabilities for attacker id ' + str(attackerId))
  
  def updateAttacker(self,parameters):
    try:
      session = self.conn()
      session.execute('call deleteAttackerComponents(:id)',{'id':parameters.id()})
      attackerId = parameters.id()
      attackerName = parameters.name()
      attackerDesc = parameters.description()
      attackerImage = parameters.image()
      tags = parameters.tags()

      session = self.conn()
      session.execute("call updateAttacker(:id,:name,:desc,:image)",{'id':attackerId,'name':attackerName,'desc':attackerDesc,'image':attackerImage})
      session.commit()
      session.close()
      self.addTags(attackerName,'attacker',tags)
      for environmentProperties in parameters.environmentProperties():
        environmentName = environmentProperties.name()
        self.addDimensionEnvironment(attackerId,'attacker',environmentName)
        self.addAttackerMotives(attackerId,environmentName,environmentProperties.motives())
        self.addAttackerCapabilities(attackerId,environmentName,environmentProperties.capabilities())
        self.addDimensionRoles(attackerId,'attacker',environmentName,environmentProperties.roles())
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating attacker id ' + str(parameters.id()) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteAttacker(self,attackerId):
    self.deleteObject(attackerId,'attacker')
    
  def deleteObject(self,objtId,tableName):
    try: 
      session = self.conn()
      sqlTxt = 'call delete_' + tableName + '(:obj)'
      session.execute(sqlTxt,{'obj':objtId})
      session.commit()
      session.close()
    except _mysql_exceptions.IntegrityError, e:
      id,msg = e
      exceptionText = 'Cannot remove ' + tableName + ' due to dependent data (id:' + str(id) + ',message:' + msg + ').'
      raise IntegrityException(exceptionText) 
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error deleting ' + tableName + 's (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addAsset(self,parameters):
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
    try:
      session = self.conn()
      sql ='call addAsset(%s,"%s","%s","%s","%s","%s","%s","%s")'%(assetId,assetName,shortCode,assetDesc.encode('utf-8'),assetSig.encode('utf-8'),assetType,assetCriticality,assetCriticalRationale)
      session.execute(sql)
      session.commit()
      session.close()
      self.addTags(assetName,'asset',tags)
      self.addInterfaces(assetName,'asset',ifs)
      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(assetId,'asset',environmentName)
        self.addAssetAssociations(assetId,assetName,environmentName,cProperties.associations())
        self.addSecurityProperties('asset',assetId,environmentName,cProperties.properties(),cProperties.rationale())
      return assetId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding asset ' + assetName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateAsset(self,parameters):
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
    try:
      session = self.conn()
      session.execute('call deleteAssetComponents(:id)',{'id':assetId})
      session.execute('call updateAsset(:id,:name,:shortCode,:desc,:sig,:type,:crit,:rationale)',{'id':assetId,'name':assetName,'shortCode':shortCode,'desc':assetDesc,'sig':assetSig,'type':assetType,'crit':assetCriticality,'rationale':assetCriticalRationale})
      session.commit()
      session.close()
      self.addTags(assetName,'asset',tags)
      self.addInterfaces(assetName,'asset',ifs)
      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(assetId,'asset',environmentName)
        self.addAssetAssociations(assetId,assetName,environmentName,cProperties.associations())
        self.addSecurityProperties('asset',assetId,environmentName,cProperties.properties(),cProperties.rationale())
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating asset ' + assetName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addTemplateAssetProperties(self,taId,cProp,iProp,avProp,acProp,anProp,panProp,unlProp,unoProp,cRat,iRat,avRat,acRat,anRat,panRat,unlRat,unoRat):
    callTxt = 'call add_template_asset_properties(:ta,:cPr,:iPr,:avPr,:acPr,:anPr,:panPr,:unlPr,:unoPr,:cRa,:iRa,:avRa,:acRa,:anRa,:panRa,:unlRa,:unoRa)'
    self.updateDatabase(callTxt, {'ta':taId,'cPr':cProp,'iPr':iProp,'avPr':avProp,'acPr':acProp,'anPr':anProp,'panPr':panProp,'unlPr':unlProp,'unoPr':unoProp,'cRa':cRat,'iRa':iRat,'avRa':avRat,'acRa':acRat,'anRa':anRat,'panRa':panRat,'unlRa':unlRat,'unoRa':unoRat},'MySQL error adding security properties to template asset')

  def updateTemplateAssetProperties(self,taId,cProp,iProp,avProp,acProp,anProp,panProp,unlProp,unoProp,cRat,iRat,avRat,acRat,anRat,panRat,unlRat,unoRat):
    sqlTxt = 'update template_asset_property set property_value_id=%s, property_rationale="%s" where template_asset_id = %s and property_id = %s' 
    try:
      session = self.conn()
      stmt = sqlTxt %(cProp,cRat,taId,C_PROPERTY)
      session.execute(stmt)
      stmt = sqlTxt %(iProp,iRat,taId,I_PROPERTY) 
      session.execute(stmt)
      stmt = sqlTxt %(avProp,avRat,taId,AV_PROPERTY) 
      session.execute(stmt)
      stmt = sqlTxt %(acProp,acRat,taId,AC_PROPERTY) 
      session.execute(stmt)
      stmt = sqlTxt %(anProp,anRat,taId,AN_PROPERTY) 
      session.execute(stmt)
      stmt = sqlTxt %(panProp,panRat,taId,PAN_PROPERTY) 
      session.execute(stmt)
      stmt = sqlTxt %(unlProp,unlRat,taId,UNL_PROPERTY) 
      session.execute(stmt)      
      stmt = sqlTxt %(unoProp,unoRat,taId,UNO_PROPERTY) 
      session.execute(stmt)
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating security properties for template asset id ' + str(taId) +  ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addSecurityProperties(self,dimTable,objtId,environmentName,securityProperties,pRationale):
    sqlTxt = 'call add_' + dimTable + '_properties(:obj,:env,:cPr,:iPr,:avPr,:acPr,:anPr,:panPr,:unlPr,:unoPr,:cRa,:iRa,:avRa,:acRa,:anRa,:panRa,:unlRa,:unoRa)'
    try:
      session = self.conn()
      session.execute(sqlTxt,{'obj':objtId,'env':environmentName,'cPr':securityProperties[C_PROPERTY],'iPr':securityProperties[I_PROPERTY],'avPr':securityProperties[AV_PROPERTY],'acPr':securityProperties[AC_PROPERTY],'anPr':securityProperties[AN_PROPERTY],'panPr':securityProperties[PAN_PROPERTY],'unlPr':securityProperties[UNL_PROPERTY],'unoPr':securityProperties[UNO_PROPERTY],'cRa':pRationale[C_PROPERTY],'iRa':pRationale[I_PROPERTY],'avRa':pRationale[AV_PROPERTY],'acRa':pRationale[AC_PROPERTY],'anRa':pRationale[AN_PROPERTY],'panRa':pRationale[PAN_PROPERTY],'unlRa':pRationale[UNL_PROPERTY],'unoRa':pRationale[UNO_PROPERTY]})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding security properties for ' + dimTable + ' id ' + str(objtId) + ' in environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteAsset(self,assetId):
    self.deleteObject(assetId,'asset')
    

  def dimensionObject(self,constraintName,dimensionTable):
    if (dimensionTable != 'requirement'):
      constraintId = self.getDimensionId(constraintName,dimensionTable)
    objts = {}
    if (dimensionTable == 'provided_interface' or dimensionTable == 'required_interface'):
      objts = self.getInterfaces(constraintId)
    if (dimensionTable == 'goalassociation'):
      objts = self.getGoalAssociations(constraintId)
    if (dimensionTable == 'asset'):
      objts = self.getAssets(constraintId)
    if (dimensionTable == 'template_asset'):
      objts = self.getTemplateAssets(constraintId)
    if (dimensionTable == 'template_requirement'):
      objts = self.getTemplateRequirements(constraintId)
    if (dimensionTable == 'template_goal'):
      objts = self.getTemplateGoals(constraintId)
    if (dimensionTable == 'securitypattern'):
      objts = self.getSecurityPatterns(constraintId)
    if (dimensionTable == 'component_view'):
      objts = self.getComponentViews(constraintId)
    if (dimensionTable == 'component'):
      objts = self.getComponents(constraintId)
    if (dimensionTable == 'classassociation'):
      objts = self.getClassAssociations(constraintId)
    if (dimensionTable == 'goal'):
      objts = self.getGoals(constraintId)
    if (dimensionTable == 'obstacle'):
      objts = self.getObstacles(constraintId)
    elif (dimensionTable == 'attacker'):
      objts = self.getAttackers(constraintId)
    elif (dimensionTable == 'threat'):
      objts = self.getThreats(constraintId)
    elif (dimensionTable == 'vulnerability'):
      objts = self.getVulnerabilities(constraintId)
    elif (dimensionTable == 'risk'):
      objts = self.getRisks(constraintId)
    elif (dimensionTable == 'response'):
      objts = self.getResponses(constraintId)
    elif (dimensionTable == 'countermeasure'):
      objts = self.getCountermeasures(constraintId)
    elif (dimensionTable == 'persona'):
      objts = self.getPersonas(constraintId)
    elif (dimensionTable == 'task'):
      objts = self.getTasks(constraintId)
    elif (dimensionTable == 'usecase'):
      objts = self.getUseCases(constraintId)
    elif (dimensionTable == 'misusecase'):
      objts = self.getMisuseCases(constraintId)
    elif (dimensionTable == 'requirement'):
      objts = self.getRequirement(constraintName)
    elif (dimensionTable == 'environment'):
      objts = self.getEnvironments(constraintId)
    elif (dimensionTable == 'role'):
      objts = self.getRoles(constraintId)
    elif (dimensionTable == 'domainproperty'):
      objts = self.getDomainProperties(constraintId)
    elif (dimensionTable == 'document_reference'):
      objts = self.getDocumentReferences(constraintId)
    elif (dimensionTable == 'concept_reference'):
      objts = self.getConceptReferences(constraintId)
    elif (dimensionTable == 'persona_characteristic'):
      objts = self.getPersonaCharacteristics(constraintId)
    elif (dimensionTable == 'task_characteristic'):
      objts = self.getTaskCharacteristics(constraintId)
    elif (dimensionTable == 'external_document'):
      objts = self.getExternalDocuments(constraintId)
    elif (dimensionTable == 'internal_document'):
      objts = self.getInternalDocuments(constraintId)
    elif (dimensionTable == 'code'):
      objts = self.getCodes(constraintId)
    elif (dimensionTable == 'memo'):
      objts = self.getMemos(constraintId)
    elif (dimensionTable == 'reference_synopsis'):
      objts = self.getReferenceSynopsis(constraintId)
    elif (dimensionTable == 'reference_contribution'):
      objts = self.getReferenceContributions(constraintId)
    elif (dimensionTable == 'persona_implied_process'):
      objts = self.getImpliedProcesses(constraintId)
    elif (dimensionTable == 'trust_boundary'):
      objts = self.getTrustBoundaries(constraintId)

    return (objts.values())[0]


  def getAssets(self,constraintId = -1):
    assetRows = self.responseList('call getAssets(:id)',{'id':constraintId},'MySQL error getting assets')
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


  def getThreats(self,constraintId = -1):
    threats = {}
    threatRows = self.responseList('call getThreats(:id)',{'id':constraintId},'MySQL error getting threats')
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
    try:
      session = self.conn()
      sqlText = ''
      if ((dimensionTable == 'classassociation') or (dimensionTable == 'goalassociation')):
        associationComponents = dimensionName.split('/')
        if (dimensionTable == 'goalassociation'):
          rs = session.execute('select goalAssociationId(:ac0,:ac1,:ac2,:ac3,ac:4)',{'ac0':associationComponents[0],'ac1':associationComponents[1],'ac2':associationComponents[2],'ac3':associationComponents[3],'ac4':associationComponents[4]})
        elif (dimensionTable == 'classassociation'):
          rs = session.execute('select classAssociationId(:ac0,:ac1,:ac2)',{'ac0':associationComponents[0],'ac1':associationComponents[1],'ac2':associationComponents[2]})
      elif ((dimensionTable == 'provided_interface') or (dimensionTable == 'required_interface')):
        cName,ifName = dimensionName.split('_')
        rs = session.execute('select interfaceId(:name)',{'name':ifName})
      else:
        dimensionName = self.conn.connection().connection.escape_string(dimensionName)
        rs = session.execute('call dimensionId(:name,:table)',{'name':dimensionName,'table':dimensionTable})

      if (rs.rowcount == 0):
        exceptionText = 'No identifier associated with '
        exceptionText += dimensionTable + ' object ' + dimensionName
        raise DatabaseProxyException(exceptionText)

      row = rs.fetchone() 
      dimId = row[0]
      if (dimId == None and dimensionTable == 'requirement'):
        rs = session.execute('select requirementNameId(:name)',{'name':dimensionName})
        row = rs.fetchone()
        dimId = row[0]
      rs.close()
      session.close()
      return dimId
    except _mysql_exceptions.DatabaseError, e:
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
    if (dimensionTable != 'template_asset' and dimensionTable != 'template_requirement' and dimensionTable != 'template_goal' and dimensionTable != 'locations' and dimensionTable != 'persona_characteristic_synopsis'):
      callTxt = 'call ' + dimensionTable + 'Names(:env)' 
      argDict = {'env':currentEnvironment}
      return self.responseList(callTxt,argDict,'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'template_asset'):
      return self.responseList('call template_assetNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'template_requirement'):
      return self.responseList('call template_requirementNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'template_goal'):
      return self.responseList('call template_goalNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'locations'):
      return self.responseList('call locationsNames()',{},'MySQL error getting ' + dimensionTable + 's')
    elif (dimensionTable == 'persona_characteristic_synopsis'):
      return self.responseList('call persona_characteristic_synopsisNames()',{},'MySQL error getting ' + dimensionTable + 's')

  def getEnvironmentNames(self):
    return self.responseList('call nonCompositeEnvironmentNames()',{},'MySQL error getting environments')

  def addThreat(self,parameters,update = False):
    threatId = self.newId()
    threatName = parameters.name()
    threatType = parameters.type()
    threatMethod = parameters.method()
    tags = parameters.tags()
    try:
      session = self.conn()
      session.execute("call addThreat(:id,:name,:type,:method)",{'id':threatId,'name':threatName,'type':threatType,'method':threatMethod.encode('utf-8')})
      session.commit()
      self.addTags(threatName,'threat',tags)
      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(threatId,'threat',environmentName)
        session.execute("call addThreatLikelihood(:tId,:env,:likely)",{'tId':threatId,'env':environmentName,'likely':cProperties.likelihood()})
        self.addSecurityProperties('threat',threatId,environmentName,cProperties.properties(),cProperties.rationale())

        for assetName in cProperties.assets():
          session.execute("call addAssetThreat(:tId,:env,:assName)",{'tId':threatId,'env':environmentName,'assName':assetName})
        for attacker in cProperties.attackers():
          session.execute("call addThreatAttacker(:tId,:env,:attacker)",{'tId':threatId,'env':environmentName,'attacker':attacker})
      session.commit()
      session.close()
      return threatId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding threat ' + threatName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def updateThreat(self,parameters):
    threatId = parameters.id()
    threatName = parameters.name()
    threatType = parameters.type()
    threatMethod = parameters.method()
    tags = parameters.tags()

    try:
      session = self.conn()
      session.execute('call deleteThreatComponents(:id)',{'id':threatId})
      session.execute('call updateThreat(:id,:name,:type,:method)',{'id':threatId,'name':threatName,'type':threatType,'method':threatMethod.encode('utf-8')})
      session.commit()
      self.addTags(threatName,'threat',tags)

      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(threatId,'threat',environmentName)
        session.execute("call addThreatLikelihood(:tId,:env,:likely)",{'tId':threatId,'env':environmentName,'likely':cProperties.likelihood()})
        self.addSecurityProperties('threat',threatId,environmentName,cProperties.properties(),cProperties.rationale())

        for assetName in cProperties.assets():
          session.execute("call addAssetThreat(:tId,:env,:assName)",{'tId':threatId,'env':environmentName,'assName':assetName})
        for attacker in cProperties.attackers():
          session.execute("call addThreatAttacker(:tId,:env,:attacker)",{'tId':threatId,'env':environmentName,'attacker':attacker})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating threat ' + threatName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getVulnerabilities(self,constraintId = -1):
    vulRows = self.responseList('call getVulnerabilities(:id)',{'id':constraintId},'MySQL error getting vulnerabilities')
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
    vulName = parameters.name()
    vulDesc = parameters.description()
    vulType = parameters.type()
    tags = parameters.tags()
    try:
      vulId = self.newId()
      session = self.conn()
      session.execute('call addVulnerability(:id,:name,:desc,:type)',{'id':vulId,'name':vulName,'desc':vulDesc.encode('utf-8'),'type':vulType})
      session.commit()
      self.addTags(vulName,'vulnerability',tags)
      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(vulId,'vulnerability',environmentName)
        session.execute("call addVulnerabilitySeverity(:vId,:env,:severity)",{'vId':vulId,'env':environmentName,'severity':cProperties.severity()})
        for assetName in cProperties.assets():
          session.execute("call addAssetVulnerability(:vId,:env,:assName)",{'vId':vulId,'env':environmentName,'assName':assetName})
      session.commit()
      session.close()
      return vulId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding vulnerability ' + vulName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateVulnerability(self,parameters):
    vulId = parameters.id()
    vulName = parameters.name()
    vulDesc = parameters.description()
    vulType = parameters.type()
    tags = parameters.tags()

    try:
      session = self.conn()
      session.execute('call deleteVulnerabilityComponents(:id)',{'id':vulId})
      session.execute('call updateVulnerability(:id,:name,:desc,:type)',{'id':vulId,'name':vulName,'desc':vulDesc.encode('utf-8'),'type':vulType})
      session.commit()
      self.addTags(vulName,'vulnerability',tags)
      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(vulId,'vulnerability',environmentName)
        session.execute("call addVulnerabilitySeverity(:vId,:env,:severity)",{'vId':vulId,'env':environmentName,'severity':cProperties.severity()})
        for assetName in cProperties.assets():
          session.execute("call addAssetVulnerability(:vId,:env,:assName)",{'vId':vulId,'env':environmentName,'assName':assetName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating vulnerability (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
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

      session = self.conn()
      session.execute('call addPersona(:id,:name,:act,:att,:apt,:mot,:skills,:intr,:cont,:img,:ass,:type)',{'id':personaId,'name':personaName,'act':activities.encode('utf-8'),'att':attitudes.encode('utf-8'),'apt':aptitudes.encode('utf-8'),'mot':motivations.encode('utf-8'),'skills':skills.encode('utf-8'),'intr':intrinsic.encode('utf-8'),'cont':contextual.encode('utf-8'),'img':image,'ass':isAssumption,'type':pType})
      session.commit()
      session.close()
      self.addPersonaCodes(personaName,codes)
      self.addTags(personaName,'persona',tags)
      for environmentProperties in parameters.environmentProperties():
        environmentName = environmentProperties.name()
        self.addDimensionEnvironment(personaId,'persona',environmentName)
        self.addPersonaNarrative(personaId,environmentName,environmentProperties.narrative().encode('utf-8'))
        self.addPersonaDirect(personaId,environmentName,environmentProperties.directFlag())
        self.addDimensionRoles(personaId,'persona',environmentName,environmentProperties.roles())
        self.addPersonaEnvironmentCodes(personaName,environmentName,environmentProperties.codes())
      return personaId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding persona (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addDimensionRoles(self,personaId,table,environmentName,roles):
    try:
      session = self.conn()
      for role in roles:
        sqlTxt = 'call add_' + table + '_role (%s,"%s","%s")' %(personaId, environmentName,role)
        session.execute(sqlTxt)
      session.commit() 
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding roles to ' + table + ' id ' + str(personaId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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

    try:
      session = self.conn()
      session.execute('call deletePersonaComponents(:id)',{'id':personaId})
      session.execute('call updatePersona(:id,:name,:act,:att,:apt,:mot,:skills,:intr,:cont,:img,:ass,:type)',{'id':personaId,'name':personaName,'act':activities.encode('utf-8'),'att':attitudes.encode('utf-8'),'apt':aptitudes.encode('utf-8'),'mot':motivations.encode('utf-8'),'skills':skills.encode('utf-8'),'intr':intrinsic.encode('utf-8'),'cont':contextual.encode('utf-8'),'img':image,'ass':isAssumption,'type':pType})
      session.commit()
      self.addPersonaCodes(personaName,codes)
      self.addTags(personaName,'persona',tags)
      for environmentProperties in parameters.environmentProperties():
        environmentName = environmentProperties.name()
        self.addDimensionEnvironment(personaId,'persona',environmentName)
        self.addPersonaNarrative(personaId,environmentName,environmentProperties.narrative().encode('utf-8'))
        self.addPersonaDirect(personaId,environmentName,environmentProperties.directFlag())
        self.addDimensionRoles(personaId,'persona',environmentName,environmentProperties.roles())
        self.addPersonaEnvironmentCodes(personaName,environmentName,environmentProperties.codes())
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating persona (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
        envCodes = self.taskEnvironmentCodes(taskName,environmentName)
        properties = TaskEnvironmentProperties(environmentName,dependencies,personas,assets,concernAssociations,narrative,consequences,benefits,envCodes)
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
        narrative = self.misuseCaseNarrative(mcId,environmentId)
        properties = MisuseCaseEnvironmentProperties(environmentName,narrative)
        environmentProperties.append(properties)
      parameters = MisuseCaseParameters(mcName,environmentProperties,risk)
      mc = ObjectFactory.build(mcId,parameters)
      mcs[mcName] = mc
    return mcs

  def riskMisuseCase(self,riskId):
    try:
      session = self.conn()
      rs = session.execute('call riskMisuseCase(:id)',{'id':riskId})
      if (rs.rowcount == 0):
      	rs.close()
      	session.close()
        return None
      else:
        row = rs.fetchone()
        mcId = row[0]
        mcName = row[1]
        rs.close()
        session.close()
        risk = self.misuseCaseRisk(mcId)
        environmentProperties = []
        for environmentId,environmentName in self.dimensionEnvironments(mcId,'misusecase'):
          narrative = self.misuseCaseNarrative(mcId,environmentId)
          properties = MisuseCaseEnvironmentProperties(environmentName,narrative)
          environmentProperties.append(properties)
        parameters = MisuseCaseParameters(mcName,environmentProperties,risk)
        mc = ObjectFactory.build(mcId,parameters)
      return mc
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting misuse case (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 



  def misuseCaseRisk(self,mcId):
    return self.responseList('select misuseCaseRisk(:id)',{'id':mcId},'MySQL error getting risk for misuse case id ' + str(mcId))[0]

  def taskPersonas(self,taskId,environmentId):
    return self.responseList('call taskPersonas(:tId,:eId)',{'tId':taskId,'eId':environmentId},'MySQL error getting task personas for environment id ' + str(environmentId))

  def taskAssets(self,taskId,environmentId):
    return self.responseList('call taskAssets(:tId,:eId)',{'tId':taskId,'eId':environmentId},'MySQL error getting task assets for environment id ' + str(environmentId))

  def addTask(self,parameters):
    taskName = self.conn.connection().connection.escape_string(parameters.name())
    taskShortCode = self.conn.connection().connection.escape_string(parameters.shortCode())
    taskObjective = self.conn.connection().connection.escape_string(parameters.objective())
    isAssumption = parameters.assumption()
    taskAuthor = parameters.author()
    tags = parameters.tags()
    try:
      taskId = self.newId()
      session = self.conn()
      session.execute('call addTask(:id,:name,:shortCode,:obj,:ass,:auth)',{'id':taskId,'name':taskName,'shortCode':taskShortCode,'obj':taskObjective,'ass':isAssumption,'auth':taskAuthor})
      session.commit()
      session.close()
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
        self.addTaskNarrative(taskId,cProperties.narrative().encode('utf-8'),cProperties.consequences().encode('utf-8'),cProperties.benefits().encode('utf-8'),environmentName)
        self.addTaskEnvironmentCodes(taskName,environmentName,cProperties.codes())
      return taskId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding task ' + taskName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addMisuseCase(self,parameters):
    mcName = parameters.name()
    mcId = self.newId()
    self.updateDatabase('call addMisuseCase(:id,:name)',{'id':mcId,'name':mcName},'MySQL error adding misuse case ' + mcName)
    self.addMisuseCaseRisk(mcId,parameters.risk())
    for cProperties in parameters.environmentProperties():
      environmentName = cProperties.name()
      self.addDimensionEnvironment(mcId,'misusecase',environmentName)
      self.addMisuseCaseNarrative(mcId,cProperties.narrative().encode('utf-8'),environmentName)
    return mcId


  def updateTask(self,parameters):
    taskId = parameters.id()
    taskName = parameters.name()
    taskShortCode = parameters.shortCode()
    taskObjective = parameters.objective()
    isAssumption = parameters.assumption()
    taskAuthor = parameters.author()
    tags = parameters.tags()
    try:
      session = self.conn()
      session.execute('call deleteTaskComponents(:id)',{'id':taskId})
      session.execute('call updateTask(:id,:name,:shortCode,:obj,:ass,:auth)',{'id':taskId,'name':taskName,'shortCode':taskShortCode,'obj':taskObjective,'ass':isAssumption,'auth':taskAuthor})
      session.commit()
      session.close()
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
        self.addTaskNarrative(taskId,cProperties.narrative().encode('utf-8'),cProperties.consequences().encode('utf-8'),cProperties.benefits().encode('utf-8'),environmentName)
        self.addTaskEnvironmentCodes(taskName,environmentName,cProperties.codes())
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding task ' + taskName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateMisuseCase(self,parameters):
    mcId = parameters.id()
    mcName = parameters.name()
    try:
      session = self.conn()
      session.execute('call deleteMisuseCaseComponents(:id)',{'id':mcId})
      session.execute('call updateMisuseCase(:id,:name)',{'id':mcId,'name':mcName})
      session.commit()
      session.close()
      self.addMisuseCaseRisk(mcId,parameters.risk())
      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(mcId,'misusecase',environmentName)
        self.addMisuseCaseNarrative(mcId,cProperties.narrative().encode('utf-8'),environmentName)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding misuse case ' + mcName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def addTaskPersonas(self,taskId,personas,environmentName):
    try:
      session = self.conn()
      for persona,duration,frequency,demands,goalsupport in personas:
        session.execute('call addTaskPersona(:tId,:pers,:dur,:freq,:dem,:goal,:env)',{'tId':taskId,'pers':persona,'dur':duration,'freq':frequency,'dem':demands,'goal':goalsupport,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating personas used in task ' + str(taskId) + ' with environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addTaskAssets(self,taskId,assets,environmentName):
    try:
      session = self.conn()
      for asset in assets:
        session.execute('call addTaskAsset(:tId,:ass,:env)',{'tId':taskId,'ass':asset,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating assets used in task ' + str(taskId) + ' with environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addMisuseCaseRisk(self,mcId,riskName):
    self.updateDatabase('call addMisuseCaseRisk(:id,:risk)',{'id':mcId,'risk':riskName},'MySQL error associating risk with misuse case')

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
    parameterList = self.responseList('call getRisks(:id)',{'id':constraintId},'MySQL error getting risks')
    risks = {}
    for parameters in parameterList:
      riskId = parameters[0]
      mc = self.riskMisuseCase(riskId)
      tags = self.getTags(parameters[1],'risk')
      parameters = RiskParameters(parameters[1],parameters[2],parameters[3],mc,tags)
      risk = ObjectFactory.build(riskId,parameters)
      risks[risk.name()] = risk
    return risks


  def addRisk(self,parameters):
    threatName = parameters.threat()
    vulName = parameters.vulnerability()
    tags = parameters.tags()
    riskId = self.newId()
    riskName = parameters.name()
    inTxt = parameters.intent()
    self.updateDatabase('call addRisk(:threat,:vuln,:rId,:risk,:txt)',{'threat':threatName,'vuln':vulName,'rId':riskId,'risk':riskName,'txt':inTxt},'MySQL error adding risk')
    mc = parameters.misuseCase()
    mcParameters = MisuseCaseParameters(mc.name(),mc.environmentProperties(),mc.risk())
    self.addMisuseCase(mcParameters)
    self.addTags(riskName,'risk',tags)
    return riskId

  def updateRisk(self,parameters):
    riskId = parameters.id()
    threatName = parameters.threat()
    vulName = parameters.vulnerability()
    tags = parameters.tags()
    riskName = parameters.name()
    inTxt = parameters.intent()
    self.updateDatabase('call updateRisk(:threat,:vuln,:rId,:risk,:txt)',{'threat':threatName,'vuln':vulName,'rId':riskId,'risk':riskName,'txt':inTxt},'MySQL error updating risk')
    mc = parameters.misuseCase()
    mcParameters = MisuseCaseParameters('Exploit ' + riskName,mc.environmentProperties(),riskName)
    mcParameters.setId(mc.id())
    self.updateMisuseCase(mcParameters)
    self.addTags(riskName,'risk',tags)

  def deleteRisk(self,riskId):
    self.deleteObject(riskId,'risk')
    

  def deleteMisuseCase(self,mcId):
    self.deleteObject(mcId,'misusecase')
    
  def getResponses(self,constraintId = -1):
    responseRows = self.responseList('call getResponses(:id)',{'id':constraintId},'MySQL error getting responses')
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
    respName = parameters.name()
    respRisk = parameters.risk()
    respType = parameters.responseType()
    tags = parameters.tags()
    respId = self.newId()
    self.updateDatabase('call addResponse(:id,:name,:type,:risk)',{'id':respId,'name':respName,'type':respType,'risk':respRisk},'MySQL error adding response')
    self.addTags(respName,'response',tags)
    for cProperties in parameters.environmentProperties():
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
    try:
      session = self.conn()
      for role,cost in roles:
        session.execute('call addResponseRole(:id,:role,:cost,:env,:desc)',{'id':responseId,'role':role,'cost':cost,'env':environmentName,'desc':respDesc})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating roles with response ' + str(responseId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def updateResponse(self,parameters):
    respName = parameters.name()
    respRisk = parameters.risk()
    respType = parameters.responseType()
    tags = parameters.tags()
    respId = parameters.id()
    try:
      session = self.conn()
      session.execute('call deleteResponseComponents(:id)',{'id':respId})
      session.execute('call updateResponse(:id,:name,:type,:risk)',{'id':respId,'name':respName,'type':respType,'risk':respRisk})
      session.commit()
      session.close()
      self.addTags(respName,'response',tags)
      for cProperties in parameters.environmentProperties():
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
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

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
        if (fromObjt != dimensionName) and (toObjt != dimensionName):
          continue
      if (objectName != ''):
        if (fromName != objectName) and (toName != objectName):
          continue
      parameters = DotTraceParameters(fromObjt,fromName,toObjt,toName)
      traces.append(ObjectFactory.build(-1,parameters))
    return traces

  def removableTraces(self,environmentName):
    traceRows = self.responseList('call viewRemovableTraces(:env)',{'env':environmentName},'MySQL error getting removable trace relations')
    traces = []
    for fromObjt,fromName,toObjt,toName in traceRows:
      if (fromObjt == 'task' and toObjt == 'asset'):
        continue
      traces.append((fromObjt,fromName,toObjt,toName))
    return traces

  def allowableTraceDimension(self,fromId,toId):
    return self.responseList('call allowableTraceDimension(:frm,:to)',{'frm':fromId,'to':toId},'MySQL error getting allowable trace dimensions for from_id ' + str(fromId) + ' and to_id ' + str(toId))[0]

  def reportDependencies(self,dimName,objtId):
    return self.responseList('call reportDependents(:id,:name)',{'id':objtId,'name':dimName},'MySQL error getting dependencies for ' + dimName + ' id ' + str(objtId))

  def deleteDependencies(self,deps):
    for dep in deps:
      dimName = dep[0]
      objtId = dep[1]
      self.deleteObject(objtId,dimName)
    

  def threatenedAssets(self,threatId,environmentId):
    return self.responseList('call threat_asset(:tId,:eId)',{'tId':threatId,'eId':environmentId},'MySQL error getting assets associated with threat id ' + str(threatId) + ' in environment id ' + str(environmentId))

  def vulnerableAssets(self,vulId,environmentId):
    return self.responseList('call vulnerability_asset(:vId,:eId)',{'vId':vulId,'eId':environmentId},'MySQL error getting assets associated with vulnerability id ' + str(vulId) + ' in environment id ' + str(environmentId))

  def addTrace(self,traceTable,fromId,toId,contributionType = 'and'):
    try:
      session = self.conn()
     
      if (traceTable != 'requirement_task' and traceTable != 'requirement_usecase' and traceTable != 'requirement_requirement'):
        sqlText = 'insert into ' + traceTable + ' values(%s,%s)' %(fromId,toId)
        session.execute(sqlText) 
      elif (traceTable == 'requirement_requirement'):
        sqlText = 'insert into ' + traceTable + ' values(%s,%s,"%s")' %(fromId,toId,contributionType)
        session.execute(sqlText) 
      else:
        refTypeId = self.getDimensionId(contributionType,'reference_type')
        sqlText = 'insert into ' + traceTable + ' values(%s,%s,%s)' %(fromId,toId,refTypeId)
        session.execute(sqlText) 
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding fromId ' + str(fromId) + ' and toId ' + str(toId) + ' to link table ' + traceTable + ' (id: ' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteEnvironment(self,environmentId):
    try: 
      curs = self.conn.connection().connection.cursor()
      sqlTxt = 'call delete_environment(%s)'
      curs.execute(sqlTxt,[environmentId])
      curs.close()
    except _mysql_exceptions.IntegrityError, e:
      id,msg = e
      exceptionText = 'Cannot remove environment due to dependent data (id:' + str(id) + ',message:' + msg + ').'
      raise IntegrityException(exceptionText) 
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error deleting environments (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)     

  def riskRating(self,thrName,vulName,environmentName):
    return self.responseList('call riskRating(:thr,:vuln,:env)',{'thr':thrName,'vuln':vulName,'env':environmentName},'MySQL error rating risk associated with threat/vulnerability/environment ' + thrName + '/' + vulName + '/' + environmentName)[0]


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
      if (targetName in targets):
        targets[targetName].add(responseName)
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
        properties = RoleEnvironmentProperties(environmentName,roleResponses,roleCountermeasures)
        environmentProperties.append(properties)
      parameters = RoleParameters(roleName,roleType,shortCode,roleDescription,environmentProperties)
      role = ObjectFactory.build(roleId,parameters)
      roles[roleName] = role
    return roles

  def addRole(self,parameters):
    roleId = self.newId()
    roleName = parameters.name()
    roleType = parameters.type()
    shortCode = parameters.shortCode()
    roleDesc = parameters.description()
    try:
      session = self.conn()
      session.execute('call addRole(:id,:name,:type,:shortCode,:desc)',{'id':roleId,'name':roleName,'type':roleType,'shortCode':shortCode,'desc':roleDesc})
      session.commit()
      session.close()
      return roleId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding role ' + roleName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateRole(self,parameters):
    roleId = parameters.id()
    roleName = parameters.name()
    roleType = parameters.type()
    shortCode = parameters.shortCode()
    roleDesc = parameters.description()
    try:
      session = self.conn()
      session.execute('call updateRole(:id,:name,:type,:shortCode,:desc)',{'id':roleId,'name':roleName,'type':roleType,'shortCode':shortCode,'desc':roleDesc})
      session.commit()
      session.close()
      return roleId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating role ' + roleName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteRole(self,roleId):
    self.deleteObject(roleId,'role')
    

  def roleResponsibilities(self,roleId,environmentId):
    return self.responseList('call roleResponses(:rId,:eId)',{'rId':roleId,'eId':environmentId},'MySQL error getting responses for role id ' + str(roleId) + ' in environment ' + str(environmentId))

  def roleCountermeasures(self,roleId,environmentId):
    return self.responseList('call roleCountermeasures(:rId,:eId)',{'rId':roleId,'eId':environmentId},'MySQL error getting countermeasures for role id ' + str(roleId) + ' in environment ' + str(environmentId))

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
    cmName = parameters.name()
    cmDesc = parameters.description()
    cmType = parameters.type()
    tags = parameters.tags()
    cmId = self.newId()
    try:
      session = self.conn()
      session.execute('call addCountermeasure(:id,:name,:desc,:type)',{'id':cmId,'name':cmName,'desc':cmDesc,'type':cmType})
      session.commit()
      session.close()
      self.addTags(cmName,'countermeasure',tags)

      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(cmId,'countermeasure',environmentName)
        self.addCountermeasureTargets(cmId,cProperties.requirements(),cProperties.targets(),environmentName)
        self.addSecurityProperties('countermeasure',cmId,environmentName,cProperties.properties(),cProperties.rationale())
        self.addCountermeasureCost(cmId,cProperties.cost(),environmentName)
        self.addCountermeasureRoles(cmId,cProperties.roles(),environmentName)
        self.addCountermeasurePersonas(cmId,cProperties.personas(),environmentName)
        self.addRequirementRoles(cmName,cProperties.roles(),cProperties.requirements(),environmentName)

      return cmId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding countermeasure ' + cmName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def updateCountermeasure(self,parameters):
    cmName = parameters.name()
    cmDesc = parameters.description()
    cmType = parameters.type()
    tags = parameters.tags()
    cmId = parameters.id()
    environmentProperties = parameters.environmentProperties()
    try:
      session = self.conn()
      session.execute('call deleteCountermeasureComponents(:id)',{'id':cmId})
      session.execute('call updateCountermeasure(:id,:name,:desc,:type)',{'id':cmId,'name':cmName,'desc':cmDesc,'type':cmType})
      session.commit()
      session.close()
      self.addTags(cmName,'countermeasure',tags)

      for cProperties in environmentProperties:
        environmentName = cProperties.name()
        self.addDimensionEnvironment(cmId,'countermeasure',environmentName)
        self.updateCountermeasureTargets(cmId,cProperties.requirements(),cProperties.targets(),environmentName)
        self.addSecurityProperties('countermeasure',cmId,environmentName,cProperties.properties(),cProperties.rationale())
        self.addCountermeasureCost(cmId,cProperties.cost(),environmentName)
        self.addCountermeasureRoles(cmId,cProperties.roles(),environmentName)
        self.addCountermeasurePersonas(cmId,cProperties.personas(),environmentName)
        self.updateRequirementRoles(cmName,cProperties.roles(),cProperties.requirements(),environmentName)
      return cmId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating countermeasure ' + cmName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def addCountermeasureTargets(self,cmId,reqs,targets,environmentName):
    try:
      session = self.conn()
      for reqLabel in reqs:
        session.execute('call addCountermeasureRequirement(:cmId,:lbl,:env)',{'cmId':cmId,'lbl':reqLabel,'env':environmentName})
      for target in targets:
        session.execute('call addCountermeasureTarget(:cmId,:name,:effectiveness,:rationale,:env)',{'cmId':cmId,'name':target.name(),'effectiveness':target.effectiveness(),'rationale':target.rationale(),'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating targets with countermeasure ' + str(cmId) + ' in environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def updateCountermeasureTargets(self,cmId,reqs,targets,environmentName):
    try:
      session = self.conn()
      for reqLabel in reqs:
        session.execute('call updateCountermeasureRequirement(:cmId,:lbl,:env)',{'cmId':cmId,'lbl':reqLabel,'env':environmentName})
      for target in targets:
        session.execute('call addCountermeasureTarget(:cmId,:name,:effectiveness,:rationale,:env)',{'cmId':cmId,'name':target.name(),'effectiveness':target.effectiveness(),'rationale':target.rationale(),'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating targets with countermeasure ' + str(cmId) + ' in environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)


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
    try:
      session = self.conn()
      session.execute('call addRequirementRole(:aId,:cm,:role,:req,:env)',{'aId':associationId,'cm':cmName,'role':roleName,'req':reqName,'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating requirement ' + reqName + ' with role ' + roleName + ' in environment ' + envName + ' - response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def updateRequirementRole(self,cmName,roleName,reqName,envName):
    associationId = self.newId()
    try:
      session = self.conn()
      session.execute('call updateRequirementRole(:aId,:cm,:role,:req,:env)',{'aId':associationId,'cm':cmName,'role':roleName,'req':reqName,'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating requirement ' + reqName + ' with role ' + roleName + ' in environment ' + envName + ' - response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def deleteRequirementRole(self,roleName,reqName,envName):
    try:
      session = self.conn()
      session.execute('call deleteRequirementRole(:role,:req,:env)',{'role':roleName,'req':reqName,'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error de-associating requirement ' + reqName + ' with role ' + roleName + ' in environment ' + environmentName + ' - response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def addCountermeasureCost(self,cmId,costName,environmentName):
    try:
      session = self.conn()
      session.execute('call addCountermeasureCost(:cmId,:cost,:env)',{'cmId':cmId,'cost':costName,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating cost ' + costName + ' with response ' + str(cmId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def addCountermeasureRoles(self,cmId,roles,environmentName):
    try:
      session = self.conn()
      for role in roles:
        session.execute('call addCountermeasureRole(:cmId,:role,:env)',{'cmId':cmId,'role':role,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating role ' + role + ' with countermeasure ' + str(cmId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def addCountermeasurePersonas(self,cmId,personas,environmentName):
    try:
      session = self.conn()
      for task,persona,duration,frequency,demands,goalSupport in personas:
        session.execute('call addCountermeasurePersona(:id,:persona,:task,:dur,:freq,:dem,:goal,:env)',{'id':cmId,'persona':persona,'task':task,'dur':duration,'freq':frequency,'dem':demands,'goal':goalSupport,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating personas with countermeasure ' + str(cmId) + ' in environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def personaNarrative(self,scId,environmentId):
    return self.responseList('select personaNarrative(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting narrative for persona id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def personaDirect(self,scId,environmentId):
    directFlag = self.responseList('select personaDirect(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting directFlag for persona id ' + str(scId) + ' in environment ' + str(environmentId))[0]
    directValue = 'False'
    if (directFlag == 1):
      directValue = 'True'
    return directValue
   

  def addPersonaNarrative(self,stId,environmentName,descriptionText):
    try:
      session = self.conn()
      session.execute('call addPersonaNarrative(:stId,:desc,:env)',{'stId':stId,'desc':descriptionText,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating narrative with persona ' + str(stId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def addPersonaDirect(self,stId,environmentName,directText):
    try:
      session = self.conn()
      session.execute('call addPersonaDirect(:stId,:txt,:env)',{'stId':stId,'txt':directText,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating direct flag with persona ' + str(stId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def taskNarrative(self,scId,environmentId):
    return self.responseList('select taskNarrative(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting narrative for task id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def taskConsequences(self,scId,environmentId):
    return self.responseList('select taskConsequences(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting consequences for task id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def taskBenefits(self,scId,environmentId):
    return self.responseList('select taskBenefits(:scId,:env)',{'scId':scId,'env':environmentId},'MySQL error getting benefits for task id ' + str(scId) + ' in environment ' + str(environmentId))[0]

  def addTaskNarrative(self,scId,narrativeText,cText,bText,environmentName):
    try:
      session = self.conn()
      session.execute('call addTaskNarrative(:scId,:nTxt,:cTxt,:bTxt,:env)',{'scId':scId,'nTxt':narrativeText,'cTxt':cText,'bTxt':bText,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating narrative with task ' + str(scId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def misuseCaseNarrative(self,mcId,environmentId):
    return self.responseList('select misuseCaseNarrative(:mcId,:env)',{'mcId':mcId,'env':environmentId},'MySQL error getting narrative for misusecase id ' + str(mcId) + ' in environment ' + str(environmentId))[0]

  def addMisuseCaseNarrative(self,mcId,narrativeText,environmentName):
    try:
      session = self.conn()
      session.execute('call addMisuseCaseNarrative(:mcId,:nTxt,:env)',{'mcId':mcId,'nTxt':narrativeText,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating narrative with misuse case ' + str(mcId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def riskEnvironmentNames(self,riskName):
    return self.responseList('call riskEnvironmentNames(:risk)',{'risk':riskName},'MySQL error getting environments associated with risk ' + riskName)

  def threatVulnerabilityEnvironmentNames(self,threatName,vulName):
    return self.responseList('call threatVulnerabilityEnvironmentNames(:threat,:vuln)',{'threat':threatName,'vuln':vulName},'MySQL error getting environments associated with threat ' + threatName + ' and vulnerability ' + vulName);

  def taskDependencies(self,tId,environmentId):
    return self.responseList('select taskDependencies(:tId,:eId)',{'tId':tId,'eId':environmentId},'MySQL error getting dependencies for task id ' + str(tId) + ' in environment ' + str(environmentId))[0]

  def addTaskDependencies(self,tId,depsText,environmentName):
    try:
      session = self.conn()
      session.execute('call addTaskDependencies(:tId,:txt,:env)',{'tId':tId,'txt':depsText,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating objective with task ' + str(tId) + ' in environment ' + environmentName + ' response (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def mitigatedRisks(self,cmId):
    return self.responseList('call mitigatedRisks(:id)',{'id':cmId},'MySQL error getting risks mitigated by countermeasure id ' + str(cmId))

  def deleteTrace(self,fromObjt,fromName,toObjt,toName):
    try:
      session = self.conn()
      session.execute('call delete_trace(:fObj,:fName,:tObj,:tName)',{'fObj':fromObjt,'fName':fromName,'tObj':toObjt,'tName':toName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error deleting trace relation: (' + fromObjt + ',' + fromName + ',' + toObjt + ',' + toName + ') (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText)

  def deleteCountermeasure(self,cmId):
    self.deleteObject(cmId,'countermeasure')
    

  def addGoal(self,parameters):
    goalId = self.newId()
    goalName = parameters.name()
    goalOrig = parameters.originator()
    tags = parameters.tags()
    try:
      session = self.conn()
      session.execute('call addGoal(:id,:name,:orig)',{'id':goalId,'name':goalName,'orig':goalOrig})
      session.commit()
      session.close()
      self.addTags(goalName,'goal',tags)
      for environmentProperties in parameters.environmentProperties():
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
      return goalId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding goal ' + goalName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateGoal(self,parameters):
    goalId = parameters.id()
    goalName = parameters.name()
    goalOrig = parameters.originator()
    tags = parameters.tags()
    try:
      session = self.conn()
      session.execute('call deleteGoalComponents(:id)',{'id':goalId})
      session.execute('call updateGoal(:id,:name,:orig)',{'id':goalId,'name':goalName,'orig':goalOrig})
      session.commit()
      session.close()
      self.addTags(goalName,'goal',tags)
      for environmentProperties in parameters.environmentProperties():
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
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating goal ' + goalName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
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
        properties = GoalEnvironmentProperties(environmentName,goalLabel,goalDef,goalType,goalPriority,goalFitCriterion,goalIssue,goalRefinements,subGoalRefinements,concerns,concernAssociations)
        environmentProperties.append(properties) 
      return environmentProperties
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting goal environment properties for goal id ' + str(goalId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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

  def environmentDimensions(self,dimension,envName):
    return self.responseList('call ' + dimension + 'Names(:env)',{'env':envName},'MySQL error getting ' + dimension + 's associated with environment ' + envName)

  def environmentAssets(self,envName):
    return self.environmentDimensions('asset',envName)

  def environmentGoals(self,envName):
    return self.environmentDimensions('goal',envName)

  def environmentObstacles(self,envName):
    return self.environmentDimensions('obstacle',envName)

  def environmentDomainProperties(self,envName):
    return self.environmentDimensions('domainProperty',envName)

  def environmentCountermeasures(self,envName):
    return self.environmentDimensions('countermeasure',envName)

  def environmentTasks(self,envName):
    return self.environmentDimensions('task',envName)

  def environmentThreats(self,envName):
    return self.environmentDimensions('threat',envName)

  def environmentVulnerabilities(self,envName):
    return self.environmentDimensions('vulnerability',envName)

  def environmentUseCases(self,envName):
    return self.environmentDimensions('usecase',envName)

  def environmentMisuseCases(self,envName):
    return self.environmentDimensions('misusecase',envName)

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

    try:
      session = self.conn()
      session.execute('call addClassAssociation(:ass,:env,:hAss,:hType,:hNav,:hMult,:hRole,:tRole,:tMult,:tNav,:tType,:tAss)',{'ass':associationId,'env':envName,'hAss':headAsset,'hType':headType,'hNav':headNav,'hMult':headMult,'hRole':headRole,'tRole':tailRole,'tMult':tailMult,'tNav':tailNav,'tType':tailType,'tAss':tailAsset})
      session.commit()
      session.close()
      return associationId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding class association ' + envName + '/' + headAsset + '/' + tailAsset + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateClassAssociation(self,parameters):
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

    try:
      session = self.conn()
      session.execute('call updateClassAssociation(:ass,:env,:hAss,:hType,:hNav,:hMult,:hRole,:tRole,:tMult,:tNav,:tType,:tAss)',{'ass':associationId,'env':envName,'hAss':headAsset,'hType':headType,'hNav':headNav,'hMult':headMult,'hRole':headRole,'tRole':tailRole,'tMult':tailMult,'tNav':tailNav,'tType':tailType,'tAss':tailAsset})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating class association ' + envName + '/' + headAsset + '/' + tailAsset + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    for associationId,envName,goalDim,goalName,aType,subGoalName,subGoalDimName,alternativeId,rationale in rows:
      parameters = GoalAssociationParameters(envName,goalName,goalDimName,aType,subGoalName,subGoalDimName,alternativeId,rationale)
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
    if (goalName == ''):
      return
    goalDimName = parameters.goalDimension()
    aType = parameters.type()
    subGoalName = parameters.subGoal()
    subGoalDimName = parameters.subGoalDimension()
    alternativeId = parameters.alternative()
    rationale = parameters.rationale()
    try:
      session = self.conn()
      session.execute('call addGoalAssociation(:assId,:env,:goal,:dim,:type,:sGName,:sGDName,:altId,:rationale)',{'assId':associationId,'env':envName,'goal':goalName,'dim':goalDimName,'type':aType,'sGName':subGoalName,'sGDName':subGoalDimName,'altId':alternativeId,'rationale':rationale})
      session.commit()
      session.close()
      return associationId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding goal association ' + envName + '/' + goalName + '/' + subGoalName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
      session = self.conn()
      session.execute('call updateGoalAssociation(:assId,:env,:goal,:dim,:type,:sGName,:sGDName,:altId,:rationale)',{'assId':associationId,'env':envName,'goal':goalName,'dim':goalDimName,'type':aType,'sGName':subGoalName,'sGDName':subGoalDimName,'altId':alternativeId,'rationale':rationale})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating goal association ' + envName + '/' + goalName + '/' + subGoalName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteGoalAssociation(self,associationId,goalDimName,subGoalDimName):
    try:
      session = self.conn()
      session.execute('call delete_goalassociation(:ass,:gDName,:sGDName)',{'ass':associationId,'gDName':goalDimName,'sGDName':subGoalDimName})
      session.commit()
      session.close()
    except _mysql_exceptions.IntegrityError, e:
      id,msg = e
      exceptionText = 'Cannot remove goal association due to dependent data.  Check the goal model model for further information  (id:' + str(id) + ',message:' + msg + ')'
      raise IntegrityException(exceptionText) 
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error deleting goal association (id:' + str(id) + ',message:' + msg + ')'


  def addGoalDefinition(self,goalId,environmentName,goalDef):
    try:
      session = self.conn()
      session.execute('call addGoalDefinition(:gId,:env,:gDef)',{'gId':goalId,'env':environmentName,'gDef':goalDef})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating details with goal id ' + str(goalId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addGoalCategory(self,goalId,environmentName,goalCat):
    try:
      session = self.conn()
      session.execute('call addGoalCategory(:gId,:env,:gCat)',{'gId':goalId,'env':environmentName,'gCat':goalCat})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating details with goal id ' + str(goalId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addGoalPriority(self,goalId,environmentName,goalPri):
    try:
      session = self.conn()
      session.execute('call addGoalPriority(:gId,:env,:gPri)',{'gId':goalId,'env':environmentName,'gPri':goalPri})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating details with goal id ' + str(goalId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addGoalFitCriterion(self,goalId,environmentName,goalFC):
    try:
      session = self.conn()
      session.execute('call addGoalFitCriterion(:gId,:env,:gFC)',{'gId':goalId,'env':environmentName,'gFC':goalFC})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating details with goal id ' + str(goalId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addGoalIssue(self,goalId,environmentName,goalIssue):
    try:
      session = self.conn()
      session.execute('call addGoalIssue(:gID,:env,:gIssue)',{'gID':goalId,'env':environmentName,'gIssue':goalIssue})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating details with goal id ' + str(goalId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addGoalRefinements(self,goalId,goalName,environmentName,goalAssociations,subGoalAssociations):
    for goal,goalDim,refinement,altName,rationale in subGoalAssociations:
      alternativeId = 0
      if (altName == 'Yes'):
        alternativeId = 1
      parameters = GoalAssociationParameters(environmentName,goalName,'goal',refinement,goal,goalDim,alternativeId,rationale)
      self.addGoalAssociation(parameters) 
    for goal,goalDim,refinement,altName,rationale in goalAssociations:
      alternativeId = 0
      if (altName == 'Yes'):
        alternativeId = 1
      parameters = GoalAssociationParameters(environmentName,goal,goalDim,refinement,goalName,'goal',alternativeId,rationale)
      self.addGoalAssociation(parameters) 

  def addGoalConcernAssociations(self,goalId,environmentName,associations):
    for source,sourceMultiplicity,link,target,targetMultiplicity in associations:
      self.addGoalConcernAssociation(goalId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity) 

  def addGoalConcernAssociation(self,goalId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity):
    self.updateDatabase('call addGoalConcernAssociation(:gId,:env,:src,:sMulti,:link,:trgt,:tMulti)',{'gId':goalId,'env':environmentName,'src':source,'sMulti':sourceMultiplicity,'linl':link,'trgt':target,'tMulti':targetMultiplicity},'MySQL error adding goal concern association')

  def addTaskConcernAssociations(self,taskId,environmentName,associations):
    for source,sourceMultiplicity,link,target,targetMultiplicity in associations:
      self.addTaskConcernAssociation(taskId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity) 

  def addTaskConcernAssociation(self,taskId,environmentName,source,sourceMultiplicity,link,target,targetMultiplicity):
    self.updateDatabase('call addTaskConcernAssociation(:tId,:env,:src,:sMulti,:link,:trgt,:tMulti)',{'tId':taskId,'env':environmentName,'src':source,'sMulti':sourceMultiplicity,'link':link,'trgt':target,'tMulti':targetMultiplicity},'MySQL error adding task concern association')

  def addObstacleRefinements(self,goalId,goalName,environmentName,goalAssociations,subGoalAssociations):
    for goal,goalDim,refinement,altName,rationale in subGoalAssociations:
      alternativeId = 0
      if (altName == 'Yes'):
        alternativeId = 1
      parameters = GoalAssociationParameters(environmentName,goalName,'obstacle',refinement,goal,goalDim,alternativeId,rationale)
      self.addGoalAssociation(parameters) 
    for goal,goalDim,refinement,altName,rationale in goalAssociations:
      alternativeId = 0
      if (altName == 'Yes'):
        alternativeId = 1
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
    try:
      session = self.conn()
      session.execute('call add_goal_concern(:goal,:env,:conc)',{'goal':goalId,'env':environmentName,'conc':concern})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding concern ' + concern + ' to goal id ' + str(goalId) + ' in environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    dpId = self.newId()
    dpName = parameters.name()
    dpDesc = parameters.description()
    dpType = parameters.type()
    dpOrig = parameters.originator()
    tags = parameters.tags()
    self.updateDatabase('call addDomainProperty(:id,:name,:desc,:type,:orig)',{'id':dpId,'name':dpName,'desc':dpDesc,'type':dpType,'orig':dpOrig},'MySQL error adding domain property')
    self.addTags(dpName,'domainproperty',tags)
    return dpId

  def updateDomainProperty(self,parameters):
    dpId = parameters.id()
    dpName = parameters.name()
    dpDesc = parameters.description()
    dpType = parameters.type()
    dpOrig = parameters.originator()
    tags = parameters.tags()
    self.updateDatabase('call updateDomainProperty(:id,:name,:desc,:type,:orig)',{'id':dpId,'name':dpName,'desc':dpDesc,'type':dpType,'orig':dpOrig},'MySQL error updating domain property')
    self.addTags(dpName,'domainproperty',tags)
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
    obsId = self.newId()
    obsName = parameters.name().encode('utf-8')
    obsOrig = parameters.originator().encode('utf-8')
    tags = parameters.tags()
    self.updateDatabase('call addObstacle(:id,:name,:orig)',{'id':obsId,'name':obsName,'orig':obsOrig},'MySQL error adding obstacle')
    self.addTags(obsName,'obstacle',tags)
    for environmentProperties in parameters.environmentProperties():
      environmentName = environmentProperties.name()
      self.addDimensionEnvironment(obsId,'obstacle',environmentName)
      self.addObstacleDefinition(obsId,environmentName,environmentProperties.definition(),environmentProperties.probability(),environmentProperties.probabilityRationale())
      self.addObstacleCategory(obsId,environmentName,environmentProperties.category())
      self.addObstacleRefinements(obsId,obsName,environmentName,environmentProperties.goalRefinements(),environmentProperties.subGoalRefinements())
      self.addObstacleConcerns(obsId,environmentName,environmentProperties.concerns())
    return obsId

  def updateObstacle(self,parameters):
    obsId = parameters.id()
    obsName = parameters.name()
    obsOrig = parameters.originator()
    tags = parameters.tags()
    try:
      session = self.conn()
      session.execute('call deleteObstacleComponents(:id)',{'id':obsId})
      session.execute('call updateObstacle(:id,:name,:orig)',{'id':obsId,'name':obsName,'orig':obsOrig})
      session.commit()
      session.close()
      self.addTags(obsName,'obstacle',tags)
      for environmentProperties in parameters.environmentProperties():
        environmentName = environmentProperties.name()
        self.addDimensionEnvironment(obsId,'obstacle',environmentName)
        self.addObstacleDefinition(obsId,environmentName,environmentProperties.definition(),environmentProperties.probability(),environmentProperties.probabilityRationale())
        self.addObstacleCategory(obsId,environmentName,environmentProperties.category())
        self.addObstacleRefinements(obsId,obsName,environmentName,environmentProperties.goalRefinements(),environmentProperties.subGoalRefinements())
        self.addObstacleConcerns(obsId,environmentName,environmentProperties.concerns())
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating obstacle ' + obsName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addObstacleDefinition(self,obsId,environmentName,obsDef,obsProb,obsProbRat):
    self.updateDatabase('call addObstacleDefinition(:id,:env,:def,:prob,:probRat)',{'id':obsId,'env':environmentName,'def':obsDef,'prob':obsProb,'probRat':obsProbRat},'MySQL error adding obstacle definition')

  def addObstacleCategory(self,obsId,environmentName,obsCat):
    self.updateDatabase('call addObstacleCategory(:obs,:env,:cat)',{'obs':obsId,'env':environmentName,'cat':obsCat},'MySQL error adding obstacle category')

  def deleteObstacle(self,obsId):
    self.deleteObject(obsId,'obstacle')
    

  def updateSettings(self, projName, background, goals, scope, definitions, contributors,revisions,richPicture,fontSize = '7.5',fontName = 'Times New Roman'):
    try:
      session = self.conn()
      session.execute('call updateProjectSettings(:proj,:bg,:goals,:scope,:picture,:fontSize,:font)',{'proj':projName,'bg':background.encode('utf-8'),'goals':goals.encode('utf-8'),'scope':scope.encode('utf-8'),'picture':richPicture,'fontSize':fontSize,'font':fontName})
      session.execute('call deleteDictionary()')
      for entry in definitions:
        session.execute('call addDictionaryEntry(:e0,:e1)',{'e0':entry[0],'e1':entry[1].encode('utf-8')})
      session.execute('call deleteContributors()')
      for entry in contributors:
        session.execute('call addContributorEntry(:e0,:e1,:e2,:e3)',{'e0':entry[0],'e1':entry[1],'e2':entry[2],'e3':entry[3]})
      session.execute('call deleteRevisions()')
      for entry in revisions:
        session.execute('call addRevision(:e0,:e1,:e2)',{'e0':entry[0],'e1':entry[1],'e2':entry[2]})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating project settings (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getProjectSettings(self):
    rows = self.responseList('call getProjectSettings()',{},'MySQL error getting project settings')
    pSettings = {}
    for key,value in rows:
      pSettings[key] = value
    return pSettings
  
  def getDictionary(self):
    rows = self.responseList('call getDictionary()',{},'MySQL error getting dictionary')
    pDict = {}
    for key,value in rows:
      pDict[key] = value
    return pDict

  def getContributors(self):
    return self.responseList('call getContributors()',{},'MySQL error getting contributors')

  def getRevisions(self):
    return self.responseList('call getRevisions()',{},'MySQL error getting revisions')

  def getRequirementVersions(self,reqId):
    return self.responseList('call getRequirementVersions(:id)',{'id':reqId},'MySQL error getting requirement versions')

  def existingResponseGoal(self,responseId):
    return int(self.responseList('select existingResponseGoal(:id)',{'id':responseId},'MySQL error getting existing response goal')[0])

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

  def deleteCapability(self,objtId):
    self.deleteValueType(objtId,'capability')

  def deleteMotivation(self,objtId):
    self.deleteValueType(objtId,'motivation')

  def deleteAssetType(self,objtId):
    self.deleteValueType(objtId,'asset_type')

  def deleteThreatType(self,objtId):
    self.deleteValueType(objtId,'threat_type')

  def deleteVulnerabilityType(self,objtId):
    self.deleteValueType(objtId,'vulnerability_type')

  def deleteValueType(self,objtId,value_type):
    self.deleteObject(objtId,value_type)
    
  def addValueType(self,parameters):
    if (parameters.id() != -1):
      valueTypeId = parameters.id()
    else:
      valueTypeId = self.newId()
    vtName = parameters.name()
    vtDesc = parameters.description()
    vtType = parameters.type()
    vtScore = parameters.score()
    if vtScore == '':
      vtScore = 0
    else:
      vtScore = int(vtScore)
    vtRat = parameters.rationale()
    if ((vtType == 'asset_value') or (vtType == 'threat_value') or (vtType == 'risk_class') or (vtType == 'countermeasure_value')):
      exceptionText = 'Cannot add ' + vtType + 's'
      raise DatabaseProxyException(exceptionText) 
    self.updateDatabase('call addValueType(:id,:name,:desc,:type,:score,:rat)',{'id':valueTypeId,'name':vtName,'desc':vtDesc,'type':vtType,'score':vtScore,'rat':vtRat},'MySQL error adding value type')
    return valueTypeId

  def updateValueType(self,parameters):
    valueTypeId = parameters.id()
    vtName = parameters.name()
    vtDesc = parameters.description()
    vtType = parameters.type()
    envName = parameters.environment()
    vtScore = parameters.score()
    vtRat = parameters.rationale()
    self.updateDatabase('call updateValueType(:id,:name,:desc,:type,:env,:score,:rat)',{'id':valueTypeId,'name':vtName,'desc':vtDesc,'type':vtType,'env':envName,'score':vtScore,'rat':vtRat},'MySQL error updating value type')

  def threatTypes(self,envName = ''):
    rows = self.responseList('call threatTypes(:env)',{'env':envName},'MySQL error getting threat types')
    stats = {}
    for key,value in rows:
      stats[row[0]] = row[1]
    return stats

  def inheritedAssetProperties(self,assetId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    syProperties,pRationale = self.relatedProperties('asset',assetId,environmentId)
    assetAssociations = self.assetAssociations(assetId,environmentId)
    return AssetEnvironmentProperties(environmentName,syProperties,pRationale,assetAssociations)

  def inheritedAttackerProperties(self,attackerId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    roles = self.dimensionRoles(attackerId,environmentId,'attacker')
    capabilities = self.attackerCapabilities(attackerId,environmentId)
    motives = self.attackerMotives(attackerId,environmentId)
    return AttackerEnvironmentProperties(environmentName,roles,motives,capabilities)

  def inheritedThreatProperties(self,threatId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    likelihood = self.threatLikelihood(threatId,environmentId)
    assets = self.threatenedAssets(threatId,environmentId) 
    attackers = self.threatAttackers(threatId,environmentId)
    syProperties,pRationale = self.relatedProperties('threat',threatId,environmentId)
    return ThreatEnvironmentProperties(environmentName,likelihood,assets,attackers,syProperties,pRationale)

  def inheritedVulnerabilityProperties(self,vulId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    severity = self.vulnerabilitySeverity(vulId,environmentId)
    assets = self.vulnerableAssets(vulId,environmentId)
    return VulnerabilityEnvironmentProperties(environmentName,severity,assets)

  def inheritedTaskProperties(self,taskId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    dependencies = self.taskDependencies(taskId,environmentId)
    personas = self.taskPersonas(taskId,environmentId)
    assets = self.taskAssets(taskId,environmentId)
    concs = self.taskConcernAssociations(taskId,environmentId)
    narrative = self.taskNarrative(taskId,environmentId)
    return TaskEnvironmentProperties(environmentName,dependencies,personas,assets,concs,narrative)

  def inheritedUseCaseProperties(self,ucId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    preConds,postConds = self.useCaseConditions(ucId,environmentId)
    ucSteps = self.useCaseSteps(ucId,environmentId)
    return UseCaseEnvironmentProperties(environmentName,preConds,ucSteps,postConds)

  def inheritedGoalProperties(self,goalId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    goalDef = self.goalDefinition(goalId,environmentId)
    goalType = self.goalCategory(goalId,environmentId)
    goalPriority = self.goalPriority(goalId,environmentId)
    goalFitCriterion = self.goalFitCriterion(goalId,environmentId)
    goalIssue = self.goalIssue(goalId,environmentId) 
    concs = self.goalConcerns(goalId,environmentId)
    cas = self.goalConcernAssociations(goalId,environmentId)
    goalRefinements,subGoalRefinements = self.goalRefinements(goalId,environmentId)
    return GoalEnvironmentProperties(environmentName,'',goalDef,goalType,goalPriority,goalFitCriterion,goalIssue,goalRefinements,subGoalRefinements,concs,cas)

  def inheritedObstacleProperties(self,obsId,environmentName):
    environmentId = self.getDimensionId(environmentName,'environment')
    obsDef = self.obstacleDefinition(obsId,environmentId)
    obsType = self.obstacleCategory(obsId,environmentId)
    goalRefinements,subGoalRefinements = self.goalRefinements(obsId,environmentId)
    return ObstacleEnvironmentProperties(environmentName,'',obsDef,obsType,goalRefinements,subGoalRefinements)

  def getVulnerabilityDirectory(self,vulName = ''):
    return self.responseList('call getVulnerabilityDirectory(:vuln)',{'vuln':vulName},'MySQL error getting vulnerability directory')

  def getThreatDirectory(self,thrName = ''):
    return self.responseList('call getThreatDirectory(:threat)',{'threat':thrName},'MySQL error getting threat directory')

  def reassociateAsset(self,assetName,envName,reqId):
    self.updateDatabase('call reassociateAsset(:ass,:env,:req)',{'ass':assetName,'env':envName,'req':reqId},'MySQL error reassociating asset')

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

  def reportAssociationDependencies(self,fromAsset,toAsset,envName):
    return self.responseList('call associationDependencyCheck(:from,:to,:env)',{'from':fromAsset,'to':toAsset,'env':envName},'MySQL error reporting association dependencies')

  def reportAssociationTargetDependencies(self,assetProperties,toAsset,envName):
    return self.responseList('call associationTargetDependencyCheck(:a0,:a1,:a2,:a3,:a4,:a5,:a6,:a7,:to,:env)',{'a0':assetProperties[0],'a1':assetProperties[1],'a2':assetProperties[2],'a3':assetProperties[3],'a4':assetProperties[4],'a5':assetProperties[5],'a6':assetProperties[6],'a7':assetProperties[7],'to':toAsset,'env':envName},'MySQL error reporting association target dependencies')

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
    try:
      session = self.conn()
      session.execute('call deleteSecurityPatternComponents(:pat)',{'pat':patternId})
      session.execute('call updateSecurityPattern(:id,:name,:cont,:prob,:sol)',{'id':patternId,'name':patternName,'cont':patternContext,'prob':patternProblem,'sol':patternSolution})
      session.commit()
      session.close()
      self.addPatternStructure(patternId,patternStructure)
      self.addPatternRequirements(patternId,patternRequirements)
      return patternId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating security pattern  ' + patternName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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

  def isCountermeasureAssetGenerated(self,cmId):
    return self.responseList('select isCountermeasureAssetGenerated(:cm)',{'cm':cmId},'MySQL error checking assets associated with countermeasure')[0]

  def isCountermeasurePatternGenerated(self,cmId):
    return self.responseList('select isCountermeasurePatternGenerated(:cm)',{'cm':cmId},'MySQL error checking patterns associated with countermeasure')[0]


  def exposedCountermeasures(self,parameters):
    objtId = parameters.id()
    expCMs = []
    for cProperties in parameters.environmentProperties():
      envName = cProperties.name()
      expAssets = cProperties.assets()
      for expAsset in expAssets:
        expCMs += self.exposedCountermeasure(envName,expAsset)
    return expCMs

  def exposedCountermeasure(self,envName,assetName):
    rows = self.responseList('call exposedCountermeasure(:env,:ass)',{'env':envName,'ass':assetName},'MySQL error checking countermeasures exposed by ' + assetName)
    expCMs = []
    for r1, r2 in rows:
      expCMs.append((envName,r1,assetName,r2))
    return expCMs
  
  def updateCountermeasuresEffectiveness(self,objtId,dimName,expCMs):
    for envName,cmName,assetName,cmEffectiveness in expCMs:
      self.updateCountermeasureEffectiveness(objtId,dimName,cmName,assetName,envName,cmEffectiveness) 

  def updateCountermeasureEffectiveness(self,objtId,dimName,cmName,assetName,envName,cmEffectiveness):
    self.updateDatabase('call updateCountermeasureEffectiveness(:obj,:dim,:cm,:ass,:env,:cmEff)',{'obj':objtId,'dim':dimName,'cm':cmName,'ass':assetName,'env':envName,'cmEff':cmEffectiveness},'MySQL error updating effectiveness of countermeasure ' + cmName)

  def countermeasurePatterns(self,cmId):
    return self.responseList('call countermeasurePatterns(:cm)',{'cm':cmId},'MySQL error getting patterns associated with countermeasure')

  def deleteSituatedPattern(self,cmId,patternName):
    self.updateDatabase('call deleteSituatedPattern(:cm,:pat)',{'cm':cmId,'pat':patternName},'MySQL deleting situated pattern')

  def candidateCountermeasurePatterns(self,cmId):
    return self.responseList('call candidateCountermeasurePatterns(:cm)',{'cm':cmId},'MySQL error getting candidate countermeasure patterns')

  def associateCountermeasureToPattern(self,cmId,patternName):
    self.updateDatabase('call associateCountermeasureToPattern(:cm,:pat)',{'cm':cmId,'pat':patternName},'MySQL error associating countermeasure to pattern')

  def nameCheck(self,objtName,dimName):
    objtCount = self.responseList('call nameExists(:obj,:dim)',{'obj':objtName,'dim':dimName},'MySQL error checking existence of ' + dimName + ' ' + objtName)[0]
    if (objtCount > 0):
      exceptionText = dimName + ' ' + objtName + ' already exists.'
      raise ARMException(exceptionText) 
   

  def nameCheckEnvironment(self,objtName,envName,dimName):
    objtCount = self.responseList('call nameEnvironmentExists(:obj,:env,:dim)',{'obj':objtName,'env':envName,'dim':dimName},'MySQL error naming checking in environment')[0]
    if (objtCount > 0):
      exceptionText = dimName + ' ' + objtName + ' in environment ' + envName + ' already exists.'
      raise ARMException(exceptionText) 

  def nameExists(self,objtName,dimName):
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

  def getExternalDocumentReferences(self,docName = ''):
    drRows = self.responseList('call getDocumentReferencesByExternalDocument(:doc)',{'doc':docName},'MySQL error getting document references for external document ' + docName)
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
    docName = self.conn.connection().connection.escape_string(parameters.name().replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u2013", "-").replace(u"\u2022","*"))
    docVersion = parameters.version()
    docDate = self.conn.connection().connection.escape_string(parameters.date())
    docAuthors = self.conn.connection().connection.escape_string(parameters.authors())
    docDesc = self.conn.connection().connection.escape_string(parameters.description())
    self.updateDatabase('call addExternalDocument(:id,:name,:vers,:date,:auth,:desc)',{'id':docId,'name':docName.encode('utf-8'),'vers':docVersion.encode('utf-8'),'date':docDate.encode('utf-8'),'auth':docAuthors.encode('utf-8'),'desc':docDesc.encode('utf-8')},'MySQL error adding external document')
    return docId


  def updateExternalDocument(self,parameters):
    docId = parameters.id()
    docName = self.conn.connection().connection.escape_string(parameters.name())
    docVersion = parameters.version()
    docDate = self.conn.connection().connection.escape_string(parameters.date())
    docAuthors = self.conn.connection().connection.escape_string(parameters.authors())
    docDesc = self.conn.connection().connection.escape_string(parameters.description())
    self.updateDatabase('call updateExternalDocument(:id,:name,:vers,:date,:auth,:desc)',{'id':docId,'name':docName.encode('utf-8'),'vers':docVersion.encode('utf-8'),'date':docDate.encode('utf-8'),'auth':docAuthors.encode('utf-8'),'desc':docDesc.encode('utf-8')},'MySQL error updating external document')

  def addDocumentReference(self,parameters):
    refId = self.newId()
    refName = parameters.name()
    refName = self.conn.connection().connection.escape_string(parameters.name().replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u2013", "-").replace(u"\u2022","*"))
    refName = self.conn.connection().connection.escape_string(parameters.name().replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u2013", "-"))
    docName = self.conn.connection().connection.escape_string(parameters.document().replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u2013", "-").replace(u"\u2022","*"))
    cName = parameters.contributor()
    refExc = parameters.description()
    self.updateDatabase('call addDocumentReference(:rId,:rName,:dName,:cName,:rExec)',{'rId':refId,'rName':refName.encode('utf-8'),'dName':docName.encode('utf-8'),'cName':cName.encode('utf-8'),'rExec':refExc.encode('utf-8')},'MySQL error adding document reference')
    return refId

  def updateDocumentReference(self,parameters):
    refId = parameters.id()
    refName = parameters.name()
    docName = parameters.document()
    cName = parameters.contributor()
    refExc = parameters.description()
    self.updateDatabase('call updateDocumentReference(:rId,:rName,:dName,:cName,:rExec)',{'rId':refId,'rName':refName.encode('utf-8'),'dName':docName.encode('utf-8'),'cName':cName.encode('utf-8'),'rExec':refExc.encode('utf-8')},'MySQL error updating document reference')

  def addPersonaCharacteristic(self,parameters):
    pcId = self.newId()
    personaName = parameters.persona()
    qualName = parameters.qualifier()
    bVar = parameters.behaviouralVariable()
    cDesc = parameters.characteristic()
    grounds = parameters.grounds()
    warrant = parameters.warrant() 
    rebuttal = parameters.rebuttal()
    self.updateDatabase('call addPersonaCharacteristic(:pc,:pers,:qual,:bVar,:cDesc)',{'pc':pcId,'pers':personaName,'qual':qualName,'bVar':bVar,'cDesc':cDesc.encode('utf-8')},'MySQL error adding persona characteristic')
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
    try:
      session = self.conn()
      session.execute('call deletePersonaCharacteristicComponents(:pers)',{'pers':pcId})
      session.execute('call updatePersonaCharacteristic(:pc,:pers,:qual,:bVar,:cDesc)',{'pc':pcId,'pers':personaName,'qual':qualName,'bVar':bVar,'cDesc':cDesc.encode('utf-8')})
      session.commit()
      session.close()
      self.addPersonaCharacteristicReferences(pcId,grounds,warrant,rebuttal)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating persona characteristic ' + cDesc + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getPersonaBehaviouralCharacteristics(self,pName,bvName):
    rows = self.responseList('call personaBehaviouralCharacteristics(:pName,:bvName)',{'pName':pName,'bvName':bvName},'MySQL error getting persona behavioural characteristics')
    pChars = {}
    pcSumm = []
    for pcId, qualName, pcDesc in rows:
      pcSumm.append((pcId,pName,bvName,qualName,pcDesc))
    for pcId,pName,bvName,qualName,pcDesc in pcSumm:
      grounds,warrant,backing,rebuttal = self.characteristicReferences(pcId,'characteristicReferences')
      parameters = PersonaCharacteristicParameters(pName,qualName,bvName,pcDesc,grounds,warrant,backing,rebuttal)
      pChar = ObjectFactory.build(pcId,parameters)
      pChars[pName + '/' + bvName + '/' + pcDesc] = pChar
    return pChars

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
    self.updateDatabase('call addConceptReference(:rId,:rName,:dName,:obj,:cDesc)',{'rId':refId,'rName':refName,'dName':dimName,'obj':objtName,'cDesc':cDesc.encode('utf-8')},'MySQL error adding concept reference')
    return refId

  def updateConceptReference(self,parameters):
    refId = parameters.id()
    refName = parameters.name()
    dimName = parameters.dimension()
    objtName = parameters.objectName()
    cDesc = parameters.description()
    self.updateDatabase('call updateConceptReference(:rId,:rName,:dName,:obj,:cDesc)',{'rId':refId,'rName':refName,'dName':dimName,'obj':objtName,'cDesc':cDesc.encode('utf-8')},'MySQL error updating concept reference')
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
    self.updateDatabase('call addPersonaCharacteristicReference(:pc,:ref,:cr,:refD,:dim)',{'pc':pcId,'ref':refName,'cr':crTypeName,'refD':refDesc.encode('utf-8'),'dim':dimName},'MySQL error adding persona characteristic reference')

  def referenceDescription(self,dimName,refName):
    return self.responseList('call referenceDescription(:dim,:ref)',{'dim':dimName,'ref':refName},'MySQL error getting reference description')[0]
  
  def documentReferenceNames(self,docName):
    return self.responseList('call documentReferenceNames(:doc)',{'doc':docName},'MySQL error getting document reference names')

  def referenceUse(self,refName,dimName):
    return self.responseList('call referenceUse(:ref,:dim)',{'ref':refName,'dim':dimName},'MySQL error getting reference use')

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

  def getTaskGrounds(self,constraintName):
    return self.getArgReference('TaskGrounds',constraintName)

  def getTaskWarrant(self,constraintName):
    return self.getArgReference('TaskWarrant',constraintName)

  def getTaskRebuttal(self,constraintName):
    return self.getArgReference('TaskRebuttal',constraintName)


  def getArgReference(self,atName,constraintName):
    try:
      session = self.conn()
      rs = session.execute('call get' + atName + '(:const)',{'const':constraintName})
      groundsName = ''
      dimName = ''
      objtName = ''
      refDesc = ''
      for row in rs.fetchall():
        row = list(row)
        groundsName = row[0] 
        dimName = row[1]
        objtName = row[2]
        refDesc = row[3]
      rs.close()
      session.close()   
      return (dimName,objtName,refDesc) 
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting ' + atName + ':' + constraintName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addThreatDirectory(self,tDir,isOverwrite = 1):
    self.addDirectory(tDir,'threat',isOverwrite)

  def addVulnerabilityDirectory(self,vDir,isOverwrite = 1):
    self.addDirectory(vDir,'vulnerability',isOverwrite)

  def addDirectory(self,gDir,dimName,isOverwrite):
    try:
      if (isOverwrite):
        self.deleteObject(-1,dimName + '_directory')
      for dLabel,dName,dDesc,dType,dRef in gDir:
        dTypeId = self.getDimensionId(dType,dimName + '_type')
        self.addDirectoryEntry(dLabel,dName,dDesc,dTypeId,dRef,dimName)
      
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error importing ' + dimName + ' directory (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addDirectoryEntry(self,dLabel,dName,dDesc,dTypeId,dRef,dimName):
    try:
      dimName = string.upper(dimName[0]) + dimName[1:]
      session = self.conn()
      session.execute('call add' + dimName + 'DirectoryEntry(:lbl,:name,:desc,:type,:ref)',{'lbl':dLabel,'name':dName,'desc':dDesc.encode('utf-8'),'type':dTypeId,'ref':dRef})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error importing ' + dimName + ' directory entry ' + dLabel + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def lastRequirementLabel(self,assetName):
    return self.responseList('select lastRequirementLabel(:ass)',{'ass':assetName},'MySQL error getting last requirement label')[0]

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
    ucName = parameters.name()
    ucAuth = parameters.author()
    ucCode = parameters.code()
    ucActors = parameters.actors()
    ucDesc = parameters.description()
    tags = parameters.tags()
    try:
      ucId = self.newId()
      session = self.conn()
      session.execute('call addUseCase(:id,:name,:auth,:code,:desc)',{'id':ucId,'name':ucName,'auth':ucAuth,'code':ucCode,'desc':ucDesc})
      session.commit()
      session.close()
      for actor in ucActors:
        self.addUseCaseRole(ucId,actor)
      self.addTags(ucName,'usecase',tags)

      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(ucId,'usecase',environmentName)
        self.addUseCaseConditions(ucId,environmentName,cProperties.preconditions(),cProperties.postconditions())
        self.addUseCaseSteps(ucId,environmentName,cProperties.steps())
      return ucId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding use case ' + ucName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addUseCaseRole(self,ucId,actor):
    try:
      session = self.conn()
      session.execute('call addUseCaseRole(:id,:act)',{'id':ucId,'act':actor}) 
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating actor' + actor + ' with use case id ' + str(ucId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addUseCaseConditions(self,ucId,envName,preCond,postCond):
    try:
      session = self.conn()
      session.execute('call addUseCaseConditions(:id,:env,:pre,:post)',{'id':ucId,'env':envName,'pre':preCond,'post':postCond}) 
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding conditions to use case id ' + str(ucId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addUseCaseSteps(self,ucId,envName,steps):
    for pos,step in enumerate(steps.theSteps):
      stepNo = pos + 1
      self.addUseCaseStep(ucId,envName,stepNo,step)

  def addUseCaseStep(self,ucId,envName,stepNo,step):
    try:
      session = self.conn()
      session.execute('call addUseCaseStep(:id,:env,:step,:text,:synopsis,:actor,:type)',{'id':ucId,'env':envName,'step':stepNo,'text':step.text(),'synopsis':step.synopsis(),'actor':step.actor(),'type':step.actorType()}) 
      session.commit()
      session.close()
      for tag in step.tags():
        self.addUseCaseStepTag(ucId,envName,stepNo,tag)

      for idx,exc in (step.theExceptions).iteritems():
        self.addUseCaseStepException(ucId,envName,stepNo,exc[0],exc[1],exc[2],exc[3],exc[4])
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding step: ' + step.text() + ' to use case id ' + str(ucId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addUseCaseStepTag(self,ucId,envName,stepNo,tag):
    try:
      session = self.conn()
      session.execute('call addUseCaseStepTag(:id,:env,:step,:tag)',{'id':ucId,'env':envName,'step':stepNo,'tag':tag})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding tag ' + tag + ' to use case id ' + str(ucId) + ' step ' + str(stepNo) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addUseCaseStepException(self,ucId,envName,stepNo,exName,dimType,dimName,catName,exDesc):
    try:
      session = self.conn()
      session.execute('call addUseCaseStepException(:uc,:env,:step,:ex,:dType,:dName,:cName,:desc)',{'uc':ucId,'env':envName,'step':stepNo,'ex':exName,'dType':dimType,'dName':dimName,'cName':catName,'desc':exDesc})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding step exception ' + exName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateUseCase(self,parameters):
    ucId = parameters.id()
    ucName = parameters.name()
    ucAuth = parameters.author()
    ucCode = parameters.code()
    ucActors = parameters.actors()
    ucDesc = parameters.description()
    tags = parameters.tags()
    try:
      session = self.conn()
      session.execute('call deleteUseCaseComponents(:uc)',{'uc':ucId})
      session.execute('call updateUseCase(:id,:name,:auth,:code,:desc)',{'id':ucId,'name':ucName,'auth':ucAuth,'code':ucCode,'desc':ucDesc})
      session.commit()
      session.close()
      for actor in ucActors:
        self.addUseCaseRole(ucId,actor)
      self.addTags(ucName,'usecase',tags)
      for cProperties in parameters.environmentProperties():
        environmentName = cProperties.name()
        self.addDimensionEnvironment(ucId,'usecase',environmentName)
        self.addUseCaseConditions(ucId,environmentName,cProperties.preconditions(),cProperties.postconditions())
        self.addUseCaseSteps(ucId,environmentName,cProperties.steps())
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating use case ' + ucName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteUseCase(self,ucId):
    self.deleteObject(ucId,'usecase')
    

  def riskModel(self,environmentName,riskName):
    rows = self.responseList('call riskModel(:risk,:env)',{'risk':riskName,'env':environmentName},'MySQL error getting risk model')
    traces = []
    for fromObjt,fromName,toObjt,toName in rows:
      parameters = DotTraceParameters(fromObjt,fromName,toObjt,toName)
      traces.append(ObjectFactory.build(-1,parameters))
    return traces

  def isRisk(self,candidateRiskName):
    return self.responseList('select is_risk(:cand)',{'cand':candidateRiskName},'MySQL error checking candidate risk')[0]

  def textualArgumentationModel(self,personaName,bvType):
    return self.responseList('call assumptionPersonaModel_textual(:pers,:type)',{'pers':personaName,'type':bvType},'MySQL error getting textual argumentation model')

  def riskAnalysisToXml(self,includeHeader=True):
    return self.responseList('call riskAnalysisToXml(:head)',{'head':includeHeader},'MySQL error exporting risk analysis artifacts to XML')[0]

  def goalsToXml(self,includeHeader=True):
    return self.responseList('call goalsToXml(:head)',{'head':includeHeader},'MySQL error exporting goals to XML')[0]

  def usabilityToXml(self,includeHeader=True):
    return self.responseList('call usabilityToXml(:head)',{'head':includeHeader},'MySQL error exporting usability data to XML')[0]

  def misusabilityToXml(self,includeHeader=True):
    return self.responseList('call misusabilityToXml(:head)',{'head':includeHeader},'MySQL error exporting misusability data to XML')[0]

  def associationsToXml(self,includeHeader=True):
    return self.responseList('call associationsToXml(:head)',{'head':includeHeader},'MySQL error exporting association data to XML')[0]

  def dataflowsToXml(self,includeHeader=True):
    return self.responseList('call dataflowsToXml(:head)',{'head':includeHeader},'MySQL error exporting dataflow data to XML')[0]

  def projectToXml(self,includeHeader=True):
    return self.responseList('call projectToXml(:head)',{'head':includeHeader},'MySQL error exporting project data to XML')[0]

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
    try:
      session = self.conn()
      session.execute('call addTaskCharacteristic(:id,:task,:qual,:desc)',{'id':tcId,'task':taskName,'qual':qualName,'desc':cDesc})
      session.commit()
      session.close()
      self.addTaskCharacteristicReferences(tcId,grounds,warrant,rebuttal)
      return tcId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding task characteristic ' + cDesc + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addTaskCharacteristicReferences(self,tcId,grounds,warrant,rebuttal):
    for g,desc,dim in grounds:
      self.addTaskCharacteristicReference(tcId,g,'grounds',desc.encode('utf-8'),dim)

    for w,desc,dim in warrant:
      self.addTaskCharacteristicReference(tcId,w,'warrant',desc.encode('utf-8'),dim)

    for r,desc,dim in rebuttal:
      self.addTaskCharacteristicReference(tcId,r,'rebuttal',desc.encode('utf-8'),dim)


  def addTaskCharacteristicReference(self,tcId,refName,crTypeName,refDesc,dimName):
    try:
      session = self.conn()
      session.execute('call addTaskCharacteristicReference(:id,:ref,:type,:desc,:dim)',{'id':tcId,'ref':refName,'type':crTypeName,'desc':refDesc,'dim':dimName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding ' + crTypeName + ' ' + refName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def updateTaskCharacteristic(self,parameters):
    tcId = parameters.id()
    taskName = parameters.task()
    qualName = parameters.qualifier()
    cDesc = parameters.characteristic()
    grounds = parameters.grounds()
    warrant = parameters.warrant() 
    rebuttal = parameters.rebuttal()
    try:
      session = self.conn()
      session.execute('call deleteTaskCharacteristicComponents(:task)',{'task':tcId})
      session.execute('call updateTaskCharacteristic(:id,:task,:qual,:desc)',{'id':tcId,'task':taskName,'qual':qualName,'desc':cDesc})
      session.commit()
      session.close()
      self.addTaskCharacteristicReferences(tcId,grounds,warrant,rebuttal)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating task characteristic ' + cDesc + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteTaskCharacteristic(self,pcId = -1):
    self.deleteObject(pcId,'task_characteristic')
    

  def assumptionTaskModel(self,taskName = '',tcName = ''):
    return self.responseList('call assumptionTaskModel(:task,:tc)',{'task':taskName,'tc':tcName},'MySQL error getting assumption task model')

  def getTaskSpecificCharacteristics(self,tName):
    rows = self.responseList('call taskSpecificCharacteristics(:task)',{'task':tName},'MySQL error getting task specific characteristics')
    tChars = {}
    tcSumm = []
    for tcId,qualName,tcDesc in rows:
      tcSumm.append((tcId,tName,qualName,tcDesc))
    for tcId,tName,qualName,tcDesc in tcSumm:
      grounds,warrant,backing,rebuttal = self.characteristicReferences(tcId,'taskCharacteristicReferences')
      parameters = TaskCharacteristicParameters(tName,qualName,tcDesc,grounds,warrant,backing,rebuttal)
      tChar = ObjectFactory.build(tcId,parameters)
      tChars[tName + '/' + tcDesc] = tChar
    return tChars

  def prettyPrintGoals(self,categoryName):
    try:
      session = self.conn()
      rs = session.execute('call goalsPrettyPrint(:category)',{'category':categoryName})
      row = rs.fetchone()
      buf = row[0] 
      rs.close()
      session.close()
      return buf
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL pretty printing goals (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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

  def getExternalDocumentReferencesByExternalDocument(self,edName):
    return self.responseList('call getExternalDocumentReferences(:name)',{'name':edName},'MySQL error external document references')

  def dimensionNameByShortCode(self,scName):
    return self.responseList('call dimensionNameByShortCode(:shortCode)',{'shortCode':scName},'MySQL error calling dimension name by short code')

  def misuseCaseRiskComponents(self,mcName):
    return self.responseList('call misuseCaseRiskComponents(:misuse)',{'misuse':mcName},'MySQL error getting risk components associated with misuse case ' + mcName)[0]

  def personaToXml(self,pName):
    return self.responseList('call personaToXml(:persona)',{'persona':pName},'MySQL error exporting persona to XML')[0]

  def defaultEnvironment(self):
    return self.responseList('select defaultEnvironment()',{},'MySQL error obtaining default environment')[0]

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
    try:
      session = self.conn()
      rs = session.execute('call getReferenceSynopsis(:ref)',{'ref':refName})
      row = rs.fetchone()
      rsId = row[0]
      synName = row[1]
      dimName = row[2]
      aType = row[3]
      aName = row[4]
      rs.close()
      session.close()
      rs = ReferenceSynopsis(rsId,refName,synName,dimName,aType,aName)
      return rs 
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting synopsis for reference ' + refName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getReferenceContribution(self,charName,refName):
    try:
      session = self.conn()
      rs = session.execute('call getReferenceContribution(:ref,:char)',{'ref':refName,'char':charName})
      row = rs.fetchone()
      rsName = row[0]
      csName = row[1]
      me = row[2]
      cont = row[3]
      rs.close()
      session.close()
      rc = ReferenceContribution(rsName,csName,me,cont)
      return rc
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting contribution for reference ' + refName + ' and characteristic ' + charName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addReferenceContribution(self,rc):
    rsName = rc.source()
    csName = rc.destination()
    meName = rc.meansEnd()
    contName = rc.contribution()
    try:
      session = self.conn()
      session.execute('call addReferenceContribution(:rs,:cs,:me,:cont)',{'rs':rsName,'cs':csName,'me':meName,'cont':contName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding contribution for reference synopsis ' + rsName + ' and characteristic synopsis ' + csName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateReferenceContribution(self,rc):
    rsName = rc.source()
    csName = rc.destination()
    meName = rc.meansEnd()
    contName = rc.contribution()
    try:
      session = self.conn()
      session.execute('call updateReferenceContribution(:rs,:cs,:me,:cont)',{'rs':rsName,'cs':csName,'me':meName,'cont':contName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating contribution for reference synopsis ' + rsName + ' and characteristic synopsis ' + csName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addReferenceSynopsis(self,rs):
    rsId = self.newId()
    refName = rs.reference()
    rsName = rs.synopsis()
    rsDim = rs.dimension()
    atName = rs.actorType()
    actorName = rs.actor()
    try:
      session = self.conn()
      session.execute('call addReferenceSynopsis(:rsId,:ref,:rs,:dim,:atName,:actName)',{'rsId':rsId,'ref':refName,'rs':rsName,'dim':rsDim,'atName':atName,'actName':actorName})
      session.commit()
      session.close()
      return rsId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding synopsis ' + rsName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateReferenceSynopsis(self,rs):
    rsId = rs.id()
    refName = rs.reference()
    rsName = rs.synopsis()
    rsDim = rs.dimension()
    atName = rs.actorType()
    actorName = rs.actor()
    try:
      session = self.conn()
      session.execute('call updateReferenceSynopsis(:rsId,:ref,:rs,:dim,:atName,:actName)',{'rsId':rsId,'ref':refName,'rs':rsName,'dim':rsDim,'atName':atName,'actName':actorName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating synopsis ' + rsName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addCharacteristicSynopsis(self,cs):
    cName = cs.reference()
    csName = cs.synopsis()
    csDim = cs.dimension()
    atName = cs.actorType()
    actorName = cs.actor()
    try:
      session = self.conn()
      session.execute('call addCharacteristicSynopsis(:cName,:csName,:csDim,:atName,:actName)',{'cName':cName,'csName':csName,'csDim':csDim,'atName':atName,'actName':actorName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding synopsis ' + csName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateCharacteristicSynopsis(self,cs):
    cName = cs.reference()
    csName = cs.synopsis()
    csDim = cs.dimension()
    atName = cs.actorType()
    actorName = cs.actor()
    try:
      session = self.conn()
      session.execute('call updateCharacteristicSynopsis(:cName,:csName,:csDim,:atName,:actName)',{'cName':cName,'csName':csName,'csDim':csDim,'atName':atName,'actName':actorName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating synopsis ' + csName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def referenceCharacteristic(self,refName):
    return self.responseList('call referenceCharacteristic(:ref)',{'ref':refName},'MySQL error getting characteristics associated with reference ' + refName)

  def getCharacteristicSynopsis(self,cName):
    try:
      session = self.conn()
      rs = session.execute('call getCharacteristicSynopsis(:characteristic)',{'characteristic':cName})
      row = rs.fetchone()
      synName = row[0]
      dimName = row[1]
      aType = row[2]
      aName = row[3]
      if synName == '':
        synId = -1
      else:
        synId = 0
      rs.close()
      session.close()
      rs = ReferenceSynopsis(synId,cName,synName,dimName,aType,aName)
      return rs 
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting synopsis for characteristic ' + cName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def hasCharacteristicSynopsis(self,charName):
    try:
      session = self.conn()
      rs = session.execute('select hasCharacteristicSynopsis(:characteristic)',{'characteristic':charName})
      row = rs.fetchone()
      hs = row[0]
      rs.close()
      session.close()
      return hs
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error finding synopsis for characteristic ' + charName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def hasReferenceSynopsis(self,refName):
    try:
      session = self.conn()
      rs = session.execute('select hasReferenceSynopsis(:ref)',{'ref':refName})
      row = rs.fetchone()
      hs = row[0]
      rs.close()
      session.close()
      return hs
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error finding synopsis for reference ' + refName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addUseCaseSynopsis(self,cs):
    cName = cs.reference()
    csName = cs.synopsis()
    csDim = cs.dimension()
    atName = cs.actorType()
    actorName = cs.actor()
    try:
      session = self.conn()
      session.execute('call addUseCaseSynopsis(:cName,:csName,:csDim,:atName,:actName)',{'cName':cName,'csName':csName,'csDim':csDim,'atName':atName,'actName':actorName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding synopsis ' + csName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
      session = self.conn()
      session.execute('call addUseCaseContribution(:useCase,:csName,:meName,:cont)',{'useCase':ucName,'csName':csName,'meName':meName,'cont':contName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding contribution for use case ' + ucName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateUseCaseContribution(self,rc):
    ucName = rc.source()
    csName = rc.destination()
    meName = rc.meansEnd()
    contName = rc.contribution()
    try:
      session = self.conn()
      session.execute('call updateUseCaseContribution(:useCase,:csName,:meName,:cont)',{'useCase':ucName,'csName':csName,'meName':meName,'cont':contName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating contribution for use case ' + ucName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def pcToGrl(self,pNames,tNames,envName):
    try:
      session = self.conn()
      rs = session.execute('call pcToGrl(":pNames", ":tNames", :env)',{'pNames':pNames,'tNames':tNames,'env':envName})
      row = rs.fetchone()
      buf = row[0]
      rs.close()
      session.close()
      return buf
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL exporting persona and task to GRL (id:' + str(id) + ',message:' + msg + ')'

  def getEnvironmentGoals(self,goalName,envName):
    goalRows = self.responseList('call getEnvironmentGoals(:goal,:env)',{'goal':goalName,'env':envName},'MySQL error getting goals')
    oals = []
    for goalId,goalName,goalOrig in goalRows:
      environmentProperties = self.goalEnvironmentProperties(goalId)
      parameters = GoalParameters(goalName,goalOrig,[],self.goalEnvironmentProperties(goalId))
      goal = ObjectFactory.build(goalId,parameters)
      goals.append(goal)
    return goals

  def updateEnvironmentGoal(self,g,envName):
    envProps = g.environmentProperty(envName)
    goalDef = envProps.definition()
    goalCat = envProps.category()
    goalPri = envProps.priority()
    goalFc = envProps.fitCriterion()
    goalIssue = envProps.issue()
    
    try:
      session = self.conn()
      session.execute('call updateEnvironmentGoal(:id,:env,:name,:orig,:def,:cat,:pri,:fc,:issue)',{'id':g.id(),'env':envName,'name':g.name(),'orig':g.originator(),'def':goalDef,'cat':goalCat,'pri':goalPri,'fc':goalFc,'issue':goalIssue})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL adding updating goal ' + str(g.id()) + '(id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 
 
  def getSubGoalNames(self,goalName,envName):
    rows = ['']
    rows += self.responseList('call subGoalNames(:goal,:env)',{'goal':goalName,'env':envName},'MySQL error getting sub goal names')
    return rows

  def dependentLabels(self,goalName,envName):
    return self.responseList('call dependentLabels(:goal,:env)',{'goal':goalName,'env':envName},'MySQL error getting dependent labels')

  def goalEnvironments(self,goalName):
    rows = ['']
    rows += self.responseList('call goalEnvironments(:goal)',{'goal':goalName},'MySQL error getting goal environments')
    return rows

  def obstacleEnvironments(self,obsName):
    rows = ['']
    rows += self.responseList('call obstacleEnvironments(:obs)',{'obs':obsName},'MySQL error getting obstacle environments')
    return rows

  def getSubObstacleNames(self,obsName,envName):
    rows = ['']
    rows += self.responseList('call subObstacleNames(:obs,:env)',{'obs':obsName,'env':envName},'MySQL error getting sub obstacle names')
    return rows

  def getEnvironmentObstacles(self,obsName,envName):
    obsRows = self.responseList('call getEnvironmentObstacles(:obs,:env)',{'obs':obsName,'env':envName},'MySQL error getting obstacles')
    obs = []
    for obsId,obsName,obsOrig in obsRows:
      environmentProperties = self.obstacleEnvironmentProperties(obsId)
      parameters = ObstacleParameters(obsName,obsOrig,self.obstacleEnvironmentProperties(obsId))
      obstacle = ObjectFactory.build(obsId,parameters)
      obs.append(obstacle)
    return obs

  def updateEnvironmentObstacle(self,o,envName):
    envProps = o.environmentProperty(envName)
    obsDef = envProps.definition()
    obsCat = envProps.category()
    
    try:
      session = self.conn()
      session.execute('call updateEnvironmentObstacle(:id,:env,:name,:orig,:def,:cat)',{'id':o.id(),'env':envName,'name':o.name(),'orig':o.originator(),'def':obsDef,'cat':obsCat})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL adding updating obstacle ' + str(o.id()) + '(id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 

  def relabelGoals(self,envName):
    try:
      session = self.conn()
      session.execute('call relabelGoals(:env)',{'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting labelled goals (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def relabelObstacles(self,envName):
    try:
      session = self.conn()
      session.execute('call relabelObstacles(:env)',{'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting labelled obstacles (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def obstacleLabel(self,goalId,environmentId):
    try:
      session = self.conn()
      rs = session.execute('select obstacle_label(:goal,:env)',{'goal':goalId,'env':environmentId})
      row = rs.fetchone()
      goalAttr = row[0] 
      rs.close()
      session.close()
      return goalAttr
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting label for obstacle id ' + str(goalId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getLabelledGoals(self,envName):
    goalRows = self.responseList('call getEnvironmentGoals(:goal,:env)',{'goal':'','env':envName},'MySQL error getting labelled goals')
    goals = {}
    for goalId,goalName,goalOrig in goalRows:
      environmentProperties = self.goalEnvironmentProperties(goalId)
      parameters = GoalParameters(goalName,goalOrig,[],self.goalEnvironmentProperties(goalId))
      g = ObjectFactory.build(goalId,parameters)
      lbl = g.label(envName)
      goals[lbl] = g
    lbls = goals.keys()
    lbls.sort(key=lambda x: [int(y) for y in x.split('.')])
    return lbls,goals

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
    lbls = goals.keys()
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

  def domainValuesToXml(self,includeHeader=True):
    return self.responseList('call domainValuesToXml(:head)',{'head':includeHeader},'MySQL error exporting domain values to XML')[0]

  def clearDatabase(self,session_id = None):
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
      dbUser = ses_settings['dbUser']
      dbPasswd = ses_settings['dbPasswd']
      dbName = ses_settings['dbName']
    else:
      raise RuntimeError('Run mode not recognized')
    db_proxy.close()
    srcDir = b.cairisRoot + '/sql'
    initSql = srcDir + '/init.sql'
    procsSql = srcDir + '/procs.sql'
    cmd = '/usr/bin/mysql -h ' + dbHost + ' --port=' + str(dbPort) + ' --user ' + dbUser + ' --password=\'' + dbPasswd + '\'' + ' --database ' + dbName + ' < ' + initSql
    os.system(cmd)
    cmd = '/usr/bin/mysql -h ' + dbHost + ' --port=' + str(dbPort) + ' --user ' + dbUser + ' --password=\'' + dbPasswd + '\'' + ' --database ' + dbName + ' < ' + procsSql
    os.system(cmd)
    db_proxy.reconnect(False, session_id)


  def conceptMapModel(self,envName,reqName = ''):
    callTxt = 'call parameterisedConceptMapModel(:env,:req)'
    argDict = {'env':envName,'req':reqName}
    if reqName == '':
      callTxt = 'call conceptMapModel(:env)'
      argDict = {'env':envName}
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

  def addTag(self,tagObjt,tagName,tagDim, curs):
    try:
      curs.execute('call addTag(%s,%s,%s)',[tagObjt,tagName,tagDim])
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding tag ' + tagName + ' to ' + tagDim + ' ' + tagObjt +  ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteTags(self,tagObjt,tagDim):
    try:
      session = self.conn()
      session.execute('call deleteTags(:obj,:dim)',{'obj':tagObjt,'dim':tagDim})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error deleting tags from ' + tagDim + ' ' + tagObjt +  ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addTags(self,dimObjt,dimName,tags):
    try:
      self.deleteTags(dimObjt,dimName)
      curs = self.conn.connection().connection.cursor()
      for tag in tags:
        self.addTag(dimObjt,tag,dimName, curs)
      curs.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error deleting tags from ' + dimName + ' ' + dimObjt +  ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getTags(self,dimObjt,dimName):
    return self.responseList('call getTags(:obj,:name)',{'obj':dimObjt,'name':dimName},'MySQL error getting tags')

  def deleteTag(self,tagId):
    self.deleteObject(tagId,'tag')
    

  def componentView(self,cvName):
    interfaces = self.responseList('call componentViewInterfaces(:cv)',{'cv':cvName},'MySQL error getting component view interfaces')
    connectors = self.componentViewConnectors(cvName)
    return (interfaces,connectors)


  def componentViewConnectors(self,cvName):
    return self.responseList('call componentViewConnectors(:cv)',{'cv':cvName},'MySQL error getting component view connectors')

  def addComponentToView(self,cId,cvId):
    self.updateDatabase('call addComponentToView(:cId,:cvId)',{'cId':cId,'cvId':cvId},'MySQL error adding component to view')

  def addComponent(self,parameters,cvId = -1):
    componentId = self.newId()
    componentName = parameters.name()
    componentDesc = parameters.description()
    structure = parameters.structure()
    requirements = parameters.requirements()
    goals = parameters.goals()
    assocs = parameters.associations()

    try:
      session = self.conn()
      session.execute('call addComponent(:id,:name,:desc)',{'id':componentId,'name':componentName,'desc':componentDesc})
      if cvId != -1:
        session.execute('call addComponentToView(:compId,:cvId)',{'compId':componentId,'cvId':cvId})
      session.commit()
      session.close()
      for ifName,ifType,arName,pName in parameters.interfaces():
        self.addComponentInterface(componentId,ifName,ifType,arName,pName)
      self.addComponentStructure(componentId,structure)
      self.addComponentRequirements(componentId,requirements)
      self.addComponentGoals(componentId,goals)
      self.addComponentAssociations(componentId,assocs)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding component ' + componentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateComponent(self,parameters,cvId = -1):
    componentId = parameters.id()
    componentName = parameters.name()
    componentDesc = parameters.description()
    structure = parameters.structure()
    requirements = parameters.requirements()
    goals = parameters.goals()
    assocs = parameters.associations()

    try:
      session = self.conn()
      session.execute('call deleteComponentComponents(:comp)',{'comp':componentId})
      if (componentId != -1):
        session.execute('call updateComponent(:id,:name,:desc)',{'id':componentId,'name':componentName,'desc':componentDesc})
      else:
        componentId = self.newId()
        session.execute('call addComponent(:id,:name,:desc)',{'id':componentId,'name':componentName,'desc':componentDesc})
      session.commit()   
      if cvId != -1:
        session.execute('call addComponentToView(:compId,:cvId)',{'compId':componentId,'cvId':cvId})
      session.commit()
      session.close()
      for ifName,ifType,arName,pName in parameters.interfaces():
        self.addComponentInterface(componentId,ifName,ifType,arName,pName)
      self.addComponentStructure(componentId,structure)
      self.addComponentRequirements(componentId,requirements)
      self.addComponentGoals(componentId,goals)
      self.addComponentAssociations(componentId,assocs)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding component ' + componentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addComponentInterface(self,componentId,ifName,ifType,arName,pName):
    try:
      session = self.conn()
      session.execute('call addComponentInterface(:compId,:ifName,:ifType,:arName,:pName)',{'compId':componentId,'ifName':ifName,'ifType':ifType,'arName':arName,'pName':pName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding interface ' + ifName + ' to component ' + str(componentId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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

    try:
      session = self.conn()
      session.execute('call addConnector(:connId,:cvName,:cName,:fName,:fRole,:fIf,:tName,:tIf,:tRole,:conAsset,:pName,:arName)',{'connId':connId,'cvName':cvName,'cName':cName,'fName':fromName,'fRole':fromRole,'fIf':fromIf,'tName':toName,'tIf':toIf,'tRole':toRole,'conAsset':conAsset,'pName':pName,'arName':arName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding connector ' + cName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getInterfaces(self,dimObjt,dimName):
    rows = self.responseList('call getInterfaces(:obj,:name)',{'obj':dimObjt,'name':dimName},'MySQL error getting interfaces')
    ifs = []
    for ifName,ifTypeId,arName,prName in rows:
      ifType = 'provided'
      if (ifTypeId == 1):
        ifType = 'required'
      ifs.append((ifName,ifType,arName,prName))
    return ifs

  def addInterfaces(self,dimObjt,dimName,ifs):
    try:
      self.deleteInterfaces(dimObjt,dimName)
      for ifName,ifType,arName,pName in ifs:
        self.addInterface(dimObjt,ifName,ifType,arName,pName,dimName)
    except _mysql_exceptions.DatabaseError, e:
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

  def addComponentRequirement(self,reqLabel,componentId,reqName):
    self.updateDatabase('call addComponentRequirement(:reqLbl,:comp,:req)',{'reqLbl':reqLabel,'comp':componentId,'req':reqName},'MySQL error adding component requirement')

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

    try:
      session = self.conn()
      session.execute('call addComponentView(:id,:name,:syn)',{'id':cvId,'name':cvName,'syn':cvSyn})
      session.commit()
      session.close()
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
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding component view (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateComponentView(self,parameters):
    cvId = parameters.id()
    cvName = parameters.name()
    cvSyn = parameters.synopsis()
    cvAssets = parameters.assets()
    cvReqs = parameters.requirements()
    cvComs = parameters.components()
    cvCons = parameters.connectors()

    try:
      session = self.conn()
      session.execute('call deleteComponentViewComponents(:id)',{'id':cvId})

      session.execute('call updateComponentView(:id,:name,:syn)',{'id':cvId,'name':cvName,'syn':cvSyn})
      session.commit()
      session.close()
      for taParameters in cvAssets:
        self.updateTemplateAsset(taParameters)
      for trParameters in cvReqs:
        self.updateTemplateRequirement(trParameters)
      for comParameters in cvComs:
        self.addComponent(comParameters,cvId)
      for conParameters in cvCons:
        self.addConnector(conParameters)
      return cvId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating component view (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteComponentView(self,cvId):
    self.deleteObject(cvId,'component_view')
    

  def componentViewComponents(self,cvId):
    return self.responseList('call getComponents(:id)',{'id':cvId},'MySQL error getting components')

  def componentViewWeaknesses(self,cvName,envName):
    try:
      session = self.conn()
      rs = session.execute('call componentViewWeaknesses(:cv,:env)',{'cv':cvName,'env':envName})
      thrDict = {}
      vulDict = {}
      for row in rs.fetchall():
        row = list(row)
        cName = row[0]
        taName = row[1]
        aName = row[2]
        targetName = row[3]
        targetType = row[4]
        t = None
        if targetType == 'threat':
          if targetName not in thrDict:
            t = WeaknessTarget(targetName)
          else:
            t = thrDict[targetName]
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
      rs.close()
      session.close()
      return (thrDict,vulDict)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting weaknesses associated with the ' + cvName + ' component view (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def componentAssets(self,cvName,reqName = ''):
    return self.responseList('call componentAssets(:cv,:req)',{'cv':cvName,'req':reqName},'MySQL error getting component assets')

  def componentGoalAssets(self,cvName,goalName = ''):
    return self.responseList('call componentGoalAssets(:cv,:goal)',{'cv':cvName,'goal':goalName},'MySQL error getting component goal assets')

  def existingObject(self,objtName,dimName):
    try:
      session = self.conn()
      existingSql = 'call existing_object("%s","%s")' %(objtName, dimName)
      if (dimName == 'persona_characteristic' or dimName == 'task_characteristic'):
        existingSql = 'call existing_characteristic("%s","%s")' %(objtName, dimName)
      rs = session.execute(existingSql)
      row = rs.fetchone()
      objtId = row[0]
      rs.close()
      session.close()
      return objtId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error checking the existence of ' + dimName + ' ' + objtName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def situateComponentView(self,cvName,envName,acDict,assetParametersList,targets,obstructParameters):
    try:
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
      for target in targets:
        self.addComponentViewTargets(target,envName)
      for op in obstructParameters:
        self.addGoalAssociation(op)
 
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error situating ' + cvName + ' component view in ' + envName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def situateComponentAsset(self,componentName,assetId):
    try:
      session = self.conn()
      session.execute('call situateComponentAsset(:ass,:comp)',{'ass':assetId,'comp':componentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error situating asset id ' + str(assetId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addComponentViewTargets(self,target,envName):
    try:
      session = self.conn()
      for componentName in target.components():
        session.execute('call addComponentTarget(:comp,:asset,:name,:effectiveness,:rationale,:env)',{'comp':componentName,'asset':target.asset(),'name':target.name(),'effectiveness':target.effectiveness(),'rationale':target.rationale(),'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error targetting  ' + target.name() + ' with components ' + ",".join(target.components()) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
      session = self.conn()
      session.execute('call addTemplateRequirement(:id,:name,:asset,:type,:desc,:rat,:fc)',{'id':reqId,'name':reqName,'asset':reqAsset,'type':reqType,'desc':reqDesc,'rat':reqRat,'fc':reqFC})
      session.commit()
      session.close()
      return reqId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding template requirement ' + reqName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateTemplateRequirement(self,parameters):
    reqId = parameters.id()
    reqName = parameters.name()
    reqAsset = parameters.asset()
    reqType = parameters.type()
    reqDesc = parameters.description()
    reqRat = parameters.rationale()
    reqFC = parameters.fitCriterion()
    try:
      session = self.conn()
      session.execute('call updateTemplateRequirement(:id,:name,:asset,:type,:desc,:rat,:fc)',{'id':reqId,'name':reqName,'asset':reqAsset,'type':reqType,'desc':reqDesc,'rat':reqRat,'fc':reqFC})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating template requirement ' + reqName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    

  def componentViewRequirements(self,cvName):
    return self.responseList('call componentViewRequirements(:cv)',{'cv':cvName},'MySQL error getting component view requirements')

  def componentViewGoals(self,cvName):
    return self.responseList('call componentViewGoals(:cv)',{'cv':cvName},'MySQL error getting component view goals')

  def situateComponentViewRequirements(self,cvName):
    try:
      session = self.conn()
      session.execute('call situateComponentViewRequirements(:cv)',{'cv':cvName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error situating requirements for component view ' + cvName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    for c1,c2 in rows:
      pImpact.append((c1,str(c2)))
    return pImpact

  def personaImpactRationale(self,cvName,personaName,envName):
    try:
      session = self.conn()
      rs = session.execute('call personaImpactRationale(:cv,:pers,:env)',{'cv':cvName,'pers':personaName,'env':envName})
      piRationale = {}
      for row in rs.fetchall():
        row = list(row)
        taskName = row[0] 
        durLabel = row[1]
        freqLabel = row[2]
        pdLabel = row[3]
        gcLabel = row[4]
        piRationale[taskName] = [durLabel,freqLabel,pdLabel,gcLabel]
      rs.close()
      session.close()
      for taskName in piRationale:
        ucDict = {}
        taskUseCases = self.taskUseCases(taskName)
        for ucName in taskUseCases:
          ucComs = self.usecaseComponents(ucName) 
          ucDict[ucName] = []
          for componentName in ucComs:
            ucDict[ucName].append(componentName)
        piRationale[taskName].append(ucDict) 
      return piRationale
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting rationale for persona impact (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def taskUseCases(self,taskName):
    return self.responseList('call taskUseCases(:task)',{'task':taskName},'MySQL error getting task use cases')

  def usecaseComponents(self,ucName):
    return self.responseList('call usecaseComponents(:useCase)',{'useCase':ucName},'MySQL error getting use case components')

  def attackSurfaceMetric(self,cvName):
    return self.responseList('call attackSurfaceMetric(:cv)',{'cv':cvName},'MySQL error getting attack surface metrics')[0]

  def componentAssetModel(self,componentName):
    try:
      session = self.conn()
      rs = session.execute('call componentClassModel(:comp)',{'comp':componentName})
      associations = {}
      for row in rs.fetchall():
        row = list(row)
        associationId = -1
        envName = ''
        headName = row[0]
        headDim  = 'template_asset'
        headNav =  row[2]
        headType = row[1]
        headMult = row[3]
        headRole = row[4]
        tailRole = row[5]
        tailMult = row[6]
        tailType = row[8]
        tailNav =  row[7]
        tailDim  = 'template_asset'
        tailName = row[9]
        rationale = ''
        parameters = ClassAssociationParameters(envName,headName,headDim,headNav,headType,headMult,headRole,tailRole,tailMult,tailType,tailNav,tailDim,tailName,rationale)
        association = ObjectFactory.build(associationId,parameters)
        asLabel = envName + '/' + headName + '/' + tailName
        associations[asLabel] = association
      rs.close()
      session.close()
      return associations
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting component class associations (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
      session = self.conn()
      session.execute('call addInternalDocument(:id,:name,:desc,:cont)',{'id':docId,'name':docName.encode('utf-8'),'desc':docDesc.encode('utf-8'),'cont':docContent.encode('utf-8')})
      session.commit()
      session.close()
      self.addDocumentCodes(docName,docCodes)
      self.addDocumentMemos(docName,docMemos)
      return docId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding internal document ' + docName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def updateInternalDocument(self,parameters):
    docId = parameters.id()
    docName = parameters.name()
    docDesc = parameters.description()
    docContent = parameters.content()
    docCodes = parameters.codes()
    docMemos = parameters.memos()
    try:
      session = self.conn()
      session.execute('call deleteInternalDocumentComponents(:id)',{'id':docId})

      session.execute('call updateInternalDocument(:id,:name,:desc,:cont)',{'id':docId,'name':docName.encode('utf-8'),'desc':docDesc.encode('utf-8'),'cont':docContent.encode('utf-8')})
      session.commit()
      session.close()
      self.addDocumentCodes(docName,docCodes)
      self.addDocumentMemos(docName,docMemos)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating internal document ' + docName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getCodes(self,constraintId = -1):
    try:
      session = self.conn()
      rs = session.execute('call getCodes(:const)',{'const':constraintId})
      cObjts = {}
      for row in rs.fetchall():
        row = list(row)
        codeId = row[0]
        codeName = row[1]
        codeType = row[2]
        codeDesc = row[3]
        incCriteria = row[4]
        codeEg = row[5]
        parameters = CodeParameters(codeName,codeType,codeDesc,incCriteria,codeEg)
        cObjt = ObjectFactory.build(codeId,parameters)
        cObjts[codeName] = cObjt
      rs.close()
      session.close()
      return cObjts
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting codes (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteCode(self,codeId = -1):
    self.deleteObject(codeId,'code')
    

  def addCode(self,parameters):
    codeId = self.newId()
    codeName = parameters.name()
    codeType = parameters.type()
    codeDesc = parameters.description()
    incCriteria = parameters.inclusionCriteria()
    codeEg  = parameters.example()
    try:
      session = self.conn()
      session.execute('call addCode(:id,:name,:type,:desc,:crit,:eg)',{'id':codeId,'name':codeName.encode('utf-8'),'type':codeType,'desc':codeDesc.encode('utf-8'),'crit':incCriteria.encode('utf-8'),'eg':codeEg.encode('utf-8')})
      session.commit()
      session.close()
      return codeId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding code ' + codeName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def updateCode(self,parameters):
    codeId = parameters.id()
    codeName = parameters.name()
    codeType = parameters.type()
    codeDesc = parameters.description()
    incCriteria = parameters.inclusionCriteria()
    codeEg  = parameters.example()
    try:
      session = self.conn()
      session.execute('call updateCode(:id,:name,:type,:desc,:crit,:eg)',{'id':codeId,'name':codeName.encode('utf-8'),'type':codeType,'desc':codeDesc.encode('utf-8'),'crit':incCriteria.encode('utf-8'),'eg':codeEg.encode('utf-8')})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating code ' + codeName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def documentCodes(self,docName):
    try:
      session = self.conn()
      rs = session.execute('call documentCodes(:name)',{'name':docName})
      codes = {}
      for row in rs.fetchall():
        row = list(row)
        codeName = row[0]
        startIdx = int(row[1])
        endIdx = int(row[2])
        codes[(startIdx,endIdx)] = codeName
      rs.close()
      session.close()
      return codes
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting codes for ' + docName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 
  
  def addDocumentCodes(self,docName,docCodes):
    for (startIdx,endIdx) in docCodes:
      docCode = docCodes[(startIdx,endIdx)]
      self.addDocumentCode(docName,docCode,startIdx,endIdx)

  def addDocumentCode(self,docName,docCode,startIdx,endIdx,codeLabel='',codeSynopsis=''):
    try:
      session = self.conn()
      session.execute('call addDocumentCode(:name,:code,:sIdx,:eIdx,:lbl,:syn)',{'name':docName,'code':docCode,'sIdx':startIdx,'eIdx':endIdx,'lbl':codeLabel,'syn':codeSynopsis})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding code ' + docCode + ' to '  + docName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def artifactCodes(self,artName,artType,sectName):
    try:
      session = self.conn()
      rs = session.execute('call artifactCodes(:art,:type,:sect)',{'art':artName,'type':artType,'sect':sectName})
      codes = {}
      for row in rs.fetchall():
        row = list(row)
        codeName = row[0]
        startIdx = int(row[1])
        endIdx = int(row[2])
        codes[(startIdx,endIdx)] = codeName
      rs.close()
      session.close()
      return codes
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting codes for ' + artType + ' ' + artName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
      session = self.conn()
      session.execute('call addArtifactCode(:art,:type,:sect,:code,:sIdx,:eIdx)',{'art':artName,'type':artType,'sect':sectName,'code':docCode,'sIdx':startIdx,'eIdx':endIdx})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding code ' + docCode + ' to '  + artType + ' ' + artName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
      session = self.conn()
      rs = session.execute('call artifactEnvironmentCodes(:art,:env,:type,:sect)',{'art':artName,'env':envName,'type':artType,'sect':sectName})
      codes = {}
      for row in rs.fetchall():
        row = list(row)
        codeName = row[0]
        startIdx = int(row[1])
        endIdx = int(row[2])
        codes[(startIdx,endIdx)] = codeName
      rs.close()
      session.close()
      return codes
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting codes for ' + artType + ' ' + artName + ' in environment ' + envName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addArtifactEnvironmentCodes(self,artName,envName,artType,sectName,docCodes):
    for (startIdx,endIdx) in docCodes:
      docCode = docCodes[(startIdx,endIdx)]
      self.addArtifactEnvironmentCode(artName,envName,artType,sectName,docCode,startIdx,endIdx)

  def addArtifactEnvironmentCode(self,artName,envName,artType,sectName,docCode,startIdx,endIdx):
    try:
      session = self.conn()
      session.execute('call addArtifactEnvironmentCode(:art,:env,:type,:sect,:code,:sIdx,:eIdx)',{'art':artName,'env':envName,'type':artType,'sect':sectName,'code':docCode,'sIdx':startIdx,'eIdx':endIdx})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding code ' + docCode + ' to '  + artType + ' ' + artName + ' in environment ' + envName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def personaCodeNetwork(self,personaName,fromCode='',toCode=''):
    try:
      session = self.conn()
      rs = session.execute('call artifactCodeNetwork(:pers,:a,:fCode,:tCode)',{'pers':personaName,'a':'persona','fCode':fromCode,'tCode':toCode})
      network = []
      for row in rs.fetchall():
        row = list(row)
        fromCode = row[0]
        fromType = row[1]
        toCode = row[2]
        toType = row[3]
        rType = row[4]
        network.append((fromCode,fromType,toCode,toType,rType))
      rs.close()
      session.close()
      return network
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting code network for persona ' + personaName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addCodeRelationship(self,personaName,fromName,toName,rshipType):
    try:
      session = self.conn()
      session.execute('call addArtifactCodeNetwork(:pers,:a,:fName,:tName,:type)',{'pers':personaName,'a':'persona','fName':fromName,'tName':toName,'type':rshipType})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding ' + rshipType + ' to ' + personaName + ' code network (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateCodeNetwork(self,personaName,rships):
    try:
      session = self.conn()
      session.execute('call deleteArtifactCodeNetwork(:pers,:a)',{'pers':personaName,'a':'persona'})
      session.commit()
      session.close()
      for fromName,toName,rshipType in rships:
        self.addCodeRelationship(personaName,fromName,toName,rshipType)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating code network for ' + ' personaName (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getImpliedProcesses(self,constraintId = -1):
    try:
      session = self.conn()
      rs = session.execute('call getImpliedProcesses(:const)',{'const':constraintId})

      ipRows = []
      for row in rs.fetchall():
        row = list(row)
        ipId = row[0]
        ipName = row[1]
        ipDesc = row[2]
        pName = row[3]
        ipSpec = row[4]
        ipRows.append((ipId,ipName,ipDesc,pName,ipSpec))
      rs.close()
      session.close()

      ips = {}
      for ipId,ipName,ipDesc,pName,ipSpec in ipRows:
        ipNet = self.impliedProcessNetwork(ipName)
        chs = self.impliedProcessChannels(ipName)
        parameters = ImpliedProcessParameters(ipName,ipDesc,pName,ipNet,ipSpec,chs)
        ip = ObjectFactory.build(ipId,parameters)
        ips[ipName] = ip
      return ips
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting implied processes (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def impliedProcessNetwork(self,ipName):
    try:
      session = self.conn()
      rs = session.execute('call impliedProcessNetwork(:name)',{'name':ipName})
      rows = []
      for row in rs.fetchall():
        row = list(row)
        fromName = row[0]
        fromType = row[1]
        toName = row[2]
        toType = row[3]
        rType = row[4]
        rows.append((fromName,fromType,toName,toType,rType))
      rs.close()
      session.close()
      return rows
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting implied process network ' + ipName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addImpliedProcess(self,parameters):
    try:
      ipId = self.newId()
      ipName = parameters.name()
      ipDesc = parameters.description()
      pName = parameters.persona()
      cNet = parameters.network()
      ipSpec = parameters.specification()
      chs = parameters.channels()

      session = self.conn()
      session.execute('call addImpliedProcess(:id,:name,:desc,:proc,:spec)',{'id':ipId,'name':ipName,'desc':ipDesc.encode('utf-8'),'proc':pName,'spec':ipSpec.encode('utf-8')})
      session.commit()
      session.close()
      self.addImpliedProcessNetwork(ipId,pName,cNet)
      self.addImpliedProcessChannels(ipId,chs)
      return ipId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding implied process ' + ipName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateImpliedProcess(self,parameters):
    try:
      ipId = parameters.id()
      ipName = parameters.name()
      ipDesc = parameters.description()
      pName = parameters.persona()
      cNet = parameters.network()
      ipSpec = parameters.specification()
      chs = parameters.channels()

      session = self.conn()
      session.execute('call deleteImpliedProcessComponents(:id)',{'id':ipId})

      session.execute('call updateImpliedProcess(:id,:name,:desc,:proc,:spec)',{'id':ipId,'name':ipName,'desc':ipDesc.encode('utf-8'),'proc':pName,'spec':ipSpec.encode('utf-8')})
      session.commit()
      session.close()
      self.addImpliedProcessNetwork(ipId,pName,cNet)
      self.addImpliedProcessChannels(ipId,chs)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating implied process ' + ipName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addImpliedProcessNetwork(self,ipId,personaName,cNet):
    for fromName,fromType,toName,toType,rType in cNet:
      self.addImpliedProcessNetworkRelationship(ipId,personaName,fromName,toName,rType)

  def addImpliedProcessNetworkRelationship(self,ipId,personaName,fromName,toName,rType):
    try:
      session = self.conn()
      session.execute('call addImpliedProcessNetworkRelationship(:id,:pers,:fName,:tName,:type)',{'id':ipId,'pers':personaName,'fName':fromName,'tName':toName,'type':rType})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating implied process  (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteImpliedProcess(self,ipId):
    self.deleteObject(ipId,'persona_implied_process')
    

  def addStepSynopsis(self,ucName,envName,stepNo,synName,aType,aName):
    try:
      session = self.conn()
      session.execute('call addStepSynopsis(:uc,:env,:step,:syn,:aName,:aType)',{'uc':ucName,'env':envName,'step':stepNo,'syn':synName,'aName':aName,'aType':aType})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding step synopsis ' + synName + '  (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def directoryEntry(self,objtName,dType):
    try:
      session = self.conn()
      rs = session.execute('call directoryEntry(:obj,:dir)',{'obj':objtName,'dir':dType})
      row = rs.fetchone()
      eName = row[0]
      eDesc = row[1]
      eType = row[2]
      rs.close()
      session.close()
      return (eName,eDesc,eType)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting details for ' + objtName + ' from ' + dType + ' directory  (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getTemplateGoals(self,constraintId = -1):
    try:
      session = self.conn()
      rs = session.execute('call getTemplateGoals(:const)',{'const':constraintId})
      templateGoals = {}
      tgRows = []
      for row in rs.fetchall():
        row = list(row)
        tgId = row[0]
        tgName = row[1]
        tgDef = row[2]
        tgRat = row[3]
        tgRows.append((tgId,tgName,tgDef,tgRat))
      rs.close()
      session.close()
      for tgId,tgName,tgDef,tgRat in tgRows:
        tgConcerns = self.templateGoalConcerns(tgId)
        tgResps = self.templateGoalResponsibilities(tgId)
        parameters = TemplateGoalParameters(tgName,tgDef,tgRat,tgConcerns,tgResps)
        templateGoal = ObjectFactory.build(tgId,parameters)
        templateGoals[tgName] = templateGoal
      session.close()
      return templateGoals
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting template goals (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteTemplateGoal(self,tgId):
    self.deleteObject(tgId,'template_goal')
    

  def componentViewGoals(self,cvName):
    try:
      session = self.conn()
      rs = session.execute('call componentViewGoals(:cv)',{'cv':cvName})
      rows = []
      for row in rs.fetchall():
        row = list(row)
        rows.append(row[0])
      rs.close()
      session.close()
      return rows
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting goals for component view ' + cvName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def situateComponentViewGoals(self,cvName,envName):
    try:
      session = self.conn()
      session.execute('call situateComponentViewGoals(:cv,:env)',{'cv':cvName,'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error situating goals for component view ' + cvName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def situateComponentViewGoalAssociations(self,cvName,envName):
    try:
      session = self.conn()
      session.execute('call situateComponentViewGoalAssociations(:cv,:env)',{'cv':cvName,'env':envName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error situating goal associations for component view ' + cvName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def templateGoalConcerns(self,tgId):
    try:
      session = self.conn()
      rs = session.execute('call templateGoalConcerns(:tg)',{'tg':tgId})
      concs = []
      for row in rs.fetchall():
        row = list(row)
        concs.append(row[0])
      rs.close()
      session.close()
      return concs
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting concerns for template goal id ' + str(tgId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addTemplateGoal(self,parameters):
    goalId = self.newId()
    goalName = parameters.name()
    goalDef = parameters.definition()
    goalRat = parameters.rationale()
    goalConcerns = parameters.concerns()
    goalResponsibilities = parameters.responsibilities()
    try:
      session = self.conn()
      session.execute('call addTemplateGoal(:id,:name,:def,:rat)',{'id':goalId,'name':goalName,'def':goalDef,'rat':goalRat})
      session.commit()
      session.close()
      self.addTemplateGoalConcerns(goalId,goalConcerns)
      self.addTemplateGoalResponsibilities(goalId,goalResponsibilities)
      return goalId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding template goal ' + goalName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateTemplateGoal(self,parameters):
    goalId = parameters.id()
    goalName = parameters.name()
    goalDef = parameters.definition()
    goalRat = parameters.rationale()
    goalConcerns = parameters.concerns()
    goalResponsibilities = parameters.responsibilities()
    try:
      session = self.conn()
      session.execute('call deleteTemplateGoalComponents(:id)',{'id':goalId})
      session.execute('call updateTemplateGoal(:id,:name,:def,:rat)',{'id':goalId,'name':goalName,'def':goalDef,'rat':goalRat})
      session.commit()
      session.close()
      self.addTemplateGoalConcerns(goalId,goalConcerns)
      self.addTemplateGoalResponsibilities(goalId,goalResponsibilities)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating template goal ' + goalName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 


  def addTemplateGoalConcerns(self,goalId,concerns):
    for concern in concerns:
      if concern != '':
        self.addTemplateGoalConcern(goalId,concern)

  def addTemplateGoalConcern(self,goalId,concern):
    try:
      session = self.conn()
      session.execute('call add_template_goal_concern(:id,:con)',{'id':goalId,'con':concern})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding template goal concern ' + concern + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def componentGoals(self,componentId):
    try:
      session = self.conn()
      rs = session.execute('call getComponentGoals(:comp)',{'comp':componentId})
      rows = []
      for row in rs.fetchall():
        row = list(row)
        rows.append(row[0])
      rs.close()
      session.close()
      return rows
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting goals for component id ' + str(componentId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addComponentGoals(self,componentId,componentGoals):
    for idx,goalName in enumerate(componentGoals):
      self.addComponentGoal(componentId,goalName)

  def addComponentGoal(self,componentId,goalName):
    try:
      session = self.conn()
      session.execute('call addComponentGoal(:comp,:goal)',{'comp':componentId,'goal':goalName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding goal to component id ' + str(componentId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addComponentAssociations(self,componentId,assocs):
    for idx,assoc in enumerate(assocs):
      self.addComponentGoalAssociation(componentId,assoc[0],assoc[1],assoc[2],assoc[3])

  def addComponentGoalAssociation(self,componentId,goalName,subGoalName,refType,rationale):
    try:
      session = self.conn()
      session.execute('call addComponentGoalAssociation(:comp,:goal,:sGoal,:ref,:rationale)',{'comp':componentId,'goal':goalName,'sGoal':subGoalName,'ref':refType,'rationale':rationale})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding goal association to component id ' + str(componentId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def componentGoalAssociations(self,componentId):
    try:
      session = self.conn()
      rs = session.execute('call componentGoalAssociations(:comp)',{'comp':componentId})
      assocs = []
      for row in rs.fetchall():
        row = list(row)
        assocs.append((row[0],row[1],row[2],row[3]))
      rs.close()
      session.close()
      return assocs
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting component goal associations (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def componentAttackSurface(self,cName):
    try:
      session = self.conn()
      rs = session.execute('call componentAttackSurfaceMetric(:comp)',{'comp':cName})
      row = rs.fetchone()
      asValue = row[0]
      rs.close()
      session.close()
      return asValue
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting attack surface for component ' + cName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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

    try:
      for ifName,ifType,arName,pName in parameters.interfaces():
        self.addComponentInterface(componentId,ifName,ifType,arName,pName)
      self.addComponentStructure(componentId,structure)
      self.addComponentRequirements(componentId,requirements)
      self.addComponentGoals(componentId,goals)
      self.addComponentAssociations(componentId,assocs)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error merging component ' + componentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addTemplateGoalResponsibilities(self,goalId,resps):
    for resp in resps:
      if resp != '':
        self.addTemplateGoalResponsibility(goalId,resp)

  def addTemplateGoalResponsibility(self,goalId,resp):
    try:
      session = self.conn()
      session.execute('call add_template_goal_responsibility(:goal,:resp)',{'goal':goalId,'resp':resp})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding template goal responsibility ' + resp + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def templateGoalResponsibilities(self,tgId):
    try:
      session = self.conn()
      rs = session.execute('call templateGoalResponsibilities(:tg)',{'tg':tgId})
      concs = []
      for row in rs.fetchall():
        row = list(row)
        concs.append(row[0])
      rs.close()
      session.close()
      return concs
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting responsibilities for template goal id ' + str(tgId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def importTemplateAsset(self,taName,environmentName):
    try:
      session = self.conn()
      session.execute('call importTemplateAssetIntoEnvironment(:ta,:env)',{'ta':taName,'env':environmentName})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error importing asset ' + taName + ' into environment ' + environmentName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def candidateGoalObstacles(self,cvName,envName):
    try:
      session = self.conn()
      rs = session.execute('call candidateGoalObstacles(:cv,:env)',{'cv':cvName,'env':envName})
      gos = []
      for row in rs.fetchall():
        row = list(row)
        gos.append((row[0],row[1]))
      rs.close()
      session.close()
      return gos
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting candidate obstacles associated with architectural pattern ' + cvName + ' and environment ' + envName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def templateGoalDefinition(self,tgId):
    try:
      session = self.conn()
      rs = session.execute('select definition from template_goal where id =:tg',{'tg':tgId})
      row = rs.fetchone()
      tgDef = row[0]
      rs.close()
      session.close()
      return tgDef
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting definition for template goal id ' + str(tgId) + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def redmineArchitectureSummary(self,envName):
    try:
      session = self.conn()
      rs = session.execute('call redmineArchitectureSummary(:env)',{'env':envName})
      aps = []
      for row in rs.fetchall():
        row = list(row)
        aName = row[0]
        aTxt = row[1]
        aps.append((row[0],row[1]))
      rs.close()
      session.close()
      return aps
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error exporting architecture summary to Redmine (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def redmineAttackPatternsSummary(self,envName):
    try:
      session = self.conn()
      rs = session.execute('call redmineAttackPatternsSummary(:env)',{'env':envName})
      row = rs.fetchone()
      buf = row[0]
      rs.close()
      session.close()
      return buf
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error exporting attack patterns summary to Redmine (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def processesToXml(self,includeHeader=True):
    try:
      session = self.conn()
      rs = session.execute('call processesToXml(:head)',{'head':includeHeader})
      row = rs.fetchone()
      xmlBuf = row[0] 
      idCount = row[1]
      codeCount = row[2]
      memoCount = row[3]
      qCount = row[4]
      pcnCount = row[5]
      icCount = row[6]
      ipnCount = row[7]
      rs.close()
      session.close()
      return (xmlBuf,idCount,codeCount,memoCount,qCount,pcnCount,icCount,ipnCount)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error exporting processes to XML (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

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
    try:
      session = self.conn()
      rs = session.execute('call getMemos(:const)',{'const':constraintId})
      mObjts = {}
      for row in rs.fetchall():
        row = list(row)
        memoId = row[0]
        memoName = row[1]
        memoDesc = row[2]
        parameters = MemoParameters(memoName,memoDesc)
        mObjt = ObjectFactory.build(memoId,parameters)
        mObjts[memoName] = mObjt
      rs.close()
      session.close()
      return mObjts
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting memos (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteMemo(self,memoId = -1):
    self.deleteObject(memoId,'memo')
    

  def addMemo(self,parameters):
    memoId = self.newId()
    memoName = parameters.name()
    memoDesc = parameters.description()
    try:
      session = self.conn()
      session.execute('call addMemo(:id,:name,:desc)',{'id':memoId,'name':memoName.encode('utf-8'),'desc':memoDesc.encode('utf-8')})
      session.commit()
      session.close()
      return memoId
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding memo ' + memoName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateMemo(self,parameters):
    memoId = parameters.id()
    memoName = parameters.name()
    memoDesc = parameters.description()
    try:
      session = self.conn()
      session.execute('call updateMemo(:id,:name,:desc)',{'id':memoId,'name':memoName.encode('utf-8'),'desc':memoDesc.encode('utf-8')})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating memo ' + memoName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def documentMemos(self,docName):
    try:
      session = self.conn()
      rs = session.execute('call documentMemos(:doc)',{'doc':docName})
      memos = {}
      for row in rs.fetchall():
        row = list(row)
        memoName = row[0]
        memoTxt = row[1]
        startIdx = int(row[2])
        endIdx = int(row[3])
        memos[(startIdx,endIdx)] = (memoName,memoTxt)
      rs.close()
      session.close()
      return memos
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting codes for ' + docName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addDocumentMemos(self,docName,docMemos):
    for (startIdx,endIdx) in docMemos:
      memoName,memoTxt = docMemos[(startIdx,endIdx)]
      self.addDocumentMemo(docName,memoName,memoTxt,startIdx,endIdx)

  def addDocumentMemo(self,docName,memoName,memoTxt,startIdx,endIdx):
    try:
      session = self.conn()
      session.execute('call addDocumentMemo(:doc,:mem,:txt,:sIdx,:eIdx)',{'doc':docName,'mem':memoName,'txt':memoTxt,'sIdx':startIdx,'eIdx':endIdx})
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding memo ' + memoName + ' to '  + docName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def impliedProcess(self,procName):
    try:
      session = self.conn()
      rs = session.execute('call impliedProcess(:proc)',{'proc':procName})
      row = rs.fetchone()
      cspBuf = row[0] 
      rs.close()
      session.close()
      return cspBuf
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error exporting implied process ' + procName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addImpliedProcessChannels(self,ipId,channels):
    for channelName,dataType in channels:
      self.addImpliedProcessChannel(ipId,channelName,dataType)

  def addImpliedProcessChannel(self,ipId,channelName,dataType):
    try:
      session = self.conn()
      session.execute('call addImpliedProcessChannel(:id,:chan,:type)',{'id':ipId,'chan':channelName,'type':dataType})
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding implied process channel ' + channelName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def impliedProcessChannels(self,procName):
    try:
      session = self.conn()
      rs = session.execute('call impliedProcessChannels(:proc)',{'proc':procName})
      chs = []
      for row in rs.fetchall():
        row = list(row)
        chs.append((row[0],row[1]))
      rs.close()
      session.close()
      return chs
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting channels for implied process ' + procName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def getQuotations(self):
    try:
      session = self.conn()
      rs = session.execute('call getQuotations()')
      qs = []
      for row in rs.fetchall():
        row = list(row)
        code = row[0] 
        aType = row[1]
        aName = row[2]
        sectName = row[3]
        startIdx = row[4]
        endIdx = row[5]
        quote = row[6]
        synopsis = row[7]
        label = row[8]
        qs.append((code,aType,aName,sectName,quote,startIdx,endIdx,synopsis,label))
      rs.close()
      session.close()
      return qs
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting quotations (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateQuotation(self,codeName,atName,aName,oldStartIdx,oldEndIdx,startIdx,endIdx,synopsis,label):
    try:
      if atName == 'internal_document':
        session = self.conn()
        session.execute('call updateDocumentCode(:aName,:code,:oSIdx,:oEIdx,:sIdx,:eIdx,:syn,:lbl)',{'aName':aName,'code':codeName,'oSIdx':oldStartIdx,'oEIdx':oldEndIdx,'sIdx':startIdx,'eIdx':endIdx,'syn':synopsis,'lbl':label})
        session.commit()
        session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating code ' + codeName + ' with '  + aName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteQuotation(self,codeName,atName,aName,startIdx,endIdx):
    try:
      if atName == 'internal_document':
        session = self.conn()
        session.execute('call deleteDocumentCode(:aName,:code,:sIdx,:eIdx)',{'aName':aName,'code':codeName,'sIdx':startIdx,'eIdx':endIdx})
        session.commit()
        session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error associating code ' + codeName + ' with '  + aName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def artifactText(self,artType,artName):
    try:
      if artType == 'internal_document':
        session = self.conn()
        rs = session.execute('call artifactText(:type,:name)',{'type':artType,'name':artName})
        row = rs.fetchone()
        content = row[0]
        rs.close()
        session.close()
        return content 
      else: 
        return ''
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting context for ' + artType + ' ' + artName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def impliedCharacteristic(self,pName,fromCode,toCode,rtName):
    try:
      session = self.conn()
      rs = session.execute('call impliedCharacteristic(:pName,:fCode,:tCode,:rt)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName})
      row = rs.fetchone()
      if row is None:
        rs.close()
        session.close()
        raise NoImpliedCharacteristic(pName,fromCode,toCode,rtName)
      charName = row[0]
      qualName = row[1]
      varName = row[2]
      rs.close()
      session.close()
      return (charName,qualName,varName)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting implied characteristic for ' + pName + '/' + fromCode + '/' + toCode + '/' + rtName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def impliedCharacteristicElements(self,pName,fromCode,toCode,rtName,isLhs):
    return self.responseList('call impliedCharacteristicElements(:pName,:fCode,:tCode,:rt,:lhs)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName,'lhs':isLhs},'MySQL error getting implied characteristic elements')

  def initialiseImpliedCharacteristic(self,pName,fromCode,toCode,rtName):
    self.updateDatabase('call initialiseImpliedCharacteristic(pName,fCode,tCode,rt)',{'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName},'MySQL error initialising implied characteristic')

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

  def updateImpliedCharacteristicIntention(self,charName,intName,intType):
    self.updateDatabase('call updateImpliedCharacteristicIntention(:char,:int,:type)',{'char':charName,'int':intName,'type':intType},'MySQL error updating implied characteristic intention')

  def addImpliedCharacteristicElement(self,charName,lblName,rtName):
    self.updateDatabase('call addImpliedCharacteristicElement(:char,:lbl,:rt)',{'char':charName,'lbl':lblName,'rt':rtName},'MySQL error adding implied characteristic element')

  def updateImpliedCharacteristicElement(self,charName,lblName,rtName):
    self.updateDatabase('call updateImpliedCharacteristicElement(:char,:lbl,:rt)',{'char':charName,'lbl':lblName,'rt':rtName},'MySQL error updating implied characteristic element')

  def codeCount(self,codeName):
    return self.responseList('select codeCount(:code)',{'code':codeName},'MySQL error getting code count')[0]

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

  def impliedCharacteristicIntention(self,synName,pName,fromCode,toCode,rtName):
    return self.responseLis('select impliedCharacteristicIntention(:syn,:pName,:fCode,:tCode,:rt)',{'syn':synName,'pName':pName,'fCode':fromCode,'tCode':toCode,'rt':rtName},'MySQL error getting implied characteristic intention')[0].split('#')

  def impliedCharacteristicElementIntention(self,ciName,elName):
    return self.responseList('select impliedCharacteristicElementIntention(:ci,:el)',{'ci':ciName,'el':elName},'MySQL error getting implied characteristic element intention')[0].split('#')

  def updateImpliedCharacteristicElementIntention(self,ciName,elName,intName,intDim,meName,contName):
    self.updateDatabase('call updateImpliedCharacteristicElementIntention(:ci,:el,:int,:dim,:me,:cont)',{'ci':ciName,'el':elName,'int':intName,'dim':intDim,'me':meName,'cont':contName},'MySQL error updating intention for element ' + elName + ' for implied characteristic ' + ciName)

  def deniedGoals(self,codeName):
    return self.responseList('call deniedGoals(:code)',{'code':codeName},'MySQL error getting denied goals')

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
    try:
      session = self.conn()
      rs = session.execute('call getLocationLinks(:locs)',{'locs':locsName})
      linkDict = {}
      for row in rs.fetchall():
        row = list(row)
        tailLoc = row[0]
        headLoc = row[1]
        if tailLoc in linkDict:
          linkDict[tailLoc].append(headLoc)
        else:
          linkDict[tailLoc] = [headLoc]

        if headLoc in linkDict:
          linkDict[headLoc].append(tailLoc)
        else:
          linkDict[headLoc] = [tailLoc]
      rs.close()
      session.close()
      return linkDict
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting location links (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exception)

  def getAssetInstances(self,locName):
    try:
      session = self.conn()
      rs = session.execute('call getAssetInstances(:locs)',{'locs':locName})
      instanceRows = []
      for row in rs.fetchall():
        row = list(row)
        instanceName = row[0]
        assetName = row[1]
        instanceRows.append((instanceName,assetName))
      rs.close()
      session.close()
      return instanceRows
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting asset instances for location ' + locName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exception)

  def getPersonaInstances(self,locName):
    try:
      session = self.conn()
      rs = session.execute('call getPersonaInstances(:locs)',{'locs':locName})
      instanceRows = []
      for row in rs.fetchall():
        row = list(row)
        instanceName = row[0]
        personaName = row[1]
        instanceRows.append((instanceName,personaName))
      rs.close()
      session.close()
      return instanceRows
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting persona instances for location ' + locName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exception)

  def deleteLocations(self,locsId):
    self.deleteObject(locsId,'locations')
    

  def locationsRiskModel(self,locationsName,environmentName):
    traceRows = self.responseList('call locationsRiskModel(:locs,:env)',{'locs':locationsName,'env':environmentName},'MySQL error getting location risk model')
    traces = []
    for fromObjt,fromName,toObjt,toName in traceRows:
      parameters = DotTraceParameters(fromObjt,fromName,toObjt,toName)
      traces.append(ObjectFactory.build(-1,parameters))
    return traces

  def prepareDatabase(self):
    try:
      import logging
      logger = logging.getLogger(__name__)
      self.conn.query('select @@max_sp_recursion_depth;')
      result = self.conn.store_result()
      if (result is None):
        exceptionText = 'Error returned stored_result'
        raise DatabaseProxyException(exceptionText)

      real_result = result.fetch_row()
      if (len(real_result) < 1):
        exceptionText = 'Error getting max_sp_recursion_depth from database'
        raise DatabaseProxyException(exceptionText)

      try:
        rec_value = real_result[0][0]
      except LookupError:
        rec_value = -1

      if rec_value == -1:
        logger.warning('Unable to get max_sp_recursion_depth. Be sure max_sp_recursion_depth is set to 255 or more.')
      elif rec_value < 255:
        self.conn.query('set max_sp_recursion_depth = 255')
        self.conn.store_result()

        self.conn.query('select @@max_sp_recursion_depth;')
        result = self.conn.use_result()
        real_result = result.fetch_row()

        try:
          rec_value = real_result[0][0]
          logger.debug('max_sp_recursion_depth is %d.' % rec_value)
          if rec_value < 255:
            logger.warning('WARNING: some features may not work because the maximum recursion depth for stored procedures is too low')
        except LookupError:
          logger.warning('Unable to get max_sp_recursion_depth. Be sure max_sp_recursion_depth is set to 255 or more.')

    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error preparing database'
      raise DatabaseProxyException(exceptionText)

  def templateAssetMetrics(self,taName):
    return self.responseList('call templateAssetMetrics(:ta)',{'ta':taName},'MySQL error getting template asset metrics')[0]

  def riskModelElements(self,envName):
    try: 
      session = self.conn()
      rs = session.execute('call riskAnalysisModelElements(:env)',{'env':envName})
      elNames = []
      for elNameRow in rs.fetchall():
        elNameRow = list(elNameRow)
        elNames.append(elNameRow[1])
      rs.close()
      session.close() 
      return elNames
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error getting elements for risk model in environment ' + envName + ' (id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 

  def assetThreatRiskLevel(self,assetName,threatName):
    return self.responseList('call assetThreatRiskLevel(:ass,:thr)',{'ass':assetName,'thr':threatName},'MySQL error getting asset threat risk level')[0]

  def assetRiskLevel(self,assetName):
    return self.responseList('call assetRiskLevel(:ass)',{'ass':assetName},'MySQL error getting asset risk level')[0]

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
    dbPasswd = ses_settings['dbPasswd']

    host = b.dbHost
    port = b.dbPort
    user = b.dbUser
    passwd = b.dbPasswd
    db = dbName

    try:
      dbEngine = create_engine('mysql+mysqldb://root:'+rPasswd+'@'+dbHost+':'+str(dbPort))
      self.conn = scoped_session(sessionmaker(bind=dbEngine))
      stmts = ['drop database if exists `' + dbName + '`',
               'create database ' + dbName,
               "grant all privileges on `" + dbName + "`.* TO '" + dbUser + "'@'%' identified by '" + dbPasswd + "'",
               'alter database ' + dbName + ' default character set utf8',
               'alter database ' + dbName + ' default collate utf8_general_ci',
               'flush tables',
               'flush privileges']
      session = self.conn()
      for stmt in stmts:
        session.execute(stmt)
      session.close()
      self.conn.close()
      b.settings[session_id]['dbName'] = dbName
      self.clearDatabase(session_id)
      self.reconnect(True,session_id)
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error creating CAIRIS database ' + dbName + ' on host ' + b.dbHost + ' at port ' + str(b.dbPort) + ' with user ' + b.dbUser + ' (id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 

  def openDatabase(self,dbName,session_id):
    b = Borg()
    b.settings[session_id]['dbName'] = dbName
    self.reconnect(True,session_id)

  def showDatabases(self,session_id):
    b = Borg()
    ses_settings = b.get_settings(session_id)
    dbName = ses_settings['dbName']
    session = self.conn()
    rs = session.execute('show databases')
    dbs = []
    restrictedDbs = ['information_schema','flaskdb','mysql','performance_schema',dbName]
    for row in rs.fetchall():
      row = list(row)
      dbName = row[0]
      if (dbName not in restrictedDbs):
        dbs.append(row[0])
    session.close()
    return dbs

  def deleteDatabase(self,dbName,session_id):
    b = Borg()
    ses_settings = b.get_settings(session_id)
    dbHost = ses_settings['dbHost']
    dbPort = ses_settings['dbPort']
    rPasswd = ses_settings['rPasswd']

    try:
      dbEngine = create_engine('mysql+mysqldb://root'+':'+rPasswd+'@'+dbHost+':'+str(dbPort))
      tmpConn = scoped_session(sessionmaker(bind=dbEngine))
      stmt = 'drop database if exists `' + dbName + '`'
      session = tmpConn()
      session.execute(stmt)
      session.close()
      tmpConn.remove()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error creating CAIRIS database ' + dbName + '(id:' + str(id) + ',message:' + msg
      raise DatabaseProxyException(exceptionText) 

  def getUseCaseRequirements(self,ucName):
    return self.responseList('call useCaseRequirements(:uc)',{'uc':ucName},'MySQL error getting requirements associated with use case ' + ucName)

  def getUseCaseGoals(self,ucName,envName):
    return self.responseList('call useCaseGoals(:uc,:env)',{'uc':ucName,'env':envName},'MySQL error getting goals associated with use case ' + ucName)

  def synopsisId(self,synTxt):
    return self.responseList('select synopsisId(:syn)',{'syn':synTxt},'MySQL error finding synopsis id for text ' + synTxt)[0]

  def hasContribution(self,contType,rsName,csName):
    try:
      session = self.conn()
      sqlTxt = 'hasReferenceContribution'
      if contType == 'usecase':
        sqlTxt = 'hasUseCaseContribution'
      rs = session.execute('select ' + sqlTxt + '(:rName,:cName)',{'rName':rsName,'cName':csName})
      row = rs.fetchone()
      hasRC = row[0]
      rs.close()
      session.close()
      if (hasRC == 1): 
        return True
      else:
        return False
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error finding reference contribution for  ' + rsName + '/' + csName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def removeUseCaseContributions(self,ucId):
    self.updateDatabase('call removeUseCaseContributions(:id)',{'id':ucId},'MySQL error removing use case contribution')

  def getDataFlows(self,dfName='',envName=''):
    dfRows = self.responseList('call getDataFlows(:df,:env)',{'df':dfName,'env':envName},'MySQL error getting data flows')
    dataFlows = {}
    for dfName,envName,fromName,fromType,toName,toType in dfRows:
      dfAssets = self.getDataFlowAssets(dfName,envName)
      parameters = DataFlowParameters(dfName,envName,fromName,fromType,toName,toType,dfAssets)
      df = ObjectFactory.build(-1,parameters)
      dataFlows[dfName + '/' + envName] = df
    return dataFlows

  def getDataFlowAssets(self,dfName,envName):
    return self.responseList('call getDataFlowAssets(:df,:env)',{'df':dfName,'env':envName},'MySQL error getting assets for data flow ' + dfName)

  def addDataFlow(self,parameters):
    dfName = parameters.name()
    envName = parameters.environment()
    fromName = parameters.fromName()
    fromType = parameters.fromType()
    toName = parameters.toName()
    toType = parameters.toType()
    dfAssets = parameters.assets()
    try:
      session = self.conn()
      session.execute('call addDataFlow(:df,:env,:fName,:fType,:tName,:tType)',{'df':dfName,'env':envName,'fName':fromName,'fType':fromType,'tName':toName,'tType':toType})
      session.commit()
      for dfAsset in dfAssets:
        self.addDataFlowAsset(dfName,envName,dfAsset, session)
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding dataflow ' + parameters.name() + '/' + parameters.environment() + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def addDataFlowAsset(self,dfName,envName,dfAsset, session):
    try:
      session.execute('call addDataFlowAsset(:df,:env,:ass)',{'df':dfName,'env':envName,'ass':dfAsset})
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error adding asset ' + dfAsset + ' to dataflow ' + dfName + '/' + envName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def updateDataFlow(self,oldDfName,oldEnvName,parameters):
    dfName = parameters.name()
    envName = parameters.environment()
    fromName = parameters.fromName()
    fromType = parameters.fromType()
    toName = parameters.toName()
    toType = parameters.toType()
    dfAssets = parameters.assets()
    try:
      session = self.conn()
      session.execute('call deleteDataFlowAssets(:df,:env)',{'df':oldDfName,'env':oldEnvName})
      session.execute('call updateDataFlow(:oDf,:nDf,:oEnv,:nEnv,:fName,:fType,:tName,:tType)',{'oDf':oldDfName,'nDf':dfName,'oEnv':oldEnvName,'nEnv':envName,'fName':fromName,'fType':fromType,'tName':toName,'tType':toType})
      session.commit
      for dfAsset in dfAssets:
        self.addDataFlowAsset(dfName,envName,dfAsset,session)
      session.commit()
      session.close()
    except _mysql_exceptions.DatabaseError, e:
      id,msg = e
      exceptionText = 'MySQL error updating dataflow ' + oldDfName + '/' + oldEnvName + ' (id:' + str(id) + ',message:' + msg + ')'
      raise DatabaseProxyException(exceptionText) 

  def deleteDataFlow(self,dfName,envName):
    self.updateDatabase('call deleteDataFlow(:df,:env)',{'df':dfName,'env':envName},'MySQL Error deleting data flow')

  def dataFlowDiagram(self,envName,filterElement = ''):
    return self.responseList('call dataFlowDiagram(:env,:fe)',{'env':envName,'fe':filterElement},'MySQL error getting data flow diagram')

  def relabelRequirements(self,reqReference):
    self.updateDatabase('call relabelRequirements(:reqReference)',{'reqReference':reqReference},'MySQL error relabelling requirements')

  def getTrustBoundaries(self,constraintId = -1):
    tbRows = self.responseList('call getTrustBoundaries(:id)',{'id':constraintId},'MySQL error getting trust boundaries')
    tbs = {} 
    for tbId,tbName,tbDesc in tbRows:
      environmentProperties = {}
      for environmentId,environmentName in self.dimensionEnvironments(tbId,'trust_boundary'):
        environmentProperties[environmentName] = self.trustBoundaryComponents(tbId,environmentId)
      tbs[tbName] = TrustBoundary(tbId,tbName,tbDesc,environmentProperties)
    return tbs

  def trustBoundaryComponents(self,tbId, envId):
    return self.responseList('call trustBoundaryComponents(:tbId,:envId)',{'tbId':tbId,'envId':envId},'MySQL error getting trust boundary components for trust boundary id ' + str(tbId))

  def addTrustBoundary(self,tb):
    tbId = self.newId()
    self.updateDatabase("call addTrustBoundary(:id,:name,:desc)",{'id':tbId,'name':tb.name(),'desc':tb.description()},'MySQL error adding trust boundary ' + str(tbId))
    for environmentName in tb.environmentProperties().keys():
      for tbComponentType,tbComponent in tb.environmentProperties()[environmentName]:
        self.addTrustBoundaryComponent(tbId,environmentName,tbComponent)

  def addTrustBoundaryComponent(self,tbId,envName,tbComponent):
    self.updateDatabase('call addTrustBoundaryComponent(:id,:environment,:component)',{'id':tbId,'environment':envName,'component':tbComponent},'MySQL error adding trust boundary component ' + tbComponent + ' to trust boundary id ' + str(tbId))


  def updateTrustBoundary(self,tb):
    self.updateDatabase('call deleteTrustBoundaryComponents(:id)',{'id':tb.id()},'MySQL error deleting trust boundary components for ' + tb.name())
    self.updateDatabase("call updateTrustBoundary(:id,:name,:desc)",{'id':tb.id(),'name':tb.name(),'desc':tb.description()},'MySQL error adding trust boundary ' + tb.name())
    for environmentName in tb.environmentProperties().keys():
      for tbComponentType,tbComponent in tb.environmentProperties()[environmentName]:
        self.addTrustBoundaryComponent(tb.id(),environmentName,tbComponent)

  def deleteTrustBoundary(self,tbId):
    self.deleteObject(tbId,'trust_boundary')
