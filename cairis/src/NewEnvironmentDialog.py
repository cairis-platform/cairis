#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/NewEnvironmentDialog.py $ $Id: NewEnvironmentDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory

class NewEnvironmentDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.NEWENVIRONMENT_ID,'New Environment',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,200))
    self.environmentName = ''
    self.environmentDescription = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.NEWENVIRONMENT_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),armid.NEWENVIRONMENT_TEXTSHORTCODE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),armid.NEWENVIRONMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.NEWENVIRONMENT_BUTTONCOMMIT_ID,True))
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.NEWENVIRONMENT_BUTTONCOMMIT_ID,self.onCreate)


  def onCreate(self,evt):
    nameCtrl = self.FindWindowById(armid.NEWENVIRONMENT_TEXTNAME_ID)
    shortCodeCtrl = self.FindWindowById(armid.NEWENVIRONMENT_TEXTSHORTCODE_ID)
    valueCtrl = self.FindWindowById(armid.NEWENVIRONMENT_TEXTDESCRIPTION_ID)
    self.environmentName = nameCtrl.GetValue()
    self.shortCode = shortCodeCtrl.GetValue()
    self.environmentDescription = valueCtrl.GetValue()

    if len(self.environmentName) == 0:
      dlg = wx.MessageDialog(self,'Environment name cannot be empty','Create environment',wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.shortCode) == 0):
      dlg = wx.MessageDialog(self,'Environment short code cannot be empty','Create environment',wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.environmentDescription) == 0):
      dlg = wx.MessageDialog(self,'Environment description cannot be empty','Create environment',wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(wx.ID_OK)

  def name(self):
    return self.environmentName

  def description(self):
    return self.environmentDescription

  def shortCode(self):
    return self.shortCode

