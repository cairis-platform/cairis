#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ExternalDocumentsDialog.py $ $Id: ExternalDocumentsDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import ExternalDocument
from ExternalDocumentDialog import ExternalDocumentDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class ExternalDocumentsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.EXTERNALDOCUMENTS_ID,'External Documents',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [armid.EXTERNALDOCUMENTS_DOCLIST_ID,armid.EXTERNALDOCUMENTS_BUTTONADD_ID,armid.EXTERNALDOCUMENTS_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getExternalDocuments,'external_document')
    listCtrl = self.FindWindowById(armid.EXTERNALDOCUMENTS_DOCLIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.EXTERNALDOCUMENT_ID,'Add External Document',ExternalDocumentDialog,armid.EXTERNALDOCUMENT_BUTTONCOMMIT_ID,self.dbProxy.addExternalDocument,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add external document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.EXTERNALDOCUMENT_ID,'Edit External Document',ExternalDocumentDialog,armid.EXTERNALDOCUMENT_BUTTONCOMMIT_ID,self.dbProxy.updateExternalDocument,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit external document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No external document','Delete external document',self.dbProxy.deleteExternalDocument)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete external document',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
