#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetDialog.py $ $Id: AssetDialog.py 330 2010-10-31 15:01:28Z shaf $
import wx
import armid
import ARM
from SearchPanel import SearchPanel
from Borg import Borg

class SearchDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.SEARCHMODEL_ID,'Search model',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(700,500))
    b = Borg()
    self.dbProxy = b.dbProxy
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = SearchPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.SEARCHMODEL_BUTTONFIND_ID,self.onFind)

  def onFind(self,evt):
    ssCtrl = self.FindWindowById(armid.SEARCHMODEL_TEXTSEARCHSTRING_ID)
    ssValue = ssCtrl.GetValue()

    if (len(ssValue) == 0) or (ssValue == ' '):
      dlg = wx.MessageDialog(self,'Search string empty','Search model',wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return

    listCtrl = self.FindWindowById(armid.SEARCHMODEL_LISTRESULTS_ID)
    listCtrl.DeleteAllItems()
    searchOptionsCtrl = self.FindWindowById(armid.SEARCHOPTIONSPANEL_ID)
    searchOptions = searchOptionsCtrl.optionFlags()

    try:
      searchResults = self.dbProxy.searchModel(ssValue,searchOptions)
      for idx,result in enumerate(searchResults):
        listCtrl.InsertStringItem(idx,result[0])
        listCtrl.SetStringItem(idx,1,result[1])
        listCtrl.SetStringItem(idx,2,result[2])
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Search model',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
