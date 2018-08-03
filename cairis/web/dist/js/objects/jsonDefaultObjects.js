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
  "rationale": "None",
  "value": "None",
  "name": "Confidentiality"
};
var IntegritySecurityAttribute =
{
  "rationale": "None",
  "value": "None",
  "name": "Integrity"
};
var AvailabilitySecurityAttribute =
{
  "rationale": "None",
  "value": "None",
  "name": "Availability"
};
var AccountabilitySecurityAttribute =
{
  "rationale": "None",
  "value": "None",
  "name": "Accountability"
};
var AnonymitySecurityAttribute =
{
  "rationale": "None",
  "value": "None",
  "name": "Anonymity"
};
var PseudonymitySecurityAttribute =
{
  "rationale": "None",
  "value": "None",
  "name": "Pseudonymity"
};
var UnlinkabilitySecurityAttribute =
{
  "rationale": "None",
  "value": "None",
  "name": "Unlinkability"
};
var UnobservabilitySecurityAttribute =
{
  "rationale": "None",
  "value": "None",
  "name": "Unobservability"
};
var assetEnvironmentDefault =
{
  "theAssociations": [],
  "theProperties": [ConfidentialitySecurityAttribute,IntegritySecurityAttribute,AvailabilitySecurityAttribute,AccountabilitySecurityAttribute,AnonymitySecurityAttribute,PseudonymitySecurityAttribute,UnlinkabilitySecurityAttribute,UnobservabilitySecurityAttribute],
  "theEnvironmentName": ""
};
var assetDefault =
{
  "theDescription" : "",
  "theSignificance" : "",
  "theTags" : [],
  "theCriticalRationale" : "",
  "theInterfaces" : [],
  "theType" : "",
  "theName" : "",
  "isCritical" : 0,
  "theShortCode" : "",
  "theEnvironmentProperties": []
};

var templateAssetDefault = {
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
  "theType": "",
  "theName": "",
  "theShortCode": "",
  "theDescription": ""
};
var tensionDefault = {
  "rationale": "",
  "attr_id": -1,
  "base_attr_id": -1,
  "value": -1
};
var environmentDefault = {
  "theDuplicateProperty": "",
  "theTensions": [],
  "theName": "",
  "theEnvironments": [],
  "theShortCode": "",
  "theDescription": "",
  "theOverridingEnvironment": ""
};
var vulnerabilityDefault = {
  "theVulnerabilityName": "",
  "theVulnerabilityType": "",
  "theTags": [],
  "theVulnerabilityDescription": "",
  "theEnvironmentProperties": []
};
var vulEnvironmentsDefault = {
  "theEnvironmentName": "",
  "theAssets": [],
  "theSeverity": ""
};
var threatEnvironmentDefault = {
  "theAssets": [],
  "theLikelihood": "",
  "theEnvironmentName": "",
  "theAttackers": [],
  "theProperties": [ConfidentialitySecurityAttribute,IntegritySecurityAttribute,AvailabilitySecurityAttribute,AccountabilitySecurityAttribute,AnonymitySecurityAttribute,PseudonymitySecurityAttribute,UnlinkabilitySecurityAttribute,UnobservabilitySecurityAttribute]
};
var threatDefault = {
  "theTags": [],
  "theThreatName": "",
  "theType": "",
  "theMethod": "",
  "theEnvironmentProperties": []
};

var attackerEnvDefault = {
  "theRoles": [],
  "theMotives": [],
  "theCapabilities": [],
  "theEnvironmentName": ""
};

var attackerDefault = {
  "theDescription": "",
  "theTags": [],
  "theName": "",
  "theImage": "",
  "theEnvironmentProperties": []
};

var taskEnvDefault = {
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
  "theName": "",
  "theShortCode": "",
  "theObjective": "",
  "isAssumption": false,
  "theAuthor": "",
  "theTags": [],
  "theEnvironmentProperties": []
};

var useCaseEnvDefault = {
  "theEnvironmentName": "",
  "thePreCond": "",
  "theSteps": [],
  "thePostCond": ""
};

var useCaseDefault = {
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
  "theDirectFlag": 1,
  "theNarrative": "",
  "theRoles": []
};

var personaDefault = {
  "theDescription": "",
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
  "theFitCriterion": "None",
  "theConcerns": [],
  "theSubGoalRefinements": [],
  "thePriority": "Low",
  "theEnvironmentName": "",
  "theCategory": "Maintain",
  "theDefinition": "None",
  "theConcernAssociations": [],
  "theGoalRefinements": [],
  "theIssue": ""
};
var goalDefault = {
  "theOriginator": "",
  "theTags": [],
  "theName": "",
  "theEnvironmentProperties": []
};

var obstacleEnvDefault =     {
  "theDefinition": "None",
  "theCategory": "Vulnerability",
  "theGoalRefinements": [],
  "theSubGoalRefinements": [],
  "theConcerns": [],
  "theProbability": "0",
  "theProbabilityRationale": "None",
  "theEnvironmentName": ""
};
var obstacleDefault = {
  "theName": "",
  "theTags": [],
  "theOriginator": "",
  "theEnvironmentProperties": []
};

var countermeasureEnvDefault =     {
  "theEnvironmentName": "",
  "theRequirements": [],
  "theTargets": [],
  "theProperties": [ConfidentialitySecurityAttribute,IntegritySecurityAttribute,AvailabilitySecurityAttribute,AccountabilitySecurityAttribute,AnonymitySecurityAttribute,PseudonymitySecurityAttribute,UnlinkabilitySecurityAttribute,UnobservabilitySecurityAttribute],
  "theRationale": [],
  "theRoles": [],
  "thePersonas": []
};
var countermeasureDefault = {
  "theName": "",
  "theTags": [],
  "theDescription": "",
  "theType": "",
  "theEnvironmentProperties": []
};
var respRoleDefault = {
  "roleName": "",
  "cost": ""
};
var acceptEnvDefault = {
  "theCost": "",
  "theRationale": "",
  "theEnvironmentName": ""
};
var transferEnvDefault = {
  "theRationale": "",
  "theRoles": [],
  "theEnvironmentName": ""
};
var mitigateEnvDefault = {
  "theDetectionMechanisms": [],
  "theDetectionPoint": "",
  "theType": "",
  "theEnvironmentName" : ""
};

var domainPropertyDefault = {
  "theName": "",
  "theTags": [],
  "theDescription": "",
  "theType": "",
  "theOriginator": ""
};
var dependencyDefault = {
  "theDependencyType": "goal",
  "theRationale": "",
  "theEnvironmentName": "",
  "theDepender": "",
  "theDependee": "",
  "theDependency": ""
};
var classAssociationDefault = {
  "theEnvironmentName" : "",
  "theHeadAsset" : "",
  "theHeadType" : "",
  "theHeadNavigation" : "",
  "theHeadMultiplicity" : "",
  "theHeadRole" : "",
  "theTailRole" : "",
  "theTailMultiplicity" : "",
  "theTailType" : "",
  "theTailNavigation" : "",
  "theTailAsset" : "",
  "theRationale" : ""
};
var goalAssociationDefault = {
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
  "theName" : "",
  "theVersion" : "",
  "thePublicationDate" : "",
  "theAuthors" : "",
  "theDescription" : ""
};
var documentReferenceDefault = {
  "theName" : "",
  "theDocName" : "",
  "theContributor" : "",
  "theExcerpt" : ""
};
var conceptReferenceDefault = {
  "theName" : "",
  "theDimName" : "",
  "theObjtName" : "",
  "theDescription" : ""
};

var referenceContributionDefault = {
  "theMeansEnd" : "",
  "theContribution" : ""
};

var referenceSynopsisDefault = {
  "theActor" : "",
  "theSynopsis" : "",
  "theDimension" : "",
  "theActorType" : ""
};

var characteristicReferenceDefault = {
  "theReferenceName" : "",
  "theDimensionName" : "document",
  "theCharacteristicType" : "grounds",
  "theReferenceDescription" : "",
  "theReferenceSynopsis" : referenceSynopsisDefault,
  "theReferenceContribution" : referenceContributionDefault
};

var personaCharacteristicDefault = {
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
  "theTaskName" : "",
  "theModQual" : "",
  "theCharacteristic" : "",
  "theGrounds" : [],
  "theWarrant" : [],
  "theRebuttal" : [],
  "theBacking" :[] 
};
var valueTypeDefault = {
  "theName" : "",
  "theType" : "",
  "theEnvironmentName" : "all",
  "theDescription" : "",
  "theRationale" : "None",
  "theScore" : 0
};
var responseDefault = {
  "theRisk" : "",
  "theName" : "",
  "theEnvironmentProperties" : {'accept': [], 'mitigate' : [], 'transfer' : []},
  "theResponseType" : "",
  "theTags" : []
};

var riskRatingDefault = {
  "environment" : "",
  "rating" : "",
  "threat" : "",
  "vulnerability" : "" 
};

var misuseCaseEnvironmentDefault = {
  "theAssets" : [],
  "theAttackers" : [],
  "theDescription" : [],
  "theEnvironmentName" : [],
  "theLikelihood" : "",
  "theObjective" : "",
  "theRiskRating" : riskRatingDefault
};

var misuseCaseDefault = {
  "theName" : "",
  "theRiskName" : "",
  "theThreatName" : "",
  "theVulnerabilityName" : "",
  "theEnvironmentProperties" : []
};

var riskDefault = {
  "theVulnerabilityName" : "",
  "theMisuseCase" : "",
  "theTags" : [],
  "theThreatName" : "",
  "theRiskName" : ""
};

var componentDefault = {
  "theName" : "",
  "theDescription": "",
  "theInterfaces" : [],
  "theStructure" : [],
  "theRequirements" : [],
  "theGoals" : [],
  "theGoalAssociations" : []
};

var connectorDefault = {
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
  "theName" : "",
  "theSynopsis" : "",
  "theComponents" : [],
  "theConnectors" : []
};
var templateRequirementDefault = {
  "theName" : "",
  "theAssetName" : "",
  "theType" : "",
  "theDescription" : "",
  "theRationale" : "",
  "theFitCriterion" : ""
};
var templateGoalDefault = {
  "theName" : "",
  "theDefinition" : "",
  "theRationale" : "",
  "theConcerns" : [],
  "theResponsibilities" : []
};
var locationDefault = {
  "theName" : "",
  "theAssetInstances" : [],
  "thePersonaInstances" : [],
  "theLinks" : []
};
var locationsDefault = {
  "theName" : "",
  "theDiagram" : "",
  "theLocations" : []
};
var securityPatternDefault = {
  "theName" : "",
  "theContext" : "",
  "theProblem" : "",
  "theSolution" : "",
  "theRequirements" : [],
  "theConcernAssociations" : []
};
var dataflowDefault = {
  "theName" : "",
  "theEnvironmentName" : "",
  "theFromName" : "",
  "theFromType" : "entity",
  "theToName" : "",
  "theToType" : "process",
  "theAssets" : []
};
var trustBoundaryDefault = {
  "theName" : "",
  "theDescription" : "",
  "theEnvironmentProperties" : []
};
