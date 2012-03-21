#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentListCtrl.py $ $Id: EnvironmentListCtrl.py 365 2010-12-14 12:21:00Z shaf $
import wx
import armid
from DimensionListCtrl import DimensionListCtrl
from SingleEnvironmentDialog import SingleEnvironmentDialog
from Borg import Borg

class EnvironmentListCtrl(DimensionListCtrl):
  def __init__(self,parent,winId,dp):
    DimensionListCtrl.__init__(self,parent,winId,wx.DefaultSize,'Environment','environment',dp,'Context of use',wx.LC_REPORT | wx.LC_SINGLE_SEL)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theInheritedEnvironment = ''
    self.theDimMenu.Append(armid.ENVLIST_MENUNEWENVIRONMENT_ID,'New Environment')
    self.theDimMenu.Append(armid.ENVLIST_MENUINHERITENVIRONMENT_ID,'Inherit Environment')
    wx.EVT_MENU(self.theDimMenu,armid.ENVLIST_MENUNEWENVIRONMENT_ID,self.onNewEnvironment)
    wx.EVT_MENU(self.theDimMenu,armid.ENVLIST_MENUINHERITENVIRONMENT_ID,self.onInheritEnvironment)

  def onNewEnvironment(self,evt):
    dlg = SingleEnvironmentDialog(self)
    if (dlg.ShowModal() == armid.ENVIRONMENT_BUTTONCOMMIT_ID):
      self.dbProxy.addEnvironment(dlg.parameters())   
      idx = self.GetItemCount()
      self.InsertStringItem(idx,dlg.name())

  def onInheritEnvironment(self,evt):
    from DimensionNameDialog import DimensionNameDialog
    dimensions = self.dbProxy.getEnvironmentNames()
    dlg = DimensionNameDialog(self,'environment',dimensions,'Inherit from ')
    if (dlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
      self.theInheritedEnvironment = dlg.dimensionName()
      adddlg = DimensionNameDialog(self,'environment',dimensions,'Add')
      if (adddlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        idx = self.GetItemCount()
        self.InsertStringItem(idx,adddlg.dimensionName())

  def inheritedEnvironment(self):
    return self.theInheritedEnvironment
