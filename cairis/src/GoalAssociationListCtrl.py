#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalAssociationListCtrl.py $ $Id: GoalAssociationListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import ARM
from GoalRefinementDialog import GoalRefinementDialog

class GoalAssociationListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dp,goalList=False,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dbProxy = dp
    self.goalList = goalList
    self.theCurrentEnvironment = ''
    if (self.goalList == True):
      self.InsertColumn(0,'Goal')
    else:
      self.InsertColumn(0,'Sub-Goal')

    self.SetColumnWidth(0,200)
    self.InsertColumn(1,'Type')
    self.SetColumnWidth(1,100)
    self.InsertColumn(2,'Refinement')
    self.SetColumnWidth(2,100)
    self.InsertColumn(3,'Alternative')
    self.SetColumnWidth(3,50)
    self.InsertColumn(4,'Rationale')
    self.SetColumnWidth(4,200)
    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.SGA_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.SGA_MENUDELETE_ID,'Delete')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.SGA_MENUADD_ID,self.onAddAssociation)
    wx.EVT_MENU(self.theDimMenu,armid.SGA_MENUDELETE_ID,self.onDeleteAssociation)

    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onGoalActivated)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddAssociation(self,evt):
    dlg = GoalRefinementDialog(self,self.dbProxy,self.theCurrentEnvironment,isGoal=self.goalList)
    if (dlg.ShowModal() == armid.GOALREFINEMENT_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      self.InsertStringItem(self.theSelectedIdx,dlg.goal())
      self.SetStringItem(self.theSelectedIdx,1,dlg.goalDimension())
      self.SetStringItem(self.theSelectedIdx,2,dlg.refinement())
      self.SetStringItem(self.theSelectedIdx,3,dlg.alternate())
      self.SetStringItem(self.theSelectedIdx,4,dlg.rationale())

  def onDeleteAssociation(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No association selected'
      errorLabel = 'Delete goal association'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)

  
  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onGoalActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    goal = self.GetItemText(self.theSelectedIdx)
    goalDim = self.GetItem(self.theSelectedIdx,1)
    refinement = self.GetItem(self.theSelectedIdx,2)
    alternate = self.GetItem(self.theSelectedIdx,3)
    rationale = self.GetItem(self.theSelectedIdx,4)
     
    dlg = GoalRefinementDialog(self,self.dbProxy,self.theCurrentEnvironment,goal,goalDim.GetText(),refinement.GetText(),alternate.GetText())
    if (dlg.ShowModal() == armid.GOALREFINEMENT_BUTTONCOMMIT_ID):
      self.SetStringItem(self.theSelectedIdx,0,dlg.goal())
      self.SetStringItem(self.theSelectedIdx,1,dlg.goalDimension())
      self.SetStringItem(self.theSelectedIdx,2,dlg.refinement())
      self.SetStringItem(self.theSelectedIdx,3,dlg.alternate())
      self.SetStringItem(self.theSelectedIdx,4,dlg.rationale())

  def load(self,goals):
    for goal,goalDim,refinement,alternate,rationale in goals:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,goal)
      self.SetStringItem(idx,1,goalDim)
      self.SetStringItem(idx,2,refinement)
      self.SetStringItem(idx,3,alternate)
      self.SetStringItem(idx,4,rationale)

  def dimensions(self):
    goals = []
    for x in range(self.GetItemCount()):
      goal = self.GetItemText(x)
      goalDim = self.GetItem(x,1)
      refinement = self.GetItem(x,2)
      alternate = self.GetItem(x,3)
      rationale = self.GetItem(x,4)
      goals.append((goal,goalDim.GetText(),refinement.GetText(),alternate.GetText(),rationale.GetText()))
    return goals
