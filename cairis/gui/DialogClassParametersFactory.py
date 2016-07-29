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
from cairis.core.armid import *
from ResponseDialogParameters import ResponseDialogParameters
from DialogClassParameters import DialogClassParameters
from cairis.core.Borg import Borg
from DocumentReferenceDialog import DocumentReferenceDialog
from AssetDialog import AssetDialog
from AttackerDialog import AttackerDialog
from GoalDialog import GoalDialog
from ObstacleDialog import ObstacleDialog
from VulnerabilityDialog import VulnerabilityDialog
from ThreatDialog import ThreatDialog
from MisuseCaseDialog import MisuseCaseDialog
from TaskDialog import TaskDialog
from UseCaseDialog import UseCaseDialog
from PersonaDialog import PersonaDialog
from TaskCharacteristicDialog import TaskCharacteristicDialog
from PersonaCharacteristicDialog import PersonaCharacteristicDialog
from ConceptReferenceDialog import ConceptReferenceDialog
from DomainPropertyDialog import DomainPropertyDialog
from RoleDialog import RoleDialog
from ResponseDialog import ResponseDialog
from AcceptEnvironmentPanel import AcceptEnvironmentPanel
from TransferEnvironmentPanel import TransferEnvironmentPanel
from MitigateEnvironmentPanel import MitigateEnvironmentPanel
from CountermeasureDialog import CountermeasureDialog
from ExternalDocumentDialog import ExternalDocumentDialog
from CodeDialog import CodeDialog
from MemoDialog import MemoDialog
from InternalDocumentDialog import InternalDocumentDialog

__author__ = 'Shamal Faily'

def build(dimLabel):
  dcp = None
  dimName = '' 
  dlg = None
  dlgCode = wx.ID_CLOSE
  ufn = None

  b = Borg()

  if (dimLabel == 'Document Reference'):
    dimName = 'document_reference'
    dcp = DialogClassParameters(DOCUMENTREFERENCE_ID,'Edit Document Reference')
    dlg = DocumentReferenceDialog
    dlgCode = DOCUMENTREFERENCE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateDocumentReference
  elif (dimLabel == 'Asset'):
    dimName = 'asset'
    dcp = DialogClassParameters(ASSET_ID,'Edit Asset')
    dlg = AssetDialog
    dlgCode = ASSET_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateAsset
  elif (dimLabel == 'Attacker'):
    dimName = 'attacker'
    dcp = DialogClassParameters(ATTACKER_ID,'Edit Attacker')
    dlg = AttackerDialog
    dlgCode = ATTACKER_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateAttacker
  elif (dimLabel == 'Goal'):
    dimName = 'goal'
    dcp = DialogClassParameters(GOAL_ID,'Edit Goal')
    dlg = GoalDialog
    dlgCode = GOAL_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateGoal
  elif (dimLabel == 'Obstacle'):
    dimName = 'obstacle'
    dcp = DialogClassParameters(OBSTACLE_ID,'Edit Obstacle')
    dlg = ObstacleDialog
    dlgCode = OBSTACLE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateObstacle
  elif (dimLabel == 'Vulnerability'):
    dimName = 'vulnerability'
    dcp = DialogClassParameters(VULNERABILITY_ID,'Edit Vulnerability')
    dlg = VulnerabilityDialog
    dlgCode = VULNERABILITY_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateVulnerability
  elif (dimLabel == 'Threat'):
    dimName = 'threat'
    dcp = DialogClassParameters(THREAT_ID,'Edit Threat')
    dlg = ThreatDialog
    dlgCode = THREAT_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateThreat
  elif (dimLabel == 'Misuse Case'):
    dimName = 'misusecase'
    dlg = MisuseCaseDialog
    dlgCode = MISUSECASE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateMisuseCase
  elif (dimLabel == 'Task'):
    dimName = 'task'
    dcp = DialogClassParameters(TASK_ID,'Edit Task')
    dlg = TaskDialog
    dlgCode = TASK_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateTask
  elif (dimLabel == 'Use Case'):
    dimName = 'usecase'
    dcp = DialogClassParameters(USECASE_ID,'Edit Use Case')
    dlg = UseCaseDialog
    dlgCode = USECASE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateUseCase
  elif (dimLabel == 'Persona'):
    dimName = 'persona'
    dcp = DialogClassParameters(PERSONA_ID,'Edit Persona')
    dlg = PersonaDialog
    dlgCode = PERSONA_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updatePersona
  elif (dimLabel == 'Persona Characteristic'):
    dimName = 'persona_characteristic'
    dcp = DialogClassParameters(PERSONACHARACTERISTIC_ID,'Edit Persona Characteristic')
    dlg = PersonaCharacteristicDialog
    dlgCode = PERSONACHARACTERISTIC_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updatePersonaCharacteristic
  elif (dimLabel == 'Task Characteristic'):
    dimName = 'task_characteristic'
    dcp = DialogClassParameters(TASKCHARACTERISTIC_ID,'Edit Task Characteristic')
    dlg = TaskCharacteristicDialog
    dlgCode = TASKCHARACTERISTIC_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateTaskCharacteristic
  elif (dimLabel == 'Concept Reference'):
    dimName = 'concept_reference'
    dcp = DialogClassParameters(CONCEPTREFERENCE_ID,'Edit Concept Reference')
    dlg = ConceptReferenceDialog
    dlgCode = CONCEPTREFERENCE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateConceptReference
  elif (dimLabel == 'Domain Property'):
    dimName = 'domainproperty'
    dcp = DialogClassParameters(DOMAINPROPERTY_ID,'Edit Domain Property')
    dlg = DomainPropertyDialog
    dlgCode = DOMAINPROPERTY_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateDomainProperty
  elif (dimLabel == 'Role'):
    dimName = 'role'
    dcp = DialogClassParameters(ROLE_ID,'Edit Role')
    dlg = RoleDialog
    dlgCode = ROLE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateRole
  elif (dimLabel == 'Accept'):
    dimName = 'response'
    dcp = ResponseDialogParameters(RESPONSE_ID,'Edit Response',respPanel = AcceptEnvironmentPanel, respType = 'Accept')
    dlg = ResponseDialog
    dlgCode = RESPONSE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateResponse
  elif (dimLabel == 'Transfer'):
    dimName = 'response'
    dcp = ResponseDialogParameters(RESPONSE_ID,'Edit Response',respPanel = TransferEnvironmentPanel, respType = 'Transfer')
    dlg = ResponseDialog
    dlgCode = RESPONSE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateResponse
  elif (dimLabel == 'Mitigate'):
    dimName = 'response'
    dcp = ResponseDialogParameters(RESPONSE_ID,'Edit Response',respPanel = MitigateEnvironmentPanel, respType = 'Mitigate')
    dlg = ResponseDialog
    dlgCode = RESPONSE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateResponse
  elif (dimLabel == 'Countermeasure'):
    dimName = 'countermeasure'
    dcp = DialogClassParameters(COUNTERMEASURE_ID,'Edit Countermeasure')
    dlg = CountermeasureDialog
    dlgCode = COUNTERMEASURE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateCountermeasure
  elif (dimLabel == 'External Document'):
    dimName = 'external_document'
    dcp = DialogClassParameters(EXTERNALDOCUMENT_ID,'Edit External Document')
    dlg = ExternalDocumentDialog
    dlgCode = EXTERNALDOCUMENT_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateExternalDocument
  elif (dimLabel == 'Code'):
    dimName = 'code'
    dcp = DialogClassParameters(CODE_ID,'Edit Code')
    dlg = CodeDialog
    dlgCode = CODE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateCode
  elif (dimLabel == 'Memo'):
    dimName = 'memo'
    dcp = DialogClassParameters(MEMO_ID,'Edit Memo')
    dlg = MemoDialog
    dlgCode = MEMO_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateMemo
  elif (dimLabel == 'Internal Document'):
    dimName = 'internal_document'
    dcp = DialogClassParameters(INTERNALDOCUMENT_ID,'Edit Internal Document')
    dlg = InternalDocumentDialog
    dlgCode = INTERNALDOCUMENT_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateInternalDocument
  return (dcp,dimName,dlg,dlgCode,ufn)
