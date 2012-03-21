#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TemplateAssetDialog.py $ $Id: TemplateAssetDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from TemplateAssetPanel import TemplateAssetPanel
from TemplateAssetParameters import TemplateAssetParameters
import DialogClassParameters

class TemplateAssetDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.theAssetName = ''
    self.theShortCode = ''
    self.theAssetDescription = ''
    self.theAssetSignificance = ''
    self.theType = ''
    self.theCriticalIndicator = False
    self.theCriticalRationale = ''
    self.theSecurityProperties = []
    self.theAssetId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = TemplateAssetPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.TEMPLATEASSET_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,asset):
    self.theAssetId = asset.id()
    self.panel.loadControls(asset)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' template asset'
    nameCtrl = self.FindWindowById(armid.ASSET_TEXTNAME_ID)
    shortCodeCtrl = self.FindWindowById(armid.ASSET_TEXTSHORTCODE_ID)
    descriptionCtrl = self.FindWindowById(armid.ASSET_TEXTDESCRIPTION_ID)
    sigCtrl = self.FindWindowById(armid.ASSET_TEXTSIGNIFICANCE_ID)
    typeCtrl = self.FindWindowById(armid.ASSET_COMBOTYPE_ID)
    criticalCtrl = self.FindWindowById(armid.ASSET_CHECKCRITICAL_ID)
    criticalRationaleCtrl = self.FindWindowById(armid.ASSET_TEXTCRITICALRATIONALE_ID)
    propertiesCtrl = self.FindWindowById(armid.TEMPLATEASSET_LISTPROPERTIES_ID)
    self.theAssetName = nameCtrl.GetValue()
    self.theShortCode = shortCodeCtrl.GetValue()
    self.theAssetDescription = descriptionCtrl.GetValue()
    self.theAssetSignificance = sigCtrl.GetValue()
    self.theType = typeCtrl.GetValue()
    self.theCriticalIndicator = criticalCtrl.GetValue()
    self.theCriticalRationale = criticalRationaleCtrl.GetValue()
    self.theSecurityProperties = propertiesCtrl.properties()

    if len(self.theAssetName) == 0:
      dlg = wx.MessageDialog(self,'Asset name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theShortCode) == 0:
      dlg = wx.MessageDialog(self,'Short code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theType) == 0:
      dlg = wx.MessageDialog(self,'Asset type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAssetDescription) == 0):
      dlg = wx.MessageDialog(self,'Asset description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAssetSignificance) == 0):
      dlg = wx.MessageDialog(self,'Asset significance cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.TEMPLATEASSET_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = TemplateAssetParameters(self.theAssetName,self.theShortCode,self.theAssetDescription,self.theAssetSignificance,self.theType,self.theCriticalIndicator,self.theCriticalRationale,self.theSecurityProperties[0],self.theSecurityProperties[1],self.theSecurityProperties[2],self.theSecurityProperties[3])
    parameters.setId(self.theAssetId)
    return parameters
