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

from flask.ext.restful import fields
from flask.ext.restful_swagger import swagger
from cairis.core.AcceptEnvironmentProperties import AcceptEnvironmentProperties

from cairis.core.Asset import Asset
from cairis.core.AssetEnvironmentProperties import AssetEnvironmentProperties
from cairis.core.Attacker import Attacker
from cairis.core.AttackerEnvironmentProperties import AttackerEnvironmentProperties
from cairis.core.Dependency import Dependency
from cairis.core.Goal import Goal
from cairis.core.GoalEnvironmentProperties import GoalEnvironmentProperties
from cairis.core.MisuseCase import MisuseCase
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.MitigateEnvironmentProperties import MitigateEnvironmentProperties
from cairis.core.Requirement import Requirement
from cairis.core.Risk import Risk
from cairis.core.Role import Role
from cairis.core.ThreatEnvironmentProperties import ThreatEnvironmentProperties
from cairis.core.TransferEnvironmentProperties import TransferEnvironmentProperties
from cairis.core.ValueType import ValueType
from cairis.core.Vulnerability import Vulnerability
from cairis.core.VulnerabilityEnvironmentProperties import VulnerabilityEnvironmentProperties
from cairis.tools.PseudoClasses import EnvironmentTensionModel, SecurityAttribute, ValuedRole, RiskRating

__author__ = 'Robin Quetin'

obj_id_field = "__python_obj__"
likelihood_metadata = { "enum": ['Incredible', 'Improbable', 'Remote', 'Occasional', 'Probable', 'Frequent'] }
severity_metadata = { "enum": ['Negligible', 'Marginal', 'Critical', 'Catastrophic'] }
def gen_class_metadata(class_ref):
    return {
        "enum": [class_ref.__module__+'.'+class_ref.__name__]
    }

@swagger.model
@swagger.nested(attributes=SecurityAttribute.__name__)
class AssetEnvironmentPropertiesModel(object):
    def __init__(self, env_name='', associations=[], attributes=[]):
        self.environment = env_name
        self.associations = associations
        self.attributes = attributes
        self.attributesDictionary = {}

    def json_prepare(self):
        self.attributes = self.attributesDictionary.values()
        self.attributesDictionary = {}
        for idx in range(0, len(self.associations)):
            self.associations[idx] = list(self.associations[idx])

    resource_fields = {
        "__python_obj__": fields.String,
        "theAssociations": fields.List(fields.List(fields.String)),
        "theProperties": fields.List(fields.Nested(SecurityAttribute.resource_fields)),
        "theEnvironmentName": fields.String,
        "theRationale": fields.List(fields.String)
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove("theRationale")
    swagger_metadata = {
        obj_id_field: gen_class_metadata(AssetEnvironmentProperties)
    }

@swagger.model
@swagger.nested(
    theEnvironmentProperties=AssetEnvironmentPropertiesModel.__name__
)
class AssetModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theDescription": fields.String,
        "theSignificance": fields.String,
        "theId": fields.Integer,
        "theTags": fields.List(fields.String),
        "theCriticalRationale": fields.String,
        "theInterfaces": fields.List(fields.String),
        "theType": fields.String,
        "theName": fields.String,
        "isCritical": fields.Integer,
        "theShortCode": fields.String,
        "theEnvironmentProperties": fields.List(fields.Nested(AssetEnvironmentPropertiesModel.resource_fields))
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field : gen_class_metadata(Asset)
    }


@swagger.model
class CapabilityModel(object):
    resource_fields = {
        "name": fields.String,
        "value": fields.String
    }
    required = resource_fields.keys()

@swagger.model
@swagger.nested(
    theCapabilities=CapabilityModel.__name__
)
class AttackerEnvironmentPropertiesModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theMotives': fields.List(fields.String),
        'theRoles': fields.List(fields.String),
        'theCapabilities': fields.List(fields.Nested(CapabilityModel.resource_fields)),
        'theEnvironmentName': fields.String,
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field: gen_class_metadata(AttackerEnvironmentProperties)
    }

@swagger.model
@swagger.nested(
    theEnvironmentProperties=AttackerEnvironmentPropertiesModel.__name__
)
class AttackerModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theEnvironmentDictionary': fields.List(fields.Nested(AttackerEnvironmentPropertiesModel.resource_fields)),
        'theDescription': fields.String,
        'theId': fields.Integer,
        'theTags': fields.List(fields.String),
        'isPersona': fields.Integer,
        'theName': fields.String,
        'theImage': fields.String,
        'theEnvironmentProperties': fields.List(fields.Nested(AttackerEnvironmentPropertiesModel.resource_fields)),
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove('theEnvironmentDictionary')
    swagger_metadata = {
        obj_id_field: gen_class_metadata(Attacker)
    }

@swagger.model
class CImportParams(object):
    resource_fields = {
        'urlenc_file_contents': fields.String,
        'type': fields.String,
        'overwrite': fields.Integer
    }
    required = resource_fields.keys()
    required.remove('overwrite')
    swagger_metadata = {
        'type': {
            'enum': [
                'securitypattern',
                'attackpattern',
                'tvtypes',
                'directory',
                'requirements',
                'riskanalysis',
                'usability',
                'project',
                'domainvalues',
                'architecturalpattern',
                'associations',
                'synopses',
                'processes',
                'assets',
                'all'
            ]
        }
    }

@swagger.model
class DependencyModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theDependencyType': fields.String,
        'theRationale': fields.String,
        'theEnvironmentName': fields.String,
        'theDepender': fields.String,
        'theDependee': fields.String,
        'theDependency': fields.String,
        'theId': fields.Integer,
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metamodel = {
        obj_id_field : gen_class_metadata(Dependency)
    }

@swagger.model
@swagger.nested(
    theTensions=EnvironmentTensionModel.__name__,
)
class EnvironmentModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theId": fields.Integer,
        "theName": fields.String,
        "theShortCode": fields.String,
        "theDescription": fields.String,
        "theEnvironments": fields.List(fields.String),
        "theDuplicateProperty": fields.String,
        "theOverridingEnvironment": fields.String,
        "theTensions": fields.List(fields.Nested(EnvironmentTensionModel.resource_fields)),
        }
    required = resource_fields.keys()
    required.remove(obj_id_field)

@swagger.model
class GoalEnvironmentPropertiesModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theCategory": fields.String,
        "theConcernAssociations": fields.List(fields.String),
        "theConcerns": fields.List(fields.String),
        "theDefinition": fields.String,
        "theEnvironmentName": fields.String,
        "theFitCriterion": fields.String,
        "theGoalRefinements": fields.List(fields.String),
        "theIssue": fields.String,
        "theLabel": fields.String,
        "thePriority": fields.String,
        "theSubGoalRefinements": fields.List(fields.String)
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field : gen_class_metadata(GoalEnvironmentProperties)
    }

@swagger.model
@swagger.nested(
    theEnvironmentProperties=GoalEnvironmentPropertiesModel.__name__
)
class GoalModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theColour": fields.String,
        "theEnvironmentDictionary": fields.List,
        "theEnvironmentProperties": fields.List(fields.Nested(GoalEnvironmentPropertiesModel.resource_fields)),
        "theId": fields.Integer,
        "theName": fields.String,
        "theOriginator": fields.String,
        "theTags": fields.List(fields.String)
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove("theEnvironmentDictionary")
    swagger_metadata = {
        obj_id_field : gen_class_metadata(Goal)
    }

@swagger.model
@swagger.nested(
    theRiskRating=RiskRating.__name__
)
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
    swagger_metadata = {
        obj_id_field : gen_class_metadata(MisuseCaseEnvironmentProperties),
        "theLikelihood": likelihood_metadata,
        "theSeverity": severity_metadata
    }

@swagger.model
@swagger.nested(
    theEnvironmentProperties=MisuseCaseEnvironmentPropertiesModel.__name__
)
class MisuseCaseModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theId": fields.Integer,
        "theName": fields.String,
        "theThreatName": fields.String,
        "theRiskName": fields.String,
        "theVulnerabilityName": fields.String,
        "theEnvironmentDictionary": fields.List(fields.Nested(MisuseCaseEnvironmentPropertiesModel.resource_fields)),
        "theEnvironmentProperties": fields.List(fields.Nested(MisuseCaseEnvironmentPropertiesModel.resource_fields))
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove("theEnvironmentDictionary")
    swagger_metadata = {
        obj_id_field : gen_class_metadata(MisuseCase)
    }

@swagger.model
class RequirementAttributesModel(object):
    resource_fields = {
        "originator": fields.String,
        "supportingMaterial": fields.String,
        "fitCriterion": fields.String,
        "asset": fields.String,
        "rationale": fields.String,
        "type": fields.String
    }

@swagger.model
@swagger.nested(
    dirtyAttrs=RequirementAttributesModel.__name__,
    attrs=RequirementAttributesModel.__name__
)
class RequirementModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theId": fields.Integer,
        "dirtyAttrs": fields.Nested(RequirementAttributesModel.resource_fields),
        "attrs": fields.Nested(RequirementAttributesModel.resource_fields),
        "theName": fields.String,
        "theLabel": fields.String,
        "theDescription": fields.String,
        "thePriority": fields.Integer,
        "theVersion": fields.Integer
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field : gen_class_metadata(Requirement)
    }


@swagger.model
class AcceptEnvironmentPropertiesModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theCost': fields.String,
        'theRationale': fields.String,
        'theEnvironmentName': fields.String
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = { obj_id_field: gen_class_metadata(AcceptEnvironmentProperties) }


@swagger.model
class MitigateEnvironmentPropertiesModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theDetectionMechanisms': fields.List(fields.String),
        'theDetectionPoint': fields.String,
        'theType': fields.String,
        'theEnvironmentName': fields.String,
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = { obj_id_field: gen_class_metadata(MitigateEnvironmentProperties) }


@swagger.model
@swagger.nested(
    theRoles=ValuedRole.__name__
)
class TransferEnvironmentPropertiesModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theRoles': fields.List(fields.Nested(ValuedRole.resource_fields)),
        'theRationale': fields.String,
        'theEnvironmentName': fields.String
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = { obj_id_field: gen_class_metadata(TransferEnvironmentProperties) }


@swagger.model
@swagger.nested(
    accept=AcceptEnvironmentPropertiesModel.__name__,
    mitigate=MitigateEnvironmentPropertiesModel.__name__,
    transfer=TransferEnvironmentPropertiesModel.__name__,
)
class ResponseEnvironmentPropertiesModel(object):
    resource_fields = {
        'accept': fields.List(fields.Nested(AcceptEnvironmentPropertiesModel.resource_fields)),
        'mitigate': fields.List(fields.Nested(MitigateEnvironmentPropertiesModel.resource_fields)),
        'transfer': fields.List(fields.Nested(TransferEnvironmentPropertiesModel.resource_fields))
    }
    field_names = resource_fields.keys()


@swagger.model
@swagger.nested(
    theEnvironmentProperties=ResponseEnvironmentPropertiesModel.__name__
)
class ResponseModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theId': fields.Integer,
        'theTags': fields.List(fields.String),
        'theRisk': fields.String,
        'theName': fields.String,
        'theEnvironmentProperties': fields.Nested(ResponseEnvironmentPropertiesModel.resource_fields),
        'theResponseType': fields.String
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)

@swagger.model
@swagger.nested(
    theMisuseCase=MisuseCaseModel.__name__
)
class RiskModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theVulnerabilityName": fields.String,
        "theId": fields.Integer,
        "theMisuseCase": fields.Nested(MisuseCaseModel.resource_fields),
        "theTags": fields.List(fields.Nested(fields.String)),
        "theThreatName": fields.String,
        "theName": fields.String
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field : gen_class_metadata(Risk)
    }


@swagger.model
class RoleModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theId": fields.Integer,
        "theName": fields.String,
        "theType": fields.String,
        "theShortCode": fields.String,
        "theDescription": fields.String,
        "theEnvironmentProperties": None
    }

    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove("theEnvironmentProperties")

    swagger_metadata = {
        obj_id_field : gen_class_metadata(Role)
    }

@swagger.model
class RoleEnvironmentPropertiesModel(object):
    resource_fields = {
        "theEnvironmentName": fields.String,
        "theResponses": fields.List(fields.List(fields.String)),
        "theCountermeasures": fields.List(fields.String)
    }
    required = resource_fields.keys()

@swagger.model
@swagger.nested(
    theProperties=SecurityAttribute.__name__
)
class ThreatEnvironmentPropertiesModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theAssets': fields.List(fields.String),
        'theLikelihood': fields.String,
        'theEnvironmentName': fields.String,
        'theAttackers': fields.List(fields.String),
        'theRationale': fields.List(fields.String),
        'theProperties': fields.List(fields.Nested(SecurityAttribute.resource_fields)),
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove('theRationale')
    swagger_metadata = {
        obj_id_field : gen_class_metadata(ThreatEnvironmentProperties),
        'theLikelihood' : likelihood_metadata
    }

@swagger.model
@swagger.nested(
    theEnvironmentProperties=ThreatEnvironmentPropertiesModel.__name__
)
class ThreatModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theEnvironmentDictionary': fields.List(fields.String),
        'theId': fields.Integer,
        'theTags': fields.List(fields.String),
        'theThreatPropertyDictionary': fields.List(fields.String),
        'theThreatName': fields.String,
        'theType': fields.String,
        'theMethod': fields.String,
        'theEnvironmentProperties': fields.List(fields.Nested(ThreatEnvironmentPropertiesModel.resource_fields)),
        'likelihoodLookup': fields.List(fields.String),
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove('theThreatPropertyDictionary')
    required.remove('theEnvironmentDictionary')
    required.remove('likelihoodLookup')

@swagger.model
class UserConfigModel(object):
    resource_fields = {
        "user": fields.String,
        "passwd": fields.String,
        "db": fields.String,
        "host": fields.String,
        "port": fields.Integer,
        "jsonPrettyPrint": fields.String
    }
    required = resource_fields.keys()
    required.remove("jsonPrettyPrint")
    swagger_metadata = {
        'jsonPrettyPrint':
            {
                'enum': ['on', 'off']
            }
    }

@swagger.model
class ValueTypeModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theScore': fields.Integer,
        'theId': fields.Integer,
        'theRationale': fields.String,
        'theType': fields.String,
        'theName': fields.String,
        'theDescription': fields.String,
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field: gen_class_metadata(ValueType),
        "theType": {
            "enum": ['asset_value','threat_value','risk_class','countermeasure_value','capability','motivation','asset_type','threat_type','vulnerability_type','severity','likelihood','access_right','protocol','privilege','surface_type']
        }
    }

@swagger.model
class VulnerabilityEnvironmentPropertiesModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        "theAssets": fields.List(fields.String),
        "theEnvironmentName": fields.String,
        "theSeverity": fields.String
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field : gen_class_metadata(VulnerabilityEnvironmentProperties),
        "theSeverity": severity_metadata
    }

@swagger.model
@swagger.nested(
    theEnvironmentProperties=VulnerabilityEnvironmentPropertiesModel.__name__,
    theEnvironmentDictionary=VulnerabilityEnvironmentPropertiesModel.__name__
)
class VulnerabilityModel(object):
    resource_fields = {
        obj_id_field: fields.String,
        'theEnvironmentDictionary': fields.List(fields.Nested(VulnerabilityEnvironmentPropertiesModel.resource_fields)),
        'theVulnerabilityName': fields.String,
        'theVulnerabilityType': fields.String,
        'theTags': fields.List(fields.String),
        'theVulnerabilityDescription': fields.String,
        'theVulnerabilityId': fields.Integer,
        'severityLookup': fields.List(fields.String),
        'theEnvironmentProperties': fields.List(fields.Nested(VulnerabilityEnvironmentPropertiesModel.resource_fields))
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    required.remove('theEnvironmentDictionary')
    required.remove('severityLookup')
    swagger_metadata = {
        obj_id_field: gen_class_metadata(Vulnerability),
        'theVulnerabilityType' : {
            "enum": ['Configuration', 'Design', 'Implementation']
        }
    }
