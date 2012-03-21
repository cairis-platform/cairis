#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentGrid.py $ $Id: EnvironmentGrid.py 503 2011-10-28 13:04:39Z shaf $
import armid
from Traceable import Traceable
import wx
from ARM import *
from RequirementHistoryDialog import RequirementHistoryDialog
from TraceExplorer import TraceExplorer
from GoalAssociationParameters import GoalAssociationParameters
from Borg import Borg

class EnvironmentGrid(Traceable):
  def __init__(self):
    Traceable.__init__(self)
    self.theTraceMenu.Enable(armid.TRACE_MENUTRACE_TO_ID,False)
    self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onRightClick)

  def onAddSupportLink(self,evt):
    pass

  def onAddContributionLink(self,evt):
    try:
      objtTable = self.GetTable()
      selectedObjt = (objtTable.om.objects())[self.GetGridCursorRow()]
      self.onTraceFrom(objtTable.dimension,selectedObjt.id(),objtTable.envName)
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add contribution link',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onTrace(self,dimensionName,fromId,isFrom,envName):
    dlg = TraceExplorer(self,dimensionName,isFrom,envName)
    if (dlg.ShowModal() == armid.TRACE_BUTTONADD_ID):
      objtTable = self.GetTable()
      objtName = ((objtTable.om.objects())[self.GetGridCursorRow()]).name()
      p = GoalAssociationParameters(envName,objtName,dimensionName,'and',dlg.toValue(),dlg.toDimension(),0,'')
      self.dbProxy.addGoalAssociation(p)
    dlg.Destroy()
