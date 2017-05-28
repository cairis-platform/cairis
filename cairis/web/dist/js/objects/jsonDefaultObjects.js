/*  Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

    Authors: Raf Vandelaer, Shamal Faily */

'use strict';

var ConfidentialitySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Confidentiality"
};
var IntegritySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Integrity"
};
var AvailabilitySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Availability"
};
var AccountabilitySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Accountability"
};
var AnonymitySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Anonymity"
};
var PseudonymitySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Pseudonymity"
};
var UnlinkabilitySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Unlinkability"
};
var UnobservabilitySecurityAttribute =
{
  "__python_obj__": "tools.PseudoClasses.SecurityAttribute",
  "rationale": "None",
  "value": "None",
  "name": "Unobservability"
};
var assetEnvironmentDefault =
{
  "__python_obj__": "tools.ModelDefinitions.AssetEnvironmentPropertiesModel",
  "theAssociations": [],
  "theProperties": [ConfidentialitySecurityAttribute,IntegritySecurityAttribute,AvailabilitySecurityAttribute,AccountabilitySecurityAttribute,AnonymitySecurityAttribute,PseudonymitySecurityAttribute,UnlinkabilitySecurityAttribute,UnobservabilitySecurityAttribute],
  "theEnvironmentName": ""
};
var mainAssetObject =
{
  "__python_obj__": "Asset.Asset",
  "theEnvironmentDictionary": {},
  "theDescription": "",
  "theAssetPropertyDictionary": {},
  "theSignificance": "",
  "theId": -1,
  "theTags": [],
  "theCriticalRationale": "",
  "theInterfaces": [],
  "theType": "",
  "theName": "",
  "isCritical": 0,
  "theShortCode": "",
  "theEnvironmentProperties": []
};

var templateAssetDefault = {
  "__python_obj__": "TemplateAsset.TemplateAsset",
  "theId": -1,
  "theName": "",
  "theShortCode": "",
  "theDescription": "",
  "theSignificance": "",
  "theType": "",
  "theSurfaceType": "",
  "theAccessRight": "",
  "theProperties": [ConfidentialitySecurityAttribute,IntegritySecurityAttribute,AvailabilitySecurityAttribute,AccountabilitySecurityAttribute,AnonymitySecurityAttribute,PseudonymitySecurityAttribute,UnlinkabilitySecurityAttribute,UnobservabilitySecurityAttribute],
  "theTags": [],
  "theInterfaces": []
};

var roleDefaultObject = {
  "__python_obj__": "Role.Role",
  "theEnvironmentDictionary": {},
  "theEnvironmentProperties": [],
  "theId": -1,
  "costLookup": {},
  "theType": "",
  "theName": "",
  "theShortCode": "",
  "theDescription": ""
};
var tensionDefault = {
  "__python_obj__": "tools.PseudoClasses.EnvironmentTensionModel",
  "rationale": "",
  "attr_id": -1,
  "base_attr_id": -1,
  "value": -1
};
var environmentDefault = {"__python_obj__": "Environment.Environment",
  "theId": -1,
  "theDuplicateProperty": "",
  "theTensions": [],
  "theName": "",
  "theEnvironments": [],
  "theShortCode": "",
  "theDescription": "",
  "theOverridingEnvironment": ""
};
var vulnerabilityDefault = {
  "__python_obj__": "Vulnerability.Vulnerability",
  "theEnvironmentDictionary": {},
  "theVulnerabilityName": "",
  "theVulnerabilityType": "",
  "theTags": [],
  "theVulnerabilityDescription": "",
  "theVulnerabilityId": -1,
  "severityLookup": {},
  "theEnvironmentProperties": []
};
var vulEnvironmentsDefault = {
  "__python_obj__": "VulnerabilityEnvironmentProperties.VulnerabilityEnvironmentProperties",
  "theEnvironmentName": "",
  "theAssets": [],
  "theSeverity": ""
};
var threatEnvironmentDefault = {"__python_obj__": "ThreatEnvironmentProperties.ThreatEnvironmentProperties",
  "theAssets": [],
  "theLikelihood": "",
  "theEnvironmentName": "",
  "theAttackers": [],
  "theRationale": [],
  "theProperties": [ConfidentialitySecurityAttribute,IntegritySecurityAttribute,AvailabilitySecurityAttribute,AccountabilitySecurityAttribute,AnonymitySecurityAttribute,PseudonymitySecurityAttribute,UnlinkabilitySecurityAttribute,UnobservabilitySecurityAttribute]
};
var threatDefault = {
  "__python_obj__": "Threat.Threat",
  "theId": -1,
  "theTags": [],
  "theThreatName": "",
  "theType": "",
  "theMethod": "",
  "theEnvironmentProperties": [],
  "theProperties": []
};

var attackerEnvDefault = {
  "__python_obj__": "AttackerEnvironmentProperties.AttackerEnvironmentProperties",
  "theRoles": [],
  "theMotives": [],
  "theCapabilities": [],
  "theEnvironmentName": ""
};

var attackerDefault = {
  "__python_obj__": "Attacker.Attacker",
  "theDescription": "",
  "theId": -1,
  "theTags": [],
  "isPersona": false,
  "theName": "",
  "theImage": "",
  "theEnvironmentProperties": []
};

var taskEnvDefault = {
  "__python_obj__": "TaskEnvironmentProperties.TaskEnvironmentProperties",
  "theEnvironmentName": "",
  "thePersonas": [],
  "theAssets": [],
  "theDependencies": "",
  "theNarrative": "",
  "theConsequences": "",
  "theBenefits": "",
  "theConcernAssociations": [],
  "theCodes": []
};

var taskDefault = {
  "__python_obj__": "Task.Task",
  "theId": -1,
  "theName": "",
  "theShortCode": "",
  "theObjective": "",
  "isAssumption": false,
  "theAuthor": "",
  "theTags": [],
  "theEnvironmentProperties": []
};

var useCaseEnvDefault = {
  "__python_obj__": "UseCaseEnvironmentProperties.UseCaseEnvironmentProperties",
  "theEnvironmentName": "",
  "thePreCond": "",
  "theSteps": [],
  "thePostCond": ""
};

var useCaseDefault = {
  "__python_obj__": "UseCase.UseCase",
  "theId": -1,
  "theName": "",
  "theTags": [],
  "theAuthor": "",
  "theCode": "",
  "theObjective": "",
  "theActors": [],
  "theDescription": "",
  "theReferenceContributions" : [],
  "theEnvironmentProperties": []
};

var personaEnvDefault = {
  "__python_obj__": "PersonaEnvironmentProperties.PersonaEnvironmentProperties",
  "theDirectFlag": 1,
  "theNarrative": "",
  "theRoles": [],
  "theCodes": []
};

var personaDefault = {
  "__python_obj__": "Persona.Persona",
  "theDescription": "",
  "theId": -1,
  "theName": "",
  "theTags": [],
  "theActivities": "",
  "theAttitudes": "",
  "theAptitudes": "",
  "theMotivations": "",
  "theSkills": "",
  "theIntrinsic": "",
  "theContextual": "",
  "theImage": "",
  "isAssumption": 0,
  "thePersonaType": "Primary",
  "theEnvironmentProperties": []
};

var goalEnvDefault = { 
  "__python_obj__": "GoalEnvironmentProperties.GoalEnvironmentProperties",
  "theFitCriterion": "None",
  "theConcerns": [],
  "theSubGoalRefinements": [],
  "thePriority": "Low",
  "theEnvironmentName": "",
  "theCategory": "Maintain",
  "theDefinition": "None",
  "theConcernAssociations": [],
  "theGoalRefinements": [],
  "theLabel": "",
  "theIssue": ""
};
var goalDefault = {
  "__python_obj__": "Goal.Goal",
  "theColour": "",
  "theId": -1,
  "theOriginator": "",
  "theTags": [],
  "theName": "",
  "theEnvironmentProperties": []
};

var obstacleEnvDefault =     {
  "__python_obj__": "ObstacleEnvironmentProperties.ObstacleEnvironmentProperties",
  "theLabel": "",
  "theDefinition": "None",
  "theCategory": "Vulnerability",
  "theGoalRefinements": [],
  "theSubGoalRefinements": [],
  "theConcerns": [],
  "theProbability": "",
  "theProbabilityRationale": "",
  "theEnvironmentName": ""
};
var obstacleDefault = {
  "__python_obj__": "Obstacle.Obstacle",
  "theColour": "",
  "theId": -1,
  "theName": "",
  "theTags": [],
  "theOriginator": "",
  "theEnvironmentProperties": []
};

var countermeasureEnvDefault =     {
  "__python_obj__": "CountermeasureEnvironmentProperties.CountermeasureEnvironmentProperties",
  "theEnvironmentName": "",
  "theRequirements": [],
  "theTargets": [],
  "theProperties": [ConfidentialitySecurityAttribute,IntegritySecurityAttribute,AvailabilitySecurityAttribute,AccountabilitySecurityAttribute,AnonymitySecurityAttribute,PseudonymitySecurityAttribute,UnlinkabilitySecurityAttribute,UnobservabilitySecurityAttribute],
  "theRationale": [],
  "theRoles": [],
  "thePersonas": []
};
var countermeasureDefault = {
  "__python_obj__": "Countermeasure.Countermeasure",
  "theId": -1,
  "theName": "",
  "theTags": [],
  "theDescription": "",
  "theTyp": "",
  "theEnvironmentProperties": []
};
var respRoleDefault = {
  "__python_obj__": "tools.PseudoClasses.ValuedRole",
  "roleName": "",
  "cost": ""
};
var acceptEnvDefault = {
  "__python_obj__": "AcceptEnvironmentProperties.AcceptEnvironmentProperties",
  "theCost": "",
  "theRationale": "",
  "theEnvironmentName": ""
};
var transferEnvDefault = {
  "__python_obj__": "TransferEnvironmentProperties.TransferEnvironmentProperties",
  "theRationale": "",
  "theRoles": [],
  "theEnvironmentName": ""
};
var mitigateEnvDefault = {
  "__python_obj__": "MitigateEnvironmentProperties.MitigateEnvironmentProperties",
  "theDetectionMechanisms": [],
  "theDetectionPoint": "",
  "theType": "",
  "theEnvironmentName" : ""
};

var domainPropertyDefault = {
  "__python_obj__": "DomainProperty.DomainProperty",
  "theId": -1,
  "theName": "",
  "theTags": [],
  "theDescription": "",
  "theType": "",
  "theOriginator": ""
};
var dependencyDefault = {
  "__python_obj__": "Dependency.Dependency",
  "theId": -1,
  "theDependencyType": "goal",
  "theRationale": "",
  "theEnvironmentName": "",
  "theDepender": "",
  "theDependee": "",
  "theDependency": ""
};
var classAssociationDefault = {
  "__python_obj__": "ClassAssociation.ClassAssociation",
  "theId": -1,
  "theEnvironmentName" : "",
  "theHeadAsset" : "",
  "theHeadType" : "",
  "theHeadDim" : "",
  "theHeadNavigation" : "",
  "theHeadMultiplicity" : "",
  "theHeadRole" : "",
  "theTailRole" : "",
  "theTailMultiplicity" : "",
  "theTailType" : "",
  "theTailNavigation" : "",
  "theTailDim" : "",
  "theTailAsset" : "",
  "theRationale" : ""
};
var goalAssociationDefault = {
  "__python_obj__": "GoalAssociation.GoalAssociation",
  "theId": -1,
  "theEnvironmentName" : "",
  "theGoal" : "",
  "theGoalDimension" : "",
  "theAssociationType" : "",
  "theSubGoal" : "",
  "theSubGoalDimension" : "",
  "theAlternativeId" : "",
  "theRationale" : ""
};
var externalDocumentDefault = {
  "__python_obj__": "ExternalDocument.ExternalDocument",
  "theId": -1,
  "theName" : "",
  "theVersion" : "",
  "thePublicationDate" : "",
  "theAuthors" : "",
  "theDescription" : ""
};
var documentReferenceDefault = {
  "__python_obj__": "DocumentReference.DocumentReference",
  "theId": -1,
  "theName" : "",
  "theDocName" : "",
  "theContributor" : "",
  "theExcerpt" : ""
};
var conceptReferenceDefault = {
  "__python_obj__": "ConceptReference.ConceptReference",
  "theId": -1,
  "theName" : "",
  "theDimName" : "",
  "theObjtName" : "",
  "theDescription" : ""
};

var referenceContributionDefault = {
  "__python_obj__": "cairis.tools.PseudoClasses.CharacteristicReferenceContribution",
  "theId" : -1,
  "theMeansEnd" : "",
  "theContribution" : ""
};

var referenceSynopsisDefault = {
  "__python_obj__": "cairis.tools.PseudoClasses.CharacteristicReferenceSynopsis",
  "theId" : -1,
  "theActor" : "",
  "theSynopsis" : "",
  "theDimension" : "",
  "theActorType" : ""
};

var characteristicReferenceDefault = {
  "__python_obj__": "cairis.tools.PseudoClasses.CharacteristicReference",
  "theReferenceName" : "",
  "theDimensionName" : "document",
  "theCharacteristicType" : "grounds",
  "theReferenceDescription" : "",
  "theReferenceSynopsis" : referenceSynopsisDefault,
  "theReferenceContribution" : referenceContributionDefault
};

var personaCharacteristicDefault = {
  "__python_obj__": "PersonaCharacteristic.PersonaCharacteristic",
  "theId": -1,
  "thePersonaName" : "",
  "theModQual" : "",
  "theVariable" : "",
  "theCharacteristic" : "",
  "theCharacteristicSynopsis" : referenceSynopsisDefault,
  "theGrounds" : [],
  "theWarrant" : [],
  "theRebuttal" : [],
  "theBacking" :[] 
};
var taskCharacteristicDefault = {
  "__python_obj__": "TaskCharacteristic.TaskCharacteristic",
  "theId": -1,
  "theTaskName" : "",
  "theModQual" : "",
  "theCharacteristic" : "",
  "theGrounds" : [],
  "theWarrant" : [],
  "theRebuttal" : [],
  "theBacking" :[] 
};
var valueTypeDefault = {
  "__python_obj__": "ValueType.ValueType",
  "theId": -1,
  "theName" : "",
  "theType" : "",
  "theEnvironmentName" : "all",
  "theDescription" : "",
  "theRationale" : "None",
  "theScore" : 0
};
var responseDefault = {
  "__python_obj__": "Response.Response",
  "theId": -1,
  "theRisk" : "",
  "theName" : "",
  "theEnvironmentProperties" : {'accept': [], 'mitigate' : [], 'transfer' : []},
  "theResponseType" : "",
  "theTags" : []
};

var riskRatingDefault = {
  "__python_obj__": "PseudoClasses.RiskRating",
  "environment" : "",
  "rating" : "",
  "threat" : "",
  "vulnerability" : "" 
};

var misuseCaseEnvironmentDefault = {
  "__python_obj__": "MisuseCaseEnvironmentProperties.MisuseCaseEnvironmentProperties",
  "theAssets" : [],
  "theAttackers" : [],
  "theDescription" : [],
  "theEnvironmentName" : [],
  "theLikelihood" : "",
  "theObjective" : "",
  "theRiskRating" : riskRatingDefault
};

var misuseCaseDefault = {
  "__python_obj__": "MisuseCase.MisuseCase",
  "theId" : -1,
  "theName" : "",
  "theRiskName" : "",
  "theThreatName" : "",
  "theVulnerabilityName" : "",
  "theEnvironmentProperties" : []
};

var riskDefault = {
  "__python_obj__": "Risk.Risk",
  "theId" : -1,
  "theVulnerabilityName" : "",
  "theMisuseCase" : "",
  "theTags" : [],
  "theThreatName" : "",
  "theRiskName" : ""
};

var componentDefault = {
  "__python_obj__": "Component.Component",
  "theName" : "",
  "theDescription": "",
  "theInterfaces" : [],
  "theStructure" : [],
  "theRequirements" : [],
  "theGoals" : [],
  "theGoalAssociations" : []
};

var connectorDefault = {
  "__python_obj__": "Connector.Connector",
  "theConnectorName" : "",
  "theFromComponent" : "",
  "theFromRole" : "",
  "theFromInterface" : "",
  "theToComponent" : "",
  "theToRole" : "",
  "theToInterface" : "",
  "theAssetName" : "",
  "theProtocol" : "",
  "theAccessRight" : ""
};
var architecturalPatternDefault = {
  "__python_obj__": "ArchitecturalPattern.ArchitecturalPattern",
  "theId" : -1,
  "theName" : "",
  "theSynopsis" : "",
  "theComponents" : [],
  "theConnectors" : [],
  "theAttackSurfaceMetric" : [0,0,0]
};
var templateRequirementDefault = {
  "__python_obj__": "TemplateRequirement.TemplateRequirement",
  "theId" : -1,
  "theName" : "",
  "theAssetName" : "",
  "theType" : "",
  "theDescription" : "",
  "theRationale" : "",
  "theFitCriterion" : ""
};
var templateGoalDefault = {
  "__python_obj__": "TemplateGoal.TemplateGoal",
  "theId" : -1,
  "theName" : "",
  "theDefinition" : "",
  "theRationale" : "",
  "theConcerns" : [],
  "theResponsibilities" : []
};
var locationDefault = {
  "__python_obj__": "Location.Location",
  "theName" : "",
  "theAssetInstances" : [],
  "thePersonaInstances" : [],
  "theLinks" : []
};
var locationsDefault = {
  "__python_obj__": "Locations.Locations",
  "theId" : -1,
  "theName" : "",
  "theDiagram" : "",
  "theLocations" : []
};
var securityPatternDefault = {
  "__python_obj__": "SecurityPattern.SecurityPattern",
  "theId" : -1,
  "theName" : "",
  "theContext" : "",
  "theProblem" : "",
  "theSolution" : "",
  "theRequirements" : [],
  "theConcernAssociations" : []
};
var dataflowDefault = {
  "__python_obj__": "DataFlow.DataFlow",
  "theName" : "",
  "theEnvironmentName" : "",
  "theFromName" : "",
  "theFromType" : "",
  "theToName" : "",
  "theToType" : "",
  "theAssets" : []
};
