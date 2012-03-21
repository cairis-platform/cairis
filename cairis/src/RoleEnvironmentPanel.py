#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleEnvironmentPanel.py $ $Id: RoleEnvironmentPanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from DimensionListCtrl import DimensionListCtrl
from RoleEnvironmentProperties import RoleEnvironmentProperties
from DimensionCostListCtrl import DimensionCostListCtrl


class RoleEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.ROLE_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = DimensionListCtrl(self,armid.ROLE_LISTENVIRONMENTS_ID,wx.DefaultSize,'Environment','environment',self.dbProxy,listStyle=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)

    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    rSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentDimSizer.Add(rSizer,1,wx.EXPAND)
    self.responseList = DimensionCostListCtrl(self,armid.ROLE_LISTRESPONSES_ID,'Response')
    responseBox = wx.StaticBox(self)
    responseSizer = wx.StaticBoxSizer(responseBox,wx.HORIZONTAL)
    responseSizer.Add(self.responseList,1,wx.EXPAND)
    rSizer.Add(responseSizer,1,wx.EXPAND)

    cSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentDimSizer.Add(cSizer,1,wx.EXPAND)
    self.cmList = DimensionListCtrl(self,armid.ROLE_LISTCOUNTERMEASURES_ID,wx.DefaultSize,'Countermeasure','countermeasure',self.dbProxy,listStyle = wx.LC_REPORT | wx.LC_SINGLE_SEL)
    cmBox = wx.StaticBox(self)
    cmSizer = wx.StaticBoxSizer(cmBox,wx.HORIZONTAL)
    cmSizer.Add(self.cmList,1,wx.EXPAND)
    cSizer.Add(cmSizer,1,wx.EXPAND)

    self.SetSizer(mainSizer)
    self.environmentList.Unbind(wx.EVT_RIGHT_DOWN)
    self.responseList.Unbind(wx.EVT_RIGHT_DOWN)
    self.cmList.Unbind(wx.EVT_RIGHT_DOWN)
    
  def loadControls(self,role):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)

# We load the environment name control before anything else.  Weird stuff happens if we don't do this.  Don't ask me why!!!
    environmentNames = []
    for cp in role.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in role.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp

    if (len(environmentNames) > 0):
      environmentName = environmentNames[0]
      p = self.theEnvironmentDictionary[environmentName]
      self.responseList.load(p.responses()) 
      self.cmList.load(p.countermeasures()) 
      self.environmentList.Select(0)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]
    self.responseList.load(p.responses()) 
    self.cmList.load(p.countermeasures())
      
  def OnEnvironmentDeselected(self,evt):
    self.responseList.DeleteAllItems() 
    self.cmList.DeleteAllItems() 
    self.theSelectedIdx = -1
