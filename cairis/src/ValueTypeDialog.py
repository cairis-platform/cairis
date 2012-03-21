#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ValueTypeDialog.py $ $Id: ValueTypeDialog.py 427 2011-02-27 12:29:59Z shaf $

import wx
import armid
import WidgetFactory
from ValueTypeParameters import ValueTypeParameters
from ValueTypePanel import ValueTypePanel

class ValueTypeDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(475,400))
    self.theValueTypeId = -1
    self.theValueType = parameters.type()
    self.theName = ''
    self.theDescription = ''
    self.theEnvironmentName = parameters.environment()
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ValueTypePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.VALUETYPE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theValueTypeId = objt.id()
    self.panel.loadControls(objt)
    self.theCommitVerb = 'Edit'
    if (self.theValueType == 'severity' or self.theValueType == 'likelihood'):
      nameCtrl = self.FindWindowById(armid.VALUETYPE_TEXTNAME_ID)
      nameCtrl.Disable()
     
   
  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.VALUETYPE_TEXTNAME_ID)
    descCtrl = self.FindWindowById(armid.VALUETYPE_TEXTDESCRIPTION_ID)

    self.theName = nameCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()

    commitLabel = self.theCommitVerb + ' value type'

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.VALUETYPE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ValueTypeParameters(self.theName,self.theDescription,self.theValueType,self.theEnvironmentName)
    parameters.setId(self.theValueTypeId)
    return parameters
