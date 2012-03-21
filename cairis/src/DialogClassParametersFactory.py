#$Id: DialogClassParametersFactory.py 415 2011-01-21 14:59:08Z shaf $
import wx
import armid
from ResponseDialogParameters import ResponseDialogParameters
from DialogClassParameters import DialogClassParameters
from Borg import Borg
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

def build(dimLabel):
  dcp = None
  dimName = '' 
  dlg = None
  dlgCode = wx.ID_CLOSE
  ufn = None

  b = Borg()

  if (dimLabel == 'Document Reference'):
    dimName = 'document_reference'
    dcp = DialogClassParameters(armid.DOCUMENTREFERENCE_ID,'Edit Document Reference')
    dlg = DocumentReferenceDialog
    dlgCode = armid.DOCUMENTREFERENCE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateDocumentReference
  elif (dimLabel == 'Asset'):
    dimName = 'asset'
    dcp = DialogClassParameters(armid.ASSET_ID,'Edit Asset')
    dlg = AssetDialog
    dlgCode = armid.ASSET_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateAsset
  elif (dimLabel == 'Attacker'):
    dimName = 'attacker'
    dcp = DialogClassParameters(armid.ATTACKER_ID,'Edit Attacker')
    dlg = AttackerDialog
    dlgCode = armid.ATTACKER_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateAttacker
  elif (dimLabel == 'Goal'):
    dimName = 'goal'
    dcp = DialogClassParameters(armid.GOAL_ID,'Edit Goal')
    dlg = GoalDialog
    dlgCode = armid.GOAL_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateGoal
  elif (dimLabel == 'Obstacle'):
    dimName = 'obstacle'
    dcp = DialogClassParameters(armid.OBSTACLE_ID,'Edit Obstacle')
    dlg = ObstacleDialog
    dlgCode = armid.OBSTACLE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateObstacle
  elif (dimLabel == 'Vulnerability'):
    dimName = 'vulnerability'
    dcp = DialogClassParameters(armid.VULNERABILITY_ID,'Edit Vulnerability')
    dlg = VulnerabilityDialog
    dlgCode = armid.VULNERABILITY_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateVulnerability
  elif (dimLabel == 'Threat'):
    dimName = 'threat'
    dcp = DialogClassParameters(armid.THREAT_ID,'Edit Threat')
    dlg = ThreatDialog
    dlgCode = armid.THREAT_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateThreat
  elif (dimLabel == 'Misuse Case'):
    dimName = 'misusecase'
    dlg = MisuseCaseDialog
    dlgCode = armid.MISUSECASE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateMisuseCase
  elif (dimLabel == 'Task'):
    dimName = 'task'
    dcp = DialogClassParameters(armid.TASK_ID,'Edit Task')
    dlg = TaskDialog
    dlgCode = armid.TASK_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateTask
  elif (dimLabel == 'Use Case'):
    dimName = 'usecase'
    dcp = DialogClassParameters(armid.USECASE_ID,'Edit Use Case')
    dlg = UseCaseDialog
    dlgCode = armid.USECASE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateUseCase
  elif (dimLabel == 'Persona'):
    dimName = 'persona'
    dcp = DialogClassParameters(armid.PERSONA_ID,'Edit Persona')
    dlg = PersonaDialog
    dlgCode = armid.PERSONA_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updatePersona
  elif (dimLabel == 'Persona Characteristic'):
    dimName = 'persona_characteristic'
    dcp = DialogClassParameters(armid.PERSONACHARACTERISTIC_ID,'Edit Persona Characteristic')
    dlg = PersonaCharacteristicDialog
    dlgCode = armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updatePersonaCharacteristic
  elif (dimLabel == 'Task Characteristic'):
    dimName = 'task_characteristic'
    dcp = DialogClassParameters(armid.TASKCHARACTERISTIC_ID,'Edit Task Characteristic')
    dlg = TaskCharacteristicDialog
    dlgCode = armid.TASKCHARACTERISTIC_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateTaskCharacteristic
  elif (dimLabel == 'Concept Reference'):
    dimName = 'concept_reference'
    dcp = DialogClassParameters(armid.CONCEPTREFERENCE_ID,'Edit Concept Reference')
    dlg = ConceptReferenceDialog
    dlgCode = armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateConceptReference
  elif (dimLabel == 'Domain Property'):
    dimName = 'domainproperty'
    dcp = DialogClassParameters(armid.DOMAINPROPERTY_ID,'Edit Domain Property')
    dlg = DomainPropertyDialog
    dlgCode = armid.DOMAINPROPERTY_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateDomainProperty
  elif (dimLabel == 'Role'):
    dimName = 'role'
    dcp = DialogClassParameters(armid.ROLE_ID,'Edit Role')
    dlg = RoleDialog
    dlgCode = armid.ROLE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateRole
  elif (dimLabel == 'Accept'):
    dimName = 'response'
    dcp = ResponseDialogParameters(armid.RESPONSE_ID,'Edit Response',respPanel = AcceptEnvironmentPanel, respType = 'Accept')
    dlg = ResponseDialog
    dlgCode = armid.RESPONSE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateResponse
  elif (dimLabel == 'Transfer'):
    dimName = 'response'
    dcp = ResponseDialogParameters(armid.RESPONSE_ID,'Edit Response',respPanel = TransferEnvironmentPanel, respType = 'Transfer')
    dlg = ResponseDialog
    dlgCode = armid.RESPONSE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateResponse
  elif (dimLabel == 'Mitigate'):
    dimName = 'response'
    dcp = ResponseDialogParameters(armid.RESPONSE_ID,'Edit Response',respPanel = MitigateEnvironmentPanel, respType = 'Mitigate')
    dlg = ResponseDialog
    dlgCode = armid.RESPONSE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateResponse
  elif (dimLabel == 'Countermeasure'):
    dimName = 'countermeasure'
    dcp = DialogClassParameters(armid.COUNTERMEASURE_ID,'Edit Countermeasure')
    dlg = CountermeasureDialog
    dlgCode = armid.COUNTERMEASURE_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateCountermeasure
  elif (dimLabel == 'External Document'):
    dimName = 'external_document'
    dcp = DialogClassParameters(armid.EXTERNALDOCUMENT_ID,'Edit External Document')
    dlg = ExternalDocumentDialog
    dlgCode = armid.EXTERNALDOCUMENT_BUTTONCOMMIT_ID
    ufn = b.dbProxy.updateExternalDocument
  return (dcp,dimName,dlg,dlgCode,ufn)
