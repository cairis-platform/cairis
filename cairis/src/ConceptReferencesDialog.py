#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ConceptReferencesDialog.py $ $Id: ConceptReferencesDialog.py 459 2011-04-02 09:36:25Z shaf $
import wx
import armid
import ConceptReference
from ConceptReferenceDialog import ConceptReferenceDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class ConceptReferencesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.CONCEPTREFERENCES_ID,'Concept References',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [armid.CONCEPTREFERENCES_REFLIST_ID,armid.CONCEPTREFERENCES_BUTTONADD_ID,armid.CONCEPTREFERENCES_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getConceptReferences,'concept_reference')
    listCtrl = self.FindWindowById(armid.CONCEPTREFERENCES_REFLIST_ID)
    listCtrl.SetColumnWidth(0,800)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.CONCEPTREFERENCE_ID,'Add Concept Reference',ConceptReferenceDialog,armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.addConceptReference,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add concept reference',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.CONCEPTREFERENCE_ID,'Edit Concept Reference',ConceptReferenceDialog,armid.CONCEPTREFERENCE_BUTTONCOMMIT_ID,self.dbProxy.updateConceptReference,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit concept reference',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No concept reference','Delete concept reference',self.dbProxy.deleteConceptReference)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete concept reference',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
