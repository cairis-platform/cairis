#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalListCtrl.py $ $Id: GoalListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import GoalRequirementFactory
from Borg import Borg
from DimensionNameDialog import DimensionNameDialog
from ARM import *

class GoalListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,'Generate Requirement')
    self.theRequirementGrid = parent.theMainWindow.requirementGrid()
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_GENERATESPECIFIC_ID,self.onSelectGenerate)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onSelectGenerate(self,evt):
    objt = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
#    objtId = objt.id()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      domains = dbProxy.getDimensionNames('domain',False)
      cDlg = DimensionNameDialog(self,'domain',domains,'Select')
      if (cDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        domainName = cDlg.dimensionName()
        GoalRequirementFactory.build(objt,domainName,self.theParentDialog.theMainWindow)
# Change domain in panel
# Add requirement
# add goalrequirement_goalassociation
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Generate goal requirement',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
