#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskDialog.py $ $Id: TaskDialog.py 572 2012-03-16 21:37:33Z shaf $
import wx
import armid
from TaskParameters import TaskParameters
from TaskPanel import TaskPanel
from BaseDialog import BaseDialog
from TaskEnvironmentProperties import TaskEnvironmentProperties
from Borg import Borg

class TaskDialog(BaseDialog):
  def __init__(self,parent,parameters):
    BaseDialog.__init__(self,parent,parameters.id(),parameters.label(),(700,800))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theTaskId = -1
    self.theName = ''
    self.theShortCode = ''
    self.theObjective = ''
    self.isAssumption = False
    self.theAuthor = ''
    self.theEnvironmentProperties = []
    self.panel = 0
    self.buildControls(parameters)
    self.theCommitVerb = 'Create'

  def buildControls(self,parameters):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = TaskPanel(self,self.dbProxy)
    self.panel.buildControls(parameters.createFlag())
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.TASK_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,task):
    self.theTaskId = task.id()
    self.panel.loadControls(task)
    self.theCommitVerb = 'Edit'

  def onCommit(self,evt):
    nameCtrl = self.FindWindowById(armid.TASK_TEXTNAME_ID)
    shortCodeCtrl = self.FindWindowById(armid.TASK_TEXTSHORTCODE_ID)
    authorCtrl = self.FindWindowById(armid.TASK_TEXTAUTHOR_ID)
    objectiveCtrl = self.FindWindowById(armid.TASK_TEXTOBJECTIVE_ID)
    assumptionCtrl = self.FindWindowById(armid.TASK_CHECKASSUMPTION_ID)
    environmentCtrl = self.FindWindowById(armid.TASK_PANELENVIRONMENT_ID)

    self.theName = nameCtrl.GetValue()
    self.theShortCode = shortCodeCtrl.GetValue()
    self.theAuthor = authorCtrl.GetValue()
    self.isAssumption = assumptionCtrl.GetValue()
    self.theObjective = objectiveCtrl.GetValue()
    self.theEnvironmentProperties = environmentCtrl.environmentProperties()
    commitLabel = self.theCommitVerb +  ' Task' 

    if (len(self.theName) == 0):
      dlg = wx.MessageDialog(self,'Name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theShortCode) == 0):
      dlg = wx.MessageDialog(self,'Short Code cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAuthor) == 0):
      dlg = wx.MessageDialog(self,'Author cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theObjective) == 0):
      dlg = wx.MessageDialog(self,'Objective cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      for environmentProperties in self.theEnvironmentProperties:
        if len(environmentProperties.personas()) == 0:
          errorTxt = 'No personas defined in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.dependencies()) == 0:
          errorTxt = 'No dependencies defined in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
        if len(environmentProperties.narrative()) == 0:
          errorTxt = 'No narrative defined in environment ' + environmentProperties.name()
          dlg = wx.MessageDialog(self,errorTxt,commitLabel,wx.OK) 
          dlg.ShowModal()
          dlg.Destroy()
          return
    self.EndModal(armid.TASK_BUTTONCOMMIT_ID)

  def parameters(self): 
    parameters = TaskParameters(self.theName,self.theShortCode,self.theObjective,self.isAssumption,self.theAuthor,self.theEnvironmentProperties)
    parameters.setId(self.theTaskId)
    return parameters
