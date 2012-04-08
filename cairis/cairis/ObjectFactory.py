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


from ARM import *
from Attacker import Attacker
from Persona import Persona
from Goal import Goal
from Obstacle import Obstacle
from DomainProperty import DomainProperty
from Asset import Asset
from TemplateAsset import TemplateAsset
from SecurityPattern import SecurityPattern
from Threat import Threat
from Vulnerability import Vulnerability
from Risk import Risk
from Response import Response
from Countermeasure import Countermeasure
from Task import Task
from MisuseCase import MisuseCase
from Trace import Trace
from DotTrace import DotTrace
from Environment import Environment
from Role import Role
from ExternalDocument import ExternalDocument
from DocumentReference import DocumentReference
from ConceptReference import ConceptReference
from PersonaCharacteristic import PersonaCharacteristic
from TaskCharacteristic import TaskCharacteristic
from Responsibility import Responsibility
from ClassAssociation import ClassAssociation
from DomainAssociation import DomainAssociation
from GoalAssociation import GoalAssociation
from Dependency import Dependency
from AttackerParameters import AttackerParameters
from PersonaParameters import PersonaParameters
from GoalParameters import GoalParameters
from ObstacleParameters import ObstacleParameters
from AssetParameters import AssetParameters
from TemplateAssetParameters import TemplateAssetParameters
from SecurityPatternParameters import SecurityPatternParameters
from ThreatParameters import ThreatParameters
from VulnerabilityParameters import VulnerabilityParameters
from RiskParameters import RiskParameters
from ResponseParameters import ResponseParameters
from CountermeasureParameters import CountermeasureParameters
from TaskParameters import TaskParameters
from MisuseCaseParameters import MisuseCaseParameters
from TraceParameters import TraceParameters
from UpdateTraceParameters import UpdateTraceParameters
from DotTraceParameters import DotTraceParameters
from EnvironmentParameters import EnvironmentParameters
from RoleParameters import RoleParameters
from ResponsibilityParameters import ResponsibilityParameters
from AttackerEnvironmentProperties import AttackerEnvironmentProperties
from AssetEnvironmentProperties import AssetEnvironmentProperties
from ThreatEnvironmentProperties import ThreatEnvironmentProperties
from VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from RoleEnvironmentProperties import RoleEnvironmentProperties
from ClassAssociationParameters import ClassAssociationParameters
from DomainAssociationParameters import DomainAssociationParameters
from GoalAssociationParameters import GoalAssociationParameters
from DependencyParameters import DependencyParameters
from DomainPropertyParameters import DomainPropertyParameters
from DomainParameters import DomainParameters
from Domain import Domain
from ValueType import ValueType
from ValueTypeParameters import ValueTypeParameters
from ExternalDocumentParameters import ExternalDocumentParameters
from PersonaCharacteristicParameters import PersonaCharacteristicParameters
from TaskCharacteristicParameters import TaskCharacteristicParameters
from UseCase import UseCase
from UseCaseParameters import UseCaseParameters

def build(objtId,p):
  if (p.__class__.__name__ == 'AttackerParameters'):
    return Attacker(objtId,p.name(),p.description(),p.image(),p.tags(),p.environmentProperties())
  if (p.__class__.__name__ == 'PersonaParameters'):
    return Persona(objtId,p.name(),p.activities(),p.attitudes(),p.aptitudes(),p.motivations(),p.skills(),p.image(),p.assumption(),p.type(),p.environmentProperties())
  if (p.__class__.__name__ == 'AssetParameters'):
    return Asset(objtId,p.name(),p.shortCode(),p.description(),p.significance(),p.type(),p.critical(),p.criticalRationale(),p.tags(),p.interfaces(),p.environmentProperties())
  if (p.__class__.__name__ == 'TemplateAssetParameters'):
    return TemplateAsset(objtId,p.name(),p.shortCode(),p.description(),p.significance(),p.type(),p.critical(),p.criticalRationale(),p.confidentialityProperty(),p.integrityProperty(),p.availabilityProperty(),p.accountabilityProperty(),p.anonymityProperty(),p.pseudonymityProperty(),p.unlinkabilityProperty(),p.unobservabilityProperty(),p.interfaces())
  if (p.__class__.__name__ == 'SecurityPatternParameters'):
    return SecurityPattern(objtId,p.name(),p.context(),p.problem(),p.solution(),p.requirements(),p.associations())
  if (p.__class__.__name__ == 'ValueTypeParameters'):
    return ValueType(objtId,p.name(),p.description(),p.type())
  if (p.__class__.__name__ == 'ClassAssociationParameters'):
    return ClassAssociation(objtId,p.environment(),p.headAsset(),p.headDimension(),p.headNavigation(),p.headType(),p.headMultiplicity(),p.headRole(),p.tailRole(),p.tailMultiplicity(),p.tailType(),p.tailNavigation(),p.tailDimension(),p.tailAsset(),p.rationale())
  if (p.__class__.__name__ == 'DomainAssociationParameters'):
    return DomainAssociation(objtId,p.headDomain(),p.tailDomain(),p.phenomena(),p.connectionDomain())
  if (p.__class__.__name__ == 'GoalAssociationParameters'):
    return GoalAssociation(objtId,p.environment(),p.goal(),p.goalDimension(),p.type(),p.subGoal(),p.subGoalDimension(),p.alternative(),p.rationale())
  if (p.__class__.__name__ == 'DependencyParameters'):
    return Dependency(objtId,p.environment(),p.depender(),p.dependee(),p.dependencyType(),p.dependency(),p.rationale())
  if (p.__class__.__name__ == 'GoalParameters'):
    return Goal(objtId,p.name(),p.originator(),p.environmentProperties())
  if (p.__class__.__name__ == 'ObstacleParameters'):
    return Obstacle(objtId,p.name(),p.originator(),p.environmentProperties())
  if (p.__class__.__name__ == 'DomainPropertyParameters'):
    return DomainProperty(objtId,p.name(),p.description(),p.type(),p.originator())
  if (p.__class__.__name__ == 'ThreatParameters'):
    return Threat(objtId,p.name(),p.type(),p.method(),p.tags(),p.environmentProperties())
  if (p.__class__.__name__ == 'VulnerabilityParameters'):
    return Vulnerability(objtId,p.name(),p.description(),p.type(),p.tags(),p.environmentProperties())
  if (p.__class__.__name__ == 'RiskParameters'):
    return Risk(objtId,p.name(),p.threat(),p.vulnerability(),p.tags(),p.misuseCase())
  if (p.__class__.__name__ == 'ResponseParameters'):
    return Response(objtId,p.name(),p.risk(),p.environmentProperties(),p.responseType())
  if (p.__class__.__name__ == 'CountermeasureParameters'):
    return Countermeasure(objtId,p.name(),p.description(),p.type(),p.environmentProperties())
  if (p.__class__.__name__ == 'TaskParameters'):
    return Task(objtId,p.name(),p.shortCode(),p.objective(),p.assumption(),p.author(),p.environmentProperties())
  if (p.__class__.__name__ == 'UseCaseParameters'):
    return UseCase(objtId,p.name(),p.author(),p.code(),p.actors(),p.description(),p.environmentProperties())
  if (p.__class__.__name__ == 'MisuseCaseParameters'):
    return MisuseCase(objtId,p.name(),p.environmentProperties(),p.risk())
  if (p.__class__.__name__ == 'TraceParameters'):
    return Trace(p.fromObject(),p.fromName(),p.fromId(),p.toObject(),p.toName(),p.toId())
  if (p.__class__.__name__ == 'DotTraceParameters'):
    return DotTrace(p.fromObject(),p.fromName(),p.toObject(),p.toName())
  if (p.__class__.__name__ == 'UpdateTraceParameters'):
    return Trace(p.fromObject(),p.fromName(),p.fromId(),p.toObject(),p.toName(),p.toId())
  if (p.__class__.__name__ == 'EnvironmentParameters'):
    return Environment(objtId,p.name(),p.shortCode(),p.description(),p.environments(),p.duplicateProperty(),p.overridingEnvironment(),p.tensions())
  if (p.__class__.__name__ == 'RoleParameters'):
    return Role(objtId,p.name(),p.type(),p.shortCode(),p.description(),p.environmentProperties())
  if (p.__class__.__name__ == 'ResponsibilityParameters'):
    return Responsibility(objtId,p.name())
  if (p.__class__.__name__ == 'DomainParameters'):
    return Domain(objtId,p.name(),p.shortCode(),p.description(),p.type(),p.given(),p.domains())
  if (p.__class__.__name__ == 'ExternalDocumentParameters'):
    return ExternalDocument(objtId,p.name(),p.version(),p.date(),p.authors(),p.description())
  if (p.__class__.__name__ == 'DocumentReferenceParameters'):
    return DocumentReference(objtId,p.name(),p.document(),p.contributor(),p.description())
  if (p.__class__.__name__ == 'ConceptReferenceParameters'):
    return ConceptReference(objtId,p.name(),p.dimension(),p.objectName(),p.description())
  if (p.__class__.__name__ == 'PersonaCharacteristicParameters'):
    return PersonaCharacteristic(objtId,p.persona(),p.qualifier(),p.behaviouralVariable(),p.characteristic(),p.grounds(),p.warrant(),p.backing(),p.rebuttal())
  if (p.__class__.__name__ == 'TaskCharacteristicParameters'):
    return TaskCharacteristic(objtId,p.task(),p.qualifier(),p.characteristic(),p.grounds(),p.warrant(),p.backing(),p.rebuttal())
  else:
    raise UnknownParameterClass(str(objectId))
