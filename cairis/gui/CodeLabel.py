import wx
from cairis.core.Borg import Borg

class CodeLabel(wx.StaticText):
  def __init__(self,parent,winId,lblTxt):
    wx.StaticText.__init__(self,parent,winId,lblTxt)
