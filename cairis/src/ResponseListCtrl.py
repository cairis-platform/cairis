import wx
import armid
import GoalFactory
from Borg import Borg
from ARM import *

class ResponseListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Generate Goal')
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSelectGenerate)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    generateItem = self.theTraceMenu.FindItemById(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID)
    if (evt.GetIndex() == -1):
      generateItem.Enable(False)
    else:
      response = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
      if (response.responseType() == 'Mitigate'):
        generateItem.Enable(True)
      else:
        generateItem.Enable(False)
    self.PopupMenu(self.theTraceMenu)

  def onSelectGenerate(self,evt):
    response = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    try:
      if (self.dbProxy.existingResponseGoal(response.id())):
        dlg = wx.MessageDialog(self,'A goal has already been generated for this response','Generate response goal',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      else:
        goalParameters = GoalFactory.build(response)
        riskParameters = goalParameters[0]
        riskGoalId = self.dbProxy.addGoal(riskParameters)
        self.dbProxy.addTrace('response_goal',response.id(),riskGoalId)
        if (goalParameters > 1):
          threatParameters = goalParameters[1]
          vulnerabilityParameters = goalParameters[2]
          self.dbProxy.addGoal(vulnerabilityParameters)
          self.dbProxy.addGoal(threatParameters)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate response goal',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
