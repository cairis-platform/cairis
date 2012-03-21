#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskEnvironmentPanel.py $ $Id: TaskEnvironmentPanel.py 532 2011-11-17 15:47:35Z shaf $
import wx
import armid
from EnvironmentListCtrl import EnvironmentListCtrl
from TaskEnvironmentProperties import TaskEnvironmentProperties
from TaskEnvironmentNotebook import TaskEnvironmentNotebook

class TaskEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.TASK_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theTaskId = None
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.TASK_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbBoxSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    environmentDimSizer.Add(nbBoxSizer,1,wx.EXPAND)
    self.notebook = TaskEnvironmentNotebook(self,self.dbProxy)
    nbBoxSizer.Add(self.notebook,1,wx.EXPAND)

    self.dependenciesCtrl = self.notebook.FindWindowById(armid.TASK_TEXTDEPENDENCIES_ID)
    self.personaList = self.notebook.FindWindowById(armid.TASK_LISTPERSONAS_ID)
    self.assetList = self.notebook.FindWindowById(armid.TASK_LISTASSETS_ID)
    self.caList = self.notebook.FindWindowById(armid.TASK_LISTCONCERNASSOCIATIONS_ID)
    self.narrativeCtrl = self.notebook.FindWindowById(armid.TASK_TEXTNARRATIVE_ID)
    self.consequencesCtrl = self.notebook.FindWindowById(armid.TASK_TEXTCONSEQUENCES_ID)
    self.benefitsCtrl = self.notebook.FindWindowById(armid.TASK_TEXTBENEFITS_ID)

    self.SetSizer(mainSizer)

    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)
    self.dependenciesCtrl.Disable()
    self.personaList.Disable() 
    self.assetList.Disable() 
    self.caList.Disable()
    self.narrativeCtrl.Disable()
    self.consequencesCtrl.Disable()
    self.benefitsCtrl.Disable()

    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.DIMLIST_MENUADD_ID,'Add Goal')
    self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.DIMLIST_MENUADD_ID,self.onAddGoal)

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddGoal(self,evt):
    print 'goal'



  def loadControls(self,task):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    self.theTaskId = task.id()
    environmentNames = []
    for cp in task.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in task.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]

    self.dependenciesCtrl.SetValue(p.dependencies())
    self.personaList.setEnvironment(environmentName)
    self.assetList.setEnvironment(environmentName)
    self.caList.setEnvironment(environmentName)   
    self.narrativeCtrl.setEnvironment(environmentName)
    self.personaList.load(p.personas()) 
    self.assetList.load(p.assets()) 
    self.caList.load(p.concernAssociations()) 
    self.narrativeCtrl.SetValue(p.narrative())
    self.consequencesCtrl.SetValue(p.consequences())
    self.benefitsCtrl.SetValue(p.benefits())

    self.environmentList.Select(0)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.dependenciesCtrl.Enable()
    self.personaList.Enable() 
    self.assetList.Enable() 
    self.caList.Enable()
    self.narrativeCtrl.Enable()
    self.consequencesCtrl.Enable()
    self.benefitsCtrl.Enable()
    self.theSelectedIdx = 0
    self.narrativeCtrl.setTask(task.name())

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]

    self.dependenciesCtrl.SetValue(p.dependencies())
    self.personaList.setEnvironment(environmentName)
    self.assetList.setEnvironment(environmentName)
    self.caList.setEnvironment(environmentName)
    self.personaList.load(p.personas()) 
    self.assetList.load(p.assets()) 
    self.caList.load(p.concernAssociations()) 
    self.narrativeCtrl.SetValue(p.narrative())
    self.consequencesCtrl.SetValue(p.consequences())
    self.benefitsCtrl.SetValue(p.benefits())
    self.dependenciesCtrl.Enable()
    self.personaList.Enable() 
    self.assetList.Enable() 
    self.caList.Enable()
    self.narrativeCtrl.Enable()
    self.consequencesCtrl.Enable()
    self.benefitsCtrl.Enable()
    self.narrativeCtrl.setEnvironment(environmentName)

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = TaskEnvironmentProperties(environmentName,self.dependenciesCtrl.GetValue(),self.personaList.dimensions(),self.assetList.dimensions(),self.caList.dimensions(),self.narrativeCtrl.GetValue(),self.consequencesCtrl.GetValue(),self.benefitsCtrl.GetValue())
    self.dependenciesCtrl.SetValue('')
    self.personaList.setEnvironment('')
    self.assetList.setEnvironment('')
    self.caList.setEnvironment('')
    self.narrativeCtrl.setEnvironment('')
    self.personaList.DeleteAllItems() 
    self.assetList.DeleteAllItems() 
    self.caList.DeleteAllItems() 
    self.narrativeCtrl.SetValue('')
    self.consequencesCtrl.SetValue('')
    self.benefitsCtrl.SetValue('')
    self.theSelectedIdx = -1
    self.dependenciesCtrl.Disable()
    self.personaList.Disable() 
    self.assetList.Disable() 
    self.caList.Disable() 
    self.narrativeCtrl.Disable()
    self.consequencesCtrl.Disable()
    self.benefitsCtrl.Disable()

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = TaskEnvironmentProperties(environmentName)
    self.environmentList.Select(self.theSelectedIdx)
    self.personaList.setEnvironment(environmentName)
    self.assetList.setEnvironment(environmentName)
    self.caList.setEnvironment(environmentName)
    self.narrativeCtrl.setEnvironment(environmentName)
    self.personaList.DeleteAllItems() 
    self.assetList.DeleteAllItems() 
    self.caList.DeleteAllItems() 
    self.dependenciesCtrl.SetValue('')
    self.narrativeCtrl.SetValue('')
    self.consequencesCtrl.SetValue('')
    self.benefitsCtrl.SetValue('')
    self.dependenciesCtrl.Enable()
    self.personaList.Enable() 
    self.assetList.Enable() 
    self.caList.Enable() 
    self.narrativeCtrl.Enable()
    self.consequencesCtrl.Enable()
    self.benefitsCtrl.Enable()
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theTaskId != None):
      p = self.dbProxy.inheritedTaskProperties(self.theTaskId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.dependenciesCtrl.SetValue(p.dependencies())
      self.personaList.setEnvironment(environmentName)
      self.assetList.setEnvironment(environmentName)
      self.caList.setEnvironment(environmentName)
      self.narrativeCtrl.setEnvironment(environmentName)
      self.personaList.load(p.personas()) 
      self.assetList.load(p.assets()) 
      self.caList.load(p.concernAssociations()) 
      self.narrativeCtrl.SetValue(p.narrative())
      self.consequencesCtrl.SetValue(p.consequences())
      self.benefitsCtrl.SetValue(p.benefits())
      self.dependenciesCtrl.Enable()
      self.personaList.Enable() 
      self.assetList.Enable() 
      self.caList.Enable() 
      self.narrativeCtrl.Enable()
      self.consequencesCtrl.Enable()
      self.benefitsCtrl.Enable()

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.dependenciesCtrl.SetValue('')
    self.personaList.setEnvironment('')
    self.assetList.setEnvironment('')
    self.caList.setEnvironment('')
    self.narrativeCtrl.setEnvironment('')
    self.personaList.DeleteAllItems() 
    self.assetList.DeleteAllItems() 
    self.caList.DeleteAllItems() 
    self.narrativeCtrl.SetValue('')
    self.consequencesCtrl.SetValue('')
    self.benefitsCtrl.SetValue('')
    self.dependenciesCtrl.Disable()
    self.personaList.Disable() 
    self.assetList.Disable() 
    self.caList.Disable() 
    self.narrativeCtrl.Disable()
    self.consequencesCtrl.Disable()
    self.benefitsCtrl.Disable()


  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = TaskEnvironmentProperties(environmentName,self.dependenciesCtrl.GetValue(),self.personaList.dimensions(),self.assetList.dimensions(),self.caList.dimensions(),self.narrativeCtrl.GetValue(),self.consequencesCtrl.GetValue(),self.benefitsCtrl.GetValue())
    return self.theEnvironmentDictionary.values() 
