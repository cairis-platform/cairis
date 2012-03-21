#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasureTaskListCtrl.py $ $Id: CountermeasureTaskListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid

class CountermeasureTaskListCtrl(wx.ListCtrl):
  def __init__(self,parent,dp):
    wx.ListCtrl.__init__(self,parent,armid.COUNTERMEASURE_LISTTASKS_ID,size=wx.DefaultSize,style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    self.dbProxy = dp
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Task')
    self.SetColumnWidth(0,150)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName

  def load(self,dims):
    self.DeleteAllItems()
    for idx,dim in enumerate(dims):
      self.InsertStringItem(idx,str(dim))

  def dimensions(self):
    dimList = []
    for x in range(self.GetItemCount()):
      dimList.append(self.GetItemText(x))
    return dimList
