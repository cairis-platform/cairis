#$URL$ $Id: UseCaseEnvironmentPanel.py 449 2011-03-22 12:40:04Z shaf $

import wx
import armid
from Borg import Borg
from EnvironmentListCtrl import EnvironmentListCtrl
from UseCaseEnvironmentNotebook import UseCaseEnvironmentNotebook
from UseCaseEnvironmentProperties import UseCaseEnvironmentProperties

class UseCaseEnvironmentPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.USECASE_PANELENVIRONMENT_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theUseCaseId = None
    self.theUseCaseName = ''
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.USECASE_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbBoxSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    environmentDimSizer.Add(nbBoxSizer,1,wx.EXPAND)
    self.notebook = UseCaseEnvironmentNotebook(self,self.dbProxy)
    nbBoxSizer.Add(self.notebook,1,wx.EXPAND)

    self.preCondCtrl = self.notebook.FindWindowById(armid.USECASE_TEXTPRECONDITION_ID)
    self.postCondCtrl = self.notebook.FindWindowById(armid.USECASE_TEXTPOSTCONDITION_ID)
    self.stepsCtrl = self.notebook.FindWindowById(armid.USECASE_PANELFLOW_ID)

    self.SetSizer(mainSizer)

    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)
    self.preCondCtrl.Disable()
    self.stepsCtrl.Disable() 
    self.postCondCtrl.Disable() 
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)


  def loadControls(self,uc):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    self.theUseCaseId = uc.id()
    self.theUseCaseName = uc.name()
    environmentNames = []
    for cp in uc.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in uc.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]

    self.preCondCtrl.SetValue(p.preconditions())
    self.stepsCtrl.reloadSteps(p.steps())
    self.stepsCtrl.setUseCase(self.theUseCaseName)
    self.postCondCtrl.SetValue(p.postconditions())
    self.stepsCtrl.setEnvironment(environmentName)
    self.preCondCtrl.setEnvironment(environmentName)
    self.preCondCtrl.setUseCase(self.theUseCaseName)
    self.postCondCtrl.setEnvironment(environmentName)
    self.postCondCtrl.setUseCase(self.theUseCaseName)

    self.environmentList.Select(0)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.preCondCtrl.Enable()
    self.stepsCtrl.Enable() 
    self.postCondCtrl.Enable()
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]

    self.preCondCtrl.SetValue(p.preconditions())
    self.stepsCtrl.reloadSteps(p.steps())
    self.postCondCtrl.SetValue(p.postconditions())
    self.stepsCtrl.setEnvironment(environmentName)
    self.preCondCtrl.setEnvironment(environmentName)
    self.preCondCtrl.setUseCase(self.theUseCaseName)
    self.postCondCtrl.setEnvironment(environmentName)
    self.postCondCtrl.setUseCase(self.theUseCaseName)
    self.preCondCtrl.Enable()
    self.stepsCtrl.Enable() 
    self.postCondCtrl.Enable()


  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = UseCaseEnvironmentProperties(environmentName,self.preCondCtrl.GetValue(),self.stepsCtrl.steps(),self.postCondCtrl.GetValue())
    self.preCondCtrl.SetValue('')
    self.stepsCtrl.clear()
    self.stepsCtrl.setEnvironment('')
    self.postCondCtrl.SetValue('')
    self.preCondCtrl.setEnvironment('')
    self.preCondCtrl.setUseCase('')
    self.postCondCtrl.setEnvironment('')
    self.postCondCtrl.setUseCase('')
    self.theSelectedIdx = -1
    self.preCondCtrl.Disable()
    self.stepsCtrl.Disable()
    self.postCondCtrl.Disable() 

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = UseCaseEnvironmentProperties(environmentName)
    self.environmentList.Select(self.theSelectedIdx)
    self.preCondCtrl.SetValue('')
    self.stepsCtrl.setEnvironment(environmentName)
    self.stepsCtrl.clear()
    self.postCondCtrl.SetValue('')
    self.preCondCtrl.setEnvironment(environmentName)
    self.preCondCtrl.setUseCase(self.theUseCaseName)
    self.postCondCtrl.setEnvironment(environmentName)
    self.postCondCtrl.setUseCase(self.theUseCaseName)
    inheritedEnv = self.environmentList.inheritedEnvironment()
    if (inheritedEnv != '' and self.theUseCaseId != None):
      p = self.dbProxy.inheritedUseCaseProperties(self.theUseCaseId,inheritedEnv)
      self.theEnvironmentDictionary[environmentName] = p
      self.preCondCtrl.SetValue(p.preconditions())
      self.stepsCtrl.reloadSteps(p.steps())
      self.stepsCtrl.setEnvironment(environmentName)
      self.postCondCtrl.SetValue(p.preconditions())
      self.preCondCtrl.setEnvironment(environmentName)
      self.preCondCtrl.setUseCase(self.theUseCaseName)
      self.postCondCtrl.setEnvironment(environmentName)
      self.postCondCtrl.setUseCase(self.theUseCaseName)
    self.preCondCtrl.Enable()
    self.stepsCtrl.Enable()
    self.postCondCtrl.Enable()

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.preCondCtrl.SetValue('')
    self.stepsCtrl.clear()
    self.stepsCtrl.setEnvironment('')
    self.postCondCtrl.SetValue('')
    self.preCondCtrl.setEnvironment('')
    self.preCondCtrl.setUseCase('')
    self.postCondCtrl.setEnvironment('')
    self.postCondCtrl.setUseCase('')
    self.preCondCtrl.Disable()
    self.stepsCtrl.Disable()
    self.postCondCtrl.Disable()


  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = UseCaseEnvironmentProperties(environmentName,self.preCondCtrl.GetValue(),self.stepsCtrl.steps(),self.postCondCtrl.GetValue())
    return self.theEnvironmentDictionary.values() 
