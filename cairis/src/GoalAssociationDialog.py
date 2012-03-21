#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalAssociationDialog.py $ $Id: GoalAssociationDialog.py 336 2010-11-07 23:08:30Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg
from GoalAssociationParameters import GoalAssociationParameters

class GoalAssociationDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,armid.GOALASSOCIATION_ID,'Goal association',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(600,400))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theGoalAssociationId = -1
    self.theEnvironmentName = ''
    self.theGoal = ''
    self.theGoalDimension = ''
    self.theGoalAssociationType = ''
    self.theSubGoal = ''
    self.theSubGoalDimension = ''
    self.theRationale = 'None.'
    self.theAlternativeFlag = 0
    self.buildControls(parameters)
    self.commitVerb = 'Add'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    associationSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(WidgetFactory.buildCheckSizer(self,'Alternative',armid.GOALASSOCIATION_CHECKALTERNATIVE_ID,False),0,wx.EXPAND)
    mainSizer.Add(associationSizer,0,wx.EXPAND)
    environments = self.dbProxy.getDimensionNames('environment')
    goals = []
    associationTypes = ['and','or','conflict','responsible','obstruct','resolve']
    goalDimensions = ['goal','requirement','countermeasure','obstacle']
    subGoalDimensions = ['goal','requirement','role','task','usecase','countermeasure','domainproperty','obstacle','threat','vulnerability']

    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Environment',(87,30),armid.GOALASSOCIATION_COMBOENVIRONMENT_ID,environments),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Dimension',(87,30),armid.GOALASSOCIATION_COMBOGOALDIM_ID,goalDimensions),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Goal',(87,30),armid.GOALASSOCIATION_COMBOGOAL_ID,goals),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),armid.GOALASSOCIATION_COMBOATYPE_ID,associationTypes),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Dimension',(87,30),armid.GOALASSOCIATION_COMBOSUBGOALDIM_ID,subGoalDimensions),0,wx.EXPAND)
    associationSizer.Add(WidgetFactory.buildComboSizerList(self,'Sub-Goal',(87,30),armid.GOALASSOCIATION_COMBOSUBGOAL_ID,goals),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Rationale',(87,60),armid.GOALASSOCIATION_TEXTRATIONALE_ID),1,wx.EXPAND,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.GOALASSOCIATION_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.GOALASSOCIATION_BUTTONCOMMIT_ID,self.onCommit)
    wx.EVT_COMBOBOX(self,armid.GOALASSOCIATION_COMBOENVIRONMENT_ID,self.onEnvironmentChange)
    wx.EVT_COMBOBOX(self,armid.GOALASSOCIATION_COMBOGOALDIM_ID,self.onGoalDimChange)
    wx.EVT_COMBOBOX(self,armid.GOALASSOCIATION_COMBOSUBGOALDIM_ID,self.onSubGoalDimChange)

  def load(self,association):
    self.theGoalAssociationId = association.id()
    envCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOAL_ID)
    goalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOALDIM_ID)
    atypeCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOATYPE_ID)
    subGoalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOAL_ID)
    subGoalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    alternativeCtrl = self.FindWindowById(armid.GOALASSOCIATION_CHECKALTERNATIVE_ID)
    rationaleCtrl = self.FindWindowById(armid.GOALASSOCIATION_TEXTRATIONALE_ID)
    buttonCtrl = self.FindWindowById(armid.GOALASSOCIATION_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
  
    self.theEnvironmentName = association.environment()
    self.theGoal = association.goal()
    self.theGoalDimension = association.goalDimension()
    self.theGoalAssociationType = association.type()
    self.theSubGoal = association.subGoal()
    self.theSubGoalDimension = association.subGoalDimension()
    self.theAlternativeFlag = association.alternative()
    self.theRationale = association.rationale()


    envCtrl.SetValue(self.theEnvironmentName)
    goalCtrl.SetValue(self.theGoal)
    goalDimCtrl.SetValue(self.theGoalDimension)
    atypeCtrl.SetValue(self.theGoalAssociationType)
    subGoalCtrl.SetValue(self.theSubGoal)
    subGoalDimCtrl.SetValue(self.theSubGoalDimension)
    alternativeCtrl.SetValue(self.theAlternativeFlag)
    rationaleCtrl.SetValue(self.theRationale)
    
    self.commitVerb = 'Edit'
    
  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' association'
    envCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOAL_ID)
    goalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOALDIM_ID)
    atypeCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOATYPE_ID)
    subGoalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOAL_ID)
    subGoalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    alternativeCtrl = self.FindWindowById(armid.GOALASSOCIATION_CHECKALTERNATIVE_ID)
    rationaleCtrl = self.FindWindowById(armid.GOALASSOCIATION_TEXTRATIONALE_ID)

    self.theEnvironmentName = envCtrl.GetValue()
    self.theGoal = goalCtrl.GetValue()
    self.theGoalDimension = goalDimCtrl.GetValue()
    self.theGoalAssociationType = atypeCtrl.GetValue()
    self.theSubGoal = subGoalCtrl.GetValue()
    self.theSubGoalDimension = subGoalDimCtrl.GetValue()
    self.theAlternativeFlag = alternativeCtrl.GetValue()
    self.theRationale = rationaleCtrl.GetValue()

    if (len(self.theRationale) == 0):
      self.theRationale = 'None.'

    if len(self.theEnvironmentName) == 0:
      dlg = wx.MessageDialog(self,'No environment selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoalDimension) == 0:
      dlg = wx.MessageDialog(self,'No goal dimension selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theGoal) == 0:
      dlg = wx.MessageDialog(self,'No goal selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theSubGoalDimension) == 0:
      dlg = wx.MessageDialog(self,'No sub goal dimension selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theSubGoal) == 0:
      dlg = wx.MessageDialog(self,'No sub goal selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theGoalAssociationType) == 0):
      dlg = wx.MessageDialog(self,'No association type selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.GOALASSOCIATION_BUTTONCOMMIT_ID)

  def onEnvironmentChange(self,evt):
    envCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOAL_ID)
    goalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOALDIM_ID)
    atypeCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOATYPE_ID)
    subGoalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOAL_ID)
    subGoalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    alternativeCtrl = self.FindWindowById(armid.GOALASSOCIATION_CHECKALTERNATIVE_ID)
    rationaleCtrl = self.FindWindowById(armid.GOALASSOCIATION_TEXTRATIONALE_ID)
    goalCtrl.SetItems([])
    subGoalCtrl.SetItems([])
    goalCtrl.SetValue('')
    goalDimCtrl.SetValue('')
    atypeCtrl.SetValue('')
    subGoalCtrl.SetValue('')
    subGoalDimCtrl.SetValue('')
    alternativeCtrl.SetValue(0)
    rationaleCtrl.SetValue('')
    envName = envCtrl.GetStringSelection()

  def onGoalDimChange(self,evt):
    envCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOENVIRONMENT_ID)
    goalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOALDIM_ID)
    envName = envCtrl.GetStringSelection()
    goalDimName = goalDimCtrl.GetStringSelection()

    if (envName != '') and (goalDimName != ''):
      goalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOGOAL_ID)
      if (goalDimName == 'goal'):
        goalCtrl.SetItems(self.dbProxy.environmentGoals(envName))
      elif (goalDimName == 'obstacle'):
        goalCtrl.SetItems(self.dbProxy.environmentObstacles(envName))
      elif (goalDimName == 'countermeasure'):
        goalCtrl.SetItems(self.dbProxy.environmentCountermeasures(envName))
      elif (goalDimName == 'requirement'):
        reqDict = self.dbProxy.getRequirements()
        descList = []
        for r in reqDict.values():
          descList.append(r.label())
        goalCtrl.SetItems(descList)


  def onSubGoalDimChange(self,evt):
    envCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOENVIRONMENT_ID)
    subGoalDimCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOALDIM_ID)
    envName = envCtrl.GetStringSelection()
    subGoalDimName = subGoalDimCtrl.GetStringSelection()

    if (envName != '') and (subGoalDimName != ''):
      subGoalCtrl = self.FindWindowById(armid.GOALASSOCIATION_COMBOSUBGOAL_ID)
      if (subGoalDimName == 'goal'):
        subGoalCtrl.SetItems(self.dbProxy.environmentGoals(envName))
      elif (subGoalDimName == 'obstacle'):
        subGoalCtrl.SetItems(self.dbProxy.environmentObstacles(envName))
      elif (subGoalDimName == 'domainproperty'):
        subGoalCtrl.SetItems(self.dbProxy.environmentDomainProperties(envName))
      elif (subGoalDimName == 'task'):
        subGoalCtrl.SetItems(self.dbProxy.environmentTasks(envName))
      elif (subGoalDimName == 'usecase'):
        subGoalCtrl.SetItems(self.dbProxy.environmentUseCases(envName))
      elif (subGoalDimName == 'countermeasure'):
        subGoalCtrl.SetItems(self.dbProxy.environmentCountermeasures(envName))
      elif (subGoalDimName == 'requirement'):
        reqDict = self.dbProxy.getRequirements()
        descList = []
        for r in reqDict.values():
          descList.append(r.label())
        subGoalCtrl.SetItems(descList)
      elif (subGoalDimName == 'role'):
        roleDict = self.dbProxy.getRoles()
        descList = []
        for r in roleDict.values():
          descList.append(r.name())
        subGoalCtrl.SetItems(descList)


  def parameters(self):
    parameters = GoalAssociationParameters(self.theEnvironmentName,self.theGoal,self.theGoalDimension,self.theGoalAssociationType,self.theSubGoal,self.theSubGoalDimension,self.theAlternativeFlag,self.theRationale)
    parameters.setId(self.theGoalAssociationId)
    return parameters
