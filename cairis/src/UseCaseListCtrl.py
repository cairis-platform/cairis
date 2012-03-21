#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReferencedCharacteristicsListCtrl.py $ $Id: ReferencedCharacteristicsListCtrl.py 260 2010-06-17 14:19:36Z shaf $
import wx
import armid
from Borg import Borg
from ARM import *
from UseCaseContributionDialog import UseCaseContributionDialog
from DimensionNameDialog import DimensionNameDialog
from ReferenceContribution import ReferenceContribution

class UseCaseListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theSelectedLabel = ""
    self.theSelectedIdx = -1
    self.theMenu = wx.Menu()
    self.theMenu.Append(armid.CLC_MENU_REFERENCECONTRIBUTION_ID,'Use Case Contribution')
    wx.EVT_MENU(self,armid.CLC_MENU_REFERENCECONTRIBUTION_ID,self.onUseCaseContribution)

    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)

    self.rsItem = self.theMenu.FindItemById(armid.CLC_MENU_REFERENCECONTRIBUTION_ID)
    self.rsItem.Enable(False)

  def onRightClick(self,evt):
    self.PopupMenu(self.theMenu)

  def OnItemSelected(self,evt):
    self.theSelectedLabel = evt.GetLabel()
    self.theSelectedIdx = evt.GetIndex()
    self.rsItem.Enable(True)

  def OnItemDeselected(self,evt):
    self.theSelectedLabel = ""
    self.theSelectedIdx = -1
    self.rsItem.Enable(False)

  def onUseCaseContribution(self,evt):
    ucName = self.GetItemText(self.theSelectedIdx)
    ucs  = self.dbProxy.getUseCaseContributions(ucName)
    ucKeys = ucs.keys()
    ucKeys.append('[New Contribution]')
    rsDlg = DimensionNameDialog(self,'usecase_contribution',ucKeys,'Select')
    if (rsDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      synName = rsDlg.dimensionName()
      rType = 'reference'
      if (synName != '[New Contribution]'):
        rc,rType = ucs[synName]
      else:
        rc = ReferenceContribution(ucName,'','','')
      dlg = UseCaseContributionDialog(self,rc,rType)
      if (dlg.ShowModal() == armid.REFERENCECONTRIBUTION_BUTTONCOMMIT_ID):
        if (rc.meansEnd() == ''):
          self.dbProxy.addUseCaseContribution(dlg.parameters())
        else:
          self.dbProxy.updateUseCaseContribution(dlg.parameters())

  def selectedLabel(self):
    return self.GetItemText(self.theSelectedIdx)
