#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainPropertyDialog.py $ $Id: DomainPropertyDialog.py 511 2011-10-30 15:48:53Z shaf $
import wx
import armid
from DomainPropertyPanel import DomainPropertyPanel
from DomainPropertyParameters import DomainPropertyParameters
import DialogClassParameters

class DomainPropertyDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    self.theId = -1
    self.theName = ''
    self.theType = ''
    self.theOriginator = ''
    self.theDescription = ''
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = DomainPropertyPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.DOMAINPROPERTY_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,dp):
    self.theId = dp.id()
    self.panel.loadControls(dp)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(armid.DOMAINPROPERTY_COMBOTYPE_ID)
    origCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTORIGINATOR_ID)
    descCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTDESCRIPTION_ID)

    self.theName = nameCtrl.GetValue()
    self.theType = typeCtrl.GetValue()
    self.theOriginator = origCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()

    commitLabel = self.commitVerb + ' Domain Property'
    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Property name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Domain Property type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theOriginator) == 0:
      dlg = wx.MessageDialog(self,'Originator cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Domain Property description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.DOMAINPROPERTY_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = DomainPropertyParameters(self.theName,self.theDescription,self.theType,self.theOriginator)
    parameters.setId(self.theId)
    return parameters
