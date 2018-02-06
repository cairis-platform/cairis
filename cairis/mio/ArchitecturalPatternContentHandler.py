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


from xml.sax.handler import ContentHandler,EntityResolver
from cairis.core.ComponentViewParameters import ComponentViewParameters
from cairis.core.ComponentParameters import ComponentParameters
from cairis.core.ConnectorParameters import ConnectorParameters
from cairis.core.RoleParameters import RoleParameters
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.TemplateAssetParameters import TemplateAssetParameters
from cairis.core.TemplateRequirementParameters import TemplateRequirementParameters
from cairis.core.TemplateGoalParameters import TemplateGoalParameters
from cairis.core.Borg import Borg
from xml.sax.saxutils import unescape

__author__ = 'Shamal Faily'

def a2i(spLabel):
  if spLabel == 'Low':
    return 1
  elif spLabel == 'Medium':
    return 2
  elif spLabel == 'High':
    return 3
  else:
    return 0

class ArchitecturalPatternContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theViewParameters = None
    self.theViewName = ''
    self.theSynopsis = ''
    self.inSynopsis = 0
    self.theMetricTypes = []
    self.theRoles = []
    self.theAssets = []
    self.theRequirements = []
    self.theGoals = []
    self.theComponents = []
    self.theConnectors = []
    self.resetRoleAttributes()
    self.resetAssetAttributes()
    self.resetRequirementAttributes()
    self.resetGoalAttributes()
    self.resetComponentAttributes()
    self.resetSecurityPropertyAttributes()
    self.resetConnectorAttributes()
    self.resetComponentGoalAssociationAttributes()
    b = Borg()
    self.configDir = b.configDir

  def resolveEntity(self,publicId,systemId):
    return systemId

  def view(self):
    return self.theViewParameters

  def resetRoleAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theType = ''
    self.theShortCode = ''
    self.theDescription = ''


  def resetValueTypeAttributes(self):
    self.inDescription = 0
    self.inRationale = 0
    self.theName = ''
    self.theDescription = ''
    self.theRationale = ''
    self.theScore = 0

  def resetComponentAttributes(self):
    self.inDescription = 0
    self.theName = ''
    self.theDescription = ''
    self.theInterfaces = []
    self.theStructure = []
    self.theComponentRequirements = []
    self.theComponentGoals = []
    self.theComponentGoalAssociations = []
    self.resetStructure()

  def resetStructure(self):
    self.theHeadName = ''
    self.theHeadAdornment = ''
    self.theHeadNav = ''
    self.theHeadNry = ''
    self.theHeadRole = ''
    self.theTailRole = ''
    self.theTailNry = ''
    self.theTailNav = ''
    self.theTailAdornment = ''
    self.theTailName = ''

  def resetRequirementAttributes(self):
    self.inDescription = 0
    self.inRationale = 0
    self.inFitCriterion = 0
    self.theAsset = ''
    self.theType = ''
    self.theReqName = ''
    self.theDescription = ''
    self.theRationale = ''
    self.theFitCriterion = ''

  def resetGoalAttributes(self):
    self.inDefinition = 0
    self.inRationale = 0
    self.theName = ''
    self.theDefinition = ''
    self.theRationale = ''
    self.theConcerns = []
    self.theResponsibilities = []

  def resetAssetAttributes(self):
    self.inDescription = 0
    self.inSignificance = 0
    self.theName = ''
    self.theShortCode = ''
    self.theAssetType = ''
    self.theSurfaceType = ''
    self.theAccessRight = ''
    self.theDescription = ''
    self.theSignificance = ''
    self.theTags = []
    self.theInterfaces = []
    self.theSecurityProperties = []

  def resetSecurityPropertyAttributes(self):
    self.thePropertyName = ''
    self.thePropertyValue = 'None'
    self.inRationale = 0
    self.theRationale = ''


  def resetConnectorAttributes(self):
    self.theName = ''
    self.theFromName = ''
    self.theFromRole = ''
    self.theFromInterface = ''
    self.theToName = ''
    self.theToRole = ''
    self.theToInterface = ''
    self.theConnectorAsset = ''
    self.theProtocolName = ''
    self.theAccessRight = ''

  def resetComponentGoalAssociationAttributes(self):
    self.inRationale = 0
    self.theGoalName = ''
    self.theSubGoalName = ''
    self.theRefType = ''
    self.theRationale = ''


  def startElement(self,name,attrs):
    if (name == 'architectural_pattern'):
      self.theViewName = attrs['name']
    elif (name == 'synopsis'):
      self.inSynopsis = 1
      self.theSynopsis = ''
    elif (name == 'role'):
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theType = attrs['type']
    elif (name == 'component'):
      self.theName = attrs['name']
    elif (name == 'description'):
      self.inDescription = 1
      self.theDescription = ''
    elif (name == 'definition'):
      self.inDefinition = 1
      self.theDefinition = ''
    elif (name == 'fit_criterion'):
      self.inFitCriterion = 1
      self.theFitCriterion = ''
    elif name == 'significance':
      self.inSignificance = 1
      self.theSignificance = ''
    elif name == 'rationale':
      self.inRationale = 1
      self.theRationale = ''
    elif name == 'interface':
      self.theInterfaces.append((attrs['name'],attrs['type'],attrs['access_right'],attrs['privilege']))
    elif name == 'concern':
      self.theConcerns.append(attrs['name'])
    elif name == 'responsibility':
      self.theResponsibilities.append(attrs['name'])
    elif name == 'asset':
      self.theName = attrs['name']
      self.theShortCode = attrs['short_code']
      self.theAssetType = attrs['type']
      self.theSurfaceType = attrs['surface_type']
      self.theAccessRight = attrs['access_right']
      self.theSecurityProperties = []
    elif name == 'tag':
      self.theTags.append(attrs['name'])
    elif name == 'security_property':
      self.thePropertyName = attrs['property']
      self.thePropertyValue = attrs['value']
    elif (name == 'connector'):
      self.theName = attrs['name']
      self.theFromName = attrs['from_component']
      self.theFromInterface = attrs['from_interface']
      self.theFromRole = attrs['from_role']
      self.theToName = attrs['to_component']
      self.theToInterface = attrs['to_interface']
      self.theToRole = attrs['to_role']
      self.theConnectorAsset = attrs['asset_name']
      self.theProtocolName = attrs['protocol']
      self.theAccessRight = attrs['access_right']
    elif name == 'structure':
      self.theHeadName = attrs['head_asset']
      self.theHeadAdornment = attrs['head_adornment']
      self.theHeadNav = attrs['head_nav']
      rawHeadNry = attrs['head_nry']
      if (rawHeadNry == 'a'):
        rawHeadNry = '*'
      elif (rawHeadNry == '1..a'):
        rawHeadNry = '1..*'
      self.theHeadNry = rawHeadNry
      self.theHeadRole = attrs['head_role']
      self.theTailRole = attrs['tail_role']
      rawTailNry = attrs['tail_nry']
      if (rawTailNry == 'a'):
        rawTailNry = '*'
      elif (rawTailNry == '1..a'):
        rawTailNry = '1..*'
      self.theTailNry = rawTailNry
      self.theTailNav = attrs['tail_nav']
      self.theTailAdornment = attrs['tail_adornment']
      self.theTailName = attrs['tail_asset']
    elif name == 'requirement':
      self.theReqName = attrs['name']
      self.theAsset = attrs['asset']
      rawType = attrs['type']
      self.theType = rawType.replace('_',' ')
    elif name == 'goal':
      self.theName = attrs['name']
    elif name == 'component_requirement':
      self.theComponentRequirements.append(attrs['name'])
    elif name == 'component_goal':
      self.theComponentGoals.append(attrs['name'])
    elif name == 'access_right' or name == 'protocol' or name == 'privilege' or name == 'surface_type':
      self.theName = attrs['name']
      self.theScore = int(attrs['value'])
    elif name == 'component_goal_association':
      self.theGoalName = attrs['goal_name']
      self.theSubGoalName = attrs['subgoal_name']
      self.theRefType = attrs['ref_type']

  def characters(self,data):
    if self.inDescription:
      self.theDescription += data
    elif self.inDefinition:
      self.theDefinition += data
    elif self.inSynopsis:
      self.theSynopsis += data
    elif self.inSignificance:
      self.theSignificance += data
    elif self.inRationale:
      self.theRationale += data
    elif self.inFitCriterion:
      self.theFitCriterion += data


  def endElement(self,name):
    if (name == 'component'):
      p = ComponentParameters(unescape(self.theName),unescape(self.theDescription),self.theInterfaces,self.theStructure,self.theComponentRequirements,self.theComponentGoals,self.theComponentGoalAssociations)
      self.theComponents.append(p)
      self.resetComponentAttributes() 
    elif name == 'role':
      p = RoleParameters(unescape(self.theName),self.theType,unescape(self.theShortCode),unescape(self.theDescription),[])
      self.theRoles.append(p)
      self.resetRoleAttributes()
    elif name == 'asset':
      spDict = {}
      spDict['confidentiality'] = 0
      spDict['integrity'] = 0
      spDict['availability'] = 0
      spDict['accountability'] = 0
      spDict['anonymity'] = 0
      spDict['pseudonymity'] = 0
      spDict['unlinkability'] = 0
      spDict['unobservability'] = 0
      srDict = {}
      srDict['confidentiality'] = 'None'
      srDict['integrity'] = 'None'
      srDict['availability'] = 'None'
      srDict['accountability'] = 'None'
      srDict['anonymity'] = 'None'
      srDict['pseudonymity'] = 'None'
      srDict['unlinkability'] = 'None'
      srDict['unobservability'] = 'None'
      for sp in self.theSecurityProperties:
        spName = sp[0]
        spValue = a2i(sp[1])
        spRationale = sp[2]
        if spName in spDict:
          spDict[spName] = spValue
        if spName in srDict:
          srDict[spName] = spRationale
      spValues = [] 
      spValues.append(spDict['confidentiality'])
      spValues.append(spDict['integrity'])
      spValues.append(spDict['availability'])
      spValues.append(spDict['accountability'])
      spValues.append(spDict['anonymity'])
      spValues.append(spDict['pseudonymity'])
      spValues.append(spDict['unlinkability'])
      spValues.append(spDict['unobservability'])
      srValues = [] 
      srValues.append(srDict['confidentiality'])
      srValues.append(srDict['integrity'])
      srValues.append(srDict['availability'])
      srValues.append(srDict['accountability'])
      srValues.append(srDict['anonymity'])
      srValues.append(srDict['pseudonymity'])
      srValues.append(srDict['unlinkability'])
      srValues.append(srDict['unobservability'])
      p = TemplateAssetParameters(unescape(self.theName),unescape(self.theShortCode),unescape(self.theDescription),unescape(self.theSignificance),self.theAssetType,unescape(self.theSurfaceType),unescape(self.theAccessRight),spValues,srValues,self.theTags,self.theInterfaces)
      self.theAssets.append(p)
      self.resetAssetAttributes()
    elif name == 'security_property':
      self.theSecurityProperties.append((self.thePropertyName,self.thePropertyValue,unescape(self.theRationale)))
      self.resetSecurityPropertyAttributes()
    elif name == 'structure':
      self.theStructure.append((unescape(self.theHeadName),unescape(self.theHeadAdornment),unescape(self.theHeadNav),unescape(self.theHeadNry),unescape(self.theHeadRole),unescape(self.theTailRole),unescape(self.theTailNry),unescape(self.theTailNav),unescape(self.theTailAdornment),unescape(self.theTailName)))
      self.resetStructure()
    elif name == 'requirement':
      p = TemplateRequirementParameters(unescape(self.theReqName),unescape(self.theAsset),unescape(self.theType),unescape(self.theDescription),unescape(self.theRationale),unescape(self.theFitCriterion))
      self.theRequirements.append(p)
      self.resetRequirementAttributes()
    elif name == 'goal':
      p = TemplateGoalParameters(unescape(self.theName),unescape(self.theDefinition),unescape(self.theRationale),self.theConcerns,self.theResponsibilities)
      self.theGoals.append(p)
      self.resetGoalAttributes()
    elif name == 'connector':
      p = ConnectorParameters(unescape(self.theName),unescape(self.theViewName),unescape(self.theFromName),unescape(self.theFromRole),unescape(self.theFromInterface),unescape(self.theToName),unescape(self.theToInterface),unescape(self.theToRole),unescape(self.theConnectorAsset),unescape(self.theProtocolName),unescape(self.theAccessRight))
      self.theConnectors.append(p)
      self.resetConnectorAttributes() 
    elif name == 'component_goal_association':
      self.theComponentGoalAssociations.append((unescape(self.theGoalName),unescape(self.theSubGoalName),self.theRefType,unescape(self.theRationale)))
      self.resetComponentGoalAssociationAttributes()
    elif name == 'description':
      self.inDescription = 0
    elif name == 'definition':
      self.inDefinition = 0
    elif name == 'synopsis':
      self.inSynopsis = 0
    elif name == 'rationale':
      self.inRationale = 0
    elif name == 'significance':
      self.inSignificance = 0
    elif name == 'fit_criterion':
      self.inFitCriterion = 0
    elif name == 'access_right' or name == 'protocol' or name == 'privilege' or name == 'surface_type':
      p = ValueTypeParameters(unescape(self.theName),unescape(self.theDescription),name,'',self.theScore,unescape(self.theRationale))
      self.theMetricTypes.append(p)
      self.resetValueTypeAttributes()
    elif name == 'architectural_pattern':
      self.theViewParameters = ComponentViewParameters(unescape(self.theViewName),unescape(self.theSynopsis),self.theMetricTypes,self.theRoles,self.theAssets,self.theRequirements,self.theGoals,self.theComponents,self.theConnectors)
