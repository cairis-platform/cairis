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
from flask_restful_swagger import swagger
import PseudoClasses

__author__ = 'Robin Quetin, Shamal Faily'

import ModelDefinitions

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

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.AssetEnvironmentPropertiesModel.__name__
)
# endregion
class AssetEnvironmentPropertiesMessage(DefaultMessage):
  resource_fields = gen_message_multival_fields(ModelDefinitions.AssetEnvironmentPropertiesModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.AssetModel.__name__
)
# endregion
class AssetMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.AssetModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.AssetAssociationModel.__name__
)
# endregion
class AssetAssociationMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.AssetAssociationModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.GoalAssociationModel.__name__
)
# endregion
class GoalAssociationMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.GoalAssociationModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.AttackerModel.__name__,
)
# endregion
class AttackerMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.AttackerModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.CImportParams.__name__
)
# endregion
class CImportMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.CImportParams)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.CExportParams.__name__
)
# endregion
class CExportMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.CExportParams)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.DocumentationParams.__name__
)
# endregion
class DocumentationMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DocumentationParams)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.DependencyModel.__name__
)
# endregion
class DependencyMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DependencyModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.EnvironmentModel.__name__
)
# endregion
class EnvironmentMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.EnvironmentModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.GoalModel.__name__
)
# endregion
class GoalMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.GoalModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ObstacleModel.__name__
)
# endregion
class ObstacleMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ObstacleModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.DomainPropertyModel.__name__
)
# endregion
class DomainPropertyMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DomainPropertyModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.CountermeasureModel.__name__
)
# endregion
class CountermeasureMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.CountermeasureModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=PseudoClasses.ProjectSettings.__name__
)
# endregion
class ProjectMessage(DefaultMessage):
  resource_fields = gen_message_fields(PseudoClasses.ProjectSettings)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.RequirementModel.__name__
)
# endregion
class RequirementMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.RequirementModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ResponseModel.__name__
)
# endregion
class ResponseMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ResponseModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.RiskModel.__name__
)
# endregion
class RiskMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.RiskModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.RoleModel.__name__,
  property_0=ModelDefinitions.RoleEnvironmentPropertiesModel.__name__
)
# endregion
class RoleMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.RoleModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ThreatModel.__name__
)
# endregion
class ThreatMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ThreatModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ValueTypeModel.__name__
)
# endregion
class ValueTypeMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ValueTypeModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.VulnerabilityModel.__name__
)
# endregion
class VulnerabilityMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.VulnerabilityModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.PersonaEnvironmentPropertiesModel.__name__
)
# endregion
class PersonaEnvironmentPropertiesMessage(DefaultMessage):
  resource_fields = gen_message_multival_fields(ModelDefinitions.PersonaEnvironmentPropertiesModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.PersonaModel.__name__,
)
# endregion
class PersonaMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.PersonaModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.TaskModel.__name__,
)
# endregion
class TaskMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TaskModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.UseCaseModel.__name__,
)
# endregion
class UseCaseMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.UseCaseModel)
  required = DefaultMessage.required


# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.FindModel.__name__,
)
# endregion
class FindMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.FindModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ExternalDocumentModel.__name__,
)
# endregion
class ExternalDocumentMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ExternalDocumentModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.DocumentReferenceModel.__name__,
)
# endregion
class DocumentReferenceMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.DocumentReferenceModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ConceptReferenceModel.__name__,
)
# endregion
class ConceptReferenceMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ConceptReferenceModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.PersonaCharacteristicModel.__name__,
)
# endregion
class PersonaCharacteristicMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.PersonaCharacteristicModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.TaskCharacteristicModel.__name__,
)
# endregion
class TaskCharacteristicMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TaskCharacteristicModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ObjectDependencyModel.__name__,
)
# endregion
class ObjectDependencyMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ObjectDependencyModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ArchitecturalPatternModel.__name__,
)
# endregion
class ArchitecturalPatternMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ArchitecturalPatternModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.ValueTypeModel.__name__,
)
# endregion
class ValueTypeMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.ValueTypeModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.TemplateGoalModel.__name__,
)
# endregion
class TemplateGoalMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TemplateGoalModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.TemplateAssetModel.__name__,
)
# endregion
class TemplateAssetMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TemplateAssetModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.TemplateRequirementModel.__name__,
)
# endregion

class LocationsMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.LocationsModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.LocationsModel.__name__,
)
# endregion

class TraceMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.TraceModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.TraceModel.__name__,
)
# endregion

class SecurityPatternMessage(DefaultMessage):
  resource_fields = gen_message_fields(ModelDefinitions.SecurityPatternModel)
  required = DefaultMessage.required

# region Swagger Doc
@swagger.model
@swagger.nested(
  object=ModelDefinitions.SecurityPatternModel.__name__,
)
# endregion

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
