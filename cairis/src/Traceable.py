#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Traceable.py $ $Id: Traceable.py 567 2012-03-13 22:31:40Z shaf $
import armid
import ARM
import wx
from Borg import Borg
from TraceExplorer import TraceExplorer

class Traceable:
  def __init__(self):
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTraceMenu = wx.Menu()
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_TO_ID,'Supported by')
    self.theTraceMenu.Append(armid.TRACE_MENUTRACE_FROM_ID,'Contributes to')
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_FROM_ID,self.onAddContributionLink)
    wx.EVT_MENU(self,armid.TRACE_MENUTRACE_TO_ID,self.onAddSupportLink)

  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onTraceFrom(self,dimensionName,fromId,envName=''):
    self.onTrace(dimensionName,fromId,True,envName)

  def onTraceTo(self,dimensionName,toId):
    self.onTrace(dimensionName,toId,False,envName)

  def onTrace(self,dimensionName,fromId,isFrom,envName):
    dlg = TraceExplorer(self,dimensionName,isFrom,envName)
    if (dlg.ShowModal() == armid.TRACE_BUTTONADD_ID):
      if (isFrom):
        traceDimension = dlg.fromDimension()
        traceLabel = dlg.label()
        linkTable = dimensionName + '_' + traceDimension
        toId = dlg.toId()
        self.dbProxy.addTrace(linkTable,fromId,toId,traceLabel)
      else: 
        traceDimension = dlg.toDimension()
        traceLabel = dlg.label()
        linkTable = traceDimension + '_' + dimensionName
        toId = dlg.toId()
        self.dbProxy.addTrace(linkTable,toId,fromId,traceLabel)
    dlg.Destroy()
