#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ExposedCountermeasureDialog.py $ $Id: ExposedCountermeasureDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from ExposedCountermeasurePanel import ExposedCountermeasurePanel

class ExposedCountermeasureDialog(wx.Dialog):
  def __init__(self,parent,vulCms = []):
    wx.Dialog.__init__(self,parent,armid.EXPOSEDCOUNTERMEASURE_ID,'Exposed countermeasures',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ExposedCountermeasurePanel(self,vulCms)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizerAndFit(mainSizer)
    wx.EVT_BUTTON(self,armid.EXPOSEDCOUNTERMEASURE_BUTTONCOMMIT_ID,self.onCommit)


  def onCommit(self,evt):
    self.EndModal(armid.EXPOSEDCOUNTERMEASURE_BUTTONCOMMIT_ID)

  def countermeasureEffectiveness(self): return self.panel.countermeasureEffectiveness()
