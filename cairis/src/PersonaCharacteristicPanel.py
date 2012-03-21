#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristicPanel.py $ $Id: PersonaCharacteristicPanel.py 527 2011-11-07 11:46:40Z shaf $
import wx
import armid
from BasePanel import BasePanel
from DimensionNameDialog import DimensionNameDialog
from DialogClassParameters import DialogClassParameters
from DocumentReferenceDialog import DocumentReferenceDialog
from ConceptReferenceDialog import ConceptReferenceDialog
from Borg import Borg

class PersonaCharacteristicPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.PERSONACHARACTERISTIC_ID)
    self.theId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,inPersona):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    if (inPersona == False):
      personas = self.dbProxy.getDimensionNames('persona')
      mainSizer.Add(self.buildComboSizerList('Persona',(87,30),armid.PERSONACHARACTERISTIC_COMBOPERSONA_ID,personas),0,wx.EXPAND)

    mainSizer.Add(self.buildRadioButtonSizer('Type',(87,30),[(armid.PERSONACHARACTERISTIC_RADIOREFERENCE_ID,'Reference'),(armid.PERSONACHARACTERISTIC_RADIOCONCEPT_ID,'Concept')]))

    refs = ['[New reference]']
    refs += self.dbProxy.getDimensionNames('document_reference')
    mainSizer.Add(self.buildComboSizerList('Reference',(87,30),armid.PERSONACHARACTERISTIC_COMBOREFERENCE_ID,refs),0,wx.EXPAND)

    if (inPersona == False):
      bVars = self.dbProxy.getDimensionNames('behavioural_variable')
      mainSizer.Add(self.buildComboSizerList('Behavioural Variable',(87,30),armid.PERSONACHARACTERISTIC_COMBOVARIABLE_ID,bVars),0,wx.EXPAND)

    mainSizer.Add(self.buildMLTextSizer('Characteristic',(87,30),armid.PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    wx.EVT_COMBOBOX(self,armid.PERSONACHARACTERISTIC_COMBOREFERENCE_ID,self.onReferenceChange)
    wx.EVT_RADIOBUTTON(self,armid.PERSONACHARACTERISTIC_RADIOREFERENCE_ID,self.onReferenceSelected)
    wx.EVT_RADIOBUTTON(self,armid.PERSONACHARACTERISTIC_RADIOCONCEPT_ID,self.onConceptSelected)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,inPersona):
    self.theId = objt.id()

    refCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
    charCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    refCtrl.SetValue(objt.reference())
    charCtrl.SetValue(objt.characteristic())

    if (inPersona == False):
      pCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOPERSONA_ID)
      varCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOVARIABLE_ID)
      pCtrl.SetValue(objt.persona())
      varCtrl.SetValue(objt.behaviouralVariable())

  def onReferenceChange(self,evt):
    refValue = evt.GetString()
    if (refValue == '[New reference]' or refValue == '[New concept]'):
      if (refValue == '[New reference]'):
        addParameters = DialogClassParameters(armid.DOCUMENTREFERENCE_ID,'Add Document Reference',DocumentReferenceDialog,armid.DOCUMENTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addDocumentReference,True)
      else:
        addParameters = DialogClassParameters(armid.CONCEPTREFERENCE_ID,'Add Concept Reference',ConceptReferenceDialog,armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addConceptReference,True)
      dialogClass = addParameters.dclass()
      addDialog = dialogClass(self,addParameters)
      if (addDialog.ShowModal() == addParameters.createButtonId()):
        dialogOutParameters = addDialog.parameters()
        addFn = addParameters.setter()
        objtId = addFn(dialogOutParameters)
        dimName = dialogOutParameters.name()
        refCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
        refCtrl.Append(dimName)
        refCtrl.SetValue(dimName)
      addDialog.Destroy()

  def onReferenceSelected(self,evt):
    refCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
    refs = ['[New reference]']
    refs += self.dbProxy.getDimensionNames('document_reference')
    refCtrl.SetItems(refs)
    refCtrl.SetValue('')

  def onConceptSelected(self,evt):
    refCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_COMBOREFERENCE_ID)
    refs = ['[New concept]']
    refs += self.dbProxy.getDimensionNames('concept_reference')
    refCtrl.SetItems(refs)
    refCtrl.SetValue('')

