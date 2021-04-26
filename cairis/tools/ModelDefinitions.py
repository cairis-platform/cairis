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

from flask_restful import fields
from cairis.core.AcceptEnvironmentProperties import AcceptEnvironmentProperties

from cairis.core.ObjectSummary import ObjectSummary
from cairis.core.Asset import Asset
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.Attacker import Attacker
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.core.ClassAssociation import ClassAssociation
from cairis.core.GoalAssociation import GoalAssociation
from cairis.core.Dependency import Dependency
from cairis.core.Directory import Directory
from cairis.core.Goal import Goal
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.Obstacle import Obstacle
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.DomainProperty import DomainProperty
from cairis.core.MisuseCase import MisuseCase
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.MitigateEnvironmentProperties import MitigateEnvironmentProperties
from cairis.core.Persona import Persona
from cairis.core.PersonaEnvironmentProperties import PersonaEnvironmentProperties
from cairis.core.Requirement import Requirement
from cairis.core.Risk import Risk
from cairis.core.Role import Role
from cairis.core.SecurityPattern import SecurityPattern
from cairis.core.Target import Target
from cairis.core.Task import Task
from cairis.core.Trace import Trace
from cairis.core.TrustBoundary import TrustBoundary
from cairis.core.UseCase import UseCase
from cairis.core.TaskEnvironmentProperties import TaskEnvironmentProperties
from cairis.core.UseCaseEnvironmentProperties import UseCaseEnvironmentProperties
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.TransferEnvironmentProperties import TransferEnvironmentProperties
from cairis.core.ValidationResult import ValidationResult
from cairis.core.ValueType import ValueType
from cairis.core.Vulnerability import Vulnerability
from cairis.core.VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from cairis.core.Countermeasure import Countermeasure
from cairis.core.CountermeasureEnvironmentProperties import CountermeasureEnvironmentProperties
from cairis.core.ClassAssociation import ClassAssociation
from cairis.core.GoalAssociation import GoalAssociation
from cairis.core.ExternalDocument import ExternalDocument
from cairis.core.DocumentReference import DocumentReference
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from cairis.core.ReferenceContribution import ReferenceContribution
from cairis.core.GoalContribution import GoalContribution
from cairis.core.ConceptReference import ConceptReference
from cairis.core.PersonaCharacteristic import PersonaCharacteristic
from cairis.core.TaskCharacteristic import TaskCharacteristic
from cairis.core.ComponentView import ComponentView
from cairis.core.Component import Component
from cairis.core.TemplateGoal import TemplateGoal
from cairis.core.TemplateAsset import TemplateAsset
from cairis.core.TemplateRequirement import TemplateRequirement
from cairis.core.Location import Location
from cairis.core.Locations import Locations
from cairis.core.WeaknessTarget import WeaknessTarget
from cairis.core.DataFlow import DataFlow
from cairis.core.UserStory import UserStory
from cairis.tools.PseudoClasses import EnvironmentTensionModel, SecurityAttribute, ValuedRole, RiskRating, CountermeasureTarget,PersonaTaskCharacteristics, StepAttributes, CharacteristicReference,ObjectDependency,CharacteristicReferenceSynopsis,CharacteristicReferenceContribution

__author__ = 'Robin Quetin, Shamal Faily'

obj_id_field = "__python_obj__"
likelihood_metadata = { "enum": ['Incredible', 'Improbable', 'Remote', 'Occasional', 'Probable', 'Frequent'] }
severity_metadata = { "enum": ['Negligible', 'Marginal', 'Critical', 'Catastrophic'] }
value_metadata = { "enum": ['None','Low', 'Medium', 'High'] }
assettype_metadata = { "enum" : ['Information','Systems','Software','Hardware','People']}

def gen_class_metadata(class_ref):
  return {
    "enum": [class_ref.__module__+'.'+class_ref.__name__]
  }

class InterfaceModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theInterfaceName": fields.String,
    "theInterfaceType": fields.String,
    "theAccessRight": fields.String,
    "thePrivilege": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class AssetEnvironmentPropertiesModel(object):
  def __init__(self, env_name='', associations=[], attributes=[]):
    self.environment = env_name
    self.associations = associations
    self.attributes = attributes
    self.attributesDictionary = {}

  def json_prepare(self):
    self.attributes = list(self.attributesDictionary.values())
    self.attributesDictionary = {}
    for idx in range(0, len(self.associations)):
      self.associations[idx] = list(self.associations[idx])

  resource_fields = {
    "__python_obj__": fields.String,
    "theAssociations": fields.List(fields.List(fields.String)),
    "theProperties": fields.List(fields.Nested(SecurityAttribute.resource_fields)),
    "theEnvironmentName": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class AssetModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theDescription": fields.String,
    "theSignificance": fields.String,
    "theTags": fields.List(fields.String),
    "theCriticalRationale": fields.String,
    "theInterfaces": fields.List(fields.Nested(InterfaceModel.resource_fields)),
    "theType": fields.String,
    "theName": fields.String,
    "isCritical": fields.Integer,
    "theShortCode": fields.String,
    "theEnvironmentProperties": fields.List(fields.Nested(AssetEnvironmentPropertiesModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ObjectSummaryModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theType": fields.String,
    "theDescription": fields.String,
    "theOriginator": fields.String,
    "theStatus": fields.String,
    "theVulnerability": fields.String,
    "theThreat": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)


class CapabilityModel(object):
  resource_fields = {
    "name": fields.String,
    "value": fields.String
  }
  required = list(resource_fields.keys())

class AttackerEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theMotives': fields.List(fields.String),
    'theRoles': fields.List(fields.String),
    'theCapabilities': fields.List(fields.Nested(CapabilityModel.resource_fields)),
    'theEnvironmentName': fields.String,
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class AttackerModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theImage': fields.String,
    'theDescription': fields.String,
    'theTags': fields.List(fields.String),
    'theEnvironmentProperties': fields.List(fields.Nested(AttackerEnvironmentPropertiesModel.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class CImportParams(object):
  resource_fields = {
    'urlenc_file_contents': fields.String,
    'type': fields.String,
    'overwrite': fields.Integer
  }
  required = list(resource_fields.keys())

class CExportParams(object):
  resource_fields = {
    'theModel': fields.String
  }
  required = list(resource_fields.keys())

class DocumentationParams(object):
  resource_fields = {
    'theDocumentType': fields.String,
    'theTypeFlags': fields.List(fields.Integer),
    'theSectionFlags': fields.List(fields.Integer)
  }
  required = list(resource_fields.keys())

class DependencyModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theDependencyType': fields.String,
    'theRationale': fields.String,
    'theEnvironmentName': fields.String,
    'theDepender': fields.String,
    'theDependee': fields.String,
    'theDependency': fields.String,
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ClassAssociationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theEnvironmentName': fields.String,
    'theHeadAsset': fields.String,
    'theHeadNav': fields.String,
    'theHeadType': fields.String,
    'theHeadMultiplicity': fields.String,
    'theHeadRole': fields.String,
    'theTailRole': fields.String,
    'theTailMultiplicity': fields.String,
    'theTailType': fields.String,
    'theTailNav': fields.String,
    'theTailAsset': fields.String,
    'theRationale': fields.String,
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class GoalAssociationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theEnvironmentName': fields.String,
    'theGoal': fields.String,
    'theGoalDimension': fields.String,
    'theAssociation': fields.String,
    'theSubGoal': fields.String,
    'theSubGoalDimension': fields.String,
    'theAlternativeId': fields.String,
    'theRationale': fields.String,
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class EnvironmentModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theShortCode": fields.String,
    "theDescription": fields.String,
    "theEnvironments": fields.List(fields.String),
    "theDuplicateProperty": fields.String,
    "theOverridingEnvironment": fields.String,
    "theTensions": fields.List(fields.Nested(EnvironmentTensionModel.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ConcernAssociationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theSource': fields.String,
    'theSourceNry': fields.String,
    'theLinkVerb': fields.String,
    'theTargetNry': fields.String,
    'theTarget': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,src,srcNry,linkVerb,targ,targNry):
    self.theSource = src
    self.theSourceNry = srcNry
    self.theLinkVerb = linkVerb
    self.theTargetNry = targNry
    self.theTarget = targ

class RefinementModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theEndName': fields.String,
    'theEndType': fields.String,
    'theRefType': fields.String,
    'isAlternate': fields.String,
    'theRationale': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,eName,eType,refType,isAlt,refRat):
    self.theEndName = eName
    self.theEndType = eType
    self.theRefType = refType
    self.isAlternate = isAlt
    self.theRationale = refRat

class PolicyStatementModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theGoalName': fields.String,
    'theEnvironmentName': fields.String,
    'theSubject': fields.String,
    'theAccessType': fields.String,
    'theResource': fields.String,
    'thePermission': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,g,e,s,a,r,p):
    self.theGoalName = g
    self.theEnvironmentName = e
    self.theSubject = s
    self.theAccessType = a
    self.theResource = r
    self.thePermission = p

class GoalEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theCategory": fields.String,
    "theConcernAssociations": fields.List(fields.Nested(ConcernAssociationModel.resource_fields)),
    "theConcerns": fields.List(fields.String),
    "theDefinition": fields.String,
    "theEnvironmentName": fields.String,
    "theFitCriterion": fields.String,
    "theGoalRefinements": fields.List(fields.Nested(RefinementModel.resource_fields)),
    "theIssue": fields.String,
    "thePriority": fields.String,
    "theSubGoalRefinements": fields.List(fields.Nested(RefinementModel.resource_fields)),
    "thePolicy" : fields.Nested(PolicyStatementModel.resource_fields)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class GoalModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theEnvironmentProperties": fields.List(fields.Nested(GoalEnvironmentPropertiesModel.resource_fields)),
    "theName": fields.String,
    "theOriginator": fields.String,
    "theTags": fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ObstacleEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theDefinition": fields.String,
    "theCategory": fields.String,
    "theGoalRefinements": fields.List(fields.Nested(RefinementModel.resource_fields)),
    "theSubGoalRefinements": fields.List(fields.Nested(RefinementModel.resource_fields)),
    "theConcerns": fields.List(fields.String),
    "theProbability": fields.Float,
    "theProbabilityRationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ObstacleModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theTags": fields.List(fields.String),
    "theOriginator": fields.String,
    "theEnvironmentProperties": fields.List(fields.Nested(ObstacleEnvironmentPropertiesModel.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class DomainPropertyModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theTags": fields.List(fields.String),
    "theDescription": fields.String,
    "theType": fields.String,
    "theOriginator": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)



class MisuseCaseEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theAssets": fields.List(fields.String),
    "theAttackers": fields.List(fields.String),
    "theDescription": fields.String,
    "theEnvironmentName": fields.String,
    "theObjective": fields.String,
    "theLikelihood": fields.String,
    "theRiskRating": fields.Nested(RiskRating.resource_fields),
    "theSeverity": fields.String,
  }
  required = ["theDescription", "theEnvironmentName"]

class MisuseCaseModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theRiskName": fields.String,
    "theEnvironmentProperties": fields.List(fields.Nested(MisuseCaseEnvironmentPropertiesModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class RequirementModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theLabel": fields.String,
    "theDescription": fields.String,
    "thePriority": fields.Integer,
    "theOriginator": fields.String,
    "theFitCriterion": fields.String,
    "theRationale": fields.String,
    "theType": fields.String,
    "theDomain" : fields.String,
    "theDomainType" : fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)


class AcceptEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theCost': fields.String,
    'theRationale': fields.String,
    'theEnvironmentName': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class MitigateEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theDetectionMechanisms': fields.List(fields.String),
    'theDetectionPoint': fields.String,
    'theType': fields.String,
    'theEnvironmentName': fields.String,
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)


class TransferEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theRoles': fields.List(fields.Nested(ValuedRole.resource_fields)),
    'theRationale': fields.String,
    'theEnvironmentName': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ResponseEnvironmentPropertiesModel(object):
  resource_fields = {
    'accept': fields.List(fields.Nested(AcceptEnvironmentPropertiesModel.resource_fields)),
    'mitigate': fields.List(fields.Nested(MitigateEnvironmentPropertiesModel.resource_fields)),
    'transfer': fields.List(fields.Nested(TransferEnvironmentPropertiesModel.resource_fields))
  }
  field_names = list(resource_fields.keys())

class ResponseModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theTags': fields.List(fields.String),
    'theRisk': fields.String,
    'theName': fields.String,
    'theEnvironmentProperties': fields.Nested(ResponseEnvironmentPropertiesModel.resource_fields),
    'theResponseType': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
  required.remove('theTags')

class RiskModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theVulnerabilityName": fields.String,
    "theMisuseCase": fields.Nested(MisuseCaseModel.resource_fields),
    "theTags": fields.List(fields.Nested(fields.String)),
    "theThreatName": fields.String,
    "theRiskName": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
  required.remove("theTags")

class RoleModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theType": fields.String,
    "theShortCode": fields.String,
    "theDescription": fields.String,
  }

  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class RoleEnvironmentPropertiesModel(object):
  resource_fields = {
    "theEnvironmentName": fields.String,
    "theResponses": fields.List(fields.List(fields.String)),
    "theCountermeasures": fields.List(fields.String),
    "theGoals": fields.List(fields.String),
    "theRequirements": fields.List(fields.String)
  }
  required = list(resource_fields.keys())

class ThreatEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theAssets': fields.List(fields.String),
    'theLikelihood': fields.String,
    'theEnvironmentName': fields.String,
    'theAttackers': fields.List(fields.String),
    'theProperties': fields.List(fields.Nested(SecurityAttribute.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ThreatModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theTags': fields.List(fields.String),
    'theName': fields.String,
    'theType': fields.String,
    'theMethod': fields.String,
    'theEnvironmentProperties': fields.List(fields.Nested(ThreatEnvironmentPropertiesModel.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class UserConfigModel(object):
  resource_fields = {
    "user": fields.String,
    "passwd": fields.String,
    "db": fields.String,
    "host": fields.String,
    "port": fields.Integer,
    "jsonPrettyPrint": fields.String
  }
  required = list(resource_fields.keys())
  required.remove("jsonPrettyPrint")

class VulnerabilityEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theAssets": fields.List(fields.String),
    "theEnvironmentName": fields.String,
    "theSeverity": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class VulnerabilityModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theType': fields.String,
    'theTags': fields.List(fields.String),
    'theDescription': fields.String,
    'theEnvironmentProperties': fields.List(fields.Nested(VulnerabilityEnvironmentPropertiesModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class CountermeasureTask(object):
  resource_fields = {
    "thePersona": fields.String,
    "theTask": fields.String,
    "theDuration": fields.String,
    "theFrequency": fields.String,
    "theDemands": fields.String,
    "theGoalConflict": fields.String
  }
  required = list(resource_fields.keys())

  def __init__(self,pName,tName,tDur,tFreq,tDemands,tGoalConflict):
    self.thePersona = pName
    self.theTask = tName
    self.theDuration = tDur
    self.theFrequency = tFreq
    self.theDemands = tDemands
    self.theGoalConflict = tGoalConflict

class CountermeasureEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theEnvironmentName": fields.String,
    "theRequirements": fields.List(fields.String),
    "theTargets": fields.List(fields.Nested(CountermeasureTarget.resource_fields)),
    'theProperties': fields.List(fields.Nested(SecurityAttribute.resource_fields)),
    "theCost": fields.String,
    "theRoles": fields.List(fields.String),
    "thePersonas": fields.List(fields.Nested(CountermeasureTask.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class CountermeasureModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theTags': fields.List(fields.String),
    'theDescription': fields.String,
    'theType': fields.String,
    'theEnvironmentProperties': fields.List(fields.Nested(CountermeasureEnvironmentPropertiesModel.resource_fields)),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
  required.remove('theTags')

class PersonaEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theDirectFlag': fields.Integer,
    'theNarrative': fields.String,
    'theRoles': fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class PersonaModel(object):
  resource_fields = {
    obj_id_field: fields.String,
      'theName': fields.String,
      'theTags': fields.List(fields.String),
      'theActivities': fields.String,
      'theAttitudes': fields.String,
      'theAptitudes': fields.String,
      'theMotivations': fields.String,
      'theSkills': fields.String,
      'theIntrinsic': fields.String,
      'theContextual': fields.String,
      'theImage': fields.String,
      'isAssumption': fields.Integer,
      'thePersonaType': fields.String,
      'theEnvironmentProperties': fields.List(fields.Nested(PersonaEnvironmentPropertiesModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)


class TaskEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'thePersonas': fields.List(fields.Nested(PersonaTaskCharacteristics.resource_fields)),
    'theAssets': fields.List(fields.String),
    'theDependencies': fields.String,
    'theNarrative': fields.String,
    'theConsequences': fields.String,
    'theBenefits': fields.String,
    'theConcernAssociations': fields.List(fields.Nested(ConcernAssociationModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class TaskModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theShortCode': fields.String,
    'theObjective': fields.String,
    'isAssumption': fields.Integer,
    'theAuthor': fields.String,
    'theTags': fields.List(fields.String),
    'theEnvironmentProperties': fields.List(fields.Nested(TaskEnvironmentPropertiesModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class UseCaseEnvironmentPropertiesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'thePreCond': fields.String,
    'theSteps': fields.List(fields.Nested(StepAttributes.resource_fields)),
    'thePostCond': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class UseCaseContributionModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theContributionTo': fields.String,
    'theReferenceContribution': fields.Nested(CharacteristicReferenceContribution.resource_fields)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,contTo,rc):
    self.theContributionTo = contTo
    self.theReferenceContribution = rc

  def __getitem__(self,varName):
    if (varName == 'theContributionTo'): return self.theContributionTo
    elif (varName == 'theReferenceContribution'): return self.theReferenceContribution
    else: return None



class UseCaseModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theTags': fields.List(fields.String),
    'theAuthor': fields.String,
    'theCode': fields.String,
    'theActors': fields.List(fields.String),
    'theDescription': fields.String,
    'theReferenceContributions': fields.List(fields.Nested(UseCaseContributionModel.resource_fields)),
    'theEnvironmentProperties': fields.List(fields.Nested(UseCaseEnvironmentPropertiesModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class SearchValuesModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theEnvironmentName': fields.String,
    'theTypeName': fields.String,
    'theObjectName': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class FindModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theSearchValues': fields.List(fields.Nested(SearchValuesModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class VersionModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theVersion': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ValidationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theLabel': fields.String,
    'theMessage': fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class AssetAssociationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theEnvironmentName": fields.String,
    "theHeadAsset": fields.String,
    "theHeadType": fields.String,
    "theHeadNavigation": fields.String,
    "theHeadMultiplicity": fields.String,
    "theHeadRole": fields.String,
    "theTailRole": fields.String,
    "theTailMultiplicity": fields.String,
    "theTailType": fields.String,
    "theTailNavigation": fields.String,
    "theTailAsset": fields.String,
    "theRationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class GoalAssociationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theEnvironmentName": fields.String,
    "theGoal": fields.String,
    "theGoalDimension": fields.String,
    "theAssociationType": fields.String,
    "theSubGoal": fields.String,
    "theSubGoalDimension": fields.String,
    "theAlternativeId": fields.String,
    "theRationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ExternalDocumentModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theVersion": fields.String,
    "thePublicationDate": fields.String,
    "theAuthors": fields.String,
    "theDescription": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class DocumentReferenceModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theDocName": fields.String,
    "theContributor": fields.String,
    "theExcerpt": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ReferenceSynopsisModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theReference": fields.String,
    "theSynopsis": fields.String,
    "theDimension": fields.String,
    "theActor": fields.String,
    "theSynopsisDimension" : fields.String,
    "theInitialSatisfaction" : fields.String,
    "theRelatedGoals" : fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ReferenceContributionModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theSource": fields.String,
    "theDestination": fields.String,
    "theMeansEnd": fields.String,
    "theContribution": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class GoalContributionModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theSource": fields.String,
    "theSourceType": fields.String,
    "theDestination": fields.String,
    "theDestinationType": fields.String,
    "theMeansEnd": fields.String,
    "theContribution": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ConceptReferenceModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theDimName": fields.String,
    "theObjtName": fields.String,
    "theDescription": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class PersonaCharacteristicModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "thePersonaName": fields.String,
    "theModQual": fields.String,
    "theVariable": fields.String,
    "theName": fields.String,
    "theCharacteristicSynopsis": fields.Nested(CharacteristicReferenceSynopsis.resource_fields),
    "theGrounds": fields.List(fields.Nested(CharacteristicReference.resource_fields)),
    "theWarrant": fields.List(fields.Nested(CharacteristicReference.resource_fields)),
    "theRebuttal": fields.List(fields.Nested(CharacteristicReference.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class TaskCharacteristicModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theTaskName": fields.String,
    "theModQual": fields.String,
    "theName": fields.String,
    "theGrounds": fields.List(fields.Nested(CharacteristicReference.resource_fields)),
    "theWarrant": fields.List(fields.Nested(CharacteristicReference.resource_fields)),
    "theRebuttal": fields.List(fields.Nested(CharacteristicReference.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)


class ObjectDependencyModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theDependencies": fields.List(fields.Nested(ObjectDependency.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self):
    self.theDependencies = []

class ComponentStructureModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theHeadAsset": fields.String,
    "theHeadAdornment": fields.String,
    "theHeadNav": fields.String,
    "theHeadNry": fields.String,
    "theHeadRole": fields.String,
    "theTailRole": fields.String,
    "theTailNry": fields.String,
    "theTailNav": fields.String,
    "theTailAdornment": fields.String,
    "theTailAsset": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ComponentGoalAssociationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theHeadGoal": fields.String,
    "theRefType": fields.String,
    "theTailGoal": fields.String,
    "theRationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ComponentModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theDescription": fields.String,
    "theInterfaces" : fields.List(fields.Nested(InterfaceModel.resource_fields)),
    "theStructure" : fields.List(fields.Nested(ComponentStructureModel.resource_fields)),
    "theRequirements" : fields.List(fields.String),
    "theGoals" : fields.List(fields.String),
    "theGoalAssociations" : fields.List(fields.Nested(ComponentGoalAssociationModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ConnectorModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theConnectorName": fields.String,
    "theFromComponent": fields.String,
    "theFromRole": fields.String,
    "theFromInterface": fields.String,
    "theToComponent": fields.String,
    "theToInterface": fields.String,
    "theToRole": fields.String,
    "theAssetName": fields.String,
    "theProtocol": fields.String,
    "theAccessRight": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ArchitecturalPatternModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theSynopsis": fields.String,
    "theComponents": fields.List(fields.Nested(ComponentModel.resource_fields)),
    "theConnectors": fields.List(fields.Nested(ConnectorModel.resource_fields)),
    "theAttackSurfaceMetric": fields.List(fields.Integer)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
  required.remove('theAttackSurfaceMetric')

class ValueTypeModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theDescription": fields.String,
    "theType": fields.String,
    "theEnvironmentName": fields.String,
    "theScore": fields.Integer,
    "theRationale": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class TemplateGoalModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theDefinition": fields.String,
    "theRationale": fields.String,
    "theConcerns": fields.List(fields.String),
    "theResponsibilities": fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class TemplateAssetModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theShortCode": fields.String,
    "theDescription": fields.String,
    "theSignificance": fields.String,
    "theType": fields.String,
    "theSurfaceType": fields.String,
    "theAccessRight": fields.String,
    "theProperties": fields.List(fields.Nested(SecurityAttribute.resource_fields)),
    "theTags": fields.String,
    "theInterfaces" : fields.List(fields.Nested(InterfaceModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
  required.remove('theTags')

class TemplateRequirementModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theAssetName": fields.String,
    "theType": fields.String,
    "theDescription": fields.String,
    "theRationale": fields.String,
    "theFitCriterion": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class LocationModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theAssetInstances": fields.List(fields.String),
    "thePersonaInstances": fields.List(fields.String),
    "theLinks": fields.List(fields.String),
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class LocationsModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theDiagram": fields.List(fields.String),
    "theLocations" : fields.List(fields.Nested(LocationModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class SummaryModel(object):
  resource_fields = {
    "theLabel": fields.String,
    "theValue": fields.String
  }
  required = list(resource_fields.keys())

  def __init__(self,lbl,val):
    self.theLabel = lbl 
    self.theValue = val

class TraceModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theFromObject": fields.String,
    "theFromName": fields.String,
    "theToObject": fields.String,
    "theToName": fields.String,
    "theLabel" : fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,fromObjt,fromName,toObjt,toName,lbl):
    self.theFromObject = fromObjt
    self.theFromName = fromName
    self.theToObject = toObjt
    self.theToName = toName
    self.theLabel = lbl

class WeaknessTargetModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theTargetName": fields.String,
    "theComponents": fields.List(fields.String),
    "theTemplateAssets": fields.List(fields.String),
    "theAssets": fields.List(fields.String),
    "theTreatmentRequirement": fields.String,
    "theTreatmentAsset": fields.String,
    "theTreatmentEffectiveness": fields.String,
    "theTreatmentRationale" : fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self):
    self.theTargetName = ''
    self.theComponents = []
    self.theTemplateAssets = []
    self.theAssets = []
    self.theTreatmentRequirement = ''
    self.theTreatmentAsset = ''
    self.theTreatmentEffectiveness = ''
    self.theTreatmentRationale = ''

class PersonaImpactModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "thePersonaName": fields.String,
    "theImpactScore": fields.Integer
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,pName,iScore):
    self.thePersonaName = pName
    self.theImpactScore = iScore


class CandidateGoalObstacleModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theGoalName": fields.String,
    "theObstacleName": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,gName,oName):
    self.theGoalName = gName
    self.theObstacleName = oName

class WeaknessAnalysisModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theVulnerabilityWeaknesses" : fields.List(fields.Nested(WeaknessTargetModel.resource_fields)),
    "theThreatWeaknesses" : fields.List(fields.Nested(WeaknessTargetModel.resource_fields)),
    "thePersonaImpact" : fields.List(fields.Nested(PersonaImpactModel.resource_fields)),
    "theCandidateGoals" : fields.List(fields.Nested(CandidateGoalObstacleModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self):
    self.theVulnerabilityWeaknesses = []
    self.theThreatWeaknesses = []
    self.thePersonaImpact = []
    self.theCandidateGoals = []

class SecurityPatternStructureModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theHeadAsset": fields.String,
    "theHeadAdornment": fields.String,
    "theHeadNry": fields.String,
    "theHeadRole": fields.String,
    "theTailRole": fields.String,
    "theTailNry": fields.String,
    "theTailAdornment": fields.String,
    "theTailAsset": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)


class PatternRequirementModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theAsset": fields.String,
    "theType": fields.String,
    "theDescription": fields.String,
    "theRationale": fields.String,
    "theFitCriterion": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class SecurityPatternModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theContext": fields.String,
    "theProblem": fields.String,
    "theSolution": fields.String,
    "theRequirements": fields.List(fields.Nested(PatternRequirementModel.resource_fields)),
    "theConcernAssociations" : fields.List(fields.Nested(SecurityPatternStructureModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class DataFlowObstacle(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theObstacleName" : fields.String,
    "theKeyword" : fields.String,
    "theContext" : fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class DataFlowModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theType": fields.String,
    "theEnvironmentName": fields.String,
    "theFromName": fields.String,
    "theFromType": fields.String,
    "theToName": fields.String,
    "theToType": fields.String,
    "theAssets": fields.List(fields.String),
    "theObstacles": fields.List(fields.Nested(DataFlowObstacle.resource_fields)),
    "theTags": fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class DirectoryModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theLabel": fields.String,
    "theName": fields.String,
    "theDescription": fields.String,
    "theType": fields.String,
    "theReference": fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class TrustBoundaryComponent(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theType': fields.String,
    "theTags": fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,n,t):
    self.theName = n 
    self.theType = t

  def name(self): return self.theName
  def type(self): return self.theType

class TrustBoundaryEnvironmentModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theEnvironmentName': fields.String,
    'theComponents': fields.List(fields.Nested(TrustBoundaryComponent.resource_fields)),
    'thePrivilege' : fields.String
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

  def __init__(self,n,c,p):
    self.theEnvironmentName = n
    self.theComponents = c
    self.thePrivilege = p

class TrustBoundaryModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theName': fields.String,
    'theType': fields.String,
    'theDescription': fields.String,
    'theEnvironmentProperties': fields.List(fields.Nested(TrustBoundaryEnvironmentModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ThreatModelPropertyModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theProperty': fields.String,
    'theThreats': fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ThreatModelElementModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theElement': fields.String,
    'theProperties': fields.List(fields.Nested(ThreatModelPropertyModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class ThreatModelModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    'theEntities': fields.List(fields.Nested(ThreatModelElementModel.resource_fields)),
    'theProcesses': fields.List(fields.Nested(ThreatModelElementModel.resource_fields)),
    'theDatastores': fields.List(fields.Nested(ThreatModelElementModel.resource_fields)),
    'theDataflows': fields.List(fields.Nested(ThreatModelElementModel.resource_fields))
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)

class UserStoryModel(object):
  resource_fields = {
    obj_id_field: fields.String,
    "theName": fields.String,
    "theAuthor": fields.String,
    "theRole": fields.String,
    "theDescription": fields.String,
    "theUserGoal": fields.String,
    "theAcceptanceCriteria": fields.List(fields.String),
    "theTags": fields.List(fields.String)
  }
  required = list(resource_fields.keys())
  required.remove(obj_id_field)
