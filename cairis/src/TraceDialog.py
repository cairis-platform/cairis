#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TraceDialog.py $ $Id: TraceDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
import TraceParameters
import UpdateTraceParameters
import TracePanel

class TraceDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,275))
    if (parameters.__class__.__name__ == 'TraceDialogParameters'):
      self.theOriginalFromObject = parameters.fromObject()
      self.theOriginalFromId = parameters.fromId()
      self.theOriginalToObject = parameters.toObject()
      self.theOriginalToId = parameters.toId()
    else:
      self.theOriginalFromObject = -1
      self.theOriginalFromId = -1
      self.theOriginalToObject = -1
      self.theOriginalToId = -1
    self.theFromObject = -1
    self.theFromId = -1
    self.theToObject = -1
    self.theToId = -1
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Add'
    
  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = TracePanel.TracePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.TRACE_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,threat):
    self.panel.loadControls(threat)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    self.theFromObject = self.panel.theFromObject
    self.theFromId = self.panel.theFromId
    self.theToObject = self.panel.theToObject
    self.theToId = self.panel.theToId
    self.theFromName = self.panel.theFromName
    self.theToName = self.panel.theToName
    self.EndModal(armid.TRACE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = 0
    if (self.theOriginalFromObject == -1):
      parameters = TraceParameters.TraceParameters(self.theFromObject,self.theFromId,self.theToObject,self.theToId,self.theFromName,self.theToName)
    else:
      parameters = UpdateTraceParameters.UpdateTraceParameters(self.theFromObject,self.theFromId,self.theToObject,self.theToId,self.theFromName,self.theToName,self.theOriginalFromId,self.theOriginalToId)
    parameters.setId(-1)
    return parameters
