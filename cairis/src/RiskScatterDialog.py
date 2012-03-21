#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RiskScatterDialog.py $ $Id: RiskScatterDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from RiskScatterPanel import RiskScatterPanel

class RiskScatterDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,-1,'View Risk Scatter',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,525))
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = RiskScatterPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
