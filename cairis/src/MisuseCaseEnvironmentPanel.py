#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCaseEnvironmentPanel.py $ $Id: MisuseCaseEnvironmentPanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from EnvironmentListCtrl import EnvironmentListCtrl
from MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from MisuseCaseNotebook import MisuseCaseNotebook


class MisuseCaseEnvironmentPanel(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent,armid.MISUSECASE_PANELENVIRONMENT_ID)
    self.dbProxy = dp
    self.theEnvironmentDictionary = {}
    self.theSelectedIdx = -1
    self.theSelectedRisk = ''
    self.theSelectedThreat = ''
    self.theSelectedVulnerability = ''

    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    environmentBox = wx.StaticBox(self)
    environmentListSizer = wx.StaticBoxSizer(environmentBox,wx.HORIZONTAL)
    mainSizer.Add(environmentListSizer,0,wx.EXPAND)
    self.environmentList = EnvironmentListCtrl(self,armid.MISUSECASE_LISTENVIRONMENTS_ID,self.dbProxy)
    self.environmentList.Unbind(wx.EVT_RIGHT_DOWN)
    environmentListSizer.Add(self.environmentList,1,wx.EXPAND)
    environmentDimSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(environmentDimSizer,1,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    environmentDimSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = MisuseCaseNotebook(self)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.SetSizer(mainSizer)

    self.objectiveCtrl = self.notebook.FindWindowById(armid.MISUSECASE_TEXTOBJECTIVE_ID)
    self.attackerList = self.notebook.FindWindowById(armid.MISUSECASE_LISTATTACKERS_ID)
    self.assetList = self.notebook.FindWindowById(armid.MISUSECASE_LISTASSETS_ID)
    self.threatCtrl = self.notebook.FindWindowById(armid.MISUSECASE_TEXTTHREAT_ID)
    self.lhoodCtrl = self.notebook.FindWindowById(armid.MISUSECASE_TEXTLIKELIHOOD_ID)
    self.vulCtrl = self.notebook.FindWindowById(armid.MISUSECASE_TEXTVULNERABILITY_ID)
    self.sevCtrl = self.notebook.FindWindowById(armid.MISUSECASE_TEXTSEVERITY_ID)
    self.ratingCtrl = self.notebook.FindWindowById(armid.MISUSECASE_TEXTSCORE_ID)
    self.narrativeCtrl = self.notebook.FindWindowById(armid.MISUSECASE_TEXTNARRATIVE_ID)


    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)

    self.narrativeCtrl.Disable()



  def unloadMCComponents(self):
    self.ratingCtrl.SetValue('')
    self.threatCtrl.SetValue('')
    self.lhoodCtrl.SetValue('')
    self.vulCtrl.SetValue('')
    self.sevCtrl.SetValue('')
    self.attackerList.DeleteAllItems()
    self.assetList.DeleteAllItems()
    self.objectiveCtrl.SetValue('')
    

  def loadMCComponents(self): 
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.ratingCtrl.SetValue(self.dbProxy.riskRating(self.theSelectedThreat,self.theSelectedVulnerability,environmentName) )

    self.threatCtrl.SetValue(self.theSelectedThreat)
    threatId = self.dbProxy.getDimensionId(self.theSelectedThreat,'threat')
    environmentId = self.dbProxy.getDimensionId(environmentName,'environment')
    self.lhoodCtrl.SetValue(self.dbProxy.threatLikelihood(threatId,environmentId))

    self.vulCtrl.SetValue(self.theSelectedVulnerability)
    vulId = self.dbProxy.getDimensionId(self.theSelectedVulnerability,'vulnerability')
    self.sevCtrl.SetValue(self.dbProxy.vulnerabilitySeverity(vulId,environmentId))

    self.attackerList.DeleteAllItems()
    attackers = self.dbProxy.threatAttackers(threatId,environmentId)
    attackerSet = set(attackers)
    for atidx,attacker in enumerate(attackerSet):
      self.attackerList.InsertStringItem(atidx,attacker)

    
    threatenedAssets = self.dbProxy.threatenedAssets(threatId,environmentId)
    vulnerableAssets = self.dbProxy.vulnerableAssets(vulId,environmentId)

    objectiveText = 'Exploit vulnerabilities in '
    for idx,vulAsset in enumerate(vulnerableAssets):
      objectiveText += vulAsset
      if (idx != (len(vulnerableAssets) -1)):
        objectiveText += ','
    objectiveText += ' to threaten '
    for idx,thrAsset in enumerate(threatenedAssets):
      objectiveText += thrAsset
      if (idx != (len(threatenedAssets) -1)):
        objectiveText += ','
    objectiveText += '.'
    self.objectiveCtrl.SetValue(objectiveText)

    self.assetList.DeleteAllItems()
    assetSet = set(threatenedAssets + vulnerableAssets)
    for asidx,asset in enumerate(assetSet):
      self.assetList.InsertStringItem(asidx,asset)


  def loadMisuseCase(self,mc):
    self.theSelectedRisk = mc.risk()
    self.theSelectedThreat = mc.threat()
    self.theSelectedVulnerability = mc.vulnerability()

    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    environmentNames = []
    for cp in mc.environmentProperties():
      environmentNames.append(cp.name())
    self.environmentList.load(environmentNames)

    for cp in mc.environmentProperties():
      environmentName = cp.name()
      self.theEnvironmentDictionary[environmentName] = cp
      environmentNames.append(environmentName) 
    environmentName = environmentNames[0]
    p = self.theEnvironmentDictionary[environmentName]

    self.narrativeCtrl.SetValue(p.narrative())
    self.environmentList.Select(0)
    self.loadMCComponents()
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.narrativeCtrl.Enable()
    self.theSelectedIdx = 0

  def loadRiskComponents(self,threatName,vulName):
    self.theSelectedThreat = threatName
    self.theSelectedVulnerability = vulName
    self.environmentList.Unbind(wx.EVT_LIST_INSERT_ITEM)
    self.environmentList.Unbind(wx.EVT_LIST_DELETE_ITEM)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_SELECTED)
    self.environmentList.Unbind(wx.EVT_LIST_ITEM_DESELECTED)
    environments = self.dbProxy.threatVulnerabilityEnvironmentNames(threatName,vulName)
    for environmentName in environments:
      self.theEnvironmentDictionary[environmentName] = MisuseCaseEnvironmentProperties(environmentName)
    self.environmentList.load(environments)
    self.environmentList.Select(0)
    self.theSelectedIdx = 0
    self.loadMCComponents()
    self.environmentList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnEnvironmentSelected)
    self.environmentList.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnEnvironmentDeselected)
    self.environmentList.Bind(wx.EVT_LIST_INSERT_ITEM,self.OnAddEnvironment)
    self.environmentList.Bind(wx.EVT_LIST_DELETE_ITEM,self.OnDeleteEnvironment)


  def OnEnvironmentSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    p = self.theEnvironmentDictionary[environmentName]
    self.narrativeCtrl.SetValue(p.narrative())
    self.loadMCComponents()
    self.narrativeCtrl.Enable()

  def OnEnvironmentDeselected(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = MisuseCaseEnvironmentProperties(environmentName,self.narrativeCtrl.GetValue())
    self.narrativeCtrl.SetValue('')
    self.narrativeCtrl.Disable()
    self.unloadMCComponents()

  def OnAddEnvironment(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
    self.theEnvironmentDictionary[environmentName] = MisuseCaseEnvironmentProperties(environmentName)
    self.environmentList.Select(self.theSelectedIdx)
    self.loadMCComponents()
    self.narrativeCtrl.Enable()

  def OnDeleteEnvironment(self,evt):
    selectedIdx = evt.GetIndex()
    environmentName = self.environmentList.GetItemText(selectedIdx)
    del self.theEnvironmentDictionary[environmentName]
    self.theSelectedIdx = -1
    self.narrativeCtrl.SetValue('')
    self.narrativeCtrl.Disable()
    self.unloadMCComponents()


  def environmentProperties(self):
    if (self.theSelectedIdx != -1):
      environmentName = self.environmentList.GetItemText(self.theSelectedIdx)
      self.theEnvironmentDictionary[environmentName] = MisuseCaseEnvironmentProperties(environmentName,self.narrativeCtrl.GetValue())
    return self.theEnvironmentDictionary.values() 
