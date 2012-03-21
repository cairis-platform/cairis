#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RevisionEntryDialog.py $ $Id: RevisionEntryDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory

class RevisionEntryDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.REVISIONENTRY_ID,'Add Revision',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,300))
    self.theRemarks = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Remarks',(87,30),armid.REVISIONENTRY_TEXTREMARKS_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.REVISIONENTRY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.REVISIONENTRY_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'

  def onCommit(self,evt):
    remarksCtrl = self.FindWindowById(armid.REVISIONENTRY_TEXTREMARKS_ID)
    self.theRemarks = remarksCtrl.GetValue()
    if (len(self.theRemarks) == 0):
      dlg = wx.MessageDialog(self,'No revision remarks','Add revision',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.REVISIONENTRY_BUTTONCOMMIT_ID)

  def remarks(self): return self.theRemarks
