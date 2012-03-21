#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DocumentReferenceDialog.py $ $Id: DocumentReferenceDialog.py 409 2011-01-14 20:22:34Z shaf $
import wx
import armid
from DocumentReferencePanel import DocumentReferencePanel
from DocumentReferenceParameters import DocumentReferenceParameters
import DialogClassParameters

class DocumentReferenceDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,350))
    self.theName = ''
    self.theDocument = ''
    self.theContributor = ''
    self.theExcerpt = ''
    self.theId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = DocumentReferencePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.DOCUMENTREFERENCE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theId = objt.id()
    self.panel.loadControls(objt)
    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' document reference'

    nameCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTNAME_ID)
    docCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_COMBODOCNAME_ID)
    conCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTCONTRIBUTOR_ID)
    excCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTEXCERPT_ID)


    self.theName = nameCtrl.GetValue()
    self.theDocument = docCtrl.GetValue()
    self.theContributor = conCtrl.GetValue()
    self.theExcerpt = excCtrl.GetValue()

    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDocument) == 0:
      dlg = wx.MessageDialog(self,'Document cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theContributor) == 0:
      dlg = wx.MessageDialog(self,'Contributor cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.DOCUMENTREFERENCE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = DocumentReferenceParameters(self.theName,self.theDocument,self.theContributor,self.theExcerpt)
    parameters.setId(self.theId)
    return parameters
