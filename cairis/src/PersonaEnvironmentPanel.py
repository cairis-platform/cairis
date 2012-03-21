#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaEnvironmentPanel.py $ $Id: PersonaEnvironmentPanel.py 265 2010-06-21 22:20:07Z shaf $
import wx
import armid
from PersonaEnvironmentProperties import PersonaEnvironmentProperties
from PersonaEnvironmentNotebook import PersonaEnvironmentNotebook
from EnvironmentListCtrl import EnvironmentListCtrl

class PersonaEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.PERSONA_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1
    self.thePersonaName = ''

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.PERSONA_LISTENVIRONMENTS_ID,self.dbProxy)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.HORIZONTAL)
    environmentDimSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = PersonaEnvironmentNotebook(self,self.dbProxy)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.SetSizer(mainSizer)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)

    self.directCtrl = self.notebook.FindWindowById(armid.PERSONA_CHECKDIRECT_ID)
    self.roleList = self.notebook.FindWindowById(armid.PERSONA_LISTROLES_ID)
    self.descriptionCtrl = self.notebook.FindWindowById(armid.PERSONA_TEXTNARRATIVE_ID)
    self.directCtrl.Disable()
    self.descriptionCtrl.Disable()
    self.roleList.Disable() 


  def loadControls(self,persona):
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    self.thePersonaName = persona.name()
    environmentNames = []
    for cp in persona.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in persona.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]

    if (p.directFlag() == 'True'):
      self.directCtrl.SetValue(True)
    else:
      self.directCtrl.SetValue(False)
    self.descriptionCtrl.Set(self.thePersonaName,'Environment Narrative',p.narrative())
    self.roleList.setEnvironment(environmentName)
    self.roleList.load(p.roles()) 

    self.environmentList.Select(0)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.directCtrl.Enable()
    self.descriptionCtrl.Enable()
    self.roleList.Enable() 
    self.theSelectedIdx = 0

  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]

    if (p.directFlag() == 'True'):
      self.directCtrl.SetValue(True)
    else:
      self.directCtrl.SetValue(False)
    self.descriptionCtrl.Set(self.thePersonaName,'Environment Narrative',p.narrative())
    self.roleList.setEnvironment(environmentName)
    self.roleList.load(p.roles()) 
    self.directCtrl.Enable()
    self.descriptionCtrl.Enable()
    self.roleList.Enable() 

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = PersonaEnvironmentProperties(environmentName,str(self.directCtrl.GetValue()),self.descriptionCtrl.GetValue(),self.roleList.dimensions())

    self.directCtrl.SetValue(False)
    self.descriptionCtrl.Set(self.thePersonaName,'Environment Narrative','')
    self.roleList.setEnvironment('')
    self.roleList.DeleteAllItems() 
    self.theSelectedIdx = -1
    self.directCtrl.Disable()
    self.descriptionCtrl.Disable()
    self.roleList.Disable() 

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = PersonaEnvironmentProperties(environmentName)
    self.environmentList.Select(self.theSelectedIdx)
    self.directCtrl.SetValue(False)
    self.descriptionCtrl.Set(self.thePersonaName,'Environment Narrative','')
    self.roleList.setEnvironment(environmentName)
    self.roleList.DeleteAllItems() 
    self.directCtrl.Enable()
    self.descriptionCtrl.Enable()
    self.roleList.Enable() 

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.directCtrl.SetValue(False)
    self.descriptionCtrl.Set(self.thePersonaName,'Environment Narrative','')
    self.roleList.setEnvironment('')
    self.roleList.DeleteAllItems() 
    self.theSelectedIdx = -1
    self.directCtrl.Disable()
    self.descriptionCtrl.Disable()
    self.roleList.Disable() 


  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = PersonaEnvironmentProperties(environmentName,str(self.directCtrl.GetValue()),self.descriptionCtrl.GetValue(),self.roleList.dimensions())
    return self.theEnvironmentDictionary.values() 
