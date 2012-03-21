#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TracesDialog.py $ $Id: TracesDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import ObjectFactory
import armid
import Trace
import TraceDialog
import DialogClassParameters
import TraceDialogParameters
import DimensionBaseDialog
import ARM

class TracesDialog(DimensionBaseDialog.DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.DimensionBaseDialog.__init__(self,parent,armid.TRACES_ID,'Traces',(800,300))
    self.traces = self.dbProxy.riskAnalysisModel()
    idList = [armid.TRACES_LISTTRACES_ID,armid.TRACES_BUTTONADD_ID,armid.TRACES_BUTTONDELETE_ID]
    columnList = ['From','Description','To','Description']
    self.buildControls(idList,columnList,0,'trace')

  def addObjectRow(self,listCtrl,listRow,trace):
    listCtrl.InsertStringItem(listRow,trace.fromObject())
    listCtrl.SetStringItem(listRow,1,trace.fromName())
    listCtrl.SetStringItem(listRow,2,trace.toObject())
    listCtrl.SetStringItem(listRow,3,trace.toName())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters.DialogClassParameters(armid.TRACE_ID,'Add trace',TraceDialog.TraceDialog,armid.TRACE_BUTTONCOMMIT_ID,self.dbProxy.addTrace,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add trace',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedIdx = evt.GetIndex()
    selectedObjt = self.traces[selectedIdx]
    try:
      updateParameters = TraceDialogParameters.TraceDialogParameters(armid.TRACE_ID,'Edit trace',TraceDialog.TraceDialog,armid.TRACE_BUTTONCOMMIT_ID,self.dbProxy.updateTrace,False,selectedObjt.fromObject(),selectedObjt.fromId(),selectedObjt.toObject(),selectedObjt.toId())
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit trace',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy


  def onDelete(self,evt):
    if len(self.selectedLabel) == 0:
      dlg = wx.MessageDialog(self,'No trace','Delete trace',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      objtToGo = self.traces[self.selectedIdx]
      del self.traces[self.selectedIdx]
      self.dbProxy.deleteTrace(objtToGo.fromId(),objtToGo.toId())
      listCtrl = self.FindWindowById(self.listId)
      listCtrl.DeleteItem(self.selectedIdx)
      self.selectedLabel = ''
    return

  def addObjectToDialog(self,objtId,listId,dialogParameters):
    listCtrl = self.FindWindowById(self.listId)
    listRow = listCtrl.GetItemCount()
    newObjt = ObjectFactory.build(objtId,dialogParameters)
    self.addObjectRow(listCtrl,listRow,newObjt)
    self.traces.append(newObjt)

  def updateDialogObject(self,objtId,listId,dialogParameters):
    objtToGo = self.traces[self.selectedIdx]
    del self.traces[self.selectedIdx]
    listCtrl = self.FindWindowById(self.listId)
    listCtrl.DeleteItem(self.selectedIdx)
    updatedObjt = ObjectFactory.build(-1,dialogParameters)
    self.addObjectRow(listCtrl,self.selectedIdx,updatedObjt)
    self.traces.insert(self.selectedIdx,updatedObjt)
