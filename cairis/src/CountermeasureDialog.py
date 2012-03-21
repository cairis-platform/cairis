#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasureDialog.py $ $Id: CountermeasureDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from CountermeasureParameters import CountermeasureParameters
from CountermeasurePanel import CountermeasurePanel

class CountermeasureDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(1000,600))

    self.theCountermeasureId = -1
    self.panel = 0
    self.buildControls(parameters)

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = CountermeasurePanel(self)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.COUNTERMEASURE_BUTTONCOMMIT_ID,self.onCommit)


  def load(self,countermeasure):
    self.theCountermeasureId = countermeasure.id()
    self.panel.loadControls(countermeasure)

  def onCommit(self,evt):
    if (self.panel.commit() != -1):
      self.EndModal(armid.COUNTERMEASURE_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = self.panel.parameters()
    parameters.setId(self.theCountermeasureId)
    return parameters
