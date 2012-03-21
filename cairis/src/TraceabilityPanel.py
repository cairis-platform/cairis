#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TraceabilityPanel.py $ $Id: TraceabilityPanel.py 523 2011-11-04 18:07:01Z shaf $
import wx
from BasePanel import BasePanel
from Borg import Borg
import armid

class TraceabilityPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.TRACEABILITY_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.traces = self.dbProxy.riskAnalysisModel(initContxt)

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    columnList = ['From','Name','To','Name']
    mainSizer.Add(self.buildTraceListCtrl(self,armid.TRACEABILITY_LISTTRACES_ID,columnList,self.traces),1,wx.EXPAND)
    mainSizer.Add(self.buildAddDeleteCloseButtonSizer(self,armid.TRACEABILITY_BUTTONADD_ID,armid.TRACEABILITY_BUTTONDELETE_ID,wx.HORIZONTAL),0,wx.EXPAND | wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)
