#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReferenceDialog.py $ $Id: ReferenceDialog.py 329 2010-10-31 14:59:16Z shaf $
import wx
import armid
from ReferencePanel import ReferencePanel
import DialogClassParameters

class ReferenceDialog(wx.Dialog):
  def __init__(self,parent,crTypeName,refName = '',desc = '',dimName = ''):
    wx.Dialog.__init__(self,parent,armid.CHARACTERISTICREFERENCE_ID,'Add Characteristic Reference',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    self.theCharacteristicReferenceType = crTypeName
    self.theReferenceName = refName
    self.theDescription = desc
    self.theDimensionName = dimName
    self.commitVerb = 'Add'

    if refName != '':
      self.commitVerb = 'Edit'
      self.SetTitle('Edit Characteristic Reference')

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ReferencePanel(self,self.theReferenceName,self.theDescription, self.theDimensionName)


    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' Characteristic Reference'

    refCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBOREFERENCE_ID)
    descCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_TEXTDESCRIPTION_ID)
    dimCtrl = self.FindWindowById(armid.CHARACTERISTICREFERENCE_COMBODIMENSION_ID)

    self.theReferenceName = refCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()
    self.theDimensionName = dimCtrl.GetValue()


    if len(self.theReferenceName) == 0:
      dlg = wx.MessageDialog(self,'Reference name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDimensionName) == 0:
      dlg = wx.MessageDialog(self,'Dimension name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDescription) == 0:
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID)

  def reference(self):
    return self.theReferenceName

  def dimension(self):
    return self.theDimensionName

  def description(self):
    return self.theDescription
