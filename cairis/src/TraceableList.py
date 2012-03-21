#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TraceableList.py $ $Id: TraceableList.py 249 2010-05-30 17:07:31Z shaf $
import armid
import wx
from Borg import Borg
from TraceExplorer import TraceExplorer
from ARM import *

class TraceableList(wx.ListCtrl):

  def __init__(self,parent,winId,dimensionName):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_TO_ID,'Supported by')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_FROM_ID,'Contributes to')
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_FROM_ID,self.onAddContributionLink)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_TO_ID,self.onAddSupportLink)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
    self.theDimensionName = dimensionName
    self.theParentDialog = parent

  def onRightClick(self,evt):
    selectItem = self.theTraceMenu.FindItemById(armid.TRACE_MENUTRACE_FROM_ID)
    if (evt.GetIndex() == -1):
      selectItem.Enable(False)  
    else:
      selectItem.Enable(True)  
    self.PopupMenu(self.theTraceMenu)

  def selectedId(self):
    if (len(self.theParentDialog.objts) == 0):
      dlg = wx.MessageDialog(self,'No Use Cases and Misuse Cases defined','Edit Scenarios', wx.OK | wx.ICON_EXCLAMATION)
      dlg.ShowModal()
      dlg.Destroy() 
      return -1
    else:
      selectedObjt = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
      return selectedObjt.id()

  def onAddContributionLink(self,evt):
    fromId = self.selectedId()
    if (fromId != -1):
      try:
        dlg = TraceExplorer(self,self.theDimensionName,True)
        if (dlg.ShowModal() == armid.TRACE_BUTTONADD_ID):
          traceToDimension = dlg.toDimension()
          linkTable = self.theDimensionName + '_' + traceToDimension
          toId = dlg.toId()
          self.dbProxy.addTrace(linkTable,fromId,toId)
        dlg.Destroy()
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add Contribution Link',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

  def onAddSupportLink(self,evt):
    toId = self.selectedId()
    if (toId != -1):
      try:
        dlg = TraceExplorer(self,self.theDimensionName,False)
        if (dlg.ShowModal() == armid.TRACE_BUTTONADD_ID):
          traceFromDimension = dlg.toDimension()
          linkTable = traceFromDimension + '_' + self.theDimensionName
          fromId = dlg.toId()
          self.dbProxy.addTrace(linkTable,fromId,toId)
        dlg.Destroy()
      except ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add support link',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return
