#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DependentsDialog.py $ $Id: DependentsDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid

class DependentsDialog(wx.Dialog):
  def __init__(self,parent,dependents,dimName):
    wx.Dialog.__init__(self,parent,armid.DEPENDENTS_ID,'Delete ' + dimName,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    labelTxt = 'The following artifacts are dependent on this ' + dimName + ', and removing it also removes them.\n  Do you want to continue?'
    mainSizer.Add(wx.StaticText(self,-1,labelTxt),0,wx.EXPAND)
    dependentsListCtrl = wx.ListCtrl(self,-1,style=wx.LC_REPORT)
    dependentsListCtrl.InsertColumn(0,"Artifact")
    dependentsListCtrl.InsertColumn(1,"Name")
    
    for idx,artifact in enumerate(dependents):
      dimName = artifact[0]
      objtName = artifact[2]
      dependentsListCtrl.InsertStringItem(idx,dimName)
      dependentsListCtrl.SetStringItem(idx,1,objtName)
    dependentsListCtrl.SetColumnWidth(0,75)
    dependentsListCtrl.SetColumnWidth(1,200)
    mainSizer.Add(dependentsListCtrl,1,wx.EXPAND)
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.CENTER)
    yesButton = wx.Button(self,armid.DEPENDENTS_BUTTONCONFIRM_ID,"Yes")
    buttonSizer.Add(yesButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Cancel")
    buttonSizer.Add(cancelButton)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.DEPENDENTS_BUTTONCONFIRM_ID,self.onConfirm)

  def onConfirm(self,evt):
    self.EndModal(armid.DEPENDENTS_BUTTONCONFIRM_ID)
