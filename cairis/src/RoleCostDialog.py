#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleCostDialog.py $ $Id: RoleCostDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg

class RoleCostDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.ROLECOST_ID,'Add Role Cost',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,140))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theRoleName = ''
    self.theRoleCost = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    roleList = self.dbProxy.getDimensionNames('role')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Role',(87,30),armid.ROLECOST_COMBOROLE_ID,roleList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Cost',(87,30),armid.ROLECOST_COMBOCOST_ID,['Low','Medium','High']),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.ROLECOST_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.ROLECOST_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    roleCtrl = self.FindWindowById(armid.ROLECOST_COMBOROLE_ID)
    costCtrl = self.FindWindowById(armid.ROLECOST_COMBOCOST_ID)
    self.theRoleName = roleCtrl.GetStringSelection()
    self.theRoleCost = costCtrl.GetStringSelection()

    if len(self.theRoleName) == 0:
      dlg = wx.MessageDialog(self,'No role selected','Add Role Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRoleCost) == 0):
      dlg = wx.MessageDialog(self,'No cost selected','Add Role Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.ROLECOST_BUTTONADD_ID)

  def role(self): return self.theRoleName

  def cost(self): return self.theRoleCost
