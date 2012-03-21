#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CapabilityDialog.py $ $Id: CapabilityDialog.py 330 2010-10-31 15:01:28Z shaf $
import wx
import armid
import WidgetFactory

class CapabilityDialog(wx.Dialog):
  def __init__(self,parent,setCapabilities,dp):
    wx.Dialog.__init__(self,parent,armid.CAPABILITY_ID,'Add Capability',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,150))
    self.theCapabilityName = ''
    self.theCapabilityValue = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    defaultCapabilities = set(dp.getDimensionNames('capability'))
    capabilityList = list(defaultCapabilities.difference(setCapabilities))
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Capability',(87,30),armid.CAPABILITY_COMBOCAPABILITY_ID,capabilityList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Value',(87,30),armid.CAPABILITY_COMBOVALUE_ID,['Low','Medium','High']),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.CAPABILITY_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.CAPABILITY_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    capCtrl = self.FindWindowById(armid.CAPABILITY_COMBOCAPABILITY_ID)
    valueCtrl = self.FindWindowById(armid.CAPABILITY_COMBOVALUE_ID)
    self.theCapabilityName = capCtrl.GetStringSelection()
    self.theCapabilityValue = valueCtrl.GetStringSelection()

    if len(self.theCapabilityName) == 0:
      dlg = wx.MessageDialog(self,'No capability selected','Add Capability',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theCapabilityValue) == 0):
      dlg = wx.MessageDialog(self,'No value selected','Add Capability',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.CAPABILITY_BUTTONADD_ID)

  def capability(self): return self.theCapabilityName

  def value(self): return self.theCapabilityValue
