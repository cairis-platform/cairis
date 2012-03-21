#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DictionaryEntryDialog.py $ $Id: DictionaryEntryDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory

class DictionaryEntryDialog(wx.Dialog):
  def __init__(self,parent,name = '',definition = ''):
    wx.Dialog.__init__(self,parent,armid.DICTIONARYENTRY_ID,'Add Dictionary Entry',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,300))
    self.theName = name
    self.theDefinition = definition
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.DICTIONARYENTRY_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Definition',(87,30),armid.DICTIONARYENTRY_TEXTDEFINITION_ID),1,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.DICTIONARYENTRY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.DICTIONARYENTRY_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theName) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Dictionary Entry')
      nameCtrl = self.FindWindowById(armid.DICTIONARYENTRY_TEXTNAME_ID)
      nameCtrl.SetValue(self.theName)
      defCtrl = self.FindWindowById(armid.DICTIONARYENTRY_TEXTDEFINITION_ID)
      defCtrl.SetValue(self.theDefinition)
      buttonCtrl = self.FindWindowById(armid.DICTIONARYENTRY_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.DICTIONARYENTRY_TEXTNAME_ID)
    defCtrl = self.FindWindowById(armid.DICTIONARYENTRY_TEXTDEFINITION_ID)

    self.theName = nameCtrl.GetValue()
    self.theDefinition = defCtrl.GetValue()

    if (len(self.theName) == 0):
      dlg = wx.MessageDialog(self,'No name entry',self.commitLabel + ' Dictionary Entry',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDefinition) == 0):
      dlg = wx.MessageDialog(self,'No definition entry',self.commitLabel + ' Dictionary Entry',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.DICTIONARYENTRY_BUTTONCOMMIT_ID)

  def name(self): return self.theName
  def definition(self): return self.theDefinition
