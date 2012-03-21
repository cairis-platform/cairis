#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponseCostDialog.py $ $Id: ResponseCostDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg

class ResponseCostDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.RESPONSECOST_ID,'Add Response Cost',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,100))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theResponseName = ''
    self.theResponseCost = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    responseList = self.dbProxy.getDimensionNames('response')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Response',(87,30),armid.RESPONSECOST_COMBORESPONSE_ID,responseList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Cost',(87,30),armid.RESPONSECOST_COMBOCOST_ID,['Low','Medium','High']),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.RESPONSECOST_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.RESPONSECOST_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    responseCtrl = self.FindWindowById(armid.RESPONSECOST_COMBORESPONSE_ID)
    costCtrl = self.FindWindowById(armid.RESPONSECOST_COMBOCOST_ID)
    self.theResponseName = responseCtrl.GetStringSelection()
    self.theResponseCost = costCtrl.GetStringSelection()

    if len(self.theResponseName) == 0:
      dlg = wx.MessageDialog(self,'No response selected','Add Response Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theResponseCost) == 0):
      dlg = wx.MessageDialog(self,'No cost selected','Add Response Cost',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.RESPONSECOST_BUTTONADD_ID)

  def response(self): return self.theResponseName

  def cost(self): return self.theResponseCost
