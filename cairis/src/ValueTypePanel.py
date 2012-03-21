#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ValueTypePanel.py $ $Id: ValueTypePanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory

class ValueTypePanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.ROLE_ID)

  def buildControls(self,isCreate):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.VALUETYPE_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,80),armid.VALUETYPE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.VALUETYPE_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt):
    nameCtrl = self.FindWindowById(armid.VALUETYPE_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.VALUETYPE_TEXTDESCRIPTION_ID)
    nameCtrl.SetValue(objt.name())
    descCtrl.SetValue(objt.description())
