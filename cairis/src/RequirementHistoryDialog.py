#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementHistoryDialog.py $ $Id: RequirementHistoryDialog.py 564 2012-03-12 17:53:00Z shaf $
import wx
import armid

class RequirementHistoryDialog(wx.Dialog):
  def __init__(self,parent,history):
    wx.Dialog.__init__(self,parent,armid.REQUIREMENTHISTORY_ID,'Requirement History',style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX,size=(1000,300))
    self.theId = -1
    self.panel = wx.Panel(self,-1)
    panelSizer = wx.BoxSizer(wx.VERTICAL)
    reqList = wx.ListCtrl(self,-1,style=wx.LC_REPORT)
    reqList.InsertColumn(0,'Version')
    reqList.SetColumnWidth(0,50)
    reqList.InsertColumn(1,'Label')
    reqList.SetColumnWidth(1,50)
    reqList.InsertColumn(2,'Name')
    reqList.SetColumnWidth(2,75)
    reqList.InsertColumn(3,'Description')
    reqList.SetColumnWidth(3,150)
    reqList.InsertColumn(4,'Priority')
    reqList.SetColumnWidth(4,50)
    reqList.InsertColumn(5,'Rationale')
    reqList.SetColumnWidth(5,150)
    reqList.InsertColumn(6,'Fit Criterion')
    reqList.SetColumnWidth(6,150)
    reqList.InsertColumn(7,'Originator')
    reqList.SetColumnWidth(7,100)
    reqList.InsertColumn(8,'Type')
    reqList.SetColumnWidth(8,100)
    reqList.InsertColumn(9,'Rev. Date')
    reqList.SetColumnWidth(9,150)
 
    for version,label,name,desc,priority,rationale,fitCriterion,originator,reqType,revDate in history:
      idx = reqList.GetItemCount()
      reqList.InsertStringItem(idx,str(version))
      reqList.SetStringItem(idx,1,str(label))
      reqList.SetStringItem(idx,2,name)
      reqList.SetStringItem(idx,3,desc)
      reqList.SetStringItem(idx,4,str(priority))
      reqList.SetStringItem(idx,5,rationale)
      reqList.SetStringItem(idx,6,fitCriterion)
      reqList.SetStringItem(idx,7,originator)
      reqList.SetStringItem(idx,8,reqType)
      reqList.SetStringItem(idx,9,revDate)

    panelSizer.Add(reqList,1,wx.EXPAND)
    self.panel.SetSizer(panelSizer)
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
