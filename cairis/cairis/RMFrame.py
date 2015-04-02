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


import wx 
import os
from NewEnvironmentDialog import NewEnvironmentDialog
from Borg import Borg
import MySQLDatabaseProxy
from ARM import *
from Environment import Environment
import armid
from EnvironmentsDialog import EnvironmentsDialog
from ArchitecturalPatternsDialog import ArchitecturalPatternsDialog
from AttackersDialog import AttackersDialog
from DomainPropertiesDialog import DomainPropertiesDialog
from GoalsDialog import GoalsDialog
from ObstaclesDialog import ObstaclesDialog
from AssetsDialog import AssetsDialog
from TemplateAssetsDialog import TemplateAssetsDialog
from TemplateRequirementsDialog import TemplateRequirementsDialog
from SecurityPatternsDialog import SecurityPatternsDialog
from ClassAssociationsDialog import ClassAssociationsDialog
from GoalAssociationsDialog import GoalAssociationsDialog
from DependenciesDialog import DependenciesDialog
from ThreatsDialog import ThreatsDialog
from VulnerabilitiesDialog import VulnerabilitiesDialog
from PersonasDialog import PersonasDialog
from TasksDialog import TasksDialog
from UseCasesDialog import UseCasesDialog
from RisksDialog import RisksDialog
from ResponsesDialog import ResponsesDialog
from CountermeasuresDialog import CountermeasuresDialog
from TracesDialog import TracesDialog
from EnvironmentModelViewer import EnvironmentModelViewer
from CanonicalModelViewer import CanonicalModelViewer
from ComponentModelViewer import ComponentModelViewer
from APModelViewer import APModelViewer
from ATModelViewer import ATModelViewer
from EnvironmentModel import EnvironmentModel
from AssumptionPersonaModel import AssumptionPersonaModel
from AssumptionTaskModel import AssumptionTaskModel
from AssetModel import AssetModel
from KaosModel import KaosModel
from DependentsDialog import DependentsDialog
from RolesDialog import RolesDialog
from TraceabilityEditor import TraceabilityEditor
from DimensionNameDialog import DimensionNameDialog
from DependentsDialog import DependentsDialog
from GenerateDocumentationDialog import GenerateDocumentationDialog
from ProjectSettingsDialog import ProjectSettingsDialog
from ValueTypesDialog import ValueTypesDialog
from ExternalDocumentsDialog import ExternalDocumentsDialog
from InternalDocumentsDialog import InternalDocumentsDialog
from CodesDialog import CodesDialog
from QuotationsDialog import QuotationsDialog
from DocumentReferencesDialog import DocumentReferencesDialog
from ConceptReferencesDialog import ConceptReferencesDialog
from PersonaCharacteristicsDialog import PersonaCharacteristicsDialog
from TaskCharacteristicsDialog import TaskCharacteristicsDialog
from ValueTypeParameters import ValueTypeParameters
from ModelImport import *
from SearchDialog import SearchDialog
from ConceptMapModel import ConceptMapModel
from ComponentModel import ComponentModel
from CodeNetworkModel import CodeNetworkModel
from CodeNetworkViewer import CodeNetworkViewer
from ImpliedProcessesDialog import ImpliedProcessesDialog
import DocumentBuilder
from itertools import izip
import gtk
import gtk.gdk
import xml.sax

from RMPanel import RMPanel
from GMPanel import GMPanel
from OMPanel import OMPanel

class RMFrame(wx.Frame):
  def __init__(self, parent, id, title):
    wx.Frame.__init__(self,parent,id,title, size=(900,500))
    self.b = Borg()
    self.dbProxy = self.b.dbProxy

    self.statusBar = self.CreateStatusBar()

    self.toolbar = self.CreateToolBar()

    self.directoryPrefix = self.b.imageDir + '/'
    dimIcon = wx.Icon(self.directoryPrefix + 'iris.png',wx.BITMAP_TYPE_PNG)
    self.SetIcon(dimIcon)

    pnewBmp = wx.ArtProvider.GetBitmap(wx.ART_NEW,wx.ART_TOOLBAR, (30,30))
    findBmp = wx.ArtProvider.GetBitmap(wx.ART_FIND,wx.ART_TOOLBAR,(30,30))
    settingsBmp = wx.Image(self.directoryPrefix + 'projectSettings.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    environmentBmp = wx.Image(self.directoryPrefix + 'environment.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    componentBmp = wx.Image(self.directoryPrefix + 'component.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    domainPropertiesBmp = wx.Image(self.directoryPrefix + 'domainproperty.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    goalsBmp = wx.Image(self.directoryPrefix + 'goal.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    obstaclesBmp = wx.Image(self.directoryPrefix + 'obstacle.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    saveBmp = wx.Image(self.directoryPrefix + 'commitEO.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    addBmp = wx.Image(self.directoryPrefix + 'addEO.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    deleteBmp = wx.Image(self.directoryPrefix + 'deleteEO.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    assetsBmp = wx.Image(self.directoryPrefix + 'asset.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    attackersBmp = wx.Image(self.directoryPrefix + 'attacker.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    threatsBmp = wx.Image(self.directoryPrefix + 'threat.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    vulnerabilitiesBmp = wx.Image(self.directoryPrefix + 'vulnerability.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    risksBmp = wx.Image(self.directoryPrefix + 'risk.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    responsesBmp = wx.Image(self.directoryPrefix + 'response.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    countermeasuresBmp = wx.Image(self.directoryPrefix + 'countermeasure.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    personasBmp = wx.Image(self.directoryPrefix + 'persona.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    roleBmp = wx.Image(self.directoryPrefix + 'role.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    taskBmp = wx.Image(self.directoryPrefix + 'task.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    ucBmp = wx.Image(self.directoryPrefix + 'usecase.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()


    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_NEW,pnewBmp,'New project')
    self.toolbar.AddSeparator()
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_SETTINGS,settingsBmp,'Edit Project Settings')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_CON,environmentBmp,'Edit Environments')
    self.toolbar.AddSeparator()
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_ADD,addBmp,'Add new requirement')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_DELETE,deleteBmp,'Delete requirement')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_COMMITREQUIREMENTS,saveBmp,'Commit latest requirement changes')
    self.toolbar.AddSeparator()
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_DOMAINPROPERTIES,domainPropertiesBmp,'Edit Domain Properties')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_GOALS,goalsBmp,'Edit Goals')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_OBSTACLES,obstaclesBmp,'Edit Obstacles')
    self.toolbar.AddSeparator()
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_ROLES,roleBmp,'Edit Roles')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_PERSONAS,personasBmp,'Edit Personas')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_TASKS,taskBmp,'Edit Tasks')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_USECASES,ucBmp,'Edit Use Cases')
    self.toolbar.AddSeparator()
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_ASSETS,assetsBmp,'Edit Assets')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_VULNERABILITIES,vulnerabilitiesBmp,'Edit Vulnerabilities')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_ATTACKERS,attackersBmp,'Edit Attackers')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_THREATS,threatsBmp,'Edit Threats')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_RISKS,risksBmp,'Edit Risks')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_RESPONSES,responsesBmp,'Edit Responses')
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_COUNTERMEASURES,countermeasuresBmp,'Edit Countermeasures')
    self.toolbar.AddSeparator()
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_COM,componentBmp,'Edit Architectural Patterns')
    self.toolbar.AddSeparator()
    self.toolbar.AddSimpleTool(armid.RMFRAME_TOOL_FIND,findBmp,'Find object')

    self.toolbar.Realize()

    menubar = wx.MenuBar()
    file = wx.Menu()
    file.Append(armid.RMFRAME_MENU_NEW,'New','New project')

    exportMenu = wx.Menu()
    exportMenu.Append(armid.RMFRAME_MENU_EXPORTMODEL,'Model','Export XML model')
    exportMenu.AppendSeparator()
    exportMenu.Append(armid.RMFRAME_MENU_EXPORTPROJECT,'Project data','Export project data')
    exportMenu.Append(armid.RMFRAME_MENU_REMAN_EXPORT,'Requirements','Export Requirements')
    exportMenu.Append(armid.RMFRAME_MENU_RIMAN_EXPORTRA,'Risk Analysis', 'Export Risk Analysis data')
    exportMenu.Append(armid.RMFRAME_MENU_IRIS_EXPORTUD,'Usability', 'Export usability data ')
    exportMenu.Append(armid.RMFRAME_MENU_IRIS_EXPORTPERSONA,'Persona', 'Export Persona data ')
    exportMenu.Append(armid.RMFRAME_MENU_IRIS_EXPORTASSOCIATIONS,'Associations', 'Export association data ')
    exportMenu.Append(armid.RMFRAME_MENU_OPTIONS_EXPORTTVTYPES,'Threat and Vulnerability Types','Export Threat and Vulnerability Types')
    exportMenu.Append(armid.RMFRAME_MENU_OPTIONS_EXPORTDOMAINVALUES,'Domain Values','Export Domain Values')
    exportMenu.Append(armid.RMFRAME_MENU_OPTIONS_EXPORTPROCESSES,'Processes','Export Processes')
    exportMenu.AppendSeparator()
    exportMenu.Append(armid.RMFRAME_MENU_OPTIONS_EXPORTIMPLIEDSPEC,'Implied Specification','Export Implied Specification')
    file.AppendMenu(armid.RMFRAME_MENU_EXPORT,'Export',exportMenu)
    
    importMenu = wx.Menu()
    importMenu.Append(armid.RMFRAME_MENU_IMPORTMODEL,'Model','Import XML model')
    importMenu.AppendSeparator()
    importMenu.Append(armid.RMFRAME_MENU_IMPORTPROJECT,'Project data','Import project data')
    importMenu.Append(armid.RMFRAME_MENU_REMAN_IMPORT,'Requirements','Import Requirements')
    importMenu.Append(armid.RMFRAME_MENU_RIMAN_IMPORTRA,'Risk Analysis', 'Import')
    importMenu.Append(armid.RMFRAME_MENU_IRIS_IMPORTUD,'Usability', 'Import usability data')
    importMenu.Append(armid.RMFRAME_MENU_IRIS_IMPORTASSOCIATIONS,'Associations', 'Import association data')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTTVTYPES,'Threat and Vulnerability Types','Import Threat and Vulnerability Types')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTDOMAINVALUES,'Domain Values','Import Domain Values')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTDIRECTORIES,'Threat and Vulnerability Directory','Import Threat and Vulnerability Directory')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTSECURITYPATTERNS,'Security Pattern','Import Security Pattern')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTCOMPONENTVIEW,'Architectural Pattern','Import Architectural Pattern')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTATTACKPATTERN,'Attack Pattern','Import Attack Pattern')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTSYNOPSES,'Synopses','Import Synopses and Contributions')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTASSETS,'Assets','Import Template Assets')
    importMenu.Append(armid.RMFRAME_MENU_OPTIONS_IMPORTPROCESSES,'Processes','Import Processes')
    file.AppendMenu(armid.RMFRAME_MENU_IMPORT,'Import',importMenu)


    file.Append(armid.RMFRAME_TOOL_DOCUMENTATION,'Documentation','Generate Documentation')
    file.Append(armid.RMFRAME_MENU_EXIT,'Quit', 'Quit application')
    menubar.Append(file,'&File')

    reman = wx.Menu()
    reman.Append(armid.RMFRAME_MENU_REMAN_SAVE,'Commit','Commit latest requirements changes')
    reman.Append(armid.RMFRAME_MENU_REMAN_ADD,'Add','Add Requirement')
    reman.Append(armid.RMFRAME_MENU_REMAN_DELETE,'Delete','Delete Requirement')
    reman.AppendSeparator()
    reman.Append(armid.RMFRAME_MENU_IRIS_DOMAINPROPERTIES,'Domain Properties', 'Edit Domain Properties')
    reman.Append(armid.RMFRAME_MENU_IRIS_GOALS,'Goals', 'Edit Goals')
    reman.Append(armid.RMFRAME_MENU_IRIS_OBSTACLES,'Obstacles', 'Edit Obstacles')
    menubar.Append(reman,'&Requirement Management')

    riman = wx.Menu()
    riman.Append(armid.RMFRAME_MENU_IRIS_ROLES,'Roles', 'Edit Roles')
    riman.Append(armid.RMFRAME_MENU_RIMAN_ASSETS,'Assets', 'Edit Assets')
    riman.Append(armid.RMFRAME_MENU_RIMAN_ASSETS,'Class Associations', 'Edit Class Associations')
    riman.Append(armid.RMFRAME_MENU_RIMAN_ATTACKERS,'Attackers', 'Edit Attackers')
    riman.Append(armid.RMFRAME_MENU_RIMAN_THREATS,'Threats', 'Edit Threats')
    riman.Append(armid.RMFRAME_MENU_RIMAN_VULNERABILITIES,'Vulnerabilities', 'Edit Vulnerabilities')
    riman.Append(armid.RMFRAME_MENU_RIMAN_RISKS,'Risks', 'Edit Risks')
    riman.Append(armid.RMFRAME_MENU_RIMAN_RESPONSES,'Responses', 'Edit Responses')
    riman.Append(armid.RMFRAME_MENU_RIMAN_COUNTERMEASURES,'Countermeasures', 'Edit Countermeasures')
    riman.AppendSeparator()
    riman.Append(armid.RMFRAME_MENU_OPTIONS_SECURITYPATTERNS,'Security Patterns','Edit Security Patterns')
    menubar.Append(riman,'&Risk Management')

    iris = wx.Menu()
    iris.Append(armid.RMFRAME_MENU_IRIS_FIND,'Find','Search model')
    iris.AppendSeparator()
    iris.Append(armid.RMFRAME_MENU_IRIS_NEWENVIRONMENT,'Environments','Edit Environments')
    iris.Append(armid.RMFRAME_MENU_IRIS_PERSONAS,'Personas', 'Edit Personas')
    iris.Append(armid.RMFRAME_MENU_IRIS_TASKS,'Tasks', 'Edit Tasks')
    iris.AppendSeparator()
    iris.Append(armid.RMFRAME_MENU_OPTIONS_EXTERNALDOCUMENTS,'External Documents','Edit External Documents')
    iris.Append(armid.RMFRAME_MENU_OPTIONS_DOCUMENTREFERENCES,'Document References','Edit Document References')
    iris.Append(armid.RMFRAME_MENU_OPTIONS_CONCEPTREFERENCES,'Concept References','Edit Concept References')
    iris.Append(armid.RMFRAME_MENU_OPTIONS_PERSONACHARACTERISTICS,'Persona Characteristics','Edit Persona Characteristics')
    iris.Append(armid.RMFRAME_MENU_OPTIONS_TASKCHARACTERISTICS,'Task Characteristics','Edit Task Characteristics')
    menubar.Append(iris,'&IRIS')

    eustace = wx.Menu()
    eustace.Append(armid.RMFRAME_MENU_EUSTACE_INTERNALDOCUMENTS,'Internal Documents','Edit Internal Documents')
    eustace.Append(armid.RMFRAME_MENU_EUSTACE_CODES,'Codes','Edit Codes')
    eustace.Append(armid.RMFRAME_MENU_EUSTACE_QUOTATIONS,'Quotations','Edit Quotations')
    eustace.AppendSeparator()
    eustace.Append(armid.RMFRAME_MENU_EUSTACE_CODENETWORK,'Code Network','View code network')
    eustace.AppendSeparator()
    eustace.Append(armid.RMFRAME_MENU_EUSTACE_IMPLIEDPROCESSES,'Implied Processes','View implied processes')
    menubar.Append(eustace,'&EUSTACE')

    optionm = wx.Menu()
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_ASSETS,'Asset values','Edit Asset values')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_ASSETTYPES,'Asset Types','Edit Asset Types')
    optionm.AppendSeparator()
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_ACCESSRIGHTS,'Access rights','Edit Access rights')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_PROTOCOLS,'Protocols','Edit Protocols')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_PRIVILEGES,'Privileges','Edit Privileges')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_SURFACETYPES,'Surface types','Edit Surface types')
    optionm.AppendSeparator()
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_VULNERABILITYTYPES,'Vulnerability Types','Edit Vulnerability Types')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_SEVERITIES,'Vulnerability Severities','Edit Vulnerability Severities')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_CAPABILITIES,'Capabilities','Edit Attacker Capabilities')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_MOTIVATIONS,'Motivations','Edit Attacker Motivations')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_THREATTYPES,'Threat Types','Edit Threat Types')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_LIKELIHOODS,'Threat Likelihoods','Edit Threat Likelihoods')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_THREATS,'Threat values','Edit Threat values')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_RISKS,'Risk values','Edit Risk values')
    optionm.AppendSeparator()
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_TEMPLATEASSETS,'Template Assets','Edit Template Assets')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_TEMPLATEREQUIREMENTS,'Template Requirements','Edit Template Requirements')
    optionm.Append(armid.RMFRAME_MENU_OPTIONS_COUNTERMEASURES,'Countermeasure values','Edit Countermeasure values')
    menubar.Append(optionm,'&Options')

    viewm = wx.Menu()
    viewm.Append(armid.RMFRAME_MENU_VIEW_ENVIRONMENT,'Risk Analysis','View risk analysis model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_ASSETMODEL,'Asset Model','View asset model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_GOALMODEL,'Goal Model','View goal model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_OBSTACLEMODEL,'Obstacle Model','View obstacle model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_RESPONSIBILITYMODEL,'Responsibility Model','View responsibility model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_TASKMODEL,'Task Model','View task model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_APMODEL,'Assumption Persona Model','View assumption persona model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_ATMODEL,'Assumption Task Model','View assumption task model')
    viewm.Append(armid.RMFRAME_MENU_VIEW_TRACEABILITY,'Traceability','View Traceability relations')
    menubar.Append(viewm,'&View')
  
    gridm = wx.Menu()
    gridm.Append(armid.RMFRAME_MENU_GRID_REQUIREMENTS,'Requirements','Requirements editor')
    gridm.Append(armid.RMFRAME_MENU_GRID_GOALS,'Goals','Goals editor')
    gridm.Append(armid.RMFRAME_MENU_GRID_OBSTACLES,'Obstacles','Obstacles editor')
    self.toolbar.AddSeparator()
    gridm.Append(armid.RMFRAME_MENU_RELABEL_OBJECTS,'Relabel objects','')

    menubar.Append(gridm,'&Grid')
    
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_ENVIRONMENT,self.OnViewEnvironment)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_ASSETMODEL,self.OnViewAssets)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_GOALMODEL,self.OnViewGoals)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_OBSTACLEMODEL,self.OnViewObstacles)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_RESPONSIBILITYMODEL,self.OnViewResponsibilities)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_TASKMODEL,self.OnViewTasks)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_APMODEL,self.OnViewAPModel)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_ATMODEL,self.OnViewATModel)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_EUSTACE_CODENETWORK,self.OnViewCodeNetwork)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_EUSTACE_IMPLIEDPROCESSES,self.OnImpliedProcesses)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_TRACEABILITY,self.OnViewTraceability)

    wx.EVT_MENU(self,armid.RMFRAME_MENU_GRID_REQUIREMENTS,self.OnGridRequirements)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_GRID_GOALS,self.OnGridGoals)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_GRID_OBSTACLES,self.OnGridObstacles)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RELABEL_OBJECTS,self.OnRelabelObjects)

    helpm = wx.Menu()
    helpm.Append(armid.RMFRAME_MENU_HELP_ABOUT,'About','About CAIRIS')
    wx.EVT_MENU(self,armid.RMFRAME_MENU_HELP_ABOUT,self.OnAbout)
    menubar.Append(helpm,'&Help')


    self.SetMenuBar(menubar)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_NEW,self.OnNewProject)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_COMMITREQUIREMENTS,self.OnCommitEditorObjects)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_ADD,self.OnAddEditorObject)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_DELETE,self.OnDeleteEditorObject)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_CON,self.OnEnvironments)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_COM,self.OnComponents)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_SETTINGS,self.OnSettings)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_ENVIRONMENTMODEL,self.OnViewEnvironment)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_ASSETMODEL,self.OnViewAssets)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_GOALMODEL,self.OnViewGoals)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_OBSTACLEMODEL,self.OnViewObstacles)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_RESPONSIBILITYMODEL,self.OnViewResponsibilities)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_TASKMODEL,self.OnViewTasks)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_APMODEL,self.OnViewAPModel)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_ATMODEL,self.OnViewATModel)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_CMMODEL,self.OnViewCMModel)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_COMPONENTMODEL,self.OnViewComponentModel)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_FIND,self.OnSearchModel)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_DOMAINPROPERTIES,self.OnDomainProperties)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_GOALS,self.OnGoals)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_OBSTACLES,self.OnObstacles)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_ASSETS,self.OnAssets)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_CLASSASSOCIATIONS,self.OnClassAssociations)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_GOALASSOCIATIONS,self.OnGoalAssociations)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_DEPENDENCIES,self.OnDependencies)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_ATTACKERS,self.OnAttackers)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_THREATS,self.OnThreats)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_VULNERABILITIES,self.OnVulnerabilities)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_RISKS,self.OnRisks)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_RESPONSES,self.OnResponses)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_COUNTERMEASURES,self.OnCountermeasures)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_PERSONAS,self.OnPersonas)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_ROLES,self.OnRoles)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_TASKS,self.OnTasks)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_USECASES,self.OnUseCases)
    wx.EVT_MENU(self,armid.RMFRAME_TOOL_DOCUMENTATION,self.OnDocumentation)

    wx.EVT_MENU(self,armid.RMFRAME_MENU_EXPORTMODEL,self.OnExportModel)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IMPORTMODEL,self.OnImportModel)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_EXPORTPROJECT,self.OnExportProject)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IMPORTPROJECT,self.OnImportProject)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_EXIT,self.OnQuit)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_REMAN_SAVE,self.OnCommitEditorObjects)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_REMAN_ADD,self.OnAddEditorObject)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_REMAN_DELETE,self.OnDeleteEditorObject)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_FIND,self.OnSearchModel)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_REMAN_IMPORT,self.OnImportRequirements)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_REMAN_EXPORT,self.OnExportRequirements)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_ATTACKERS,self.OnAttackers)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_DOMAINPROPERTIES,self.OnDomainProperties)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_GOALS,self.OnGoals)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_OBSTACLES,self.OnObstacles)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_EXPORTUD,self.OnExportUsability)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_EXPORTPERSONA,self.OnExportPersona)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_IMPORTUD,self.OnImportUsability)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_EXPORTASSOCIATIONS,self.OnExportAssociations)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_IMPORTASSOCIATIONS,self.OnImportAssociations)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_ASSETS,self.OnAssets)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_CLASSASSOCIATIONS,self.OnClassAssociations)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_GOALASSOCIATIONS,self.OnGoalAssociations)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_THREATS,self.OnThreats)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_VULNERABILITIES,self.OnVulnerabilities)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_RISKS,self.OnRisks)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_RESPONSES,self.OnResponses)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_EXPORTRA,self.OnExportRiskAnalysis)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_RIMAN_IMPORTRA,self.OnImportRiskAnalysis)

    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_NEWENVIRONMENT,self.OnEnvironments)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_PERSONAS,self.OnPersonas)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_ROLES,self.OnRoles)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_TASKS,self.OnTasks)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_IRIS_USECASES,self.OnUseCases)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_ASSETS,self.OnAssetOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_THREATS,self.OnThreatOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_RISKS,self.OnRiskOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_COUNTERMEASURES,self.OnCountermeasureOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_CAPABILITIES,self.OnCapabilityOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_MOTIVATIONS,self.OnMotivationOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_ASSETTYPES,self.OnAssetTypeOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_ACCESSRIGHTS,self.OnAccessRightOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_PROTOCOLS,self.OnProtocolOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_PRIVILEGES,self.OnPrivilegeOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_SURFACETYPES,self.OnSurfaceTypeOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_VULNERABILITYTYPES,self.OnVulnerabilityTypeOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_THREATTYPES,self.OnThreatTypeOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTTVTYPES,self.OnImportTVTypes)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_EXPORTTVTYPES,self.OnExportTVTypes)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTDOMAINVALUES,self.OnImportDomainValues)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_EXPORTDOMAINVALUES,self.OnExportDomainValues)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTPROCESSES,self.OnImportProcesses)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_EXPORTPROCESSES,self.OnExportProcesses)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_EXPORTIMPLIEDSPEC,self.OnExportImpliedSpec)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_SEVERITIES,self.OnSeverityOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_LIKELIHOODS,self.OnLikelihoodOptions)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_TEMPLATEASSETS,self.OnTemplateAssets)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_TEMPLATEREQUIREMENTS,self.OnTemplateRequirements)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_SECURITYPATTERNS,self.OnSecurityPatterns)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_EXTERNALDOCUMENTS,self.OnExternalDocuments)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_EUSTACE_INTERNALDOCUMENTS,self.OnInternalDocuments)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_EUSTACE_CODES,self.OnCodes)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_EUSTACE_QUOTATIONS,self.OnQuotations)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_DOCUMENTREFERENCES,self.OnDocumentReferences)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_CONCEPTREFERENCES,self.OnConceptReferences)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_PERSONACHARACTERISTICS,self.OnPersonaCharacteristics)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_TASKCHARACTERISTICS,self.OnTaskCharacteristics)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTDIRECTORIES,self.OnImportDirectories)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTSECURITYPATTERNS,self.OnImportSecurityPatterns)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTCOMPONENTVIEW,self.OnImportComponentView)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTATTACKPATTERN,self.OnImportAttackPattern)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTSYNOPSES,self.OnImportSynopses)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_OPTIONS_IMPORTASSETS,self.OnImportAssets)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_ENVIRONMENT,self.OnViewEnvironment)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_ASSETMODEL,self.OnViewAssets)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_GOALMODEL,self.OnViewGoals)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_OBSTACLEMODEL,self.OnViewObstacles)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_RESPONSIBILITYMODEL,self.OnViewResponsibilities)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_TASKMODEL,self.OnViewTasks)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_APMODEL,self.OnViewAPModel)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_ATMODEL,self.OnViewATModel)
    wx.EVT_MENU(self,armid.RMFRAME_MENU_VIEW_TRACEABILITY,self.OnViewTraceability)

    self.panel = RMPanel(self,armid.RMPANEL_ID)
    self.mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.situatePanel()

    self.SetTitle('CAIRIS')

    b = Borg()
    b.mainFrame = self
    self.Centre()
    self.Show(True)

  def OnQuit(self,event):
    self.Close()

  def OnCommitEditorObjects(self,event):
    grid = self.FindWindowById(armid.ID_REQGRID)
    try:
      grid.commitChanges()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Save environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnAddEditorObject(self,event):
    try:
      self.panel.addObject()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add Editor Object',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnDeleteEditorObject(self,event):
    try:
      grid = self.FindWindowById(armid.ID_REQGRID)
      pos = grid.GetGridCursorRow()
      if (pos >= 0):
        om = grid.GetTable().om
        objts = om.objects()
        eo = objts[pos]
        eoDim = self.panel.objectDimension
        eoDeps = self.dbProxy.reportDependencies(eoDim,eo.id())
        if (len(eoDeps) > 0):
          dlg = DependentsDialog(self,eoDeps,eoDim)
          retValue = dlg.ShowModal()
          dlg.Destroy()
          if (retValue != armid.DEPENDENTS_BUTTONCONFIRM_ID):
            return
          else:
            self.dbProxy.deleteDependencies(eoDeps)
        grid.DeleteRows(pos)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete Editor Object',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnEnvironments(self,event):
    try:
      dialog = EnvironmentsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Environments',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnComponents(self,event):
    try:
      dialog = ArchitecturalPatternsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Architectural Patterns',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnAttackers(self,event):
    try:
      dialog = AttackersDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Attackers',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnGoals(self,event):
    try:
      dialog = GoalsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Goals',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnObstacles(self,event):
    try:
      dialog = ObstaclesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Obstacles',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnDomainProperties(self,event):
    try:
      dialog = DomainPropertiesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Domain Properties',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnAssets(self,event):
    try:
      dialog = AssetsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Assets',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnClassAssociations(self,event):
    try:
      dialog = ClassAssociationsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Class Associations',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnGoalAssociations(self,event):
    try:
      dialog = GoalAssociationsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Goal Associations',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnDependencies(self,event):
    try:
      dialog = DependenciesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Dependencies',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnThreats(self,event):
    try:
      dialog = ThreatsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Threats',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnVulnerabilities(self,event):
    try:
      dialog = VulnerabilitiesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Vulnerabilities',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnPersonas(self,event):
    try:
      dialog = PersonasDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Personas',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnTasks(self,event):
    try:
      dialog = TasksDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Tasks',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnUseCases(self,event):
    try:
      dialog = UseCasesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Use Cases',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnRisks(self,event):
    try:
      dialog = RisksDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Risks',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnResponses(self,event):
    try:
      dialog = ResponsesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Responses',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnCountermeasures(self,event):
    try:
      dialog = CountermeasuresDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Countermeasures',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def requirementGrid(self):
    grid = self.FindWindowById(armid.ID_REQGRID)
    return grid

  def OnViewEnvironment(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      environments = proxy.getDimensionNames('environment',False)
      cDlg = DimensionNameDialog(self,'environment',environments,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        environmentName = cDlg.dimensionName()
        tLinks = EnvironmentModel(proxy.riskAnalysisModel(environmentName),environmentName,proxy)
        cDlg.Destroy() 
        if (tLinks.size() > 0):
          dialog = EnvironmentModelViewer(environmentName,proxy)
          dialog.ShowModal(tLinks)
        else:
          dlg = wx.MessageDialog(self,'No environment relationships defined','View Environment',wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          dlg.Destroy()
      else:
        cDlg.Destroy() 
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnViewAssets(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      environments = proxy.getDimensionNames('environment',False)
      cDlg = DimensionNameDialog(self,'environment',environments,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        environmentName = cDlg.dimensionName()
        associationDictionary = proxy.classModel(environmentName)
        associations = AssetModel(associationDictionary.values(),environmentName)
        cDlg.Destroy() 
        if (associations.size() > 0):
          dialog = CanonicalModelViewer(environmentName,'class',proxy)
          dialog.ShowModal(associations)
        else:
          dlg = wx.MessageDialog(self,'No asset associations defined','View Assets',wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          dlg.Destroy()
      else:
        cDlg.Destroy() 
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Assets',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return


  def viewKaosModel(self,modelType):
    dialog = None
    try:
      proxy = self.b.dbProxy
      environments = proxy.getDimensionNames('environment',False)
      cDlg = DimensionNameDialog(self,'environment',environments,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        environmentName = cDlg.dimensionName()
        cDlg.Destroy() 

        associationDictionary = {}
        if (modelType == 'goal'):
          associationDictionary = proxy.goalModel(environmentName)
        elif (modelType == 'obstacle'):
          associationDictionary = proxy.obstacleModel(environmentName)
        elif (modelType == 'responsibility'):
          associationDictionary = proxy.responsibilityModel(environmentName)
        else: 
          associationDictionary = proxy.taskModel(environmentName)
        associationRelations = associationDictionary.values()
        if (len(associationRelations) > 0):
          associations = KaosModel(associationRelations,environmentName,modelType)
          dialog = CanonicalModelViewer(environmentName,modelType,proxy)
          dialog.ShowModal(associations)
        else:
          errorTxt = 'No ' + modelType + ' associations defined'
          dlg = wx.MessageDialog(self,errorTxt,'View Model',wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          dlg.Destroy()
      else:
        cDlg.Destroy() 
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnViewAPModel(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      personas = proxy.getDimensionNames('persona')
      cDlg = DimensionNameDialog(self,'persona',personas,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        personaName = cDlg.dimensionName()
        cDlg.Destroy() 

        modelAssocs = proxy.assumptionPersonaModel(personaName)
        if (len(modelAssocs) > 0):
          associations = AssumptionPersonaModel(modelAssocs)
          dialog = APModelViewer(personaName)
          dialog.ShowModal(associations)
        else:
          errorTxt = 'No assumption persona associations defined'
          dlg = wx.MessageDialog(self,errorTxt,'View Assumption Persona Model',wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          dlg.Destroy()
      else:
        cDlg.Destroy() 
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Assumption Persona Model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return


  def OnViewGoals(self,event):
    self.viewKaosModel('goal')
    assetName = self.panel.selectedObject()
    self.updateObjectSelection(assetName)

  def OnViewResponsibilities(self,event):
    self.viewKaosModel('responsibility')

  def OnViewObstacles(self,event):
    self.viewKaosModel('obstacle')

  def OnViewTasks(self,event):
    self.viewKaosModel('task')

  def OnViewTraceability(self,event):
    try:
      dialog = TraceabilityEditor(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Trace Relations',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnRoles(self,evt):
    try:
      dialog = RolesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Roles',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnNewProject(self,evt):
    try:
      b = Borg()
      b.dbProxy.clearDatabase()
      self.panel.updateObjectSelection()
      self.panel.updateEnvironmentSelection()
      self.panel.refresh()
    except KeyError:
      dlg = wx.MessageDialog(self,'IRIS environment variables not defined','New project',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'New Project Roles',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnDocumentation(self,evt):
    try:
      defaultDocDir = os.environ['HOME']
      gdDlg = GenerateDocumentationDialog(self)
      if (gdDlg.ShowModal() == armid.GENDOCPANEL_BUTTONGENERATE_ID):
        docType = gdDlg.documentType()
        sectionFlags = gdDlg.sectionFlags()
        typeFlags = gdDlg.typeFlags()
        gdDlg.Destroy()
        odlg = wx.FileDialog(self,message='Generate documentation',defaultDir=defaultDocDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if (odlg.ShowModal() == wx.ID_OK):
          fileName = odlg.GetFilename()
          docDir = odlg.GetDirectory()
          docFile = odlg.GetPath()
          odlg.Destroy()
          if (os.access(docFile,os.F_OK)):
            if (os.access(docFile,os.W_OK | os.R_OK) == False):
              dlg = wx.MessageDialog(self,'Cannot read or write to' + docFile,'Generate documentation',wx.OK | wx.ICON_ERROR)
              dlg.ShowModal()
              dlg.Destroy()
              return
          DocumentBuilder.build(docType,sectionFlags,typeFlags,fileName,docDir)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate documentation',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnSettings(self,evt):
    try:
# Necessary to re-create the project, as calling this just after opening a project file seems to return nothing for some reason
      self.dbProxy = self.b.dbProxy
      pSettings = self.dbProxy.getProjectSettings()
      pDict = self.dbProxy.getDictionary()

      contributors = self.dbProxy.getContributors()
      revisions = self.dbProxy.getRevisions()
      dlg = ProjectSettingsDialog(self,pSettings,pDict,contributors,revisions)
      if (dlg.ShowModal() == armid.PROJECTSETTINGS_BUTTONCOMMIT_ID):
        self.dbProxy.updateSettings(dlg.name(),dlg.background(),dlg.goals(),dlg.scope(),dlg.definitions(),dlg.contributors(),dlg.revisions(),dlg.richPicture(),self.b.fontSize,self.b.fontName)
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Project Settings',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def updateObjectSelection(self,selectedObject = ''):
    self.panel.updateObjectSelection(selectedObject)

  def updateEnvironmentSelection(self,selectedEnvironment = ''):
    self.panel.updateEnvironmentSelection(selectedEnvironment)


  def OnAssetOptions(self,event):
    try:
      defaultEnv = self.dbProxy.defaultEnvironment()
      if defaultEnv == '':
        dlg = wx.MessageDialog(self,'No environments specified','Edit Asset Values',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return
      else:
        dialog = ValueTypesDialog(self,'asset_value',defaultEnv)
        dialog.ShowModal()
        dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Asset Values',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnThreatOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'threat_value')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Threat Values',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnRiskOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'risk_class')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Risk Values',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnCountermeasureOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'countermeasure_value')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Countermeasure Values',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnCapabilityOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'capability')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Capabilities',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnMotivationOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'motivation')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Motivations',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnAssetTypeOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'asset_type')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Asset Types',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnAccessRightOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'access_right')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Access Right',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnProtocolOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'protocol')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Protocol',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnPrivilegeOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'privilege')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Privilege',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnSurfaceTypeOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'surface_type')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Surface Type',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnVulnerabilityTypeOptions(self,event): 
    try:
      dialog = ValueTypesDialog(self,'vulnerability_type')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Vulnerability Types',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnThreatTypeOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'threat_type')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Threat Types',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnSeverityOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'severity')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Vulnerability Severities',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnLikelihoodOptions(self,event):
    try:
      dialog = ValueTypesDialog(self,'likelihood')
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Threat Likelihoods',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnTemplateAssets(self,event):
    try:
      dialog = TemplateAssetsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Template Assets',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnTemplateRequirements(self,event):
    try:
      dialog = TemplateRequirementsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Template Requirements',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return


  def OnSecurityPatterns(self,event):
    try:
      dialog = SecurityPatternsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Security Patterns',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnExternalDocuments(self,event):
    try:
      dialog = ExternalDocumentsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit External Documents',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnInternalDocuments(self,event):
    try:
      dialog = InternalDocumentsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Internal Documents',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnCodes(self,event):
    try:
      dialog = CodesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Codes',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnDocumentReferences(self,event):
    try:
      dialog = DocumentReferencesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Document References',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnPersonaCharacteristics(self,event):
    try:
      dialog = PersonaCharacteristicsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Persona Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnTaskCharacteristics(self,event):
    try:
      dialog = TaskCharacteristicsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Task Characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnConceptReferences(self,event):
    try:
      dialog = ConceptReferencesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Concept References',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return


  def OnImportSecurityPatterns(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Pattern Catalogue (*.xml) | *.xml |"

      spdlg = wx.FileDialog(None,'Import Security Patterns',defaultDir,style=wx.OPEN)
      if (spdlg.ShowModal() == wx.ID_OK):
        msgStr = importSecurityPatterns(spdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import Security Patterns',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      spdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import Security Patterns',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnImportComponentView(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Component View (*.xml) | *.xml |"

      cvdlg = wx.FileDialog(None,'Import Component View',defaultDir,style=wx.OPEN)
      if (cvdlg.ShowModal() == wx.ID_OK):
        msgStr = importComponentViewFile(cvdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import Component View',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      cvdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import Component View',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnImportAttackPattern(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Attack Pattern (*.xml) | *.xml |"

      cvdlg = wx.FileDialog(None,'Import Attack Pattern',defaultDir,style=wx.OPEN)
      if (cvdlg.ShowModal() == wx.ID_OK):
        msgStr = importAttackPattern(cvdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import Attack Pattern',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      cvdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import Attack Pattern',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnImportSynopses(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Synopses (*.xml) | *.xml |"

      cvdlg = wx.FileDialog(None,'Import Synopses',defaultDir,style=wx.OPEN)
      if (cvdlg.ShowModal() == wx.ID_OK):
        msgStr = importSynopsesFile(cvdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import Synopses',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      cvdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import Synopses',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnImportAssets(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Template Assets (*.xml) | *.xml |"

      cvdlg = wx.FileDialog(None,'Import Assets',defaultDir,style=wx.OPEN)
      if (cvdlg.ShowModal() == wx.ID_OK):
        msgStr = importAssetsFile(cvdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import Assets',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      cvdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import Assets',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnImportTVTypes(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Types files (*.xml) | *.xml |"

      tdlg = wx.FileDialog(None,'Import Types',defaultDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importTVTypeFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import Security Patterns',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import Types',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnExportTVTypes(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export threat and vulnerability types',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,ttCount,vtCount = self.dbProxy.tvTypesToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(ttCount) + ' threat types, and ' + str(vtCount) + ' vulnerability types','Export threat and vulnerability types',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export threat and vulnerability types',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def OnImportDirectories(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Types files (*.xml) | *.xml |"

      tdlg = wx.FileDialog(None,'Import Directories',defaultDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importDirectoryFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import Directories',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import Directories',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnAbout(self,event):
    import re
    svnid = '$Id: RMFrame.py 580 2012-03-19 17:45:52Z shaf $' 
    svnidrep = r'^\$Id: (?P<filename>.+) (?P<revision>\d+) (?P<date>\d{4}-\d{2}-\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2})Z (?P<user>\w+) \$$'
    mo = re.match(svnidrep,svnid)
    repVersion = 'Revision ' + mo.group('revision')

    info = wx.AboutDialogInfo()
    info.SetIcon(wx.Icon(self.directoryPrefix + 'iris.png',wx.BITMAP_TYPE_PNG))
    info.SetName('CAIRIS')
    info.SetVersion(repVersion)
    info.SetDescription('CAIRIS is a tool for specifying usable and secure systems')
    info.SetWebSite('http://www.cs.ox.ac.uk/cairis')
    info.SetLicense('CAIRIS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;\nwithout even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\nPlease contact Shamal Faily at the University of Oxford for specific licensing queries.')
    info.AddDeveloper('Shamal Faily')
    wx.AboutBox(info)

  def OnImportRequirements(self,event):
    try:
      defaultBackupDir = './sql'
      tdlg = wx.FileDialog(self,message='Import goals and requirements',defaultDir=defaultBackupDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importRequirementsFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import goals and requirements',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import goals and requirements',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnExportRequirements(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export goals and requirements',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,dpCount,goalCount,obsCount,reqCount,cmCount = self.dbProxy.goalsToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(dpCount) + ' domain properties, ' + str(goalCount) + ' goals, ' + str(obsCount) + ' obstacles, ' + str(reqCount) + ' requirements, and ' + str(cmCount) + ' countermeasures','Export goals and requirements',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export goals and requirements',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def OnExportRiskAnalysis(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export risk data',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT|wx.SAVE)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,roleCount,assetCount,vulCount,attackerCount,threatCount,riskCount,responseCount,relCount = self.dbProxy.riskAnalysisToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(roleCount) + ' roles, ' + str(assetCount) + ' assets, ' + str(vulCount) + ' vulnerabilities, ' + str(attackerCount) + ' attackers, ' + str(threatCount) + ' threats, ' + str(riskCount) + ' risks, ' + str(responseCount) + ' responses, and ' + str(relCount) + ' asset associations','Export risk data',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export risk data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy


  def OnImportRiskAnalysis(self,event):
    try:
      defaultBackupDir = './sql'
      tdlg = wx.FileDialog(self,message='Import risk data',defaultDir=defaultBackupDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importRiskAnalysisFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import risk data',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import risk data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()


  def OnExportUsability(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export usability data',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,personaCount,edCount,drCount,pcCount,taskCount,ucCount = self.dbProxy.usabilityToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(personaCount) + ' personas, ' + str(edCount) + ' external documents, ' + str(drCount) + ' document and concept references, ' + str(pcCount) + ' persona references, ' + str(taskCount) + ' tasks, and ' + str(ucCount) + ' use cases','Export usability data',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export usability data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy



  def OnImportUsability(self,event):
    try:
      defaultBackupDir = './sql'
      tdlg = wx.FileDialog(self,message='Import usability data',defaultDir=defaultBackupDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importUsabilityFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import usability data',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import usability data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()


  def OnExportUsability(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export usability data',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,pCount,edCount,drCount,pcCount,taskCount,ucCount = self.dbProxy.usabilityToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(pCount) + ' personas, ' + str(drCount) + ' document references, ' + str(pcCount) + ' persona characteristics, ' + str(taskCount) + ' tasks, and ' + str(ucCount) + ' use cases','Export usability data',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export usability data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy


  def OnExportAssociations(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export association data',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,maCount,gaCount,rrCount,depCount = self.dbProxy.associationsToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(maCount) + ' manual associations, ' + str(gaCount) + ' goal associations, ' + str(rrCount) + ' non-goal responsibility relationships, and ' + str(depCount) + ' dependency associations','Export association data',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export association data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
  
  def OnImportAssociations(self,event):
    try:
      defaultBackupDir = './sql'
      tdlg = wx.FileDialog(self,message='Import association data',defaultDir=defaultBackupDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importAssociationsFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import association data',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import association data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnExportProject(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export project data',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf= self.dbProxy.projectToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported project data','Export project data',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export project data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def OnImportModel(self,event):
    try:
      defaultBackupDir = './sql'
      tdlg = wx.FileDialog(self,message='Import model',defaultDir=defaultBackupDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importModelFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import model',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnImportProject(self,event):
    try:
      defaultBackupDir = './sql'
      tdlg = wx.FileDialog(self,message='Import project data',defaultDir=defaultBackupDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        msgStr = importProjectFile(tdlg.GetPath()) 
        dlg = wx.MessageDialog(self,msgStr,'Import project data',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import project data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnExportModel(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export model',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf = '<?xml version="1.0"?>\n<!DOCTYPE cairis_model PUBLIC "-//CAIRIS//DTD MODEL 1.0//EN" "http://www.cs.ox.ac.uk/cairis/dtd/cairis_model.dtd">\n<cairis_model>\n\n\n'
        xmlBuf+= self.dbProxy.tvTypesToXml(0)[0] + '\n\n'
        xmlBuf+= self.dbProxy.domainValuesToXml(0)[0] + '\n\n'
        xmlBuf+= self.dbProxy.projectToXml(0) + '\n\n'
        xmlBuf+= self.dbProxy.riskAnalysisToXml(0)[0] + '\n\n'
        xmlBuf+= self.dbProxy.usabilityToXml(0)[0] + '\n\n'
        xmlBuf+= self.dbProxy.goalsToXml(0)[0] + '\n\n'
        xmlBuf+= self.dbProxy.associationsToXml(0)[0] + '\n\n</cairis_model>'
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported model','Export model',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def OnViewATModel(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      tasks = proxy.getDimensionNames('misusability_case')
      cDlg = DimensionNameDialog(self,'misusability_case',tasks,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        taskName = cDlg.dimensionName()
        cDlg.Destroy() 

        modelAssocs = proxy.assumptionTaskModel(taskName)
        if (len(modelAssocs) > 0):
          associations = AssumptionTaskModel(modelAssocs)
          dialog = ATModelViewer(taskName)
          dialog.ShowModal(associations)
        else:
          errorTxt = 'No assumption task associations defined'
          dlg = wx.MessageDialog(self,errorTxt,'View Assumption Task Model',wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          dlg.Destroy()
      else:
        cDlg.Destroy() 
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Assumption Task Model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnSearchModel(self,evt):
    try:
      dialog = SearchDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Search Model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnExportPersona(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      personas = proxy.getDimensionNames('persona')
      cDlg = DimensionNameDialog(self,'persona',personas,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        personaName = cDlg.dimensionName()
        defaultBackupDir = './sql'
        dlg = wx.FileDialog(self,message='Export persona',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if (dlg.ShowModal() == wx.ID_OK):
          exportFile = dlg.GetPath() + ".xml"
          xmlBuf,edCount,drCount,pcCount = self.dbProxy.personaToXml(personaName)
          f = open(exportFile,'w')
          f.write(xmlBuf)
          f.close()
          confDlg = wx.MessageDialog(self,'Exported ' + str(edCount) + ' external documents, ' + str(drCount) + ' document references, and ' + str(pcCount) + ' persona characteristics','Export personas',wx.OK | wx.ICON_INFORMATION)
          confDlg.ShowModal()
          confDlg.Destroy()
        dlg.Destroy()
      cDlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export persona',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def OnGridRequirements(self,event):
    self.mainSizer.Clear(True)
    self.panel = RMPanel(self,armid.RMPANEL_ID)
    self.situatePanel()

  def OnGridGoals(self,event):
    self.mainSizer.Clear(True)
    self.panel = GMPanel(self,armid.RMPANEL_ID)
    self.situatePanel()

  def OnGridObstacles(self,event):
    self.mainSizer.Clear(True)
    self.panel = OMPanel(self,armid.RMPANEL_ID)
    self.situatePanel()

  def situatePanel(self):
    self.mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizeHints(1500,700)
    self.SetSizerAndFit(self.mainSizer)

  def OnRelabelObjects(self,evt):
    try:
      self.panel.relabel()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Relabel objects',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def OnImportDomainValues(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Types files (*.xml) | *.xml |"

      tdlg = wx.FileDialog(None,'Domain Values',defaultDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        tFileName = tdlg.GetPath() 
        msgStr = importDomainValuesFile(tdlg.GetPath())
        dlg = wx.MessageDialog(self,msgStr,'Import domain values data',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import domain values data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnExportDomainValues(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export domain values',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,tvCount,rvCount,cvCount,svCount,lvCount = self.dbProxy.domainValuesToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(tvCount) + ' threat values, ' + str(rvCount) + ' risk values, ' + str(cvCount) + ' countermeasure values, ' + str(svCount) + ' severity values, and ' + str(lvCount) + ' likelihood values','Export domain values',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export domain values',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()

  def OnImportProcesses(self,event):
    try:
      defaultDir = './sql'
      wildcard = "Types files (*.xml) | *.xml |"

      tdlg = wx.FileDialog(None,'Processes',defaultDir,style=wx.OPEN)
      if (tdlg.ShowModal() == wx.ID_OK):
        tFileName = tdlg.GetPath() 
        msgStr = importProcessesFile(tdlg.GetPath())
        dlg = wx.MessageDialog(self,msgStr,'Import processes data',wx.OK | wx.ICON_INFORMATION )
        dlg.ShowModal()
        dlg.Destroy()
      tdlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Import processes data',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()

  def OnExportProcesses(self,event):
    try:
      defaultBackupDir = './sql'
      dlg = wx.FileDialog(self,message='Export processes',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
      if (dlg.ShowModal() == wx.ID_OK):
        exportFile = dlg.GetPath() + ".xml"
        xmlBuf,idCount,codeCount,memoCount,qCount,pcnCount,icCount,ipnCount = self.dbProxy.processesToXml()
        f = open(exportFile,'w')
        f.write(xmlBuf)
        f.close()
        confDlg = wx.MessageDialog(self,'Exported ' + str(idCount) + ' internal documents, ' + str(codeCount) + ' codes, ' + str(memoCount) + ' memos, ' + str(qCount) + ' quotations, ' + str(pcnCount) + ' code relationships, ' + str(icCount) + ' implied characteristics, and ' + str(ipnCount) + ' implied processes.','Export processes',wx.OK | wx.ICON_INFORMATION)
        confDlg.ShowModal()
        confDlg.Destroy()
      dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export processes',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()

  def OnViewCMModel(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      environments = proxy.getDimensionNames('environment',False)
      cDlg = DimensionNameDialog(self,'environment',environments,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        environmentName = cDlg.dimensionName()
        associationDictionary = proxy.conceptMapModel(environmentName)
        associations = ConceptMapModel(associationDictionary.values(),environmentName)
        cDlg.Destroy() 
        if (associations.size() > 0):
          dialog = CanonicalModelViewer(environmentName,'conceptmap',proxy)
          dialog.ShowModal(associations)
        else:
          dlg = wx.MessageDialog(self,'No concept map associations defined','View Concept Map',wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          dlg.Destroy()
      else:
        cDlg.Destroy() 
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Concept Map',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnViewComponentModel(self,event):
    dialog = None
    try: 
      proxy = self.b.dbProxy
      cvs = ['ALL']
      cvs += proxy.getDimensionNames('component_view',False)
      cDlg = DimensionNameDialog(self,'component_view',cvs,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        cvName = cDlg.dimensionName()
        interfaces,connectors = self.dbProxy.componentView(cvName)
        if (len(interfaces) == 0):
          dlg = wx.MessageDialog(self,'No components defined','View Component Model',wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          dlg.Destroy()
        else: 
          cModel = ComponentModel(interfaces,connectors)
          dialog = ComponentModelViewer(cvName)
          dialog.ShowModal(cModel)
          dialog.destroy()
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Component Diagram',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnViewCodeNetwork(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      personas = proxy.getDimensionNames('persona')
      cDlg = DimensionNameDialog(self,'persona',personas,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        personaName = cDlg.dimensionName()
        codeNet = CodeNetworkModel(proxy.personaCodeNetwork(personaName),personaName)
        codeNet.graph()
        cDlg.Destroy() 
        dialog = CodeNetworkViewer(self,personaName,codeNet)
        dialog.ShowModal()
        dialog.Destroy()
      else:
        cDlg.Destroy() 
    except ARMException,errorText:
      if (dialog != None):
        dialog.destroy()
      dlg = wx.MessageDialog(self,str(errorText),'View Code Network',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnImpliedProcesses(self,event):
    try:
      dialog = ImpliedProcessesDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Implied Processes',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def OnExportImpliedSpec(self,event):
    dialog = None
    try:
      proxy = self.b.dbProxy
      environments = proxy.getDimensionNames('persona_implied_process',False)
      cDlg = DimensionNameDialog(self,'persona_implied_process',environments,'Select')
      ipName = None
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        ipName = cDlg.dimensionName()
      cDlg.Destroy() 
      if ipName != None:
        defaultBackupDir = './csp'
        dlg = wx.FileDialog(self,message='Export implied process',defaultDir=defaultBackupDir,style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if (dlg.ShowModal() == wx.ID_OK):
          exportFile = dlg.GetPath() + ".csp"
          cspBuf = self.dbProxy.impliedProcess(ipName)
          f = open(exportFile,'w')
          f.write(cspBuf)
          f.close()
          confDlg = wx.MessageDialog(self,'Exported ' + ipName + ' implied process','Export implied process',wx.OK | wx.ICON_INFORMATION)
          confDlg.ShowModal()
          confDlg.Destroy()
        dlg.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Export implied process',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()

  def OnQuotations(self,event):
    try:
      dialog = QuotationsDialog(self)
      dialog.ShowModal()
      dialog.Destroy()
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Quotations',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
