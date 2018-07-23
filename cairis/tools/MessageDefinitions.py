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
from . import PseudoClasses

__author__ = 'Robin Quetin, Shamal Faily'

from . import ModelDefinitions

def gen_message_fields(class_ref):
  resource_fields = {
    "session_id": fields.String,
    "object": fields.Nested(class_ref.resource_fields),
  }
  return resource_fields

def gen_message_multival_fields(class_ref):
  resource_fields = {
    "session_id": fields.String,
    "object": fields.List(fields.Nested(class_ref.resource_fields))
  }
  return resource_fields

class DefaultMessage(object):
  required = ['object']

class AssetEnvironmentPropertiesMessage(DefaultMessage):
  resource_fields = gen_message_multival_fields(ModelDefinitions.AssetEnvironmentPropertiesModel)
  required = DefaultMessage.required

class AssetMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.AssetModel)
  required = DefaultMessage.required

class ObjectSummaryMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ObjectSummaryModel)
  required = DefaultMessage.required

class AssetAssociationMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.AssetAssociationModel)
  required = DefaultMessage.required

class GoalAssociationMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.GoalAssociationModel)
  required = DefaultMessage.required

class AttackerMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.AttackerModel)
  required = DefaultMessage.required

class CImportMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.CImportParams)
  required = DefaultMessage.required

class CExportMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.CExportParams)
  required = DefaultMessage.required

class DocumentationMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DocumentationParams)
  required = DefaultMessage.required

class DependencyMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DependencyModel)
  required = DefaultMessage.required

class EnvironmentMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.EnvironmentModel)
  required = DefaultMessage.required

class GoalMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.GoalModel)
  required = DefaultMessage.required

class ObstacleMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ObstacleModel)
  required = DefaultMessage.required

class DomainPropertyMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DomainPropertyModel)
  required = DefaultMessage.required

class CountermeasureMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.CountermeasureModel)
  required = DefaultMessage.required

class ProjectMessage(DefaultMessage):
  resource_fields = gen_message_fields(PseudoClasses.ProjectSettings)
  required = DefaultMessage.required

class RequirementMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.RequirementModel)
  required = DefaultMessage.required

class ResponseMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ResponseModel)
  required = DefaultMessage.required

class RiskMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.RiskModel)
  required = DefaultMessage.required

class RoleMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.RoleModel)
  required = DefaultMessage.required

class ThreatMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ThreatModel)
  required = DefaultMessage.required

class ValueTypeMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ValueTypeModel)
  required = DefaultMessage.required

class VulnerabilityMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.VulnerabilityModel)
  required = DefaultMessage.required

class PersonaMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.PersonaModel)
  required = DefaultMessage.required

class TaskMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TaskModel)
  required = DefaultMessage.required

class UseCaseMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.UseCaseModel)
  required = DefaultMessage.required

class FindMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.FindModel)
  required = DefaultMessage.required

class VersionMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.VersionModel)
  required = DefaultMessage.required

class ValidationMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ValidationModel)
  required = DefaultMessage.required

class ExternalDocumentMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ExternalDocumentModel)
  required = DefaultMessage.required

class DocumentReferenceMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DocumentReferenceModel)
  required = DefaultMessage.required

class ConceptReferenceMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ConceptReferenceModel)
  required = DefaultMessage.required

class PersonaCharacteristicMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.PersonaCharacteristicModel)
  required = DefaultMessage.required

class TaskCharacteristicMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TaskCharacteristicModel)
  required = DefaultMessage.required

class ObjectDependencyMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ObjectDependencyModel)
  required = DefaultMessage.required

class ArchitecturalPatternMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ArchitecturalPatternModel)
  required = DefaultMessage.required

class ValueTypeMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ValueTypeModel)
  required = DefaultMessage.required

class TemplateGoalMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TemplateGoalModel)
  required = DefaultMessage.required

class TemplateAssetMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TemplateAssetModel)
  required = DefaultMessage.required

class LocationsMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.LocationsModel)
  required = DefaultMessage.required

class TraceMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TraceModel)
  required = DefaultMessage.required

class SecurityPatternMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.SecurityPatternModel)
  required = DefaultMessage.required

class DataFlowMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DataFlowModel)
  required = DefaultMessage.required

class DirectoryMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DirectoryModel)
  required = DefaultMessage.required

class TrustBoundaryMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TrustBoundaryModel)
  required = DefaultMessage.required

class TemplateRequirementMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TemplateRequirementModel)
  required = DefaultMessage.required

class CountermeasureTaskMessage(DefaultMessage):
  resource_fields = fields.List(fields.Nested(ModelDefinitions.CountermeasureTask.resource_fields))
  required = DefaultMessage.required

class SummaryMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.SummaryModel)
  required = DefaultMessage.required

class WeaknessAnalysisMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.WeaknessAnalysisModel)
  required = DefaultMessage.required
