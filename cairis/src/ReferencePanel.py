#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReferencePanel.py $ $Id: ReferencePanel.py 527 2011-11-07 11:46:40Z shaf $

import wx
import armid
from BasePanel import BasePanel
from DialogClassParameters import DialogClassParameters
from DocumentReferenceDialog import DocumentReferenceDialog
from ConceptReferenceDialog import ConceptReferenceDialog
from Borg import Borg

class ReferencePanel(BasePanel):
  def __init__(self,parent,refName,descName,dimName):
    BasePanel.__init__(self,parent,armid.CHARACTERISTICREFERENCEPANEL_ID)
    self.theId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    isCreate = True
    self.newArtifactString = '[New artifact reference]'
    self.newConceptString = '[New concept reference]'
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    dims = ['document','asset','attacker','countermeasure','domainproperty','environment','goal','misusecase','obstacle','persona','requirement','response','risk','role','task','threat','vulnerability']
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.CHARACTERISTICREFERENCE_COMBODIMENSION_ID,dims),0,wx.EXPAND)
    mainSizer.Add(self.buildComboSizerList('Artifact',(87,30),armid.CHARACTERISTICREFERENCE_COMBODOCUMENT_ID,[]),0,wx.EXPAND)

    self.docNameCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBODOCUMENT_ID)
    self.docNameCtrl.Disable()

    if (dimName != ''):
      dimCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBODIMENSION_ID)
      dimCtrl.SetValue(dimName)
      isCreate = False
       
    mainSizer.Add(self.buildComboSizerList('Reference',(87,30),armid.CHARACTERISTICREFERENCE_COMBOREFERENCE_ID,[self.newArtifactString,self.newConceptString]),0,wx.EXPAND)

    mainSizer.Add(self.buildMLTextSizer('Description',(87,60),armid.CHARACTERISTICREFERENCE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    descCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_TEXTDESCRIPTION_ID)

    if (refName != ''):
      refCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBOREFERENCE_ID)
      refs = [self.newArtifactString,self.newConceptString]
      dimTable = dimName + '_reference'
      refs += self.dbProxy.getDimensionNames(dimTable)
      refCtrl.SetItems(refs)
      refCtrl.SetValue(refName)
      descCtrl.SetValue(descName)

    mainSizer.Add(self.buildCommitButtonSizer(armid.CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)

    if (dimName != ''):
      buttonCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')

    wx.EVT_COMBOBOX(self,armid.CHARACTERISTICREFERENCE_COMBODIMENSION_ID,self.onDimensionChange)
    wx.EVT_COMBOBOX(self,armid.CHARACTERISTICREFERENCE_COMBODOCUMENT_ID,self.onDocumentChange)
    wx.EVT_COMBOBOX(self,armid.CHARACTERISTICREFERENCE_COMBOREFERENCE_ID,self.onReferenceChange)
    self.SetSizer(mainSizer)
    mainSizer.Layout()

  def onDocumentChange(self,evt):
    docName = evt.GetString()
    if (docName != ''):
      refCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBOREFERENCE_ID)
      descCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_TEXTDESCRIPTION_ID)
      refNames = [self.newArtifactString,self.newConceptString]
      refNames += self.dbProxy.documentReferenceNames(docName)
      refCtrl.SetItems(refNames)
      refCtrl.Enable()
      descCtrl.SetValue('')
    
  def onDimensionChange(self,evt):
    dimValue = evt.GetString()
    if (dimValue != ''):
      refCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBOREFERENCE_ID)
      descCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_TEXTDESCRIPTION_ID)
      if (dimValue == 'document'):
        self.docNameCtrl.Enable()
        docs = self.dbProxy.getDimensionNames('external_document')
        self.docNameCtrl.SetItems(docs)
        self.docNameCtrl.SetValue('')
        refCtrl.SetItems([])
        refCtrl.SetValue('')
        descCtrl.SetValue('')
        refCtrl.Enable()
      else:
        self.docNameCtrl.Disable()
        self.docNameCtrl.SetValue('')
        self.docNameCtrl.SetItems([])
        refs = [self.newArtifactString,self.newConceptString]
        dimTable = dimValue + '_reference'
        refs += self.dbProxy.getDimensionNames(dimTable)
        refCtrl.SetItems(refs)
        refCtrl.SetValue('')
        descCtrl.SetValue('')
        refCtrl.Enable()
      


  def onReferenceChange(self,evt):
    refValue = evt.GetString()
    descCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_TEXTDESCRIPTION_ID)
    
    if (refValue == self.newArtifactString or refValue == self.newConceptString):
      if (refValue == self.newArtifactString):
        addParameters = DialogClassParameters(armid.DOCUMENTREFERENCE_ID,'Add Artifact Reference',DocumentReferenceDialog,armid.DOCUMENTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addDocumentReference,True)
      else:
        addParameters = DialogClassParameters(armid.CONCEPTREFERENCE_ID,'Add Concept Reference',ConceptReferenceDialog,armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addConceptReference,True)
      dialogClass = addParameters.dclass()
      addDialog = dialogClass(self,addParameters)
      if (addDialog.ShowModal() == addParameters.createButtonId()):
        dialogOutParameters = addDialog.parameters()
        addFn = addParameters.setter()
        objtId = addFn(dialogOutParameters)
        dimName = dialogOutParameters.name()
        refDesc = dialogOutParameters.description()
        refCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBOREFERENCE_ID)
        refCtrl.Append(dimName)
        refCtrl.SetValue(dimName)
        descCtrl.SetValue(refDesc)
      addDialog.Destroy()
    else:
      dimCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBODIMENSION_ID)
      dimName = dimCtrl.GetValue()
      refDesc = self.dbProxy.referenceDescription(dimName,refValue)
      descCtrl.SetValue(refDesc)
