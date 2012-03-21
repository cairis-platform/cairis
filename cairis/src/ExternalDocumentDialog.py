#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ExternalDocumentDialog.py $ $Id: ExternalDocumentDialog.py 419 2011-01-25 21:34:13Z shaf $
import wx
import armid
from ExternalDocumentPanel import ExternalDocumentPanel
from ExternalDocumentParameters import ExternalDocumentParameters
import DialogClassParameters

class ExternalDocumentDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    self.theName = ''
    self.theVersion = ''
    self.theDate = ''
    self.theAuthors = ''
    self.theDescription = ''
    self.theId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ExternalDocumentPanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.EXTERNALDOCUMENT_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theId = objt.id()
    self.panel.loadControls(objt)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' external document'
    nameCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTNAME_ID)
    versionCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTVERSION_ID)
    dateCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTDATE_ID)
    authorsCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTAUTHORS_ID)
    descCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTDESCRIPTION_ID)
    self.theName = nameCtrl.GetValue()
    self.theVersion = versionCtrl.GetValue()
    self.theDate = dateCtrl.GetValue()
    self.theAuthors = authorsCtrl.GetValue()
    self.theDescription = descCtrl.GetValue()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theVersion) == 0:
      dlg = wx.MessageDialog(self,'Version cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDate) == 0:
      dlg = wx.MessageDialog(self,'Date cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAuthors) == 0):
      dlg = wx.MessageDialog(self,'Authors cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDescription) == 0):
      dlg = wx.MessageDialog(self,'Description cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.EXTERNALDOCUMENT_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ExternalDocumentParameters(self.theName,self.theVersion,self.theDate,self.theAuthors,self.theDescription)
    parameters.setId(self.theId)
    return parameters
