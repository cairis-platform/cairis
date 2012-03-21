#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleDialog.py $ $Id: RoleDialog.py 395 2011-01-06 01:17:45Z shaf $
import wx
import armid
import WidgetFactory
import ARM
from Borg import Borg
from RoleParameters import RoleParameters
from RolePanel import RolePanel

class RoleDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(475,400))
    self.theRoleId = -1
    self.theName = ''
    self.theType = ''
    self.theShortCode = ''
    self.theDescription = ''
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = RolePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.ROLE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,role):
    self.theRoleId = role.id()
    self.panel.loadControls(role)
    self.theCommitVerb = 'Edit'
   

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.ROLE_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(armid.ROLE_COMBOTYPE_ID)
    scCtrl = self.FindWindowById(armid.ROLE_TEXTSHORTCODE_ID)
    descCtrl = self.FindWindowById(armid.ROLE_TEXTDESCRIPTION_ID)

    self.theName = nameCtrl.GetValue()
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theName,'role')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add role',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theType = typeCtrl.GetValue()
    self.theShortCode = scCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()

    commitLabel = self.theCommitVerb + ' role'

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Role name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Role type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theShortCode) == 0:
      dlg = wx.MessageDialog(self,'Short code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Role description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.ROLE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = RoleParameters(self.theName,self.theType,self.theShortCode,self.theDescription,[])
    parameters.setId(self.theRoleId)
    return parameters
