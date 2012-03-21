#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DirectoryEntryDialog.py $ $Id: DirectoryEntryDialog.py 277 2010-06-28 21:31:11Z shaf $
import wx
import armid
import WidgetFactory

class DirectoryEntryDialog(wx.Dialog):
  def __init__(self,parent,dLabel,dName,dType,dDesc):
    wx.Dialog.__init__(self,parent,armid.DIRECTORYENTRY_ID,'Directory Entry',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,300))
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Label',(87,30),armid.DIRECTORYENTRY_TEXTLABEL_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.DIRECTORYENTRY_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Type',(87,30),armid.DIRECTORYENTRY_TEXTTYPE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),armid.DIRECTORYENTRY_TEXTDESCRIPTION_ID),1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.ALIGN_CENTER)
    okButton = wx.Button(self,wx.ID_OK,'Ok')
    buttonSizer.Add(okButton)
    mainSizer.Add(buttonSizer,0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    labelCtrl = self.FindWindowById(armid.DIRECTORYENTRY_TEXTLABEL_ID)
    labelCtrl.SetValue(dLabel)
    labelCtrl.Disable()
    nameCtrl = self.FindWindowById(armid.DIRECTORYENTRY_TEXTNAME_ID)
    nameCtrl.SetValue(dName)
    nameCtrl.Disable()
    typeCtrl = self.FindWindowById(armid.DIRECTORYENTRY_TEXTTYPE_ID)
    typeCtrl.SetValue(dType)
    typeCtrl.Disable()
    descCtrl = self.FindWindowById(armid.DIRECTORYENTRY_TEXTDESCRIPTION_ID)
    descCtrl.SetValue(dDesc)
    descCtrl.Disable()

  def onOk(self,evt):
    self.EndModal(wx.ID_OK)
